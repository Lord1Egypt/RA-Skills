## Description: <br>
Turn 1–9 images into platform-specific captions and mood-matched music hints, then route to mock, dry-run, or real publishers with publish logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MiLab-Bit](https://clawhub.ai/user/MiLab-Bit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and social publishing operators use this skill to turn image sets and a theme into platform-specific publish-pack JSON with captions, hashtags, music hints, routing mode, and publish logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real publisher mode could post generated captions, tags, or platform settings before they are fully reviewed. <br>
Mitigation: Keep the skill in mock or dry-run mode until publisher adapters and account settings are reviewed, and require explicit human confirmation before real posting. <br>
Risk: Social publishing credentials could be exposed or granted broader access than needed. <br>
Mitigation: Store tokens in environment variables, avoid committing credentials, and use least-privilege platform API tokens. <br>
Risk: Generated captions, hashtags, or music hints may be misleading, policy-sensitive, or unsuitable for the target platform. <br>
Mitigation: Review each publish pack before posting and preserve the prompt constraints against medical or political claims and guaranteed virality. <br>


## Reference(s): <br>
- [Prompt Library](artifact/PROMPTS.md) <br>
- [Publish Pack Templates](artifact/TEMPLATES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Guidance] <br>
**Output Format:** [JSON files containing platform-specific captions, hashtags, music hints, routing choices, and publish-log results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports 1-9 input images, language and platform selection, optional mood/style hints, and mock, dry-run, or real publisher modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
