## Description: <br>
Advertises Chinese lunar calendar reference material, but the bundled script currently outputs generic life-domain guidance rather than the listed calendar commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can run a local command-line reference helper for Chinese calendar topics. Reviewers should treat the output as generic reference text until the maintainer aligns the implementation with the advertised lunar calendar features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the skill does not provide the Chinese calendar features it advertises, which could mislead users relying on lunar conversion, solar terms, zodiac, festival, or auspicious-date guidance. <br>
Mitigation: Review outputs against authoritative calendar sources and require maintainer alignment before using the skill for calendar decisions. <br>
Risk: Release evidence, SKILL.md frontmatter, and the shell script report different versions. <br>
Mitigation: Confirm the intended release version and update artifact metadata before distribution or automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/chinese-calendar-cn) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Plain text and Markdown-style reference sections from a local Bash command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external API calls or credentials are declared; bundled behavior should be reviewed for mismatch with advertised calendar commands.] <br>

## Skill Version(s): <br>
5.0.1 (source: server release evidence; artifact frontmatter says 5.0.0 and script says 4.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
