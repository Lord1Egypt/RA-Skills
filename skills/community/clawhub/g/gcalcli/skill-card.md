## Description:

Interact with Google Calendar via gcalcli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gargravish](https://clawhub.ai/user/gargravish)

### License/Terms of Use:


## Use Case:

Developers and calendar users use this skill to guide agents in viewing, searching, filtering, and exporting Google Calendar events and meeting attachments through gcalcli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run a remote gcalcli fork without pinning it to a reviewed commit.

Mitigation: Pin the fork to a reviewed commit or use an official release before installing or running the command.

Risk: Calendar events, meeting notes, recordings, chats, and shared document links can contain sensitive information.

Mitigation: Use the skill only with calendars and meeting artifacts the user is authorized to access, and avoid bulk exports unless explicitly approved.

Risk: The bulk export example uses a shell pipeline that includes sh -c argument handling.

Mitigation: Replace the pipeline with safer argument passing or a reviewed script before running exports at scale.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gargravish/skills/gcalcli)
- [Official gcalcli documentation](https://github.com/insanum/gcalcli)
- [Custom gcalcli fork with attachment support](https://github.com/shanemcd/gcalcli/tree/attachments-in-tsv-and-json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Markdown]

**Output Format:** [Markdown guidance with inline bash commands and JSON, TSV, and text output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides read-only calendar queries, attachment filtering, and optional export workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
