// Everything the merge decision rests on, derived deterministically: no model,
// no judgement. The same records always produce the same evidence.

import { defineScript } from "@cargo-ai/cdk";

import { type Account, readAccounts } from "./account";
import { agreementOn, clusterAround, identifiesOneCompany } from "./cluster";
import { rankBySurvivorPrecedence } from "./survivor";

export const deriveEvidence = defineScript(
  ({ records, accountId }: { records: unknown; accountId: string }) => {
    const accounts = readAccounts(records);
    const account = accounts.find((candidate) => candidate.id === accountId);
    const cluster = clusterAround(accounts, account);
    const duplicates = cluster.filter((candidate) => candidate !== account);
    const hasDuplicates = duplicates.length > 0;

    const agreement = {
      linkedinCompanyId: agreementOn(cluster, "linkedinCompanyId"),
      linkedinHandle: agreementOn(cluster, "linkedinHandle"),
      domain: agreementOn(cluster, "domain"),
      protectedBusinessId: agreementOn(cluster, "protectedBusinessId"),
    };

    const exactLinkedinId =
      hasDuplicates && agreement.linkedinCompanyId.sharedByAll;
    const exactLinkedinUrl =
      hasDuplicates && agreement.linkedinHandle.sharedByAll;
    const exactDomain =
      hasDuplicates &&
      agreement.domain.sharedByAll &&
      identifiesOneCompany(agreement.domain.value);
    const identityConflict =
      agreement.linkedinCompanyId.conflicting ||
      agreement.linkedinHandle.conflicting ||
      agreement.domain.conflicting;

    // An account whose parent is also in the cluster is a subsidiary, and a
    // subsidiary is a different company however much it looks like this one.
    const clusterIds = cluster.map((candidate) => candidate.id);
    const parentOrSubsidiaryWarning = cluster.some((candidate) => {
      return (
        candidate.parentCompanyId !== undefined &&
        clusterIds.includes(candidate.parentCompanyId)
      );
    });

    const [survivor, ...merged] = rankBySurvivorPrecedence(cluster);

    return {
      accountFound: account !== undefined,
      hasDuplicates,
      duplicateCount: duplicates.length,
      primaryId: survivor === undefined ? undefined : survivor.id,
      idsToMerge: merged.map((candidate) => candidate.id),
      exactLinkedinId,
      exactLinkedinUrl,
      exactDomain,
      identityConflict,
      protectedIdConflict: agreement.protectedBusinessId.conflicting,
      parentOrSubsidiaryWarning,
      // The only class safe enough to merge unattended.
      autoEligible:
        exactLinkedinId &&
        identityConflict === false &&
        agreement.protectedBusinessId.conflicting === false &&
        parentOrSubsidiaryWarning === false,
      evidenceSummary: summarizeForReview(cluster),
    };
  },
);

// One line per account for the Slack review message. Protected business IDs
// are reported as present or absent, never printed.
const summarizeForReview = (cluster: Account[]): string => {
  return cluster
    .map((account) => {
      return [
        account.id,
        `linkedin id ${account.linkedinCompanyId === undefined ? "none" : account.linkedinCompanyId}`,
        `linkedin ${account.linkedinHandle === undefined ? "none" : account.linkedinHandle}`,
        `domain ${account.domain === undefined ? "none" : account.domain}`,
        `protected ${account.protectedBusinessId === undefined ? "no" : "yes"}`,
        `parent ${account.parentCompanyId === undefined ? "none" : account.parentCompanyId}`,
      ].join(", ");
    })
    .join("\n");
};
