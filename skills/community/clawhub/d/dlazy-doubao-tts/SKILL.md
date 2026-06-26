---
name: dlazy-doubao-tts
version: 1.2.0
description: Synthesize text into natural and fluent speech using Doubao TTS.
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
    'openclaw': { 'systemPrompt': 'When invoking this skill, use dlazy doubao-tts -h for help.' },
  }
---

# dlazy-doubao-tts

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Synthesize text into natural and fluent speech using Doubao TTS.

## Trigger Keywords

- doubao tts
- text to speech
- generate speech
- voice broadcast

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
Run the `dlazy doubao-tts` command to get results.

```bash
dlazy doubao-tts -h

Options:
  --prompt [prompt]                    Prompt
  --voice_language [voice_language]    Voice Language [default: zh-cn] (choices: "zh-cn", "en")
  --voiceId [voiceId]                  Voice ID Options depend on "voice_language". when voice_language="zh-cn": zh_female_vv_uranus_bigtts (Vivi 2.0), zh_female_xiaohe_uranus_bigtts (小何 2.0), zh_male_m191_uranus_bigtts (云舟 2.0), zh_male_taocheng_uranus_bigtts (小天 2.0), zh_male_liufei_uranus_bigtts (刘飞 2.0), zh_male_sophie_uranus_bigtts (魅力苏菲 2.0), zh_female_qingxinnvsheng_uranus_bigtts (清新女声 2.0), zh_female_cancan_uranus_bigtts (知性灿灿 2.0), zh_female_sajiaoxuemei_uranus_bigtts (撒娇学妹 2.0), zh_female_tianmeixiaoyuan_uranus_bigtts (甜美小源 2.0), zh_female_tianmeitaozi_uranus_bigtts (甜美桃子 2.0), zh_female_shuangkuaisisi_uranus_bigtts (爽快思思 2.0), zh_female_peiqi_uranus_bigtts (佩奇猪 2.0), zh_female_linjianvhai_uranus_bigtts (邻家女孩 2.0), zh_male_shaonianzixin_uranus_bigtts (少年梓辛/Brayan 2.0), zh_male_sunwukong_uranus_bigtts (猴哥 2.0), zh_female_yingyujiaoxue_uranus_bigtts (Tina老师 2.0), zh_female_kefunvsheng_uranus_bigtts (暖阳女声 2.0), zh_female_xiaoxue_uranus_bigtts (儿童绘本 2.0), zh_male_dayi_uranus_bigtts (大壹 2.0), zh_female_mizai_uranus_bigtts (黑猫侦探社咪仔 2.0), zh_female_jitangnv_uranus_bigtts (鸡汤女 2.0), zh_female_meilinvyou_uranus_bigtts (魅力女友 2.0), zh_female_liuchangnv_uranus_bigtts (流畅女声 2.0), zh_male_ruyayichen_uranus_bigtts (儒雅逸辰 2.0), saturn_zh_female_keainvsheng_tob (可爱女生), saturn_zh_female_tiaopigongzhu_tob (调皮公主), saturn_zh_male_shuanglangshaonian_tob (爽朗少年), saturn_zh_male_tiancaitongzhuo_tob (天才同桌), saturn_zh_female_cancan_tob (知性灿灿), saturn_zh_female_qingyingduoduo_cs_tob (轻盈朵朵 2.0), saturn_zh_female_wenwanshanshan_cs_tob (温婉珊珊 2.0), saturn_zh_female_reqingaina_cs_tob (热情艾娜 2.0); when voice_language="en": timen_male_tim_uranus_bigtts (Timen), en_female_dacey_uranus_bigtts (Dacey), en_female_stokie_uranus_bigtts (Stokie) [default: zh_female_shuangkuaisisi_uranus_bigtts] [options depend on --voice_language; voice_language=zh: zh_female_vv_uranus_bigtts (Vivi 2.0), zh_female_xiaohe_uranus_bigtts (小何 2.0), zh_male_m191_uranus_bigtts (云舟 2.0), zh_male_taocheng_uranus_bigtts (小天 2.0), zh_male_liufei_uranus_bigtts (刘飞 2.0), zh_male_sophie_uranus_bigtts (魅力苏菲 2.0), zh_female_qingxinnvsheng_uranus_bigtts (清新女声 2.0), zh_female_cancan_uranus_bigtts (知性灿灿 2.0), zh_female_sajiaoxuemei_uranus_bigtts (撒娇学妹 2.0), zh_female_tianmeixiaoyuan_uranus_bigtts (甜美小源 2.0), zh_female_tianmeitaozi_uranus_bigtts (甜美桃子 2.0), zh_female_shuangkuaisisi_uranus_bigtts (爽快思思 2.0), zh_female_peiqi_uranus_bigtts (佩奇猪 2.0), zh_female_linjianvhai_uranus_bigtts (邻家女孩 2.0), zh_male_shaonianzixin_uranus_bigtts (少年梓辛/Brayan 2.0), zh_male_sunwukong_uranus_bigtts (猴哥 2.0), zh_female_yingyujiaoxue_uranus_bigtts (Tina老师 2.0), zh_female_kefunvsheng_uranus_bigtts (暖阳女声 2.0), zh_female_xiaoxue_uranus_bigtts (儿童绘本 2.0), zh_male_dayi_uranus_bigtts (大壹 2.0), zh_female_mizai_uranus_bigtts (黑猫侦探社咪仔 2.0), zh_female_jitangnv_uranus_bigtts (鸡汤女 2.0), zh_female_meilinvyou_uranus_bigtts (魅力女友 2.0), zh_female_liuchangnv_uranus_bigtts (流畅女声 2.0), zh_male_ruyayichen_uranus_bigtts (儒雅逸辰 2.0), saturn_zh_female_keainvsheng_tob (可爱女生), saturn_zh_female_tiaopigongzhu_tob (调皮公主), saturn_zh_male_shuanglangshaonian_tob (爽朗少年), saturn_zh_male_tiancaitongzhuo_tob (天才同桌), saturn_zh_female_cancan_tob (知性灿灿), saturn_zh_female_qingyingduoduo_cs_tob (轻盈朵朵 2.0), saturn_zh_female_wenwanshanshan_cs_tob (温婉珊珊 2.0), saturn_zh_female_reqingaina_cs_tob (热情艾娜 2.0); voice_language=en: timen_male_tim_uranus_bigtts (Timen), en_female_dacey_uranus_bigtts (Dacey), en_female_stokie_uranus_bigtts (Stokie)]
  --speed_ratio [speed_ratio]          Speed Ratio [default: 1.0] (choices: "0.8", "1.0", "1.2", "1.5", "2.0")
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
    "tool": "doubao-tts",
    "modelId": "doubao-tts",
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
dlazy doubao-tts --prompt 'prompt text'

# complex call:
dlazy doubao-tts --prompt 'prompt text'
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
