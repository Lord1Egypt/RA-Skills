## Description:

Cognitive Loop implements a high-autonomy think-act-reflect-test execution loop for task planning, multi-step execution, error recovery, and test verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[world-peace001](https://clawhub.ai/user/world-peace001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure complex agent work into planning, monitored execution, reflection, and testing loops. It is intended for multi-step development tasks, refactoring, recovery from errors, and test-driven validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external package whose reviewed commit or package version is not pinned in the artifact.

Mitigation: Review the cognitive-agent source and npm package before installation, and prefer a pinned version or reviewed commit.

Risk: The skill describes a high-autonomy planning and execution loop that may propose complex changes.

Mitigation: Require explicit user confirmation for complex operations and run first use in a sandbox.

Risk: The skill can persist experience and knowledge under documented memory directories.

Mitigation: Limit persistent writes to the documented memory/ subdirectories and avoid storing secrets or sensitive task context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/world-peace001/skills/cognitive-loop)
- [cognitive-agent npm package](https://www.npmjs.com/package/cognitive-agent)
- [cognitive-agent GitHub project](https://github.com/World-peace001/cognitive-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe persistent memory paths under memory/ and recommends sandboxed first use.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
