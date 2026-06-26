---
name: dlazy-gemini-2.5-tts
version: 1.2.0
description: Generate multilingual, highly natural audio using Gemini 2.5 text-to-speech.
metadata:
  {
    'clawdbot':
      {
        'emoji': '🤖',
        'requires': { 'bins': ['npm', 'npx'] },
        'install': 'npm install -g @dlazy/cli@1.2.0',
        'installAlternative': 'npx @dlazy/cli@1.2.0',
        'homepage': 'https://github.com/dlazyai/cli',
        'source': 'https://github.com/dlazyai/cli',
        'author': 'dlazyai',
        'license': 'see-repo',
        'npm': 'https://www.npmjs.com/package/@dlazy/cli',
        'configLocation': '~/.dlazy/config.json',
        'apiEndpoints': ['api.dlazy.com', 'files.dlazy.com'],
      },
    'openclaw': { 'systemPrompt': 'When invoking this skill, use dlazy gemini-2.5-tts -h for help.' },
  }
---

# dlazy-gemini-2.5-tts

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Generate multilingual, highly natural audio using Gemini 2.5 text-to-speech.

## Trigger Keywords

- gemini tts
- text to speech
- generate speech

## Authentication

All requests require a dLazy API key. The recommended way to authenticate is:

```bash
dlazy login
```

This runs a device-code flow (also works in remote shells) and **automatically saves your API key** to the local CLI config — no manual copy/paste required.

### Alternative: Set the Key Manually

If you already have an API key, you can save it directly:

```bash
dlazy auth set YOUR_API_KEY
```

The CLI saves the key in your user config directory (`~/.dlazy/config.json` on macOS/Linux, `%USERPROFILE%\.dlazy\config.json` on Windows), with file permissions restricted to your OS user account. You can also supply the key per-invocation via the `DLAZY_API_KEY` environment variable.

### Getting Your API Key Manually

1. Sign in or create an account at [dlazy.com](https://dlazy.com)
2. Go to [dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key)
3. Copy the key shown in the API Key section

Each key is scoped to your dLazy organization and can be **rotated or revoked at any time** from the same dashboard.

## About & Provenance

- **CLI source code**: [github.com/dlazyai/cli](https://github.com/dlazyai/cli)
- **Maintainer**: dlazyai
- **npm package**: `@dlazy/cli` (pinned to `1.0.9` in this skill's install spec)
- **Homepage**: [dlazy.com](https://dlazy.com)

You can install on demand without persisting a global binary by running:

```bash
npx @dlazy/cli@1.2.0 <command>
```

Or, if you prefer a global install, the skill's `metadata.clawdbot.install` field declares the exact pinned version (`npm install -g @dlazy/cli@1.2.0`). Review the GitHub source before installing.

## How It Works

This skill is a thin client over the dLazy hosted API. When you invoke it:

- Prompts and parameters you provide are sent to the dLazy API endpoint (`api.dlazy.com`) for inference.
- Any local file paths you pass to image / video / audio fields are uploaded to dLazy's media storage (`files.dlazy.com`) so the model can read them — the same flow as any cloud-based generation API.
- Generated output URLs returned by the API are hosted on `files.dlazy.com`.

This is the standard SaaS pattern; the skill itself does not access network or filesystem resources beyond what the dLazy CLI already handles. See [dlazy.com](https://dlazy.com) for the full service terms.

## Usage

**CRITICAL INSTRUCTION FOR AGENT**:
Run the `dlazy gemini-2.5-tts` command to get results.

```bash
dlazy gemini-2.5-tts -h

Options:
  --prompt [prompt]                    Prompt
  --voice_language [voice_language]    Voice Language [default: cmn] (choices: "cmn", "en")
  --voiceName [voiceName]              Voice Name Options depend on "voice_language". when voice_language="cmn": Zephyr (Zephyr - 明亮), Puck (Puck - 欢快), Charon (Charon - 信息丰富), Kore (Kore - 坚定), Fenrir (Fenrir - 兴奋), Leda (Leda - 青春), Orus (Orus - 公正), Aoede (Aoede - 清爽), Callirrhoe (Callirrhoe - 轻松), Autonoe (Autonoe - 明亮), Enceladus (Enceladus - 气声), Iapetus (Iapetus - 清晰), Umbriel (Umbriel - 轻松愉快), Algieba (Algieba - 平滑), Despina (Despina - 平滑), Erinome (Erinome - 清晰), Algenib (Algenib - 沙哑), Rasalgethi (Rasalgethi - 信息丰富), Laomedeia (Laomedeia - 欢快), Achernar (Achernar - 柔和), Alnilam (Alnilam - 坚定), Schedar (Schedar - 均匀), Gacrux (Gacrux - 成熟), Pulcherrima (Pulcherrima - 转折), Achird (Achird - 友好), Zubenelgenubi (Zubenelgenubi - 随意), Vindemiatrix (Vindemiatrix - 温和), Sadachbia (Sadachbia - 活泼), Sadaltager (Sadaltager - 知识渊博), Sulafat (Sulafat - 偏高); when voice_language="en": Zephyr (Zephyr - Bright), Puck (Puck - Cheerful), Charon (Charon - Informative), Kore (Kore - Firm), Fenrir (Fenrir - Excitable), Leda (Leda - Youthful), Orus (Orus - Just), Aoede (Aoede - Breezy), Callirrhoe (Callirrhoe - Relaxed), Autonoe (Autonoe - Bright), Enceladus (Enceladus - Breath), Iapetus (Iapetus - Clear), Umbriel (Umbriel - Light), Algieba (Algieba - Smooth), Despina (Despina - Smooth), Erinome (Erinome - Clear), Algenib (Algenib - Gravelly), Rasalgethi (Rasalgethi - Informative), Laomedeia (Laomedeia - Cheerful), Achernar (Achernar - Soft), Alnilam (Alnilam - Firm), Schedar (Schedar - Even), Gacrux (Gacrux - Mature), Pulcherrima (Pulcherrima - Turning), Achird (Achird - Friendly), Zubenelgenubi (Zubenelgenubi - Casual), Vindemiatrix (Vindemiatrix - Gentle), Sadachbia (Sadachbia - Lively), Sadaltager (Sadaltager - Scholarly), Sulafat (Sulafat - High) [default: Kore] [options depend on --voice_language; voice_language=cmn: Zephyr (Zephyr - 明亮), Puck (Puck - 欢快), Charon (Charon - 信息丰富), Kore (Kore - 坚定), Fenrir (Fenrir - 兴奋), Leda (Leda - 青春), Orus (Orus - 公正), Aoede (Aoede - 清爽), Callirrhoe (Callirrhoe - 轻松), Autonoe (Autonoe - 明亮), Enceladus (Enceladus - 气声), Iapetus (Iapetus - 清晰), Umbriel (Umbriel - 轻松愉快), Algieba (Algieba - 平滑), Despina (Despina - 平滑), Erinome (Erinome - 清晰), Algenib (Algenib - 沙哑), Rasalgethi (Rasalgethi - 信息丰富), Laomedeia (Laomedeia - 欢快), Achernar (Achernar - 柔和), Alnilam (Alnilam - 坚定), Schedar (Schedar - 均匀), Gacrux (Gacrux - 成熟), Pulcherrima (Pulcherrima - 转折), Achird (Achird - 友好), Zubenelgenubi (Zubenelgenubi - 随意), Vindemiatrix (Vindemiatrix - 温和), Sadachbia (Sadachbia - 活泼), Sadaltager (Sadaltager - 知识渊博), Sulafat (Sulafat - 偏高); voice_language=en: Zephyr (Zephyr - Bright), Puck (Puck - Cheerful), Charon (Charon - Informative), Kore (Kore - Firm), Fenrir (Fenrir - Excitable), Leda (Leda - Youthful), Orus (Orus - Just), Aoede (Aoede - Breezy), Callirrhoe (Callirrhoe - Relaxed), Autonoe (Autonoe - Bright), Enceladus (Enceladus - Breath), Iapetus (Iapetus - Clear), Umbriel (Umbriel - Light), Algieba (Algieba - Smooth), Despina (Despina - Smooth), Erinome (Erinome - Clear), Algenib (Algenib - Gravelly), Rasalgethi (Rasalgethi - Informative), Laomedeia (Laomedeia - Cheerful), Achernar (Achernar - Soft), Alnilam (Alnilam - Firm), Schedar (Schedar - Even), Gacrux (Gacrux - Mature), Pulcherrima (Pulcherrima - Turning), Achird (Achird - Friendly), Zubenelgenubi (Zubenelgenubi - Casual), Vindemiatrix (Vindemiatrix - Gentle), Sadachbia (Sadachbia - Lively), Sadaltager (Sadaltager - Scholarly), Sulafat (Sulafat - High)]
  --dry-run                            Print payload + cost estimate without calling API
  --no-wait                            Return generateId immediately for async tasks
  --timeout <seconds>                  Max seconds to wait for async completion (default: "1800")
  -h, --help                           display help for command
```

> Any flag also accepts pipe references — `-` (auto-pick from upstream stdin), `@N` (n-th output), `@N.path` (jsonpath into output), `@*` (all primary values), `@stdin` / `@stdin:path` (whole envelope). See `dlazy --help` for details.

## Output Format

```json
{
  "ok": true,
  "result": {
    "tool": "gemini-2.5-tts",
    "modelId": "gemini-2.5-tts",
    "outputs": [
      {
        "type": "image",
        "id": "o_xxxxxxxx",
        "url": "https://files.dlazy.com/result.png",
        "mimeType": "image/png"
      }
    ]
  }
}
```

> Async tasks (when `--no-wait` is passed) return `outputs: []` and a `task: { generateId, status }` field instead. Use `dlazy status <generateId> --wait` to poll.

## Command Examples

```bash
# basic call:
dlazy gemini-2.5-tts --prompt 'prompt text'

# complex call:
dlazy gemini-2.5-tts --prompt 'prompt text'
```

## Error Handling

| Code | Error Type                         | Example Message                                                                                                          |
| ---- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| 401  | Unauthorized (No API Key)          | `ok: false, code: "unauthorized", message: "API key is missing or invalid"`                                              |
| 501  | Missing required parameter         | `error: required option '--prompt <prompt>' not specified`                                                               |
| 502  | Local file read error              | `Error: Image file/Video file not found: C:\path\to\your\file`                                                           |
| 503  | API request failed (no balance)    | `ok: false, code: "insufficient_balance"`                                                                                |
| 503  | API request failed (server error)  | `HTTP status code error (500 server crash)`                                                                              |
| 504  | Asynchronous task execution failed | `=== Generation Failed ===` / `{Specific error reason returned by backend, for example "Prompt violates safety policy"}` |

> **AGENT CRITICAL INSTRUCTION**:
>
> 1. If the execution result returns `code: "insufficient_balance"`, you MUST explicitly inform the user that their credits are insufficient and guide them to recharge: [https://dlazy.com/dashboard/organization/settings?tab=credits](https://dlazy.com/dashboard/organization/settings?tab=credits)
> 2. If the execution result returns `code: "unauthorized"` or indicates missing API key, you MUST inform the user to get their API key from [https://dlazy.com/dashboard/organization/api-key](https://dlazy.com/dashboard/organization/api-key) and save it using `dlazy auth set <key>` and resume the task.

## Tips

Visit https://dlazy.com for more information.
