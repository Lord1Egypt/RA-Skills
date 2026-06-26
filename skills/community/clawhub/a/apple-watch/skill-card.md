## Description: <br>
Apple Watch Health Sync helps agents set up, query, and troubleshoot Apple Watch health data synchronization through the Health Auto Export app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LainNet-42](https://clawhub.ai/user/LainNet-42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to configure a local Apple Watch health-data pipeline, query recent metrics, view a dashboard, and troubleshoot sync between Health Auto Export and a PC or Mac. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data through a persistent local server with network exposure and stored records. <br>
Mitigation: Run it only on a trusted private network, protect the API key, limit selected health metrics, and define how to stop the service and delete stored data. <br>
Risk: The setup flow may configure long-running background services or startup tasks. <br>
Mitigation: Review persistence settings before enabling them, avoid unnecessary elevated privileges, and remove the service when health syncing is no longer needed. <br>
Risk: The setup script can install dependencies and download upstream reference files. <br>
Mitigation: Inspect the setup script before running it, use a dedicated directory or virtual environment, and confirm network downloads are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LainNet-42/apple-watch) <br>
- [Health Auto Export app](https://apps.apple.com/us/app/health-auto-export-json-csv/id1115567069) <br>
- [Health Auto Export server reference](https://github.com/HealthyApps/health-auto-export-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated Python/HTML/JSON files, REST query examples, and health-data summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and may create a local server, dashboard, API key configuration, phone templates, and append-only health data files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
