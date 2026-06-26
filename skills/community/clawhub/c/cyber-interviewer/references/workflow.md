# Workflow

## Inputs

Expect these inputs when available:

- local resume PDF path
- GitHub username, if repo discovery should be automatic
- one or more GitHub repository URLs or local repository paths
- target role
- target company or company list
- preferred interview language
- interview mode: `report`, `interactive`, or `both`

If a target role is missing, infer one from the evidence and say that the role was inferred.

If only a GitHub username is available:

1. discover recent public repositories first
2. prefer non-fork repositories by default
3. cap discovery to a manageable count unless the user asks for exhaustive review
4. tell the user which repositories were selected

## Phase 1: Resume Extraction

Read the resume PDF and extract:

- candidate summary
- work history
- project list
- claimed technologies
- metrics and impact claims

Flag:

- vague claims without implementation evidence
- inflated verbs without scale details
- project bullets that are likely to trigger deep follow-ups
- stack mismatch against the target role

## Phase 2: Repository Analysis

Start wide, then go deep:

1. Read the top-level structure.
2. Read the README, dependency files, and build or run instructions.
3. Identify the main execution path.
4. Inspect the most interview-relevant modules.
5. Inspect tests and evaluation or benchmark code.
6. Extract exact files, functions, classes, and failure-prone paths that are worth cross-examining.

For each repository, answer:

- What problem does this project solve?
- What is the control flow from input to output?
- Which exact files, classes, or functions carry the core responsibility?
- Which parts show engineering maturity?
- Which parts look fragile or under-explained?
- What questions would an interviewer naturally ask next?

When highlighting risks, sort them into:

- `bug`: likely correctness issue
- `design`: architecture or maintainability risk
- `evidence-gap`: claim appears stronger than the code supports
- `interview-risk`: area where the user may struggle to explain tradeoffs

## Phase 3: Fresh Interview Research

Search for recent interview experiences and role signals using role, company, location, seniority, and stack. Always include concrete dates in the final writeup.

Prioritize:

1. recent interview experience posts for the named company, if provided, from interview-heavy domains like Nowcoder first
2. company engineering blog or hiring rubric
3. current role descriptions for that company
4. broader role-level prep content only as fallback

Summarize trends, not isolated anecdotes. If only anecdotal sources exist, say that clearly.

## Phase 4: Synthesis

Merge the three evidence streams:

- resume claims
- code reality
- current interview expectations

Find mismatches such as:

- resume claims stronger than repository evidence
- repository quality stronger than resume wording
- likely interview topics not represented in the candidate story
- target-role expectations missing from both resume and code

## Phase 5: Interview Delivery

In `report` mode:

- provide the full report in one response

In `interactive` mode:

- provide a short setup summary
- ask one question
- wait for the answer
- ask the next question naturally without public scoring
- keep private notes on strengths, weak spots, and follow-up ideas
- stop when coverage is sufficient, not when a fixed count is reached
- deliver the consolidated critique only after the questioning phase is over

In `both` mode:

- provide the compact report
- then begin the interactive interview

Coverage is usually sufficient after you have tested:

- project ownership
- architecture and control flow
- tradeoffs and alternatives
- testing, correctness, and failure handling
- algorithm problem-solving, if the role normally includes coding rounds
- at least one company-specific pressure point when a company is provided

## Fallbacks

If the PDF is image-based and text extraction is weak:

- say that extraction quality is limited
- use visible headings and available text
- rely more on repository evidence

If the repository is inaccessible:

- continue with resume-only review
- give a checklist of what repo evidence is still needed

If the repository is very large:

- review the most central code path
- extract a few exact code surfaces to drill into instead of pretending to cover the whole codebase
- say what was not inspected
- avoid pretending to have covered the entire system
