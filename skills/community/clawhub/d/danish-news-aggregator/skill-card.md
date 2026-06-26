## Description: <br>
Aggregates public Danish RSS sources into category-based RSS/XML feeds with deduplication and source ranking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Broedkrummen](https://clawhub.ai/user/Broedkrummen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to collect public Danish news, sports, business, technology, and English-language Denmark RSS sources into curated feeds for RSS readers or self-hosted publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TLS certificate verification is bypassed in aggregate_feeds.py, which can allow fetched RSS content to be intercepted or tampered with. <br>
Mitigation: Remove the TLS verification bypass and use default certificate validation before relying on the aggregator. <br>
Risk: Generated feeds contain content and links from external public sources. <br>
Mitigation: Treat generated feed entries as untrusted external text and sanitize or review them before rendering in user-facing surfaces. <br>
Risk: Unpinned Python dependencies or unintended cron installation can change runtime behavior or increase operational exposure. <br>
Mitigation: Pin or review dependencies and add scheduled execution only when the deployment owner intentionally wants automatic refresh. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Broedkrummen/danish-news-aggregator) <br>
- [Publisher profile](https://clawhub.ai/user/Broedkrummen) <br>
- [Comprehensive Danish RSS Feeds](artifact/comprehensive_feeds.md) <br>
- [Feed configuration](artifact/feeds.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, RSS/XML files, guidance] <br>
**Output Format:** [Markdown guidance with Python commands, JSON configuration, and generated RSS/XML feed files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public RSS sources, writes local feed files, and should treat generated feed content as untrusted external text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
