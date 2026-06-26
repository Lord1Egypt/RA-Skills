## Description: <br>
Aggregates recent China AI policy updates from national agencies, Guangdong, Guangzhou, and related public sources into concise brief-style analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whitetin](https://clawhub.ai/user/whitetin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Policy analysts, developers, and operators use this skill to run a disclosed Python crawler over public government, media, and aggregator sources, filter recent AI-related policy items, and produce a concise Markdown brief with key points, source links, and trend analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler contacts public government, media, and aggregator websites, so individual sites may fail, block access, or omit usable dates. <br>
Mitigation: Review crawler errors and treat the brief as a current lead list rather than a completeness guarantee. <br>
Risk: Media and smartcity.team results may be supplemental interpretations or aggregations rather than authoritative policy text. <br>
Mitigation: Verify important conclusions against official government source links before relying on them. <br>
Risk: The skill executes a Python crawler with network access and third-party dependencies. <br>
Mitigation: Install it in controlled environments, pin dependencies where possible, and review the crawler before execution. <br>


## Reference(s): <br>
- [AI policy source list](references/policy_sources.md) <br>
- [ClawHub skill page](https://clawhub.ai/whitetin/ai-policy-brief) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown brief with source links, optional JSON crawler output, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses recent public-source crawl results, prioritizes government sources, and summarizes supplemental media or aggregator results separately.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
