## Description: <br>
Plan and coordinate events in Discord. Use when users ask to create, schedule, or manage events, plan meetups, organize activities, set up reminders, or track RSVPs in Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Discord community managers and event organizers use this skill to plan events, track RSVP status, and manage local event records. The included script provides command-line event creation, listing, RSVP updates, details, and cancellation backed by an events.json file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill wording suggests Discord scheduling and reminders, but server security evidence says the artifact is a local event tracker and does not create Discord events, post reminders, notify attendees, or enforce Discord permissions. <br>
Mitigation: Present generated commands and guidance as local event-management support only; verify Discord-facing actions separately before relying on them. <br>
Risk: Event data is stored in a local events.json file. <br>
Mitigation: Run the script from a trusted working directory, keep events.json under appropriate access controls, and review event IDs before canceling records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fuzzyb33s/discord-event-planner-fuzzy) <br>
- [Publisher Profile](https://clawhub.ai/user/fuzzyb33s) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and local JSON file behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local events.json file when the bundled event_manager.py script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
