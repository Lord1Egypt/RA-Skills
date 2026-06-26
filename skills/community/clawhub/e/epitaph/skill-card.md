## Description: <br>
Scans a user's logged-in social media accounts and distills posts, saves, unfinished plans, interests, and cross-platform patterns into a poetic, data-driven digital epitaph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sophie-xin9](https://clawhub.ai/user/sophie-xin9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users working with an AI agent use this skill to inspect their own selected social media accounts and generate a humorous, reflective Markdown summary of their digital footprint. It is intended for self-reflection, shareable personality summaries, and reviewing patterns such as unfinished reading lists, hidden interests, multi-platform personas, and activity timelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect logged-in social accounts, including saves, likes, favorites, follows, comments, ratings, and posts. <br>
Mitigation: Use it only on accounts and platforms the user intentionally selects, and prefer a separate browser profile for collection. <br>
Risk: Generated summaries and raw collected data can reveal private preferences or account history. <br>
Mitigation: Review the raw output before sharing, and delete epitaph-data/ after use if retained local history is not desired. <br>
Risk: The workflow depends on ManoBrowser browser automation and may prompt dependency setup. <br>
Mitigation: Approve ManoBrowser setup manually and confirm the browser connection before allowing collection. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sophie-xin9/epitaph) <br>
- [Artifact README](artifact/README.md) <br>
- [Epitaph output template](artifact/templates/epitaph_template.md) <br>
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown digital epitaph with optional local JSON raw data files and setup commands for browser automation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may save raw social account data and generated epitaph files under epitaph-data/ for local review.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
