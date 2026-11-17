## Description:

Guides an agent through autonomous multi-step research using Google Gemini Deep Research Agent for market analysis, competitive landscaping, literature reviews, technical research, and due diligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai)

### License/Terms of Use:


## Use Case:

Developers and research-oriented users use this skill to request detailed research reports, monitor long-running research tasks, resume prior research, and receive markdown, JSON, or raw responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package does not include the research script and requirements that the skill tells agents to run.

Mitigation: Review or supply the missing script and requirements before installing or running the skill.

Risk: Research queries and follow-up prompts may be sent to Google Gemini.

Mitigation: Avoid sensitive due-diligence material unless sending it to Google Gemini is intended and approved.

Risk: The workflow uses a paid external Gemini service.

Mitigation: Monitor API costs and usage before starting long or repeated research tasks.

## Reference(s):

- [Google AI Studio](https://aistudio.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports, JSON, raw API responses, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research tasks are described as taking 2-10 minutes with optional streaming, status checks, and continuation by interaction ID.]

## Skill Version(s):

1.0.0 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
