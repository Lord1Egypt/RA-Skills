// Which accounts are the same company as the one being deduplicated, and how
// their identity keys agree across that cluster.

import { sameKey } from "../common/values";
import type { Account } from "./account";
import { GENERIC_DOMAINS } from "./policy";

/**
 * The account plus every account sharing an identity key with it. An account
 * the search no longer returns was absorbed by an earlier merge, so its cluster
 * is empty — which leaves every flag false and emits no merge ID.
 */
export const clusterAround = (
  accounts: Account[],
  account: Account | undefined,
): Account[] => {
  if (account === undefined) {
    return [];
  }

  return accounts.filter((candidate) => {
    return (
      candidate.id === account.id ||
      sameKey(account.linkedinCompanyId, candidate.linkedinCompanyId) ||
      sameKey(account.linkedinHandle, candidate.linkedinHandle) ||
      (identifiesOneCompany(account.domain) &&
        sameKey(account.domain, candidate.domain))
    );
  });
};

/**
 * How one identity key agrees across the cluster. `sharedByAll` is the bar for
 * merging unattended — every account carries the key and they all agree — and
 * `conflicting` is what disqualifies a cluster outright.
 */
export const agreementOn = (
  cluster: Account[],
  key:
    "linkedinCompanyId" | "linkedinHandle" | "domain" | "protectedBusinessId",
) => {
  const values = cluster
    .map((account) => account[key])
    .filter((value): value is string => value !== undefined);
  const distinctValues = values.filter((value, index) => {
    return values.indexOf(value) === index;
  });

  return {
    value: distinctValues.length === 1 ? distinctValues[0] : undefined,
    sharedByAll:
      values.length === cluster.length && distinctValues.length === 1,
    conflicting: distinctValues.length > 1,
  };
};

/** A domain that names one company, rather than a host thousands share. */
export const identifiesOneCompany = (domain: string | undefined): boolean => {
  return domain !== undefined && GENERIC_DOMAINS.includes(domain) === false;
};
