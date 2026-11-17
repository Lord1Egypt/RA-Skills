## Description:

Set up or repair Gemini in Chrome (Glic) on Windows, macOS, or Linux when enabling it for the first time outside the US or when the sidebar, floating panel, Alt+G shortcut, or top-bar entry disappears.

This skill is ready for commercial/non-commercial use.

## Publisher:

[at386369-ai](https://clawhub.ai/user/at386369-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to guide setup or repair of Chrome Gemini/Glic by backing up and patching Chrome Local State, then checking the relevant flags and language settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill deliberately changes Chrome Local State to make Gemini/Glic appear eligible, including region fields and default language normalization.

Mitigation: Run the script with --dry-run first, close Chrome before writing, keep the generated backup, and use --language "" when language normalization is not desired.

Risk: Managed Chrome profiles or unsupported-region behavior may prevent the setup from working or may create policy and account-environment problems.

Mitigation: Avoid running it on managed or primary profiles when those changes would be disruptive, and stop if policy management blocks the setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/at386369-ai/skills/enable-chrome-gemini)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and Python script execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chrome Local State repair instructions, dry-run guidance, backup guidance, and platform-specific profile path handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
