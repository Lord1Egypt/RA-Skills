# Customer Research & Validation Skill

**Trigger conditions:**
- User asks to validate a product idea, persona, or market assumption
- User mentions "customer research", "validate assumption", "talk to users"
- User requests Reddit/forum mining, competitor analysis, or sentiment analysis
- User wants to generate surveys or interview scripts
- User asks about customer pain points, needs, or jobs-to-be-done

## Purpose

Pre-pipeline validation for DaVinci Enterprises products. Ensures marketing strategy is built on real customer signal, not assumptions. Prevents building features nobody wants.

## What It Does

1. **Reddit/Forum Mining** — Extract threads, comments, sentiment from subreddits and forums
2. **Survey Generation** — Convert research questions into structured surveys
3. **Interview Scripts** — Generate customer interview guides with probing questions
4. **Persona Validation** — Test persona assumptions against real user behavior
5. **Competitor Review Scraping** — Aggregate reviews from G2, Trustpilot, Reddit
6. **Sentiment Analysis** — Aggregate and score customer sentiment across sources

## Usage

### Quick Start
```bash
# Validate a product hypothesis via Reddit mining
scripts/reddit-miner.sh --subreddit "personalfinance" --query "FIRE calculator" --limit 50

# Generate a customer interview script
scripts/interview-generator.sh --persona "FIRE enthusiast" --problem "retirement planning tools"

# Scrape competitor reviews
scripts/competitor-scraper.sh --product "Personal Capital" --sources "g2,trustpilot,reddit"
```

### Integration with Marketing Pipeline

This skill feeds into the content strategy workflow:
1. **Discovery** → Run customer research to identify pain points
2. **Validation** → Test persona assumptions against real data
3. **Strategy** → Build content pillars around validated needs
4. **Execution** → Ogilvy creates content targeting real customer language

Output format: JSON reports to `data/research/` for downstream consumption.

## Scripts

### reddit-miner.sh
Fetch Reddit threads matching keywords, extract sentiment, output structured JSON.

**Usage:**
```bash
./scripts/reddit-miner.sh --subreddit SUBREDDIT --query "search terms" [--limit N] [--sentiment]
```

**Output:** `data/research/reddit-{subreddit}-{timestamp}.json`

### interview-generator.sh
Generate customer interview script from persona + problem statement.

**Usage:**
```bash
./scripts/interview-generator.sh --persona "description" --problem "pain point"
```

**Output:** Markdown interview guide to stdout

### competitor-scraper.sh
Aggregate reviews from multiple sources, extract themes and sentiment.

**Usage:**
```bash
./scripts/competitor-scraper.sh --product "Product Name" --sources "g2,trustpilot,reddit"
```

**Output:** `data/research/competitor-{product}-{timestamp}.json`

## Output Schema

All scripts output to `data/research/` with consistent JSON schema:

```json
{
  "meta": {
    "skill": "customer-research",
    "script": "reddit-miner",
    "timestamp": "2026-03-22T00:43:00Z",
    "query": {...}
  },
  "findings": [
    {
      "source": "reddit",
      "source_id": "thread_abc123",
      "text": "I wish there was a FIRE calculator that...",
      "sentiment": 0.65,
      "themes": ["pain point", "feature request"],
      "metadata": {...}
    }
  ],
  "summary": {
    "total_sources": 47,
    "avg_sentiment": 0.42,
    "top_themes": ["complexity", "cost", "trust"],
    "key_insights": ["Users want transparency", "Price sensitivity high"]
  }
}
```

## Dependencies

- `jq` — JSON processing
- `curl` — HTTP requests
- Reddit API access (optional: can scrape public threads without auth)
- OpenClaw LLM access for sentiment analysis

## Example Workflow

**Scenario:** Validate demand for FIRE Sim product

1. **Mine Reddit pain points:**
   ```bash
   ./scripts/reddit-miner.sh --subreddit "financialindependence" \
     --query "retirement calculator problems" --limit 100 --sentiment
   ```

2. **Scrape Personal Capital reviews:**
   ```bash
   ./scripts/competitor-scraper.sh --product "Personal Capital" \
     --sources "g2,trustpilot,reddit"
   ```

3. **Generate interview script:**
   ```bash
   ./scripts/interview-generator.sh \
     --persona "30-40 tech worker, $200K income, aiming FIRE by 45" \
     --problem "existing retirement tools too conservative or too complex"
   ```

4. **Analyze findings:**
   - Review JSON outputs in `data/research/`
   - Identify recurring themes, pain points, language patterns
   - Validate/invalidate persona assumptions
   - Feed insights into content strategy

5. **Document learnings:**
   - Update `projects/davinci-enterprises/customer-insights.md`
   - Flag validated needs for product roadmap
   - Inform Ogilvy content pillars with real customer language

## Quality Gates

- **Minimum sample size:** 30+ sources per research question
- **Sentiment confidence:** Only report sentiment scores with >50 samples
- **Theme validation:** Themes must appear in ≥3 independent sources
- **Source diversity:** Mix Reddit, review sites, forums (not just one platform)

## Anti-Patterns

❌ **Don't:**
- Build features based on one Reddit comment
- Cherry-pick data to confirm existing beliefs
- Skip competitor analysis (reinventing the wheel wastes time)
- Ignore negative sentiment (it's the most valuable signal)

✅ **Do:**
- Let data challenge your assumptions
- Track quotes verbatim (real customer language = gold for content)
- Cross-reference findings across sources
- Document what you disproved, not just what you confirmed

## Integration Points

- **Content Strategy:** Feed validated pain points to Ogilvy for pillar creation
- **Product Roadmap:** Link research findings to JIRA/task tickets
- **Persona Database:** Update persona definitions based on validation results
- **Marketing Copy:** Extract customer language for landing pages, ads

## Maintenance

- Research data retention: 90 days (then archive to cold storage)
- Re-run validation quarterly for active products
- Update scripts when Reddit/review site APIs change
- Log failed scrapes to `logs/customer-research-errors.log`

---

**Next Steps After Running Research:**
1. Review findings in `data/research/`
2. Update persona docs with validated/invalidated assumptions
3. Create content strategy tasks based on identified pain points
4. Schedule customer interviews if online research raises questions
5. Document learnings in project-specific CONTEXT.md
