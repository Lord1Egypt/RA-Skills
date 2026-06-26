## Description: <br>
Score marketing copy for resonance, hook strength, NLP technique usage, and conversion readiness. Returns a 0-100 Content Resonance Score with per-dimension breakdown and actionable rewrite suggestions. Calibrated against fMRI brain-response data (TRIBE v2). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, sales, and content teams use this skill to evaluate copy before publishing, compare hooks, check forbidden terms, and request targeted rewrites. Agent workflows can use its JSON mode to score copy programmatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal scoring, rewriting, or comparison can send submitted marketing copy to Anthropic when the local backend is unavailable. <br>
Mitigation: Use --demo or --compliance-only for no external call, or set LLM_BACKEND=local when local-only processing is required. <br>


## Reference(s): <br>
- [Content Scorer ClawHub Page](https://clawhub.ai/drivenautoplex1/content-scorer) <br>
- [Project Homepage](https://github.com/drivenautoplex1/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Human-readable score report or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include per-dimension scores, compliance findings, hook comparisons, and rewrite suggestions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
