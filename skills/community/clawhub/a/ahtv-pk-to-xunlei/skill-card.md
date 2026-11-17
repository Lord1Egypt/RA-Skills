## Description:

Finds 安徽网络电视台《快乐无敌大PK》 full-episode pages from a user-provided date expression, extracts each episode's real video URL, and saves the episodes into 迅雷云盘.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volumexxx](https://clawhub.ai/user/volumexxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to resolve one or more 快乐无敌大PK episodes by date expression and add the resolved media links to Xunlei Cloud Drive with deterministic filenames and deduplication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires Xunlei phone-number and SMS-code login, which exposes sensitive account credentials during use.

Mitigation: Provide credentials only in the real Xunlei login flow and do not share SMS codes outside that flow.

Risk: The agent may add, move, or rename files in the user's Xunlei Cloud Drive.

Mitigation: Review each cloud-drive add, move, and rename action before it is completed.

Risk: AHTV site changes or ambiguous search results can produce missing, ambiguous, or failed episode resolutions.

Mitigation: Use the resolver output as the source of truth and report not-found, ambiguous, video-url-missing, or error statuses rather than fabricating URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volumexxx/skills/ahtv-pk-to-xunlei)
- [AHTV search](https://www.ahtv.cn/search)
- [AHTV 快乐无敌大PK channel](https://www.ahtv.cn/pindao/ahzh/pk)
- [Xunlei Cloud Drive](https://pan.xunlei.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown containing a compact JSON-like summary and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final summaries include input_expr, expanded_dates, aggregate counts, per-date status, episode URL, video URL, target filename, Xunlei path, and message.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
