// Everything the contact merge decision rests on, derived deterministically: no
// model, no judgement. The same records always produce the same evidence.

import { defineScript } from "@cargo-ai/cdk";

import {
  allShare,
  allSharePhone,
  clusterAround,
  findConflicts,
  isChainedByHighConfidenceKeys,
} from "./cluster";
import { type Contact, readContacts } from "./contact";
import { rankBySurvivorPrecedence } from "./survivor";

export const deriveContactEvidence = defineScript(
  ({
    directRecords,
    transitiveRecords,
    sourceId,
  }: {
    directRecords: unknown;
    transitiveRecords: unknown;
    sourceId: string;
  }) => {
    const contacts = readContacts(directRecords, transitiveRecords);
    const source = contacts.find((contact) => contact.id === sourceId);
    const cluster = clusterAround(contacts, source);
    const duplicates = cluster.slice(1);
    const conflicts = findConflicts(cluster);

    // The approved classes, each of which is exact on its own. They are not
    // mutually exclusive, so several can be true for one group.
    const exactLinkedinPersonId = allShare(
      source,
      duplicates,
      "linkedinPersonId",
    );
    const exactLinkedinUrl =
      allShare(source, duplicates, "linkedinUrl") &&
      conflicts.conflictingLinkedinPersonIds === false;
    const exactNonGenericEmail =
      allShare(source, duplicates, "email") &&
      conflicts.genericOrSharedEmail === false &&
      conflicts.conflictingLinkedinIdentity === false;
    const exactKeyAcrossCluster =
      exactLinkedinPersonId || exactLinkedinUrl || exactNonGenericEmail;

    // A chain of those exact classes, for a group no single key spans.
    const transitiveHighConfidence =
      exactKeyAcrossCluster === false &&
      isChainedByHighConfidenceKeys(cluster) &&
      conflicts.conflictingLinkedinIdentity === false &&
      conflicts.genericOrSharedEmail === false;

    // Reported so a reviewer knows phone is all that gathered the group. It is
    // never an automatic class.
    const phoneOnly =
      exactKeyAcrossCluster === false &&
      transitiveHighConfidence === false &&
      allSharePhone(source, duplicates);

    const [survivor, ...merged] = rankBySurvivorPrecedence(cluster);

    return {
      sourceFound: source !== undefined,
      hasDuplicates: duplicates.length > 0,
      duplicateCount: duplicates.length,
      primaryId: survivor?.id,
      idsToMerge: merged.map((contact) => contact.id),
      exactLinkedinPersonId,
      exactLinkedinUrl,
      exactNonGenericEmail,
      transitiveHighConfidence,
      phoneOnly,
      ...conflicts,
      // The only groups safe enough to merge unattended: one approved class,
      // and no conflict anywhere in the group.
      autoEligible:
        (exactKeyAcrossCluster || transitiveHighConfidence) &&
        conflicts.conflictingLinkedinIdentity === false &&
        conflicts.genericOrSharedEmail === false,
      reviewLines: cluster.map((contact) => summarizeForReview(contact)),
    };
  },
);

// One line per contact for the Slack review message, showing the email as the
// CRM holds it rather than as this code compares it.
const summarizeForReview = (contact: Contact): string => {
  return [
    contact.id,
    [contact.firstName, contact.lastName].filter(Boolean).join(" ") ||
      "(no name)",
    contact.storedEmail ?? "(no email)",
    contact.linkedinPersonId ?? "(no LinkedIn ID)",
    contact.jobTitle ?? "(no title)",
    contact.primaryAssociatedCompanyId ?? "(no company)",
  ].join(" | ");
};
