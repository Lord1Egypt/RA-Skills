## Description: <br>
Prepare scripts for FlowSpeech text-to-speech workflows, including narration copy, emotion tags, pause markers, voice direction, multilingual TTS segmentation, QA checks, and guidance for turning raw text into expressive audio scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waeckerlinfederowicz66-sketch](https://clawhub.ai/user/waeckerlinfederowicz66-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to convert raw copy into FlowSpeech-ready narration scripts with mode selection, voice direction, emotion and pause tags, segmentation, pronunciation notes, and publication QA checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is tagged as requiring sensitive credentials and the security guidance notes workflows may interact with authenticated local or platform tools. <br>
Mitigation: Install and use it only in environments where configured credentials are appropriate for the requested work, and review any authenticated actions before proceeding. <br>
Risk: Generated voice scripts can contain claims, emotional direction, or voice-cloning related requests that may be unsuitable for publication without review. <br>
Mitigation: Use the skill's QA checklist to verify claims, review emotion and pause density, check pronunciation, and confirm consent for any voice-cloning scenario. <br>


## Reference(s): <br>
- [FlowSpeech Script Patterns](references/flowspeech-script-patterns.md) <br>
- [FlowSpeech](https://flowspeech.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with headings, optional tables, bracketed voice direction tags, pause markers, pronunciation notes, and QA checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Long scripts may be segmented into paste-ready sections; timing is estimated from spoken words per minute.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
