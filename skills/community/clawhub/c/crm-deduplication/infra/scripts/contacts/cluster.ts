// Which contacts are the same person as the one being deduplicated, how their
// identity keys agree, and what disqualifies the group from merging unattended.

import { sameKey, unique } from "../common/values";
import type { Contact } from "./contact";
import { isGenericEmail } from "./identity";

/**
 * The contact plus every contact reachable from it through a candidate key,
 * however many records the chain passes through. A contact the searches no
 * longer return was absorbed by an earlier merge, so its cluster is empty —
 * which leaves every flag false and emits no merge ID.
 */
export const clusterAround = (
  contacts: Contact[],
  source: Contact | undefined,
): Contact[] => {
  if (source === undefined) {
    return [];
  }

  const cluster = [source];
  // Each contact added is itself searched for further matches, so `cluster`
  // grows while this walks it and ends holding the whole chain.
  for (let index = 0; index < cluster.length; index += 1) {
    for (const contact of contacts) {
      if (
        cluster.includes(contact) === false &&
        sharesCandidateKey(cluster[index], contact)
      ) {
        cluster.push(contact);
      }
    }
  }
  return cluster;
};

/**
 * What disqualifies a group however exactly its keys match: two people's
 * LinkedIn identities inside one group, or an address that reaches a role
 * rather than a person.
 */
export const findConflicts = (cluster: Contact[]) => {
  const conflictingLinkedinPersonIds =
    distinctValues(cluster, "linkedinPersonId").length > 1;
  const conflictingLinkedinIdentity =
    conflictingLinkedinPersonIds ||
    distinctValues(cluster, "linkedinUrl").length > 1;

  return {
    conflictingLinkedinPersonIds,
    conflictingLinkedinIdentity,
    // One address held by records whose LinkedIn identities disagree is shared
    // by two people, whatever its local part says.
    genericOrSharedEmail:
      cluster.some((contact) => isGenericEmail(contact.email)) ||
      (distinctValues(cluster, "email").length === 1 &&
        conflictingLinkedinIdentity),
  };
};

/** Whether every duplicate carries the source's value for one identity key. */
export const allShare = (
  source: Contact | undefined,
  duplicates: Contact[],
  key: "linkedinPersonId" | "linkedinUrl" | "email",
): boolean => {
  const value = source?.[key];
  return (
    value !== undefined &&
    duplicates.length > 0 &&
    duplicates.every((duplicate) => duplicate[key] === value)
  );
};

/** Whether every duplicate carries a phone number the source also holds. */
export const allSharePhone = (
  source: Contact | undefined,
  duplicates: Contact[],
): boolean => {
  if (source === undefined || source.phoneKeys.length === 0) {
    return false;
  }

  return (
    duplicates.length > 0 &&
    duplicates.every((duplicate) => sharesPhone(source, duplicate))
  );
};

/**
 * Whether one chain of exact high-confidence keys ties the whole group
 * together: this record to the next by LinkedIn ID, that one to a third by
 * email, and so on. A group a weaker key alone holds together is not chained.
 */
export const isChainedByHighConfidenceKeys = (cluster: Contact[]): boolean => {
  if (cluster.length < 3) {
    return false;
  }

  const chained = [cluster[0]];
  for (let index = 0; index < chained.length; index += 1) {
    for (const contact of cluster) {
      if (
        chained.includes(contact) === false &&
        sharesHighConfidenceKey(chained[index], contact)
      ) {
        chained.push(contact);
      }
    }
  }
  return chained.length === cluster.length;
};

// Enough to make two records candidates for the same person and gather them
// into one group. Phone is here and nowhere else: it collects a group for a
// reviewer to read, and never merges one on its own.
const sharesCandidateKey = (left: Contact, right: Contact): boolean => {
  return (
    sameKey(left.linkedinPersonId, right.linkedinPersonId) ||
    sameKey(left.linkedinUrl, right.linkedinUrl) ||
    sameKey(left.email, right.email) ||
    sharesPhone(left, right)
  );
};

// Enough to merge two records unattended, before the group-wide conflict guards
// apply: the same LinkedIn person, or the same address that reaches a person.
const sharesHighConfidenceKey = (left: Contact, right: Contact): boolean => {
  const samePerson = sameKey(left.linkedinPersonId, right.linkedinPersonId);
  const sameProfile =
    sameKey(left.linkedinUrl, right.linkedinUrl) &&
    contradicts(left.linkedinPersonId, right.linkedinPersonId) === false;
  const sameMailbox =
    sameKey(left.email, right.email) &&
    isGenericEmail(left.email) === false &&
    isGenericEmail(right.email) === false;
  return samePerson || sameProfile || sameMailbox;
};

const sharesPhone = (left: Contact, right: Contact): boolean => {
  return left.phoneKeys.some((key) => right.phoneKeys.includes(key));
};

// Two keys that are both present and disagree, which is a different person —
// not the silence of one record simply not carrying the key.
const contradicts = (
  left: string | undefined,
  right: string | undefined,
): boolean => {
  return left !== undefined && right !== undefined && left !== right;
};

const distinctValues = (
  cluster: Contact[],
  key: "linkedinPersonId" | "linkedinUrl" | "email",
): string[] => {
  return unique(
    cluster
      .map((contact) => contact[key])
      .filter((value): value is string => value !== undefined),
  );
};
