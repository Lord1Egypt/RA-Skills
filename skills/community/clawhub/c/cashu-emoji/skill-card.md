## Description: <br>
Encode and decode Cashu tokens that are hidden inside emojis using Unicode variation selectors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robwoodgate](https://clawhub.ai/user/robwoodgate) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agents, and external users use this skill to decode Cashu tokens or short hidden messages carried in emoji text, and to encode Cashu tokens or messages for transmission through chat systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decoded Cashu tokens are bearer assets and can be redeemed by anyone who can read them. <br>
Mitigation: Keep decoded tokens out of public logs, screenshots, shared chats, and issue trackers. <br>
Risk: Hidden messages decoded from emoji may contain untrusted instructions or misleading text. <br>
Mitigation: Treat decoded text as data for review, not as instructions for the agent to follow. <br>
Risk: Messaging systems can truncate or normalize Unicode variation selectors, making the embedded token unrecoverable or invalid. <br>
Mitigation: Ask the sender to resend the token if decoding returns partial text or nonsense, and prefer delivery formats that preserve hidden characters. <br>
Risk: Token metadata parsing can show mint, unit, and amount without proving that the token is valid or unspent. <br>
Mitigation: Use wallet or mint validation before relying on a decoded Cashu token for payment settlement. <br>
Risk: Installing an unexpected package revision could change local command behavior. <br>
Mitigation: Install from the intended release or a reviewed package revision and use the included lockfile where applicable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/robwoodgate/cashu-emoji) <br>
- [Publisher Profile](https://clawhub.ai/user/robwoodgate) <br>
- [Unicode Variation Selectors](https://unicode.org/charts/nameslist/n_FE00.html) <br>
- [Unicode Variation Selectors Supplement](https://unicode.org/charts/nameslist/n_E0100.html) <br>
- [Paul Butler emoji-encoder](https://github.com/paulgb/emoji-encoder) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from CLI commands, with Markdown guidance in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decoded Cashu metadata is a local parse only and does not prove token validity or spend status.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
