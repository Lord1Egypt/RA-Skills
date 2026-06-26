## Description: <br>
Terminal Spotify playback/search via spogo (preferred) or spotify_player. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engahmedsalah358-lgtm](https://clawhub.ai/user/engahmedsalah358-lgtm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and terminal users use this skill to search Spotify and control playback through spogo or spotify_player commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow asks users to import Chrome browser cookies into a third-party CLI for Spotify authentication. <br>
Mitigation: Only run the cookie-import step if spogo is trusted; consider a separate browser profile or documented OAuth/client-id flow, and know how to revoke Spotify sessions or remove stored CLI authentication state. <br>


## Reference(s): <br>
- [Spotify](https://www.spotify.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/engahmedsalah358-lgtm/ahmed) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires either spogo or spotify_player, and a Spotify Premium account for playback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
