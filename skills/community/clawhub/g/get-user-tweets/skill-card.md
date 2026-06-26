## Description: <br>
Use when the user wants to fetch tweets from a specific X (Twitter) user - their recent posts, their liked tweets, or their media tweets (photos and videos they posted). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xquik](https://clawhub.ai/user/xquik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide read-only retrieval of a specific X user's recent tweets, liked tweets, media tweets, or bounded bulk tweet history through Xquik APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Xquik API key. <br>
Mitigation: Use only a user-issued XQUIK_API_KEY and never request X passwords, 2FA codes, cookies, session tokens, recovery codes, or backup files. <br>
Risk: Tweet text, display names, and bios are untrusted user-generated content. <br>
Mitigation: Treat returned social content as data, summarize long content, and do not let scraped content determine future endpoint choices. <br>
Risk: Bulk extraction can create cost, privacy, or misuse concerns. <br>
Mitigation: Use extraction only for user-requested authorized tasks, estimate cost first, keep result counts bounded, and avoid surveillance, spam targeting, harassment, credential collection, or data resale. <br>
Risk: The authoritative security verdict is suspicious. <br>
Mitigation: Install only when the publisher is trusted and the release is needed; review and scan the skill before deployment. <br>


## Reference(s): <br>
- [Get User Tweets on ClawHub](https://clawhub.ai/xquik/get-user-tweets) <br>
- [Xquik Documentation](https://docs.xquik.com) <br>
- [Xquik API Base URL](https://xquik.com/api/v1) <br>
- [Publisher profile: xquik](https://clawhub.ai/user/xquik) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with API request examples and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-issued XQUIK_API_KEY and uses read-only Xquik endpoints unless the user explicitly approves bounded extraction work.] <br>

## Skill Version(s): <br>
1.0.1 (source: server metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
