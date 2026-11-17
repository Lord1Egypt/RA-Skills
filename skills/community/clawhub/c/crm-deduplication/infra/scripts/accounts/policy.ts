// The knobs a consumer adapts on the account path. The rest of `accounts/` is
// machinery that reads them, so an adaptation review starts, and usually ends,
// here.

import type { Account } from "./account";

/**
 * Domains thousands of unrelated companies share. One of these tells you
 * nothing, so it can neither pair two accounts nor score.
 */
export const GENERIC_DOMAINS = [
  "bit.ly",
  "facebook.com",
  "github.com",
  "google.com",
  "hubs.ly",
  "instagram.com",
  "linkedin.com",
  "linktr.ee",
  "substack.com",
  "uk.com",
];

/**
 * Which account survives a merge, most decisive rule first. Each rule scores an
 * account and the higher score wins; `rankBySurvivorPrecedence` breaks what is
 * still tied.
 */
export const SURVIVOR_PRECEDENCE: ((account: Account) => number)[] = [
  (account) => (account.protectedBusinessId !== undefined ? 1 : 0),
  (account) => (account.isCustomer === true ? 1 : 0),
  (account) => account.openDealCount,
  (account) => account.contactCount,
  (account) => account.activityCount,
  (account) => account.filledPropertyCount,
];
