## Description: <br>
Caches user-specified context fragments in a local file so agents can reuse them across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoxiang616](https://clawhub.ai/user/shaoxiang616) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to save recurring context fragments and preload them in later sessions, reducing repeated setup or prompting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved fragments may be loaded into future sessions and could persist sensitive or untrusted content. <br>
Mitigation: Do not cache secrets, credentials, or untrusted instructions unless persistent reuse is intentional. <br>
Risk: The clear-cache command removes the local cache directory. <br>
Mitigation: Run the clear-cache command only when intentionally deleting saved context fragments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaoxiang616/context-memoize-cache) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist user-provided fragments in a local cache file for later sessions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
