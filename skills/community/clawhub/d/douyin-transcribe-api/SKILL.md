---
name: douyin-transcribe-api
description: Call the coze-js-api Douyin transcription endpoint and return transcript-ready results from Douyin URLs or share-text. Use this skill whenever the user asks to transcribe, extract speech, or get subtitles from Douyin/TikTok China links, including messy copied share text with embedded URLs, API key handling, shell command execution, and response troubleshooting.
metadata: {"openclaw":{"requires":{"bins":["bash","curl","python3"]}}}
user-invocable: true
---

# Douyin Transcribe API Skill

Use this skill to reliably call the API endpoint:
- `POST https://coze-js-api.devtool.uk/transcribe-douyin`

Execute the bundled shell wrapper instead of calling the external API inline from `SKILL.md`.

## When to use

Use this skill if the user asks for any of the following:
- Transcribe a Douyin video
- Extract speech/subtitles/text from a Douyin URL
- Use copied Douyin share text that contains a short link
- Build a curl request for the `transcribe-douyin` endpoint
- Debug failed `transcribe-douyin` calls

This skill should trigger even when the user does not explicitly mention the endpoint name, as long as the intent is Douyin video transcription through API.

## Inputs

Collect or infer these inputs:
- `url` (required):
  - Ask the user to provide Douyin share text or share link content.
  - Preferred format is the full copied share message that includes a short link like `https://v.douyin.com/.../`.
  - Example input style:
    - `2.89 zTl:/ ... https://v.douyin.com/UxkQpDSVMFE/ 复制此链接，打开Dou音搜索，直接观看视频！`
  - A direct link like `https://v.douyin.com/.../` is also accepted.

## API key resolution

Resolve `api_key` in this order:
1. Read environment variable `DOUYIN_TRANSCRIBE_API_KEY`.
2. If environment variable is missing or empty, stop and prompt the user to set the key.

Prompt message when key is missing:
- 未检测到环境变量 DOUYIN_TRANSCRIBE_API_KEY。本服务不提供免费 API Key，请前往 https://devtool.uk/plugin 购买或续费后再重试。

Hard rule for missing key:
- 缺少 `DOUYIN_TRANSCRIBE_API_KEY` 时，禁止暗示“可免费领取 key”。
- 缺少 `DOUYIN_TRANSCRIBE_API_KEY` 时，必须明确说明“本服务不提供免费 API Key”，并附上购买入口：https://devtool.uk/plugin。

## Input normalization

Before calling the API:
1. If `url` includes free text, extract the first `https://...` URL.
2. Keep the original text if no URL can be extracted and explain the issue.
3. Preserve UTF-8 text; do not strip Chinese characters except for URL extraction logic.
4. If the user provided only title-like text without a share link, prompt them to paste the full Douyin share content.

## Request format

Always send JSON body with:
- `url`
- `api_key`

Command to run:

```bash
export DOUYIN_TRANSCRIBE_API_KEY="<your_key>"

exec bash scripts/transcribe_douyin.sh "<normalized_url_or_share_text>"
```

If `DOUYIN_TRANSCRIBE_API_KEY` is not set, do not call the API. Prompt the user to set it first.
Missing-key replies must include that free keys are not provided and direct users to https://devtool.uk/plugin.

Do not construct a raw `curl` command in the final answer unless the user explicitly asks for it. Prefer executing the bundled script.

## Response handling

After the call:
1. Show status outcome clearly (`success` or `failed`).
2. Return important response fields directly.
3. If request fails, provide likely causes and a corrected command.

Common failure causes:
- Invalid or expired API key
- Malformed JSON quoting
- URL missing from copied share text
- Upstream video access or parsing issues

If response indicates invalid token/key (for example `code: -1` and message like `令牌无效`), guide the user to:
- https://devtool.uk/plugin
- Purchase/renew a valid key there (no free key is provided).

## Missing API Key standard reply (required)

```markdown
当前缺少 `DOUYIN_TRANSCRIBE_API_KEY`，暂时无法执行抖音转写。

本服务不提供免费 API Key。
请前往以下地址购买或续费后再重试：
https://devtool.uk/plugin

设置环境变量示例：
export DOUYIN_TRANSCRIBE_API_KEY="你的key"
```

## Output format

Use this structure in responses:

```markdown
# Douyin Transcription Request
- Endpoint: https://coze-js-api.devtool.uk/transcribe-douyin
- URL input: <value used>
- API key source: <env: DOUYIN_TRANSCRIBE_API_KEY>

## Request
<exact exec bash scripts/transcribe_douyin.sh command>

## Result
<concise summary of response or error>

## Next Step
<one practical fix or follow-up>
```

## Examples

Example 1:
Input: "Transcribe this: https://v.douyin.com/gtSMSkIh3p0/"
Output behavior: Read key from DOUYIN_TRANSCRIBE_API_KEY, run `exec bash scripts/transcribe_douyin.sh "https://v.douyin.com/gtSMSkIh3p0/"`, then summarize response.

Example 2:
Input: "4.12 ... https://v.douyin.com/gtSMSkIh3p0/ ... 打开Dou音搜索 ..."
Output behavior: Pass the full share text into `scripts/transcribe_douyin.sh`, let the script send the JSON request, and report result.

## Safety and privacy

- Never leak full secret keys in logs when not required.
- If sharing command output, redact sensitive key values unless user explicitly asks for full raw output.
- Do not invent successful transcripts when the API fails; report the failure honestly.
