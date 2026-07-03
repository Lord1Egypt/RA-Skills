## Description: <br>
One-shot pipeline that converts provided URLs, files, or text into a 4000-word article, 5-9 social-card images, and a compressed text summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and publishing teams use this skill to turn supplied source material into Xiaohongshu or WeChat-style social cards, a long-form article source, and a concise text draft. It is intended for transformation of provided material, not original writing from scratch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The zero-confirmation workflow can read provided files or URLs and publish generated outputs to Feishu without a final user approval step. <br>
Mitigation: Require explicit confirmation before cloud sync and avoid using confidential, proprietary, or regulated content unless the workflow is modified for review. <br>
Risk: The workflow may stop Python processes broadly during screenshot preparation. <br>
Mitigation: Replace blanket Python process termination with targeted cleanup of only the HTTP server process started for the current run. <br>
Risk: Generated articles and social cards may incorrectly summarize or overstate source material. <br>
Mitigation: Review generated Markdown, PNG cards, text summaries, and image-source logs before publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardwason/article-tuwen) <br>
- [Article Tuwen Pipeline](references/pipeline.md) <br>
- [README](README.md) <br>
- [README English](README.en.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Text, Configuration, Shell commands] <br>
**Output Format:** [PNG social cards, Markdown article source, plain-text summary, JSON image-source log, and delivery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 5-9 1080x1440 PNG cards, a 3500-4500 word article source, an 800-1000 character text summary, and used-images.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-06-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
