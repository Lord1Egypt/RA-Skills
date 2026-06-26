## Description: <br>
Pure intelligence gathering for TikTok and Instagram that helps an agent discover trending hooks, analyze competitor strategy, or look up creator profile data without generating content or posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iammiracle](https://clawhub.ai/user/iammiracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developer-operated agents use this skill to research TikTok and Instagram trends, competitor hooks, and creator profile metrics before planning content strategy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ScrapeCreators API key and sends researched keywords, hashtags, and creator handles to ScrapeCreators. <br>
Mitigation: Use a limited or quota-bound API key where possible, keep the key in the environment instead of command-line arguments, and avoid sending sensitive private research terms. <br>
Risk: The metadata recommends installing uv with a curl-to-shell command. <br>
Mitigation: Review the installer before execution or install uv through a trusted package manager approved for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iammiracle/cocreator-content-research) <br>
- [Publisher profile](https://clawhub.ai/user/iammiracle) <br>
- [uv installer referenced by skill metadata](https://astral.sh/uv/install.sh) <br>
- [ScrapeCreators TikTok profile endpoint](https://api.scrapecreators.com/v1/tiktok/profile) <br>
- [ScrapeCreators Instagram profile endpoint](https://api.scrapecreators.com/v1/instagram/profile) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and SCRAPE_CREATORS_API_KEY; scripts send researched keywords, hashtags, and creator handles to ScrapeCreators.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
