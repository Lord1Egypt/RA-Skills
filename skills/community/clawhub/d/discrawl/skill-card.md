## Description: <br>
Discord archive: search, sync freshness, DMs, channel slices, SQL counts, and Discrawl repo work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw](https://clawhub.ai/user/openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Discrawl to inspect local Discord archive data, check archive freshness, search DMs or channel slices, and report exact counts, date spans, and known gaps before relying on live Discord APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Discord archives and DMs may contain sensitive conversations. <br>
Mitigation: Install only when archive search is intended, treat exported snapshots as private, and do not include secrets or private DM rows in shared snapshots. <br>
Risk: Discord synchronization can require bot credentials or access to local Discord Desktop artifacts. <br>
Mitigation: Use least-privilege bot credentials, do not provide Discord user tokens, and do not write to Discord storage. <br>
Risk: Unsafe SQL mutations could alter archive data. <br>
Mitigation: Keep SQL read-only unless the user explicitly approves a reviewed mutation. <br>


## Reference(s): <br>
- [Discrawl repository](https://github.com/openclaw/discrawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and query snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include absolute date spans, channel or DM names, counts, and known gaps from local Discord archive data.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
