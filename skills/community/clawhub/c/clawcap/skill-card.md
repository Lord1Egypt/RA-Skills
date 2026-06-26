## Description: <br>
ClawCap routes OpenClaw provider traffic through clawcap.co so agents can enforce daily and monthly spending caps, detect runaway loops, and trigger remote stops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kintupercy](https://clawhub.ai/user/Kintupercy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route configured model providers through ClawCap for centralized spend caps, usage visibility, loop detection, and emergency stop controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw provider traffic and provider forwarding are routed through the third-party ClawCap proxy. <br>
Mitigation: Use the skill only when ClawCap's privacy and retention practices meet the deployment requirements, and avoid confidential prompts if those practices are not acceptable. <br>
Risk: The setup script modifies ~/.openclaw/openclaw.json provider baseUrl values. <br>
Mitigation: Review the changed configuration after setup and keep the generated backup or uninstall script available to restore the prior provider URLs. <br>
Risk: The ClawCap proxy token is required for setup and ongoing routing. <br>
Mitigation: Store CLAWCAP_TOKEN as a secret, use rotatable provider credentials, and rotate affected keys if a token or forwarding credential is exposed. <br>


## Reference(s): <br>
- [ClawCap Website](https://clawcap.co) <br>
- [ClawCap Setup Page](https://clawcap.co/setup) <br>
- [ClawHub Skill Page](https://clawhub.ai/Kintupercy/clawcap) <br>
- [Publisher Profile](https://clawhub.ai/user/Kintupercy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node.js setup and uninstall scripts to update or restore OpenClaw provider configuration.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
