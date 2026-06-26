## Description: <br>
Audits agent skill quality against Anthropic skill guidance, checking structure, YAML frontmatter, description quality, instruction completeness, examples, and improvement opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xzxiaoshan](https://clawhub.ai/user/xzxiaoshan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, skill authors, and reviewers use this skill to audit agent skill folders or SKILL.md content before publishing or sharing. It produces structured quality findings, scores, and improvement recommendations based on Anthropic skill development guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional third-party install examples can run external package code if copied without review. <br>
Mitigation: Run optional npx install examples only when the source is trusted and the user explicitly intends to install that separate skill. <br>
Risk: Skill reviews can produce incorrect or incomplete quality guidance if the wrong SKILL.md or folder is supplied. <br>
Mitigation: Provide only the specific skill file or folder intended for review, and verify the generated findings before applying changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xzxiaoshan/agent-skill-reviewer) <br>
- [Publisher Profile](https://clawhub.ai/user/xzxiaoshan) <br>
- [Anthropic Skills Development Guide](references/anthropic-skills-development-guide.md) <br>
- [Skill Review Checklist](references/checklist.md) <br>
- [Official Guide Summary](references/official-guide-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with checklists, scores, findings, recommendations, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce quick audits or full review reports depending on the user's requested review depth.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
