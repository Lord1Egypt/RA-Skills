## Description: <br>
This skill helps developers create dynamic C# features at runtime with the Natasha library, including dynamic class generation, delegate generation, private member access, and compilation metadata management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nmsazulxxiaohao](https://clawhub.ai/user/nmsazulxxiaohao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building .NET applications that need runtime C# compilation, dynamic types, generated delegates, controlled load contexts, or Natasha migration and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dynamic compilation examples can execute arbitrary C# code when applied to untrusted inputs. <br>
Mitigation: Use the skill only with controlled code provenance, and isolate execution in a separate low-privilege process or container for any higher-risk workflow. <br>
Risk: Private-member access examples can bypass normal encapsulation boundaries. <br>
Mitigation: Avoid applying private-member access patterns to third-party objects, secrets, shared writable paths, or multi-tenant production paths unless isolation and review controls are in place. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nmsazulxxiaohao/csharp-dotnetcore-natasha) <br>
- [Natasha Official Documentation](https://natasha.dotnetcore.xyz/zh-Hans/docs) <br>
- [DotNetCore.Natasha.CSharp.Compiler NuGet Package](https://www.nuget.org/packages/DotNetCore.Natasha.CSharp.Compiler) <br>
- [DotNetCore.Natasha.CSharp.Compiler.Domain NuGet Package](https://www.nuget.org/packages/DotNetCore.Natasha.CSharp.Compiler.Domain) <br>
- [Initialization Patterns](references/initialization-patterns.md) <br>
- [Context Management](references/context-management.md) <br>
- [Compiler Options](references/compiler-options.md) <br>
- [Migration Guide](references/migration-guide.md) <br>
- [Common Patterns](references/common-patterns.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with C# and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
3.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
