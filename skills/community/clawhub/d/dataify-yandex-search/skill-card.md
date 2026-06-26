## Description: <br>
This skill helps an agent search Yandex through Dataify's API with a preview-and-confirm workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Yandex search requests, preview parameters with documented defaults, obtain user confirmation, and return the Dataify API response directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passing the Dataify API token on the command line can expose it through shell history or process listings. <br>
Mitigation: Set DATAIFY_API_TOKEN in the environment and avoid using the --token command-line argument when running the bundled script. <br>
Risk: Search queries and selected options are sent to Dataify's API. <br>
Mitigation: Avoid submitting sensitive or confidential queries unless the user has approved that external API use. <br>


## Reference(s): <br>
- [Dataify Yandex Search on ClawHub](https://clawhub.ai/dataify-server/dataify-yandex-search) <br>
- [Dataify publisher profile](https://clawhub.ai/user/dataify-server) <br>
- [Dataify Yandex Search API Fields](references/api_fields.md) <br>
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API responses] <br>
**Output Format:** [Markdown preview tables, shell command invocations, and raw Dataify API response text in JSON or HTML formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided search query and a Dataify API token; the skill instructs the agent to show parameters before any API call.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
