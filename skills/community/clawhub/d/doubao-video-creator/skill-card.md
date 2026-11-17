## Description:

Assists agents with requirements collection, scene planning, cinematic prompt generation, and per-scene Doubao Seedance video creation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and agent operators use this skill to plan short promotional or social videos, confirm scene prompts, call Doubao Seedance text-to-video or image-to-video generation, and assemble scene outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes hardcoded credentials and examples of plaintext API key storage.

Mitigation: Do not use bundled credentials; rotate any matching keys and store user-provided credentials only through a secure secret mechanism.

Risk: Publishing helper files can push code to fixed GitHub or ClawHub destinations and include unsafe publishing guidance.

Mitigation: Remove or disable quick-publish helpers before installation and review all repository or marketplace publishing commands before execution.

Risk: The server security verdict is suspicious.

Mitigation: Review and scan the release before deployment, with particular attention to credential handling and publishing scripts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cindypapa/skills/doubao-video-creator)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [QUICK_REFERENCE.md](artifact/QUICK_REFERENCE.md)
- [BEST_PRACTICES.md](artifact/BEST_PRACTICES.md)
- [TECH_SPECS_GUIDE.md](artifact/TECH_SPECS_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompts, configuration examples, Python snippets, shell commands, and generated video task metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-scene prompts and task guidance; generated media depends on external video and image APIs.]

## Skill Version(s):

3.0.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
