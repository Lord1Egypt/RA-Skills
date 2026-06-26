## Description: <br>
Clawfy Pro processes browser extension webhook messages so an agent can use page URL, page context, and recent conversation context to detect intent, offer targeted help, and suggest relevant ClawHub skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VabbleJames](https://clawhub.ai/user/VabbleJames) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to respond to Clawfy Pro browser-extension webhook messages by interpreting page context and recent conversation context, offering direct assistance, and suggesting relevant ClawHub skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can receive browser page text, code blocks, URLs, and the last 10 chat messages when triggered. <br>
Mitigation: Install only when this context sharing is acceptable, and avoid triggering it on pages or conversations containing sensitive information. <br>
Risk: Responses may not clearly state that browser extension context informed the reply. <br>
Mitigation: Users should understand that Clawfy Pro-triggered replies can be based on browser context and recent chat context. <br>
Risk: Suggested ClawHub skills or install commands may be inappropriate for the user's task. <br>
Mitigation: Review suggested skills before manually installing them; this skill presents install commands but does not execute them. <br>


## Reference(s): <br>
- [Clawfy Pro skill page](https://clawhub.ai/VabbleJames/clawfy-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with ClawHub skill links and copyable shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include 3-5 skill suggestions, relevance explanations, and user-run clawhub install commands; does not execute installs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
