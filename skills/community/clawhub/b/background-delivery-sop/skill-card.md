## Description:

Standardizes how agents handle background, sub-agent, or ACP work so completed results are proactively delivered back to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangwang0301](https://clawhub.ai/user/wangwang0301)

### License/Terms of Use:

MIT-0

## Use Case:

Agent builders and workflow maintainers use this skill to make async, background, sub-agent, and ACP task handling end with a clear final result, progress update, or blocker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may over-apply the SOP and move routine tool work into background execution when a local response would be clearer.

Mitigation: Review the workflow wording before deployment and tune it for teams that prefer more work to remain in the main session.

Risk: Acknowledgment examples may not match every user's language or communication style.

Mitigation: Adapt example acknowledgments to the deployment audience while preserving the requirement to send one start update and one completion delivery.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance and response patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; the skill provides operating rules for agent responses.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
