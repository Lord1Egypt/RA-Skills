## Description: <br>
Fortune Telling Bazi calculates local BaZi birth charts, stores multiple profiles, and provides active-user or joint analysis summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youhan2021](https://clawhub.ai/user/youhan2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using ClawHub agents can use this skill to enter birth details, generate local BaZi summaries, manage saved profiles, and compare multiple profiles in a joint analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores names, birth dates and times, gender, and derived fortune summaries locally for reuse. <br>
Mitigation: Install only when users are comfortable storing that data locally, avoid entering another person's data without consent, and remove saved profiles when they are no longer needed. <br>
Risk: Saved active profiles can be included in later chat context, which may expose personal birth-profile data in shared sessions. <br>
Mitigation: Use the stop, deactivate, or remove commands when finished, and avoid using the skill in shared chat sessions where stored profiles could be shown unexpectedly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youhan2021/fortune-telling-bazi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-like chat text with local command output and JSON-backed profile state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local profile and active-user data in data/users.json and data/active.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
