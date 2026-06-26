## Description: <br>
Extract summaries from all documents in a Feishu folder by recursively scanning wiki or drive folders, reading documents and sub-documents, and generating a comprehensive Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henryjing96](https://clawhub.ai/user/henryjing96) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to summarize accessible Feishu wiki spaces or drive folders into one structured report with a directory tree, per-document summaries, status counts, and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the selected Feishu folder and reachable subdocuments, which may combine sensitive, confidential, or mixed-permission content into a single summary. <br>
Mitigation: Run it only on Feishu folders the user intends to summarize together, and review folder permissions and report contents before sharing the generated Markdown. <br>


## Reference(s): <br>
- [Feishu API Reference](references/feishu_api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source URL, generation timestamp, document counts, directory structure, hierarchical summaries, status statistics, and links to original documents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
