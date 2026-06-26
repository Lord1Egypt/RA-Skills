## Description: <br>
Chou Fei helps agents fetch external resources, extract useful information from content, and allocate compute handling based on task priority and load. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lt8899789](https://clawhub.ai/user/lt8899789) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to route resource-ingestion tasks, summarize or extract key points from supplied content, and receive lightweight allocation guidance for processing requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resource fetching and content processing may expose sensitive URLs, API targets, or files to the host agent workflow. <br>
Mitigation: Use the skill only with resources you are permitted to process, and avoid private or credential-bearing targets unless the host execution path has been reviewed. <br>
Risk: Broad resource-ingestion wording can make the expected execution boundary unclear. <br>
Mitigation: Review host permissions and execution behavior before deployment, especially for URL, file, and API-style inputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lt8899789/chou-fei) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON objects and streamed text, with command examples in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch results are truncated to 500 characters in the script; streaming helpers emit typed progress chunks.] <br>

## Skill Version(s): <br>
1.0.35 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
