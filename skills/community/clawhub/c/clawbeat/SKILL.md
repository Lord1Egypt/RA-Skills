---
name: clawbeat
description: Query live OpenClaw ecosystem intelligence from ClawBeat.co — news, research papers, events, repos, and daily briefings for the OpenClaw agentic framework and alternatives.
metadata: {"openclaw": {"homepage": "https://clawbeat.co/?utm_source=clawhub&utm_medium=skill&utm_campaign=openclaw", "emoji": "📡"}}
---

# ClawBeat: OpenClaw News, Research & Events

ClawBeat.co is a live intelligence feed for the OpenClaw agentic AI framework ecosystem and alternatives (NanoClaw, etc.). Use this skill to fetch curated news, research papers, GitHub projects, events, and daily briefings.

All requests use the public read-only API key. No credentials required.

```bash
CLAWBEAT_URL="https://twouuiapzrkezwbtylij.supabase.co/rest/v1"
CLAWBEAT_KEY="sb_publishable_j-AmOSIuQPEeKIyYAOA2Gg_8ekguDsG"
```

## get_news
Fetch the latest intel/news items (most recent first).

```bash
curl -s "$CLAWBEAT_URL/news_items?select=title,url,summary,pub_date,tags&order=pub_date.desc&limit=20" \
  -H "apikey: $CLAWBEAT_KEY" \
  -H "Authorization: Bearer $CLAWBEAT_KEY"
```

## search_news
Search news by keyword (replace KEYWORD).

```bash
curl -s "$CLAWBEAT_URL/news_items?select=title,url,summary,pub_date,tags&title=ilike.*KEYWORD*&order=pub_date.desc&limit=20" \
  -H "apikey: $CLAWBEAT_KEY" \
  -H "Authorization: Bearer $CLAWBEAT_KEY"
```

## get_events
Fetch upcoming events sorted by start date.

```bash
curl -s "$CLAWBEAT_URL/events?select=title,url,organizer,event_type,location_city,location_state,start_date,end_date&order=start_date.asc&limit=50" \
  -H "apikey: $CLAWBEAT_KEY" \
  -H "Authorization: Bearer $CLAWBEAT_KEY"
```

## get_daily_edition
Fetch the most recent Daily Edition briefing (stories + summaries).

```bash
curl -s "$CLAWBEAT_URL/daily_editions?select=edition_date,stories&order=edition_date.desc&limit=1" \
  -H "apikey: $CLAWBEAT_KEY" \
  -H "Authorization: Bearer $CLAWBEAT_KEY"
```

## get_repos
Fetch tracked GitHub projects in the OpenClaw ecosystem.

```bash
curl -s "$CLAWBEAT_URL/github_projects?select=name,url,description,stars,language,topics&order=stars.desc&limit=50" \
  -H "apikey: $CLAWBEAT_KEY" \
  -H "Authorization: Bearer $CLAWBEAT_KEY"
```

## get_research
Fetch research papers tracked by ClawBeat.

```bash
curl -s "$CLAWBEAT_URL/research_papers?select=title,url,authors,pub_date,abstract&order=pub_date.desc&limit=20" \
  -H "apikey: $CLAWBEAT_KEY" \
  -H "Authorization: Bearer $CLAWBEAT_KEY"
```
