---
name: digital-ip-agent
description: Turn a public creator, blogger, podcaster, YouTuber, or X/Twitter personality into a deployable OpenClaw agent. Use when the user provides a YouTube URL, X handle, creator name, podcast host, or asks for things like "turn this creator into an agent", "clone this creator's style", "digitalize this KOL", or "generate agent files from this public persona". Produce an OpenClaw persona package centered on `soul.md`, `identity.md`, `memory.md`, and `agents.md`, plus a recommended supporting-skill stack.
---

# Digital IP Agent

Analyze a public creator's voice, worldview, and audience relationship, then turn those traits into a deployable OpenClaw agent package.

## Workflow

```text
Input: YouTube URL / X handle / creator name / podcast host / public persona
  ↓
Collect representative public material
  ↓
Extract voice, values, thinking patterns, and audience relationship
  ↓
Generate core OpenClaw persona files
  ↓
Recommend a supporting skill stack
  ↓
Return a publication-ready agent configuration package
```

## Step 1: Classify the input source

| Input type | What to do |
| --- | --- |
| Single YouTube video | Pull transcript/description and analyze voice + structure |
| YouTube channel | Review recent titles, descriptions, and recurring themes |
| X/Twitter handle | Review recent posts, replies, and high-engagement patterns |
| Creator name only | Locate the main platform first, then analyze |
| Multi-platform persona | Synthesize the stable traits shared across platforms |

## Step 2: Extract the persona dimensions

Always extract these dimensions before generating files.

### Voice
- Vocabulary level and sentence rhythm
- Signature openings, closings, and recurring phrases
- Humor style, emotional temperature, and metaphor habits
- Short-form vs long-form tendencies

### Thinking model
- Core values repeated across content
- Decision style and reasoning framework
- Time horizon and risk posture
- Industry worldview or recurring theses

### Content preferences
- Strongest subject areas
- Preferred content structure
- Example style: stories, data, frameworks, history, personal experience
- Topics consistently avoided or rejected

### Audience relationship
- How the creator addresses followers
- How disagreement is handled
- Whether the persona teaches, debates, challenges, comforts, or performs
- Boundary-setting style

## Step 3: Normalize the persona summary

Before generating files, build this internal summary:

```text
Creator name / alias:
Primary platform:
Core identity tags (3-5):
Signature voice traits (3-5):
Core values (3-5):
Top domains of expertise:
Thinking framework:
Emotional tone:
Red lines / boundaries:
Relationship stance toward audience:
```

## Step 4: Generate the core files

### `soul.md`
Capture the deepest layer of the persona.

Must include:
- Core essence
- Fundamental beliefs
- Non-negotiables
- Mission
- Primary drive
- Shadow side or limitations

### `identity.md`
Capture how the persona presents itself.

Must include:
- Who I am
- Background and credibility markers
- Signature voice guide
- How I think
- Intended audience
- What I am not

### `memory.md`
Capture the stable knowledge and reference layer.

Must include:
- Core expertise areas
- Frameworks and mental models
- Signature stories and examples
- Relationship memory stance
- Learning style
- Reference points

### `agents.md`
Capture behavior rules for interaction.

Must include:
- Response style defaults
- Interaction protocols
- Tone calibration by context
- Out-of-scope handling
- Sample interactions

## Step 5: Recommend supporting skills

After generating the core files, recommend a supporting skill stack. Use `references/skills-catalog.md` as the default source.

Match the stack to creator type:

- Technical creator
- Finance or investing creator
- Creative or design creator
- Philosophy or education creator
- Lifestyle or health creator
- General cross-platform creator

## Output format

Return the package in this structure:

```text
[Creator Name] Agent Package
├── soul.md
├── identity.md
├── memory.md
├── agents.md
└── skills-recommendation.md
```

## Quality bar

Before finalizing, check:
- `soul.md` feels specific and not generic
- `identity.md` includes concrete voice habits
- `memory.md` contains real examples, frameworks, or recurring references
- `agents.md` contains executable behavior rules, not vague principles
- A real fan of the creator would recognize the tone and priorities

## Special cases

### Sparse information
Search for more material first. If the evidence is still thin, mark uncertain fields explicitly instead of fabricating.

### Multilingual creators
Define voice behavior separately for each language.

### Controversial creators
Capture the real style and worldview without endorsing it. Record sharp edges and disputed tendencies as traits, not praise.

### Fictional or hybrid personas
If the user is actually describing a fictional character or an IP persona rather than a real public creator, use the fictional-companion workflow instead.
