---
name: aggclaw
description: "AppGrowing Global intelligent ad creative analysis assistant. Connects to the Explore mode API to analyze user intent, find the most relevant overseas ad creatives, and deliver automated analysis. Includes Inspire mode. Triggers: keywords analyze creatives, creative analysis, overseas campaigns, explore creatives, find creatives; commands /aggclaw, /aggclaw-game, /aggclaw-app, /aggclaw-shortdrama, /agg_inspire"
homepage: https://appgrowing.net/
metadata:
  {
    "openclaw": {
      "slug": "aggclaw",
      "version": "1.1.0",
      "author": "youcloud",
      "emoji": "🌍",
      "requires": {
        "env": ["YOUCLOUD_API_KEY"]
      }
    }
  }
---

# aggclaw

AppGrowing Global intelligent ad creative analysis assistant. Connects to the Explore mode API to analyze user intent, find the most relevant overseas ad creatives, and deliver automated analysis — allowing users to interact directly with creative insights. Includes new Inspire mode for creative strategy and ideation.

## Access

Available to **AI plus** and **Pro** subscribers of AppGrowing Global. To get an API Key: log in to AppGrowing Global → Profile → Enterprise Info.

## Triggers

- Keywords: analyze creatives, creative analysis, overseas campaigns, explore creatives, find creatives
- Commands:
  - `/aggclaw` → Auto-detect: discussion-style questions → Inspire mode; game content → Game mode; other content → Non-game mode
  - `/aggclaw-game` → Game mode (`chat_mode=7`)
  - `/aggclaw-app` → Non-game app mode (`chat_mode=8`)
  - `/aggclaw-shortdrama` → Short drama mode (`chat_mode=8`)
  - `/agg_inspire` → Inspire mode (`chat_mode=9`)

## Language Detection

Before any API call, detect the language of the user's input and respond in that language throughout the session.

- **Detection rule:**
  - If the user's input contains Chinese characters (CJK Unified Ideographs) → Chinese
  - If the user's input contains Japanese characters (Hiragana or Katakana) → Japanese
  - Otherwise → English
- This language preference persists for the entire session (including follow-up questions within the same session_id).
- The `input` field sent to the API should remain in the user's original language — do not translate the user's query.
- All framing text, error messages, and summaries added by the agent should be in the detected language.

### language_code Parameter

Based on the detected language, set the `language_code` parameter for API calls:

| Detected Language | `language_code` Value |
|---|---|
| Chinese | `zh` |
| Japanese | `ja` |
| English | `en` |
| Other / Undetermined | *(omit the parameter)* |

**Rule:** `language_code` may only be `zh`, `ja`, or `en`. For any other language, do not include the parameter in the request.

## Execution Flow

1. **Check API Key** (read from environment variable `YOUCLOUD_API_KEY`):
   - Key present → proceed
   - Key empty/missing → prompt user to configure:
     ```
     Please configure your API Key first:
     1. Log in to AppGrowing Global → Profile → Enterprise Info to get your API Key
     2. Set it as environment variable YOUCLOUD_API_KEY, e.g.:
        - Linux/macOS: export YOUCLOUD_API_KEY="your-key-here"
        - Windows: $env:YOUCLOUD_API_KEY="your-key-here"
     3. Send your request again after configuration.
     ```
   - ✅ Rule: **Never send requests without a valid API Key**

2. **⚠️ Mandatory Timeout Rules**
   - API request timeout: **600 seconds**
   - **🔴 Absolutely forbidden: do NOT interrupt a request before timeout, do NOT send any "still processing" or "will let you know" messages**
   - **Must: wait for the API to return a complete result, then reply to the user in one shot**
   - Only two situations allow sending a message:
     1. API returns a complete analysis result → output the result directly
     2. API timeout or request error → output error message

3. **Detect Language & Set `language_code`** (see Language Detection section above)

4. **Determine chat_mode:**
   - **Command-specified:**
     - `/aggclaw-game` → Game mode (`chat_mode=7`)
     - `/aggclaw-app`, `/aggclaw-shortdrama` → Non-game mode (`chat_mode=8`)
     - `/agg_inspire` → Inspire mode (`chat_mode=9`)
   - **Auto-detect (keyword/content trigger):**
     - Input is a discussion-style question (asking for advice, strategies, ideas, comparisons, "how to", "what should", brainstorming, creative inspiration — as opposed to asking for specific ad creative data analysis) → Inspire mode (`chat_mode=9`)
     - Input contains game-related content (game titles, gaming terminology like RPG/SLG/MMO) → Game mode (`chat_mode=7`)
     - Other content (apps, e-commerce, utilities, short dramas) → Default non-game mode (`chat_mode=8`)

5. **Call the API directly — do NOT ask the user questions:**
   - When the user initiates a creative analysis request, assemble the intent into an `input` and call the API directly. Do not ask for product positioning, target market, or other supplementary info — let the API search and analyze on its own.
   - New analysis request → start a new session, pass `chat_mode` and `language_code`, do NOT carry `session_id`
   - Follow-up question (about a previous analysis) → reuse the previous `session_id`, do NOT pass `chat_mode` or `language_code` (preserve the session's existing mode and language)
   - Output the API response result directly.

## API Specification

- URL: `https://ai-chat-global.youcloud.com/aichat/claw`
- Method: POST JSON
- Headers: `Authorization: Bearer {KEY}`, `Content-Type: application/json`
- Parameters:
  - `input`: User question (required)
  - `session_id`: For follow-up questions, omit for new conversations
  - `chat_mode`: Chat mode, 7=game, 8=non-game, 9=inspire. **Only pass for new conversations (no session_id); omit for follow-ups to preserve the session's mode**
  - `language_code`: Language code, `zh`/`ja`/`en`. **Only pass for new conversations (no session_id); omit for follow-ups to preserve the session's language**
- Response: Output `output` (markdown) **as-is unless the user's language differs from the API response language — in that case, translate the output to the user's language**; save `session_id` for future follow-ups
- Timeout: ≥600s

## PowerShell Call Template

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$apiKey = $env:YOUCLOUD_API_KEY
$body = @{input="Your analysis request"; chat_mode=8; language_code="en"} | ConvertTo-Json -Compress
$params = @{
  Uri = "https://ai-chat-global.youcloud.com/aichat/claw"
  Method = "Post"
  ContentType = "application/json; charset=utf-8"
  Headers = @{Authorization="Bearer $apiKey"}
  Body = $body
  TimeoutSec = 600
}
Invoke-RestMethod @params | Select-Object -ExpandProperty output
```

## Error Handling

- 400 Invalid credentials / 401 Authentication failed:
  ```
  API Key authentication failed. Please check if your key is active or expired. Get your API Key from AppGrowing Global Profile → Enterprise Info, or contact support.
  ```
- 400 "System error" (API returns "Sorry, system error, please try again later."):
  - Repeated occurrences indicate temporary server instability, unrelated to API Key or request content.
  - Retry strategy: try a more generic/shorter query 1-2 times; if still failing, inform the user that the server is temporarily unavailable and suggest trying later.
  - Observed behavior: certain vertical categories (e.g., AI tool apps) may trigger this error due to insufficient creative data; trying an adjacent category (e.g., e-commerce) may work normally.
- Timeout: "Analysis is still in progress. Try asking again or resend your request."
- Other errors: "Request returned an error (code={code}). Please check your API Key permissions, account quota, or contact customer support."

## Notes

- ⚠️ API response time is typically **60 seconds+**, always use a 600-second timeout
- ⚠️ API Key is read from environment variable `YOUCLOUD_API_KEY`
- **Inspire mode**: `/agg_inspire` command uses `chat_mode=9` for creative strategy and ideation. Unlike Explore modes (7/8), Inspire mode focuses on decision trees, creative frameworks, and strategic guidance based on real-world creative data.

## Examples

For full input/output examples, see [references/example.md](references/example.md)
