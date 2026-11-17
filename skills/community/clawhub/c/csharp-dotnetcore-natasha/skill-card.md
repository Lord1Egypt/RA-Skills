## Description:

This skill should be used when developers need to create dynamic C# features at runtime, including dynamic class generation, dynamic method creation, accessing private members through dynamic compilation, and managing compilation metadata strategies using the Natasha library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmsazulxxiaohao](https://clawhub.ai/user/nmsazulxxiaohao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get implementation guidance, code examples, package setup commands, and troubleshooting patterns for runtime C# code generation with Natasha.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime C# compilation can execute high-impact generated code if examples are applied to untrusted input.

Mitigation: Use this guidance only with trusted code or add isolation such as a least-privileged process or container, strict input validation, reviewed package versions, and explicit filesystem and network limits.

Risk: Private-member access examples can bypass intended encapsulation and increase exposure of internal application state.

Mitigation: Limit private-member access to reviewed maintenance or test scenarios and require code review before using these patterns in production systems.

## Reference(s):

- [Natasha GitHub](https://github.com/dotnetcore/Natasha)
- [Natasha Official Documentation](https://natasha.dotnetcore.xyz/zh-Hans/docs)
- [DotNetCore.Natasha.CSharp.Compiler NuGet Package](https://www.nuget.org/packages/DotNetCore.Natasha.CSharp.Compiler)
- [DotNetCore.Natasha.CSharp.Compiler.Domain NuGet Package](https://www.nuget.org/packages/DotNetCore.Natasha.CSharp.Compiler.Domain)
- [initialization-patterns.md](references/initialization-patterns.md)
- [context-management.md](references/context-management.md)
- [compiler-options.md](references/compiler-options.md)
- [migration-guide.md](references/migration-guide.md)
- [common-patterns.md](references/common-patterns.md)
- [troubleshooting.md](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline C# and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides documentation-oriented guidance for NuGet setup, Natasha initialization, compilation modes, private-member access, error handling, and optimization patterns.]

## Skill Version(s):

3.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
