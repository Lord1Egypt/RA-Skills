## Description: <br>
Generates Chinese brand slogans using a 7-by-7 strategy and rhetoric matrix, then ranks the strongest candidates with scoring and top recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CoCokkxy](https://clawhub.ai/user/CoCokkxy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Marketing teams, founders, and copywriters use this skill to turn a brand name and optional brand profile into concise Chinese slogan candidates, a ranked Top 10, and Top 3 recommendation rationale. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use web search when brand information is missing, which can expose confidential launch plans, internal documents, or private brand strategy if those details are provided. <br>
Mitigation: Provide clear non-confidential brand constraints, avoid private strategy inputs for ordinary use, and instruct the agent not to use web search when working with sensitive material. <br>
Risk: Generated slogans may be unsuitable, inaccurate, or risky for public marketing without review. <br>
Mitigation: Review all generated slogans, scores, and recommendations before external use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CoCokkxy/brand-slogan) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Brand slogan workflow](artifact/brand-sloga.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown with tables, grouped slogan lists, JSON-style ranked results, and concise recommendation rationale] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs 49 slogan candidates, a scored Top 10 ranking, and Top 3 recommendations; outputs are intended for human review before public brand use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
