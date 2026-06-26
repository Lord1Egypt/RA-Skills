## Description: <br>
Batch-adds, checks, and annotates American English IPA pronunciations for English word lists, with text, Markdown, and CSV output options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pe1984](https://clawhub.ai/user/pe1984) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and vocabulary maintainers use this skill to batch annotate English word lists with American IPA pronunciations, verify or repair existing phonetic entries, and export formatted vocabulary files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vocabulary terms are sent to dictionaryapi.dev during lookup. <br>
Mitigation: Use non-sensitive word lists, avoid confidential vocabulary, and review whether the public API is appropriate for the data being processed. <br>
Risk: The script writes results to a user-selected output file. <br>
Mitigation: Choose a separate output path when preserving the original input file matters. <br>


## Reference(s): <br>
- [Usage Examples](references/usage-examples.md) <br>
- [API Notes & IPA Reference](references/api-notes.md) <br>
- [Free Dictionary API](https://dictionaryapi.dev/) <br>
- [ClawHub skill page](https://clawhub.ai/pe1984/english-phonetics-batch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python examples; generated agent workflows produce text, Markdown, or CSV vocabulary files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include word, American IPA phonetic transcription, part of speech, and validity status where supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
