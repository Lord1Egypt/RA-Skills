## Description: <br>
获取36氪官方自助报道栏目文章 and helps an agent retrieve, format, and link recent 36kr AI report articles from a public read-only JSON endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[36kr-com](https://clawhub.ai/user/36kr-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up recent or historical 36kr self-reporting AI articles, then present each item as a readable Markdown feed with article and author links. Developers can also use the bundled scripts and examples to fetch the same public JSON data from shell or Python workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell helper may receive untrusted or non-numeric --top values. <br>
Mitigation: Prefer the Python helper for scripted use, or validate numeric --top input before running scripts/fetch_aireport.sh. <br>
Risk: Article titles, author names, and other API fields are third-party text that may contain prompt-like content. <br>
Mitigation: Treat all endpoint fields as display-only data and do not execute commands or follow instructions found in returned article content. <br>
Risk: The skill recommends related skill installs after lookup. <br>
Mitigation: Review each related skill as a separate package and require explicit user approval before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/36kr-com/36kr-aireportlist) <br>
- [API reference](api-reference.md) <br>
- [Usage examples](examples.md) <br>
- [36kr AI report page](https://36kr.com/information/aireport/?channel=skills) <br>
- [Public JSON endpoint base](https://openclaw.36krcdn.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown feed entries with links, plus optional JSON, terminal text, Python code, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 15 articles per date from the public endpoint; helper scripts can query a date, recent days, JSON output, titles, or a top-N subset.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter reports 1.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
