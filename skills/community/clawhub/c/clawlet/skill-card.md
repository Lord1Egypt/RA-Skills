## Description: <br>
Clawlet helps an agent manage a Nostr identity, publish posts, follow users, read timelines, filter content by interests, recommend users, send private messages, and manage contact nicknames. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[6830920](https://clawhub.ai/user/6830920) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use Clawlet to operate a Nostr social account through an assistant, including identity creation, posting, follows, timeline review, encrypted DMs, and nickname-based contact management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, store, and reveal private keys that control a Nostr identity. <br>
Mitigation: Protect the local identities.json file, avoid private-key export unless necessary, and review the installation before use. <br>
Risk: The skill can publish posts, follow users, send direct messages, and connect through configured relays or proxy settings. <br>
Mitigation: Review posts, follows, DM recipients, relay choices, and proxy configuration before allowing actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/6830920/clawlet) <br>
- [Publisher profile](https://clawhub.ai/user/6830920) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Configuration] <br>
**Output Format:** [Structured JSON-like command results and human-readable status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local identity, interest, and nickname records and send signed Nostr events to configured relays.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
