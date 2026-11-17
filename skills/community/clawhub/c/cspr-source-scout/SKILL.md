---
name: source-scout
description: Collect fresh cross-source recommendation candidates for cspr using profile memory, feeds, search, Agent-Reach, and optional subagents.
---

# source-scout

Use this skill when a user asks for a daily, weekly, or monthly discovery run.

Core rule: `history_context.json is preference evidence, not a candidate source`. Do not recommend URLs copied from browser-history samples. Use history only to understand interests, source preferences, and already-seen penalties.

Workflow:

1. Read `profile.yaml` from the run folder or `~/.cspr/memory/profile.yaml`.
2. Read `history_context.json` only to infer what the user cares about. Do not turn sampled history URLs into candidate items.
3. Read `potential_sources.yaml` when present. Treat repeated creators, channels, subreddits, UPs, or posters as preferred source candidates, not permanent subscriptions.
4. Generate fresh source queries from durable interests, recent context, and potential sources. Do not reuse old `search_queries` from profile memory.
5. Run `feed-scan collect` for RSS/RSSHub candidates when feeds are configured.
6. Use Agent-Reach as a first-class discovery path, not just as a fallback phrase in notes.

   - If `agent-reach` is available, run `agent-reach doctor` and write the availability plus actual commands/routes used to `RUN/agent_reach_tool_report.md`.
   - Also write `RUN/agent_reach_tool_attempts.jsonl`. One JSON object per attempted route:

     `{"route":"agent-reach:youtube:yt-dlp","tool":"yt-dlp","command":"yt-dlp --dump-json ytsearch5:...","status":"success|failed|blocked|unavailable","output_file":"...","reason":"..."}`

   - Attempt every Agent-Reach route below at least once before finalizing candidates. Keep each attempt compact; use 3-5 results when a route supports limits. If a tool requires missing login/cookies/API keys, record `status:"unavailable"` with the command or doctor evidence and the reason. Do not mark a route as skipped unless the user explicitly disables it.
     - Web page read: `curl -s "https://r.jina.ai/URL"`; label `agent-reach:web:jina`.
     - Exa web search: `mcporter call 'exa.web_search_exa(...)'`; label `agent-reach:web-search:exa`.
     - Twitter/X: `bird search`, `bird user-tweets`, or `bird read`; label `agent-reach:twitter:bird`.
     - Reddit/community: `rdt search`, `rdt-cli search`, or Reddit JSON API; label `agent-reach:reddit:rdt-cli` or `agent-reach:reddit:curl`.
     - YouTube/video: `yt-dlp --dump-json "ytsearch5:query"`; label `agent-reach:youtube:yt-dlp`.
     - Bilibili/video: `bili search`, `bili hot`, `bili rank`, or `yt-dlp`; label `agent-reach:bilibili:bili-cli` or `agent-reach:bilibili:yt-dlp`.
     - GitHub/dev: `gh search repos`, `gh search code`, or `gh issue list`; label `agent-reach:github:gh`.
     - XiaoHongShu/social: `mcporter call 'xiaohongshu.search_feeds(...)'` plus `agent-reach format xhs`; label `agent-reach:xiaohongshu:mcporter`.
     - Douyin/video: `mcporter call 'douyin.parse_douyin_video_info(...)'` or download-link tool; label `agent-reach:douyin:mcporter`.
     - WeChat articles: `miku_ai` search or WeChat article reader; label `agent-reach:wechat:miku_ai` or `agent-reach:wechat:camoufox`.
     - Weibo/social: `mcporter call 'weibo.search_content(...)'` or trend/feed APIs; label `agent-reach:weibo:mcporter`.
     - Xiaoyuzhou podcast: transcribe script or availability check; label `agent-reach:xiaoyuzhou:transcribe`.
     - LinkedIn: `mcporter call 'linkedin.search_people(...)'` or profile fetch; label `agent-reach:linkedin:mcporter`.
     - V2EX: public JSON API hot/node routes; label `agent-reach:v2ex:curl`.
     - Xueqiu: Python channel stock quote/hot posts/search; label `agent-reach:xueqiu:python`.
     - RSS/feedparser: feedparser route; label `agent-reach:rss:feedparser` unless the item already came from `feed-scan collect`.
   - If an Agent-Reach route fails, write the command, exit status, and short reason to `RUN/agent_reach_blockers.md`. Do not silently convert that failed route into `web_search`.
   - If all surviving candidates are from `web_search` while Agent-Reach routes are available, run another Agent-Reach route pass or write `RUN/agent_reach_blockers.md` explaining why platform-route candidates were unusable.

   If the environment exposes `web_search`, use it for at least one open-web discovery pass per high-priority topic, but do not let web search replace Agent-Reach route coverage.
7. Use subagents when the active agent environment supports them. Choose the subagent model at run time by checking the current model registry, task needs, and any current leaderboard/model-quality evidence supplied in the run task. Do not hardcode model IDs in this skill.

    - open-web scout: web_search / Exa / general web
    - video scout: YouTube, Bilibili, transcripts, channel feeds
    - community scout: Reddit, GitHub, Hacker News, V2EX, X/Twitter where available
    - feed scout: configured RSS/RSSHub/subscription sources

   Each subagent should return normalized JSONL candidates or source-specific raw notes. If subagents are unavailable, run these passes sequentially.

   When subagents are used, record child session keys, task names, selected model, and output files in `RUN/subagent_report.md`. If the environment appears to support subagents but no real delegation tool call succeeds, write `RUN/subagent_blockers.md` and do not claim that subagents were used.
   Keep the post-subagent merge/editor phase as a low-context finishing pass: rely on child output files and compact counts, not large conversational transcripts. Do not load child session transcripts unless debugging a failed child; resume or launch a fresh finishing pass if the parent session context becomes large.
8. Normalize Agent-Reach and search results into `reach_candidates.jsonl` using the cspr item schema. Each item should include metadata fields when known: `discovery_method`, `source_query`, `source_tool`, `retrieved_by`, `freshness_reason`, and `why_candidate`.

   Required discovery metadata:

   - `metadata.discovery_method`: exact discovery route, e.g. `agent-reach:reddit:rdt-cli`, `agent-reach:youtube:yt-dlp`, `agent-reach:github:gh`, or `web_search`.
   - `metadata.source_query`: the query, feed route, channel, subreddit, or source URL used.
   - `metadata.source_tool`: executable/tool name, e.g. `rdt-cli`, `rdt`, `yt-dlp`, `bili-cli`, `gh`, `mcporter`, `curl+jina`, `web_search`.
   - `metadata.tool_output_file`: optional path to raw or cleaned output used to create the item.

   For every candidate produced from Agent-Reach or an Agent-Reach upstream tool, set either top-level `discovery_method` or `metadata.discovery_method` to an `agent-reach:` value so the editor can print `Found via:` accurately.
9. Merge feed and Agent-Reach candidates while filtering already-seen browser-history URLs:

    itembox merge --seen RUN/seen_urls.jsonl --out RUN/items.jsonl RUN/rss_candidates.jsonl RUN/reach_candidates.jsonl

10. Run deterministic discovery-route validation before handing off to news-editor:

    itembox validate-routes --in RUN/items.jsonl --agent-reach-report RUN/agent_reach_tool_report.md --agent-reach-attempts RUN/agent_reach_tool_attempts.jsonl --check-agent-reach-command --require-default-agent-reach-routes --blocker-out RUN/source_scout_blockers.md --json

    If this command exits non-zero, stop and fix source discovery instead of continuing to the editor.

Prefer fewer high-signal candidates over broad noisy collection.

If fresh discovery cannot run because search or Agent-Reach is unavailable, write `RUN/source_scout_blockers.md` and stop instead of filling the newspaper from browser history.
