## Description:

AI News Pusher helps an agent fetch AI industry news from RSS, Tavily, and Brave sources, score items for product relevance, manage review queues, and optionally push selected updates to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kern1x](https://clawhub.ai/user/kern1x)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to automate AI news collection, triage high-value items, review borderline items, and prepare or send Feishu updates. It supports API-backed news search when credentials are provided and RSS-only operation when no news-source API key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch content from external news services and optionally send article content to an LLM provider for scoring.

Mitigation: Use only trusted API credentials and review provider data handling requirements before enabling LLM scoring.

Risk: The Feishu webhook and API keys are sensitive credentials that could expose posting permissions or paid services if shared.

Mitigation: Store credentials in environment variables, use a dedicated Feishu webhook, keep keys out of shared environments, and rotate them if exposed.

Risk: Automated pushing can distribute incorrect, low-quality, or unwanted news items.

Mitigation: Run in dry-run mode first, review gray-zone items manually, and tune scoring thresholds before routine use.

Risk: The skill stores local JSON history and feedback data that may include article content and review notes.

Mitigation: Keep the local data directory private and clear stored history when it is no longer needed.

Risk: Unpinned dependencies can change behavior over time.

Mitigation: Pin dependency versions before production use and re-test news fetching, scoring, storage, and Feishu delivery after upgrades.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, plain text, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON history and feedback files, and may send formatted news content to Feishu when a webhook is configured.]

## Skill Version(s):

2.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
