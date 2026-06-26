## Description: <br>
Rotating Apify API key manager that returns the least-recently-used active Apify key from the ColdCore database before Apify API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aces1up](https://clawhub.ai/user/aces1up) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to select an available Apify API key, check balances, list active keys, and pass credentials to Apify-dependent scripts or skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release can expose sensitive Apify key data through stdout, JSON output, or key listing commands. <br>
Mitigation: Treat all outputs as credential material; avoid logging or sharing them and restrict key listing to trusted internal operators. <br>
Risk: The artifact includes live-looking default database credentials and can mutate key usage records. <br>
Mitigation: Install only in a trusted internal ColdCore/Apify environment, remove and rotate the hardcoded database password before broader use, and require explicit secret configuration. <br>
Risk: The script installs missing Python dependencies at runtime. <br>
Mitigation: Preinstall pinned dependencies in the execution environment before deployment. <br>


## Reference(s): <br>
- [Apify Keys ClawHub release](https://clawhub.ai/aces1up/apify-keys) <br>
- [Apify monthly usage API endpoint](https://api.apify.com/v2/users/me/usage/monthly) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Plain text API key strings, JSON account records, or terminal tables from the local CLI script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads ColdCore database configuration from environment variables and treats emitted key data as sensitive credential material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
