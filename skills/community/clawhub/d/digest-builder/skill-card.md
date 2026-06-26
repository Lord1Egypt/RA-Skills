## Description: <br>
Converts raw feed candidates, especially FreshRSS unread items, into structured Digest candidate pools through de-duplication, clustering, content checks, filtering, Chinese summarization, tagging, and preliminary ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gcdd1993](https://clawhub.ai/user/gcdd1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and feed-heavy knowledge workers use this skill to turn FreshRSS unread items or raw feed entries into a structured candidate pool for deciding what belongs in a digest. It is a preprocessing workflow, not a final daily digest writer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs access to a FreshRSS API password to fetch unread items. <br>
Mitigation: Use a FreshRSS API password rather than a web login password, prefer environment variables or a local config file, and do not share generated configuration files. <br>
Risk: Unread feed titles, links, excerpts, summaries, and reading-history-derived outputs are saved under digest output paths. <br>
Mitigation: Review generated JSON and Markdown files before sharing, committing, or uploading them to another system. <br>
Risk: The mark-as-read helper can change FreshRSS read state when deliberately invoked. <br>
Mitigation: Run the helper only on purpose, use dry-run first, and apply date filtering so it does not mark the wrong items as read. <br>


## Reference(s): <br>
- [Digest Builder ClawHub release](https://clawhub.ai/gcdd1993/digest-builder) <br>
- [Digest Spec](references/digest-spec.md) <br>
- [FreshRSS Google Reader API](references/freshrss-google-reader.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON digest files, plus concise command output and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles FreshRSS credentials, unread feed metadata, local digest files, and optional mark-as-read operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
