## Description: <br>
Randomly generates one or more words from a curated database of 300 must-know College English Test Band 4 (CET-4) vocabulary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfeng1982](https://clawhub.ai/user/zfeng1982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and English learners use this skill to request random CET-4 vocabulary study entries from a bundled word list, including pronunciation, Chinese meaning, and example sentences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares shell access even though the visible behavior only requires reading a local word list. <br>
Mitigation: Install in environments where shell access is acceptable, or prefer a future version that removes or narrows the shell requirement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zfeng1982/cet4word300) <br>
- [Bundled CET-4 word list](artifact/word.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or structured text vocabulary entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Entries include word, phonetic spelling, Chinese meaning, English example sentence, and Chinese sentence translation.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
