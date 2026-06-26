## Description: <br>
boss-job helps agents use OpenCLI to search BOSS Zhipin jobs, view job details, greet recruiters, inspect chats, and send messages through a Chrome session where the user is already logged in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spyqwer1](https://clawhub.ai/user/spyqwer1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to search and review BOSS Zhipin roles, start recruiter conversations, review chat history, and send replies from their own logged-in account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a logged-in Chrome session to read private BOSS Zhipin chats and send real messages from the user's account through external tooling not included in the reviewed artifact. <br>
Mitigation: Install only if the referenced OpenCLI package, Chrome extension, and GitHub plugin are trusted; use a separate Chrome profile where practical. <br>
Risk: Automated recruiter greetings or replies may contact the wrong person or send unintended message text. <br>
Mitigation: Manually verify the job, recruiter or chat ID, and exact message text before allowing greet or send commands to run. <br>


## Reference(s): <br>
- [OpenCLI](https://github.com/jackwener/opencli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenCLI, its Chrome extension, and an active Chrome login to zhipin.com.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
