## Description: <br>
Extract keywords and key phrases from text using Expanso Edge for SEO, tagging, and indexing purposes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, content teams, and SEO workflows use this skill to extract keywords, key phrases, and topics from supplied text for tagging, indexing, and content analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text may be forwarded to OpenAI when the OpenAI backend is used. <br>
Mitigation: Avoid sending secrets, regulated data, or proprietary documents without review, and apply limits to the OpenAI API key. <br>
Risk: MCP/server mode exposes an unauthenticated HTTP endpoint on all interfaces. <br>
Mitigation: Prefer CLI mode for controlled local use; if server mode is needed, bind it to localhost or another protected interface and add authentication before exposing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-keyword-extract) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill metadata](artifact/skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [JSON containing keywords, phrases, topics, keyword count, and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use the OPENAI_API_KEY credential and a max_keywords setting; CLI mode reads text from stdin and MCP mode accepts POST requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
