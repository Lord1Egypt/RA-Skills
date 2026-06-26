## Description: <br>
Contactor and starter selection tool. Use when json contactor tasks, csv contactor tasks, checking contactor status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to run a local shell utility for adding, listing, searching, exporting, and configuring contactor-related entries. It should be treated as a local note and configuration logger rather than as an authoritative contactor or starter status checker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be mistaken for an authoritative contactor or starter selection and status checker. <br>
Mitigation: Use it only as a local note and configuration logger, and verify any electrical equipment decisions through qualified engineering sources. <br>
Risk: Entries and configuration values are stored locally and may include operational identifiers. <br>
Mitigation: Review CONTACTOR_DIR before use and avoid entering sensitive identifiers unless local storage is acceptable. <br>
Risk: Remove, export, and config commands modify or copy local files. <br>
Mitigation: Review the target data directory and command arguments before running destructive or exporting operations. <br>


## Reference(s): <br>
- [Contactor on ClawHub](https://clawhub.ai/xueyetianya/contactor) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Command-line text output, JSONL data, CSV export, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local data under CONTACTOR_DIR, defaulting to ~/.contactor/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
