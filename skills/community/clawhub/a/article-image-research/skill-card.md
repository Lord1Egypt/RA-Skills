## Description: <br>
Researches article images, builds a traceable candidate pool, and records source, license, attribution, risk, and recommended usage for each candidate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacktian89](https://clawhub.ai/user/zacktian89) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, marketers, and content teams use this skill to find, evaluate, and document images for articles, WeChat posts, reports, and web content. It helps match images to specific sections, facts, explanations, comparisons, products, events, or cover needs while preserving attribution and publication-risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image search queries may be sent to external providers, and some providers require API keys in the environment. <br>
Mitigation: Install only when external image-search providers and environment-stored provider credentials are acceptable for the intended workflow. <br>
Risk: Search results, thumbnails, and provider metadata can be incomplete or insufficient for publication clearance. <br>
Mitigation: Treat candidates as research leads and verify the original landing page, license, attribution, subject accuracy, and rights risks before public use. <br>
Risk: Images involving people, trademarks, medical/legal/financial topics, minors, disasters, or disputed events can introduce rights or context risks. <br>
Mitigation: Flag these cases for extra review and avoid recommending images when authorization, identity, timing, context, or permitted use is unclear. <br>


## Reference(s): <br>
- [Article Image Research Skill](https://clawhub.ai/zacktian89/article-image-research) <br>
- [Provider Matrix](references/provider-matrix.md) <br>
- [Query Playbook](references/query-playbook.md) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>
- [Tool Assisted Search](references/tool-assisted-search.md) <br>
- [License Policy](references/license-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON candidate pools with concise Markdown notes and optional figure HTML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes image needs, use/backup/reject decisions, source URLs, license and attribution fields, AI-generated flags, risk flags, scores, and usage notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
