## Description:

Score marketing copy for resonance, hook strength, NLP technique usage, and conversion readiness, returning a 0-100 Content Resonance Score with per-dimension breakdown, actionable rewrite suggestions, and TRIBE v2 calibration context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales, and content teams use this skill to evaluate draft copy before publishing, with scores for hook strength, emotional resonance, NLP technique usage, specificity, CTA strength, and compliance. Agent workflows can also use its JSON mode for batch scoring, hook comparison, and rewrite suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal scoring can send pasted marketing copy to Anthropic when Haiku is selected or local backend auto-detection fails.

Mitigation: Use --demo or --compliance-only for no remote call, and set LLM_BACKEND=local for sensitive drafts.

Risk: The TRIBE v2/fMRI calibration claims are not verified by the provided provenance evidence.

Mitigation: Treat calibration claims as unverified unless the publisher provides the referenced calibration artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/drivenautoplex1/skills/content-scorer)
- [Publisher Profile](https://clawhub.ai/user/drivenautoplex1)
- [OpenClaw Skills Homepage](https://github.com/drivenautoplex1/openclaw-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Guidance]

**Output Format:** [Markdown or JSON scoring reports with optional rewritten copy and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local demo and compliance-only modes without remote calls; normal scoring can use a local LLM server or Anthropic Claude depending on backend settings.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
