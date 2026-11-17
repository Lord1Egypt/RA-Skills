## Description:

EFT analyzes AI agent responses in real time, assigning 10 emotion labels with per-sentence metrics, narrative arc detection, and explanatory output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marceloadryao](https://clawhub.ai/user/marceloadryao)

### License/Terms of Use:


## Use Case:

Developers, AI safety teams, and operators use EFT to monitor emotional patterns, drift, and narrative arcs in AI agent outputs through Clawdbot hooks, a local dashboard, and JSON API endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent responses are automatically analyzed and response-derived text is stored in a local JSONL history.

Mitigation: Use the skill only for workloads where local logging is acceptable, configure a trusted log path, and define retention or deletion controls before deployment.

Risk: History and latest-analysis data are exposed through unauthenticated local HTTP endpoints.

Mitigation: Restrict gateway access to trusted users or local-only networks and add authentication before exposing the dashboard or API beyond a controlled environment.

Risk: Wildcard CORS can make local API data easier to read from other browser contexts.

Mitigation: Remove wildcard CORS or limit it to trusted origins before using the skill with sensitive agent outputs.

Risk: Configurable engine and log paths affect what local code is executed and where records are written.

Mitigation: Set enginePath and logPath to trusted, reviewed locations and avoid user-writable paths shared with untrusted processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marceloadryao/skills/enginemind-eft)
- [EFT documentation](artifact/EFT_DOCUMENTATION.md)
- [EFT scientific evidence and market research](artifact/EFT_SCIENTIFIC_EVIDENCE.md)
- [Affective Computing in the Era of Large Language Models](https://arxiv.org/abs/2408.04638)
- [Integrated Information Theory 4.0](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011465)
- [The narrative arc](https://www.science.org/doi/abs/10.1126/sciadv.aba2196)
- [GoEmotions](https://arxiv.org/abs/2005.00547)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Files, Dashboard, API responses]

**Output Format:** [JSON analysis records, JSONL log entries, and HTML dashboard views]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python >=3.10 and a local emotion_engine.py/consciousness_rs runtime configured through Clawdbot.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
