## Description: <br>
Checks a Bilibili creator's latest videos and dynamic updates, including whether the creator posted a new video today. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jianguo99](https://clawhub.ai/user/Jianguo99) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to look up Bilibili creators by mid or username, retrieve recent videos or dynamic posts, and summarize whether there was a same-day video update. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires logged-in Bilibili cookies through the BILIBILI_COOKIES environment variable. <br>
Mitigation: Use a temporary or low-privilege Bilibili session, avoid sharing cookies in prompts or logs, and rotate or clear the session after use. <br>
Risk: Creator search results are cached locally in user_cache.json. <br>
Mitigation: Delete user_cache.json when local creator-search history should not be retained. <br>
Risk: Frequent API calls may hit Bilibili rate limits or fail when cookies expire. <br>
Mitigation: Space requests apart, report rate-limit failures plainly, and refresh cookies only through the documented local environment variable workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jianguo99/bilibili-update-viewer) <br>
- [Bilibili website](https://www.bilibili.com) <br>
- [Bilibili WBI signing reference](https://socialsisteryi.github.io/bilibili-API-collect/docs/misc/sign/wbi.html) <br>
- [Related ClawHub Bilibili API wrapper](https://clawhub.ai/Jacobzwj/bilibili-hot-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and summarized command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Bilibili creator names, mids, video titles, publication times, links, dynamic post summaries, and local cache lookup results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
