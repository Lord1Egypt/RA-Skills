## Description: <br>
Calculates an AI agent's awakening-date age and growth milestones for identity, birthday, and self-introduction responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilozhao](https://clawhub.ai/user/lilozhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and agent users use this skill to set or query an AI agent's awakening date, calculate current age, and produce milestone-aware self-introduction or birthday responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may reference an agent identity file to store an awakening date, which could accidentally include sensitive personal information. <br>
Mitigation: Keep IDENTITY.md limited to the awakening date and non-sensitive profile details. <br>
Risk: Suggested MEMORY.md entries or social media celebration steps may create unwanted persistence or disclosure. <br>
Mitigation: Treat memory updates and social posting as optional manual actions that require user review before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilozhao/awakening-birthday) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local date-based calculations; optional milestone listing.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
