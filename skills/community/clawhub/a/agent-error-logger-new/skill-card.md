## Description: <br>
Agent Error Logger records, searches, and analyzes agent errors so agents can avoid repeating past mistakes and generate corrective suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KoonChaoSo](https://clawhub.ai/user/KoonChaoSo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record task failures, search prior error patterns, and surface reminders before similar work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local error logs may capture secrets or sensitive customer or business data. <br>
Mitigation: Use the skill only for durable local error logs and avoid recording secrets or sensitive data. <br>
Risk: The included GitHub publishing script can create a public repository and push the current directory. <br>
Mitigation: Run create-repo.sh only after reviewing the files to be published and intentionally choosing public release. <br>
Risk: The artifact includes an example that places a personal access token in a Git URL. <br>
Mitigation: Use GitHub CLI, SSH, or a credential manager instead of embedding tokens in URLs. <br>


## Reference(s): <br>
- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651) <br>
- [Chain-of-Verification Reduces Hallucination in Large Language Models](https://arxiv.org/abs/2309.11495) <br>
- [ClawHub Skill Development Guide](https://clawhub.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local error-log entries, search results, and checklist-style reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
