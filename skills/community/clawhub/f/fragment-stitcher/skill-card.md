## Description: <br>
碎片知识缝纫师 helps agents collect scattered notes, files, screenshots, and web content, discover relationships with an existing local knowledge base, create connection notes, and draft outlines when a topic has enough fragments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TeamoPlum](https://clawhub.ai/user/TeamoPlum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn scattered personal or project knowledge into structured local notes, relationship summaries, and outline drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided notes, files, screenshots, or web content may be retained in the local knowledge base. <br>
Mitigation: Avoid adding secrets, credentials, regulated data, or private chats unless local retention is intended, and periodically review or delete generated knowledge files. <br>


## Reference(s): <br>
- [Fragment Metadata Fields](references/fields.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/TeamoPlum/fragment-stitcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown notes, JSON-like structured fragment records, Python API examples, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores user-provided knowledge locally when a knowledge base path or default knowledge directory is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
