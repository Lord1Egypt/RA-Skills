## Description:

Volcseed helps an agent submit image-editing prompts with reference image URLs and fetch the resulting task output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to call the Volcseed image-editing submit and fetch flow with a prompt, reference image URLs, and a task ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bearer token is sent to URLs supplied through AIZNT_PROXY_URLS.

Mitigation: Install only after verifying that AIZNT_PROXY_URLS contains HTTPS endpoints controlled by the intended Volcseed or Tianshu service.

Risk: Prompts and image URLs are transmitted to the configured external service.

Mitigation: Do not submit sensitive prompts, private image URLs, or regulated data unless the service and data handling terms are approved for that use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangshengli0421/skills/aiznt-volcseed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TS_TOKEN and AIZNT_PROXY_URLS; submit output is a task response and fetch output is the task result JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
