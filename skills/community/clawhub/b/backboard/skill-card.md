## Description: <br>
Integrate Backboard.io for assistants, threads, memories, and document RAG via a local backend on http://localhost:5100. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisk60331](https://clawhub.ai/user/chrisk60331) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to Backboard.io assistants, threaded conversations, persistent memories, and document retrieval workflows through a local backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local backend exposes powerful Backboard account actions without its own access controls. <br>
Mitigation: Bind the backend only to 127.0.0.1, firewall port 5100, and avoid exposing it on shared or public networks. <br>
Risk: The backend uses a Backboard API key for assistant, thread, memory, and document operations. <br>
Mitigation: Use the least-privileged Backboard API key available and review the skill before installing or running it. <br>
Risk: Memories and uploaded documents may be sent to Backboard for processing. <br>
Mitigation: Store memories or upload documents only when the user is comfortable sending that content to Backboard. <br>
Risk: Development-mode Flask behavior can increase exposure if enabled outside a local environment. <br>
Mitigation: Avoid Flask debug mode and run the backend only in a controlled local environment. <br>


## Reference(s): <br>
- [Backboard.io ClawHub listing](https://clawhub.ai/chrisk60331/backboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance and JSON API responses from the local backend] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BACKBOARD_API_KEY and a local backend listening on port 5100.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
