## Description:

Generates rewritten C++ competitive-programming problem statements, testlib-based validators, generators, and complete test data from an original problem and standard solution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirwym](https://clawhub.ai/user/sirwym)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and competitive-programming problem setters use this skill to turn an existing problem and C++ standard solution into a new contest-style problem package with generated tests, validation code, and packaged outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run third-party Docker code and generated C++ against a broadly mounted workspace.

Mitigation: Run it only in a clean dedicated workspace with no secrets, verify or rebuild the Docker image where possible, and avoid mounting unrelated project files.

Risk: Generated problem, validator, generator, and shell-command content can be incorrect or unsafe if accepted without review.

Mitigation: Review generated files and commands before execution, keep validators strict, and scan the resulting package before deployment.

Risk: The server security verdict is suspicious due to unverified Docker execution and untrusted C++ behavior.

Mitigation: Prefer additional Docker isolation such as no network access, a non-root user, read-only inputs, and a separate writable output directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sirwym/skills/cpp-problem-generator)
- [testlib manual](references/testlib-manual.md)
- [background catalog](references/backgrounds.md)
- [generation pipeline script](scripts/generate.py)
- [Docker sandbox release page referenced by the skill](https://github.com/sirwym/cpp-problem-generator/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with C++ source files, shell commands, generated test data, ZIP packaging, and metadata files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces contest assets such as problem.md, gen.cpp, valid.cpp, std.cpp-derived outputs, test data, meta.json, and a packaged archive when the Docker workflow succeeds.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
