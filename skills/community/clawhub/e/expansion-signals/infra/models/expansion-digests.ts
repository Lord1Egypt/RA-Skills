import { defineModel } from "@cargo-ai/cdk";

import { modelsFolder } from "../folders";

// The digest ledger: one row per week posted. The digest agent checks it
// before it posts and appends after the post succeeds, so a re-run the same
// week posts nothing and a failed post is retried. Slack history is not the
// dedupe: a deleted message or another bot's post would read as "already
// sent".
export const expansionDigests = defineModel("expansion_digests", {
  kind: "native",
  extractSlug: "defineCustom",
  config: {
    columns: [
      // Monday of the ISO week the digest covers, YYYY-MM-DD. The ledger key.
      { slug: "week_start", type: "string" },
      { slug: "posted_at", type: "string" },
      { slug: "company_count", type: "number" },
      { slug: "slack_ts", type: "string" },
    ],
  },
  folder: modelsFolder,
});
