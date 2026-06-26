## Description: <br>
Interact with a local Chrome-family browser session over CDP when the user explicitly asks to inspect, debug, or interact with a page they already have open. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[web3toolshub](https://clawhub.ai/user/web3toolshub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect, debug, capture, and interact with pages in a local Chrome-family browser session after the user enables remote debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and control a real local Chrome-family browser session, including pages with sensitive logged-in content. <br>
Mitigation: Use it only after an explicit user request, prefer a separate browser profile or close sensitive tabs, and stop the daemon or disable remote debugging when finished. <br>
Risk: Raw CDP, evaluation, navigation, typing, clicking, and tab-opening commands can perform broad browser actions. <br>
Mitigation: Review command intent before execution and avoid evalraw unless the CDP method and parameters are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/web3toolshub/chrome-cdp-skill) <br>
- [Skill homepage](https://github.com/web3toolshub/chrome-cdp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include browser tab listings, screenshots, accessibility snapshots, page HTML, network timing summaries, CDP command results, and operational guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
