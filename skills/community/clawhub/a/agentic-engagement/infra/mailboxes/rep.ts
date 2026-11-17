import { defineMailbox } from "@cargo-ai/cdk";

import { outreach } from "../domains/outreach";
import { mailboxesFolder } from "../folders";

// PLACEHOLDER — the inbox the engager sends from and is woken by. Yields
// `jane@example-outreach.com` once the domain name and username are real.
//
// Domain, username and type are create-only. Changing any of them is destroy
// plus a new `defineMailbox`: a brand-new inbox back at the bottom of the
// send ramp. `firstName` / `lastName` are the From display name; use a real
// person's name under a real identity.
//
// A mailbox is a recurring monthly credit charge for as long as it exists.
// Quote the live figure from `cargo-ai mailboxManagement pricing get` and get
// an explicit yes before the plan's `+ create mailbox:…` line is applied.
// `destroy` is the only way to stop the charge; there is no pause.
export const rep = defineMailbox("rep", {
  domain: outreach,
  type: "google",
  username: "jane",
  firstName: "Jane",
  lastName: "Doe",
  folder: mailboxesFolder,
});
