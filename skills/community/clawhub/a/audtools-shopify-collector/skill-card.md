## Description: <br>
AudTools Shopify Batch Collector reads category links from a CSV file and uses browser automation to submit them to AudTools with a product quantity of 9999 and a two-second interval between submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QirongZhang](https://clawhub.ai/user/QirongZhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and developers who use AudTools for Shopify collection workflows can use this skill to automate bulk submission of category URLs from a CSV file. It is intended for visible browser-driven collection runs where the user can log in manually and review the results before exporting data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk CSV submissions can send many URLs to AudTools and trigger unintended collection activity. <br>
Mitigation: Run a small CSV first, keep the browser visible, and confirm that every CSV URL is intended for submission before running the full batch. <br>
Risk: Dependency resolution may differ from the reviewed package-lock versions. <br>
Mitigation: Use locked installs so Playwright and csv-parser resolve to the versions captured in package-lock.json. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QirongZhang/audtools-shopify-collector) <br>
- [AudTools collection page](https://www.audtools.com/users/shopns#/users/shopns/collecs) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JavaScript automation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill runs a visible Playwright browser session, reads CSV input, may pause for manual login, and reports per-link progress in console output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
