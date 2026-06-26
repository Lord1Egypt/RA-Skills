# Engineer Communication Protocols

## Overview

All PM-to-engineer communication should be structured, specific, and actionable. Vague requests produce vague answers. Every request to the engineer should include enough context that the engineer can work independently and return a useful response without needing to ask clarifying questions.

The PM communicates with the engineer in a semi-technical register: you reference specific features, screens, data entities, and user flows — but you don't dictate architecture, technology choices, or implementation approaches. That's the engineer's domain.

**Delivery method:** Every request below should be posted to `queues/to-engineer.md` in the project folder using the standard queue message format, AND reflected as an Asana task in the Engineer Queue. The queue file entry is the record with full context attached; the Asana task is what the engineer tracks status through. Also send a `sessions_send` nudge to alert the engineer promptly.

Queue message wrapper for all requests below:
```
[YYYY-MM-DD HH:MM] [FROM: pm-agent] [TO: engineer] [TASK: asana-task-id]
[Request type and content below]
---
```

## Software Audit Request Template

Use this when a client comes with changes to existing software and you need to understand the current state before you can meaningfully discuss requirements.

```
SOFTWARE AUDIT REQUEST

Project: [Project Name]
Client: [Client Name]
Date: [YYYY-MM-DD]

PURPOSE
The client is requesting changes to [area of the software].
Before I can have an informed requirements conversation, I need
a clear picture of how these areas currently work.

AREAS TO AUDIT
Please provide a plain-language summary for each area below.
For each, cover:
  (a) What functionality currently exists
  (b) How the user interacts with it (the workflow/flow)
  (c) What data is involved (what's stored, displayed, processed)
  (d) What other parts of the system depend on or are affected
      by this area (dependencies and downstream impacts)
  (e) Any known technical debt, limitations, or quirks in this area

Areas:
1. [Feature/Screen/Module name]
   Context: [Why the client is interested in this area]

2. [Feature/Screen/Module name]
   Context: [Why the client is interested in this area]

3. [Feature/Screen/Module name]
   Context: [Why the client is interested in this area]

ADDITIONAL CONTEXT
[Any relevant background: what the client said, what they seem
to be trying to accomplish, any mockups or documents they shared]

RESPONSE FORMAT
Please structure your response as:
- One section per area audited
- Plain-language descriptions (I'll be sharing relevant parts
  with the client)
- Flag anything that would be particularly impactful or risky
  to change
- Note any areas where the current implementation is fragile
  or would benefit from refactoring as part of changes
```

## Technical Assessment Request Template

Use this after the client has confirmed the Requirements Summary and you need the engineer to evaluate feasibility, effort, and approach.

```
TECHNICAL ASSESSMENT REQUEST

Project: [Project Name]
Date: [YYYY-MM-DD]
Related Software Audit: [Yes/No — if yes, reference date]

REQUIREMENTS TO ASSESS
[Attach or inline the confirmed Requirements Summary]

For each requirement below, please provide:
  (a) Feasibility: Can this be done? Any showstoppers?
  (b) Technical approach: High-level approach (not full design)
  (c) Components affected: Which parts of the system are touched
      (frontend, backend, database, integrations, etc.)
  (d) Effort estimate:
      - Story points (for relative sizing)
      - Estimated human-hours by role (frontend dev, backend dev,
        QA, etc.)
      - Estimated AI-agent hours (how long our agents will take)
      - Complexity rating: Trivial / Low / Medium / High / Very High
  (e) Risks and concerns: What could go wrong, what's uncertain
  (f) Dependencies: What needs to happen first, or what does
      this block?

Requirements:

1. [Requirement from summary]
   Priority: [Must-Have / Should-Have / Nice-to-Have]
   Context: [Any additional context from the client]

2. [Requirement from summary]
   ...

ADDITIONAL QUESTIONS
- Are there any requirements that conflict with each other
  technically?
- Are there any requirements that would benefit from being
  implemented together (natural groupings)?
- Is there any preparatory work (refactoring, infrastructure)
  that should happen before the feature work?
- Are there any requirements where the client's request is
  technically possible but you'd recommend a different approach
  that better serves their stated goal?

RESPONSE FORMAT
Please return a structured assessment with one section per
requirement, using the (a)-(f) structure above. End with an
overall summary section covering cross-cutting concerns,
recommended implementation order, and total effort rollup.
```

## UI Comparison Request Template

Use this when changes involve interface modifications and you need visual representations to share with the client.

```
UI COMPARISON REQUEST

Project: [Project Name]
Date: [YYYY-MM-DD]

CONTEXT
The client has requested changes to [screen/feature]. I need
visual comparison materials to review with them.

REQUESTED DELIVERABLES

1. Current Interface Description
   For each screen/view affected, provide:
   - What the user sees (layout, elements, content areas)
   - What the user can do (interactions, buttons, flows)
   - Screenshot or description if codebase access allows

2. Proposed Interface Rendering
   Based on the requirements below, produce an HTML/CSS
   rendering of the proposed new interface. This should be:
   - A self-contained HTML file I can show the client
   - Focused on layout, information architecture, and workflow
     (pixel-perfect design isn't needed, but the structure and
     flow should be clear)
   - Interactive enough to demonstrate key workflows if applicable
   - Annotated with notes on what's new/changed vs. current

3. Side-by-Side Comparison
   A document or rendering that shows current vs. proposed
   with callouts highlighting the differences.

REQUIREMENTS DRIVING THE CHANGES
[List the relevant requirements from the Requirements Summary
or SRS that drive these interface changes]

CLIENT MOCKUPS (if provided)
[Reference any mockups the client has shared. Note: the
engineer should assess what the current interface looks like
relative to what the mockup shows, and flag any inconsistencies
or implementation concerns with the mockup.]

NOTES
- The HTML/CSS renderings will be shown to the client for
  feedback, so they should look clean and be self-explanatory
- If the client's mockup is unrealistic or problematic from
  a technical standpoint, note that in your response so I can
  discuss it with the client
- Focus on the user experience and workflow, not on final
  visual polish
```

## Implementation Plan Review Request

Use this after the engineer produces an implementation plan from the signed-off SRS. This isn't a request the PM initiates — it's the protocol for reviewing what the engineer delivers.

```
IMPLEMENTATION PLAN REVIEW PROTOCOL

When the engineer delivers the implementation plan, verify
the following:

SRS COVERAGE CHECK
For each requirement in the SRS:
- [ ] FR-XXX: Addressed in plan section [X] — Yes/No
- [ ] FR-XXX: Addressed in plan section [X] — Yes/No
(Go through every requirement ID)

ACCEPTANCE CRITERIA COVERAGE
For each acceptance criterion in SRS Section 10:
- [ ] Criterion for FR-XXX: Testing approach defined — Yes/No
(Verify each criterion has a corresponding test approach)

GAPS TO SURFACE
If any requirement or acceptance criterion is not addressed:

   IMPLEMENTATION PLAN GAP NOTICE
   Date: [YYYY-MM-DD]
   SRS Version: [X.X]

   The following SRS items do not appear to be addressed in
   the implementation plan:

   1. [FR/NFR-XXX]: [Requirement title]
      What's missing: [Specific gap — is the whole requirement
      missing, or is it partially addressed?]

   2. [FR/NFR-XXX]: [Requirement title]
      What's missing: [Description]

   Please update the plan to address these items, or explain
   why they are covered in a way I may have missed.

IMPORTANT: Do NOT review the engineer's technical approach
(architecture, technology choices, implementation details).
Only verify that every SRS requirement is accounted for and
that testing/QA approaches exist for every acceptance criterion.
The engineer owns technical decisions.
```

## General Communication Principles

1. **Always reference specific requirement IDs** when discussing items with the engineer. "The login feature" is vague; "FR-012: Two-factor authentication" is precise.

2. **Don't ask open-ended questions** when you need specific information. Instead of "What do you think about the reporting changes?" ask "For FR-025 through FR-030, can you confirm whether the existing report export functionality will be affected?"

3. **Set clear response expectations** in every request. Tell the engineer what format you need the response in and what information is critical.

4. **Batch your requests** when possible. One structured request with 10 items is better than 10 separate messages.

5. **Acknowledge receipt** of engineer deliverables and set expectations for your review timeline. "Received the technical assessment. I'll review against the requirements summary and get back to you within [timeframe]."

6. **Escalate, don't assume.** If an engineer's response is unclear or seems to miss something, ask for clarification rather than guessing. Misinterpretation creates downstream problems.
