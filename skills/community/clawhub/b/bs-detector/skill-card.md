## Description: <br>
Detects key claims in long messages, flags fluff and filler language, and summarizes the core point with simple local heuristics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and writers use this skill to triage long messages locally by extracting a likely core point, flagging filler terms, and noting whether the text contains numbers or deadline cues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses rough local heuristics, so its verdicts and extracted points may be incomplete or misleading. <br>
Mitigation: Treat the output as a triage aid and review the original message before making decisions. <br>
Risk: Input text may be echoed or summarized in terminal output. <br>
Mitigation: Avoid processing highly sensitive messages unless terminal display of derived content is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1477009639zw-blip/bs-detector) <br>
- [Publisher profile](https://clawhub.ai/user/1477009639zw-blip) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis, Shell commands, Guidance] <br>
**Output Format:** [Terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads text from --text, --input, or standard input and prints a verdict, likely real point, sentence count, number presence, and deadline cue presence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
