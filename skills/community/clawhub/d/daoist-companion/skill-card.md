## Description: <br>
Daoist Companion is a beginner-focused Daoist study and practice notebook that explains classic texts, suggests practice routines, supports practice logs, and provides calendar reminders while avoiding ritual, divination, medical, and oral-transmission guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cucmeliu](https://clawhub.ai/user/cucmeliu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill for beginner Daoist study, practice planning, calendar lookups, and markdown-based practice journaling. It is intended as a knowledge guide and notebook, not as a master, ritual specialist, fortune-teller, or medical advisor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate from broad terms such as practice or meditation. <br>
Mitigation: Review triggers before installation and prefer manual loading when broad religious or meditation-related activation is not desired. <br>
Risk: The skill can run Bash and proposes installing an unpinned Python package for calendar calculations. <br>
Mitigation: Require confirmation before shell execution, disable automatic package installation in untrusted environments, and preinstall a reviewed calendar dependency when needed. <br>
Risk: The skill can write persistent practice journal files under the user's home directory. <br>
Mitigation: Confirm the destination path before writing, avoid storing sensitive personal information, and review generated journal content before persistence. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/cucmeliu/daoist-companion.git) <br>
- [ClawHub skill page](https://clawhub.ai/cucmeliu/daoist-companion) <br>
- [Classic texts library](references/classics.md) <br>
- [Practice system and FAQ](references/practice.md) <br>
- [Daoist cultural encyclopedia](references/culture.md) <br>
- [Daoist practice quick-reference index](references/daoist_knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prose with optional shell or Python snippets and markdown journal files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write practice logs under ~/daoist-journal and may use Python date calculations for lunar calendar guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
