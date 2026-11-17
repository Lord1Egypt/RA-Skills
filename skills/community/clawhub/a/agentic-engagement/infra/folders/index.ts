import { defineFolder } from "@cargo-ai/cdk";

// Every resource this skill deploys is filed under folders named after the
// skill. A workspace accumulates resources from several skills plus whatever
// the team wrote by hand, and the folder is what answers "what put this here,
// and what else came with it" by looking. It is also what makes removing a
// skill bounded rather than a hunt.
//
// Folders are per-kind, which is why there are two: this skill deploys a
// mailbox and an agent, and each kind is filed separately. Domains
// have no folder kind.
export const mailboxesFolder = defineFolder("agentic_engagement_mailboxes", {
  kind: "mailbox",
  name: "Agentic engagement",
});

export const agentsFolder = defineFolder("agentic_engagement_agents", {
  kind: "agent",
  name: "Agentic engagement",
});
