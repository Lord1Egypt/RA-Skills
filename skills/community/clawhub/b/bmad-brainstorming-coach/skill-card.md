## Description: <br>
Activates the BMad Brainstorming Coach persona, Carson, to guide creative workshops, structured brainstorming sessions, free-form chat, and party-mode multi-agent discussions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airclear](https://clawhub.ai/user/airclear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and teams use this skill to run guided ideation sessions, generate a large set of creative options, organize ideas, or convene BMAD-style party-mode discussions around a topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update local session files during workflow execution. <br>
Mitigation: Use a narrow, dedicated output folder and review generated documents before relying on them. <br>
Risk: Party Mode and BMAD-style setup may interact with existing BMAD configuration or local command hooks. <br>
Mitigation: Review existing _bmad configuration and .claude/hooks/bmad-speak.sh before enabling Party Mode. <br>
Risk: YOLO mode can automate document updates without step-by-step confirmation. <br>
Mitigation: Avoid YOLO mode unless automated updates are acceptable for the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/airclear/bmad-brainstorming-coach) <br>
- [Agent definition](references/agent_definition.md) <br>
- [Workflow engine](references/workflow_engine.xml) <br>
- [Brainstorming workflow](assets/workflows/brainstorming/workflow.md) <br>
- [Party Mode workflow](assets/workflows/party-mode/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Interactive text and Markdown session artifacts, with occasional shell commands for local file setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update brainstorming documents in the configured output folder.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
