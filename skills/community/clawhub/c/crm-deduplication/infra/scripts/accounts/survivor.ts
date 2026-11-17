// Which account in a duplicate cluster survives the merge.

import type { Account } from "./account";
import { SURVIVOR_PRECEDENCE } from "./policy";

/**
 * The cluster ordered survivor first. `SURVIVOR_PRECEDENCE` decides; accounts
 * it leaves tied prefer recent activity, then the older account, then the lower
 * ID — so two runs over one cluster can never disagree.
 */
export const rankBySurvivorPrecedence = (cluster: Account[]): Account[] => {
  return cluster.slice().sort((left, right) => {
    for (const scoreOf of SURVIVOR_PRECEDENCE) {
      const difference = scoreOf(right) - scoreOf(left);
      if (difference !== 0) {
        return difference;
      }
    }

    const byRecentActivity = compareAbsentFirst(
      right.lastActivityAt,
      left.lastActivityAt,
    );
    if (byRecentActivity !== 0) {
      return byRecentActivity;
    }

    const byAge = compareAbsentFirst(left.createdAt, right.createdAt);
    if (byAge !== 0) {
      return byAge;
    }

    return left.id.localeCompare(right.id);
  });
};

// An absent value orders before any present one, exactly as the empty string it
// replaced did. That means an account with no creation date wins "oldest" —
// kept as-is, since changing it would change which account survives.
const compareAbsentFirst = (
  left: string | undefined,
  right: string | undefined,
): number => {
  return (left === undefined ? "" : left).localeCompare(
    right === undefined ? "" : right,
  );
};
