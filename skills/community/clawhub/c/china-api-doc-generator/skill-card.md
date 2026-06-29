## Description: <br>
Generate API documentation in Chinese technical writing style for Chinese developer audiences, including RESTful API documentation, WeChat and Alipay-style platform docs, SDK examples, error code systems, signature authentication docs, and changelog or migration guides. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lm203688](https://clawhub.ai/user/lm203688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to produce Chinese-market API documentation with platform-style structure, detailed error codes, multi-language SDK examples, signature authentication guidance, and migration notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation may default to Chinese-market conventions such as Beijing time, signature authentication, or Chinese platform documentation style when another convention is needed. <br>
Mitigation: Prompt explicitly for the desired language, timezone, authentication convention, and documentation style when they differ from the skill defaults. <br>
Risk: API documentation examples may describe tokens, app secrets, or signature flows and could accidentally include real credentials if supplied by the user. <br>
Mitigation: Use placeholders in generated examples and review outputs before publishing to ensure no sensitive credentials are included. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lm203688/china-api-doc-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown documentation with tables and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-facing API documentation templates, SDK examples, error code tables, authentication documentation, and changelog or migration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
