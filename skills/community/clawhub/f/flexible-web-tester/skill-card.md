## Description: <br>
A Web UI testing workbench that supports MCP-driven browser operation and Python Playwright script generation, with three testing modes and mandatory human confirmation before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MillerAllen98](https://clawhub.ai/user/MillerAllen98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to plan and run Web UI tests against a target URL or feature requirement. It can generate natural-language test steps or Python Playwright scripts, then save test plans and reports after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad filesystem, terminal, browser-control, and login access. <br>
Mitigation: Use staging sites and disposable test accounts, prefer manual login, and approve execution only after reviewing the generated plan or script. <br>
Risk: Generated reports, screenshots, or logs may contain private page content or credentials. <br>
Mitigation: Choose a dedicated output folder and redact or delete saved artifacts before sharing them. <br>
Risk: Browser automation can perform real actions on live websites after confirmation. <br>
Mitigation: Run against test environments where possible and inspect generated scripts before allowing terminal execution. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/MillerAllen98/flexible-web-tester) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and test plans, with optional Python Playwright code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save dated test plan, script, screenshot, log, and report files in the selected working directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
