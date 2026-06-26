## Description: <br>
Blog Forge helps agents generate SEO-oriented Markdown blog drafts, analyze readability, suggest images, and optionally publish drafts to Medium, WordPress, or Ghost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, content teams, and agent builders can use this skill to turn topics and keywords into blog drafts with SEO metadata, readability scoring, image suggestions, and platform-specific draft publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes humanization behavior associated with AI-detection evasion. <br>
Mitigation: Use generated drafts transparently and do not use humanization to mislead readers or bypass disclosure, platform, or institutional rules. <br>
Risk: The skill can create drafts on connected Medium, WordPress, or Ghost publishing accounts. <br>
Mitigation: Use revocable least-privilege publishing tokens, keep generated posts in draft status, and require human review before publication. <br>
Risk: Topics, prompts, and generated drafts may be sent to cloud model providers when Anthropic or OpenAI models are configured. <br>
Mitigation: Do not provide confidential topics or drafts unless that provider data sharing is acceptable for the user or organization. <br>
Risk: Generated claims, statistics, and SEO guidance may be inaccurate or only illustrative. <br>
Mitigation: Fact-check claims and independently verify statistics, citations, and platform compliance before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/blog-forge) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown blog content with JSON-like metadata objects and JavaScript usage patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured LLM providers and publishing APIs; publishing methods create draft posts by default.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
