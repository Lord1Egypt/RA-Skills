## Description: <br>
Apply a bounded multi-candidate self-refinement loop (A/B/AB + judges + do-nothing option) to improve drafts, plans, and analyses while preventing scope creep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cwheeler67](https://clawhub.ai/user/cwheeler67) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to refine writing, strategy memos, explanations, product copy, and decision frameworks through a bounded candidate-and-judge workflow that preserves intent and limits scope creep. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad request such as "improve this" may activate a refinement workflow when the user only wanted a small edit. <br>
Mitigation: Clarify success criteria when tone, audience, length, or goal are missing, and prefer no change when alternatives add mostly stylistic churn. <br>
Risk: Refined drafts may introduce inaccurate or misleading claims if candidates are optimized for style over faithfulness. <br>
Mitigation: Review outputs for factual accuracy, preserve required facts, and surface uncertainty when confidence drops. <br>
Risk: Drafts submitted for refinement may contain confidential content. <br>
Mitigation: Avoid sharing confidential drafts unless the user is comfortable with the platform handling that content. <br>


## Reference(s): <br>
- [Judge Rubric](references/judge-rubric.md) <br>
- [Autoreason Lite ClawHub Page](https://clawhub.ai/cwheeler67/autoreason-lite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a final refined result with 2-4 bullets summarizing key improvements and an optional convergence note.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
