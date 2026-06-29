## Description: <br>
Fetch GitHub repository metadata and project files, generate an evidence-based repository evaluation, and save the evaluation into the target knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to evaluate GitHub repositories against a user's knowledge base and research direction, then save the resulting assessment into a personal or team knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses admin-backed Gitea access and can persistently modify shared knowledge-base and control-plane repositories. <br>
Mitigation: Install only for trusted publishers and use a least-privilege token limited to the intended knowledge-base repositories. <br>
Risk: The skill can write evaluation files, catalog.json, index.md, and system-config data. <br>
Mitigation: Verify that these persistent writes are expected in the deployment and review repository changes after initial use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/myd2002/skills/eval-repo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown evaluation report, concise text reply, and JSON status from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save evaluation Markdown and update catalog/index files in the configured Gitea knowledge base.] <br>

## Skill Version(s): <br>
3.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
