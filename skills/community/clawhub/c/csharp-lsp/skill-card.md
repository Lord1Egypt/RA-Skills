## Description: <br>
C# language server providing code intelligence, diagnostics, and navigation for .cs and .csx files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leafbird](https://clawhub.ai/user/leafbird) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering agents use this skill to inspect C# projects with language-server features such as hover, go-to-definition, references, symbols, and diagnostics. It is intended for projects with a .sln or .csproj workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installer and helper scripts can use sudo and modify persistent shell or system paths. <br>
Mitigation: Review setup before installing, run it manually, avoid setting SUDO_PASS, and prefer a user-writable link such as ~/.local/bin/lsp-query. <br>
Risk: Language-server queries and debug logs can expose local project metadata. <br>
Mitigation: Keep LSP_WORKSPACE limited to the intended project and remove or restrict /tmp/lsp-query-debug.log if it is created. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leafbird/csharp-lsp) <br>
- [csharp-ls language server](https://github.com/razzmatazz/csharp-language-server) <br>
- [.NET SDK downloads](https://dot.net/download) <br>
- [Language Server Protocol specification](https://microsoft.github.io/language-server-protocol/) <br>
- [Architecture](docs/architecture.md) <br>
- [Troubleshooting](docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output with setup and usage snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires .NET SDK, Python 3, and a C# workspace with a .sln or .csproj for full results.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, release metadata, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
