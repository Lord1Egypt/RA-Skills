## Description: <br>
Monitor content from people, topics, and sources across platforms with smart filtering, tiered alerts, and searchable archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Follow to configure monitoring for people, topics, and feeds, filter noisy updates, archive concise summaries with links and timestamps, and retrieve digests or targeted answers from the archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring unauthorized, private, or regulated sources can create privacy, compliance, or permission issues. <br>
Mitigation: Use the skill only for authorized sources and avoid private or regulated content unless permission is documented. <br>
Risk: Archived content and alert destinations can expose sensitive watched-source information. <br>
Mitigation: Store archives in a user-controlled location and review configured alert destinations before use. <br>
Risk: External platform tooling such as APIs, scrapers, yt-dlp, RSS tools, and bots may introduce account, rate-limit, or supply-chain risk. <br>
Mitigation: Install external tools from trusted sources and follow each platform's access rules and rate limits. <br>


## Reference(s): <br>
- [Follow ClawHub release](https://clawhub.ai/ivangdavila/follow) <br>
- [Source Configuration](artifact/sources.md) <br>
- [Platform Integration](artifact/platforms.md) <br>
- [Filtering Rules](artifact/filtering.md) <br>
- [Alert Configuration](artifact/alerts.md) <br>
- [Querying the Archive](artifact/querying.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance, shell commands] <br>
**Output Format:** [Markdown guidance with source templates, alert rules, query formats, and shell-command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archives favor summaries with links and timestamps rather than full content dumps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
