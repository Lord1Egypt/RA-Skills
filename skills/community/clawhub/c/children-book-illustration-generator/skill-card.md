## Description: <br>
AI children's book illustration generator for creating whimsical storybook art, picture book pages, fairy tale scenes, and kids' story illustrations through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, self-publishing authors, teachers, parents, and KDP creators use this skill to generate children's book illustrations and related educational or nursery artwork from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Story prompts, reference image identifiers, and generation requests are sent to a third-party image service. <br>
Mitigation: Avoid private, regulated, or unpublished sensitive story material unless the provider is trusted for that use. <br>
Risk: The required Neta API token may be exposed if it is pasted directly into shared shell history, logs, or transcripts. <br>
Mitigation: Prefer environment variables or a secret store for the token and avoid sharing commands that reveal the credential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/children-book-illustration-generator) <br>
- [Neta API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands] <br>
**Output Format:** [Plain text image URL from a command-line workflow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a prompt, a Neta API token, optional size selection, and optional reference image UUID for style inheritance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
