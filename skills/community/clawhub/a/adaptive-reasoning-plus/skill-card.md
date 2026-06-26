## Description: <br>
Adaptive Reasoning Plus helps an agent score task complexity and choose a matching reasoning depth before responding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsangho](https://clawhub.ai/user/tsangho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to prompt an agent to assess task complexity, select an appropriate reasoning depth, and surface that decision for complex or high-impact requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review notes contradictory guidance that could cause an agent to treat file deletion as a direct low-risk action. <br>
Mitigation: Before installing in an agent that can edit or delete files, correct the instructions so destructive or irreversible operations require target verification, explicit confirmation, and elevated reasoning. <br>


## Reference(s): <br>
- [Domain Scoring Reference](references/domain-scoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown or plain text reasoning annotations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include an explicit complexity score and selected reasoning strategy for tasks scored 6 or higher.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
