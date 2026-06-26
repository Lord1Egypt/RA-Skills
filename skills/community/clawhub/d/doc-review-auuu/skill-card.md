## Description: <br>
Reviews Feishu/Lark technical documents across literature research, solution planning, experiment design, and external-facing materials, then produces a structured review report and summary record. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tang-auuu](https://clawhub.ai/user/tang-auuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, reviewers, and technical teams use this skill to inspect Feishu/Lark documents for structure, evidence quality, experiment rigor, AI conversation links, and publication readiness. It is intended for workflows where the agent can read source documents, create review documents, and maintain a shared review summary table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu/Lark document read and write authority. <br>
Mitigation: Authorize it only in a workspace where the agent is allowed to read source documents and create or update review artifacts. <br>
Risk: Review reports and raw document links may be stored persistently in Feishu/Lark. <br>
Mitigation: Test in a non-sensitive workspace first and avoid confidential documents unless storing report content and links is acceptable. <br>
Risk: The workflow has limited confirmation controls before creating reports or updating the summary table. <br>
Mitigation: Verify destination folders, document permissions, and summary table access before running the skill on real materials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tang-auuu/doc-review-auuu) <br>
- [Publisher profile](https://clawhub.ai/user/tang-auuu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review reports, Markdown summary tables, and lark-cli command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Feishu/Lark report documents and update a persistent review summary table when credentials and lark-cli access are available.] <br>

## Skill Version(s): <br>
2.9.4 (source: release evidence, SKILL.md frontmatter, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
