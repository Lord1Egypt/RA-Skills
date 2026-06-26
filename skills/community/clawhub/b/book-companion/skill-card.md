## Description: <br>
书搭子 is a privacy-focused local reading companion agent that helps users discuss books, maintain reading notes, and receive supportive text responses from local profile and library files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-innopower](https://clawhub.ai/user/ai-innopower) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers use this skill inside an agent workspace to keep a local reading profile, discuss pasted book text, track reading progress, and receive emotion-aware reading support. It is suited to users who want a self-contained reading companion with editable local markdown records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reading history, emotional support preferences, trigger phrases, and profile details as plaintext local markdown. <br>
Mitigation: Keep the skill directory out of shared or synced folders when privacy matters, and use encrypted storage or manual deletion for sensitive records. <br>
Risk: Optional TTS can expose sensitive notes to a third-party service or run a user-specified command through BOOK_COMPANION_TTS_CMD. <br>
Mitigation: Leave TTS disabled for sensitive content, and only configure BOOK_COMPANION_TTS_CMD with a trusted command whose behavior has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-innopower/book-companion) <br>
- [Knowledge base](artifact/references/knowledge_base.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration guidance] <br>
**Output Format:** [Markdown conversational responses and local markdown records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local files under data/ when the hosting agent follows the skill instructions; optional voice output depends on user-configured TTS.] <br>

## Skill Version(s): <br>
2.0.7 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
