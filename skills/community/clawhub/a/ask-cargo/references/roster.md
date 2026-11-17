# Roster

Which deployed agent owns which job, so Ask Cargo hands a request to the agent whose rules already
cover it instead of redoing it. The prompt in `infra/agents/ask-cargo.prompt.ts` reads this file;
`cargo-ai ai agent list` is the live truth, and when the two disagree the live list wins.

Fill it from `cargo-ai ai agent list` at install time, and update it in the same pull request that
deploys a new agent. One row per agent. Leave out agents Ask Cargo should never wake.

| Agent (as listed)  | Owns                                                   | Hand it                                   | Never hand it                          |
| ------------------ | ------------------------------------------------------ | ----------------------------------------- | -------------------------------------- |
| `standup`          | the daily recap: cadence log, PR, Slack digest         | "run today's standup now"                 | a question about yesterday: read the log |
| `weekly_planning`  | the Monday ranking of work against initiatives         | "re-run the weekly plan"                  | "what should I do today": answer it    |
| `account_scorer`   | account scores and tiers against the ICP, CRM write-back | "re-score acme.com", a short domain list | the whole book: that is a batch, propose it |
| `call_scribe`      | scribing call transcripts into context and cadence     | "scribe yesterday's Acme call"           | a summary of a call already scribed: read it |

These rows are the checked example, for the pipelines in this repo. Replace them with what your
workspace runs. A row whose agent is not in the live list is removed, not kept "for later".

Handing off is always behind a go in the thread (§3 of the prompt). The request passed to the agent
is the full request with the records it names, not a summary, because the owning agent cannot see
the Slack thread.
