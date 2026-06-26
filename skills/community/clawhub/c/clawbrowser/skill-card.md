## Description: <br>
Clawbrowser guides agents in using the Microsoft Playwright CLI (`playwright-cli`) to navigate pages, interact with forms, capture evidence, manage sessions, extract data, and debug browser workflows without a full MCP browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tezatezaz](https://clawhub.ai/user/tezatezaz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run scripted browser automation, inspect web pages, capture screenshots and traces, and manage Playwright CLI sessions during testing or debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation may expose sensitive authenticated content through sessions, screenshots, PDFs, traces, videos, or saved state. <br>
Mitigation: Use temporary or isolated sessions for sensitive work and delete saved browser artifacts and state files when the task is complete. <br>
Risk: Persistent Playwright CLI sessions can retain authentication state, history, storage, and open tabs between commands. <br>
Mitigation: Name sessions intentionally, stop or delete sessions after use, and avoid saving authentication state unless the workflow requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tezatezaz/clawbrowser) <br>
- [ClawAudit report f4d4fb45](https://clawaudit.duckdns.org/audit/f4d4fb45-ed25-4659-8235-2459d0dc8189) <br>
- [ClawAudit report a55cb413](https://clawaudit.duckdns.org/audit/a55cb413-b111-4f1a-9f39-a5c857090ebf) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance targets playwright-cli workflows and may lead agents to create browser session state or files such as screenshots, PDFs, traces, videos, and snapshots.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
