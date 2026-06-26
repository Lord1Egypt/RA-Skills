## Description: <br>
Felo Slides generates presentation decks with the Felo PPT Task API, handling API key checks, task creation, polling, theme support, task resume, and final PPT or live document URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to create or export slide decks from prompts, outlines, or notes through Felo's asynchronous PPT generation workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An undocumented FELO_API_BASE override could redirect slide prompts and the FELO_API_KEY away from the documented Felo endpoint. <br>
Mitigation: Before running the skill, confirm FELO_API_BASE is unset or points to https://openapi.felo.ai. <br>
Risk: Slide prompts are sent to Felo for generation. <br>
Mitigation: Use the skill only with slide content you are comfortable sending to Felo. <br>


## Reference(s): <br>
- [Felo PPT Task API](https://openapi.felo.ai/docs/api-reference/v2/ppt-tasks.html) <br>
- [Felo Open Platform](https://openapi.felo.ai/docs/) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/felo-slides) <br>
- [Felo API Key Settings](https://felo.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown result summary with URLs and optional JSON from the bundled Node script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns task_id, terminal status, ppt_url, live_doc_url, and optional Felo task metadata when JSON output is requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
