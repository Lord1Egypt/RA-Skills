# Cross-Project Wisdom

Total: **8**

## `CW-CREDIT-RISK-001` — Strict input DataFrame schema validation
**From**: finance-bp-050--skorecard, finance-bp-112--openLGD · **Applicable to**: credit-risk

Both skorecard and openLGD require strict validation that input DataFrames contain exactly the expected columns (X/Y for openLGD, specified variable names for skorecard). This pattern is critical when data flows through multiple transformation stages where downstream modules access columns by name without defensive checking. Always validate column existence before pipeline execution.

## `CW-CREDIT-RISK-002` — Explicit random_state for ML model reproducibility
**From**: finance-bp-112--openLGD · **Applicable to**: credit-risk

In federated learning scenarios with SGDRegressor, omitting random_state causes non-deterministic results due to random data shuffling and weight initialization. This breaks federated learning convergence guarantees. Always set random_state explicitly when reproducibility across nodes or runs is required for regulatory auditability.

## `CW-CREDIT-RISK-003` — Mandatory data sorting before multi-stage estimation
**From**: finance-bp-050--skorecard, finance-bp-119--transitionMatrix · **Applicable to**: credit-risk

Both skorecard's two-phase bucketing and transitionMatrix's Aalen-Johansen estimator require data to be in a specific order before processing. Skorecard requires prebucketing before bucketing; transitionMatrix requires sorting by entity ID then time. Violating this ordering produces incorrect results or runtime errors. Always establish and enforce processing order in multi-stage pipelines.

## `CW-CREDIT-RISK-004` — Consistent API response key naming across all endpoints
**From**: finance-bp-112--openLGD · **Applicable to**: credit-risk

In federated systems with multiple API endpoints (/start, /update), all responses must use identical key names for parameters (intercept, coefficient). Inconsistency causes coordination loop failures in downstream consumers. Define a schema contract upfront and enforce key naming consistency across all response types.

## `CW-CREDIT-RISK-005` — Cardinality bounds checking before array operations
**From**: finance-bp-050--skorecard, finance-bp-119--transitionMatrix · **Applicable to**: credit-risk

Both skorecard's bucketers (max 100 unique values) and transitionMatrix's matrix operations (state cardinality matching matrix dimensions) require strict cardinality validation before creating numpy arrays or performing computations. Violations cause NotPreBucketedError or index out-of-bounds errors. Always validate cardinality constraints before array initialization.

## `CW-CREDIT-RISK-006` — Financial validation gates before transaction execution
**From**: finance-bp-072--lending · **Applicable to**: credit-risk

Lending systems require validation that disbursement amounts do not exceed limits, collateral values, or authorized periods before any transaction executes. These are financial loss prevention controls, not optional business logic. Missing these validations creates unauthorized exposure and regulatory compliance violations that cannot be remedied retroactively.

## `CW-CREDIT-RISK-007` — Mathematical constraint validation for probability outputs
**From**: finance-bp-050--skorecard, finance-bp-119--transitionMatrix · **Applicable to**: credit-risk

Credit risk models must validate mathematical constraints on outputs: skorecard's WoE requires valid bin assignments, transitionMatrix's transition matrices require row sums equals 1.0 and generator matrices require row sums equals 0.0. Invalid mathematical properties corrupt downstream risk calculations. Validate constraints before returning results.

## `CW-CREDIT-RISK-008` — Port-to-ID mapping consistency in distributed model serving
**From**: finance-bp-112--openLGD · **Applicable to**: credit-risk

When deploying distributed model servers, port numbers must map deterministically to server IDs (e.g., port 5001 maps to server ID 1). Computation of ID from port must be consistent across all components. Inconsistencies cause incorrect data directory selection and model parameter mismatches. Document and validate port-ID mappings during deployment.
