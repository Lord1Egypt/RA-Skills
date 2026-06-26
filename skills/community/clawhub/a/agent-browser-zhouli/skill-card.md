## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to drive browser workflows, inspect pages, fill forms, capture screenshots or PDFs, manage session state, and test web interfaces through structured agent-browser CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad control over authenticated browser sessions can expose account data or perform unintended account-changing actions. <br>
Mitigation: Use disposable browser profiles or test accounts, avoid shared or committed auth.json files, and require explicit confirmation before submitting forms, uploading files, changing account data, posting content, or reading cookies/localStorage. <br>
Risk: Saved browser state, screenshots, PDFs, videos, and trace files may contain sensitive page content or credentials. <br>
Mitigation: Store generated artifacts only in approved locations, delete them when finished, and avoid committing or sharing captured state and media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/agent-browser-zhouli) <br>
- [Agent Browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash command examples and optional JSON-producing CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; uses the agent-browser CLI and can produce screenshots, PDFs, videos, trace files, saved browser state, and DOM snapshots during execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
