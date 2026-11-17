## Description:

Applies a C++/CPP code style guide based on Google C++ style conventions before writing or revising C++ code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiali](https://clawhub.ai/user/daxiali)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to keep C++ source, headers, comments, namespaces, includes, CMake files, and formatting aligned with the stated Google-style conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause agents to apply style rules that conflict with an existing repository's own C++ conventions.

Mitigation: Override this skill when a repository has its own style rules, especially around comment language or formatting changes.

Risk: Formatting or code-style proposals can introduce misleading or unwanted changes if accepted without review.

Mitigation: Review proposed edits and run the repository's normal formatting, linting, and test checks before deployment.

## Reference(s):

- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [A C++ Guide](https://www.google-styleguide.com/)
- [ClawHub skill page](https://clawhub.ai/daxiali/skills/cpp-code-style)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline C++, shell, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose style-aligned edits, clang-format usage, and .clang-format configuration checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
