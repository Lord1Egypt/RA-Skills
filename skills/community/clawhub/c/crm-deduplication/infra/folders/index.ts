import { defineFolder } from "@cargo-ai/cdk";

export const modelsFolder = defineFolder("crm_deduplication_models", {
  kind: "model",
  name: "CRM deduplication",
});

export const playsFolder = defineFolder("crm_deduplication_plays", {
  kind: "play",
  name: "CRM deduplication",
});
