## Description: <br>
Batch-compile existing Gitea, Obsidian Git, or manual zip material sources into personal or team knowledge bases with preview, confirmation, job tracking, source archiving, codebase overview generation, and import reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge-base operators use this skill to import existing Gitea repositories, Obsidian Git repositories, or uploaded archive sources into personal or team knowledge bases after preview and explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires broad Gitea administrative authority for repository and knowledge-base operations. <br>
Mitigation: Review before shared or production installation and use a narrowly scoped Gitea service account wherever possible. <br>
Risk: The workflow creates persistent control-plane state for sources, jobs, tasks, fingerprints, and notifications. <br>
Mitigation: Confirm where the system-config repository will live and restrict which repositories the service account can read and write. <br>
Risk: The skill processes untrusted zip, PDF, DOCX, and spreadsheet inputs. <br>
Mitigation: Keep the built-in zip count, size, and compression-ratio limits enabled, review scan previews before confirmation, and pin dependencies before production use. <br>
Risk: Local environment configuration includes service URL and token fields. <br>
Mitigation: Protect the .env file and avoid exposing Gitea tokens in logs, reports, or shared workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myd2002/skills/batch-compile) <br>
- [Configured Gitea service URL](http://43.134.182.170:3000) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON script outputs, interactive card payloads, generated summaries, codebase overviews, and import reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw message context and Gitea configuration; uploaded zip processing applies file count, size, and compression-ratio limits.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
