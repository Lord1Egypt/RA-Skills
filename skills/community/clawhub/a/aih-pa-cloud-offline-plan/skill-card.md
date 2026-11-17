## Description:

Helps users plan work that can continue while their computer is off, distinguishing cloud tasks from local dependencies and producing an offline task list, dependency map, and budget table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

People planning offline or cloud-assisted work use this skill to identify tasks that can run remotely, local prerequisites, checkpoints, and spending limits. Optional AI-HIVE execution requires available tools and explicit authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files may be unavailable after shutdown or uploaded outside the approved scope.

Mitigation: Separate cloud and local steps, pause work requiring unavailable files, and confirm exactly which materials may be uploaded.

Risk: Paid or external actions may exceed the user's budget or authorization.

Mitigation: Confirm current pricing, currency, budget cap, and action-specific permission before spending or changing external systems.

Risk: Credentials or sensitive materials could be disclosed during connection or task preparation.

Mitigation: Use the provider's own sign-in flow; do not collect passwords, tokens, verification codes, cookies, or full identity documents in task materials.

Risk: A task could be reported complete without the necessary tools or a verified result.

Mitigation: Check available tools and result records, label unexecuted steps clearly, and verify external results before claiming completion.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/aih-pa-cloud-offline-plan)
- [Offline workflow and acceptance](references/workflow-18.md)
- [AI-HIVE connection and authorization](references/ai-hive-connection.md)
- [Result record and verification](references/output-contract.md)
- [AI-HIVE web interface](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Task list, dependency map, and budget table; optional CSV or JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records distinguish planned work from verified execution and retain sources and checkpoints.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
