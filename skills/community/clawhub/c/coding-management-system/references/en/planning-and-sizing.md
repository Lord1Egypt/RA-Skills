# Planning And Sizing 2.1

Size a goal after it is `Ready for Planning`. Size reflects uncertainty, risk, acceptance breadth, and coordination, not AI typing speed.

## Size Matrix

| Dimension | Small | Medium | Large |
| --- | --- | --- | --- |
| Surface | One narrow behavior or artifact | Related multi-file or subsystem change | Cross-subsystem, migration, architecture, or release |
| Acceptance | Directly testable | Several criteria or one important flow | Multiple flows, environments, or stakeholder decisions |
| Uncertainty | Known approach | Some discovery or integration risk | Material unknowns or competing designs |
| Risk | Local and reversible | Moderate regression or data risk | Production, security, data integrity, or broad regression |
| Coordination | One agent can implement and verify | Developer plus independent QA | Planner, Developer, QA, and possibly Owner |

Choose the highest size indicated by any material dimension.

## Ten-Stage Budget

| Size | Stage ceiling | Ten-stage horizon | Default governance | Compact soft ceiling |
| --- | ---: | ---: | --- | --- |
| Small | 30 minutes | 5 hours | Lite | 6 files / 30k characters |
| Medium | 60 minutes | 10 hours | Standard | 10 files / 60k characters |
| Large | 120 minutes | 20 hours | Full | 16 files / 100k characters |

Time and context are ceilings, not quotas or completion promises. A stage is an outcome checkpoint, not a Milestone, Work Order, handoff, or document.

Suggested stages: orient, reproduce, first vertical slice, core behavior, integration, primary flow, material edge cases, affected regression, target-environment rehearsal, evidence consolidation and formal alignment. Adapt or finish early when evidence is sufficient.

## State-Based Resizing

| Signal | Action |
| --- | --- |
| Useful progress and stable authority | Continue current size |
| First local failure with known cause | Same Packet; bounded repair |
| Same failure signature twice without new evidence | Stop and re-plan, resize, or block |
| Scope grows more than 20 percent | Re-size before continuing |
| User flow fails behind green checks | Keep open; strengthen functional evidence |
| Global misalignment | Stop execution; run formal alignment |
| Owner decision or protected boundary | Stop autonomous work |
| Terminal Standard/Full stage passes | Ready for Independent Acceptance |

Work expected to exceed 20 hours must split into independently valuable Programs or return for Owner rebaseline.

## Planning Output

Produce one user-visible outcome, minimum useful scope, Non-Goals, delivery class, labeled acceptance criteria and failure examples, size and reasons, governance, stage ceiling and alignment points, risks, Owner decisions, one first-stage outcome, one next action, and required automatic/functional/target-environment evidence.
