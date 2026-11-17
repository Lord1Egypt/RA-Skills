## Description:

Overrides default LLM truncation behavior, enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly for tasks requiring exhaustive, unabridged output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akdira](https://clawhub.ai/user/akdira)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill when a task requires complete, unabridged deliverables such as full files, full implementations, or exhaustive multi-part answers. It guides the agent to scope requested deliverables, avoid placeholder shortcuts, and pause at clean continuation points when responses approach token limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce longer answers than desired for workflows that require concise responses.

Mitigation: Use it for tasks that require complete, unabridged deliverables and avoid enabling it for strict-brevity workflows.

Risk: The skill may conflict with workflows that require fixed output protocols.

Mitigation: Confirm that the required output protocol allows complete responses and clean continuation markers before using the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, code blocks, shell commands, configuration snippets, or other user-requested response formats without intentional omissions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce longer responses and uses clean continuation breakpoints when a response approaches token limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
