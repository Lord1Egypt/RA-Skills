## Description: <br>
Performs intelligent web and specialized searches, aggregates multi-source results, and returns summarized answers with source citations and credibility signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to research current topics, verify claims, monitor news, and gather cited information from web, academic, code, and image-oriented sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and retrieved web content may expose sensitive or confidential information to external services. <br>
Mitigation: Use only for non-sensitive web research and avoid secrets, private personal information, or confidential business queries. <br>
Risk: Search results, summaries, and credibility scores can be incomplete, stale, or misleading. <br>
Mitigation: Review cited sources directly and verify important claims before relying on the output for decisions. <br>
Risk: Global npm installation or repository use can target the wrong package if identity is not checked. <br>
Mitigation: Verify the npm package and repository identity before global installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/find-agents) <br>
- [Publisher profile](https://clawhub.ai/user/hgta23) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill description](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Source citations, Guidance] <br>
**Output Format:** [Markdown summaries and structured JSON objects with cited sources, confidence scores, and related queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source URLs, credibility scores, timestamps, language metadata, and follow-up query suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
