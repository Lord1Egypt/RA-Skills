## Description:

Evaluates mathematical expressions with common functions and constants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can use this skill to evaluate arithmetic expressions and common math functions from a Python command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the helper can evaluate non-math Python expressions despite being presented as a safe math calculator.

Mitigation: Use only fully trusted expressions, or replace the evaluator with a strict AST-based math parser and add resource limits before accepting user-submitted or copied expressions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, code]

**Output Format:** [Markdown guidance with bash examples; the helper script emits JSON results or JSON errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies; accepts a single expression string through the --expr argument.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
