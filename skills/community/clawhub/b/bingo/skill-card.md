## Description: <br>
Generate and play bingo cards with number calling and verification. Use when running bingo games. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People running casual bingo games use this skill to generate bingo cards, draw numbers, manage local call history, view stats, and check submitted numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Winner checking is a placeholder and should not be treated as fair-play or winner validation. <br>
Mitigation: Use it only for casual local play unless the script is reviewed or fixed to perform real win verification. <br>
Risk: Accurate call history is important for organized games, and the skill stores local state under ~/.local/share/bingo. <br>
Mitigation: Review the local state before game use and verify call-history behavior before relying on it for organized play. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/bingo) <br>
- [BytesAgain Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text command output and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local state under ~/.local/share/bingo for game history and stats.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
