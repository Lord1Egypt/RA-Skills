## Description: <br>
Routes natural-language questions into a three-book answer experience and returns one random cited answer with SQLite-backed minimal per-user memory, duplicate-question protection, contextual book switching, and daily fortune. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaozrrr](https://clawhub.ai/user/shaozrrr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask conversational questions and receive a short cited answer drawn from built-in movie, literature, or music quote collections. Developers can also run, extend, and debug the pure text skill locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the latest user question and answer in a local SQLite database for duplicate detection and contextual book switching. <br>
Mitigation: Avoid highly sensitive questions, relocate the database with ANSWER_LIBRARY_DB when needed, or delete the local database after use. <br>
Risk: Answers are randomly selected from quote libraries and should not be treated as factual, professional, legal, medical, or financial advice. <br>
Mitigation: Use responses as reflective prompts only and rely on appropriate qualified sources for consequential decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaozrrr/book-of-answers-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text conversational response with cited source line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are selected from a built-in three-book quote corpus and may use local SQLite state for duplicate detection and contextual book switching.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
