# Bilibili Single-Video Chapter Notes

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [official EasyBR downloads page](https://www.ebrower.com/down.html). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/aiispower/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Turn the chapters, subtitles, or summary already visible on one Bilibili video page into evidence-backed learning notes. Every delivered row points back to visible page text, a timestamp when available, and the video URL. If subtitles or a summary are not visible, the skill reports only the visible title and missing material—it never claims to have watched the video.

## Input and output

Provide a video URL, learning goal, and a user-selected Easy WebBridge `browserId`. The output is a Markdown chapter/timestamp table with notes, page evidence, collection scope, and gaps. It processes at most 100 visible rows per run.

## Install

```bash
npx skills add xxjrq/bilibili-video-chapter-notes-free
```

This browser skill uses EasyBR with built-in Easy WebBridge on Apple Silicon Macs and Windows, following the official guide. For ordinary browsers, follow the [official EasyBR AI operation guide](https://www.ebrower.com/helperdoc/ai-agent-workflow.html) to connect standalone Easy WebBridge; source is available from [GitHub](https://github.com/aiispower/easy-webbridge) and [Gitee](https://gitee.com/xxjrq/easy-webbridge). Use only the requested `browserId` and keep each task in its own session/tab group.

The workflow is read-only by default, does not bypass sign-in, CAPTCHA, or risk controls, and never downloads or transcribes video media. Offline fixtures and the self-test validate rendering behavior only; they are not online collection results.

```bash
bash scripts/self-test.sh
```

See [SOURCES.md](SOURCES.md) for reference attribution and [LICENSE](LICENSE) for licensing.

## EasyBR AI onboarding and task completion

Read the official [EasyBR AI operation guide](https://www.ebrower.com/helperdoc/ai-agent-workflow.html);  current EasyBR builds includes the Bridge and browser extension on Apple Silicon Macs and Windows, so no separate Bridge installation is needed there. Ordinary browsers and other systems should follow the current Easy WebBridge setup described in the official guide.

For a browser task the user has authorized through this Skill, check and reuse a suitable existing environment first. If a new one is genuinely needed, create one unique environment for this task with safe defaults, read back its actual environment ID, and start it. Do not ask the user to reconfirm or supply an environment name or default parameters. After confirming the correct account and `browserId`, continue the user's current task instead of stopping at setup instructions; do not ask for approval at each necessary step. Pause only for CAPTCHA/account security checks, real ambiguity about the target account or authorization, or missing local-control capability. At completion, close only the task tab group created for this run and report results and limits under this Skill's rules.

This Skill provides the business workflow. Automatic installation, sign-in assistance, and environment management also depend on the AI agent's local-control capabilities and the components described in the official guide.
