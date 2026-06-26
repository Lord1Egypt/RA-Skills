# cjl-autoresearch-cc

Auto-improve any skill, prompt, article, workflow, or system through iterative mutation-testing.

Inspired by [Karpathy/autoresearch](https://github.com/karpathy/autoresearch) and [openclaw-autoresearch-pro](https://github.com/0xcjl/openclaw-autoresearch-pro).

---

**Languages:** [English](README.md) | [中文](README_zh.md)

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [How It Works](#how-it-works)
3. [Quick Start](#quick-start)
4. [Detailed Workflow](#detailed-workflow)
5. [Optimization Modes](#optimization-modes)
6. [Mutation Types](#mutation-types)
7. [Usage Examples](#usage-examples)
8. [Precautions](#precautions)
9. [Contributing](#contributing)

---

## Design Philosophy

### The Problem

AI-generated content often has issues that are obvious to humans but hard for the AI to self-correct:
- Vague instructions that should be precise
- Missing edge case handling
- Inconsistent terminology
- Redundant or verbose content

### The Solution: Mutation Testing

Instead of asking AI to rewrite everything (which often makes things worse), we:

1. **Make one small change** at a time
2. **Test each change** against realistic scenarios
3. **Score objectively** using a checklist
4. **Keep only improvements**, discard regressions

This mirrors how evolution works — small mutations, survival of the fittest.

### Why Small Changes?

Large rewrites are **unverifiable** — you can't prove they helped or hurt. A single sentence change is verifiable: before and after are comparable.

**Core Principle:** One small verifiable change per round.

---

## How It Works

### The Loop

```
┌─────────────────────────────────────────────────────────────┐
│                      AUTORESEARCH LOOP                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│   │ MUTATE   │───▶│   TEST   │───▶│   SCORE  │           │
│   │ (1 edit) │    │ (cases)  │    │(checklist)│           │
│   └──────────┘    └──────────┘    └──────────┘           │
│                                          │                  │
│                                          ▼                  │
│                                    ┌──────────┐             │
│                                    │  DECIDE  │             │
│                                    │keep/revert│            │
│                                    └──────────┘             │
│                                          │                  │
└──────────────────────────────────────────┼──────────────────┘
                                           │
                           ┌───────────────┴───────────────┐
                           │     Repeat until done        │
                           │  (max 100 rounds)            │
                           └───────────────────────────────┘
```

### Scoring

Each round produces a score based on the checklist:
- **10/10 = 100%** (perfect)
- **7/10 = 70%** (good)
- **5/10 = 50%** (minimum viable)

Score improves? → **Keep the mutation**
Score decreases? → **Revert the mutation**

---

## Quick Start

### Installation

```bash
# Via ClawHub
clawhub install cjl-autoresearch-cc

# Or clone manually
git clone https://github.com/0xcjl/cjl-autoresearch-cc.git ~/.claude/skills/cjl-autoresearch-cc
```

### Basic Usage

```
# Optimize a skill
autoresearch coding-standards

# Optimize with path
autoresearch ~/.claude/skills/my-skill

# Optimize a prompt inline
autoresearch optimize this prompt: [paste your prompt]

# Chinese keyword
自动优化 coding-standards
```

---

## Detailed Workflow

### Step 1 — Identify Mode and Target

The skill auto-detects what you want to optimize:

| Mode | When triggered |
|------|----------------|
| **Skill** | Path to skill directory or "optimize [skill-name]" |
| **Plugin** | Path to plugin directory |
| **Prompt** | Inline prompt text |
| **Article** | Long document text |
| **Workflow** | Process description |
| **System** | System/mechanism description |

### Step 2 — Generate Checklist

The skill creates 10 yes/no questions tailored to your content type:

**For Skill mode (example questions):**
1. Is the description precise and actionable?
2. Does it cover main use cases?
3. Are workflow steps clear and unambiguous?
4. Does it handle error states?
5. Are tool usages correct for Claude Code?
6. Do examples reflect real usage?
7. Is content concise (no redundancy)?
8. Is instruction specificity appropriate?
9. Are references accurate?
10. Are all sections complete?

### Step 3 — Prepare Test Cases

Generate 3-5 realistic inputs that the content would process:

- For a skill: "What would a user say to trigger this skill?"
- For a prompt: "What inputs would this prompt handle?"
- For an article: "How would someone read this?"

### Step 4 — Run the Loop

```
Round N/100 | Best: 85% | Last: +2%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mutation: Type D (Tighten language)
         "try to" → "must"
Score: 85% → 87% ✅ KEEP
```

**Loop config:**
- 30 rounds per batch, then pause for review
- Max 100 rounds total
- Stop if: user says stop, 100 rounds done, 100% score, or 10 rounds no improvement

### Step 5 — Report Results

```
Optimized: coding-standards
Score: 65% → 92% (+27%)
Rounds: 45 (kept: 38, reverted: 7)
Top mutations: Type D (tighten language), Type A (add constraints)

---
Final content saved to: ~/.claude/skills/coding-standards/SKILL.md
```

---

## Optimization Modes

### Skill Mode
Optimize SKILL.md files for Claude Code or OpenClaw.

```
autoresearch coding-standards
autoresearch ~/.claude/skills/tdd-workflow
```

### Plugin Mode
Optimize plugin configuration and code.

```
autoresearch everything-claude-code
```

### Prompt Mode
Improve any prompt text.

```
autoresearch optimize this prompt: You are a helpful assistant that...
```

### Article Mode
Polish documentation or articles.

```
autoresearch polish this article: [paste article]
```

### Workflow Mode
Optimize processes and procedures.

```
autoresearch optimize the deployment workflow
```

### System Mode
Improve system architecture or mechanisms.

```
autoresearch improve the error handling system
```

---

## Mutation Types

Each round picks ONE mutation type:

| Type | Name | When to Use |
|------|------|-------------|
| **A** | Add constraint | Content is too vague |
| **B** | Strengthen coverage | Trigger cases are missing |
| **C** | Add example | Steps are too abstract |
| **D** | Tighten language | Words are soft ("try to" → "must") |
| **E** | Error handling | Failure modes missing |
| **F** | Remove redundancy | Content is verbose |
| **G** | Improve transitions | Flow is choppy |
| **H** | Expand thin section | Content is sparse |
| **I** | Add cross-ref | Sections are isolated |
| **J** | Adjust freedom | Balance is off |

### High-Impact Mutations

These consistently improve scores:
- Adding explicit constraints where content is vague
- Expanding coverage to edge cases
- Adding concrete examples to abstract instructions
- Tightening soft language ("try to" → "must")

### What to Avoid

- Large rewrites of entire sections
- Multiple unrelated changes at once
- Changing fundamental scope or purpose
- Formatting-only changes (no testable value)
- Removing more than 10% of content

---

## Usage Examples

### Example 1: Optimize a Skill

```bash
# Trigger
autoresearch coding-standards

# AI responds:
# "Optimize coding-standards in Skill mode? (yes/no)"
# > yes

# AI generates checklist, prepares test cases, runs loop
# After 30 rounds: Score 68% → 89%
```

### Example 2: Optimize a Prompt

```bash
# Trigger
autoresearch optimize this prompt: Write a function that...

# AI responds:
# "Optimize inline prompt in Prompt mode? (yes/no)"
# > yes

# AI generates checklist, runs loop
```

### Example 3: Chinese Usage

```bash
# Trigger
自动优化 coding-standards

# Chinese keywords also work
自动研究 错误处理系统
```

### Example 4: Semantic Trigger

```bash
# No keyword needed - intent detected
帮我优化一下这个skill
这个prompt不太行
让文章更通顺
```

---

## Precautions

### 1. One Mutation Per Round

**Critical rule.** Multiple changes = unverifiable = will be reverted.

### 2. Trust the Score

Don't rationalize a bad mutation. If score dropped, revert. Don't think "but it's actually better because..."

### 3. Minimum 5 Checklist Questions

Using fewer makes scoring unreliable. Default is 10.

### 4. Context Length

Autoresearch works best with content that fits in context. For very long documents, optimize section by section.

### 5. Meaningful Test Cases

Test cases must be realistic. Generated "test inputs" that don't match real usage will give false scores.

### 6. Human Review Points

Every 30 rounds, the loop pauses for human review. Use this to:
- Assess if optimization is heading the right direction
- Identify issues the checklist might miss
- Decide to stop or continue

### 7. Not for Everything

Autoresearch is for **text-based content** that can be scored with a checklist. It's not suitable for:
- Code with actual runtime behavior (use tests instead)
- Binary content
- Subjective creative work without clear criteria

---

## Contributing

Issues and pull requests welcome! See [SKILL.md](SKILL.md) for the full skill specification.

---

## Credits

- [Karpathy/autoresearch](https://github.com/karpathy/autoresearch) — Original concept
- [openclaw-autoresearch-pro](https://github.com/0xcjl/openclaw-autoresearch-pro) — Prompt/article optimization extension

---

For full technical documentation, see [SKILL.md](SKILL.md).
