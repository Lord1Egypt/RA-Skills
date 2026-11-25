# Free Douyin Live Monitor

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. If you specify a browser name or `browserId`, the agent uses an exact match; if you specify none and exactly one browser is online, it may use that browser. With several online environments, choose one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/aiispower/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list online browser environments. If I did not specify a target and exactly one is online, use it; if I did not specify a target and several are online, show their names and `browserId`s and wait for my choice. If I specify a browser name or `browserId`, use only that exact match and stop if it is unavailable. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Poll publicly visible Douyin live rooms only for a user-specified, bounded period, record status/title/visible signals, and report changes during the active task. Without a duration, it takes one snapshot. There is no background monitor, desktop/email/mobile notification, or reminder after the task ends.

Use an exact online browser-name or `browserId` match when the user specifies one. With no selection, use a browser only if exactly one is online; otherwise stop and ask the user to choose. If a specified browser is offline or mismatched, stop and never switch accounts. Read public page fields only; do not collect cookies, tokens, private messages, or creator-dashboard data. Save only requested results to the user-selected directory and strip query strings from room URLs. Stop at login, verification, or security challenges.

Requires [Easy WebBridge](https://github.com/aiispower/easy-webbridge), with a [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge) available.

This repository has no persistent monitor or notification program. `npm test` checks sample data and documentation constraints; it does not open a browser or perform a live check.
