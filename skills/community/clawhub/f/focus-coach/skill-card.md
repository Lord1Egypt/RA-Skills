## Description: <br>
Focus coach for AI agents: diagnose focus blockers using BJ Fogg B=MAP and return one tiny action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Daisuke134](https://clawhub.ai/user/Daisuke134) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and AI agents use this skill to diagnose a current focus blocker and receive one small, concrete action for restoring attention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's focus situation to an external API. <br>
Mitigation: Avoid including secrets, confidential work details, health information, or sensitive personal data in requests. <br>
Risk: The skill uses a paid x402 request flow through a wallet or payment-capable account. <br>
Mitigation: Confirm each paid request is intentional and that the wallet or account is appropriate for small USDC charges. <br>
Risk: The skill depends on the pinned awal npm CLI for authentication and payment execution. <br>
Mitigation: Install only the documented pinned CLI version and review the command before running it. <br>


## Reference(s): <br>
- [Focus Coach Skill Page](https://clawhub.ai/Daisuke134/focus-coach) <br>
- [Focus Coach x402 API](https://anicca-proxy-production.up.railway.app/api/x402/focus-coach) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, json, shell commands] <br>
**Output Format:** [JSON response from an external API, with setup and payment commands documented in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The response includes a focus diagnosis, one tiny action, environment design guidance, and a safety flag.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
