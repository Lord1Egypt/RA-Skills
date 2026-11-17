## Description:

Extracts YouTube lecture subtitles and produces structured lecture analysis with Chinese and English summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wallfacer-web](https://clawhub.ai/user/wallfacer-web)

### License/Terms of Use:


## Use Case:

Learners, reviewers, writers, and teachers use this skill to turn YouTube lecture captions into a structured review report with key questions, concepts, action items, uncertainties, and bilingual summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated report can include lecture transcript content saved in the current directory.

Mitigation: Run the skill only on videos whose transcript content may be stored locally, and remove generated reports when they are no longer needed.

Risk: The --summary-only option is documented but the security guidance says not to rely on it for privacy until fixed.

Mitigation: Assume transcript content may still be processed or saved, and verify behavior before using the flag in sensitive environments.

Risk: The skill fetches YouTube transcript data through a configured localhost proxy and uses external Python dependencies.

Mitigation: Use a trusted proxy configuration and pin dependencies before deploying in sensitive or controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wallfacer-web/skills/bradford-lecture-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text and a transcript-containing text report with Markdown-style headings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches YouTube transcript data through the configured localhost proxy and writes a lecture_analysis_<video_id>.txt report in the current directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
