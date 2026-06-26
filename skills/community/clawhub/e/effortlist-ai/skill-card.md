## Description: <br>
Manage EffortList AI folders, tasks, todos, schedules, booking links, and appointments through the EffortList AI platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Quarantiine](https://clawhub.ai/user/Quarantiine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users authorize an agent to organize EffortList folders, tasks, todos, schedules, booking links, and appointments on their behalf. The skill is intended for account management workflows where the user wants agent assistance with planning, scheduling, CRUD operations, undo/redo, and appointment review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated account and scheduling operations can change personal data beyond drafting task plans. <br>
Mitigation: Install only when the user intends the agent to manage the EffortList account, and keep the EFFORTLIST_API_KEY scoped to trusted agent environments. <br>
Risk: Deletes, bulk changes, booking-link updates, appointment decisions, OTP flows, and guest notifications can have high-impact or public-facing effects. <br>
Mitigation: Require explicit user confirmation before these actions and summarize the records, guests, times, and availability changes before execution. <br>
Risk: Scheduling conflicts or unintended appointment changes can occur when overriding availability or modifying booked items. <br>
Mitigation: Check current availability and user scheduling preferences before modifications, respect conflict responses, and use undo/redo only as a recovery mechanism after user review. <br>


## Reference(s): <br>
- [EffortList AI ClawHub listing](https://clawhub.ai/Quarantiine/effortlist-ai) <br>
- [EffortList homepage](https://www.effortlist.io) <br>
- [EffortList API documentation](https://www.effortlist.io/docs) <br>
- [EffortList security documentation](https://www.effortlist.io/security) <br>
- [Technical API Reference](references/api.md) <br>
- [Omni Architecture & Lifecycle](references/architecture.md) <br>
- [Security & Data Privacy](references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with REST API endpoint references and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EFFORTLIST_API_KEY and may perform authenticated account, scheduling, booking, appointment, and delete operations.] <br>

## Skill Version(s): <br>
1.10.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
