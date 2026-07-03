## Description: <br>
Runs a short end-of-day debrief that reflects on the user's day, extracts action items and open loops, previews tomorrow, and stores the result in Fulcra as a structured annotation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keng009](https://clawhub.ai/user/keng009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fulcra users use this skill with an agent to run a short evening reflection, compare the day against calendar and morning check-in context, and save ratings, meeting feedback, wins, open loops, and action items for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Fulcra calendar, check-in, and reflection data that may be personal. <br>
Mitigation: Install only when the publisher is trusted with this data, use least-privilege Fulcra tokens, and avoid sharing day ratings or calendar details publicly. <br>
Risk: The package includes broader account and CRM helpers than the evening debrief workflow requires. <br>
Mitigation: Review the package before deployment and remove or disable unused Attio and generic delete/update helpers when they are not needed. <br>
Risk: Fulcra API and CLI settings affect where the skill sends requests and how credentials are used. <br>
Mitigation: Pin Fulcra API and CLI configuration to trusted values before running the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/keng009/skills/fulcra-evening-debrief) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Fulcra annotation payload containing fields such as day_rating, meeting_count, wins, open_loops, and action_items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
