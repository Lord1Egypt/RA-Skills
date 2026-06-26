## Description: <br>
Deploy Cursor AI agents to GitHub repos. Automatically write code, generate tests, create documentation, and open PRs using your existing Cursor subscription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ParcostaBot](https://clawhub.ai/user/ParcostaBot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to dispatch coding tasks to Cursor Cloud Agents on GitHub repositories, monitor progress, retrieve conversations, and review generated pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cursor cloud agents can operate on selected GitHub repositories using the user's Cursor account. <br>
Mitigation: Install only for intended repositories, review generated pull requests before merging, and restrict Cursor GitHub App permissions to repositories that need access. <br>
Risk: Prompts and repository context may be processed by Cursor cloud services. <br>
Mitigation: Avoid sensitive prompts or repository data unless approved for Cursor cloud processing. <br>
Risk: The skill reads CURSOR_API_KEY from environment or local files, and response cache data may remain on disk. <br>
Mitigation: Prefer a protected dedicated key file or explicit environment variable, restrict env-file permissions, and clear ~/.cache/cursor-api/ on shared machines. <br>
Risk: Agent deletion and follow-up commands affect real Cursor agent state. <br>
Mitigation: Confirm agent IDs before destructive commands and check status or conversation history before follow-up actions. <br>


## Reference(s): <br>
- [Cursor Cloud Agents API Reference](references/api-reference.md) <br>
- [Cursor API Base URL](https://api.cursor.com/v0) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Cursor API key and can create, monitor, stop, delete, and follow up with Cursor cloud agents on GitHub repositories.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
