## Description: <br>
Creates and updates distilled agent skills for anime and game virtual characters by separating canon, persona, and style examples into a canonical source and runtime wrappers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobemorelucky](https://clawhub.ai/user/tobemorelucky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to build or update text-first character roleplay skills from user-supplied notes, summaries, quotes, or wiki-style materials while keeping factual canon separate from inferred persona and wording style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated child skills can retain chat-derived preferences, boundaries, relationship state, summaries, and excerpts in a local workspace database. <br>
Mitigation: Install only in workspaces where local file generation and local memory are acceptable, isolate workspaces for no-memory runs, and delete .dreamlover-data/memory.sqlite3 when a fresh memory state is required. <br>
Risk: Character generation may blur factual canon with inferred persona or style if source handling is not reviewed. <br>
Mitigation: Use the intake, source audit, canon, persona, and style layers separately, and review generated packages before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobemorelucky/dreamlover-skill) <br>
- [Output Contract](artifact/docs/output-contract.md) <br>
- [Safety Rules](artifact/docs/safety.md) <br>
- [Memory Policy](artifact/references/memory_policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown files, JSON metadata, Python-backed runtime files, and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated child skills may use conditional local memory stored outside the package under .dreamlover-data when runtime memory is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
