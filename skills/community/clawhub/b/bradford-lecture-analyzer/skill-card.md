## Description: <br>
Extracts YouTube subtitles and produces structured lecture summaries with key points, evidence, and action items for review and teaching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wallfacer-web](https://clawhub.ai/user/wallfacer-web) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Educators, learners, and reviewers use this skill to turn YouTube lecture subtitles into concise bilingual summaries and structured study or teaching notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network requests are routed through a hardcoded local proxy at 127.0.0.1:26739. <br>
Mitigation: Run the skill only where that proxy is expected and trusted, or review and adjust proxy settings before use. <br>
Risk: Transcript text and summaries are saved to a local report, and --summary-only should not be treated as a privacy/no-save mode. <br>
Mitigation: Use the skill only for videos whose transcript text may be stored locally, and remove generated reports when they are no longer needed. <br>
Risk: The skill depends on external Python packages for YouTube transcript retrieval. <br>
Mitigation: Install dependencies from trusted package sources and review dependency versions according to the target environment's software supply chain policy. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Console text and a local Markdown-style lecture analysis report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches YouTube subtitles through a local proxy and saves transcript-derived summaries locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
