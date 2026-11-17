# Codex Image Worker Prompt

`codex_image_adapter.py` 送給 Codex 的 worker prompt 邊界。Adapter 會把 AGY 提供的
authoritative slide prompt 包在這個邊界裡送給 `codex exec --json`，Codex 只能當
**圖片 renderer**。

## 邊界（Adapter 一定注入）

- 使用 `$imagegen` skill，且**只**用 built-in `image_gen` tool。
- **禁止** `scripts/image_gen.py`、OpenAI Images API、`OPENAI_API_KEY`，或任何付費 API fallback。永不換 backend。
- 若 built-in `image_gen` 不可用：只回 `IMAGE_BACKEND_UNAVAILABLE` 然後停止，**不得** fallback。
- **禁止**修改 slide content、outline、deck spec、slide job 或任何 source file，不得重寫文案。
- **禁止**寫、跑、改 code。**禁止**呼叫 Kiro。**禁止**組裝 PPTX。
- **禁止**決定下一個 workflow phase。只做一件事：產一張圖。
- 一個 turn 只產**一張**圖。
- 完成後回報 generated artifact 的絕對路徑，格式為單行 `ARTIFACT_PATH: <path>`。

## AGY prompt 是 authoritative

Adapter 只包裝，不改寫。Codex 不得重新設計簡報內容，只依 AGY 給的 prompt 產圖。

## 產物落點

built-in `image_gen` 預設把圖存到 `$CODEX_HOME/generated_images/<thread_id>/`。
Adapter 負責在 turn 後找到新產出的 artifact、驗證是有效 raster image、再 copy 進
caller 指定的 workspace `output_path`。Codex 不需要、也不應該自己指定 output path 參數。

## 失敗語意

- built-in tool 不可用 → `IMAGE_BACKEND_UNAVAILABLE`
- 未登入 / session 失效 → Adapter 判為 `CODEX_AUTH_UNAVAILABLE`
- Codex 執行失敗 → `IMAGE_GENERATION_FAILED`
- 找不到 artifact → `IMAGE_ARTIFACT_NOT_FOUND`
- 多個有效候選 artifact → `IMAGE_ARTIFACT_AMBIGUOUS`（不自行選擇，交回 AGY）
- 產物不是有效圖片 / 0 bytes → `IMAGE_OUTPUT_INVALID`
- output path 衝突（非 regenerate）→ `IMAGE_OUTPUT_PATH_CONFLICT`
- 逾時 → `CODEX_TIMEOUT`
