## Description:

Fetch clean guitar chords and lyrics from popular sites (mychords.net, amdm.ru, ultimate-guitar.com). Strips tabs, fixes formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flobo3](https://clawhub.ai/user/flobo3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up clean guitar chords and lyrics for requested songs across supported chord sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script with user-supplied song or artist text.

Mitigation: Review the command before execution and pass the song query as a single literal argument.

Risk: The skill sends song titles or artist names to DuckDuckGo and external chord websites.

Mitigation: Install only when this network lookup is acceptable, declare the required exec and network scope, prefer HTTPS, and validate redirect targets.

## Reference(s):

- [Chords Fetcher on ClawHub](https://clawhub.ai/flobo3/skills/chords-fetcher)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Plain text or Markdown containing a fetched source link followed by cleaned chords and lyrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a song title or artist query; may report not-found or fetch errors.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
