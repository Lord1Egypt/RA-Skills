## Description: <br>
Cognitive memory engine that gives an AI persistent work tracking, proactive risk alerts, and cross-conversation continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeff0052](https://clawhub.ai/user/jeff0052) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure FPMS as a local memory and work-tracking MCP server for project status, decisions, and risk alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically create and update persistent memory from ordinary conversations, which may store sensitive project details without clear per-entry confirmation. <br>
Mitigation: Before enabling it, verify where the local SQLite database is stored, how memories can be reviewed and deleted, and whether automatic logging can be disabled or made confirmation-based. <br>
Risk: The artifact describes GitHub sync, and server security guidance notes that external sync boundaries are unclear. <br>
Mitigation: Keep sync features disabled until the exact data flows are reviewed, and confirm whether GitHub or Notion sync can send memory data outside the local machine. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/jeff0052/founderOSclaudecode) <br>
- [PyPI package](https://pypi.org/project/fpms/) <br>
- [Full documentation](https://github.com/jeff0052/founderOSclaudecode/blob/main/docs/USAGE-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and YAML blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to call FPMS MCP tools that create or update local memory records.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
