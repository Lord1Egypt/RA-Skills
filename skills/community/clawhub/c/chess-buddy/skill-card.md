## Description: <br>
Stockfish-backed chess buddy for analyzing FEN positions and board images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommyclawd](https://clawhub.ai/user/tommyclawd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for chess position review, board-image-to-FEN workflows, best-move analysis, candidate lines, blunder review, and training explanations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local engine execution depends on a Stockfish binary installed on the user's machine. <br>
Mitigation: Install Stockfish from a trusted source, keep STOCKFISH_PATH under user control, and run the engine-check helper before relying on analysis. <br>
Risk: Board images and annotations can produce incorrect or ambiguous FEN positions. <br>
Mitigation: Verify board orientation, side to move, castling rights, en passant status, move counters, and annotation meaning before treating image-derived analysis as authoritative. <br>
Risk: Engine guidance can be misused for cheating in active human or rated games. <br>
Mitigation: Use the skill for post-game analysis, training, or general principles, and avoid assistance during active human or rated play. <br>


## Reference(s): <br>
- [Chess Buddy ClawHub page](https://clawhub.ai/tommyclawd/chess-buddy) <br>
- [Source package homepage](https://github.com/TommyClawd/chess-buddy-skill) <br>
- [Image to FEN workflow](references/image-to-fen.md) <br>
- [Output style](references/output-style.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with concise chess analysis, candidate lines, and caveats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local Stockfish helper commands and engine-backed move lines; image-derived positions should be verified before use.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
