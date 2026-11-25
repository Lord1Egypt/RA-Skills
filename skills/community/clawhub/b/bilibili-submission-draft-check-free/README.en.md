# Bilibili Submission Draft Check

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Read-only preflight checking for a Bilibili submission draft you already opened yourself. It identifies missing cover, title, description, category, and assets, then returns actionable suggestions with visible-page sources. It never saves, submits, or publishes; it stops when account, draft ownership, or page identity is unclear.

![Promotional image](assets/promo-1600x900.png)

## Input and result

Provide a user-selected `browserId`, an already-open draft owned by you, and its visible page content. The result is a field checklist containing observed values, omissions, suggestions, and a source for each observation. Process up to 100 asset/table rows per run; split larger work into batches.

## Install

```bash
npx skills add xxjrq/bilibili-submission-draft-check-free
```

## Browser prerequisite

Install Easy WebBridge first: [GitHub](https://github.com/xxjrq/easy-webbridge) is the primary download and [Gitee](https://gitee.com/xxjrq/easy-webbridge) is the fallback. Choose exactly one user-provided `browserId` per task and use an owned session group only—never broadcast across accounts.

The Skill reads visible web content only. It pauses for login, CAPTCHA, risk-control, security challenges, or unclear ownership. It never fills, saves, submits, or publishes, so platform auto-save cannot alter the draft.

## Local self-test

```bash
node scripts/self-test.mjs
```

Fixtures are explicitly offline page-note simulations, not evidence of online collection.

## License and reference

Licensed under [MIT-0](LICENSE). Scope reference only: [social-media-skills/skills](https://github.com/social-media-skills/skills) and its [metadata Skill](https://github.com/social-media-skills/skills/blob/main/skills/youtube-publishing-and-metadata/SKILL.md). No external implementation or prose was copied.

## Unconfirmed offline fields

“未确认” (unconfirmed) remains missing, never visible content. [All-unconfirmed input](fixtures/failure-all-unconfirmed.json) → [actual script result](fixtures/failure-all-unconfirmed-result.json); [title-only confirmed input](fixtures/success-unconfirmed-mixed.json) → [actual result](fixtures/success-unconfirmed-mixed-result.json). Every field retains its source. These are offline simulations.
