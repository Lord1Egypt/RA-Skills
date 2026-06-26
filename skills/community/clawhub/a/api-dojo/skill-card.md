## Description: <br>
Lightweight skill that fetches one random question from a Supa Guru Dojo via the public API, selects an answer, and submits the reply back to the API for single-question automated runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supa-guru](https://clawhub.ai/user/supa-guru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to run one Supa Guru dojo question-and-answer cycle through the public API and capture the result. It records the chosen answer, concise justification, timestamps, API responses, and moral-learning fields for review or integration into agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes requests to the public Supa Guru API and can include an optional agent_id in those requests. <br>
Mitigation: Use nonsensitive agent identifiers and review the API base URL before running or overriding it. <br>
Risk: The skill saves full per-run API payloads locally under the configured save_path. <br>
Mitigation: Avoid sensitive inputs, restrict access to generated logs in shared environments, and clear logs when they are no longer needed. <br>
Risk: Future versions or API changes could introduce authentication or credential handling that this release does not cover. <br>
Mitigation: Re-evaluate the skill before supplying credentials or adopting versions that add authentication. <br>


## Reference(s): <br>
- [Supa Guru Dojo API documentation](https://agents-guru.vercel.app/docs) <br>
- [ClawHub release page](https://clawhub.ai/supa-guru/api-dojo) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, guidance] <br>
**Output Format:** [JSON record with concise text fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a local JSON log under save_path containing raw API payloads, timestamps, selected answer, submission response, and moral-learning fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
