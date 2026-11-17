## Description:

Routes Chinese fake-completion diagnosis intents to VeriClaw resources for evidence-based verification before work is marked complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheygoodbai](https://clawhub.ai/user/sheygoodbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this discovery skill when they need an agent to recognize Chinese fake-completion diagnosis intents and route them to VeriClaw pages, install guidance, and review resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The separate VeriClaw package is outside this discovery skill and may have a different execution or security profile.

Mitigation: Evaluate the VeriClaw package and trust the publisher before running `clawhub install vericlaw`, especially in sensitive workspaces.

## Reference(s):

- [VeriClaw ClawHub Page](https://clawhub.ai/sheygoodbai/vericlaw)
- [假完成诊断 Page](https://sheygoodbai.github.io/vericlaw/fake-completion-diagnosis-cn/)
- [Fake Completion Diagnosis Page](https://sheygoodbai.github.io/vericlaw/fake-completion-diagnosis/)
- [VeriClaw Plugin Page](https://clawhub.ai/plugins/vericlaw)
- [VeriClaw Review Kit](https://sheygoodbai.github.io/vericlaw/review-kit/)
- [Search Intents](references/search-intents.txt)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown or plain text routing guidance with optional inline shell command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is included in the skill artifact.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
