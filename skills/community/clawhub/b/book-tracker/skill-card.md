## Description: <br>
Tracks reading progress, notes, ratings, themes, and what to read next for users who want to remember and build on what they read. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rednix](https://clawhub.ai/user/rednix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain a private reading log, capture notes and reflections, manage current and future books, and receive reading recommendations based on preferences, ratings, and recent themes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a persistent private reading log with notes, ratings, quotes, and recommendations. <br>
Mitigation: Install only if you are comfortable keeping that reading history, and surface reading lists or notes only in the owner's private channel. <br>
Risk: Broad activation phrases could lead the agent to suggest book-tracking actions when the user did not intend to update their library. <br>
Mitigation: Prefer explicit /book commands for adding, changing, or viewing entries, and require user confirmation before modifying the library or reading list. <br>
Risk: Quotes or key ideas may be offered for reuse in a knowledge base. <br>
Mitigation: Approve knowledge-base additions only for notes or quotes the user wants reused later. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rednix/book-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/rednix) <br>
- [ClawHub metadata homepage](https://clawhub.com/skills/book-tracker) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown and plain text reading logs, reflections, recommendations, theme summaries, and command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains persistent private reading state in library, reading-list, and configuration files; entries and knowledge-base additions should be made only with explicit user instruction or confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
