## Description: <br>
Doubao Genbgm uses Volcano Engine's Doubao Music Generation API to generate instrumental background music and vocal songs from prompts, lyrics, and configurable music parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fackee](https://clawhub.ai/user/fackee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content creators use this skill to generate instrumental BGM or vocal songs from text prompts or lyrics, with controls for genre, mood, timbre, key, tempo, instruments, duration, and output format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lyrics copyright checks can be bypassed with --skip-copy-check. <br>
Mitigation: Use only original or licensed lyrics, keep copyright checks enabled by default, and review any use of --skip-copy-check before generation. <br>
Risk: Prompts, lyrics, and generation settings are sent to Volcano Engine using configured API credentials. <br>
Mitigation: Avoid submitting sensitive or unapproved content, protect VOLC_ACCESS_KEY and VOLC_SECRET_KEY, and limit credential access to intended users. <br>


## Reference(s): <br>
- [Doubao Music Generation Parameter Quick Reference](references/params.md) <br>
- [Volcano Engine Console Key Management](https://console.volcengine.com/iam/keymanage/) <br>
- [Volcano Engine Open API Endpoint](https://open.volcengineapi.com/?Action=XXX&Version=2024-08-12) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands that run a Python script and produce local MP3 or WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.9+, requests, a Volcano Engine account with music generation enabled, and VOLC_ACCESS_KEY and VOLC_SECRET_KEY credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
