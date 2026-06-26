---
name: dlazy-keling-tts
version: 1.2.0
description: Convert text into high-quality, emotional speech reading using Kling TTS.
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
    'openclaw': { 'systemPrompt': 'When invoking this skill, use dlazy keling-tts -h for help.' },
  }
---

# dlazy-keling-tts

[English](./SKILL.md) · [中文](./SKILL-cn.md)

Convert text into high-quality, emotional speech reading using Kling TTS.

## Trigger Keywords

- kling tts
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
Run the `dlazy keling-tts` command to get results.

```bash
dlazy keling-tts -h

Options:
  --prompt [prompt]                    Prompt
  --voice_language [voice_language]    Voice Language [default: zh] (choices: "zh", "en")
  --voiceId [voiceId]                  Voice ID Options depend on "voice_language". when voice_language="zh": genshin_vindi2 (阳光少年), zhinen_xuesheng (懂事小弟), tiyuxi_xuedi (运动少年), ai_shatang (青春少女), genshin_klee2 (温柔小妹), genshin_kirara (元气少女), ai_kaiya (阳光男生), tiexin_nanyou (幽默小哥), ai_chenjiahao_712 (文艺小哥), girlfriend_1_speech02 (甜美邻家), chat1_female_new-3 (温柔姐姐), girlfriend_2_speech02 (职场女青), cartoon-boy-07 (活泼男童), cartoon-girl-01 (俏皮女童), ai_huangyaoshi_712 (稳重老爸), you_pingjing (温柔妈妈), ai_laoguowang_712 (严肃上司), chengshu_jiejie (优雅贵妇), zhuxi_speech02 (慈祥爷爷), uk_oldman3 (唠叨爷爷), laopopo_speech02 (唠叨奶奶), heainainai_speech02 (和蔼奶奶), dongbeilaotie_speech02 (东北老铁), chongqingxiaohuo_speech02 (重庆小伙), chuanmeizi_speech02 (四川妹子), chaoshandashu_speech02 (潮汕大叔), ai_taiwan_man2_speech02 (台湾男生), xianzhanggui_speech02 (西安掌柜), tianjinjiejie_speech02 (天津姐姐), diyinnansang_DB_CN_M_04-v2 (新闻播报男), yizhipiannan-v1 (译制片男), guanxiaofang-v2 (元气少女), tianmeixuemei-v1 (撒娇女友), daopianyansang-v1 (刀片烟嗓), mengwa-v1 (乖巧正太); when voice_language="en": genshin_vindi2 (Sunny), zhinen_xuesheng (Sage), AOT (Ace), ai_shatang (Blossom), genshin_klee2 (Peppy), genshin_kirara (Dove), ai_kaiya (Shine), oversea_male1 (Anchor), ai_chenjiahao_712 (Lyric), girlfriend_4_speech02 (Melody), chat1_female_new-3 (Tender), chat_0407_5-1 (Siren), cartoon-boy-07 (Zippy), uk_boy1 (Bud), cartoon-girl-01 (Sprite), PeppaPig_platform (Candy), ai_huangzhong_712 (Beacon), ai_huangyaoshi_712 (Rock), ai_laoguowang_712 (Titan), chengshu_jiejie (Grace), you_pingjing (Helen), calm_story1 (Lore), uk_man2 (Crag), laopopo_speech02 (Prattle), heainainai_speech02 (Hearth), reader_en_m-v1 (The Reader), commercial_lady_en_f-v1 (Commercial Lady) [default: genshin_vindi2] [options depend on --voice_language; voice_language=zh: genshin_vindi2 (阳光少年), zhinen_xuesheng (懂事小弟), tiyuxi_xuedi (运动少年), ai_shatang (青春少女), genshin_klee2 (温柔小妹), genshin_kirara (元气少女), ai_kaiya (阳光男生), tiexin_nanyou (幽默小哥), ai_chenjiahao_712 (文艺小哥), girlfriend_1_speech02 (甜美邻家), chat1_female_new-3 (温柔姐姐), girlfriend_2_speech02 (职场女青), cartoon-boy-07 (活泼男童), cartoon-girl-01 (俏皮女童), ai_huangyaoshi_712 (稳重老爸), you_pingjing (温柔妈妈), ai_laoguowang_712 (严肃上司), chengshu_jiejie (优雅贵妇), zhuxi_speech02 (慈祥爷爷), uk_oldman3 (唠叨爷爷), laopopo_speech02 (唠叨奶奶), heainainai_speech02 (和蔼奶奶), dongbeilaotie_speech02 (东北老铁), chongqingxiaohuo_speech02 (重庆小伙), chuanmeizi_speech02 (四川妹子), chaoshandashu_speech02 (潮汕大叔), ai_taiwan_man2_speech02 (台湾男生), xianzhanggui_speech02 (西安掌柜), tianjinjiejie_speech02 (天津姐姐), diyinnansang_DB_CN_M_04-v2 (新闻播报男), yizhipiannan-v1 (译制片男), guanxiaofang-v2 (元气少女), tianmeixuemei-v1 (撒娇女友), daopianyansang-v1 (刀片烟嗓), mengwa-v1 (乖巧正太); voice_language=en: genshin_vindi2 (Sunny), zhinen_xuesheng (Sage), AOT (Ace), ai_shatang (Blossom), genshin_klee2 (Peppy), genshin_kirara (Dove), ai_kaiya (Shine), oversea_male1 (Anchor), ai_chenjiahao_712 (Lyric), girlfriend_4_speech02 (Melody), chat1_female_new-3 (Tender), chat_0407_5-1 (Siren), cartoon-boy-07 (Zippy), uk_boy1 (Bud), cartoon-girl-01 (Sprite), PeppaPig_platform (Candy), ai_huangzhong_712 (Beacon), ai_huangyaoshi_712 (Rock), ai_laoguowang_712 (Titan), chengshu_jiejie (Grace), you_pingjing (Helen), calm_story1 (Lore), uk_man2 (Crag), laopopo_speech02 (Prattle), heainainai_speech02 (Hearth), reader_en_m-v1 (The Reader), commercial_lady_en_f-v1 (Commercial Lady)]
  --speed [speed]                      Speed [default: 1.0] (choices: "0.8", "1.0", "1.5")
  --format [format]                    Format [default: mp3] (choices: "mp3", "wav")
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
    "tool": "keling-tts",
    "modelId": "keling-tts",
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
dlazy keling-tts --prompt 'prompt text'

# complex call:
dlazy keling-tts --prompt 'prompt text'
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
