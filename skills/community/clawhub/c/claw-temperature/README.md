# OpenClaw Temperature Skill

OpenClaw Temperature adds a lightweight GIF reaction after OpenClaw's main reply when the moment deserves more warmth.

The skill is intentionally thin. The hosted service owns GIF selection, account state, throttling, and kill switches.

## Install

Recommended ClawHub installation:

```bash
clawhub install claw-temperature@0.1.3
```

If your OpenClaw can install skills from GitHub, use this repository:

```text
https://github.com/wangych/OpenClaw-temperature-skill
```

If your OpenClaw supports CLI-style installation, try:

```bash
openclaw skills install github:wangych/OpenClaw-temperature-skill
```

If your OpenClaw only accepts chat instructions, send it this:

```text
Please install this OpenClaw skill:
https://claw-temp.nydhfc.cn/openclaw-skill/manifest.json

After installing it, run its initialization once and tell me whether the API key is ready.
```

If your OpenClaw supports direct file URLs, use:

```text
https://claw-temp.nydhfc.cn/openclaw-skill/SKILL.md
https://claw-temp.nydhfc.cn/openclaw-skill/index.js
```

## Free Beta

The first run automatically creates an API key. The current Beta is free and does not require recharge.

Initialization returns a free-mode result like:

```json
{
  "status": "free_active",
  "billingMode": "free"
}
```

If an older installation still shows a recharge prompt, update the skill package. The `/recharge` page now explains that the service is free.

## Recommended Triggers

Start with only these:

- `task_blocked`
- `task_success`
- `user_frustration`
- `user_delight`

Do not call this skill on every turn. It is designed for occasional emotional value, not constant animation.

## Auto Classification

For normal after-reply usage, OpenClaw can pass natural context and let the skill map it to the supported event taxonomy:

```js
import { maybeAttachTemperatureReaction } from "./index.js";

const result = await maybeAttachTemperatureReaction({
  mainReply,
  userMessage,
  metadata: {
    summary: "Short non-sensitive context"
  }
});
```

The classifier is intentionally conservative. If it does not see a clear success, blocked-task, frustration, or delight signal, it returns `no_reaction` without calling the hosted API.

## Direct GIF Requests

If the user directly asks OpenClaw to send a GIF, call `createTemperatureGifReply`:

```js
import { createTemperatureGifReply } from "./index.js";

const gif = await createTemperatureGifReply({
  eventType: "user_delight",
  emotionalFamily: "playful",
  metadata: {
    summary: "User directly asked for a fun GIF"
  }
});
```

Send `gif.markdown` if it is not empty.

If the chat surface renders external GIF markdown as a static preview, keep the clean image-only output. Do not append extra playback-link text.

## Security Notes

This skill:

- Does not execute shell commands.
- Does not read arbitrary files.
- Does not upload full conversations.
- Stores only its API key.
- Calls only `https://claw-temp.nydhfc.cn`.

Keep `metadata` short and never include secrets.
