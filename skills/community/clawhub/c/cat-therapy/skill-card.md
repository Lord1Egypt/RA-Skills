## Description: <br>
Cat Therapy responds to break, stress, and cat-related prompts with cat images, cat-sound text or audio cues, and short bilingual comfort messages, with optional custom cat media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyxy](https://clawhub.ai/user/yyxy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill in chat agents to request a short relaxation break with cat images, cat sounds, and supportive quotes. Users can also save or reset one custom cat image or sound for later therapy responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes leftover user-specific preference data in user_cats.json. <br>
Mitigation: Review or delete user_cats.json before installing or redistributing the skill. <br>
Risk: Custom cat photos or sounds are stored in a shared local skill file with weak privacy boundaries. <br>
Mitigation: Use custom media only when users are comfortable with that media being stored in the skill directory, and verify how the OpenClaw environment scopes skill files between users or workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yyxy/cat-therapy) <br>
- [Cataas Cat Image API](https://cataas.com/cat) <br>
- [TheCatAPI Image Search](https://api.thecatapi.com/v1/images/search) <br>
- [PlaceKitten fallback image source](https://placekitten.com/400/300) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Media URLs, Audio files, Guidance] <br>
**Output Format:** [JSON objects and chat-ready text with image URLs and optional local audio file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Falls back to text and default image URLs when external image sources or local audio assets are unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
