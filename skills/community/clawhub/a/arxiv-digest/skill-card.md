## Description: <br>
Daily AI/ML paper digest from HuggingFace Papers Trending with accessible interpretations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifei68801](https://clawhub.ai/user/lifei68801) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and AI practitioners use this skill to fetch trending AI/ML papers, rank them by community interest and freshness, and receive concise digests in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts HuggingFace to retrieve public paper metadata. <br>
Mitigation: Allow network access only to the documented HuggingFace Papers endpoint and review generated digests before forwarding them. <br>
Risk: Some documented features appear aspirational or manually configured, including local history, arXiv-source fetching, cron delivery, and QQ/Notion push setup. <br>
Mitigation: Validate any scheduler, delivery channel, and local-history configuration separately before enabling automated delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lifei68801/arxiv-digest) <br>
- [Publisher profile](https://clawhub.ai/user/lifei68801) <br>
- [HuggingFace Papers API](https://huggingface.co/api/daily_papers) <br>
- [arXiv category taxonomy](https://arxiv.org/category_taxonomy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown digest with paper metadata, links, summaries, ranking details, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports English and Chinese output, configurable paper limits, day ranges, and HuggingFace-backed paper retrieval.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
