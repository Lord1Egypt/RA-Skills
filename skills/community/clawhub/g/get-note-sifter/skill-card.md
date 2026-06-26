## Description: <br>
Analyzes Get notes and external links against a research map, then recommends what to keep, discard, or organize in Obsidian. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duzhilei951](https://clawhub.ai/user/duzhilei951) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Knowledge workers and researchers use this skill to triage Get notes or article links against an existing research map, detect overlap with Obsidian notes, and decide whether to save, discard, or convert content into wiki-style notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read the configured Obsidian research vault. <br>
Mitigation: Install only if that vault access is acceptable, and start with read-only analysis. <br>
Risk: The skill can propose creating notes, editing index.md, or enabling scheduled scans. <br>
Mitigation: Require a preview and explicit approval before any vault write or scheduled scan is enabled. <br>
Risk: The workflow depends on the vaultctl npm package for vault access. <br>
Mitigation: Verify the vaultctl package before installation and configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/duzhilei951/get-note-sifter) <br>
- [Research Map](artifact/memory/research-map.md) <br>
- [Research Map JSON](artifact/memory/research-map.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with optional Obsidian wiki-note templates and vaultctl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose read or write actions for an Obsidian vault; require preview and explicit approval before writes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
