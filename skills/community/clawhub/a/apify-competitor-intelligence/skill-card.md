## Description: <br>
Analyze competitor strategies, content, pricing, ads, and market positioning across Google Maps, Booking.com, Facebook, Instagram, YouTube, and TikTok. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apify](https://clawhub.ai/user/apify) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to select Apify Actors, fetch actor input details, run competitor research scrapers with an APIFY_TOKEN, and summarize or export the results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Apify Actor runs use a user-provided token and may create long-running jobs or usage costs. <br>
Mitigation: Confirm the Actor, input JSON, result limits, and timeout before running, and monitor the Apify console for job status and cost. <br>
Risk: Exports may contain public contact, review, social, or business data gathered from third-party platforms. <br>
Mitigation: Handle exported data according to platform terms, privacy law, and organizational retention rules. <br>
Risk: Incorrect Actor IDs, malformed JSON, or unsafe filenames can cause failed runs or unintended output files. <br>
Mitigation: Validate Actor IDs, JSON input, result format, and output filenames before executing the provided commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/apify/apify-competitor-intelligence) <br>
- [Apify Homepage](https://apify.com) <br>
- [Apify Actor API Permission Lookup](https://api.apify.com/v2/acts/:actorId) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown guidance with bash command examples and optional CSV or JSON exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIFY_TOKEN, Node.js 20.6+, and mcpc; quick-answer mode displays top results in chat, while export mode writes CSV or JSON under the current working directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
