## Description: <br>
Run ChatGPT with stronger prompts, Projects, GPTs, memory boundaries, and output QA for research, writing, analysis, and planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, developers, and other ChatGPT users use this skill to choose the right ChatGPT surface, build reusable prompt packets, manage Projects and GPTs, maintain memory boundaries, and QA outputs before relying on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad activation preference could cause the skill to engage on casual ChatGPT mentions when the user does not want workflow guidance. <br>
Mitigation: Choose a narrow activation preference during setup and update ~/chatgpt/memory.md if the preference changes. <br>
Risk: Local workflow notes under ~/chatgpt/ could accumulate stale or sensitive information over time. <br>
Mitigation: Periodically review ~/chatgpt/ and keep notes limited to reusable workflow boundaries rather than secrets, raw private documents, or one-off content. <br>
Risk: Prompts, uploaded files, and examples used in ChatGPT workflows may leave the user's machine through ChatGPT. <br>
Mitigation: Use Temporary Chat or avoid upload for sensitive work, and only run workflows when that ChatGPT data flow is acceptable for the task. <br>
Risk: ChatGPT outputs can contain unsupported claims or miss the user's actual brief. <br>
Mitigation: Run the included output QA checks for source fidelity, constraint fit, uncertainty, and goal match before relying on or publishing an answer. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/chatgpt) <br>
- [Skill Homepage](https://clawic.com/skills/chatgpt) <br>
- [Setup - ChatGPT](artifact/setup.md) <br>
- [ChatGPT Surface Routing](artifact/surfaces.md) <br>
- [Prompt Packets for ChatGPT](artifact/prompt-packets.md) <br>
- [Output QA for ChatGPT](artifact/output-qa.md) <br>
- [ChatGPT Project Playbook](artifact/project-playbook.md) <br>
- [Memory Template - ChatGPT](artifact/memory-template.md) <br>
- [ChatGPT Troubleshooting](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with prompt templates, workflow checklists, local note structures, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to local notes under ~/chatgpt/ and to user-provided ChatGPT workflow context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
