## Description: <br>
Automatically improve OpenClaw skills, prompts, or articles through iterative mutation-testing loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt authors, and documentation maintainers use this skill to iteratively improve OpenClaw skills, prompts, and articles by proposing small mutations, scoring them against checklist criteria, and keeping improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite a selected local SKILL.md during Skill mode. <br>
Mitigation: Review resulting changes, diffs, and snapshots after each batch before deploying or publishing the optimized skill. <br>
Risk: Iterative mutations may introduce incorrect, misleading, or over-constrained guidance. <br>
Mitigation: Use the generated checklist and realistic test cases to compare behavior before and after each kept mutation. <br>
Risk: Running optimization on safety-critical skills or files containing secrets could propagate sensitive or high-impact content into outputs or snapshots. <br>
Mitigation: Avoid using the skill on safety-critical content or files containing secrets, as directed by the security guidance. <br>


## Reference(s): <br>
- [Mutation Strategies](references/mutation_strategies.md) <br>
- [Karpathy/autoresearch](https://github.com/karpathy/autoresearch) <br>
- [ClawHub Skill Page](https://clawhub.ai/0xcjl/autoresearch-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, improved text or SKILL.md content, diffs or inline final content, and optional shell command usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify a selected local SKILL.md in Skill mode and may create per-round snapshots when using the optional evaluation helper.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
