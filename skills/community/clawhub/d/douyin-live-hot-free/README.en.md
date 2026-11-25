<div align="center">

<img src="assets/icon-512.png" width="112" height="112" alt="Douyin Live Hot Free icon">

# Douyin Live Hot Free

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

## Free Douyin keyword search for AI agents

Let Claude Code, Codex, OpenCode, WorkBuddy, and other Agent Skills-compatible agents reuse a logged-in browser, search current Douyin Selected content, and export JSON, Markdown, and searchable HTML reports.

[简体中文](README.md) | [English](README.en.md)

</div>

## What it does

- Searches current Douyin Selected content for any keyword.
- Reads visible titles, authors, content types, publication text, and displayed likes.
- Scrolls only as needed for the requested result count.
- Exports normalized JSON, a Markdown table, and a searchable HTML report.
- Keeps each run in one browser task group and closes only that group afterward.

## How the repositories work together

```text
Claude Code / Codex / OpenCode / WorkBuddy
                    |
         douyin-live-hot-free Skill
           search + normalize + report
                    |
          Easy WebBridge 127.0.0.1:17777
                    |
       browser extension + logged-in Douyin Selected
```

This repository owns the Douyin search workflow. [Easy WebBridge](https://github.com/xxjrq/easy-webbridge) owns the real-browser connection. They are independent repositories connected through the local HTTP API, with no dependency on an author-specific filesystem path.

## Install

Install and configure Easy WebBridge once:

```bash
git clone https://github.com/xxjrq/easy-webbridge.git
cd easy-webbridge
npm install
node cli/easy-webbridge.mjs start
```

Load its extension in a Chromium profile already logged in to Douyin Selected. Then install this Skill:

```bash
npx skills add xxjrq/douyin-live-hot-free
```

Universal manual location:

```bash
git clone https://github.com/xxjrq/douyin-live-hot-free.git ~/.agents/skills/douyin-live-hot-free
```

## Check and run

```bash
node scripts/douyin-live-hot-free.mjs list
```

```bash
node scripts/douyin-live-hot-free.mjs search \
  --keyword "AI tools" \
  --browser "Creator" \
  --limit 20 \
  --output /absolute/path/to/output
```

## Prompt

```text
Use Douyin Live Hot Free in my logged-in browser to search for “AI tools”, collect the first 20 current results, and export JSON, Markdown, and HTML reports.
```

“Live” means a point-in-time snapshot of the visible search page. It is not an official Douyin ranking or historical trend dataset.

## License

[MIT-0](LICENSE)
