## Description:

Searches Windows local files and folders with Everything SDK IPC or localhost HTTP JSON, returning full paths and helping locate Codex session JSONL logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssesweb](https://clawhub.ai/user/ssesweb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use this skill to locate Windows files, folders, and Codex session JSONL logs through Everything while returning complete paths for follow-up tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help locate sensitive Codex conversation logs.

Mitigation: Use narrow session, date, or keyword queries; extract only requested fields and do not echo tokens, cookies, keys, or other sensitive values.

Risk: The script can load user-selected native DLLs through --dll or EVERYTHING_SDK_DLL.

Mitigation: Use the bundled verified SDK payloads by default; only provide trusted, architecture-matched DLLs whose hashes and publisher are verified.

## Reference(s):

- [Everything SDK source archive](https://www.voidtools.com/Everything-SDK.zip)
- [ClawHub skill page](https://clawhub.ai/ssesweb/skills/everything-search-ipc)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text paths or JSON arrays, with Markdown guidance and shell commands when instructing the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-only; requires a running Everything background index and uses localhost HTTP fallback when configured.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
