## Description: <br>
表达层 routes user questions, source material, links, and drafts into content generation, format conversion, visualization, presentation, and WeChat publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to coordinate content-generation skills and publishing tools from a direct user request. It is suited for producing plain-language explanations, long-form articles, Markdown analyses, PNG cards, HTML presentations, and WeChat article drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route generated drafts toward a WeChat public-account publishing workflow without clearly documented approval and privacy guardrails. <br>
Mitigation: Require manual preview and explicit confirmation of destination, account, and visibility before any draft is pushed or published. <br>
Risk: Generated content may be routed through multiple dependent skills, which can obscure which component produced a specific artifact. <br>
Mitigation: Review the selected route and final artifacts before publication, especially when sequential or parallel routes are used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/expression-layer) <br>
- [Route orchestration matrix](references/orchestration-matrix.md) <br>
- [Investor education orchestration analysis](references/ie-orchestration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, text, HTML, PNG assets, and publishing workflow guidance depending on the selected route] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate single-step, sequential, parallel, or publishing routes through related skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
