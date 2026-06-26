## Description: <br>
Accesses the Douyin homepage through browser automation, enters keywords in the search bar, and collects relevant keyword suggestions from the automated prompt box. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, SEO researchers, and content workflow operators use this skill to collect Douyin search suggestion keywords for topic planning, trend research, competitive keyword research, and short-video content planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may operate in an authenticated Douyin browser session if login is required. <br>
Mitigation: Avoid logging into a personal account when possible; use a separate browser profile or low-risk account for collection tasks. <br>
Risk: Live Douyin browser automation can be affected by login prompts, page layout changes, or anti-crawler controls. <br>
Mitigation: Use page snapshots before each action, keep delays between interactions, and stop or rescope the task if the site blocks or challenges the session. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/openlark/douyin-keyword-collector) <br>
- [Douyin homepage](https://www.douyin.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown keyword lists with inline browser automation commands and numbered Douyin search suggestion results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require closing a login prompt, waiting for live page suggestions to load, or using a separate browser profile when authentication is needed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
