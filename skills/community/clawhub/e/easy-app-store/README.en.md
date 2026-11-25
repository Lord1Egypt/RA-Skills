<div align="center">

<img src="assets/icon-512.png" width="112" height="112" alt="easyAppStore icon">

# easyAppStore

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

## App Store Connect release automation for AI agents

Let Claude Code, Codex, OpenCode, WorkBuddy, and other Agent Skills-compatible agents inspect an iOS project, build and upload it, complete App Store Connect metadata, submit it for review, verify status, and handle rejections.

[简体中文](README.md) | [English](README.en.md)

</div>

## What it does

- Detects Xcode, Flutter, React Native, Unity, and Fastlane projects.
- Chooses project-appropriate Release commands and prepares an IPA.
- Uploads builds, icons, screenshots, preview videos, and review attachments.
- Completes listing metadata, privacy, age rating, compliance, and review information.
- Selects the correct build, submits App Review, and verifies the actual status.
- Reads rejection details and routes the fix to code, assets, metadata, or review notes.

## How the repositories work together

```text
Claude Code / Codex / OpenCode / WorkBuddy
                    |
             easyAppStore Skill
          build decisions + release workflow
                    |
          Easy WebBridge 127.0.0.1:17777
                    |
       browser extension + logged-in App Store Connect
```

`easyAppStore` is an independent business Skill. [Easy WebBridge](https://github.com/xxjrq/easy-webbridge) is the shared browser runtime installed once for every browser-based business Skill. The Skill talks to the local runtime over HTTP and never depends on a repository path from the author's computer.

## Install

Install and configure Easy WebBridge once:

```bash
git clone https://github.com/xxjrq/easy-webbridge.git
cd easy-webbridge
npm install
node cli/easy-webbridge.mjs start
```

Load its extension in the Chromium profile that is already logged in to App Store Connect. Then install this Skill:

```bash
npx skills add xxjrq/easy-app-store
```

Universal manual location:

```bash
git clone https://github.com/xxjrq/easy-app-store.git ~/.agents/skills/easy-app-store
```

The root [`SKILL.md`](SKILL.md) is the cross-agent entry point. [`agents/openai.yaml`](agents/openai.yaml) is optional Codex UI metadata and is not required at runtime.

## Preflight

```bash
node scripts/easy-webbridge-client.mjs preflight
```

The command verifies Node.js, the Easy WebBridge runtime, its local token, and connected browsers without exposing credentials. It does not verify the App Store Connect login, team/app identity, Xcode signing, or build status; confirm those in the selected project and live browser session.

## Prompt

```text
Use easyAppStore to release the iOS app at /absolute/project/path to the App Store. Reuse my logged-in App Store Connect browser, build and upload the app, complete the listing and review information, submit it, and report the final status.
```

## Requirements

- Node.js 20+
- macOS and the build tools required by the iOS project
- Easy WebBridge 0.3.2+
- A Chromium browser profile already logged in to App Store Connect

## License

[MIT-0](LICENSE)
