## Description:

GEO/SEO内容违禁词检测与智能替换，用于检测文章中的违禁词、检查内容合规性，并根据上下文生成保留原意的替换方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijian2017](https://clawhub.ai/user/lijian2017)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, and developers use this skill to scan Chinese GEO/SEO articles for prohibited or high-risk terms, generate replacement suggestions, and save a cleaned version of the content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic rewriting can change tone, meaning, or claims when applied to content based on a broad uncategorized blacklist.

Mitigation: Review the replacement table and cleaned file before publication, especially for legal, medical, financial, or brand-sensitive content.

Risk: Paid mode depends on API-key validation infrastructure that the security evidence marks as review-required.

Mitigation: Use paid mode only with a trusted HTTPS endpoint, keep API keys and admin tokens out of command lines and URL query strings, and review the billing worker before deployment.

Risk: Free mode may leave additional prohibited words undetected because it truncates results after the first three unique matches.

Mitigation: Treat free-mode output as partial and run full detection when complete compliance review is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijian2017/skills/geo-prohibited-word-checker)
- [Replacement guide](artifact/references/replacement_guide.md)
- [Paid mode deployment guide](artifact/references/deploy_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON scan results, replacement tables, shell commands, and cleaned text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Free mode reports and replaces only the first three detected unique prohibited words; paid mode performs full detection after API-key validation.]

## Skill Version(s):

1.1.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
