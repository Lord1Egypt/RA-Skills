## Description:

Analyzes what search queries Gemini uses when answering a prompt by running it multiple times with Google Search grounding and reporting query frequency distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

Developers, AEO analysts, and search strategy teams use this skill to study the web search queries Gemini generates for a prompt and compare how often each query appears across repeated runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Google's Gemini API for analysis.

Mitigation: Use this skill only with prompts that are appropriate to send to Google-hosted services.

Risk: The analyzer requires a Gemini API key and the example retrieves it from a named macOS Keychain service.

Mitigation: Use a dedicated, revocable API key and verify the Keychain service name before running the command.

Risk: Repeated concurrent runs can consume quota or hit rate limits.

Mitigation: Keep concurrency at or below the documented default guidance and choose a run count appropriate for the account quota.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psyduckler/skills/aeo-prompt-frequency-analyzer)
- [Gemini GenerateContent API endpoint used by the analyzer](https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports unique search queries with frequency percentages, raw counts, and top referenced sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
