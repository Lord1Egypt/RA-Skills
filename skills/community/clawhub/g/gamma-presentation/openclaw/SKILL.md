---
name: gamma
description: Generate professional presentations with Gamma AI. Just describe what you want — topic, outline, or full content — and get a polished deck. No Gamma account needed.
metadata: {"clawdbot":{"emoji":"🎯","os":["darwin","linux","windows"],"requires":{"bins":["bun"],"env":["GAMMA_API_KEY"]}}}
---

# Gamma Presentation Generator

Generate polished presentations from a topic or content brief. Uses Gamma AI
to create professionally designed slides. The user does not need a Gamma account.

## When to Use

Trigger when the user wants to:
- Create a presentation, deck, or slides
- "Make me a pitch deck about X"
- "Generate slides for my talk on Y"
- "Create a presentation with 10 slides about Z"

Do NOT trigger for:
- PPTX file editing (use document-skills:pptx instead)
- HTML/web presentations (use frontend-slides instead)
- Presenton-specific requests (use presenton instead)

## How to Use

### Step 1: Gather Requirements

Ask the user (if not already provided):
- **Topic or content**: What the presentation is about
- **Audience**: Who is this for? (investors, team, conference)
- **Length**: How many slides? (default: ~8-10)
- **Format**: PDF or PPTX? (default: PDF)

### Step 2: Prepare the Input

For best results, compose a structured prompt:

```
Create a [N]-slide presentation about [TOPIC].

Audience: [WHO]
Tone: [professional/casual/technical]

Key points to cover:
1. [Point 1]
2. [Point 2]
3. [Point 3]

Include: [data, charts, examples, quotes, etc.]
```

### Step 3: Generate

```bash
GAMMA_API_KEY="$GAMMA_API_KEY" bun run ~/.claude/skills/gamma/generate.ts \
  --content "$(cat /tmp/gamma-prompt.txt)" \
  --format pdf \
  --output /tmp/presentation.pdf
```

Or with just a topic:
```bash
GAMMA_API_KEY="$GAMMA_API_KEY" bun run ~/.claude/skills/gamma/generate.ts \
  --topic "IrisGo Series A Pitch" \
  --pages 12 \
  --format pdf \
  --output /tmp/pitch-deck.pdf
```

### Step 4: Deliver

- If output file was saved, tell the user the file path
- If download failed, provide the Gamma URL for manual export
- Offer to open the file or share the link

## Configuration

The API key is stored in the environment. Do not expose it to the user.

```bash
# Set in your shell profile or .env
export GAMMA_API_KEY="sk-gamma-..."
```

## Limitations

- Gamma AI designs the slides — layout and visual style are Gamma's choice
- Export to PDF/PPTX may require the Gamma URL (direct download not always available)
- Generation takes 30-90 seconds depending on complexity
- Content is limited by Gamma's input length (~4000 chars recommended)

## Cost

Each generation costs Gamma credits (~$0.01/credit, typical deck = 50-100 credits).
The skill owner covers this cost — users generate for free.
