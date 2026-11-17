## Description:

Runs Cue's industry-research workflow to investigate industries or companies, covering market size, competitive landscape, business models, supply chains, policy impacts, and compliance checks with source-linked research drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaoxu](https://clawhub.ai/user/wangxiaoxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to run Cue-powered deep research on industries, companies, sectors, ETFs, industry cycles, competitive positioning, supply chains, and policy impact. It returns source-linked research drafts and should be reviewed before use in diligence, investment, legal, or underwriting decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install, update, and execute mutable external runner code from the sensedeal/cue-skills repository.

Mitigation: Use a trusted checkout, pin it to a reviewed commit when possible, and review the runner script before execution.

Risk: The runner may read the local Cue API key from ~/.cue/config.json and spend Cue credits.

Mitigation: Confirm API-key access and credit spending with the user before each run, as the skill instructs.

Risk: Generated industry research may be incomplete or unsuitable as final diligence, legal, underwriting, or investment advice.

Mitigation: Preserve source links, review the report, and verify important findings before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangxiaoxu/skills/cue-industry-research)
- [Cue Playbook API](https://cuecue.cn/api/playbook)
- [Cue Skills Runner Repository](https://github.com/sensedeal/cue-skills)
- [Cue Skills Runner Gitee Mirror](https://gitee.com/sensedeal/cue-skills)
- [Cue API Key Page](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with source links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger live Cue API calls, external runner execution, and credit consumption after user confirmation.]

## Skill Version(s):

1.0.2 (source: target metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
