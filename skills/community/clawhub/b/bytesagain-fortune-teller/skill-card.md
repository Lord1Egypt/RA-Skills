## Description: <br>
Draw tarot cards, cast I Ching hexagrams, and check daily fortunes for fun when pulling spreads, casting hexagrams, or playing fortune games. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill for entertainment-oriented fortune readings such as tarot, I Ching, daily luck, zodiac, numerology, and palmistry prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports suspicious behavior because the runtime includes broader local data-management behavior with persistent logging and export features. <br>
Mitigation: Review the skill before installing, run it in a constrained environment, and avoid entering sensitive personal information. <br>
Risk: Artifact behavior can store command history and user-provided entries on disk. <br>
Mitigation: Set FORTUNE_TELLER_DIR to a disposable directory and delete that directory after testing if persistence is not desired. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command behavior may write local history or exported data under FORTUNE_TELLER_DIR or ~/.local/share/fortune-teller/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
