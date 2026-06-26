# Growth Leader Runbook

## Daily Routine

1. **Morning pulse** (triggered by cron at 08:30 UTC)
   - Run `pulse/main.py --generate` or equivalent skill
   - Crawl 10+ news sources
   - Synthesize into `pulse/signals/signal-{date}.md`

2. **Check assigned issues**
   - `gh issue list --label "delegated/content" --state open`
   - Read issue body for task details
   - Check workspace for relevant context

3. **Execute content tasks**
   - Scaffold PaperOrchestra project in `publications/blog/{date}-{topic}/`
   - Research topic using browser agent (5-10 sources)
   - Draft sections one at a time
   - Assemble into `publications/social/draft.md`
   - Commit: `git commit -m "content: {topic} draft for review"`
   - Push and open PR

4. **Social publishing** (only after human approval)
   - Format for target platform
   - Publish via social scripts
   - Update `ops/social/published_posts.json`

## Content Quality Standards

- Minimum 2,000 words for blog posts
- All factual claims should be verifiable
- Follow PaperOrchestra section-by-section methodology
- Include GEO optimization (keywords, structured data)
- Draft must be assembled and readable in `publications/social/draft.md`

## Error Handling

- If browser research fails: try alternative sources, note gaps in issue comments
- If PaperOrchestra scaffold fails: check directory structure, retry with manual mkdir
- If publishing fails: log in `ops/incident-log.md`, escalate to CEO Agent
