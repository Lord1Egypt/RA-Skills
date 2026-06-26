## Description: <br>
Manage Bohrium knowledge bases through the open.bohrium.com API, including literature, folders, uploads, tags, notes, permissions, and search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sorrymaker0624](https://clawhub.ai/user/sorrymaker0624) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Bohrium users use this skill to create, organize, upload to, search, and administer literature knowledge bases from an agent workflow. It can guide or generate Python API calls and command-line upload steps for credentialed Bohrium operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform credentialed Bohrium operations that may delete or expose knowledge-base data. <br>
Mitigation: Use it only with trusted Bohrium accounts, verify target knowledge-base and node IDs, and require explicit confirmation before deletes, permission changes, public sharing, or bot messaging. <br>
Risk: Credential handling can be confusing, and the runtime may use an unexpected ACCESS_KEY. <br>
Mitigation: Confirm which ACCESS_KEY is configured or passed before running any operation, and keep credentials scoped to the intended Bohrium account. <br>
Risk: Upload helpers can send local file contents to Bohrium if given broad or accidental file paths. <br>
Mitigation: Review upload paths and parent IDs before execution, and prefer dry-run or single-file checks before batch uploads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sorrymaker0624/bohrium-knowledge-base) <br>
- [Bohrium Knowledge API base URL](https://open.bohrium.com/openapi/v1/knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include credentialed Bohrium API calls and file-upload commands; review target IDs, file paths, sharing settings, and destructive actions before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
