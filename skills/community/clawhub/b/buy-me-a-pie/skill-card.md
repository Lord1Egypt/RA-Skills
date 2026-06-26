## Description: <br>
Read and change Buy Me a Pie lists, including lists, items, purchased state, sharing, unique items, and account checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[powtac](https://clawhub.ai/user/powtac) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage Buy Me a Pie shopping lists through an unofficial API-first integration. It supports list, item, sharing, unique-item, and account-check workflows when the user provides Buy Me a Pie credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Buy Me a Pie login and PIN credentials to read and change shopping lists. <br>
Mitigation: Provide credentials only through trusted environment variables and avoid exposing them in shared command lines, logs, or transcripts. <br>
Risk: Write operations such as sharing, deleting, renaming, and item updates can change account data. <br>
Mitigation: Review proposed write, share, and delete commands before allowing them to run, and resolve list and item IDs before mutations. <br>
Risk: Changing the API base URL could send credentials or list data to an untrusted service. <br>
Mitigation: Use the default Buy Me a Pie API endpoint unless the replacement endpoint is trusted. <br>


## Reference(s): <br>
- [Buy Me a Pie Skill Architecture](references/architecture.md) <br>
- [Buy Me a Pie API Surface](references/api-surface.md) <br>
- [Buy Me a Pie App](https://app.buymeapie.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and BUYMEAPIE_LOGIN and BUYMEAPIE_PIN credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
