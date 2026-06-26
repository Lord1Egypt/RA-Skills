## Description: <br>
智能分析用户需求并推荐最适合的ClawHub技能，提供实时技能搜索、安全评估和使用建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jxyyjm](https://clawhub.ai/user/jxyyjm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub users use this skill to analyze a natural-language capability request, compare candidate skills, and receive recommendation reports with installation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill overstates live search and safety-review capabilities while recommending other skills as safe. <br>
Mitigation: Treat recommendations as rough offline guidance, inspect any recommended skill before installation, and do not rely on its ratings as a real security review. <br>
Risk: API-key requirements are declared even though live API behavior is not clearly implemented in the artifact. <br>
Mitigation: Avoid providing API keys unless a future version clearly documents and implements live API use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jxyyjm/ai-capability-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/jxyyjm) <br>
- [Declared homepage](https://github.com/your-username/ai-capability-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown-like text with skill recommendations, comparisons, safety notes, and installation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are advisory recommendations from a local/offline helper and should not be treated as an independent security review.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
