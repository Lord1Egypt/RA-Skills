## Description: <br>
Optimizes, improves, benchmarks, and evaluates skill prompts by running automated prompt experiments using the Karpathy autoresearch pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zning1994](https://clawhub.ai/user/zning1994) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to define binary evals, run prompt optimization experiments against a target SKILL.md or similar prompt file, and review the winning prompt variant before applying it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt content, eval cases, and generated outputs may be sent to the selected LLM provider. <br>
Mitigation: Run only with data that may be shared with that provider, avoid secrets in prompts and evals, and choose the provider API key deliberately. <br>
Risk: The optimizer modifies the target prompt file while testing variants. <br>
Mitigation: Run on a copy or in version control, use the generated baseline backup, and review the final prompt diff before committing. <br>
Risk: Verbose runs may expose prompt or model-response details in shared terminals or CI logs. <br>
Mitigation: Avoid --verbose in shared environments and keep result artifacts out of public logs when prompts or evals contain sensitive material. <br>
Risk: Repeated LLM experiments can consume paid API quota. <br>
Mitigation: Set conservative --runs and --max-experiments values, monitor provider usage, and stop runs that are not improving. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zning1994/brainforge-autoresearch) <br>
- [Project homepage](https://github.com/zning1994/brainforge-autoresearch) <br>
- [Karpathy autoresearch pattern](https://github.com/karpathy/autoresearch) <br>
- [Claude Code autoresearch adaptation](https://github.com/olelehmann100kMRR/autoresearch-skill) <br>
- [Eval guide](artifact/eval-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When executed, the optimizer can write local result files, a dashboard, and a baseline backup, and it can update the target prompt file.] <br>

## Skill Version(s): <br>
0.2.5 (source: frontmatter, changelog, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
