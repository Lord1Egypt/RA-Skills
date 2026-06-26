# Customer Research Integration Guide

## Marketing Strategy Workflow

This skill feeds into the DaVinci Enterprises marketing pipeline at the **pre-strategy** phase.

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: DISCOVERY (Customer Research Skill)                │
├─────────────────────────────────────────────────────────────┤
│ • Reddit/forum mining                                        │
│ • Competitor review scraping                                 │
│ • Initial persona hypothesis                                 │
│ Output: data/research/*.json                                 │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2: VALIDATION (Persona Validator)                     │
├─────────────────────────────────────────────────────────────┤
│ • Test assumptions against real data                         │
│ • Validate/invalidate pain points                            │
│ • Extract customer language                                  │
│ Output: Validation report + updated persona                  │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 3: CUSTOMER INTERVIEWS (Interview Generator)           │
├─────────────────────────────────────────────────────────────┤
│ • Generate interview scripts for weak-support items          │
│ • Conduct 5-10 customer interviews                           │
│ • Document findings                                          │
│ Output: Interview notes + refined personas                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ PHASE 4: STRATEGY (Ogilvy + Content Team)                   │
├─────────────────────────────────────────────────────────────┤
│ • Build content pillars from validated pain points          │
│ • Use customer language in positioning                       │
│ • Prioritize features based on validated needs               │
│ Output: Content strategy + product roadmap updates           │
└─────────────────────────────────────────────────────────────┘
```

## File Flow

### Input Files
- `skills/customer-research/examples/[product]-persona.json` — Initial persona hypothesis

### Working Files
- `data/research/reddit-*.json` — Reddit mining results
- `data/research/competitor-*.json` — Competitor review scrapes
- `data/research/interviews/[date]-[interviewee].md` — Interview notes

### Output Files
- `projects/davinci-enterprises/customer-insights.md` — Aggregated validated insights
- `projects/[product]/personas/[persona-name].json` — Updated, validated personas
- `projects/[product]/CONTEXT.md` — Product-specific learnings from research

## Integration with Existing Systems

### 1. Content Strategy (Ogilvy)

**Input from Customer Research:**
- Validated pain points → content pillars
- Customer language → headline/body copy
- Objections found in research → content addressing objections

**File locations:**
- Source: `data/research/*.json`
- Destination: `projects/davinci-enterprises/content-strategy.md`

**Workflow:**
```bash
# After research validation, extract top 3 pain points
jq '.summary.key_insights' data/research/reddit-*.json

# Feed to Ogilvy for content pillar creation
# Document in projects/davinci-enterprises/customer-insights.md
```

### 2. Product Roadmap (Task System)

**Input from Customer Research:**
- Validated needs → feature priorities
- Deal-breakers from interviews → must-have features
- Nice-to-haves → backlog

**Workflow:**
1. Review validation report
2. Create tasks for validated high-priority features
3. Link research findings in task description
4. Tag with `research-validated` label

### 3. Sales/Landing Pages

**Input from Customer Research:**
- Sample quotes → testimonial-style social proof
- Pain points → "Before/After" positioning
- Customer language → exact phrasing in headlines

**Example:**
```markdown
Research finding: "I wish there was a calculator that shows how a raise affects my FIRE date"

Landing page headline: "See How Your Next Raise Changes Your FIRE Timeline — In Real Time"
```

## Cron Integration (Optional)

For ongoing competitor monitoring:

```bash
# Add to HEARTBEAT.md or create dedicated cron:
# Every Monday, scrape competitor reviews
cron: "0 9 * * 1"  # 9 AM every Monday
task: |
  cd /Users/clawdiri/.openclaw/workspace
  ./skills/customer-research/scripts/competitor-scraper.sh \
    --product "Personal Capital" \
    --sources "reddit"
  
  # Alert if negative sentiment spike detected
  # (Implementation: compare avg_rating to baseline)
```

## DaVinciOS Integration Points

### Dashboard Widget Ideas

1. **Customer Insights Feed**
   - Recent Reddit mentions of competitors
   - Sentiment trend over time
   - Top pain points this week

2. **Persona Health**
   - Assumption validation status (validated/invalidated/needs-data)
   - Last research run date
   - Sample size indicator

3. **Research Queue**
   - Pending validation items
   - Interview script generator quick-launch
   - Competitor monitoring alerts

### API Endpoints (Future)

```typescript
// GET /api/research/personas
// Returns all personas with validation status

// POST /api/research/validate
// Runs persona validator on-demand

// GET /api/research/insights
// Returns recent customer insights for dashboard
```

## Best Practices

### When to Run Research

**Product Launch (Before):**
- Validate persona assumptions
- Test messaging with target audience
- Identify deal-breakers

**Product Launch (After):**
- Monitor customer sentiment
- Track feature requests
- Identify gaps in positioning

**Quarterly:**
- Re-validate persona assumptions
- Check competitor positioning changes
- Update customer language database

### How Much Research is Enough?

**Minimum viable:**
- 30+ Reddit threads
- 10+ competitor reviews
- 5+ customer interviews

**Gold standard:**
- 100+ Reddit threads across multiple subreddits
- 50+ competitor reviews from 3+ sources
- 10-15 customer interviews
- Survey with 50+ responses

### Red Flags

❌ All assumptions validated → You're cherry-picking data
❌ No new insights from research → You're not asking good questions
❌ Customer language sounds like marketing speak → You're leading the witness
❌ Zero contradictory data → Sample bias or confirmation bias

✅ Some assumptions invalidated → You're learning
✅ Surprising findings that challenge beliefs → Good research
✅ Verbatim customer quotes sound authentic → Real signal
✅ Contradictions between sources → Need deeper investigation

## Maintenance

### Data Retention
- Research data: 90 days in `data/research/`, then archive to cold storage
- Validated personas: Keep in `projects/[product]/personas/` indefinitely
- Interview notes: Keep in `data/research/interviews/` for 1 year

### Script Updates
- Reddit API changes: Update `reddit-miner.sh` user agent and endpoints
- New review sources: Add handlers to `competitor-scraper.sh`
- Improved sentiment: Integrate LLM sentiment analysis (currently placeholder)

### Quarterly Review
- Review validation reports for stale data
- Re-run validation on active products
- Update persona docs with new learnings
- Archive inactive personas

## Troubleshooting

**Issue:** Reddit API rate limiting
**Solution:** Add `sleep 2` between requests, or use authenticated API (higher limits)

**Issue:** No research data found
**Solution:** Run `reddit-miner.sh` or `competitor-scraper.sh` first

**Issue:** Validation shows all "NO EVIDENCE"
**Solution:** Either persona is wrong, or research query needs refinement. Try broader keywords.

**Issue:** Too many false positives in validation
**Solution:** Keyword matching is simplistic. For production, use semantic similarity (embeddings).

## Future Enhancements

1. **Sentiment Analysis Integration**
   - Use Gemini/Sonnet for nuanced sentiment scoring
   - Track sentiment over time

2. **Semantic Search**
   - Replace keyword matching with embedding-based similarity
   - Better assumption validation

3. **Survey Generation**
   - Auto-generate Typeform/Google Forms from persona assumptions
   - Track responses in research database

4. **Browser Automation**
   - Full G2/Trustpilot scraping with Playwright
   - Scheduled competitor monitoring

5. **Interview Transcription**
   - Integrate with Whisper for audio → text
   - Auto-extract themes from transcripts

---

**Integration owner:** DaVinci (CEO)
**Skill maintainer:** Research team (delegate to Einstein/Nash for analysis)
**Update frequency:** Quarterly review, ad-hoc for new products
