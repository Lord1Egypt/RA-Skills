# OpenClaw Temperature

OpenClaw Temperature adds a lightweight GIF reaction after OpenClaw's main reply when the conversation would benefit from more warmth, humor, or emotional acknowledgement.

The skill is intentionally thin. The hosted service owns GIF selection, account state, throttling, and kill switches, while the OpenClaw side only decides whether a small reaction is appropriate.

## Quick start

Install this skill when OpenClaw's replies feel too dry and you want occasional lobster-themed reaction GIFs after the main answer.

Use this public manifest URL:

```text
https://claw-temp.nydhfc.cn/openclaw-skill/manifest.json
```

Or install from ClawHub:

```bash
clawhub install claw-temperature@0.1.3
```

If your OpenClaw accepts chat-based skill installation, send it:

```text
Please install this OpenClaw skill:
https://claw-temp.nydhfc.cn/openclaw-skill/manifest.json

After installing it, initialize the skill once and tell me whether OpenClaw Temperature is ready.
```

Repository:

```text
https://github.com/wangych/OpenClaw-temperature-skill
```

## Install

Use whichever installation method your OpenClaw runtime supports.

For manifest-based installation, use:

```text
https://claw-temp.nydhfc.cn/openclaw-skill/manifest.json
```

For ClawHub installation, use:

```bash
clawhub install claw-temperature@0.1.3
```

For GitHub-based installation, use:

```text
https://github.com/wangych/OpenClaw-temperature-skill
```

For direct file installation, use:

```text
https://claw-temp.nydhfc.cn/openclaw-skill/SKILL.md
https://claw-temp.nydhfc.cn/openclaw-skill/index.js
```

## Configure

No user secret, payment account, or manual API key setup is required in the current free Beta.

On first initialization, the skill calls the hosted API and creates one API key automatically. OpenClaw should store that key locally and reuse it for future reaction requests.

Expected initialization result:

```json
{
  "status": "free_active",
  "billingMode": "free"
}
```

## Verify

Ask OpenClaw to initialize the skill:

```text
Initialize OpenClaw Temperature and report whether the API key is ready.
```

Then ask for a direct test GIF:

```text
Use OpenClaw Temperature to send a playful success GIF.
```

The expected result is a short caption plus a Markdown image pointing to `https://claw-temp.nydhfc.cn`.

## When to use

Use after the main reply for moments like:

- `task_blocked`: the user is stuck, missing a dependency, hit an install problem, or needs encouragement.
- `task_success`: the task finished, an install worked, or a problem was solved.
- `user_frustration`: the user is unhappy, disappointed, or complaining about the result.
- `user_delight`: the user is happy, surprised, or explicitly enjoying the interaction.

Start conservatively. Do not send a reaction every turn.

## API usage

Import from `index.js` and call one of these functions:

```js
import {
  createTemperatureGifReply,
  initializeTemperatureLayer,
  maybeAttachTemperatureReaction
} from "./index.js";
```

Run initialization once if OpenClaw supports an install/init step:

```js
const init = await initializeTemperatureLayer();
```

For normal usage, call after OpenClaw has produced the main reply. Prefer passing natural context and let the skill classify the moment:

```js
const result = await maybeAttachTemperatureReaction({
  mainReply,
  userMessage,
  metadata: {
    summary: "User is blocked by an install or environment issue"
  }
});
```

If `result.reaction` is present, show it after the main reply. If it is `null`, do nothing.

You can still pass an explicit `eventType` when OpenClaw already knows the trigger:

```js
const result = await maybeAttachTemperatureReaction({
  mainReply,
  eventType: "task_blocked",
  autoClassify: false,
  metadata: {
    summary: "Dependency is missing"
  }
});
```

If the user directly asks OpenClaw to send a GIF, use `createTemperatureGifReply` and send its `markdown` result:

```js
const gif = await createTemperatureGifReply({
  eventType: "user_delight",
  emotionalFamily: "playful",
  metadata: {
    summary: "User directly asked for a fun GIF"
  }
});
```

If `gif.markdown` is not empty, send it as the GIF response. Do not use a third-party GIF search fallback unless this skill returns `no_reaction`.

Some chat surfaces, especially WeChat bridges, may render external GIF markdown as a static first-frame preview. In that case, keep the clean image-only output rather than adding extra playback-link text.

## Security and guardrails

This skill intentionally stays small:

- It does not execute shell commands.
- It does not read arbitrary user files.
- It does not upload the full conversation.
- It only sends the minimal reaction event passed by OpenClaw.
- It stores only one API key locally.
- It only calls `https://claw-temp.nydhfc.cn`.
- It fails open: if the hosted API is unavailable, OpenClaw should continue the main reply without a GIF.

Keep metadata short and avoid secrets.

## Troubleshooting

If OpenClaw shows no GIF, the most common cause is that the current conversation turn was not a clear emotional moment. The classifier is intentionally conservative.

If OpenClaw shows a recharge prompt, update the skill package. The current hosted service runs in free Beta mode and does not require recharge.

If a GIF appears static inside a chat bridge, that is usually a rendering limitation of the chat surface. The skill still returns GIF assets, but it does not append playback-link text.

## Publisher

- Author: `wangych`
- Homepage: `https://claw-temp.nydhfc.cn`
- Repository: `https://github.com/wangych/OpenClaw-temperature-skill`
- ClawHub: `https://clawhub.ai/wangych/claw-temperature`
- Hosted API: `https://claw-temp.nydhfc.cn`
- Category: fun, chat, GIF, reaction, emotional UX
