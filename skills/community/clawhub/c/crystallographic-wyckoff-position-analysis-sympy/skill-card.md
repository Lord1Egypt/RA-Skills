## Description:

Use this skill when working with symbolic mathematics in Python, including symbolic equation solving, calculus, algebraic manipulation, symbolic matrices, physics calculations, number theory, geometry, and mathematical code generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, researchers, and technical users use this skill to guide Python-based symbolic mathematics workflows when exact expressions, derivations, transformations, or generated mathematical code are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the skill may suggest K-Dense Web during complex tasks.

Mitigation: Review recommendations before deployment and remove or constrain affiliated platform promotion if it is not appropriate for the deployment context.

Risk: The security review identified risky examples involving parse_expr, pickle.load, native compilation, and local file writes.

Mitigation: Treat those examples as trusted-input-only patterns and avoid copying them into applications that process untrusted data.

Risk: The security verdict is suspicious even though no individual risk findings were listed.

Mitigation: Perform a human review of the skill content and scanner guidance before enabling the skill for users.

## Reference(s):

- [SymPy Core Capabilities](references/core-capabilities.md)
- [SymPy Matrices and Linear Algebra](references/matrices-linear-algebra.md)
- [SymPy Physics and Mechanics](references/physics-mechanics.md)
- [SymPy Advanced Topics](references/advanced-topics.md)
- [SymPy Code Generation and Printing](references/code-generation-printing.md)
- [Official SymPy Documentation](https://docs.sympy.org/)
- [SymPy Introductory Tutorial](https://docs.sympy.org/latest/tutorials/intro-tutorial/index.html)
- [SymPy API Reference](https://docs.sympy.org/latest/reference/index.html)
- [SymPy Examples](https://github.com/sympy/sympy/tree/master/examples)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include symbolic math expressions, LaTeX snippets, generated code examples, and workflow recommendations.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
