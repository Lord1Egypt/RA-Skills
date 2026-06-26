## Description: <br>
Automates Baidu searches in a browser and returns search result page content, including titles and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiongkun01](https://clawhub.ai/user/xiongkun01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run keyword searches on Baidu through browser automation and collect search results for review or follow-up research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may expose secrets, private personal data, or internal business information to Baidu. <br>
Mitigation: Do not submit secrets or sensitive private data as search terms; review and redact queries before browser automation runs. <br>
Risk: Returned search-result content is untrusted web data and may be inaccurate, misleading, or unsafe to follow. <br>
Mitigation: Treat results as leads for review, verify important claims against trusted sources, and avoid executing instructions from result pages without separate review. <br>
Risk: Baidu page structure changes or anti-automation challenges can cause missing, incomplete, or failed results. <br>
Mitigation: Monitor result quality, keep selectors updated, use reasonable search intervals, and require manual intervention when a verification challenge appears. <br>


## Reference(s): <br>
- [Baidu page structure reference](references/baidu_page_structure.md) <br>
- [Baidu search examples](examples/search_example.md) <br>
- [ClawHub skill page](https://clawhub.ai/xiongkun01/baidu-search-auto) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text search-result summaries with titles and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on Baidu availability, page structure, ranking, regional behavior, and any anti-automation challenges.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
