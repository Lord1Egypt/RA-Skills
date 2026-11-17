## Description:

Automates Baidu searches with browser interaction and returns search result titles, links, and page content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongkun01](https://clawhub.ai/user/xiongkun01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run live Baidu searches through browser automation and collect result titles, links, and page content for user-provided keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Baidu during live browser-based searches.

Mitigation: Avoid sensitive queries unless the user is comfortable sending those terms to Baidu, and confirm ambiguous browser-automation requests before execution.

Risk: Frequent automated searches can trigger Baidu anti-automation checks such as CAPTCHA challenges.

Mitigation: Throttle searches, add pauses between queries, and require human intervention if anti-automation challenges appear.

Risk: Baidu page structure changes can cause result extraction to miss or mislabel titles and links.

Mitigation: Verify selectors and extracted results against the current Baidu page structure before relying on the output.

## Reference(s):

- [Baidu page structure reference](artifact/references/baidu_page_structure.md)
- [Baidu search examples](artifact/examples/search_example.md)
- [Baidu Search](https://www.baidu.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text search-result summaries with titles and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live search results may vary by query, location, Baidu ranking, page structure, and anti-automation checks.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
