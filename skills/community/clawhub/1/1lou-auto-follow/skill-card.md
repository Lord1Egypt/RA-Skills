## Description: <br>
管理追剧清单，自动检查并推送1lou网站的最新剧集更新。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluepop1991-cloud](https://clawhub.ai/user/bluepop1991-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a local drama watchlist, check 1lou for new episodes on a schedule or on request, and prepare update notifications and torrent download actions after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs scheduled network checks against 1lou domains. <br>
Mitigation: Install only when automated 1lou update checks are intended, and review the configured domains before use. <br>
Risk: The artifact uses hard-coded local paths and private service addresses. <br>
Mitigation: Review or change the /Users/bluepop paths and 192.168.1.38 service addresses before running the skill. <br>
Risk: The workflow can submit torrent files to qBittorrent after user confirmation. <br>
Mitigation: Approve torrent downloads only from sources the user trusts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bluepop1991-cloud/1lou-auto-follow) <br>
- [1lou primary domain](https://1lou.me) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status messages with links and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update a local JSON watchlist and may prepare torrent download actions after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
