## Description: <br>
Chrome Devtools Axi guides agents in using the chrome-devtools-axi CLI for Chrome DevTools Protocol browser automation, including accessibility snapshots, stale-ref-safe interactions, screenshots, console and network inspection, Lighthouse, and performance traces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a task requires terminal-driven Chrome DevTools automation, browser interaction through accessibility refs, or diagnostics from console, network, screenshot, Lighthouse, performance, or heap tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect an agent to Chrome DevTools, including existing browser sessions or profiles that may expose private browsing state. <br>
Mitigation: Prefer fresh isolated browser sessions, connect to normal logged-in profiles only when the user authorizes that scope, and stop the bridge when persistent state is no longer needed. <br>
Risk: Authenticated WebSocket headers or other DevTools connection values may contain secrets. <br>
Mitigation: Keep WebSocket header values private and avoid printing or publishing raw secret-bearing environment variables. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/kunchenguid/chrome-devtools-axi) <br>
- [ClawHub skill page](https://clawhub.ai/tmchow/chrome-devtools-axi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and environment variable guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes privacy-sensitive browser session handling and verification practices.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
