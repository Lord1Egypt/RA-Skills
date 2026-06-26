## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ddbq](https://clawhub.ai/user/ddbq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate browser workflows with deterministic accessibility snapshots and ref-based interactions, including navigation, form entry, session isolation, state checks, and page data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved sessions, cookies, local storage, screenshots, and PDFs can expose access to logged-in accounts or sensitive page content. <br>
Mitigation: Treat those files as sensitive, store them only in trusted locations, and avoid sharing or committing them. <br>
Risk: Browser automation can perform unintended actions on real accounts when run without supervision. <br>
Mitigation: Use the skill only on intended sites, review planned actions before execution, and avoid unsupervised workflows on production accounts. <br>
Risk: The skill depends on an external agent-browser package and command-line browser runtime. <br>
Mitigation: Install it only from a trusted source and keep the runtime scoped to the sites and sessions needed for the task. <br>


## Reference(s): <br>
- [agent-browser homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create browser state files, screenshots, PDFs, and saved cookies or local storage through the external CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
