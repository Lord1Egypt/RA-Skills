# Amazon Alexa for Shopping QA — Best Practices & Use Cases

This document supplements `SKILL.md` with question design guidelines, batch collection tips, and typical use case templates.

---

## Best Practices

### 1. Question Design

**Good questions**:
- "What accessories are essential for sous vide?"
- "Which brands are most reliable for coffee makers?"
- "How do I choose the right size container?"

**Avoid**:
- Too broad: "Tell me everything about coffee"
- Non-shopping related: "What's the weather today?"

---

### 2. Keyword Selection

Use search keywords related to your questions. The AI will answer based on the search results context:

```bash
# Pass keyword in batch script — navigate to the relevant search page before asking
browser-act --session amazon-qa navigate "https://www.amazon.com/s?k=sous+vide"
browser-act --session amazon-qa wait stable
# Then start batch questioning
```

---

### 3. Batch Processing Tips

- Take a screenshot every 5–10 questions for post-review
- Recommended interval between questions: 2 seconds (to avoid rate limiting)
- Batch script example (run in bash tool):

```bash
cd ".claude/skills/amazon-alexa-qa"
questions=(
  "What accessories are essential for sous vide?"
  "Which sous vide brands are most reliable?"
  "What temperature should I use for chicken breast?"
  "How long does it take to cook steak sous vide?"
  "What are the benefits of sous vide cooking?"
)
results=()
for q in "${questions[@]}"; do
  eval "$(python scripts/inject-question.py "$q")"
  browser-act --session amazon-qa wait stable --timeout 60000
  sleep 3
  result=$(browser-act --session amazon-qa eval "$(python scripts/extract-response.py)" 2>/dev/null)
  # If not ready on first attempt, retry once
  if echo "$result" | grep -q '"error":true'; then
    browser-act --session amazon-qa wait stable --timeout 15000
    sleep 3
    result=$(browser-act --session amazon-qa eval "$(python scripts/extract-response.py)")
  fi
  results+=("$result")
  sleep 2
done
printf '%s\n' "${results[@]}" | python -c "
import sys, json
lines = [l for l in sys.stdin.read().strip().split('\n') if l.strip()]
data = [json.loads(l) for l in lines]
print(json.dumps(data, ensure_ascii=False, indent=2))
" > output/alexa_qa_results.json
echo "Done. Results saved to output/alexa_qa_results.json"
```

---

### 4. Saving Results

Use JSON format for easy post-analysis:

```python
# Parse saved results with Python
import json

with open("output/alexa_qa_results.json", encoding="utf-8") as f:
    results = json.load(f)

for r in results:
    print(f"Q: {r['question']}")
    print(f"A: {r['response'][:200]}...")
    print()
```

---

### 5. Performance Reference

| Metric | Value |
|--------|-------|
| Average response time | 20–30 seconds/question |
| Supports consecutive questions | Yes (same session maintains context) |
| Recommended interval per question | ≥ 2 seconds |

---

## Common Use Cases

### Market Research

Understand core user needs and evaluations for a product category:

```bash
questions=(
  "What features do customers look for in sous vide cookers?"
  "What are common complaints about sous vide machines?"
  "Which brands dominate the sous vide market?"
)
```

---

### Competitive Analysis

Compare major brands and product differences:

```bash
questions=(
  "What are the top-rated sous vide brands?"
  "How do Anova and Joule sous vide compare?"
  "What accessories are commonly bought with sous vide cookers?"
)
```

---

### User Needs Insights

Uncover real user pain points and purchase motivations:

```bash
questions=(
  "What problems does sous vide cooking solve?"
  "Who is the target audience for sous vide machines?"
  "What are the must-have features for home sous vide cooking?"
)
```

---

### Extracting Product Recommendations

Collect specific product information returned by Alexa:

```bash
# After asking, the response field contains product names, prices, ratings, etc.
# Use regex or LLM for further parsing
question="What are the best budget sous vide cookers under \$100?"
```

> Example response includes: product names, star ratings (e.g., `4.6Stars(12,345)`), prices (e.g., `$49.99`), discount info, delivery estimates, and Alexa's comparison summary.
