## Description: <br>
Diagnose and fix common frontend issues -- white screen, JS errors, resource loading failures, React/Vue hydration, browser extension popup, and CSS layout bugs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[727155455](https://clawhub.ai/user/727155455) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to diagnose common web application failures, gather relevant browser and project context, and produce concrete fixes for rendering, hydration, resource loading, extension popup, JavaScript, and CSS layout issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI report can include local file paths and source snippets from the project being diagnosed. <br>
Mitigation: Run it only in the intended project and review output before sharing it outside the team. <br>
Risk: Troubleshooting guidance and proposed fixes may be incomplete for project-specific build, framework, or deployment constraints. <br>
Mitigation: Review suggested code and configuration changes, then verify them in the target browser, build pipeline, and deployment environment. <br>
Risk: Using an unexpected package source could expose users to a different implementation than the reviewed release. <br>
Mitigation: Install only from the package or source intended for this ClawHub release. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/727155455/frontend-doctor) <br>
- [OpenClaw ClawHub homepage](https://github.com/openclaw/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with diagnostic checklists, code snippets, shell commands, configuration examples, and local scan report text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled CLI scans local frontend project files and prints root cause, evidence, and fix entries; agent use may also produce conversational troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
