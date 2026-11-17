## Description:

Guided academic paper writing: IMRaD section drafting, citation lookup from Zotero, iterative revision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanbastias](https://clawhub.ai/user/juanbastias)

### License/Terms of Use:

MIT-0

## Use Case:

Academic authors use this skill to collect manuscript context, find verified Zotero or PubMed citations, and draft or revise IMRaD sections, abstracts, and reference lists with an iterative review workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Zotero searches and PubMed or API lookups can reveal research topics or library contents.

Mitigation: Install only in the intended JD workspace, avoid exposing sensitive research topics, and use a least-privilege Zotero key.

Risk: The workflow can propose changes to a Zotero library through add-doi operations.

Mitigation: Require a preview and explicit confirmation before any command that changes the Zotero library.

Risk: Shell command templates accept user-provided search terms, DOIs, and collection names.

Mitigation: Use structured tool calls or argument arrays, and quote or escape user input before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juanbastias/skills/academic-paper-writer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown prose with citations, reference lists, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Vancouver or APA citation formatting and follow-up revision prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
