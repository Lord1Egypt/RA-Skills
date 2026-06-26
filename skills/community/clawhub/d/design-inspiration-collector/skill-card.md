## Description: <br>
Collects design inspiration entry links from Dribbble and Pinterest, filters to official search, tag, topic, or ideas pages, and writes local Markdown and JSON reports for a requested design topic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benson126](https://clawhub.ai/user/benson126) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, product teams, and agents use this skill to gather starting points for UI, UX, and visual design research from Dribbble and Pinterest. It is intended for design-inspiration collection, trend summarization, and follow-on exploration by topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Design topics are sent to Tavily for Dribbble search. <br>
Mitigation: Avoid confidential client names, unreleased product concepts, regulated data, or sensitive research topics in prompts. <br>
Risk: The skill writes Markdown and JSON report files under ~/design_inspirations. <br>
Mitigation: Review generated files before sharing, committing, or using them in client-facing work. <br>
Risk: Search results and constructed platform URLs may reflect platform availability, ranking, or search-quality limitations. <br>
Mitigation: Review the returned Dribbble and Pinterest links and refine the topic when the results are too broad or irrelevant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benson126/design-inspiration-collector) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/benson126) <br>
- [Tavily API key setup](https://app.tavily.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, files, shell commands, guidance] <br>
**Output Format:** [Markdown report plus JSON data file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes timestamped topic reports under ~/design_inspirations and prints the generated Markdown and JSON paths.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact metadata reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
