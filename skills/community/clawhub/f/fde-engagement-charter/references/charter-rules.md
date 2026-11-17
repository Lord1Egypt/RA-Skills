# POC Contract Rules

## Success criteria structure

Each POC standard uses the following structure:

```text
Within the [user/scenario/data range], the system should reach [observable indicators and thresholds],
Confirmed by [Owner] through [Evidence Collection Method];
After passing [next decision], after failure [stop/adjust/supplementary verification].
```

Success criteria cover relevant items in at least four categories:

- Business: time, quality, cost, risk, revenue or experience;
- User: task completion, usability, trust, reuse willingness and human intervention;
- Technology: accuracy, completeness, latency, reliability, integration and cost;
- Risks: Override of authority, sensitive information, unacceptable output, auditing and rollback.

Don't average all indicators. Critical safety or compliance items should be hard thresholds.

## Scope Negotiation Rules

- Prioritize one role, one trigger, one end-to-end workflow, limited data scope;
- When using Mock, state what the Mock replaces and therefore cannot prove anything;
- Separate “must prove core value” from “just to make the presentation look good”;
- Any new scope must describe which POC standard it serves, what it adds to the cost, and what it replaces;
- Make decisions based on evidence when the time box expires, and do not avoid conclusions through infinite extensions.

## Responsibility Model

| Role | Minimum Responsibilities |
|---|---|
| Client Business Sponsor | Confirm goals, priorities, user involvement and final decisions |
| Customer User Representative | Provide real scenarios, feedback and result confirmation |
| Customer Technology/Data Owner | Provides data, access, environment and risk information |
| FDE Leader | Manage scope, evidence, blocking and handoff quality |
| R&D/Platform Leader | Confirm feasibility, technical risks and releases |
| Security/Legal/Compliance | Define unacceptable risks and approval conditions |

## Change, Pause and Stop

Pause and reaffirm the contract when any of the following is triggered: core data is unavailable, users cannot participate, success criteria are required to be temporarily lowered, risks exceed the agreement, scope increases beyond the time box.

Stopping is not failure management, it is effective decision-making. Document stopping reasons, learnings acquired, reusable assets, and restart conditions.

## PRD entry check

- Success criteria can be mapped to acceptance scenarios;
- The scope can be broken down into specific user behaviors;
- Data/system constraints are sufficient to write specifications;
- Pending items do not affect the core plan, or already have a Owner and deadline;
- Both parties agree on the time box and decision-making mechanism.
