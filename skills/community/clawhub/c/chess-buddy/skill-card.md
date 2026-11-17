## Description:

Stockfish-backed chess buddy for analyzing FEN positions and board images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommyclawd](https://clawhub.ai/user/tommyclawd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill for chess position review, FEN validation, board-image interpretation, best-move analysis, candidate lines, blunder review, and training explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs python3 and a local Stockfish executable for chess analysis.

Mitigation: Install only in environments where local helper execution is acceptable, verify Stockfish availability, and keep analysis depth or time limits modest.

Risk: Untrusted or malformed FEN strings can affect local engine calls or produce misleading results.

Mitigation: Avoid FEN strings with embedded control characters and validate that each FEN has six fields before engine analysis.

Risk: Image-derived board states and annotations can be ambiguous.

Mitigation: Verify board orientation, side to move, castling rights, en passant state, move counters, and annotation meaning before treating analysis as authoritative.

Risk: Engine-backed move recommendations could enable cheating in active human games or rated online play.

Mitigation: For active games, provide only general principles or post-game analysis rather than concrete engine moves.

## Reference(s):

- [Image to FEN Workflow](references/image-to-fen.md)
- [Output Style](references/output-style.md)
- [ClawHub Skill Page](https://clawhub.ai/tommyclawd/skills/chess-buddy)
- [Project Homepage](https://github.com/TommyClawd/chess-buddy-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Concise Markdown with optional shell commands and Stockfish analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate FEN strings, principal variations, evaluation scores, human-readable plans, and uncertainty notes.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
