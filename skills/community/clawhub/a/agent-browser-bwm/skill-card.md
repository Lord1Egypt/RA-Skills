## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate headless browser workflows that need deterministic element selection, session isolation, interaction, extraction, and browser state persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can expose sensitive cookies, localStorage, and saved authentication state. <br>
Mitigation: Use dedicated test accounts where practical, avoid printing or committing cookies, localStorage, or saved auth JSON files, and delete saved browser state when it is no longer needed. <br>
Risk: The workflow depends on an external agent-browser npm package and Chromium download. <br>
Mitigation: Install only when the external package and browser download source are trusted for the target environment. <br>


## Reference(s): <br>
- [Agent Browser repository](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-browser commands may produce JSON snapshots, screenshots, PDFs, cookies, storage values, or saved browser state depending on the workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
