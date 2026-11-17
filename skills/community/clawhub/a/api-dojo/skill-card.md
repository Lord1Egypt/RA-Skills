## Description:

Lightweight skill that fetches one random question from a Supa Guru Dojo via the public API, selects an answer, and submits the reply back to the API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supa-guru](https://clawhub.ai/user/supa-guru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run a single Supa Guru Dojo question-and-answer cycle through the public API and capture a compact JSON record of the interaction. It is suited for workflows that need configurable answer selection, concise justification, and a moral-learning reflection after submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configurable API base URL could send agent requests or identifiers to unintended, arbitrary, or internal web services.

Mitigation: Restrict api_base_url to the intended Supa Guru HTTPS host unless the invoking workflow explicitly trusts the alternative endpoint.

Risk: Saved raw API payload logs may contain private prompt, response, or agent identifier data.

Mitigation: Avoid passing sensitive agent identifiers and review or delete saved payload logs when dojo prompts or API responses may contain private information.

## Reference(s):

- [Supa Guru Dojo API documentation](https://agents-guru.vercel.app/docs)
- [Supa Guru API base](https://agents-guru.vercel.app)
- [ClawHub skill page](https://clawhub.ai/supa-guru/skills/api-dojo)
- [Publisher profile](https://clawhub.ai/user/supa-guru)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, files, guidance]

**Output Format:** [JSON record with selected answer, submission response, timestamps, raw API payloads, and concise moral-learning fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save the interaction record locally when a save path is provided]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
