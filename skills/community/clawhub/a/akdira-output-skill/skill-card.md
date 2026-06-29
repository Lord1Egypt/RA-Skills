## Description: <br>
Overrides default LLM truncation behavior, enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akdira](https://clawhub.ai/user/akdira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a task requires exhaustive, unabridged output such as complete files, full code implementations, or multi-part deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's broad trigger can encourage longer responses even when concise handling or tighter scoping would be safer. <br>
Mitigation: Use it only when complete output is explicitly valuable, and avoid applying it to sensitive, restricted, or high-risk requests where careful scoping matters more than completeness. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with complete code blocks or structured text as requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes complete deliverables, explicit pause points for long responses, and avoidance of placeholder or truncated output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
