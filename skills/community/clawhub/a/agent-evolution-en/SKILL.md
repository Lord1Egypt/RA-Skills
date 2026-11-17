---
name: agent-evolution-en
description: Apply metacognition and scientific creativity during research and complex knowledge work. Capture reusable outcomes in project memory as they emerge, then retrieve, verify, and improve them on later tasks. Use for saving research questions, hypotheses, diagnostic experiments, methods, decisions, and completed artifacts, for short post-task reviews, or for validating and rolling back durable agent practices. Use ongoing capture and review in projects where the user has enabled the memory loop.
---

# Metacognition × Scientific Creativity: Research Agent Evolution Plan

Use metacognition to regulate the current task and scientific creativity to generate and test ideas. Turn reusable outcomes into project memory. On later tasks, observe their value, limits, and exceptions, then update the records. **Capture can happen as work produces results. A closing review provides a second entry point.**

## 1. Start the task and retrieve relevant memory

- Identify the goal, important constraints, and acceptance criteria. Use project memory the host actually reads and that you can access. Retrieve a few relevant entries when helpful. Check scope, version, and supporting evidence. Treat candidate hypotheses and practices as material for exploration.
- Use the [creative metacognition framework](https://doi.org/10.1016/j.plrev.2023.07.002) to choose a strategy before work, monitor goals and progress during work, and evaluate outcomes and transferable practices afterward. Proceed directly when the goal is clear. Verify evidence, reframe, change the comparison, adjust scope, or stop when evidence is thin, ideas converge, predictions are indistinguishable, or costs exceed expectations.

## 2. Generate, verify, and capture outcomes during work

- Apply [Geneplore's generation and exploration framework](https://mitpress.mit.edu/9780262061506/creative-cognition/) and [dual-space search](https://doi.org/10.1016/0364-0213%2888%2990007-9) as appropriate. For example, propose distinct mechanisms for the same phenomenon, then find observations for which they make different predictions. Reframe scientific questions, combine methods, map relational analogies, or examine anomalies when useful.
- Capture a short record when a reusable milestone emerges, the user confirms an important decision, external verification yields a finding, or the work is about to change tasks. Include a minimal summary, a source or artifact location, scope, current status, and a trigger for recall or rechecking. Preserve a reusable pointer to completed artifacts. Save untested scientific ideas as candidates with a way to distinguish their predictions.
- Retain the minimum authorized information when work involves identifiable participants, unpublished data, or other sensitive material. Merge updates for the same result. Keep the current task primary. Complete simple tasks directly and skip memory writes when there is nothing useful to add.

## 3. Review and consolidate after the task

The project can disable reviews, run them after meaningful outcomes or changes, or run one after every task. Default to reviewing meaningful outcomes and changes when frequency is unspecified. Finish the check without writing when there is nothing useful to retain. Ask three questions:

1. **Outcome.** Which artifact, decision, or evidence can be reused?
2. **Process.** Which approach helped, and which obstacle warrants a check? Successes, partial successes, failures, and surprises can all inform later work.
3. **Transfer.** Does the lesson apply only here, or does evidence support reusing it across a class of tasks? How could the next task check whether it still holds?

Use [CoALA's modular memory architecture](https://openreview.net/pdf/07475727a2787df12052196b9f2624497ef3c3bd.pdf) to distinguish episodes, semantic knowledge, and procedural practices. Preserve episodes for traceability. Record confirmed artifacts, decisions, and facts with their evidence status. Try hypotheses, one-off successes, and tentative explanations under stated conditions. Use a new task and a regression case before adopting an experience as a standing procedural rule. See [Memory and Evaluation Operations](references/operations.md).

## 4. Reuse, consolidate, and revise

- Retrieve records that match the later task and its conditions. Check whether key sources and constraints have changed. Record new evidence about what worked, what failed, or where the scope changed. Merge, replace, or archive entries as appropriate. Give current user instructions and verified project facts priority.
- To adopt a standing rule, state the behavior to improve and existing behavior to preserve. Keep evaluation conditions comparable and compare baseline and candidate on examples held out from tuning. After the candidate passes, write it to the project's procedural memory that the host actually loads. Preserve evidence and a recoverable version. Use isolated trials for complex changes. Update explicit user preferences and verifiable facts based on their sources.
- The optional [memory utility](scripts/evolve.py) captures and retrieves entries during or after work, and supports staging, adopting, and rolling back durable memory revisions. Prefer an existing authorized memory interface. Configure per-task reviews at a project entry point the host loads and verify them in a new session. See [Product Patterns and Integration](references/product-patterns.md).

Deliver the requested work. When a memory update will affect future work, briefly state what was recorded, its status, and where it lives. Distinguish recording, later retrieval, and verified changes in later behavior.
