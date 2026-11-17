import { defineConnector } from "@cargo-ai/cdk";

// The LLM behind the tiering agent. Bound, not created: `default: true` links
// the workspace's existing Anthropic connector (key-authenticated once in the
// UI), so this example deploys with no env var.
//
// Swap it for OpenAI by changing `integration` to "openAi" and the agent's
// `languageModel` with it. The integration slug is "openAi", not "openai", and
// binding declares no `config`: the wrong casing typechecks green and only
// fails at deploy.
export const anthropic = defineConnector("anthropic", {
  integration: "anthropic",
  default: true,
});
