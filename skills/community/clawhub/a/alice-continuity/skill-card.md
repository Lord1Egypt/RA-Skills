## Description: <br>
Local-first memory and continuity for OpenClaw, with recall, resumption briefs, correction-aware memory, open-loop tracking, and provenance-backed context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samrusani](https://clawhub.ai/user/samrusani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent developers use this skill to add Alice as a continuity layer for importing memory, resuming interrupted work, tracking open loops, and explaining why remembered context is present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alice may process the OpenClaw workspace or memory directory selected by the user, which can contain sensitive conversations, credentials, or private project data. <br>
Mitigation: Review the selected workspace or memory directory before import and exclude sensitive content that should not be processed. <br>
Risk: External AliceBot code is referenced by the artifact but is not established by server-resolved provenance for this release. <br>
Mitigation: Verify any external AliceBot code independently before running it. <br>


## Reference(s): <br>
- [Alice Continuity for OpenClaw ClawHub page](https://clawhub.ai/samrusani/alice-continuity) <br>
- [samrusani ClawHub profile](https://clawhub.ai/user/samrusani) <br>
- [AliceBot project](https://github.com/samrusani/AliceBot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with workflow steps, command-oriented instructions, and integration notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for choosing an OpenClaw workspace or memory directory, importing memory, using recall and resumption workflows, and reviewing provenance or corrections.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
