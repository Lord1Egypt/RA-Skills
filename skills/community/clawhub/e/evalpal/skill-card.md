## Description: <br>
Run AI agent evaluations via EvalPal by triggering runs, checking results, and listing available evaluations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewengman](https://clawhub.ai/user/matthewengman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI evaluation teams use Evalpal to run EvalPal evaluation definitions from an OpenClaw agent, monitor run status, and review pass/fail results in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EvalPal API key for authenticated requests. <br>
Mitigation: Use a scoped or dedicated key when available, provide it through EVALPAL_API_KEY, and avoid pasting the key into chat or logs. <br>
Risk: Changing EVALPAL_API_URL can direct authenticated requests away from the trusted EvalPal endpoint. <br>
Mitigation: Keep EVALPAL_API_URL unset or set only to the trusted EvalPal endpoint expected by the operator. <br>
Risk: Evaluation lists, run status, and results may reveal project names, evaluation names, run IDs, and test outcomes. <br>
Mitigation: Use the skill only in channels where those details are appropriate, and redact sensitive IDs or results before sharing outputs. <br>


## Reference(s): <br>
- [EvalPal](https://evalpal.dev) <br>
- [EvalPal API Docs](https://evalpal.dev/api/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/matthewengman/evalpal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text from shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVALPAL_API_KEY plus curl and jq; evaluation runs may poll for up to 5 minutes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
