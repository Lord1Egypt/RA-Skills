import { defineConnector } from "@cargo-ai/cdk";

// AI Ark: the source behind `tam_companies`, carried here only because this
// skill is self-contained and its model copy needs a connector. When
// tam-building is installed, this file is dropped and the model import points
// at tam-building's connector instead: two connectors with one slug collide at
// deploy.
export const aiArk = defineConnector("ai_ark", {
  integration: "aiArk",
  default: true,
});
