## Description: <br>
Stash and recall short text snippets in a local file-backed clipboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and other users use this skill to save short notes or quotes in a local scratch clipboard and retrieve them later in the same workspace without a database or external service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved snippets may remain in plaintext in the local cache file after the session. <br>
Mitigation: Use only for non-sensitive notes or quotes, avoid passwords, tokens, private keys, and personal data, and clear or delete the cache file when the stash is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/clipboard-stash-demo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local plaintext TSV entries at ~/.cache/clipboard-stash/stash.tsv.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
