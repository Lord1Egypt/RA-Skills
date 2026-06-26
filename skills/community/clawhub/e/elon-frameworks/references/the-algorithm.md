# The Algorithm

## Core Concept

The Algorithm is a five-step process for optimizing any workflow. The crucial
insight is not just the steps, but their **strict ordering** -- most
organizations do them in reverse, which is why they stay inefficient.

The five steps, in order:

1. **Make your requirements less dumb**
2. **Delete the part or process**
3. **Simplify or optimize**
4. **Accelerate cycle time**
5. **Automate**

## Why the Order Matters

Most organizations jump straight to Step 5 (automate) because it feels
productive and technical. The result: highly efficient production of things
that shouldn't be produced at all, through processes that shouldn't exist.

**You must delete before you optimize.** If you automate a step that
shouldn't exist, you've made waste permanent and expensive to remove.

> Tesla once tore out hundreds of expensive robots from the production line
> because they automated too early -- before questioning whether those
> steps should exist at all.

## Step-by-Step Application

### Step 1: Make Your Requirements Less Dumb

Ask the user: "Walk me through every step in your current process. For
each step, who originally required it, and why?"

Key questions for each requirement:
- **Who asked for this?** Get a name, not a department. "Legal" is not
  a person. Requirements from nameless sources are suspect.
- **What happens if we remove it?** Often: nothing.
- **Is this still needed, or was it a response to a problem that no
  longer exists?**
- **Is this driven by regulation, or by someone's interpretation of
  regulation?**

**Critical insight**: The most dangerous requirements come from smart
people. You're less likely to question them. Question them anyway.
Many requirements come from people who no longer even work there.

**Rule of thumb**: If nobody can name the specific person who needs a
specific requirement, it's a candidate for deletion.

### Step 2: Delete the Part or Process

This is the hardest step because people fear deletion. The principle:

> If you're not adding deleted things back at least 10% of the time,
> you're not deleting enough.

**Deliberately overdelete.** It's almost always easier and cheaper to add
something back than to carry unnecessary weight forever.

Ask the user to categorize each step:
- **Essential**: Removing this breaks the output (physics, law, safety)
- **Valuable**: Improves quality, but the output works without it
- **Habitual**: Exists because it's always existed
- **Protective**: Added after a past failure; may be disproportionate

Delete habitual steps immediately. Challenge protective steps -- are they
proportionate to the risk they guard against?

**Target**: Remove at least 20% of steps. If the user can't identify
20% to remove, they haven't challenged hard enough.

### Step 3: Simplify or Optimize

Only now do you optimize what survived deletion:

- **Reduce complexity**: Fewer handoffs, fewer approvals, fewer tools
- **Combine steps**: Can two sequential steps become one?
- **Reduce unnecessary precision**: Measuring to millimeters when
  centimeters would do?
- **Standardize**: Inconsistency creates hidden complexity

**The most common mistake of smart engineers is to optimize a thing
that should not exist.** That's why this is step THREE, not step one.

### Step 4: Accelerate Cycle Time

Now make the simplified process faster:

- **Parallelize**: Which steps can happen simultaneously?
- **Remove wait times**: Where does work sit idle between steps?
- **Reduce batch sizes**: Smaller batches = faster feedback loops
- **Shorten feedback loops**: How quickly do you learn if something
  went wrong?

Ask: "Where does work stop moving? Where do things queue up?"

### Step 5: Automate

Only automate what survived Steps 1-4. At this point you're automating
a lean, simplified process -- not cementing waste.

Automation questions:
- What's repetitive and rule-based? -> Automate first
- What requires judgment but follows patterns? -> Semi-automate with
  human review
- What's genuinely novel each time? -> Keep manual (for now)

## Output Format

```
## The Algorithm Analysis: [Process Name]

### Current Process Map
| Step | Description | Owner | Time | Origin |
|------|------------|-------|------|--------|
| 1 | ... | ... | ... | ... |

### Step 1: Requirements Questioned
| Step | Requirement | Named Owner | Still Needed? | Action |
|------|------------|-------------|---------------|--------|
| ... | ... | ... | Yes/No/Test | Keep/Delete/Simplify |

### Step 2: Deletions
- Deleted: [list with reasoning]
- Deletion rate: X% of original steps
- (If < 20%, push harder)

### Step 3: Simplifications
| Before | After | Why |
|--------|-------|-----|
| ... | ... | ... |

### Step 4: Acceleration
- Parallelized: ...
- Wait times removed: ...
- New cycle time: X (was Y, Z% improvement)

### Step 5: Automation Candidates
| Step | Type | Tool/Method | Priority |
|------|------|-------------|----------|
| ... | Full/Semi/None | ... | High/Med/Low |

### Projected Impact
- Steps: X -> Y (Z% reduction)
- Cycle time: X -> Y (Z% faster)
- Resources: ...
```

## Application Beyond Engineering

The Algorithm applies to any process:

- **Hiring**: Question -> Delete unnecessary interview rounds ->
  Simplify remaining -> Accelerate scheduling -> Automate screening
- **Content creation**: Question -> Delete unnecessary approvals ->
  Simplify review -> Accelerate feedback -> Automate publishing
- **Personal routines**: Question -> Delete time-wasting habits ->
  Simplify commitments -> Batch similar tasks -> Automate (auto-pay,
  templates, etc.)
- **Meeting culture**: Question why each meeting exists -> Delete those
  without clear purpose -> Simplify agendas -> Shorten timebox ->
  Automate recurring updates via async tools

## Common Pitfalls

- **Skipping deletion**: "We can't delete anything" -- almost never true.
- **Premature automation**: Automating before simplifying locks in
  complexity permanently.
- **Fear of deletion**: Adding something back is usually easy and cheap.
  Not deleting is expensive every single day.
- **Optimizing the wrong metric**: Make sure you're accelerating what
  actually matters to the outcome.
- **Going backward through the steps**: This is the most common mistake,
  even for experts. Always restart from Step 1.
