## Description:

Create a ritual-rich Chinese Asakusa Temple omikuji experience that directly reveals one real lot from the bundled 1-100 fortune set, with no question intake or personalized analysis, and gently offers a single 纳签重请 ritual when the lot is unfavorable so the old slip can be symbolically destroyed and a new course invited.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaozrrr](https://clawhub.ai/user/shaozrrr)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to draw a Chinese Asakusa Temple omikuji lot, receive the poem and interpretation in restrained ceremonial prose, and optionally perform one symbolic redraw when the initial lot is unfavorable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required helper script downloads and executes mutable remote Python code at runtime.

Mitigation: Bundle the fortune data and draw logic locally, or pin and verify remote resources before execution.

Risk: Users may assume the skill is fully local because it is presented as a local fortune-drawing ritual.

Mitigation: Disclose the runtime network dependency and review the remote code source before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaozrrr/skills/asakusa-omikuji-skill)
- [Publisher profile](https://clawhub.ai/user/shaozrrr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language ritual-style fortune output; omikuji results are produced through a Python helper.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
