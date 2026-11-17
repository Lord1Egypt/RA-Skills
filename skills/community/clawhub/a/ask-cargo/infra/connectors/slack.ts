import { defineConnector } from "@cargo-ai/cdk";

// The Slack workspace people @mention the agent from. OAuth, so bound rather
// than created: a deploy cannot mint the grant. Authorize it once in the
// browser (`cargo-ai project add connector/slack`) and `default: true` binds to it.
//
// This connector is the agent's trigger, not an action on `uses`. A Slack
// connector trigger already does the whole conversation: an @mention in any
// channel the bot is in opens (or resumes) one chat per thread, the platform
// streams the agent's answer back into that thread, and a follow-up @mention
// in the same thread lands in the same chat. There is no reply to post by hand, so
// there is nothing to lock and nothing to wrap in a tool.
export const slack = defineConnector("slack", {
  integration: "slack",
  default: true,
});
