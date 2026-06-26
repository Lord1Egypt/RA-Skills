## Description: <br>
Boggle Solver finds valid English and German words on a 4x4 Boggle grid using dictionary-based trie search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianhaberl](https://clawhub.ai/user/christianhaberl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to solve Boggle boards from typed grids or confirmed photo transcriptions, with English and German results presented separately. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads large dictionary text files from GitHub on first use and caches them locally. <br>
Mitigation: For offline or high-integrity environments, preinstall and review the dictionaries, and consider pinning or verifying their hashes before use. <br>
Risk: Incorrect transcription of a board photo can produce valid-looking results for the wrong grid. <br>
Mitigation: Show the extracted 4x4 grid to the user and solve only after the user confirms it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/christianhaberl/boggle) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Dictionary data](https://github.com/christianhaberl/boggle-openclaw-skill/tree/main/data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown text with shell command examples and optional JSON solver output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results can be grouped by word length with Boggle scores; JSON output includes board, words, total score, and solve time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
