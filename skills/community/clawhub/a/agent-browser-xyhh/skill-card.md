## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyhh](https://clawhub.ai/user/xyhh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to drive browser workflows from an agent, including navigation, interaction, form filling, UI testing, page inspection, screenshots, PDFs, recordings, and saved session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing and running the agent-browser npm package and browser components.

Mitigation: Install only when the package and source are trusted, and run it in a low-risk environment.

Risk: Browser artifacts can contain sensitive information, including screenshots, PDFs, recordings, cookies, localStorage, basic-auth values, headers, and saved state files such as auth.json.

Mitigation: Treat these artifacts like credentials, avoid exposing them in logs or shared workspaces, and clean them up after use.

Risk: Automated browser actions can interact with real accounts, forms, uploads, and network requests.

Mitigation: Use scoped test accounts where possible, review targets before destructive actions, and keep credentials and upload files limited to the task.

## Reference(s):

- [Agent Browser Xyhh ClawHub Skill](https://clawhub.ai/xyhh/skills/agent-browser-xyhh)
- [xyhh ClawHub Publisher Profile](https://clawhub.ai/user/xyhh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and optional JSON CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide browser automation that creates screenshots, PDFs, recordings, uploaded files, cookies, localStorage, headers, credentials, and saved state files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
