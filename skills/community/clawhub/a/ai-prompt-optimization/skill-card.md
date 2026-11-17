## Description:

Use when users need to optimize prompts for AI conversations, generate structured templates, create few-shot examples, design chain-of-thought guidance, or diagnose and improve existing prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to improve prompts, generate reusable prompt templates, create few-shot examples, and structure prompt-writing guidance for AI tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt improvements could be applied to sensitive, harmful, evasive, or policy-bypassing requests.

Mitigation: Review generated prompts before use, especially in sensitive domains, and do not use the skill to optimize harmful or evasive requests.

Risk: Chain-of-thought prompt patterns may request full hidden reasoning where a concise reasoning summary would be more appropriate.

Mitigation: Revise chain-of-thought outputs to ask for concise reasoning summaries and final answers rather than hidden reasoning traces.

## Reference(s):

- [Prompt Template Reference](references/templates.md)
- [ClawHub Skill Page](https://clawhub.ai/openlark/skills/ai-prompt-optimization)
- [Publisher Profile](https://clawhub.ai/user/openlark)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with prompt templates, checklists, examples, and rationale.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable prompt revisions and templates; generated prompts should be reviewed before sensitive use.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
