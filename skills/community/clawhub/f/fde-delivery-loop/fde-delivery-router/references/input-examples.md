# Route input example

## Example 1: Only solution ideas

Input: "The client wants to build an agent that automatically generates weekly reports."

Judgment: This is a solution, not a confirmed issue. Route to `fde-problem-discovery`, first verify who writes the weekly report, current steps, time consumption, errors, usage results and unchanged constraints.

## Example 2: Existing interview and business data

Input includes: interviews with 5 frontline personnel, current process, weekly time consumption, reasons for rework, and target Owner.

Judgment: Check evidence coverage and question boundaries; route to `fde-engagement-charter` after passing, freezing the questions to be answered by the POC and input from both parties.

## Example 3: Customers directly request to build a demo

Input: "The leaders will visit next week. Let's make a demo version first."

Judgment: Start by checking for the presence of success criteria, available data, demo users, decision makers, and post-demo decisions. When missing, enter the POC contract and do not jump directly to the build.

## Example 4: Already have a PRD, but no data permissions

Assessment: A PRD file does not mean Stage 3 passed. Data sources and permissions are part of the executability and risk gates; complete these constraints in the PRD before deployment architecture.

## Example 5: POC works well but no one keeps using it

Judgment: Enter `fde-adoption-and-value`. Separately measure model quality, real-world usage, workflow changes, and business results.

## Example 6: Similar solution has been delivered three times

Judgment: Enter `fde-playbook-productizer`. First confirm whether the commonality is established across customers, and then decide to condense it into templates, deployment blueprints, evaluation sets, agent skills or product capabilities.

## Route output example

```markdown
## Current judgment
- Current stage: Stage 2 POC contract
- Recommended skills: fde-engagement-charter
- Judgment basis: The problem and users have evidence, but the success criteria, customer input and stopping conditions have not been confirmed.

## Gap
| Gap | Impact | owner | Completing action |
|---|---|---|---|
| The customer did not provide sample data | Unable to determine POC executability | Customer data manager | Provide de-identified samples or confirm Mock boundaries |

## After completing this stage, the output should be
- POC project contract
- A clear gateway into PRD
```
