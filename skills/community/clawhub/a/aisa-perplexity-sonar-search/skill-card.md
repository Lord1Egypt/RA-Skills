## Description: <br>
Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, and structured retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill to run AIsa-backed Perplexity Sonar searches and convert recent or multi-source retrieval into summaries, comparisons, competitor scans, trend discovery, or research briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires the sensitive AISA_API_KEY credential for API access. <br>
Mitigation: Provide the key through the environment only, avoid committing it to skill files or logs, and rotate it if exposed. <br>
Risk: Search results or provider timeouts can lead to incomplete or stale research output. <br>
Mitigation: Report unavailable providers or timeouts explicitly and avoid claiming sources that were not queried. <br>
Risk: The available scanner context was clean but did not deeply verify artifact-specific behavior. <br>
Mitigation: Review the shipped SKILL.md, README.md, and script permissions before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/aisa-perplexity-sonar-search) <br>
- [AIsa API Endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples and JSON API responses from the bundled search client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY for AIsa-backed API access; the search client prints structured JSON and returns nonzero status for failed API responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
