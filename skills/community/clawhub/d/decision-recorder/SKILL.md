---
name: decision-recorder
description: Record, review, search, and analyze decisions from technical work, product work, team discussions, and personal planning. Use when the user wants to capture why a decision was made, compare options, store rationale, track outcomes, or revisit past decisions by keyword, date, or tag.
---

# Decision Recorder

Record decisions in a structured format so they can be searched, reviewed, and improved over time.

## Core capabilities

- Detect decision-oriented text
- Create structured decision records
- Search and filter past decisions
- Review decision details
- Analyze decision patterns
- Update or delete stored decisions

## Commands

### Record a decision

```bash
decision-recorder record
decision-recorder r
```

### List decisions

```bash
decision-recorder list
decision-recorder ls
```

### Search decisions

```bash
decision-recorder search <keyword>
decision-recorder s <keyword>
```

### Analyze patterns

```bash
decision-recorder analyze
decision-recorder a
```

### View a specific decision

```bash
decision-recorder view <id>
decision-recorder v <id>
```

### Update or delete a decision

```bash
decision-recorder update <id>
decision-recorder u <id>

decision-recorder delete <id>
decision-recorder d <id>
```

### Detect decision keywords

```bash
decision-recorder detect "We decided to use Node.js"
decision-recorder keywords
```

## Common filters

```bash
# Filter by tag
decision-recorder list --tag=important

# Filter by date range
decision-recorder list --from=2024-01-01 --to=2024-12-31
```

## Programmatic usage

```javascript
const dr = require('decision-recorder');

const record = dr.createDecision({
  question: 'Which backend stack should we use?',
  options: ['Node.js', 'Python', 'Go'],
  reasoning: 'Node.js has the best fit for fast iteration and ecosystem support.',
  result: 'Node.js',
  context: 'New product launch',
  tags: ['architecture', 'backend']
});

const matches = dr.searchDecisions('architecture');
const analysis = dr.analyzeDecisions();
```

## Decision record format

```json
{
  "id": "unique-id",
  "timestamp": "ISO-8601 timestamp",
  "question": "Decision question",
  "options": ["Option A", "Option B"],
  "reasoning": "Why this choice was made",
  "result": "Final choice",
  "context": "Background",
  "tags": ["tag-a", "tag-b"]
}
```

## Data location

Decision records are stored under:

```bash
~/.decision-recorder/
```

Each decision is stored as a JSON file.

## Recommended use cases

- Architecture and technology choices
- Product tradeoff decisions
- Team decisions after discussion
- Operational decisions and retrospectives
- Personal planning and career decisions

## Good practice

1. Record decisions soon after they are made.
2. Capture reasoning, not just outcomes.
3. Use tags consistently.
4. Review decisions periodically.
5. Compare similar decisions over time.

## Notes

- Requires Node.js 14 or later.
- Uses local JSON files for storage.
- Works best when reasoning and context are written clearly.

## License

MIT
