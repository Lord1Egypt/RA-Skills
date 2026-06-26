## Description: <br>
Triage and route anything that comes up during a session - bugs, ideas, improvements, small fixes - to the right place. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, designers, and other agent users use this skill to capture off-task bugs, ideas, improvements, and follow-up work during a session, then route each item to GitHub Issues, agent memory, TODO.md, or a paste-ready fallback so it remains discoverable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad automatic triggers may turn casual off-task phrases into durable notes, memory entries, or GitHub Issues. <br>
Mitigation: Configure the agent to ask for confirmation before writing records, especially before storing conversation content or creating GitHub Issues. <br>
Risk: Persistent local or remote writes can preserve sensitive or irrelevant session content longer than intended. <br>
Mitigation: Review the proposed title, type, priority, destination, and body before approving any record. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/clarezoe/dev-inbox) <br>
- [README](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured task records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or append persistent records in GitHub Issues, agent memory, TODO.md, or paste-ready text after user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
