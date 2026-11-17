## Description:

C# language server providing code intelligence, diagnostics, and navigation for .cs and .csx files. Uses csharp-ls (lightweight Roslyn-based). Requires .sln or .csproj.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leafbird](https://clawhub.ai/user/leafbird)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to give agents command-line C# code intelligence for projects with .sln or .csproj files, including hover, definition, references, diagnostics, and symbol search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script may install a global .NET tool, edit shell startup files, and create or replace /usr/local/bin/lsp-query.

Mitigation: Review the setup script before running it, avoid privileged or shared machines, and prefer a user-local bin path when possible.

Risk: SUDO_PASS can provide the installer with unattended sudo authority for creating the lsp-query symlink.

Mitigation: Do not set SUDO_PASS; create any privileged symlink manually after inspecting the target path.

Risk: LSP_SERVER and LSP_LANG can alter which local language-server subprocess handles queried files.

Mitigation: Keep these variables unset unless intentionally testing, and restrict them to trusted language-server commands.

Risk: Queried source files are opened and sent to local language-server subprocesses.

Mitigation: Use the skill only with trusted local language servers and workspaces whose contents may be processed by those subprocesses.

## Reference(s):

- [C# LSP ClawHub Page](https://clawhub.ai/leafbird/skills/csharp-lsp)
- [Publisher Profile](https://clawhub.ai/user/leafbird)
- [csharp-ls](https://github.com/razzmatazz/csharp-language-server)
- [.NET SDK Downloads](https://dot.net/download)
- [Language Server Protocol Specification](https://microsoft.github.io/language-server-protocol/)
- [Architecture](docs/architecture.md)
- [Deployment](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on local language-server results, workspace configuration, and queried source files.]

## Skill Version(s):

1.2.0 (source: frontmatter and changelog, released 2026-03-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
