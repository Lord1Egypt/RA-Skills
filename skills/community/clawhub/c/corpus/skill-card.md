## Description: <br>
Access a user's Corpus library from OpenClaw. Use when the user asks to search saved content, fetch item details, save links into Corpus, or create reminders from Corpus content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doninocode](https://clawhub.ai/user/doninocode) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, fetch, and summarize saved Corpus content, and to save URLs or create reminders in Corpus after user intent is clear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires CORPUS_API_TOKEN, which can grant access to a user's Corpus account if exposed. <br>
Mitigation: Keep CORPUS_API_TOKEN private, provide it through the skill environment, and never print or log the token. <br>
Risk: The skill can write to Corpus by saving URLs or creating reminders. <br>
Mitigation: Prefer read operations first and confirm user intent before write operations when the request is ambiguous. <br>
Risk: Changing CORPUS_API_BASE_URL could send requests and tokens to an untrusted endpoint. <br>
Mitigation: Use the default Corpus API base URL unless the alternate endpoint is explicitly trusted. <br>
Risk: Repository-edit plans based on Corpus content could introduce incorrect or unwanted changes. <br>
Mitigation: Review implementation plans and proposed file changes before confirming repository edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/doninocode/corpus) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/doninocode) <br>
- [Corpus homepage](https://github.com/zdonino/Corpus) <br>
- [Corpus AI iPhone app](https://apps.apple.com/us/app/corpus-ai/id6748364607) <br>
- [Corpus API service](https://corpusai.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CORPUS_API_TOKEN and python3; write actions are limited to saving URLs and creating reminders.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
