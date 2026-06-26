## Description: <br>
Converts code files into MP3 music by analyzing code structure, mapping features to musical parameters, and sending a generated prompt and lyrics to the MiniMax music generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[besty0121](https://clawhub.ai/user/besty0121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to turn a selected source code file into a novelty or documentation-oriented MP3 code symphony based on line count, functions, indentation, keywords, strings, and comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code-derived metadata is sent to MiniMax for music generation. <br>
Mitigation: Use non-sensitive files and avoid proprietary code unless that disclosure is acceptable. <br>
Risk: The skill requires a MiniMax API key. <br>
Mitigation: Keep the API key in the MINIMAX_API_KEY environment variable and do not commit it to files or prompts. <br>
Risk: The generated MP3 is downloaded from a service-provided URL. <br>
Mitigation: Run the script in a trusted environment and review downloaded output before redistribution. <br>


## Reference(s): <br>
- [Code to Music on ClawHub](https://clawhub.ai/besty0121/code-to-music) <br>
- [MiniMax music generation API endpoint](https://api.minimaxi.com/v1/music_generation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown instructions with shell commands; generated MP3 file when the script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and sends code-derived music prompts and lyrics to MiniMax before downloading an MP3 from the returned audio URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
