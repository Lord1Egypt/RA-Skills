import { defineConnector } from "@cargo-ai/cdk";

// The Slack workspace the weekly digest lands in. OAuth, so bound rather than
// created: authorize it once (`cargo-ai project add connector/slack`) and
// `default: true` binds to it. The digest agent posts through
// `postMessage` with the channel locked on the use.
export const slack = defineConnector("slack", {
  integration: "slack",
  default: true,
});
