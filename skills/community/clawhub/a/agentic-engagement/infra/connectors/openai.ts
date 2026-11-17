import { defineConnector } from "@cargo-ai/cdk";

// The LLM provider the engager talks through. Bound, not created: `default:
// true` links the workspace's existing OpenAI connector (the one
// key-authenticated in the UI), so this example deploys with no env var of its
// own. Swap for anthropic/gemini and update the agent's `languageModel`
// accordingly.
//
// The integration slug is "openAi", not "openai". Binding declares no `config`,
// so the wrong casing typechecks green and only fails at deploy.
export const openai = defineConnector("openai", {
  integration: "openAi",
  default: true,
});
