# Deliver experience productization rules

## Find the correct abstraction layer

Check from bottom to top:

1. Customer-specific configuration: name, field mapping, role, threshold;
2. Configurable templates: parameter differences for the same workflow;
3. Reusable components: connectors, evaluators, permission modes, data processing;
4. Delivery playbook: standard actions for discovery, contracting, implementation and verification;
5. Product capabilities: Problems and values that stably exist across customers require formal R&D and maintenance.

Don’t wrap layer 1 into layer 5. Prioritize making changes into configurations and making stable rules into core.

## Asset priority

Score 0–2 points for each item: strength of evidence, customer coverage, value, delivery savings, strategic alignment, maintainability; reverse points are deducted based on security/compliance risk, implementation cost, and customer proprietary degree.

Security or authorization fails are considered hard access and are not offset by the total score.

## Maturity promotion

| Levels | Entry conditions | Available methods |
|---|---|---|
| Experiment | With single evidence and owner | Only original team trial |
| Candidates | Have cross-project similarities and applicable assumptions | Controlled reuse |
| Verified | Independently reproduced, passed evaluation, clear boundaries | Team internal directory |
| Standards | Documentation, support, versions, governance and monitoring complete | Default recommended path |
| Decommissioning | Decreased value, increased risk, technology substitution or unmaintained | Prohibited use in new projects |

## Reusable tests

Have an FDE who did not participate in the original project complete a new scenario using only the asset. Observe whether they know when to use it, which inputs it requires, how to configure and verify it, when to stop, and whom to escalate to.

When you can't do it alone, document gaps and iterate on assets without covering them up with verbal explanations.

## Maintain closed loop

- Record projects, versions, variants, results and failures for each reuse;
- New failures enter the evaluation or counterexample library;
- Regularly merge duplicate assets to avoid multiple approximate versions;
- Major changes retain migration instructions and compatibility;
- Decommissioning when there is no owner, no use or the risk is uncontrollable.
