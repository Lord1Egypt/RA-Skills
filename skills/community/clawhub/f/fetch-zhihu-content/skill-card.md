## Description: <br>
Downloads public Zhihu articles, answers, and question pages from user-provided URLs and saves extracted content as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucky-dreamer](https://clawhub.ai/user/lucky-dreamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch Zhihu article, answer, or question content from one or more URLs and preserve the result as local Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports under-disclosed scraping evasion behavior and weakened browser sandbox settings. <br>
Mitigation: Review the Playwright launch settings and anti-detection behavior before installation, and remove or harden those settings for sensitive environments. <br>
Risk: The skill can fetch and save third-party web content, including content that may require rights or authorization. <br>
Mitigation: Use it only for public content or content the user has a right to save, and avoid providing cookies or session data unless credential handling is explicitly documented and reviewed. <br>
Risk: Fetched content is written to local Markdown files and may include source URLs, timestamps, extracted text, and image links. <br>
Mitigation: Choose a dedicated output folder and review generated files before sharing or committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucky-dreamer/skills/fetch-zhihu-content) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown files plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes one timestamped zhihu_{type}_{title}.md file per successful URL, including source URL, content type, fetch time, extracted text, and image links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
