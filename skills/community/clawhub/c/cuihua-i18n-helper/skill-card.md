## Description: <br>
Cuihua i18n Helper helps agents extract translatable strings, generate locale JSON files, check translation coverage, and guide batch translation workflows for modern web applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supermario11](https://clawhub.ai/user/supermario11) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to internationalize React, Vue, Angular, Next.js, Nuxt.js, and JavaScript projects by extracting UI strings, creating locale files, checking translation completeness, and preparing translation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated locale files or proposed code changes may introduce incorrect strings, overwrite expected translation values, or leave untranslated content in target locales. <br>
Mitigation: Run the skill on a branch or after committing current work, then review generated locale and code diffs before merging. <br>
Risk: Batch translation workflows may send source strings to third-party translation providers. <br>
Mitigation: Do not translate secrets, customer data, unreleased copy, or sensitive internal strings through external providers unless that data sharing is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/supermario11/cuihua-i18n-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON examples, shell commands, and generated locale JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write locale files under the configured locales path and propose framework i18n changes for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
