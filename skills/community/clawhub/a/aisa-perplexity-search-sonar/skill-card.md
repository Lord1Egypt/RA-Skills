## Description: <br>
Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, and structured retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to run AIsa-backed Perplexity Sonar searches and turn web or multi-source retrieval into summaries, comparisons, competitor scans, trend notes, or research briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries, optional system instructions, and AISA_API_KEY to api.aisa.one. <br>
Mitigation: Avoid using it for secrets, regulated data, or private workspace content unless the provider's data handling has been reviewed. <br>
Risk: Returned research may be incomplete, time out, or omit sources that were not actually queried. <br>
Mitigation: Report provider timeouts or partial retrieval honestly and verify important claims against cited sources before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baofeng-tech/aisa-perplexity-search-sonar) <br>
- [AIsa API endpoint](https://api.aisa.one/apis/v1) <br>
- [Publisher profile](https://clawhub.ai/user/baofeng-tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON responses from the bundled CLI when invoked] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; sends search queries, optional system instructions, and the API key to api.aisa.one.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
