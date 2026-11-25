# Douyin Multi-Account Workbench

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Run public, read-only Douyin research for explicitly selected EasyBR browser environments and aggregate the results by account. Each account keeps its own browser ID, session group, evidence links, status, and script draft.

The four atomic skills are optional per task and are not bundled. If one is missing, only its task is reported as `unavailable`; the report includes the repository and install command, and the workbench continues with other selected tasks. The built-in `script` draft needs no atomic skills and can run on its own. Run `node scripts/workbench.mjs dependencies` to check what is installed. See the [dependency install guide](DEPENDENCIES.md) for the public repositories and commands. The workbench never stores credentials or performs comments, messages, submissions, or publishing.
