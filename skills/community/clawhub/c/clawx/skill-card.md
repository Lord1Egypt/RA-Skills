## Description: <br>
ClawX Agent Verification helps agents check verification status, embed verification widgets, and work with agent identity and trust tiers through ClawX OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianderrington](https://clawhub.ai/user/ianderrington) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to check an agent's ClawX verification tier before interaction and to display a trust indicator in a page or workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedding the ClawX widget loads a third-party script from clawx.ai. <br>
Mitigation: Before use on a live site, decide whether clawx.ai is trusted and apply normal web controls such as review, CSP, or version pinning if available. <br>


## Reference(s): <br>
- [ClawX verification API](https://clawx.ai/api/v1/agents/{handle}/verify) <br>
- [ClawX embeddable widget](https://clawx.ai/widget.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JSON, HTML, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example API responses, verification tier meanings, widget configuration, and rate-limit guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
