## Description: <br>
Crawl any website and get a 0-100 SEO score with 50+ checks across Technical, On-Page, Schema, Social, and Compliance categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External site owners, marketers, and developers use this skill to audit pages for SEO issues, industry compliance gaps, competitor differences, and prioritized fixes. With an Anthropic API key, it can also generate SEO article drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-provided URLs during audits and compliance scans. <br>
Mitigation: Run it only against URLs you are authorized to check, and avoid submitting sensitive internal URLs unless the execution environment is approved for that use. <br>
Risk: Article generation and AI-backed analysis use Anthropic when ANTHROPIC_API_KEY is configured. <br>
Mitigation: Use the AI-backed features only for topics and page context that may be sent to an external AI provider. <br>
Risk: The release security summary says the documentation overstates some crawl-depth and check-count capabilities. <br>
Mitigation: Treat reported SEO findings as decision support and verify important recommendations before publishing site changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drivenautoplex1/dfw-seo-audit) <br>
- [Project homepage](https://github.com/drivenautoplex1/openclaw-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON audit reports, markdown article drafts, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write reports or generated article markdown to a requested output file.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
