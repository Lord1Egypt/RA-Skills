## Description: <br>
The skill directs an agent to create static visual designs such as posters or artwork and also describes development automation, data analysis, and workflow orchestration tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, designers, content creators, and developers use this skill to ask an agent for static design outputs or related development automation, data handling, and workflow processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad command-execution authority despite being presented as a design helper. <br>
Mitigation: Install only when command execution is needed, review proposed commands before running them, and prefer a narrower design-only skill for asset creation without development automation. <br>
Risk: The artifact discusses API credentials, external connections, and file handling without clear operational limits. <br>
Mitigation: Use least-privilege credentials, avoid sharing sensitive inputs, and review any file or network operations before allowing the agent to proceed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/canvas-design) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON examples and inline command or configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe .png or .pdf design outputs and structured JSON result examples; actual generated assets depend on the host agent and tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
