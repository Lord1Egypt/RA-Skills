import { defineConnector } from "@cargo-ai/cdk";

// The model both agents run on. `default: true` binds the workspace's existing
// Anthropic connector, so this pipeline deploys with no env var of its own.
export const anthropic = defineConnector("anthropic", {
  integration: "anthropic",
  default: true,
});
