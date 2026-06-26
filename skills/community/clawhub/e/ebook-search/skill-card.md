## Description: <br>
Search and download ebooks from jbiaojerry.github.io/ebook-treasure-chest by title, author, category, or keywords, with support for epub, mobi, and azw3 results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eyslce](https://clawhub.ai/user/eyslce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to search a public ebook catalog, browse categories, and surface third-party download links for matching books. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The catalog download disables normal HTTPS certificate and hostname verification. <br>
Mitigation: Patch the downloader to use default HTTPS verification before relying on catalog results. <br>
Risk: The skill surfaces third-party ebook download links. <br>
Mitigation: Review download destinations and applicable rights or policies before opening or sharing links. <br>


## Reference(s): <br>
- [Ebook Search ClawHub release](https://clawhub.ai/eyslce/ebook-search) <br>
- [Ebook Treasure Chest catalog JSON](https://jbiaojerry.github.io/ebook-treasure-chest/all-books.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with shell command examples and book search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include book metadata and third-party download URLs returned from the cached public catalog.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
