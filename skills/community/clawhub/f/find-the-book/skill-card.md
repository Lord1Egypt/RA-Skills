## Description: <br>
Finds book information from Douban and WeChat Reading, including ratings, summaries, and reading links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wintersun661](https://clawhub.ai/user/wintersun661) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Readers and agents use this skill to look up book recommendations or specific titles, then present Douban ratings, author or summary information, Douban detail links, and optional WeChat Reading links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Book titles or reading interests may be sent to external search and book websites. <br>
Mitigation: Use only when sharing those queries with external services is acceptable. <br>
Risk: Runtime behavior depends on Python packages and external website responses. <br>
Mitigation: Review or pin dependencies in controlled environments and validate returned links before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wintersun661/find-the-book) <br>
- [Publisher profile](https://clawhub.ai/user/wintersun661) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown recommendations with book titles, Douban ratings and links, summaries, and optional WeChat Reading links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a required book query and optional result count; availability and freshness depend on external search and book websites.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
