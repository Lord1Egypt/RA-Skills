# OAuth / 訂閱制執行環境

## 1. 原則

本 Skill 的預設 profile 是「訂閱登入優先、零 API key」。

```text
AGY   = Google AI Pro 登入 session
Kiro  = Kiro Pro 登入 session
Codex = ChatGPT Plus / Codex 登入 session
```

各 CLI 自己管理 credential。

## 2. AGY

AGY 是主控。

Skill 安裝在 workspace：

```text
<workspace>/.agents/skills/agy-ppt/SKILL.md
```

也可使用 Antigravity global skill 位置：

```text
~/.gemini/config/skills/agy-ppt/
```

本 workflow 不要求 Gemini API key。

## 3. Kiro

先用正常方式登入 Kiro CLI，確認目前帳號／session 可用。

唯一受支援的 runtime 是 **Kiro CLI V3**：

```bash
kiro-cli --v3 acp --auth-method cli
```

ACP 使用 stdin/stdout + JSON-RPC 2.0。

`--auth-method cli` 表示由 kiro-cli 自己從本機 credential store 解析 access token。
省略時 V3 引擎會改為要求 ACP client 透過 `_kiro/auth/getAccessToken` 提供 token，
等於讓 Skill 變成 credential broker，本 profile 禁止這種模式。

V3 的 `acp` 子指令不接受 `--agent`，所以 `ppt-engineer` 在 session 建立後才切換：

```text
initialize
  -> session/new
  -> 從 modes.availableModes 發現 ppt-engineer
  -> session/set_mode {modeId: "ppt-engineer"}
  -> 確認 active agent
  -> session/prompt
  -> TurnEnd
  -> AGY
```

`session/set_mode` 即使 modeId 不存在也會回空結果，因此必須以引擎回報的 active agent
（`config_option_update` 的 `configOptions[id=mode].currentValue`，或 `current_mode_update`）
作為確認依據。

無法確認時回報 `ENGINEERING_AGENT_UNAVAILABLE`，不得改用引擎預設 agent。

`ppt-engineer` 也是整個 turn 的 invariant；turn 中 drift 時回報
`ENGINEERING_AGENT_SCOPE_LOST` 並立即 cancel。

**V2 不支援。** 沒有 V2 執行路徑，也不得 fallback。舊 caller 若送 `engine = "v2"`，
一律回報 `UNSUPPORTED_KIRO_ENGINE` 且不執行。

本 profile 不採用需要 API key 的 CI/headless 路線。

實機驗證（opt-in）：

```bash
python3 skills/agy-ppt/tests/integration/test_kiro_v3_acp.py
python3 skills/agy-ppt/tests/integration/test_kiro_v3_acp_write.py
```

## 4. Codex

Codex 使用目前已登入的 ChatGPT/Codex session（`codex login` 顯示 `Logged in using ChatGPT`）。

圖片 worker 由 `scripts/codex_image_adapter.py` 派工：

```bash
codex exec --json --skip-git-repo-check    # prompt 走 stdin
```

- 使用 `$imagegen`，只用 built-in `image_gen`。
- adapter 從子行程環境移除 API-key 類變數（`OPENAI_API_KEY`、`*_API_KEY`、
  `*_ACCESS_TOKEN`、`OPENAI_BASE_URL` 等），只回報變數名稱，不回報值。
- diagnostics 記錄 `auth: chatgpt_cli_session`、`api_fallback_used: false`、
  `credential_env_stripped: [...]`。

本 Skill 不提供 `OPENAI_API_KEY` fallback。若 built-in `image_gen` 不可用，回
`IMAGE_BACKEND_UNAVAILABLE` 並交回 AGY，不自動付費。

實機驗證（opt-in，使用訂閱 session，不用 API key）：

```bash
AGY_PPT_LIVE_CODEX_IMAGE=1 python3 skills/agy-ppt/tests/integration/test_codex_imagegen_live.py
```

細節見 `docs/codex-image-runtime.md`。

## 5. Token 安全

禁止 Skill：

- 讀取 OAuth token 檔案內容
- 複製 refresh token
- 把 credential 放進 slide job
- 把 AGY token 傳給 Kiro/Codex
- 把 Kiro token 傳給 AGY/Codex
- 把 Codex token 傳給 AGY/Kiro

每個 CLI 都只是使用自己的 local authenticated environment。

Bridge 額外保證：

- 子行程環境會移除 API-key 類變數（`KIRO_API_KEY`、`*_API_KEY`、`*_ACCESS_TOKEN` 等），
  只回報變數名稱，不回報值。
- ACP client 不宣告 `fs` / `terminal` capability，也不回應任何 token brokering 請求。
- 回傳給 AGY 的文字會遮蔽 token 形狀的字串。
