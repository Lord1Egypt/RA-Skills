## Description: <br>
Daily digest of the Bitcoin Development mailing list and Bitcoin Core commits. Use when asked about recent bitcoin-dev discussions, mailing list activity, Bitcoin Core code changes, or to set up daily summaries. Fetches threads from groups.google.com/g/bitcoindev and commits from github.com/bitcoin/bitcoin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawd21](https://clawhub.ai/user/clawd21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch a daily Bitcoin development briefing, review recent bitcoindev mailing list threads, inspect Bitcoin Core commit activity, and read archived summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public web pages and GitHub API data from the local environment. <br>
Mitigation: Install only if outbound public web requests to the Bitcoin Development mailing list, gnusha.org mirror, and Bitcoin Core GitHub repository are acceptable. <br>
Risk: The skill writes archives under ~/workspace/bitcoin-dev-archive. <br>
Mitigation: Review the archive location before scheduled use and manage retained summaries according to local storage and data retention expectations. <br>
Risk: Daily cron use creates recurring fetches and local archives. <br>
Mitigation: Enable the daily cron only when recurring Bitcoin development summaries are desired. <br>
Risk: Summaries are generated from fetched public content and may omit context or reflect fetch failures. <br>
Mitigation: Use the linked mailing list threads and commit or pull request links as the source of truth for technical decisions. <br>


## Reference(s): <br>
- [Bitcoin Daily ClawHub Page](https://clawhub.ai/clawd21/bitcoin-daily) <br>
- [Bitcoin Development Mailing List](https://groups.google.com/g/bitcoindev) <br>
- [Bitcoin Core Commits](https://github.com/bitcoin/bitcoin/commits/master/) <br>
- [bitcoindev Public-Inbox Mirror](https://gnusha.org/pi/bitcoindev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with linked mailing list threads and Bitcoin Core pull requests, plus command-line status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Archives raw fetched data and generated summaries under ~/workspace/bitcoin-dev-archive/YYYY-MM-DD/.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
