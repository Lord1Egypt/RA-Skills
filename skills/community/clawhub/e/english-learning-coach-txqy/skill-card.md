## Description: <br>
English Learning Coach turns an agent into an English practice partner that checks learner messages, routes flawed English to correction-only responses, adapts reply difficulty, and summarizes learning progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taxueqinyin](https://clawhub.ai/user/taxueqinyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External English learners use this skill for conversation practice, correction-only feedback, active vocabulary tracking, CEFR-level estimates, and short review or quiz sessions. Agents use it to keep ordinary chat immersive while recording learning signals locally when persistence is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may keep a local learning history that includes exact practice sentences, corrections, learner profile data, vocabulary records, and quiz checkpoints. <br>
Mitigation: Use a safe data directory, avoid personal or sensitive practice topics, and inspect or delete generated data files when retention is not desired. <br>
Risk: Learning data can be stored silently during normal use, which may surprise users who expect conversation-only behavior. <br>
Mitigation: Review the storage behavior before use and configure ENGLISH_LEARNING_COACH_DATA_DIR when the default skill-local data directory is not appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taxueqinyin/english-learning-coach-txqy) <br>
- [Publisher profile](https://clawhub.ai/user/taxueqinyin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown responses with correction blocks, summaries, quizzes, level guidance, and optional shell commands for local persistence.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Correction-only replies use Correction, Reason, and optional Natural version fields; persistence can produce local JSON, JSONL, and Markdown learning records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
