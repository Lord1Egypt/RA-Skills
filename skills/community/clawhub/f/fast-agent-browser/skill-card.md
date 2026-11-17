## Description:

Python CLI tool for AI agents to automate web browsers with Playwright, supporting navigation, interaction, snapshots, screenshots, and form handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent builders use this skill to automate browser navigation, element interaction, page inspection, screenshots, and form workflows through a Python CLI backed by Playwright.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad browser control over arbitrary URLs and page scripts.

Mitigation: Approve browser actions explicitly and avoid authenticated, internal, financial, admin, or private sites unless the workflow is isolated and reviewed.

Risk: Screenshots, extracted text or HTML, uploaded files, cookies, and auth state may contain sensitive information.

Mitigation: Treat captured outputs and browser profiles as sensitive, use isolated test accounts, and restrict uploads to approved files.

Risk: Server security review says the skill overstates its safety controls.

Mitigation: Review commands before execution, pin dependencies, and validate behavior in a controlled environment before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leohuang8688/skills/fast-agent-browser)
- [README](artifact/README.md)
- [API documentation](artifact/docs/api.md)
- [Playwright](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output can include plain text, HTML snippets, screenshots, PDFs, and browser state data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser outputs may include sensitive page content, uploaded files, cookies, or authenticated session state.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
