## Description: <br>
Generates interactive Gaokao English vocabulary study webpages with frequency levels, mastery tags, wrong-word warnings, search, filters, and responsive dark-themed HTML output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xpscene-ux](https://clawhub.ai/user/xpscene-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and educators use this skill to generate local HTML and JavaScript vocabulary study pages for Chinese Gaokao English preparation. The generated page organizes words and phrases by exam frequency, mastery level, and review warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated vocabulary pages may contain inaccurate or unverified exam-frequency data if the source vocabulary list is incomplete or incorrect. <br>
Mitigation: Review the vocabulary source data for accuracy and provenance before sharing generated pages. <br>
Risk: The skill creates local HTML and JavaScript files that may be modified before distribution. <br>
Mitigation: Review generated files and scan them before deployment or publication. <br>


## Reference(s): <br>
- [HTML Template Structure](references/template_structure.md) <br>
- [Vocabulary Data Generator](scripts/generate_vocab.py) <br>
- [ClawHub Release Page](https://clawhub.ai/xpscene-ux/gaokao-english-vocabulary) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, JSONL, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local HTML page and vocab_data.js data file; generated study content should be reviewed for data accuracy before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
