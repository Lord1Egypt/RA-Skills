## Description: <br>
DeepDive OSINT is an autonomous OSINT investigation tool that searches a subject, extracts entities, maps relationships into an interactive 3D graph, and highlights money flows, shell chains, gaps, and cross-links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinndarkblade](https://clawhub.ai/user/sinndarkblade) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investigators, researchers, journalists, analysts, and security teams use this skill to start and expand OSINT investigations, extract entities from search results, identify relationship patterns, and produce investigation summaries and graph artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch and run a full GitHub application and pip dependencies during invocation. <br>
Mitigation: Review or pin the repository and run the skill in a constrained environment before using it with operational data. <br>
Risk: Investigation data and provider settings may be stored locally by the underlying application. <br>
Mitigation: Avoid sensitive documents and real API keys until storage behavior and provider data flow have been reviewed. <br>
Risk: OSINT outputs may include incorrect, incomplete, or unverified relationships. <br>
Mitigation: Verify findings against independent sources before sharing results or taking action. <br>


## Reference(s): <br>
- [DeepDive GitHub repository](https://github.com/Sinndarkblade/deepdive) <br>
- [DeepDive OSINT ClawHub listing](https://clawhub.ai/sinndarkblade/deepdive-osint) <br>
- [sinndarkblade publisher profile](https://clawhub.ai/user/sinndarkblade) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline Python and shell code blocks plus generated local investigation graph files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local investigation directories, JSON graph data, and interactive HTML board artifacts when the underlying application is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
