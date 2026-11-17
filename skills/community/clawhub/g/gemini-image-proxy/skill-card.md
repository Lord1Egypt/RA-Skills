## Description:

Generate and edit images with Gemini API using the OpenAI Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yspcoder](https://clawhub.ai/user/yspcoder)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate new images or edit existing images through an OpenAI-compatible Gemini image endpoint from a Python CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images are sent to the configured external OpenAI-compatible endpoint.

Mitigation: Use only a trusted HTTPS `GOOGLE_PROXY_BASE_URL`, and avoid confidential prompts or sensitive images unless the provider is approved for that data.

Risk: Runtime behavior depends on the installed `openai` package version.

Mitigation: Install in an isolated Python environment and pin `openai` when reproducibility matters.

Risk: The skill requires API credentials in environment variables.

Mitigation: Store `GOOGLE_PROXY_API_KEY` and `GOOGLE_PROXY_BASE_URL` in the runtime environment or secret manager, and do not hard-code them into prompts, logs, or source files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yspcoder/skills/gemini-image-proxy)
- [ClawHub publisher profile](https://clawhub.ai/user/yspcoder)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown instructions with bash commands and a Python script that writes image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_PROXY_API_KEY, GOOGLE_PROXY_BASE_URL, and the openai Python package; generated or edited images are saved to the requested output path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
