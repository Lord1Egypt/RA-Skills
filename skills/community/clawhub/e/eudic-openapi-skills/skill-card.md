## Description: <br>
Provides Eudic OpenAPI guidance for managing vocabulary lists, user corpus entries, notes, and related word data across Eudic, French Assistant, German Assistant, and Spanish Assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lulu-trans](https://clawhub.ai/user/lulu-trans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Eudic OpenAPI calls for querying, adding, renaming, and deleting vocabulary books, words, notes, and corpus records with a user-provided API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user API token to access Eudic account data. <br>
Mitigation: Keep the token private, avoid logging or pasting it into shared contexts, and provide it only when an operation requires authenticated access. <br>
Risk: Rename, bulk add, and delete operations can change vocabulary books, words, notes, or corpus-related records. <br>
Mitigation: Review the exact target language, IDs, words, and operation type before running any modifying request. <br>
Risk: Vocabulary notes and corpus content may include personal information. <br>
Mitigation: Inspect returned notes and corpus entries before sharing them outside the user's private context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lulu-trans/eudic-openapi-skills) <br>
- [Eudic OpenAPI authorization](https://my.eudic.net/OpenAPI/Authorization) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with curl examples, endpoint descriptions, and parameter notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Eudic OpenAPI token and language selection for en, fr, de, or es.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
