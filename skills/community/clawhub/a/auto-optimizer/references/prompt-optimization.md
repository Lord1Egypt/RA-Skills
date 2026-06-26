# Prompt & Skill Optimization with Binary Evals

## Overview

Binary eval mode is the best approach for optimizing prompts and skills. A prompt is a distribution — a single run tells you almost nothing. Running it 10 times and scoring each output against yes/no criteria gives you a reliable signal.

## Quick Start

```bash
./auto-optimizer.sh \
  --eval-mode binary \
  --evals ./evals-templates/prompt-evals.md \
  --file ./my-system-prompt.md \
  --batch-size 10 \
  --budget 20 \
  --session "prompt-opt"
```

## Building Prompt Evals

Good prompt evals are specific to the prompt's purpose. For a customer support prompt:

```markdown
# Eval Criteria for Customer Support Prompt

1. Does the response acknowledge the customer's specific issue (not a generic greeting)? → yes/no
2. Is the response under 150 words? → yes/no
3. Does the response include at least one concrete next step? → yes/no
4. Is the tone empathetic without being sycophantic? → yes/no
5. Does the response avoid jargon the customer wouldn't understand? → yes/no
```

## What to Optimize

**High-leverage prompt changes:**
- System prompt structure (role definition, constraints, output format)
- Few-shot examples (add, remove, or replace examples)
- Chain-of-thought instructions (when to reason vs. when to answer directly)
- Persona and tone instructions
- Edge case handling instructions

**Low-leverage changes (avoid):**
- Trivial wording tweaks with no semantic difference
- Adding more constraints (usually hurts creativity without improving quality)
- Making prompts longer without purpose

## The Meta-Optimizer Play

To systematically improve an entire prompt library:

```bash
for prompt_file in ~/prompts/*.md; do
  ./auto-optimizer.sh \
    --eval-mode binary \
    --evals ./evals-templates/prompt-evals.md \
    --file "$prompt_file" \
    --batch-size 10 \
    --budget 15 \
    --session "meta-$(basename "$prompt_file" .md)"
done
```

## Skill Optimization Workflow

1. Start with the existing SKILL.md as the mutable file
2. Use the general `prompt-evals.md` as starting evals
3. Add domain-specific criteria to the evals file
4. Run 15–20 iterations
5. Save the best version back to the skill directory
6. Document what changed and why

## Expected Results

A typical skill optimization run:
- Baseline: 65–75% pass rate
- After 20 iterations: 85–95% pass rate
- Cost: $2–8 using Claude Haiku for generation

The changelog (hypothesis_log.jsonl) is as valuable as the final prompt — it documents what doesn't work and why.
