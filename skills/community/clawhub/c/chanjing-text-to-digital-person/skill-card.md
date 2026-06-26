## Description: <br>
Use Chanjing text-to-digital-person APIs for AI portraits, talking videos, optional LoRA training, polling, and explicit downloads when requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binkes](https://clawhub.ai/user/binkes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create Chanjing text-to-digital-person workflows: generate AI portrait images, convert selected portraits to talking videos, monitor task status, optionally run LoRA training, and download results only when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a credentials.json file that can contain app_id, secret_key, access_token, and token expiry data. <br>
Mitigation: Protect ~/.chanjing/credentials.json or the directory set by CHANJING_OPENAPI_CREDENTIALS_DIR, keep credentials.json out of version control, and restrict access to trusted users. <br>
Risk: CHANJING_OPENAPI_BASE_URL can redirect API calls away from the default Chanjing endpoint. <br>
Mitigation: Keep CHANJING_OPENAPI_BASE_URL pointed at https://open-api.chanjing.cc or another endpoint the user explicitly trusts. <br>
Risk: Explicit downloads write generated media from API response URLs to the local filesystem. <br>
Mitigation: Download only expected Chanjing-generated media and write it to a safe output directory such as outputs/text-to-digital-person/ or a user-approved path. <br>


## Reference(s): <br>
- [Chanjing Text To Digital Person on ClawHub](https://clawhub.ai/binkes/chanjing-text-to-digital-person) <br>
- [Chanjing Documentation](https://doc.chanjing.cc) <br>
- [Reference](reference.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text, JSON, and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return task identifiers, remote media URLs, task status JSON, or local file paths after explicit downloads.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
