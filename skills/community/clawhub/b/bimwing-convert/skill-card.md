## Description:

BIMWing 三维模型在线浏览 uploads local BIM, CAD, and 3D model files to BIMWing for online lightweight conversion, then returns browser-viewable share links and can list models, check conversion status, or create links for existing models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolboy-never-die](https://clawhub.ai/user/coolboy-never-die)

### License/Terms of Use:

MIT-0

## Use Case:

Architects, BIM coordinators, and developers use this skill to convert supported local model or drawing files into BIMWing browser viewing links. They can also ask an agent to check conversion status, list account models, or create a share link for an existing BIMWing model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BIMWing account passwords may be stored in plaintext, and the packaged evidence did not prove the claimed gitignore safeguard for config.local.json.

Mitigation: Prefer BIMWING_MOBILE and BIMWING_PASSWORD environment variables, avoid persistent credential storage on shared machines, and verify or add a .gitignore entry before saving credentials locally.

Risk: Selected model files are uploaded to BIMWing and share links are created there.

Mitigation: Upload only files intended for BIMWing processing and review the resulting share link before distributing it.

Risk: Account-level operations such as listing models can expose BIMWing model metadata from the signed-in account.

Mitigation: Run account-wide list, status, or share operations only after an explicit user request and show only the relevant results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coolboy-never-die/skills/bimwing-convert)
- [BIMWing Web App](https://bimwing.letsgrp.com)
- [BIMWing Sign In and Registration](https://bimwing.letsgrp.com/sign-in)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with command examples, configuration guidance, generated share URLs, and optional local HTML open pages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated network calls to BIMWing and may create local configuration or helper files when the user explicitly authorizes the workflow.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
