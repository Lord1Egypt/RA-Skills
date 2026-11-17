## Description:

Builds and audits trust policies for browser/computer-use agents before they take real-world actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define and audit browser-agent execution policies, planned tool actions, domain allowlists, approval gates, and audit controls before live browser workflows run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom policy or action JSON can lead to misleading audit results if it does not accurately represent the planned browser workflow.

Mitigation: Review policy and action JSON before running the audit and treat REVIEW or BLOCK findings as pre-flight gates.

Risk: Browser-agent actions involving submission, payment, deletion, or other sensitive steps may proceed without adequate approval or evidence capture.

Mitigation: Require explicit human approval and screenshot or state capture before irreversible browser actions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON trust report with findings, verdict, score, and required controls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print JSON to stdout or write a report inside the skill directory when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
