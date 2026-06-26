## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roseknife520](https://clawhub.ai/user/roseknife520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to drive deterministic browser automation from an agent, including navigation, ref-based interactions, data extraction, session isolation, and browser state management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser-session features can expose login data, cookies, local storage, or saved authentication state if used carelessly. <br>
Mitigation: Use isolated or in-memory sessions, avoid personal browser profiles unless explicitly needed, do not print raw cookies or storage values, and treat saved auth-state files like passwords. <br>
Risk: Automation against untrusted pages can act on misleading page content or unstable UI state. <br>
Mitigation: Use JSON snapshots, wait for page stability, verify refs before interaction, and review high-impact actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/roseknife520/agent-browser-clawdbot-rose) <br>
- [agent-browser homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide an agent to run the external agent-browser CLI and parse JSON snapshots, refs, and state responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
