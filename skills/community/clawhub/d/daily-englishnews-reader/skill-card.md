## Description: <br>
Generates English reading materials from current RSS articles, adapts them to a selected CEFR level, adds vocabulary explanations, and returns a Feishu/Lark cloud document link. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[chegangan](https://clawhub.ai/user/chegangan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and language learners use this skill to generate daily English reading practice from news, business, technology, science, and culture RSS sources. The skill rewrites selected articles to a configured CEFR level and includes vocabulary support plus source attribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Feishu/Lark plugin can create cloud documents after authorization. <br>
Mitigation: Review Feishu/Lark permission prompts and authorize only the intended workspace or account before using the skill. <br>
Risk: The skill fetches article content from third-party RSS services and records generated article titles and URLs locally for deduplication. <br>
Mitigation: Review the configured RSS sources and local history file before deployment, especially when handling sensitive reading preferences. <br>
Risk: The optional sudo install path increases install-time privilege. <br>
Mitigation: Avoid sudo unless necessary, and verify the package source before running elevated installation commands. <br>
Risk: Generated reading materials are rewritten from third-party news and article sources. <br>
Mitigation: Keep source attribution and original URLs in the generated document, and review intended distribution against applicable content-use requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chegangan/daily-englishnews-reader) <br>
- [Publisher profile](https://clawhub.ai/user/chegangan) <br>
- [Feishu/Lark plugin installation documentation](https://bytedance.larkoffice.com/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh) <br>
- [Al Jazeera English RSS source](https://morss.it/:format=json/https://www.aljazeera.com/xml/rss/all.xml) <br>
- [Vox Business RSS source](https://morss.it/:format=json/https://www.vox.com/rss/business-and-finance/index.xml) <br>
- [Cloudflare Blog RSS source](https://morss.it/:format=json/https://blog.cloudflare.com/rss/) <br>
- [The Conversation RSS source](https://morss.it/:format=json/https://theconversation.com/us/articles.atom) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Feishu/Lark cloud document link with rewritten article text, vocabulary notes, source links, and setup guidance when dependencies are missing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local configuration for CEFR level, target article length, vocabulary count, RSS sources, and sent-article history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
