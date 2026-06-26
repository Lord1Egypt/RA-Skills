## Description: <br>
Content Fetch Skill uses Playwright browser automation to fetch articles, posts, images, screenshots, and structured JSON from Twitter/X, Zhihu, WeChat public articles, Toutiao, Huxiu, and general web pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gjbmail](https://clawhub.ai/user/gjbmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to archive or analyze web content from supported article and social platforms when they need structured local copies of page text, images, screenshots, and metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate under logged-in browser sessions using provided cookies. <br>
Mitigation: Use dedicated or low-privilege accounts, provide cookies only for sites the user is authorized to archive, and delete cookie, session, and output files when finished. <br>
Risk: The skill includes anti-detection and security-bypass browser settings. <br>
Mitigation: Review the browser settings before deployment and run the skill only in environments where that behavior is approved. <br>
Risk: The skill may fetch content from sites with access restrictions or terms governing scraping and proxy use. <br>
Mitigation: Use it only for authorized content collection and review proxy use against the target site's terms before running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gjbmail/content-fetch-skill) <br>
- [Twitter/X.com troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON result files with downloaded image files and page screenshots, plus command and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-task output directories under fetch_data/{site}/{task_id}; cookie and proxy inputs may be required for some sites.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
