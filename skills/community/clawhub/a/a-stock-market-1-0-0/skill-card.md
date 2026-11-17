## Description:

Retrieves real-time A-share stock quotes and index data for Shanghai and Shenzhen exchange symbols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicenasa](https://clawhub.ai/user/nicenasa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-monitoring users can query A-share stock symbols or major indices from an agent workflow and receive current quote data for one or multiple symbols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock symbols are sent to Tencent Finance when quote data is requested.

Mitigation: Install only if this external data request is acceptable for the intended environment.

Risk: The documented install command creates a system-wide symlink to a user-writable workspace script.

Mitigation: Prefer running the script directly or installing a root-owned copy instead of linking /usr/local/bin/a-stock to a user-writable file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicenasa/skills/a-stock-market-1-0-0)
- [Publisher profile](https://clawhub.ai/user/nicenasa)
- [Tencent Finance quote API](https://qt.gtimg.cn/q={stock_code})

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text stock quote summaries with command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stock symbols are provided as command-line arguments using sh or sz exchange prefixes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
