## Description:

This skill helps agents use the agent-browser CLI to automate browser navigation, clicks, form filling, screenshots, and web information capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huang-shao](https://clawhub.ai/user/huang-shao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they need browser automation guidance for check-ins, form completion, page inspection, screenshots, or web data collection through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide browser actions on logged-in sites, including account actions, form submission, screenshots, and scheduled check-ins.

Mitigation: Require explicit confirmation before submitting forms, clicking account actions, capturing sensitive screenshots, or setting up recurring browser actions.

Risk: Installation guidance uses a global npm install and does not pin the CLI version.

Mitigation: Prefer a pinned, locally installed CLI version and avoid administrative or global installs when possible.

Risk: Example workflows include credentials and recurring scripts.

Mitigation: Do not store plaintext passwords in scripts, and review scheduled automation before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huang-shao/skills/agent-browser-cli-bak-skip)
- [ClawHub publisher profile](https://clawhub.ai/user/huang-shao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include browser action sequences and example shell scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
