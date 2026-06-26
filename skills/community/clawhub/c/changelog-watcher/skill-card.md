## Description: <br>
Monitor GitHub repos and npm packages for new releases and version updates, summarize changelogs, and highlight breaking changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and release managers use this skill to monitor configured GitHub repositories and npm packages, detect newly published versions, and produce concise markdown changelog reports with breaking-change highlights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured watchlist entries may cause the skill to query unexpected GitHub repositories or npm packages. <br>
Mitigation: Review watchlist.json before running the skill and keep only the repositories and packages intended for monitoring. <br>
Risk: Running with --update-state changes the local state file and advances last-seen versions. <br>
Mitigation: Use dry-run mode first when evaluating results or when state.json should not be updated. <br>
Risk: Cron scheduling or use of a GitHub token can expose the skill to long-running automation and local credential handling. <br>
Mitigation: Schedule it only in trusted environments and provide GitHub tokens through controlled environment variables when higher rate limits are required. <br>


## Reference(s): <br>
- [Changelog Watcher Setup Guide](references/setup-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/changelog-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with optional JSON release data and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are based on a user-maintained watchlist and an auto-managed last-seen state file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
