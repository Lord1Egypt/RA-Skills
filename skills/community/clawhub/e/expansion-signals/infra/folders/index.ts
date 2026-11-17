import { defineFolder } from "@cargo-ai/cdk";

// One folder per kind, named after the pipeline, so "what put this here" is
// answered by looking and removing the pipeline is a bounded job.
export const modelsFolder = defineFolder("expansion_signals_models", {
  kind: "model",
  name: "Expansion signals",
});

export const agentsFolder = defineFolder("expansion_signals_agents", {
  kind: "agent",
  name: "Expansion signals",
});

export const playsFolder = defineFolder("expansion_signals_plays", {
  kind: "play",
  name: "Expansion signals",
});
