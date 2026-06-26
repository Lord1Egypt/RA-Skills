## Description: <br>
FlyAI Flight Tracker helps agents query live FlyAI flight-search data to compare flight prices across date ranges and identify booking windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiejinsong](https://clawhub.ai/user/xiejinsong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-focused agents use this skill to track flight price trends, compare departure dates, and produce booking-oriented summaries from live FlyAI CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to install an unpinned global npm package. <br>
Mitigation: Install a reviewed, pinned FlyAI CLI version in a contained environment before enabling the skill, and do not allow autonomous global installation. <br>
Risk: Flight searches may share travel details with the FlyAI or Fliggy service. <br>
Mitigation: Inform users before sending itinerary details to the service and avoid submitting sensitive travel information unless it is required for the task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/flyai-flight-tracker) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be based on FlyAI CLI results and include detailUrl-based booking links when presenting travel options.] <br>

## Skill Version(s): <br>
v3.2.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
