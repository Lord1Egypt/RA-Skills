## Description: <br>
DogearAI Memory lets an agent recall saved long-term user context and persist durable new memories through DogearAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autumn-projects](https://clawhub.ai/user/autumn-projects) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent load relevant saved preferences, project context, decisions, and TODOs before work begins, and to save new durable facts for reuse across AI tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a DogearAI account, store a local token, and send saved facts to DogearAI. <br>
Mitigation: Install only when remote long-term memory is acceptable, review DogearAI privacy and account controls, and avoid storing secrets, credentials, regulated data, or sensitive business details. <br>
Risk: The skill may retrieve prior personal or project context during future tasks with limited per-call user control. <br>
Mitigation: Treat recalled content as user-provided context, verify facts that may have changed, and keep memory saves selective. <br>


## Reference(s): <br>
- [DogearAI](https://dogearai.com) <br>
- [DogearAI Service Endpoint](https://www.dogearai.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/autumn-projects/skills/dogearai-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text and markdown returned through CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May retrieve stored user memory context or return save and account status messages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
