# Codex 圖片執行環境

## 1. 正式架構

Codex 只是 image renderer，永遠不是 orchestrator。

```text
AGY
  -> codex_image_adapter.py
  -> Codex CLI 已登入 ChatGPT/Codex session   codex exec --json --skip-git-repo-check
  -> $imagegen skill
  -> built-in image_gen tool
  -> $CODEX_HOME/generated_images/<thread_id>/<artifact>.png
  -> 驗證 + copy 進 workspace output path
  -> structured result
  -> AGY
```

禁止：

```text
AGY -> Codex API        (付費 Images API / OPENAI_API_KEY)
Codex -> Kiro           (Codex 不得呼叫工程 worker)
Codex -> outline/文案    (Codex 不得改簡報內容)
```

## 2. CLI 實際 invocation

非互動路徑固定為：

```bash
codex exec --json --skip-git-repo-check
```

- prompt 從 **stdin** 送入（不是 positional，`codex exec` 沒有 prompt 時會讀 stdin）。
- `--json` 讓 Codex 以 JSONL event 串流輸出。
- `--skip-git-repo-check` 讓 adapter 可在任何 workspace 執行，不限 git repo。
- 使用目前 `codex login` 已登入的 ChatGPT/Codex 訂閱 session；adapter 不讀、不存、不轉傳 token。

JSONL event 主要欄位：

```text
{"type":"thread.started","thread_id":"01a0..."}
{"type":"turn.started"}
{"type":"item.completed","item":{"type":"agent_message","text":"...ARTIFACT_PATH: /.../exec-<uuid>.png"}}
{"type":"turn.completed","usage":{...}}
```

`thread_id` 對應 `$CODEX_HOME/generated_images/<thread_id>/`，用於把 artifact discovery
限縮到「這個 turn」的目錄。

## 3. built-in image_gen capability detection

`probe` operation 只檢查能力，不產圖：

```json
{"operation": "probe"}
```

流程：

1. 送出一個「只回答能力、不得產圖」的最小 prompt。
2. Codex 回 `IMAGE_BACKEND_AVAILABLE` 或 `IMAGE_BACKEND_UNAVAILABLE`。
3. adapter 依回覆判定：
   - available → `{"status":"available","backend":"codex_builtin_imagegen"}`
   - unavailable / 無法確認 → `{"status":"unavailable","error_code":"IMAGE_BACKEND_UNAVAILABLE"}`

不可靠時**不**假設可用、**不**走 API。若要更確定，可用 opt-in live probe（實際產一張最小圖）驗證。

判斷 built-in tool 是否可用的實務訊號：Codex 是否成功呼叫 built-in `image_gen` 並在
`$CODEX_HOME/generated_images/<thread_id>/` 產出檔案；或 agent text 是否出現
`IMAGE_BACKEND_UNAVAILABLE` / 「image_gen tool is not available」等 marker。

## 4. Artifact discovery 方法

built-in `image_gen` 不接受「指定 output path」參數，預設把圖存到
`$CODEX_HOME/generated_images/<thread_id>/exec-<uuid>.png`。adapter 因此採「明確路徑優先、
before/after diff 為 fallback」：

1. turn 前 snapshot `$CODEX_HOME/generated_images/` 現有 raster 檔案 + mtime。
2. 執行單一 Codex image turn。
3. 找出這個 turn 新產生的 artifact：
   - **優先**：Codex 回報的 `ARTIFACT_PATH: <path>`（存在、是允許格式、位於 generated_images 內）。
   - **fallback**：以 `thread_id` 目錄為範圍做 before/after diff，只取有效 raster image。
   - 全 root diff 只在沒有 `thread_id` 時使用。
4. 多個有效候選 → **不猜**。回 `IMAGE_ARTIFACT_AMBIGUOUS`，diagnostics 列出所有候選 path，由 AGY 決定；不選最新、不選最大、不隨機、不靠檔名猜。
5. 驗證是有效 bitmap（magic number + header 可讀、非 0 bytes）。
6. copy 進 caller `output_path`（atomic replace；預設不覆蓋，除非 `regenerate`）。

實測（live）：discovery method = `explicit_reported_path`，thread 目錄唯一新檔案，成功
copy 進 `.agy-ppt-integration/codex-imagegen-probe.png`。

## 5. Input / Output contract

Input：

```json
{
  "slide_id": "slide_03",
  "operation": "generate",
  "prompt": "完整圖片 prompt",
  "output_path": "origin_image/slide_03.png",
  "aspect_ratio": "16:9"
}
```

`operation` 第一版只支援 `generate`、`regenerate`、`probe`。`edit` 尚無可靠的
built-in local-file semantics，第一版**不**假裝支援。

Output（成功）：

```json
{
  "status": "completed",
  "slide_id": "slide_03",
  "operation": "generate",
  "backend": "codex_builtin_imagegen",
  "output_path": "origin_image/slide_03.png",
  "warnings": [],
  "diagnostics": {"auth": "chatgpt_cli_session", "api_fallback_used": false}
}
```

Output（backend 不可用）：

```json
{"status": "error", "error_code": "IMAGE_BACKEND_UNAVAILABLE", "slide_id": "slide_03"}
```

其他 error_code：`CODEX_CLI_UNAVAILABLE`、`CODEX_AUTH_UNAVAILABLE`、
`IMAGE_GENERATION_FAILED`、`IMAGE_ARTIFACT_NOT_FOUND`、`IMAGE_ARTIFACT_AMBIGUOUS`、
`IMAGE_OUTPUT_INVALID`、`IMAGE_OUTPUT_PATH_CONFLICT`、`CODEX_TIMEOUT`。

## 6. Artifact safety

- `output_path` 必須位於 workspace/repository root 內；拒絕 path traversal 與 root 外寫入。
- 自動建立必要 parent directory。
- 不覆蓋既有檔案，除非 operation 明確是 `regenerate`。
- 產物必須是有效 bitmap（PNG/JPEG/WebP，非 0 bytes，dimensions 可讀）。
- landscape / 16:9 若工具輸出非精確 16:9：記 **warning**，**不**用 Pillow 重畫簡報。
  adapter 不用 Pillow 取代 image generation，只讀 header 驗證。

## 7. 派工

```bash
python3 skills/agy-ppt/scripts/codex_image_adapter.py --input job.json --output result.json
cat job.json | python3 skills/agy-ppt/scripts/codex_image_adapter.py
```

capability probe：

```bash
echo '{"operation":"probe"}' | python3 skills/agy-ppt/scripts/codex_image_adapter.py
```

## 8. 驗證

Unit tests（不消耗 Codex 額度）：

```bash
python3 -m unittest discover -s skills/agy-ppt/tests -t skills/agy-ppt/tests -p "test_*.py"
```

Live integration test（opt-in，使用訂閱 session，不用 API key）：

```bash
AGY_PPT_LIVE_CODEX_IMAGE=1 python3 skills/agy-ppt/tests/integration/test_codex_imagegen_live.py
```

若 runtime 沒有 expose built-in `image_gen`，live test 不 fallback API，會回
`IMAGE_BACKEND_UNAVAILABLE` 並視為 runtime capability blocker（skip），不是 coding failure。
