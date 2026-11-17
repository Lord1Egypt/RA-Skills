## Description:

This skill helps agents discover, collect, and summarize the latest trending and viral open-source AI or LLM projects from public sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leon0401](https://clawhub.ai/user/leon0401)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and AI product teams use this skill to track recent open-source AI, LLM, multimodal, agent, and tooling projects and turn public trend signals into a concise Markdown intelligence report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to public trend sources and writes a local trending_report.json file.

Mitigation: Run it only in environments where outbound public web requests and local report creation are acceptable.

Risk: Generated links, paper metadata, and trend rankings may be incomplete or stale, and one arXiv fetch path uses HTTP.

Mitigation: Treat generated results as research leads and verify project licenses, release status, and important paper metadata before relying on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leon0401/skills/ai-trending-models)
- [AI Trending Sources Reference Guide](references/sources.md)
- [AI Trending Models Report Template](references/report_template.md)
- [GitHub Trending Python](https://github.com/trending?since=weekly&l=python)
- [Hugging Face Trending Models](https://huggingface.co/models?sort=trending)
- [Papers With Code Trending](https://paperswithcode.com/trending)
- [arXiv cs.AI Recent](https://arxiv.org/list/cs.AI/recent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report, with optional JSON trend data from the fetcher]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language when possible and includes dated trend summaries, ranked tables, project links, paper links, and trend observations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
