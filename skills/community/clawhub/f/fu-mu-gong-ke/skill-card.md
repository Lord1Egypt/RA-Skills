## Description:

Fu Mu Gong Ke provides parenting psychology dialogue support with structured responses, emotion recognition, scenario matching, safety checks, and optional local Python helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

External users, parents, adult children, and helpers use this skill for parenting psychology support, parent-child communication guidance, emotional triage, and crisis-aware redirection. Agents use it to produce compassionate responses, scenario-based guidance, reflective prompts, and optional local assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive parenting, child, family, or emotional-health details may be stored locally by optional helper scripts.

Mitigation: Review the helper behavior before use, avoid identifiable crisis or family details, disclose local retention to users, and delete SKILL_DIR/data when records are no longer needed.

Risk: Users may treat parenting psychology guidance as professional mental-health advice during high-risk situations.

Mitigation: Keep the skill's disclaimer visible, route self-harm, abuse, or emergency signals to professional or emergency support, and avoid diagnosis, treatment claims, or medication guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/fu-mu-gong-ke)
- [Quick Start](artifact/QUICK-START.md)
- [Crisis Intervention Protocol](artifact/theory/crisis-intervention.md)
- [Runnable Tools](artifact/tools/runnable-tools.md)
- [Research Data](artifact/references/research_data.md)
- [Theory Modules](artifact/references/theory_modules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional plaintext or JSON outputs from Python helpers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional Python helpers may write local plaintext or JSON records under SKILL_DIR/data when enabled or used.]

## Skill Version(s):

2.4.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
