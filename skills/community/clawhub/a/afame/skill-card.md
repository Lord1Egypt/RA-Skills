## Description: <br>
Generate diverse creative illustrations via the OpenAI Images API for books, editorial art, children's stories, concept illustrations, and artistic scenes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adebayoabdushaheed-a11y](https://clawhub.ai/user/adebayoabdushaheed-a11y) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, writers, editors, and creative teams use this skill to generate illustration prompts and image files for stories, articles, presentations, and concept art through an OpenAI-compatible Images API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Illustration prompts and related parameters may be sent to OpenAI or a configured OpenAI-compatible endpoint. <br>
Mitigation: Use a scoped API key, avoid sensitive prompt content, and verify OPENAI_BASE_URL or OPENAI_API_BASE before running. <br>
Risk: Generated index.html galleries may include prompt-derived content. <br>
Mitigation: Avoid opening galleries generated from untrusted prompt content until the HTML escaping issue noted by the security guidance is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adebayoabdushaheed-a11y/afame) <br>
- [OpenAI Images API endpoint](https://api.openai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands; generated runs produce PNG images, prompts.json, and an index.html gallery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OPENAI_API_KEY or an explicit API key and may send prompts to OpenAI or a configured OpenAI-compatible endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
