---
name: exa-x-search
description: "Search Twitter/X for tweets, discussions, and sentiment on topics, people, or brands using Exa's tweet category search. Use when the user mentions 'search Twitter,' 'find tweets,' 'X search,' 'what are people saying on X,' 'Twitter mentions,' 'tweets about,' or 'Twitter sentiment.' Covers tweet discovery, sentiment analysis, and trend spotting. NOT for general web search. For broader social listening with synthesis, see social-listening. For general web research, see exa-company-research."
metadata:
  version: 1.0.0
---

# Exa X Search

You help users search Twitter/X for relevant tweets and discussions using Exa's tweet category search. Your goal is to find what people are saying, identify sentiment patterns, and surface notable voices on any topic.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand what the user needs (ask if not provided):

1. **Search topic** -- brand, product, person, or topic to search for
2. **Purpose** -- sentiment monitoring, competitive intel, trend spotting, or general research
3. **Time focus** -- recent tweets only, or all-time?

## Workflow

### Step 1: Search for Tweets

Run via exec:
```bash
node tools/clis/exa.js search --query "[topic or brand]" --category "tweet" --num-results 20
```

For recent tweets only:
```bash
node tools/clis/exa.js search --query "[topic]" --category "tweet" --num-results 20 --start-date [current-year]-01-01  # Use current year
```

### Step 2: Fetch Tweet Content

For the most relevant results, fetch full content:
```bash
node tools/clis/exa.js contents --ids "[id1],[id2]" --text
```

Use the IDs returned from the search results.

### Step 3: Analyze Patterns

Review the tweets for:
- **Sentiment** -- positive, negative, neutral, mixed
- **Key voices** -- who is talking about this and do they have influence?
- **Trending themes** -- what subtopics or angles keep coming up?
- **Volume signals** -- is this a growing or declining conversation?

---

## Dry Run

To preview the request without making an API call:
```bash
node tools/clis/exa.js search --query "[topic]" --category "tweet" --dry-run
```

---

## Output Format

### Individual Tweets

For notable tweets:

- **Author:** [handle/name]
- **Content:** [tweet text or summary]
- **Sentiment:** Positive / Negative / Neutral / Mixed
- **Date:** [when posted]

### Synthesis

After listing tweets, provide:

- **Overall Sentiment:** [summary of sentiment distribution]
- **Key Themes:** [3-5 recurring topics or angles]
- **Notable Voices:** [influential accounts discussing this topic]
- **Conversation Trend:** [growing, stable, or declining interest]
- **Actionable Insights:** [what the user can do with this information]

---

## Tips

- **Brand monitoring:** Search for both the brand name and common misspellings or abbreviations
- **Competitor intel:** Compare tweet sentiment between your brand and competitors
- **Product launches:** Search around launch dates to capture initial reactions
- **Hashtags:** Include relevant hashtags in the query for more targeted results
- **Negative sentiment:** Pay special attention to complaints -- they reveal product gaps

---

## Related Skills

- **social-listening**: Broader social listening with cross-platform synthesis
- **social-content**: Create social media content based on trends
- **exa-company-research**: Research companies beyond social mentions
