## Description: <br>
Scrape any webpage using text-based DOM manipulation and export structured data to CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[science-prof-robot](https://clawhub.ai/user/science-prof-robot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to explore complex webpages, resolve ambiguous data extraction choices, and save structured scraping results to CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local browser-control bridge is unauthenticated and exposes browser session actions. <br>
Mitigation: Run it only in a trusted local environment, stop it when finished, and prefer a version with authentication or localhost-only controls. <br>
Risk: The bridge can execute page JavaScript during scraping. <br>
Mitigation: Use the skill only on sites you are authorized to scrape and review requested actions before executing them. <br>
Risk: The skill describes login flows that could involve sensitive credentials. <br>
Mitigation: Avoid pasting passwords into chat and abort workflows that require credentials unless an approved handling process is in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/science-prof-robot/auto-scraping-to-csv) <br>
- [Project homepage](https://github.com/Science-Prof-Robot/autoclick) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with CSV file output and optional code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a scraping summary, user-confirmed extraction choices, sample rows, and the generated CSV path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
