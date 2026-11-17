## Description: <br>
代码解释工具免费版 helps developers understand unfamiliar single-file code by producing analogies, ASCII diagrams, line-by-line walkthroughs, and common pitfall notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to understand unfamiliar code, support onboarding, assist code review comprehension, and learn programming concepts through analogies, ASCII diagrams, and guided walkthroughs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports a suspicious posture because the skill requests broad command execution and file-write authority that is not clearly needed for code explanation. <br>
Mitigation: Install and run it only in a limited workspace, review commands before execution, and avoid granting access to files beyond the code being explained. <br>
Risk: Code provided for explanation may include sensitive or proprietary content that the agent LLM processes. <br>
Mitigation: Avoid using the skill on sensitive proprietary code unless the agent environment and LLM data handling are approved for that code. <br>


## Reference(s): <br>
- [Detailed examples](artifact/references/detail.md) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/explain-code-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with ASCII diagrams, inline code blocks, and concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include summaries, analogies, execution-flow diagrams, line-by-line explanations, configuration examples, and common pitfall notes; the free edition focuses on single-file code explanation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
