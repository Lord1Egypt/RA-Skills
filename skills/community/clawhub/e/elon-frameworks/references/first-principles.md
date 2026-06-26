# First-Principles Thinking

## Core Concept

First-principles thinking means decomposing a problem down to its
fundamental, verifiable truths -- and reasoning upward from there. The
opposite is reasoning by analogy ("everyone does it this way, so we
should too").

Most people default to analogy because it's faster and safer. First
principles is harder but produces breakthrough insights because it
strips away inherited assumptions that may no longer be true.

**Use analogy for daily decisions. Use first principles for important ones.**

## Key Quantitative Tools

### The Magic Wand Number

If you had a magic wand and could arrange atoms perfectly, what would
the theoretical minimum cost be? Calculate raw material costs at market
prices to establish the floor.

- Rockets: Raw materials ~2% of the $65M launch price. The 98% gap was
  unchallenged industry assumptions.
- Batteries: Commodity prices showed ~$80/kWh vs. $600/kWh market price.
  Cheap batteries were physically possible.

**Application**: For any expensive product or process, ask: "What would
this cost if we only paid for the atoms?"

### The Idiot Index

**Idiot Index = Finished product cost / Raw material cost**

A high Idiot Index means your manufacturing process is inefficient.

- A $13,000 part made from $200 of steel = Idiot Index of 65. The process
  is absurdly wasteful.
- Every engineer should know the best and worst Idiot Index parts in
  their system at all times.

**Application**: Calculate the Idiot Index for your most expensive
components. Attack the highest ones first.

## Step-by-Step Application

### Step 1: Define the Real Problem

Ask: "What exactly are you trying to achieve? Not the solution you're
considering -- the underlying outcome you need."

Users often come with a solution ("Should I use Kubernetes?") when they
need to start with the problem ("I need my app to handle 10x traffic
spikes without manual intervention").

### Step 2: List Current Assumptions

Ask: "What are you currently taking as given?"

Help them enumerate every assumption:
- Cost assumptions ("This will cost $X")
- Process assumptions ("You have to do it this way")
- Market assumptions ("Customers want Y")
- Technical assumptions ("Technology Z is required")
- Time assumptions ("This takes N months")

### Step 3: Challenge Each Assumption

For every assumption, ask: "Is this a fundamental truth, or just convention?"

Categories:
- **Physics/math constraints** -> These are real. Respect them.
- **Legal/regulatory** -> Real but sometimes changeable. Distinguish
  between law and interpretation of law.
- **Industry conventions** -> Almost always worth questioning.
- **"Best practices"** -> Often outdated or context-dependent.
- **"Everyone does it this way"** -> The most dangerous assumption.

### Step 4: Identify the Fundamental Truths

After stripping assumptions, what remains? These are your first principles
-- the irreducible facts you can build on.

Help the user articulate 3-5 fundamental truths about their situation.

### Step 5: Reason Upward

Ask: "If you were designing the solution from scratch today, knowing
only these fundamentals, what would you build?"

This is where breakthroughs happen. The new design often looks nothing
like the incumbent approach.

**Cross-domain insight**: "What is simple in one arena is often profound
in another." Look for solutions from adjacent fields that practitioners
in the current field would never consider.

### Step 6: Reality-Check

Ground the new insight:
- What resources do you actually have?
- What's the minimum viable version?
- What's the biggest risk, and how would you test it cheaply?
- What's the timeline to first real-world feedback?
- What's the Idiot Index of your proposed approach?

## Output Format

```
## First-Principles Analysis: [User's Problem]

### The Real Problem
[Restatement of the actual objective]

### Assumptions Challenged
| # | Assumption | Type | Verdict |
|---|-----------|------|---------|
| 1 | ... | Convention / Fundamental | Keep / Discard / Test |

### The Magic Wand Number
[Theoretical minimum cost/time/resources]

### Idiot Index (if applicable)
[Current ratio and what it reveals]

### Fundamental Truths
1. [Truth 1]
2. [Truth 2]
3. ...

### Redesigned Approach
[The solution built from fundamentals]

### Reality Check
- Resources needed: ...
- MVP version: ...
- Biggest risk: ...
- First test: ...
- Timeline: ...
```

## Common Pitfalls

- **Fake first principles**: User claims something is fundamental when
  it's actually an assumption. Push back gently.
- **Analysis paralysis**: Don't decompose forever. 3-5 fundamentals is
  usually enough.
- **Ignoring execution**: A brilliant insight is worthless without a
  build plan. Always end with action steps.
- **Context blindness**: First principles from one domain don't
  automatically transfer.
- **Skipping the math**: If you haven't calculated the Magic Wand Number
  or Idiot Index, you're guessing, not reasoning from first principles.
