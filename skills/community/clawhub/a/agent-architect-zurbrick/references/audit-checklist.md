# Audit Checklist

Run this fast pass before recommending any structural change.

## Step 1: Confirm there is a real problem

- What is the observed symptom?
- Is it recurring, costly, or high-friction?
- Do you have more than one example, or is this a single anecdote?

If the evidence is weak, prefer **no change** or a very small local edit.

## Step 2: Identify the actual lane

- Is this mainly about voice or identity? → persona
- Is this mainly about judgment, guardrails, or workflow discipline? → rules
- Is this mainly about retention, recall, or storage placement? → memory
- Is this mainly about repeatable procedure or reusable workflow packaging? → skills

If you cannot tell, delay the recommendation and ask for one more concrete example.

## Step 3: Check for a smaller fix first

Before proposing a bigger change, ask:
- Would one sentence fix this?
- Would moving one fact into durable memory fix this?
- Does an existing skill just need tightening rather than a new skill?
- Is doing nothing better until recurrence is proven?

## Step 4: Name where the fix belongs

Do not say only "update the system."
Point to the likely home:
- `SOUL.md`
- `AGENTS.md` / `OPERATIONS.md`
- `MEMORY.md` / `memory/*.md`
- a specific skill directory

## Step 5: Bound the blast radius

State what should **not** be touched.
Examples:
- do not rewrite the constitution for a local execution miss
- do not create a new skill for a one-off task
- do not move durable preferences into daily logs only
- do not paper over weak rules by adding memory clutter

## Step 6: Emit the standard output

1. Diagnosis
2. Lane
3. Recommended fix type
4. Smallest justified patch
5. Risks / what not to touch

If confidence is low, say so explicitly inside the diagnosis instead of faking precision.
