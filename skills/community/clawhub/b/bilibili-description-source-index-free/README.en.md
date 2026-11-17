# Bilibili Description Source Index

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [official EasyBR downloads page](https://www.ebrower.com/down.html). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/aiispower/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Turn public resource links visible in the descriptions of 1–3 specified Bilibili videos into a traceable index. Provide the video URLs and an Easy WebBridge `browserId`; the result records each visible link, its visible purpose, access status, source, and honest gaps.

![Promo](assets/promo.png)

## Install

```bash
npx skills add xxjrq/bilibili-description-source-index-free
```

This browser skill requires [Easy WebBridge on GitHub](https://github.com/aiispower/easy-webbridge), with a [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge). It uses the browser environment selected by the user, creates one task-owned session/group, and never takes over existing tabs.

## Input and output

Input: a user-provided `browserId`, 1–3 Bilibili video URLs, and optional local formatting instructions.

Output: a draft JSON/table with `source_video`, `url`, `purpose`, `access`, and `evidence`; `gaps` records hidden descriptions, login requirements, or failed links. It is read-only by default. Draft filling requires explicit permission and never clicks a final publish/send action.

Only visible page content is handled. Login, CAPTCHA, and risk controls are recorded and stop the affected page; they are never bypassed. The maximum is 100 rows per run.

## Verify

```bash
node scripts/self-test.mjs
```

Fixtures are offline page simulations, not online collection results.

## License and attribution

The browser-use context references [OpenCLI](https://github.com/jackwener/OpenCLI) and its [Bilibili adapter notes](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/bilibili.md). No source implementation is copied. Licensed under [MIT-0](LICENSE).

## EasyBR AI onboarding and task completion

Read the official [EasyBR AI operation guide](https://www.ebrower.com/helperdoc/ai-agent-workflow.html);  current EasyBR builds includes the Bridge and browser extension on Apple Silicon Macs and Windows, so no separate Bridge installation is needed there. Ordinary browsers and other systems should follow the current Easy WebBridge setup described in the official guide.

For a browser task the user has authorized through this Skill, check and reuse a suitable existing environment first. If a new one is genuinely needed, create one unique environment for this task with safe defaults, read back its actual environment ID, and start it. Do not ask the user to reconfirm or supply an environment name or default parameters. After confirming the correct account and `browserId`, continue the user's current task instead of stopping at setup instructions; do not ask for approval at each necessary step. Pause only for CAPTCHA/account security checks, real ambiguity about the target account or authorization, or missing local-control capability. At completion, close only the task tab group created for this run and report results and limits under this Skill's rules.

This Skill provides the business workflow. Automatic installation, sign-in assistance, and environment management also depend on the AI agent's local-control capabilities and the components described in the official guide.
