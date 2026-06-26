## Description: <br>
Can search and get YouTuber information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poi5305](https://clawhub.ai/user/poi5305) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External marketers, creator economy analysts, and developers use this skill to search CreatorDB for YouTube creators and retrieve profile, performance, sponsorship, content, and audience data through CreatorDB API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends YouTube lookup terms and channel IDs to CreatorDB with a user-provided API key. <br>
Mitigation: Use a dedicated CreatorDB API key when possible, avoid sharing it in prompts or logs, and monitor quota or billing tied to the key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poi5305/creatordb-youtube-v3) <br>
- [CreatorDB](https://www.creatordb.app) <br>
- [CreatorDB YouTube search endpoint](https://apiv3.creatordb.app/youtube/search) <br>
- [CreatorDB YouTube profile endpoint](https://apiv3.creatordb.app/youtube/profile?channelId=UCBR8-60-B28hp2BmDPdntcQ) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline curl examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and CREATORDB_API_KEY; sends YouTube lookup terms and channel IDs to CreatorDB.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
