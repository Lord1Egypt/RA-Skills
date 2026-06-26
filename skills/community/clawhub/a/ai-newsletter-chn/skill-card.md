## Description: <br>
Generate a daily AI news newsletter for a Chinese audience from fresh web sources, summarizing current AI/ML articles into Markdown and JSON with Simplified Chinese output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to assemble concise Chinese-language AI news digests from recent web sources. It is intended for current AI/ML news, releases, funding, product launches, benchmarks, regulation, and practitioner-relevant developments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Brave and Firecrawl API keys for search and page fetching, which can create quota or billing exposure. <br>
Mitigation: Use scoped keys where available, monitor provider usage, and rotate or revoke keys if the skill is no longer needed. <br>
Risk: Generated newsletters may contain stale, incorrect, or mismatched information from live web results. <br>
Mitigation: Review generated items, source links, warnings, and fallback-search notes before publishing or sharing the newsletter. <br>
Risk: Summarizing current articles can create copyright or attribution concerns if full article text is reproduced. <br>
Mitigation: Keep summaries brief, factual, and linked to the source; do not include full copyrighted article text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/ai-newsletter-chn) <br>
- [Publisher profile](https://clawhub.ai/user/j3ffyang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown newsletter plus structured JSON newsletter data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns newsletter_items, markdown_newsletter, and json_newsletter; final summaries are translated to Simplified Chinese while source titles and URLs are preserved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
