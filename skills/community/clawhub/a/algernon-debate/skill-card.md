## Description: <br>
Runs a structured technical trade-off debate for OpenAlgernon, pressing the user to defend a position and ending with a balanced synthesis of when each side is appropriate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AntonioVFranco](https://clawhub.ai/user/AntonioVFranco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and technical learners use this skill to practice nuanced design trade-off discussions. It helps structure a debate, challenge assumptions, and produce an interview-style synthesis of the conditions where each approach is strongest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can export debate notes to Notion or append them to local conversation logs without clear approval. <br>
Mitigation: Remove or edit the Notion and memory sections unless they are explicitly wanted, and require a preview plus user confirmation before anything is appended or logged. <br>
Risk: The skill reads from a local study database path that may contain private or unexpected material. <br>
Mitigation: Verify the database path and material scope before use, and only run the database query against data the user intends to use for debate topic selection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AntonioVFranco/algernon-debate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown dialogue prompts with bash command examples and a final synthesis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append debate summaries to Notion and local conversation logs when those sections are retained and configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
