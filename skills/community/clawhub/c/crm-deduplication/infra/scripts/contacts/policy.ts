// The knobs a consumer adapts on the contact path. The rest of `contacts/` is
// machinery that reads them, so an adaptation review starts, and usually ends,
// here.

import type { Contact } from "./contact";

/**
 * Local parts that address a role rather than a person. Two records sharing one
 * of these are not evidence of one person, so it can neither merge them nor
 * score.
 */
export const GENERIC_EMAIL_LOCAL_PARTS = [
  "admin",
  "contact",
  "hello",
  "info",
  "office",
  "sales",
  "support",
  "team",
];

/**
 * Which contact survives a merge, most decisive rule first. Each rule orders
 * two contacts and the first one that separates them decides; the last rule is
 * total, so two runs over one cluster can never disagree.
 */
export const SURVIVOR_PRECEDENCE: ((
  left: Contact,
  right: Contact,
) => number)[] = [
  (left, right) => right.associatedDeals - left.associatedDeals,
  (left, right) => right.activities - left.activities,
  (left, right) => left.createdAt.localeCompare(right.createdAt),
  (left, right) => right.filledPropertyCount - left.filledPropertyCount,
  (left, right) => left.id.localeCompare(right.id),
];
