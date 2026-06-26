## Description: <br>
Timed interleaved study sprint for OpenAlgernon that shuffles due cards across installed materials and ends with a post-sprint retrieval test. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AntonioVFranco](https://clawhub.ai/user/AntonioVFranco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners using OpenAlgernon use this skill to run 15, 25, or 45 minute interleaved review sessions across installed study materials and measure retention before and after the sprint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and updates a local OpenAlgernon SQLite study database. <br>
Mitigation: Confirm the database path and sqlite3 dependency before use, and install only where the agent is allowed to access and update that study database. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with prompts, progress summaries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local OpenAlgernon SQLite database path and logs sprint retention metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
