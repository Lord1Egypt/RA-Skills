## Description: <br>
Generate mindmaps with Felo Mindmap API in Claude Code. Use when users ask to create/make/generate mindmaps, mind maps, or thinking maps, or when explicit commands like /felo-mindmap are used. Handles API key check, mindmap creation with various layouts, and final mindmap_url output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to turn a topic, question, or set of notes into a Felo-hosted mindmap with a selectable layout and optional LiveDoc attachment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mindmap prompts are sent to Felo and may contain sensitive user content. <br>
Mitigation: Use this skill only with content appropriate for Felo processing; do not include secrets, regulated data, or confidential internal material. <br>
Risk: An endpoint override could route prompts and the FELO_API_KEY away from the documented Felo API. <br>
Mitigation: Confirm FELO_API_BASE is unset or points to https://openapi.felo.ai before running the skill, and protect FELO_API_KEY as a credential. <br>


## Reference(s): <br>
- [Felo Mindmap API](https://openapi.felo.ai/docs/api-reference/v2/mindmap.html) <br>
- [Felo Open Platform](https://openapi.felo.ai/docs/) <br>
- [Felo](https://felo.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/felo-mindmap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown result with a mindmap URL, or JSON when requested through the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include resource_id, mindmap status, mindmap_url, livedoc_short_id, and setup or error guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
