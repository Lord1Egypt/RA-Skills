---
name: chanjing-credentials-guard
description: Run this skill as a lightweight pre-check for chanjing actions. When the user asks to generate or configure chanjing credentials/keys (APP_ID/SECRET_KEY), run this skill to guide them—check if already configured; if yes, ask whether to re-apply; then open login page and let the user either run the config command or paste APP_ID/SECRET_KEY for the agent to apply.
---

# Chanjing Credentials Guard

## L2 Product Skill

本文件是 **L2 产品层**主手册（**Agent 执行真值**）。

- **本文件（`chanjing-credentials-guard-SKILL.md`）**：业务逻辑、追问与异常语义；据此调度 [`scripts/cli_capabilities.py`](scripts/cli_capabilities.py) 与 [`scripts/`](scripts/) 下脚本。
- **顶层入口** [`../../SKILL.md`](../../SKILL.md)：仅负责路由到本目录，**不**承载本产品执行细则。
- **跨场景约定** [`../../orchestration/orchestration-contract.md`](../../orchestration/orchestration-contract.md)；L3 编排层说明见 [`../../orchestration/README.md`](../../orchestration/README.md)。

## When to Run

1. **As a lightweight pre-check before Chanjing API actions**: Validate credentials once in-task; if missing, guide the user.
2. **When the user asks to generate chanjing keys, get keys, or configure APP_ID/SECRET_KEY**: Run this skill and follow the “Guide to generate keys” flow below.

Before calling any Chanjing API (list voices, TTS, avatar, voice clone, etc.), credentials must be validated.

## Execution Flow

```
1. Check if local APP_ID/SECRET_KEY exists
   └─ No  → Run open_login_page.py (open login in browser) → Offer two setup options (user runs command, or pastes APP_ID/SECRET_KEY for the agent to apply) → After config, continue the original action without asking the user to re-run it
   └─ Yes → Continue

2. Check if process-level Token exists and is not expired
   └─ No  → Call API to request/refresh Token（in-memory reuse only）
   └─ Yes → Continue

3. Continue with the target Skill
```

## Credential Storage (APP_ID/SECRET_KEY read from project .env)

APP_ID/SECRET_KEY 读取自项目 `.env`。路径和格式以 **`scripts/chanjing_config.py`** 为准。

- **Path**: `skills/chanjing-content-creation-skill/.env` (overridable by env `CHANJING_ENV_FILE`)
- **Format**:
```bash
CHANJING_APP_ID=<your_app_id>
CHANJING_SECRET_KEY=<your_secret_key>
```
Token 不会写入 `.env`；仅在进程内按过期时间短时复用，过期后重新请求。

## When APP_ID/SECRET_KEY Is Missing

When local `app_id` or `secret_key` is missing:

1. **Open login page**: Run the `open_login_page.py` script to open the Chanjing sign-in page in the default browser (`https://www.chanjing.cc/openapi/login`).
2. **Offer two setup options** after the user obtains keys:
   - Option A: show the command for the user to run locally.
   - Option B: let the user paste `APP_ID=... SECRET_KEY=...` in chat and apply it for them by running `python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing_config.py --app-id ... --sk ...`.
3. **Continue automatically after setting**: Once APP_ID/SECRET_KEY is saved successfully, continue the original skill flow in the same conversation. Do not ask the user to re-run their previous action.
4. **Handle secrets carefully**:
   - Tell the user APP_ID/SECRET_KEY is sensitive and chat history may retain it.
   - If the user chooses chat-based setup, do not echo the full values back.
   - Only confirm with masked output such as `USER_ID=****`, `SECRET_KEY=****`.
   - Do not print the full secret in summaries or follow-up messages.

Commands to set app_id/secret_key (use either):

```bash
python scripts/chanjing_config.py --app-id <your_app_id> --sk <your_secret_key>
python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing_config.py --app-id <your_app_id> --sk <your_secret_key>
```

To open the login page manually: `python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/open_login_page.py`

## Guide When User Wants to Generate Keys

When the user clearly wants to **generate chanjing keys**, **get keys**, or **configure APP_ID/SECRET_KEY**, follow this flow:

### Step 1: Check if already configured

Check if local app_id/secret_key already exists (read project `.env` via `python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing_config.py --status`).

### Step 2: Branch on result

- **If already configured**: Ask the user—**“You already have Chanjing APP_ID/SECRET_KEY configured. Do you want to re-apply and overwrite the current config?”**
  - If the user confirms re-apply, run the “Guide steps” below.
  - If the user says no, stop; do not open the login page or show config commands.

- **If not configured**: Run the “Guide steps” below directly.

### Guide steps (when not configured or user confirmed re-apply)

1. **Run `open_login_page.py`** to open the Chanjing login page in the default browser.
2. **Explain the page flow clearly**:
   - New users are registered automatically and the current page will display `App ID` and `Secret Key` with copy buttons.
   - Existing users may be redirected to the console; tell them to open the left-side **API 密钥** page to view or reset keys.
3. **Offer two ways to configure credentials** after the user obtains `app_id` and `secret_key`:
   ```bash
   python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing_config.py --app-id <your_app_id> --sk <your_secret_key>
   ```
   The user may either:
   - run the command themselves, or
   - paste `APP_ID=<your_app_id> SECRET_KEY=<your_secret_key>` in chat so the agent can run the command for them.
4. **When the user pastes APP_ID/SECRET_KEY in chat**:
   - treat the values as sensitive,
   - run the config command on the user's machine,
   - avoid echoing full secrets back,
   - continue the original task after successful config instead of stopping.
5. **After setting**: Config is saved and Chanjing skills can be used immediately. If this flow was triggered by another action, continue that action automatically. For re-apply, the command above overwrites the existing config.

You can run `python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/open_login_page.py` first to open the login page, then either run the config command yourself or paste `APP_ID=... SECRET_KEY=...` in the conversation for the agent to apply.

## Token API (see chanjing-openapi.yaml)

```http
POST https://open-api.chanjing.cc/open/v1/access_token
Content-Type: application/json
```

Request body:
```json
{
  "app_id": "{{app_id}}",
  "secret_key": "{{secret_key}}"
}
```

Response (success `code: 0`):
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "access_token": "xxx",
    "expire_in": 1721289220
  }
}
```

- `expire_in`: Unix timestamp for token expiry
- If `code !== 0`, APP_ID/SECRET_KEY is invalid or the request failed

## Validation Logic

1. **app_id/secret_key**: Read from `.env` (path/format above, per `chanjing_config.py`); ensure both are non-empty.
2. **Token**: Prefer process env (`CHANJING_ACCESS_TOKEN` + `CHANJING_TOKEN_EXPIRE_IN`) or in-memory cache; refresh on expiry.

**Shortcut**: Run `python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing_get_token.py`; on success it prints access_token, on failure it prints guidance.

## Shell Config

| Script | Description |
|--------|-------------|
| `open_login_page.py` | Opens the Chanjing login page and explains how new/existing users obtain APP_ID/SECRET_KEY |
| `chanjing_config.py` | Set or view app_id/secret_key status |

```bash
# Open login page (also runs automatically when APP_ID/SECRET_KEY is missing)
python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/open_login_page.py

# Set app_id/secret_key manually
python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing_config.py --app-id <app_id> --sk <secret_key>

# View status
python skills/chanjing-content-creation-skill/products/chanjing-credentials-guard/scripts/chanjing_config.py --status
```

## With Other Skills

- **chanjing-tts**, **chanjing-avatar**, **chanjing-tts-voice-clone**, etc. must pass this credentials guard before running.
- If the agent already has a token from MCP `user-chanjing` `get_access_token`, it may use that; otherwise complete local validation and token preparation first.

## Reference

- [reference.md](reference.md): API and storage format details
- chanjing-openapi.yaml: `/access_token`, `dto.OpenAccessTokenReq`, `dto.OpenAccessTokenResp`
