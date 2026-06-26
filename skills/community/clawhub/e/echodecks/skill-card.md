## Description: <br>
EchoDecks integrates with the EchoDecks API for flashcard management, spaced repetition study sessions, AI card generation, and podcast generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drgeld](https://clawhub.ai/user/drgeld) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Learners, educators, and agents use this skill to list decks, retrieve due flashcards, submit review ratings, generate new cards from a topic or text, and create or retrieve deck-based podcasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decks, notes, and source text submitted through the skill may contain confidential or regulated material. <br>
Mitigation: Avoid submitting confidential or regulated content to EchoDecks unless the deployment is approved for that data. <br>
Risk: The skill uses an EchoDecks API key for authenticated requests. <br>
Mitigation: Use a revocable or scoped API key when available and rotate it if exposure is suspected. <br>
Risk: Review submissions and generation actions can change study state or spend credits. <br>
Mitigation: Instruct the agent to ask before submitting reviews or spending credits on card or podcast generation. <br>


## Reference(s): <br>
- [EchoDecks ClawHub listing](https://clawhub.ai/drgeld/echodecks) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ECHODECKS_API_KEY and may submit review data or spend generation credits when directed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
