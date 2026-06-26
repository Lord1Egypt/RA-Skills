## Description: <br>
Aliyun Codeup helps agents inspect Aliyun Yunxiao Codeup repositories by querying branches, recent commits, and repository statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to inspect Aliyun Codeup projects, including branch inventory, recent commit summaries, and basic repository statistics, using a configured personal access token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a personal access token for Aliyun Codeup access, which could be exposed locally if configured or logged carelessly. <br>
Mitigation: Use a dedicated read-only token with the smallest required scope, store it only in the environment, and avoid putting token values in prompts, files, logs, or command history. <br>
Risk: Private repository contents may be temporarily cloned to local storage during use. <br>
Mitigation: Run the skill only in trusted workspaces, confirm temporary clone cleanup, and avoid using it on repositories whose contents should not be present on the local machine. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexmayanjun-collab/aliyun-codeup) <br>
- [Aliyun Codeup Documentation](https://help.aliyun.com/product/44893.html) <br>
- [Codeup Personal Access Tokens](https://codeup.aliyun.com/settings/tokens) <br>
- [GitLab API Documentation](https://docs.gitlab.com/ee/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the YUNXIAO_PERSONAL_TOKEN environment variable and may temporarily clone private repositories during inspection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
