## Description: <br>
AI short drama generation - account management, script writing, video production. Integrated X2C billing for commercial deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use Ai Director to turn short-drama concepts into scripts, manage X2C account binding and characters, produce videos, and evaluate generated output quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend paid X2C credits during script, video, and retry workflows. <br>
Mitigation: Confirm generation parameters, expected costs, and delete or retry actions with the user before running commands that consume credits. <br>
Risk: API keys may be stored in local credential files. <br>
Mitigation: Protect credential files, avoid sharing them, and rotate X2C or Gemini keys if exposure is suspected. <br>
Risk: Prompts, private video URLs, and generated content may be sent to X2C or Gemini services. <br>
Mitigation: Avoid sensitive prompts or private media unless the user has approved sending that content to the relevant service. <br>
Risk: Security evidence reports a confirmed prompt-to-shell command injection path in auto-iterate behavior. <br>
Mitigation: Avoid auto-iterate with untrusted prompts until command construction is fixed; prefer manual review and direct producer commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/patches429/ai-director) <br>
- [Publisher profile](https://clawhub.ai/user/patches429) <br>
- [X2C Open API Documentation](references/X2C-OPEN-API.md) <br>
- [AIDirector API Reference](references/api-docs.md) <br>
- [Tested Workflow](references/TESTED-WORKFLOW.md) <br>
- [Quality and Retry Workflow](references/QUALITY-AND-RETRY.md) <br>
- [AI Short Drama Quality Scoring](references/quality-scoring.md) <br>
- [Ad Writer Guide](references/AD-WRITER-GUIDE.md) <br>
- [Giggle Pro](https://giggle.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON snippets; bundled scripts produce API calls, JSON status, video URLs, and credential or configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and X2C_API_KEY; quality evaluation may also require GEMINI_API_KEY; generation and iteration can consume paid X2C credits.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
