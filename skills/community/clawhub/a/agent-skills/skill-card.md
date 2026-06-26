## Description: <br>
Agent Skills standard reference guide covering SKILL.md specification format, progressive disclosure, skill discovery and activation, frontmatter metadata fields, and directory structure conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill as a reference when creating, validating, evaluating, or integrating Agent Skills across supported agent products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied integration guidance could expose full local filesystem paths to a model or user. <br>
Mitigation: Avoid disclosing full local filesystem paths when adapting the guidance into an agent integration. <br>
Risk: Skill descriptions may trigger too broadly if adapted without testing. <br>
Mitigation: Test descriptions with near-miss negative cases before deployment so the skill activates only for appropriate tasks. <br>


## Reference(s): <br>
- [ClawHub Agent Skills release](https://clawhub.ai/openlark/agent-skills) <br>
- [Integration guide](references/integrate.md) <br>
- [Skill creation best practices](references/best-practices.md) <br>
- [Skill quality evaluation](references/eval-skills.md) <br>
- [Optimizing skill descriptions](references/optimize-desc.md) <br>
- [Bundling scripts in skills](references/using-scripts.md) <br>
- [Products supporting Agent Skills](references/products.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tables, examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; no executable code is bundled with this release.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
