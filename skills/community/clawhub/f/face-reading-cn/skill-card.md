## Description: <br>
Provides entertainment-oriented Chinese traditional face-reading, image-based facial feature analysis, mole interpretation, and psychology-oriented self-reflection guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmilton09](https://clawhub.ai/user/gmilton09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer face-reading questions, generate entertainment-oriented reports from facial features or image inputs, and look up traditional Chinese physiognomy concepts. Use should be limited to consensual, non-decisional cultural learning, entertainment, and self-reflection contexts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage analysis of other people's faces or photos without clear consent. <br>
Mitigation: Use only with explicit consent from the person being analyzed, and avoid analyzing private faces or public image URLs for people who have not agreed. <br>
Risk: Face-reading, personality, fortune, health, and mental-health claims can be misleading or discriminatory if treated as factual. <br>
Mitigation: Present outputs as entertainment and cultural learning only, and do not use them for medical, psychological, employment, financial, relationship, or other important decisions. <br>
Risk: Image-analysis workflows may expose sensitive face data when users provide public URLs or third-party image-analysis tools. <br>
Mitigation: Prefer local processing when possible, avoid uploading private face images, and review the image-analysis path before deployment. <br>
Risk: Social-guide content may normalize covert observation in real interactions. <br>
Mitigation: Review or remove social-interaction guidance that supports covert analysis before using the skill in production or interpersonal settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gmilton09/face-reading-cn) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Release changelog](artifact/CHANGELOG.md) <br>
- [Face-reading basics](artifact/README.md) <br>
- [Balance analysis guide](artifact/BALANCE-ANALYSIS.md) <br>
- [Psychology mapping guide](artifact/PSYCHOLOGY-MAPPING.md) <br>
- [Self-acceptance guide](artifact/SELF-ACCEPTANCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or terminal text reports, with optional JSON report output from local scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May accept text feature queries, image URLs, or local image paths depending on script; face-image handling should be consensual.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
