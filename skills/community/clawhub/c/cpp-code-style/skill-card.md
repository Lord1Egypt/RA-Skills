## Description: <br>
C++/CPP代码都用这个coding style, code style, 代码风格，写代码之前阅读下面规则. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiali](https://clawhub.ai/user/daxiali) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to apply a Google-style C++/CPP coding convention before creating, reviewing, or formatting C++ code. It covers naming, indentation, braces, whitespace, header guards, namespaces, comments, include order, CMake practices, and clang-format usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Style guidance may lead to broad formatting changes, including .clang-format edits or files modified with clang-format -i. <br>
Mitigation: Review diffs before accepting changes and scope formatting commands to intended files. <br>
Risk: The English-comment rule may conflict with explicit project or user language conventions. <br>
Mitigation: Let project-level or user-provided conventions override this default when they are explicit. <br>


## Reference(s): <br>
- [C++/CPP Code Style release page](https://clawhub.ai/daxiali/cpp-code-style) <br>
- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html) <br>
- [A C++ Guide](https://www.google-styleguide.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with C++ and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide edits to .clang-format and formatting commands; excludes external, 3rdparty, and .gitignore paths from the style rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
