import { defineRole, defineUser } from "@cargo-ai/cdk";

// The workspace system role every reader holds. Adopted, not created: a system
// role cannot be edited, so there is no permission list here to drift.
const viewer = defineRole("viewer", { adopt: true });

// The service user every Ask Cargo turn runs as. The sandbox gets a short-lived
// `CARGO_API_TOKEN` for it, so `cargo-ai` reads the workspace as this user and
// not as whoever deployed, and the runs and handoffs it starts are attributed
// to it.
//
// Viewer is enough. It reads runs, models, connectors, agents and usage, and
// sending another agent a message needs no write grant. It cannot deploy,
// change a resource or touch billing, which is what keeps the prompt's "never
// deploy" true even if the prompt is ignored.
export const askCargoUser = defineUser("ask_cargo", {
  kind: "service",
  firstName: "Ask",
  lastName: "Cargo",
  role: viewer,
});
