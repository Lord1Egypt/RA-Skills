## Description: <br>
Generates B2B/B2C leads by scraping Google Maps, websites, Instagram, TikTok, Facebook, LinkedIn, YouTube, and Google Search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apify](https://clawhub.ai/user/apify) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, growth, and research teams use this skill to select an Apify Actor, configure a lead-generation scrape, and produce lead results for outreach or enrichment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scraping-based lead generation can collect contact data that may be governed by platform terms, privacy law, and outreach rules. <br>
Mitigation: Before each run, confirm the target source, data scope, result limit, intended use, and legal basis for using scraped contact data. <br>
Risk: Runs consume an Apify account token and may incur platform costs or expose broader account access than needed. <br>
Mitigation: Use a least-privilege APIFY_TOKEN where possible, confirm the selected Actor and cost before execution, and avoid sharing the token in prompts or output files. <br>
Risk: The skill can write lead exports locally, which may create sensitive sales or contact datasets. <br>
Mitigation: Choose a clear output destination, keep filenames within the working directory, and review exported CSV or JSON files before sharing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/apify/apify-lead-generation) <br>
- [Apify](https://apify.com) <br>
- [Apify Actor API](https://api.apify.com/v2/acts/:actorId) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown instructions with bash command blocks; optional CSV or JSON result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can display a quick answer in chat or save full Apify Actor results as CSV or JSON in the current working directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
