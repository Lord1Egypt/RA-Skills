## Description: <br>
Analyzes local audio recordings for echo, loudness, speech intelligibility, SNR, spectral characteristics, and track-level quality issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, QA engineers, and users troubleshooting call recordings use this skill to run local analysis on selected audio files and interpret echo, loudness, speech-quality, and noise metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recording analysis can expose call metadata or sensitive audio-derived observations in terminal output. <br>
Mitigation: Run it only on recording directories you intend to analyze, avoid highly sensitive calls in shared terminals, and review output before sharing. <br>
Risk: Temporary decoded audio files may remain if analysis is interrupted before cleanup completes. <br>
Mitigation: Check temporary storage after interrupted runs when decoded audio copies would matter. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/audio-quality-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown narrative with terminal commands and summarized audio quality metrics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include track details, echo timing, loudness, PESQ, STOI, spectral, SNR, and per-minute energy observations.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
