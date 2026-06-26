# Anti-Patterns (Cross-Project)

Total: **15**

## finance-bp-063--chainladder-python (4)

### `AP-INSURANCE-002` — Triangle axis construction with invalid temporal ordering <sub>(high)</sub>

Development dates are created without verifying they are strictly greater than origin dates, or development lags are calculated with incorrect formulas (e.g., using wrong divisor for monthly difference). This creates logically impossible triangle cells where development <= origin, corrupting the fundamental data structure and producing wrong loss development patterns.

### `AP-INSURANCE-003` — Cumulative/incremental triangle representation misuse <sub>(high)</sub>

Link ratios are computed on incremental triangles instead of cumulative form, or cum_to_incr/incr_to_cum conversions are not properly inverse-applied. This produces link ratios near 1.0 regardless of actual claims development, leading to misleading development factors and incorrect IBNR estimates.

### `AP-INSURANCE-004` — Including incomplete latest diagonal in development analysis <sub>(high)</sub>

Link ratio computation includes the latest diagonal which contains incomplete/in-progress development data. Without excluding this diagonal via valuation_date filtering, development factor estimation uses partial data that biases IBNR estimates. The latest diagonal must be excluded to capture true historical development patterns.

### `AP-INSURANCE-015` — Triangle grain transformation with incompatible parameters <sub>(medium)</sub>

Triangle grain() method is called without setting is_cumulative attribute, or origin grain is made finer than development grain. These produce invalid triangular data structures with misaligned periods and undefined behavior, corrupting actuarial reserving calculations.

## finance-bp-064--insurance_python (2)

### `AP-INSURANCE-005` — EIOPA calibration workflow violations <sub>(high)</sub>

Smith-Wilson calibration workflow is violated in multiple ways: calibration step is skipped before extrapolation, different alpha values are used for calibration vs extrapolation, or convergence point T uses incorrect formula. These violations produce mathematically inconsistent rate curves where observed points do not match market data and extrapolated rates violate EIOPA specifications.

### `AP-INSURANCE-006` — Missing iteration bounds causing infinite loops <sub>(high)</sub>

Root-finding algorithms like bisection for alpha calibration lack maxIter parameters. When the algorithm fails to converge (e.g., no sign change in Galfa at interval bounds), the application freezes indefinitely, causing service disruption. This is especially critical in regulatory compliance workflows where calibration must complete.

## finance-bp-064--insurance_python, finance-bp-126--lifelines (1)

### `AP-INSURANCE-007` — Invalid financial/mathematical constraints not validated <sub>(high)</sub>

Correlation coefficients outside [-1,1], non-positive-semidefinite covariance matrices, negative durations, or entry times >= duration are not validated before use. These cause Cholesky decomposition failures, imaginary values in sqrt(1-rho²), or logically impossible scenarios, producing NaN prices or corrupted at-risk calculations.

## finance-bp-065--pyliferisk (4)

### `AP-INSURANCE-008` — None values propagated to arithmetic operations <sub>(high)</sub>

Critical parameters like interest rate i are passed as None to actuarial calculations. In pyliferisk, Actuarial.__init__ with i=None causes TypeError in (1/(1+i)) and commutation arrays remain empty. Bare except clauses catch these TypeErrors and silently return 0, masking the fundamental issue and producing incorrect but seemingly valid results.

### `AP-INSURANCE-009` — Stub function implementations and duplicate definitions <sub>(high)</sub>

Critical insurance functions like deferred temporary annuities are implemented as empty stubs (only 'pass' statement) or have duplicate definitions where the second shadows the first. This causes functions to return None instead of calculated values, breaking increasing annuity and premium calculations silently in production.

### `AP-INSURANCE-010` — Dispatcher routing to undefined functions <sub>(medium)</sub>

Complex function dispatchers (like annuity()) handle many parameter combinations but call functions that do not exist (e.g., qtaaxn, qtaxn). This causes NameError at runtime when specific parameter combinations are requested, preventing deferred temporary increasing annuity calculations entirely.

### `AP-INSURANCE-014` — Actuarial convention violations in life table construction <sub>(high)</sub>

Life tables violate standard actuarial conventions: using incorrect radix (not 100000), failing to append 0 to lx array for complete extinction, or using wrong payment adjustment formula for fractional annuities. These violations scale all derived quantities (dx, ex, reserves, premiums) incorrectly.

## finance-bp-065--pyliferisk, finance-bp-064--insurance_python (1)

### `AP-INSURANCE-001` — Implicit numeric format assumptions without validation <sub>(high)</sub>

Data formats like per-mille qx values or rate-to-price conversions are applied implicitly without validation. In pyliferisk, qx values stored as per-mille (qx*1000) are used directly as probabilities yielding 1000x errors. In insurance_python, rates are converted to prices using p=(1+r)^(-M) without verifying input format. This causes material miscalculations in reserve and premium calculations.

## finance-bp-126--lifelines (3)

### `AP-INSURANCE-011` — Survival function monotonicity not enforced <sub>(high)</sub>

Non-parametric survival curve estimators do not verify that S(t) is monotonically non-increasing across timeline values. Violations produce mathematically invalid survival curves where probability of survival increases over time, or S(0) is not initialized to 1.0, breaking interpretation as probability distribution.

### `AP-INSURANCE-012` — Input data corruption via inplace operations <sub>(medium)</sub>

User-provided DataFrames are modified inplace using .pop() operations without first creating a copy. This permanently corrupts user data by removing columns, violating data isolation principles and potentially affecting downstream analysis on the original data.

### `AP-INSURANCE-013` — Interval censoring bounds not validated <sub>(medium)</sub>

Lower and upper bounds for interval-censored data are not validated, allowing upper_bound < lower_bound. Invalid interval bounds produce undefined survival probability calculations, potentially negative time intervals in the likelihood function, and corrupt NPMLE estimation.
