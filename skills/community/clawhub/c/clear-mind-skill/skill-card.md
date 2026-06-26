## Description: <br>
Memory file maintenance and optimization system that helps an agent migrate scenario-specific factual content out of MEMORY.md while preserving core rules, capabilities, indexes, and rollback paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webray1983](https://clawhub.ai/user/webray1983) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to reorganize long-term MEMORY.md content by keeping durable rules and navigation in place while moving scenario-specific facts into dedicated facts/ files. It is intended for memory cleanup when factual bloat is present, not as a line-count reduction tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory cleanup can move or delete personal, financial, project, preference, or other important notes. <br>
Mitigation: Ask for a proposed diff or dry run, keep a backup, and require explicit user approval before any deletion or migration. <br>
Risk: Incorrect classification can remove core behavioral rules, capabilities, tool descriptions, or installed-skill information from MEMORY.md. <br>
Mitigation: Preserve core rules and capability definitions in MEMORY.md, keep content there when uncertain, and verify the Quick Index and facts/ files after migration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown guidance and proposed memory-file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose creating or updating MEMORY.md and memory/facts/ files after user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
