## Description: <br>
Digital Singer turns a NuwaAI digital avatar into a karaoke-style singing performer with lip-synced vocals, synchronized accompaniment, duet flow, scoring, and blind box rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianglingling007](https://clawhub.ai/user/jianglingling007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local avatar karaoke battle experience where a NuwaAI avatar sings one half of a song and the user sings the other half. It supports browser-based setup, microphone input, song playback, and lighthearted scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles microphone audio, chat text, and avatar credentials, and the security summary says these may be sent to NuwaAI and DashScope/Qwen. <br>
Mitigation: Use only on a trusted local machine, review data handling before use, and avoid sharing sensitive audio or chat content. <br>
Risk: The security guidance identifies API key handling as an area needing review before installation. <br>
Mitigation: Replace any bundled provider keys, rotate exposed keys, and use low-value or dedicated API credentials until credential storage is reviewed. <br>
Risk: The security verdict is suspicious, with guidance to review before installing. <br>
Mitigation: Scan and inspect the release before deployment, and confirm local API protections and credential storage before using valuable accounts. <br>


## Reference(s): <br>
- [Digital Singer ClawHub page](https://clawhub.ai/jianglingling007/digital-singer) <br>
- [Publisher profile](https://clawhub.ai/user/jianglingling007) <br>
- [NuwaAI](https://nuwaai.com) <br>
- [DashScope OpenAI-compatible chat completions endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions and runtime guidance for a local browser karaoke experience.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
