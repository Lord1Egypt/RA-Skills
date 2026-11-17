// Which contact in a duplicate cluster survives the merge.

import type { Contact } from "./contact";
import { SURVIVOR_PRECEDENCE } from "./policy";

/** The cluster ordered survivor first, by `SURVIVOR_PRECEDENCE`. */
export const rankBySurvivorPrecedence = (cluster: Contact[]): Contact[] => {
  return cluster.slice().sort((left, right) => {
    for (const compare of SURVIVOR_PRECEDENCE) {
      const difference = compare(left, right);
      if (difference !== 0) {
        return difference;
      }
    }

    return 0;
  });
};
