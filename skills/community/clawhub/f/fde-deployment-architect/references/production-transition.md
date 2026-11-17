# POC to production transition

## Core Principles

A POC does not automatically qualify for production launch by proving only assumptions within the frozen scope. The production transition must turn mocks, manual patches, shared accounts, manual deployment, small samples and on-site support in the POC into operational control one by one.

## Seven production transition workflows

| Workflow | Core Issues | Minimum Exit Evidence |
|---|---|---|
| Identity and Permissions | Who can access what, perform what, how to revoke and audit |SSO/RBACDesign, least privilege testing, key rotation, approval |
| Data and integration | Is data contract, timeliness, quality, failure and recovery clear | Integration testing, lineage, quality gates, quotas and error drills |
| AI and evaluation | Can models, retrieval, tools and guardrails continue to return | Independent evaluation, red teams, version freezes, drift and regression mechanisms |
| Reliability and Operations | How to monitor, alert, degrade, rollback and respond to events | SLO, dashboard, runbook, on-call, drill records |
| Security and Compliance | Are risks accepted by authorized persons | Threat models, privacy assessments, audits, security/legal approvals |
| Users and Change | Will users stay engaged and know when to upgrade labor | UAT, training, support, feedback, exit and adoption planning |
| Governance & Business | Who owns budget, roadmap, vendor and go-live decisions | TCO, support model, RACI, procurement and change approvals |

## POC Technical Debt Clearance Form

| POC approach | Why accepted at that time | Production risk | Production substitution | owner | Deadline | Blocking the rollout |
|---|---|---|---|---|---|---|
| Mock Interface | | | | | | Yes/No |
| snapshot data | | | | | | |
| Manual deployment | | | | | | |
| Shared or temporary account | | | | | | |
| Small sample evaluation | | | | | | |
| Manual on-site full disclosure | | | | | | |

Specific technical debt cannot be summarized as "optimize after going online". Each item must describe the risks and authorized recipients.

## Grayscale stage

1. **Synthesis/Offline**: Verification process, interface contracts and obvious guardrails;
2. **Test environment**: Verify identity, integration, version, logs and error handling;
3. **Shadow Mode**: Read the real traffic but do not change the business results;
4. **Controlled pilot**: limited users, limited scenarios, clear time box and manual confirmation;
5. **Expansion in batches**: Open in batches according to users, scenarios, regions or risk levels;
6. **Stable Operations**: Go into SLO, duty, incident, capacity, cost and change governance.

Write entry conditions, exit conditions, stop conditions, observation windows and decision-makers at each stage. Do not write only the words "grayscale release".

## Rollback and downgrade

The rollback scenario at least answers:

- Which indicators, events or customer signals trigger rollback;
- Who has the authority to decide, who executes, and the maximum response time;
- Which versions of applications, configurations, models, prompts, knowledge bases, data and permissions are rolled back;
- How to compensate for write operations that have occurred, and how to return unfinished tasks to manual work;
- How to preserve evidence, notify users, investigate root causes and re-enter after rollback.

Systems without write operations also require degradation solutions, such as hiding entries, switching read-only, stopping generation, and returning to search or manual processes.

## Operation and knowledge transfer

The production transition handover package includes at least:

- System and data diagram, asset list, owners and dependencies;
- Deployment, configuration, version, key and environment description;
- Logs, metrics, alerts, dashboards and SLOs;
- Contact person for normal operation, common faults, S0–S3 events and upgrades;
- Rollback, recovery, data repair and evidence retention;
- Update rules for models, knowledge bases, evaluation sets and guardrails;
- Cost, capacity, limits and supplier troubleshooting;
- User training, support channels, and known limitations.

Have operation and maintenance or customer technical personnel who are not involved in the POC complete a walkthrough based on the runbook. Systems that must rely on verbal guidance from the original FDE to recover have not yet completed knowledge transfer.

## Production Ready Decision Record

```markdown
| Access Control | Status | Evidence | Residual Risk | Recipient | Decision Date |
|---|---|---|---|---|---|
| Identity permissions | | | | | |
| Data Integration | | | | | |
| AI Assessment | | | | | |
| Reliable operation | | | | | |
| Security Compliance | | | | | |
| Users and Support | | | | | |
| Business Governance | | | | | |
```

The status can only be "Passed/Conditionally Passed/Blocked/Not Applicable". "Conditional pass" must have a deadline and escalation blocking rules.
