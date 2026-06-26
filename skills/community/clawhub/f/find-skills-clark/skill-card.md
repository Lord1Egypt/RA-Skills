## Description: <br>
Helps agents discover, compare, and install skills when users ask for skill discovery or installation, with a Chinese-user workflow that prefers skillhub before ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clark516lian](https://clawhub.ai/user/clark516lian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need an agent to search available skill registries, present matching skill options with sources, and propose installation commands. It is especially tailored for Chinese users by checking skillhub before falling back to ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose installing third-party skills from skillhub or ClawHub. <br>
Mitigation: Before installation, review the registry source, exact skill name and version, and any risk signals, then approve the install command only if the source is trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clark516lian/find-skills-clark) <br>
- [Publisher Profile](https://clawhub.ai/user/clark516lian) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include skill names, registry source labels, install commands, version details, and risk signals for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
