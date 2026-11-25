# Free Douyin Hot Topic Planner

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

**Free to use, no third-party content API key, reuses your browser login, and returns five practical Douyin topic ideas per run.**

Provide an account niche, audience, content pillars, and optional keywords. The Skill returns the currently visible sources plus five ideas, each with a title, 3-second hook, angle, account fit, three-part outline, and source citation. EasyBR profiles remain isolated: one browser environment per run.

## What it does

- Collects the target account's currently visible Douyin hot-page and optional search signals.
- Produces exactly five ideas instead of an unfiltered topic dump.
- Connects every idea to visible source evidence.
- Auto-selects the browser only when exactly one is online; otherwise it requires an explicit browser selection.

## Get started

Install and start Easy WebBridge from [GitHub](https://github.com/xxjrq/easy-webbridge), or use the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge) when GitHub is unavailable. Sign in to Douyin in the intended browser or EasyBR profile.

Ask your AI agent:

> Use $douyin-hot-topic-maker-free. My account reviews AI tools for office workers. My pillars are tool walkthroughs and workflows, and my optional keyword is AI tools. Give me five practical ideas from the pages currently visible to this browser.

The minimum request is in `fixtures/request-valid.json`. Run:

```bash
npm test
node scripts/douyin-hot-topic-maker-free.mjs collect --request ./request.json --output ./output/account
node scripts/douyin-hot-topic-maker-free.mjs validate-plan --snapshot ./output/account/research-snapshot.json --draft ./plan-draft.json --output ./output/account
```

One online browser is selected automatically. If several are online, run `node scripts/douyin-hot-topic-maker-free.mjs list` and add the chosen `browserId` to the request.

## Boundaries

“Free” means the Skill does not call Douyin or paid third-party content data APIs. Local model, browser, and network costs may still apply. Results reflect only the selected account, region, experiment, and collection time. They are not an official global ranking, a viral-content promise, or an automatic publishing service.

The Skill does not read or expose cookies, tokens, or login identity, and it never bypasses login, CAPTCHA, or risk controls. Handle any challenge manually in the selected browser, then retry.

## Agent compatibility

This is a standard `SKILL.md` skill and is not limited to OpenAI or any single agent. Codex, Claude, WorkBuddy, OpenCode, and other tools that support Skills can follow the same instructions.

MIT-0 License. See [LICENSE](LICENSE).
