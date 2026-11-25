# Bilibili Channel Update Digest

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Turn up to 10 videos currently visible on a specified Bilibili creator page into a traceable update digest. Provide one connected `browserId` and the creator-page URL; the result contains title, displayed date, topic, link, per-item source, and omissions. Missing dates stay blank—this Skill never invents upload times or view counts.

![Promo](assets/promo.png)

## Input and result

Input: one explicit `browserId`, one creator-page URL, and a limit of up to 10 currently visible videos.

Result: a copyable Markdown table with title, date, topic, link, visible source, and limits. It is a one-off digest, not monitoring or private-analytics automation.

## Install

```bash
npx skills add xxjrq/bilibili-channel-update-digest-free
```

This browser Skill requires [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge); use the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge) when needed. Choose one browser environment at runtime. Each run owns only its own session group and never takes over existing pages or other accounts.

## Validation

Run `node scripts/self-test.mjs`. Fixtures simulate offline page material only; they are not online collection results.

## License and reference

Published under [MIT-0](LICENSE). Business-use references: [Easy WebBridge](https://github.com/xxjrq/easy-webbridge) and its [Bilibili adapter](https://github.com/xxjrq/easy-webbridge/blob/main/docs/adapters/browser/bilibili.md). No implementation or text has been copied.
