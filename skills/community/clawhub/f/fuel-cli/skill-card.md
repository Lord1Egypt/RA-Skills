## Description: <br>
UK fuel prices CLI - find nearby stations by postcode or coordinates, get station details, ranked by price/distance/freshness, and agent-friendly JSON envelopes with `--output <path>` for field projection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shan8851](https://clawhub.ai/user/shan8851) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent install and operate the `fuel` CLI for UK petrol and diesel price lookups, nearby station search, station detail retrieval, and structured result projection. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-style Fuel Finder credentials and a sensitive client secret for live data refreshes. <br>
Mitigation: Keep `FUEL_FINDER_CLIENT_SECRET` out of source control and provide it through a secure environment or credential store. <br>
Risk: The skill installs and invokes the third-party npm package `@shan8851/fuel-cli` globally. <br>
Mitigation: Verify the npm package and source before installation, and install only when the agent is expected to perform UK fuel-price lookups. <br>
Risk: Fuel-price data can be stale, missing timestamps, or affected by excluded test stations. <br>
Mitigation: Review the skill's data-quality advisories, freshness counts, and excluded test-station counts before relying on ranked results. <br>


## Reference(s): <br>
- [Fuel CLI homepage](https://fuel-cli.xyz) <br>
- [UK Fuel Finder service](https://www.fuel-finder.service.gov.uk) <br>
- [Fuel CLI on ClawHub](https://clawhub.ai/shan8851/fuel-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON field examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to produce text or JSON CLI output, including success and error envelopes and optional field projections.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
