## Description:

Configures OpenClaw to use free OpenRouter models by ranking available free models, setting a primary model, configuring fallbacks, and updating OpenClaw model settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricksmartbrain-boop](https://clawhub.ai/user/ricksmartbrain-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to route agent traffic through free OpenRouter models, maintain fallback chains during rate limits, and inspect or switch model settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes unrelated marketing and monitoring scripts beyond the advertised model-routing workflow.

Mitigation: Review the package before installing and do not run files in the jobs directory unless that behavior is intentional.

Risk: Some bundled scripts can use the user's OpenRouter API key, local tools, and home-directory files for unrelated data collection or analysis.

Mitigation: Limit credential exposure, avoid printing the full OPENROUTER_API_KEY, and run only commands needed for model routing.

Risk: The advertised commands can modify ~/.openclaw/openclaw.json.

Mitigation: Back up the OpenClaw configuration before changing model settings and review the resulting primary model, fallback list, and allowlist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ricksmartbrain-boop/skills/free-model-router)
- [OpenRouter API keys](https://openrouter.ai/keys)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw model settings and cache model metadata; requires an OPENROUTER_API_KEY for OpenRouter access.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
