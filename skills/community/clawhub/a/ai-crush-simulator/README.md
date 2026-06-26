# 💘 AI Crush Simulator

A fun, safe, and youth-friendly ClawHub skill that helps you navigate crush situations.
Analyze the vibe, decode their texts, generate thoughtful replies, and figure out your next move.

---

## Features

| Module | What it does |
|--------|-------------|
| `crushAnalysis` | Reads your situation and scores the vibe (0–100) with flag detection |
| `textDecoder` | Interprets a text message with multiple possible readings |
| `replyGenerator` | Produces three reply options (Bold / Chill / Safe) for your goal |
| `nextMove` | Recommends the smartest next step with practical tips |

---

## Quick Start

```bash
# Install dependencies
npm install

# Run the interactive CLI
npm run cli

# Run sample test scenarios
npm test

# Type-check the project
npm run typecheck

# Build to dist/
npm run build
```

---

## Project Structure

```
ai-crush-simulator/
├── src/
│   ├── types.ts                 # All shared TypeScript interfaces & enums
│   ├── scoring/
│   │   └── heuristics.ts        # Signal scoring engine (shared by all modules)
│   ├── modules/
│   │   ├── crushAnalysis.ts     # Module 1 — situation analysis
│   │   ├── textDecoder.ts       # Module 2 — text decoder
│   │   ├── replyGenerator.ts    # Module 3 — reply generator
│   │   └── nextMove.ts          # Module 4 — next move advisor
│   └── index.ts                 # Public API (re-exports everything)
├── cli/
│   └── main.ts                  # Interactive menu-driven CLI
├── tests/
│   └── scenarios.ts             # 3 sample scenarios, all 4 modules
├── SKILL.md                     # ClawHub/OpenClaw skill definition
├── README.md
├── package.json
└── tsconfig.json
```

---

## Using the Modules Directly

All four modules are pure functions — import from `src/index.ts` and call them
independently or chain them together.

### crushAnalysis

```typescript
import { analyzeCrush } from './src/index.js';

const result = analyzeCrush({
  howTheyMet:            'class',
  howLong:               '3 months',
  interactionFrequency:  'texted first a few times, chat almost every day',
  recentInteractions:    'remembered my favourite band, asked me a question about my weekend',
  yourFeelingConfidence: 5,
});

console.log(result.vibeScore);        // e.g. 82
console.log(result.connectionDepth);  // e.g. "warm"
console.log(result.flags);            // e.g. [{ color: "green", label: "remembered", ... }]
console.log(result.summary);          // formatted multi-line string
```

### textDecoder

```typescript
import { decodeText } from './src/index.js';

const decoded = decodeText({
  messageFromCrush: 'Omg we should totally watch that together!! 😭 when are you free?',
});

console.log(decoded.warmthScore);  // e.g. 78
console.log(decoded.overallVibe);  // e.g. "😄 Playful"
console.log(decoded.readings);     // Array of TextReading with interpretation + confidence
```

### replyGenerator

```typescript
import { generateReplies } from './src/index.js';

const options = generateReplies({
  decodedText: decoded,       // from textDecoder
  userGoal:    'show-interest',
});

for (const reply of options.replies) {
  console.log(`[${reply.tone}] ${reply.text}`);
  console.log(`  → ${reply.rationale}`);
}
console.log(options.tip);
```

### nextMove

```typescript
import { adviseNextMove } from './src/index.js';

const move = adviseNextMove({
  vibeScore:   result.vibeScore,    // from crushAnalysis
  warmthScore: decoded.warmthScore, // from textDecoder
  userGoal:    'ask-out',
  howLong:     '3 months',
});

console.log(move.headline);   // e.g. "🎯 Be a bit more direct"
console.log(move.reasoning);
move.tips.forEach(t => console.log('•', t.text));
```

---

## Full Crush Check (Chained Flow)

```typescript
import { analyzeCrush, decodeText, generateReplies, adviseNextMove } from './src/index.js';

const analysis = analyzeCrush(situation);
const decoded  = decodeText({ messageFromCrush: '...' });
const replies  = generateReplies({ decodedText: decoded, userGoal: 'ask-out' });
const move     = adviseNextMove({
  vibeScore:   analysis.vibeScore,
  warmthScore: decoded.warmthScore,
  userGoal:    'ask-out',
  howLong:     situation.howLong,
});
```

---

## Heuristics Scoring Engine

The scoring engine in `src/scoring/heuristics.ts` is the intelligence layer.
It exposes three functions used across all modules:

| Function | Input | Output | Used by |
|---|---|---|---|
| `scoreSignals(text)` | Situation description | 0–100 score | crushAnalysis |
| `scoreTextWarmth(text)` | Single message | 0–100 score | textDecoder |
| `detectFlags(text)` | Situation description | `Flag[]` | crushAnalysis |

### Extending the Signal Dictionaries

Add entries to the arrays in `heuristics.ts` to teach the engine new signals:

```typescript
// More positive signals
const POSITIVE_SIGNALS = [
  ...existing signals...,
  'sent a voice note',   // new
  'tagged me in a meme', // new
];
```

No changes to module logic required.

---

## Safety & Content Policy

This skill is designed for **ages 13+** and enforces the following constraints:

- **No false certainty** — every output includes a "based on what you shared" disclaimer
- **No manipulation tactics** — replies never suggest jealousy games, ignoring someone on purpose, love bombing, or pressure
- **No harassment encouragement** — red flag outputs actively encourage giving space and respecting the other person
- **No sexual content** — all templates and outputs are G-rated
- **Empowerment framing** — all advice centres the user's confidence and self-respect

---

## ClawHub Publishing

This project is ready to publish on [ClawHub.ai](https://clawhub.ai) as an OpenClaw skill.

- The `SKILL.md` file contains the full skill definition, module documentation, example interactions, and safety constraints.
- Outputs are structured and screenshot-friendly.
- No external API dependencies — runs on pure heuristics, making it fast and private.
- Extend signal dictionaries in `heuristics.ts` without touching module logic.

---

## License

ISC
