## Description:

Terminal Spotify playback/search via spogo (preferred) or spotify_player.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engahmedsalah358-lgtm](https://clawhub.ai/user/engahmedsalah358-lgtm)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to control Spotify playback, search tracks, select devices, and configure terminal clients through spogo or spotify_player.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The spogo setup path imports Chrome browser cookies, which can expose account-equivalent credentials until the cookies expire or are revoked.

Mitigation: Prefer an official OAuth or device-code flow, or use the spotify_player fallback when it avoids browser-cookie import.

Risk: The preferred spogo dependency is installed from a custom Homebrew tap.

Mitigation: Install only on a trusted machine from a trusted build, review the package source before use, and consider a dedicated browser profile for any cookie-based authentication.

## Reference(s):

- [Spotify](https://www.spotify.com)
- [ClawHub Skill Page](https://clawhub.ai/engahmedsalah358-lgtm/skills/ahmed)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires either spogo or spotify_player and a Spotify Premium account.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
