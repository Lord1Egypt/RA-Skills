## Description: <br>
Search Airbnb listings, filter short-term rentals, and analyze detail pages for parking, basement, and renovation signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suidge](https://clawhub.ai/user/suidge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Airbnb listings by date, guest count, coordinate area, price, bedrooms, rating, and distance, then compare shortlists. It supports listing detail review for parking, basement, and renovation signals when login-only data is not required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface rentals and prices that may influence booking or purchase decisions. <br>
Mitigation: Require user review and explicit confirmation before any booking, payment, or purchase action. <br>
Risk: Detail keyword matches for parking, basement, and renovation are signals, not verified listing facts. <br>
Mitigation: Verify important amenities and property characteristics against the live listing or host before relying on them. <br>
Risk: The setup script installs third-party Python dependencies and the search/detail scripts make network requests to Airbnb-related services. <br>
Mitigation: Review commands before running them, use an isolated virtual environment, and avoid providing credentials or cookies unless intentionally required. <br>


## Reference(s): <br>
- [Airbnb Agent Skill Page](https://clawhub.ai/suidge/airbnb-agent) <br>
- [Airbnb API Fields Reference](references/api-fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes filtered candidates to /tmp/airbnb_candidates.json and detail analysis to /tmp/airbnb_results.json by default.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
