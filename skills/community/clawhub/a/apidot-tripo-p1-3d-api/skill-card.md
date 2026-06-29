## Description: <br>
Use APIDot for Tripo P1 3D API workflows, including Tripo P1 API, text-to-3D API, image-to-3D API, 3D asset generation, async task submission, task_id handling, polling, task status, and webhook integration based on APIDot docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiehao71727](https://clawhub.ai/user/jiehao71727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this documentation-only skill to route APIDot Tripo P1 3D API questions to current docs, examples, model pages, async task patterns, polling guidance, and webhook integration notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: APIDOT_API_KEY exposure during live API integration work. <br>
Mitigation: Keep the key in a backend secret store or server-side environment variable and avoid placing it in browser code, logs, screenshots, public repositories, or chat output. <br>
Risk: Incorrect APIDot request fields, availability assumptions, limits, or commercial terms. <br>
Mitigation: Verify the current APIDot docs and model page before preparing or sending Tripo P1 requests. <br>
Risk: Private prompts, source image URLs, generated asset URLs, or callback URLs may be exposed through logs or debugging output. <br>
Mitigation: Avoid logging sensitive request and asset data, and treat webhook handlers as idempotent. <br>


## Reference(s): <br>
- [APIDot Tripo P1 Reference](references/api.md) <br>
- [APIDot Docs](https://apidot.ai/docs) <br>
- [APIDot Tripo P1 3D Docs](https://apidot.ai/docs/tripo-p1-3d) <br>
- [APIDot Tripo P1 Model Page](https://apidot.ai/models/tripo-p1-3d) <br>
- [APIDot Examples](https://github.com/APIDotAI/apidot-examples) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no executable files, automatic network calls, or credential storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
