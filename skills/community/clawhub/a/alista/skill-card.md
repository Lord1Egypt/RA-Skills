## Description: <br>
Save restaurants, bars, and cafes from TikTok and Instagram videos, then search saved places and get weekend suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bgrober](https://clawhub.ai/user/bgrober) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Alista to capture restaurant, bar, cafe, and event leads from Instagram or TikTok posts, verify them with Google Places, store them locally, and search or request weekend suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Social-media URLs and place queries are sent to Apify and Google Places using the user's API keys. <br>
Mitigation: Install and use the skill only when this data sharing is acceptable, and configure API keys with appropriate account controls. <br>
Risk: Image downloads and video frame extraction may process third-party media from social platforms. <br>
Mitigation: Use media download and frame extraction only for content the user is authorized to process. <br>
Risk: Saved places are stored in the local SQLite database alista.db. <br>
Mitigation: Treat the database as user data and manage local access, backup, and deletion according to the user's privacy expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bgrober/alista) <br>
- [Google Places API setup](https://console.cloud.google.com/apis/library/places-backend.googleapis.com) <br>
- [Apify Console](https://console.apify.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Conversational text with JSON returned by supporting TypeScript scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google Places and Apify API keys; saved places are stored locally in alista.db.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
