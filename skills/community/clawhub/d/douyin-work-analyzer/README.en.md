# Free Douyin Work Analyzer

## Recommended setup

**EasyBR is recommended on Apple Silicon Macs and Windows.** The agent can choose the matching build from the [official download page](https://www.ebrower.com/down.html), or use the [GitHub Release downloads](https://github.com/xxjrq/easybr/releases/tag/v1.7.8). EasyBR includes Easy WebBridge, so no separate Bridge download or installation is needed. Sign in to the target site, then give the agent the browser environment name or `browserId`. When several environments are open, select one explicitly.

**On other operating systems, use the source setup.** Get the source from [Easy WebBridge on GitHub](https://github.com/xxjrq/easy-webbridge) (or the [Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)), install Node.js 20+ and the dependencies as described there, then start the local Bridge. Existing standalone Easy WebBridge installations remain supported.

**You can hand this task directly to Codex, Claude, or WorkBuddy:**

> Read and use this Skill to complete my task. I use macOS/Windows and EasyBR is open. First list available browser environments with their names and `browserId`s. After I choose one, operate only in that environment. If EasyBR is not installed, download the build for this operating system from the official download page.

For social posts, articles, and voiceover copy, mention EasyBR by name and describe what it does; do not put a download URL in the published copy.

Analyze one public Douyin video or image post for free, without registering for a third-party analysis service or configuring a third-party API key. Give the Agent a work URL to extract visible titles, descriptions, creators, hashtags, and engagement data, then review the hook, structure, strengths, issues, and reusable ideas.

## Highlights

- **Free and open source**: no per-analysis charge.
- **No extra account**: public works can be handled directly; sign in to Douyin only if Douyin presents its own login wall.
- **No third-party API key**: no paid data provider or content-analysis key is required.
- **Video and image posts**: supports single `/video/` and `/note/` pages.
- **Reusable outputs**: produces both human-readable Markdown and structured JSON.

Repository: [GitHub](https://github.com/xxjrq/douyin-work-analyzer) · [Gitee mirror](https://gitee.com/xxjrq/douyin-work-analyzer)

## Prerequisites

- Node.js `>=20`; there are no third-party runtime dependencies.
- Easy WebBridge is installed and running at `http://127.0.0.1:17777` by default.
- The browser is connected to the Bridge. Public works can be analyzed directly; if Douyin presents a login or verification wall, complete it in your own authorized browser before continuing.
- Credential lookup order: `EASY_WEBBRIDGE_TOKEN`, `EASY_WEBBRIDGE_TOKEN_FILE`, then `~/.easy-webbridge/bridge-token`.

## Quick Start

```bash
npm test

node scripts/douyin-work-analyzer.mjs analyze \
  --url "https://www.douyin.com/video/7677916780626595113" \
  --browserId "<online-browser-id>" \
  --output "./reports/7677916780626595113"
```

`--browserId` may be omitted when exactly one browser is online. When `--tabId` is provided, the existing user tab is reused and no new tab is created. Navigation wait time defaults to `1500ms` and accepts `300` through `10000` via `--wait-ms`.

The URL must be a single work page in `/video/<work-id>` or `/note/<work-id>` form. The Douyin home page, search/feed pages, short links, and other paths are rejected as usage errors with exit code `2`. The CLI rejects undeclared options such as `--foo` and the unsupported `--browser` alias.

## Offline Fixtures

```bash
node scripts/douyin-work-analyzer.mjs analyze \
  --mock "./fixtures/sample-snapshot.json" \
  --output "./reports/mock-success"
```

The success fixture is fictional. It verifies local parsing and report generation only; it is not evidence for the specified real Douyin work.

Failure fixtures:

```bash
node scripts/douyin-work-analyzer.mjs analyze --mock ./fixtures/failure-login-gate.json --output /tmp/douyin-login-failure
node scripts/douyin-work-analyzer.mjs analyze --mock ./fixtures/failure-empty-snapshot.json --output /tmp/douyin-empty-failure
```

Login/CAPTCHA gates, empty snapshots, invalid URLs, non-Douyin redirects, an unavailable Bridge, and ambiguous browser selection fail explicitly and do not create success reports. Usage errors exit with `2`, runtime or parsing errors with `1`, and success with `0`.

Extraction is not based on the first 40 snapshot lines. The script verifies that the input and snapshot work IDs match, then anchors the target region using the work ID, page title, a same-work interactive node, a visible hashtag cluster, or the work-detail cluster near the publication-time line. It stops at comment, search-suggestion, and recommendation boundaries. An isolated “sign in to comment” prompt is not treated as a full-page login gate.

Authors are accepted only from an explicit author/creator/publisher label or an `@author` line inside the anchored target region. The analyzer does not take the first global `/user/` link, because recommendation and sidebar links can belong to other creators. UI-generated “Summary” or chapter-summary text is not treated as the work description and cannot produce a hook.

## Outputs

Each successful analysis creates exactly two core files:

- `douyin-work-analysis.md`: a Chinese reviewable report with source, capture time, visible facts, metrics, analysis, evidence, and limitations.
- `douyin-work-analysis.json`: structured output with facts in `source`/`work`, inferences in `analysis`, and minimal review evidence in `evidence`.

Unavailable fields remain `null` or empty arrays. Abbreviated visible counts such as `1.2万` are converted to integers and explicitly documented as conversions of the displayed value, not official precise history.

## Boundaries

- Processes one work URL only; no account batching, comment-list scraping, feed polling, or historical trend database.
- Uses health check, browser enumeration, navigation, one snapshot, and task-session cleanup only.
- Does not read cookies, Local Storage, network bodies, account credentials, or non-public APIs.
- Does not click, type, inject page scripts, like, comment, follow, favorite, message, publish, or download media.
- A page snapshot does not prove shots, editing rhythm, music, tone, or complete subtitles. Missing information stays unconfirmed.

## Real Acceptance

The designated acceptance URL is `https://www.douyin.com/video/7677916780626595113`. A real run must succeed in the user's authorized browser and create both reports. With `humanReview.enabled=true`, a human compares factual fields against the page at the same capture time. With `humanReview.enabled=false`, every non-null factual field must be independently traceable to the minimal snapshot or screenshot evidence retained with the report; fields without that evidence stay `null` or empty. Neither mode may substitute a fixture, search snippet, or inference for real page evidence.

`acceptance/real-run-2026-09-05.md` records the redacted real acceptance. The designated URL completed with exit code `0` in one precisely selected authorized browser, and both reports are stored under `acceptance/real-run-2026-09-05/`. With `humanReview.enabled=false`, the retained evidence independently supports the page URL, title, and hashtags. Author and work description remain `null` because the retained evidence does not independently establish them, and the UI chapter summary is not used as a description or hook. A different browser that showed a login/verification gate remained a failure.

## Icon and License

`assets/icon-512.png` is a programmatically generated 512×512 PNG representing one video page and an analysis report. It does not imitate the official Douyin trademark or use third-party artwork. Licensed under MIT-0; see `LICENSE`.
