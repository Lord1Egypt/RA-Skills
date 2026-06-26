## Description: <br>
Evaluate an Audible daily promotion against Goodreads public score, optional Goodreads CSV shelves, optional freeform reading notes, optional delivery rules, and manual Want-to-Read discount scans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lenpr](https://clawhub.ai/user/lenpr) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Readers and OpenClaw users use this skill to evaluate Audible deals against public Goodreads ratings, their Goodreads shelves, and optional reading preference notes. It can also produce on-demand Want-to-Read discount audits and route selected results to configured delivery channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Audible authentication stores durable account tokens and extra account/device data in a local auth file. <br>
Mitigation: Use the unauthenticated workflow unless member-visible prices are important; if authentication is enabled, keep the auth file out of shared, synced, or backed-up folders. <br>
Risk: The skill may read local Goodreads exports, preference notes, generated artifacts, caches, and state files. <br>
Mitigation: Point configured paths only at files intended for this workflow, and use the public-data or minimal-privacy path when personal context should not be used. <br>
Risk: Configured delivery channels and cron jobs can send or schedule results automatically. <br>
Mitigation: Review delivery targets before enabling sends, and enable cron only when scheduled runs are desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lenpr/audible-goodreads-deal-scout) <br>
- [Publisher profile](https://clawhub.ai/user/lenpr) <br>
- [Project homepage](https://github.com/lenpr/audible-goodreads-deal-scout) <br>
- [Trust and Data Access](artifact/TRUST.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON runtime payloads, Markdown reports, setup guidance, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local config, state, cache, report, and delivery artifacts in the configured workspace storage directory.] <br>

## Skill Version(s): <br>
0.1.14 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
