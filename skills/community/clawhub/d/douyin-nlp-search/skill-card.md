## Description: <br>
Douyin NLP Search helps agents parse Chinese natural-language Douyin video search requests, extract keyword, count, and sort filters, and return formatted text or JSON mock search results. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to interpret Chinese Douyin search requests and produce structured mock search responses for parsing, formatting, and workflow demonstrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results may be mock examples rather than verified live Douyin data. <br>
Mitigation: Treat outputs as parsing and demonstration results unless a real, scoped data source is configured and disclosed. <br>
Risk: Turning the skill into live browser automation, API access, account-session use, or scraping can introduce platform-compliance and credential-handling risks. <br>
Mitigation: Require explicit user confirmation, use scoped credentials or official allowed interfaces, respect platform terms, and apply rate limits before live access. <br>
Risk: Broad Douyin search trigger wording could run in situations where the user only wants planning or guidance. <br>
Mitigation: Confirm intent before enabling any live data access or automation beyond local parsing and mock result formatting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/douyin-nlp-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON search results, plus command examples and implementation guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Current results are mock examples; outputs include parsed keyword, sort order, result count, and video metadata fields such as title, author, engagement counts, duration, and URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
