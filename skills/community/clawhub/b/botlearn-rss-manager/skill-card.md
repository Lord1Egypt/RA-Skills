## Description: <br>
Aggregates and deduplicates RSS/Atom feeds, scores and clusters articles by importance, and generates concise daily digests with source attribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinxhk](https://clawhub.ai/user/calvinxhk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to manage RSS/Atom subscriptions, remove duplicate coverage, rank important stories, and produce structured daily news digests or feed health reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching untrusted RSS or Atom feed URLs can expose the agent to unwanted redirects or private-network targets. <br>
Mitigation: Subscribe only to trusted feed URLs, avoid localhost or private-network URLs, and validate redirect targets before keeping feed URL changes. <br>
Risk: Persistent feed-source changes after redirects can alter the set of sources being monitored. <br>
Mitigation: Require confirmation or validation before permanently updating subscribed feed URLs. <br>
Risk: Low-quality or malformed feeds can produce misleading digest rankings or incomplete items. <br>
Mitigation: Preserve source attribution, skip malformed items, use source credibility and corroboration signals, and surface feed health issues in the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/calvinxhk/botlearn-rss-manager) <br>
- [RSS/Atom feed formats, XML parsing, and content extraction](knowledge/domain.md) <br>
- [RSS manager best practices](knowledge/best-practices.md) <br>
- [RSS manager anti-patterns](knowledge/anti-patterns.md) <br>
- [RSS manager strategy](strategies/main.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown digest or feed management report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source attribution, importance scores, topic clusters, trend indicators, and feed health notes when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.md frontmatter; package manifests list 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
