## Description:

Uses Python and an LLM agent to classify and deeply read a specified arXiv paper by ID or URL, then prints reading notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aurora-1412](https://clawhub.ai/user/aurora-1412)

### License/Terms of Use:


## Use Case:

Developers and researchers use this skill to fetch an arXiv paper, classify it into a reading category, and generate structured Markdown notes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper content is sent to the configured LLM provider.

Mitigation: Explicitly set LLM_BASE_URL and LLM_API_KEY for the intended provider before use.

Risk: Python dependencies are unpinned.

Mitigation: Install in an isolated virtual environment and review or pin dependencies before running.

Risk: Generated notes summarize untrusted arXiv paper text and may be influenced by that content.

Mitigation: Treat generated notes as untrusted summaries and review them before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aurora-1412/skills/arxiv-reader)
- [Publisher profile](https://clawhub.ai/user/aurora-1412)
- [arXiv abstract URL example](https://arxiv.org/abs/2401.12345)
- [arXiv PDF URL example](https://arxiv.org/pdf/2401.12345.pdf)
- [OpenAI-compatible API base URL](https://api.openai.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reading notes printed to stdout, including paper metadata and analysis sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese prompts are used by default; output may depend on the configured OpenAI-compatible LLM provider and token settings.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
