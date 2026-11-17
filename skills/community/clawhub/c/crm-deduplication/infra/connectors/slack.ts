import { defineConnector } from "@cargo-ai/cdk";

// Where every cluster that is not an exact identity match goes. The native
// Human Review node posts through this connector and blocks the run until a
// reviewer clicks Approve or Decline, so this is the only path that can turn an
// unproven duplicate into a merge.
export const slack = defineConnector("slack", {
  integration: "slack",
  default: true,
});
