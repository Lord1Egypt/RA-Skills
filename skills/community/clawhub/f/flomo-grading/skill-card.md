## Description: <br>
Randomly presents Flomo notes for S/A/B/C/D/E scoring, learns the user's rating preferences, and keeps an evolving note-quality rubric. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayshna](https://clawhub.ai/user/jayshna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who keep personal notes in Flomo use this skill to review random notes, score their value, and refine a personal rubric for what makes a note worth keeping or revisiting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly accesses, displays, and stores private Flomo note data. <br>
Mitigation: Install only if this level of note access is acceptable, avoid using it on highly sensitive notes, and verify the Flomo token source and scope before use. <br>
Risk: Bundled or generated scoring history can contain note identifiers, tags, ratings, and preference metadata. <br>
Mitigation: Clear or replace bundled history before use when it is not yours, and decide how generated history files will be deleted or retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayshna/flomo-grading) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Grading principles](artifact/grading-principles.md) <br>
- [Public scoring history](artifact/scoring-history.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown responses with local Markdown and JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Displays full note content during rating sessions and updates grading-principles.md and scoring-history.json as preferences are learned.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
