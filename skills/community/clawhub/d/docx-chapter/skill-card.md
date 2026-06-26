## Description: <br>
Research-backed chapter pipeline that turns an outline into Markdown and DOCX chapters with source, DOCX, and screenshot verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ccmxigua](https://clawhub.ai/user/ccmxigua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to generate research-backed chapters from structured outlines, produce Markdown and DOCX deliverables, and verify citations, footnotes, and screenshots before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send research excerpts, visible page text, URLs, screenshots, and model-call prompts through search, browser, and agent tools. <br>
Mitigation: Use it only with public, intended source URLs and avoid internal sites, private documents, regulated data, and pages containing secrets. <br>
Risk: The skill requires sensitive credentials for dependent research tooling. <br>
Mitigation: Provide only the minimum required credentials, store them outside generated chapter artifacts, and rotate them if exposed during a run. <br>
Risk: Generated chapters may contain unsupported claims, stale citations, inaccessible URLs, or screenshot evidence that does not match the claim. <br>
Mitigation: Keep the mandatory source, DOCX, and screenshot verification steps enabled and require human review before publication or delivery. <br>


## Reference(s): <br>
- [Docx Chapter Clean on ClawHub](https://clawhub.ai/ccmxigua/docx-chapter) <br>
- [Unified Search Suite dependency](https://clawhub.ai/ccmxigua/unified-search-suite) <br>
- [Claim verification schema](references/claim_verification_schema.json) <br>
- [Mandatory search templates](references/search_templates.md) <br>
- [Citation Check Skill acknowledgment](https://github.com/serenakeyitan/citation-check-skill) <br>
- [Claude Code issue 50597](https://github.com/anthropics/claude-code/issues/50597) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, DOCX, JSON verification reports, PNG screenshots, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces chapter.md, chapter.docx, chapter_verification.json, verification_keywords.json, URL status data, and source screenshots.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
