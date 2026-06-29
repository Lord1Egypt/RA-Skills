## Description: <br>
Advanced English polish skill for non-native writing, with nativization, style consistency, diff output, and CLI scripts for detection and polishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muchenhengxin](https://clawhub.ai/user/muchenhengxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, authors, editors, and developers use this skill to polish English-language technical or analytical nonfiction written by non-native speakers while preserving facts, argument structure, and author voice. It can detect Chinglish patterns, produce nativized revisions, and generate reviewable diffs and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI reads input documents and writes polished output and reports to user-selected paths. <br>
Mitigation: Run it only on documents you intend to process, choose non-critical output filenames, and keep backups before overwriting or comparing important drafts. <br>
Risk: The diff helper uses predictable temporary files on shared systems. <br>
Mitigation: Avoid running the polisher on sensitive content in shared multi-user environments unless temporary-file exposure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muchenhengxin/english-polish) <br>
- [Publisher profile](https://clawhub.ai/user/muchenhengxin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, HTML, ANSI terminal output, JSON reports, and rewritten text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Detector output may include scores, issue density, pattern matches, and severity bands; polisher output may include rewritten files, markdown diff reports, HTML summaries, and batch JSON summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter and changelog list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
