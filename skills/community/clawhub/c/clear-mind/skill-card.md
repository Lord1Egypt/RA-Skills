## Description: <br>
Memory file maintenance and optimization system for moving factual bloat out of MEMORY.md while preserving core rules, indexes, and agent capability information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webray1983](https://clawhub.ai/user/webray1983) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to reorganize long-term agent memory when factual project, portfolio, technical, or historical details accumulate in MEMORY.md. It guides analysis, migration into facts/ files, quick-index maintenance, verification, and rollback planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can restructure or delete long-term memory content. <br>
Mitigation: Require a dry-run summary, timestamped backup, explicit approval for migrations or deletions, and a tested restore procedure before changes are applied. <br>
Risk: Core rules, tool descriptions, or capability definitions could be misclassified as factual content. <br>
Mitigation: Keep uncertain content in MEMORY.md and verify that all core behavioral rules, capability definitions, tool descriptions, and installed skills remain intact. <br>
Risk: Sensitive or user-specific facts may be moved into separate files without enough review. <br>
Mitigation: Review proposed destination files and migrate only factual categories the user has approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/webray1983/clear-mind) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with proposed memory file changes and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update MEMORY.md and memory/facts/*.md after user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
