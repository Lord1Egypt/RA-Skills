## Description:

Ask LLM Council a question from chat and return the chairman's synthesized multi-model consensus answer without opening the web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeadland](https://clawhub.ai/user/jeadland)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to submit quick decision or research questions to a local LLM Council backend and receive the final synthesized answer with a link to the full discussion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Questions are sent to a local LLM Council backend and may be processed by the models or providers configured there.

Mitigation: Install only where the local backend and its providers are trusted, and avoid sending secrets or sensitive personal data.

Risk: Untrusted model output is printed to the terminal without terminal-output sanitization.

Mitigation: Review returned output before reuse and add terminal-control sanitization before regular use.

Risk: The skill depends on a local backend and may fail or time out if that service is unavailable or still processing.

Mitigation: Confirm the backend is running before use and treat timeout or failure messages as operational errors.

## Reference(s):

- [Ask Council ClawHub skill page](https://clawhub.ai/jeadland/skills/ask-council)
- [LLM Council repository](https://github.com/jeadland/llm-council)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with a shell command invocation and a returned discussion link when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Invokes a local backend, polls for completion, and times out after 120 seconds.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter and _meta.json list 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
