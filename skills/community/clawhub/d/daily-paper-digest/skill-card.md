## Description: <br>
Daily Paper Digest aggregates recent AI papers from arXiv and Hugging Face and formats them for chat delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qjymary](https://clawhub.ai/user/qjymary) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and teams use this skill to collect daily AI paper listings from configured sources, filter them by topic, and produce a readable digest for chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to arXiv and Hugging Face to fetch public paper listings. <br>
Mitigation: Enable it only in environments where outbound access to those sources is allowed. <br>
Risk: The skill is configured for a daily 9:00 scheduled run. <br>
Mitigation: Confirm the schedule before enabling automated execution. <br>
Risk: Digests may be posted to chat channels. <br>
Mitigation: Use channels where public paper titles, summaries, authors, and links are appropriate for the audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qjymary/daily-paper-digest) <br>
- [Configured homepage](https://github.com/your-username/daily-paper-digest) <br>
- [Hugging Face Papers](https://huggingface.co/papers) <br>
- [arXiv category taxonomy](https://arxiv.org/category_taxonomy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Formatted text digest with paper titles, authors, summaries, source links, and run guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output can be filtered through JSON source configuration and is intended for chat delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
