# Timing and concurrency

Separate execution failure from an observation deadline or missing notification. Check whether work completed and whether its result was durable before retrying. Use the relevant task, request or operation identity; a later run's log cannot explain an earlier run without evidence connecting them.

For an intermittent failure, inspect shared state, ordering and publication of results or errors. Compare a passing schedule with a failing one. A narrow gate or targeted trace can expose a transition that repeated sleeps miss; ensure the probe does not introduce the fault it purports to demonstrate. Existing tests that wait until everything finishes may miss an early notification or intermediate-state defect.

Use controlled overlap or stress only when it tests the suspected mechanism. Preserve timeout semantics and distinguish an idle deadline from a total execution allowance. Increase a deadline when measured progress shows it prevents a meaningful check; do not infer that a timeout means the operation failed. Keep completed stages and retry from the failed stage.
