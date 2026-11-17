import { defineAgent } from "@cargo-ai/cdk";

import { anthropic } from "../connectors/anthropic";
import { slack } from "../connectors/slack";
import { agentsFolder } from "../folders";
import { gtmAccounts } from "../models/gtm-accounts";
import { expansionDigests } from "../models/expansion-digests";

// The weekly digest: one Slack post for the customer team, listing every
// account the play flagged this week.
//
// It runs hours after the play and reads only the gtm_accounts model, where the
// play wrote `expansion_*`. It re-judges nothing: the reason on the
// account is the reason in the digest, so a rep who opens the record reads the
// same words.
//
// The ledger is checked before posting and appended after, so a re-run the
// same week posts nothing and a failed post is retried next run.
export const expansionDigest = defineAgent("expansion_digest", {
  name: "Expansion digest",
  description:
    "Posts one weekly Slack digest of the customers flagged at an expansion moment, grouped by owner.",
  color: "green",
  connector: anthropic,
  languageModel: "claude-sonnet-5", // PLACEHOLDER: your model of choice
  maxSteps: 12,
  systemPrompt: [
    "You post the weekly expansion digest for the customer team. You never judge an account yourself and you never message a customer.",
    "You have no clock of your own, so never assume the date. First read it with SQL: SELECT CURRENT_TIMESTAMP() AS now, CURRENT_DATE() AS today. Every 'now', 'this week' and date window below is measured from those values; write timestamps as ISO 8601 strings.",
    "1. Compute week_start, the Monday of the current ISO week, as YYYY-MM-DD. If the expansion_digests model already has a row with that week_start, stop: this week is posted.",
    "2. Query the gtm_accounts model in SQL for rows whose custom__expansion_signal_at falls in the last 7 days and whose custom__expansion_signal is not 'none'. Read name, website, owner_id, the signal and the reason.",
    "3. Post one message with the Slack postMessage action. Header ':seedling: *Expansion signals, week of <week_start>*' and a one-line verdict (how many companies, how many at risk). Then 'at_risk' companies first, then 'expansion', 'repeat_purchase', 'renewal'. One line each: *<name>* (<website>) · <signal> · <the reason, as written> · owner <owner id>. A week with no flagged account posts one line saying so.",
    "4. After the post succeeds, append one row to expansion_digests: week_start, posted_at (now), company_count, slack_ts. Never before the post.",
    "Never add a fact that is not in the row. Never post more than once per run.",
  ].join("\n"),
  uses: [
    { ref: gtmAccounts, readOnly: true },
    { ref: expansionDigests, readOnly: false },
    {
      ref: slack.actions.postMessage,
      config: {
        // PLACEHOLDER: the channel the digest lands in, as a Slack id (C…)
        // read from the connector's channel autocomplete. Locked so a digest
        // that names customers and their renewal risk never lands in a
        // customer shared channel.
        channelId: "C0123456789",
        format: "markdown",
        disableUnfurling: true,
      },
    },
  ],
  triggers: [
    {
      type: "cron",
      name: "weekly",
      // Monday 15:00 UTC: nine hours after the play, so this week's runs have
      // finished writing. Move both together.
      cron: "0 15 * * 1",
      text: "Post this week's expansion digest. Follow your system prompt exactly: check the ledger, read the gtm_accounts model, post once, record it.",
    },
  ],
  folder: agentsFolder,
});
