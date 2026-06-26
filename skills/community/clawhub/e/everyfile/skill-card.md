## Description: <br>
Fast file and folder search on Windows via Voidtools Everything for finding, listing, and counting files or folders by name, path, extension, size, date, or duplicates through the ev CLI and Python API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louisgamedev](https://clawhub.ai/user/louisgamedev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill on Windows to locate, count, and inspect files or folders quickly through Voidtools Everything. It is useful for broad file discovery, duplicate checks, size/date filtering, and scripting search results with the CLI or Python API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Windows file searches can expose sensitive local file paths or filenames. <br>
Mitigation: Use counts and result limits before broad searches, and require explicit authorization before collecting, exporting, or sharing results from sensitive queries such as .env, key, token, content, or full-path searches. <br>
Risk: Search results may be piped into commands that move, copy, delete, or otherwise modify files. <br>
Mitigation: Confirm with the user before using everyfile results in destructive or bulk file operations. <br>
Risk: The skill depends on trusted local installations of the everyfile PyPI package and Voidtools Everything. <br>
Mitigation: Install only from trusted sources and verify that Everything is installed and running before relying on search results. <br>


## Reference(s): <br>
- [everyfile ClawHub release](https://clawhub.ai/louisgamedev/everyfile) <br>
- [Voidtools Everything](https://www.voidtools.com/) <br>
- [CLI Reference](references/cli.md) <br>
- [Python API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline PowerShell and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local file paths, counts, NDJSON, JSON, or one-path-per-line command output depending on the selected everyfile interface.] <br>

## Skill Version(s): <br>
2026.4.22 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
