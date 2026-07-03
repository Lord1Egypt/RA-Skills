## Description: <br>
Fetches public WeChat article pages with Playwright in a real browser, extracts the title, author, and body content, and saves Markdown and HTML copies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucky-dreamer](https://clawhub.ai/user/lucky-dreamer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to retrieve publicly available WeChat public-account articles, convert article content into local Markdown and HTML files, and report the saved paths and article metadata back to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script accepts any HTTP or HTTPS URL and launches a real browser with anti-detection behavior, which can be used beyond the stated WeChat article workflow. <br>
Mitigation: Use the skill only with public mp.weixin.qq.com article URLs and avoid internal, localhost, account, or private URLs until a strict mp.weixin.qq.com allowlist is enforced. <br>
Risk: Fetched content is written to local Markdown and HTML files in the selected output directory. <br>
Mitigation: Choose a trusted output folder and review generated files before sharing or opening them in sensitive environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, html, files, shell commands, guidance] <br>
**Output Format:** [Terminal text plus generated Markdown and HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, Playwright, and an installed supported browser; headed browser mode requires a GUI environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
