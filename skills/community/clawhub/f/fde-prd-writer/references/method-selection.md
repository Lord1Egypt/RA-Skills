# Method selection: serving handover decision-making

Use it only if a method can change the scope, priority, scheme, or validation method. Output conclusions and reasons; do not output complete "methodology homework" unless requested by the user.

| Decisions to be made | Preferred approach | Minimum output | When not applicable |
|---|---|---|---|
| What is the real problem behind the requirement | JTBD, Y model, 5W1H | Users, scenarios, pain points, expected results, assumptions to be verified | Users have given reliable problem evidence and goals |
| What to do and what not to do in this issue | KANO | Function classification, scope suggestions, reasons for selection | There is only a single requirement that must be delivered |
| Whether to do it, when to do it, which direction to choose | SWOT, Lean Canvas, Ansoff, PESTLE, Porter's Five Forces | Recommended solutions, key trade-offs, risks, next step verification | Only partial function refinement |
| How to explain complex experiences clearly | Mermaid state chart/flow chart | Key states, branches, asynchronous/failure paths | Single linear operation, numbered steps are clearer |
| How to ensure that stories are deliverable | INVEST | Story splitting that can be independently estimated, negotiable, and testable | The main body of the document uses functional requirements rather than agile stories |
| How to ensure that the completion can be judged |Given/When/Then| Observable AC and corresponding test scenarios | There are no observable results, go back to requirements clarification first |

## Correct placement of common methods

### KANO: Auxiliary range selection

Basic demand is regarded as the bottom line of quality, expected demand is regarded as the competitiveness of the current period, and exciting demand is only included when goals and resources support it. Don’t automatically equate “excited” with high priority, and don’t substitute KANO for user evidence.

### Strategic frameworks such as SWOT: assisting in “whether to do” decisions

Keep only 3–5 key points that impact the decision. Finally, write down recommendations, trade-offs, risks, and verification actions in the PRD instead of stacking four quadrants.

### Mermaid: Reduce misunderstandings of complex processes

Prioritize drawing state changes, responsibility boundaries, conditional branches and asynchronous callbacks. Diagrams do not replace rules, permissions, or acceptance criteria; each item must still map to `FR-`and`AC-`.

### JTBD / 5W1H: Avoid treating solutions as requirements

Start by asking the user what task they want to complete, in what context it occurs, and what the current alternatives and costs are. Write the conclusion as "Problem and Target User", and mark the unproven judgment as `[Hypothesis]`.
