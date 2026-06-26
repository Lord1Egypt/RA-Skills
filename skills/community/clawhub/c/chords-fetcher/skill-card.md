## Description: <br>
Fetch clean guitar chords and lyrics from popular sites (mychords.net, amdm.ru, ultimate-guitar.com). Strips tabs, fixes formatting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flobo3](https://clawhub.ai/user/flobo3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to find guitar chords and lyrics for requested songs, then return cleaned, readable chord text without tabs or page clutter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Song and artist queries are sent to DuckDuckGo and public chord websites. <br>
Mitigation: Avoid private or sensitive text in song queries and use the skill only where public web requests are acceptable. <br>
Risk: The script depends on third-party Python packages and public websites whose behavior or availability may change. <br>
Mitigation: Install dependencies from trusted package sources, review dependency updates, and handle unavailable or malformed chord-site responses before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flobo3/chords-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text chord and lyric output, with shell command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries are sent to DuckDuckGo and public chord websites; returned text is cleaned by removing guitar tabs and normalizing chord spacing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
