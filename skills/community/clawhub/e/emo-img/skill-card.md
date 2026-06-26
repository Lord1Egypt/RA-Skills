## Description: <br>
Send sticker and emoji images in chat by searching a local collection or Tenor, downloading favorites, and sending media through supported messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Horisky](https://clawhub.ai/user/Horisky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to let agents respond to chats with matching stickers or GIFs, search or manage a personal sticker collection, and send selected media through supported channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sticker names and indexed paths may allow file operations outside the intended sticker directory. <br>
Mitigation: Patch or constrain path handling before deployment, pin STICKER_DIR to a dedicated directory, and review indexed file paths before sending or deleting media. <br>
Risk: The skill can automatically download and send media in chat. <br>
Mitigation: Use it only in contexts where automatic media sending is acceptable and confirm the target chat, recipient, and media before sending. <br>
Risk: Online fallback contacts Tenor with the search query. <br>
Mitigation: Avoid sensitive search terms, prefer local-only search for private conversations, or disable online fallback where external queries are not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Horisky/emo-img) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Tenor search API endpoint](https://tenor.googleapis.com/v2/search) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Media attachments, Guidance] <br>
**Output Format:** [JSON command output and messaging-tool media payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches local sticker metadata first and can contact Tenor for online results; downloaded media is stored in the configured sticker directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
