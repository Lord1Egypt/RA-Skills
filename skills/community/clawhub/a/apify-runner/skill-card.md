## Description: <br>
Run any Apify Actor to scrape web data, including Actor discovery, quality filtering, probe testing, batched execution, and result collection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duxj4520](https://clawhub.ai/user/duxj4520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to select and run Apify Actors for web or social media scraping tasks, including probe runs, batching, and result collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run third-party Apify scraping Actors with a user token and send target data to Apify. <br>
Mitigation: Use APIFY_TOKEN or a protected config file, confirm the selected Actor and target list, and start with probe-only or small-batch runs before full execution. <br>
Risk: Runs may consume paid Apify capacity or scrape sensitive targets. <br>
Mitigation: Confirm the Actor pricing model, batch size, output path, and target sensitivity before full runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duxj4520/apify-runner) <br>
- [Apify Store API](https://api.apify.com/v2/store) <br>
- [Apify API base](https://api.apify.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON; result data may be saved as JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report selected Actors, probe status, item counts, batch counts, failures, and output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
