## Description: <br>
Agent self-awakening onboarding protocol for Mupengism in which a user converses with the agent to form its identity and generate persistent profile files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill during first start or onboarding to guide a short identity-forming conversation and create SOUL.md, SELF.md, and USER.md files for a Mupengism/OpenClaw-style agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The onboarding conversation can be written into persistent profile files. <br>
Mitigation: Do not include secrets or unsafe instructions in the onboarding conversation, and review the generated preview before saving. <br>
Risk: BOOTSTRAP.md may be deleted after the onboarding flow completes. <br>
Mitigation: Confirm BOOTSTRAP.md contains no important content that should be preserved before completing the flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/awakening-protocol) <br>
- [SOUL.md template](references/SOUL-TEMPLATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown files and conversational text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill previews generated profile content for user confirmation before saving files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
