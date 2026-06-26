# Anti-Patterns (Cross-Project)

Total: **14**

## finance-bp-050--skorecard (5)

### `AP-CREDIT-RISK-001` — Empty DataFrame passed to bucketing pipeline <sub>(high)</sub>

When preparing input data for bucketing, passing an empty DataFrame with zero rows or zero columns causes immediate ValueError at validation stage. This prevents any downstream processing and blocks the entire credit risk scoring pipeline from executing. The root cause is missing defensive validation before data enters the bucketing workflow.

### `AP-CREDIT-RISK-002` — Multi-dimensional target array causing WoE shape mismatch <sub>(high)</sub>

When providing target variable y to bucketers without normalizing to 1D numpy array through _check_y validation, downstream Weight of Evidence calculations fail with shape mismatches. The consequence is corrupted bucket tables with incorrect credit risk scores that misrepresent default probability estimates.

### `AP-CREDIT-RISK-003` — OptimalBucketer receiving high-cardinality numerical features <sub>(high)</sub>

When implementing prebucketing for OptimalBucketer on numerical features without reducing to at most 100 unique values, the system raises NotPreBucketedError and blocks the entire bucketing pipeline. Similarly, AsIsNumericalBucketer fails with the same error for columns exceeding 100 unique values, preventing feature transformation in production scoring.

### `AP-CREDIT-RISK-004` — Special values distorting optimal bin boundaries <sub>(high)</sub>

When implementing fit() for bucketers without filtering special values from X before computing bin boundaries using _filter_specials_for_fit(), outlier special values distort optimal bin boundaries. This causes incorrect weight-of-evidence calculations and unreliable credit risk scores that misrepresent borrower default probabilities.

### `AP-CREDIT-RISK-005` — Two-phase bucketing ordering violation causing special value loss <sub>(high)</sub>

When fitting a BucketingProcess with two-phase bucketing without fitting prebucketing_pipeline before bucketing_pipeline, special value remapping fails because pre-bucket labels are unavailable. Additionally, not using _find_remapped_specials() after prebucketing causes special values to lose their correct bucket mappings, resulting in runtime errors.

## finance-bp-072--lending (3)

### `AP-CREDIT-RISK-006` — Loan amount exceeding product and collateral limits <sub>(high)</sub>

When validating loan amount for loan applications without enforcing loan_amount does not exceed maximum_loan_amount from loan product or proposed securities, disbursing amounts exceeding product or collateral limits exposes the lender to uncollateralized risk. This violates lending policy and creates direct financial loss exposure through unauthorized lending.

### `AP-CREDIT-RISK-007` — Disbursement validation failures creating unauthorized exposure <sub>(high)</sub>

When implementing loan disbursement validation without checking disbursed amount against loan limit, assigned security value, available limit amount, and limit applicability dates, unauthorized disbursements occur. For Line of Credit loans, disbursement outside approved periods or exceeding available limits creates unauthorized lending exposure and regulatory compliance violations.

### `AP-CREDIT-RISK-008` — Interest accrual on written-off loans inflating income <sub>(high)</sub>

When processing interest accrual for Written Off loans without verifying posting_date is on or after the loan write-off date, interest is artificially inflated on non-performing assets. This misrepresents loan portfolio value, violates provisioning requirements, and creates false income reporting that misleads stakeholders about actual financial performance.

## finance-bp-112--openLGD (2)

### `AP-CREDIT-RISK-009` — Loop index errors in federated parameter averaging <sub>(high)</sub>

When implementing federated parameter averaging logic, using the final index n instead of the loop variable k causes only the last server's weight to be applied repeatedly. Additionally, skipping the first server by starting loop index at 1 excludes valid parameters from averaging, breaking federated convergence and producing incorrect LGD estimates across all nodes.

### `AP-CREDIT-RISK-010` — API response format inconsistency breaking federated coordination <sub>(high)</sub>

When implementing GET /start and POST /update endpoints for LGD estimation without consistent 'intercept' and 'coefficient' keys in JSON responses, the federated coordinator fails to parse responses causing KeyError. Different return key names (e.g., 'coef' instead of 'coefficient') break both standalone and federated execution paths.

## finance-bp-119--transitionMatrix (4)

### `AP-CREDIT-RISK-011` — Invalid transition probabilities corrupting Markov matrices <sub>(high)</sub>

When generating synthetic Markov chain data or estimating transition matrices with probabilities outside [0, 1] or row sums not equal to 1.0, the resulting matrices violate the fundamental mathematical definition of a stochastic transition matrix. This corrupts all downstream Markov chain modeling and credit curve generation, producing unreliable credit risk estimates.

### `AP-CREDIT-RISK-012` — Unsorted event data causing incorrect transition matrix estimates <sub>(high)</sub>

When feeding generated data to cohort or duration estimators without sorting by entity ID first, then by ascending time, incorrect timepoint assignment occurs in estimators, leading to wrong transition counts. Unsorted data also causes the Aalen-Johansen algorithm to process events out of temporal order, producing incorrect transition matrices that violate the Markov property.

### `AP-CREDIT-RISK-013` — Zero-count division causing NaN in transition matrices <sub>(high)</sub>

When normalizing counts to produce transition probabilities without checking source state population count is greater than zero before division, division by zero occurs and causes NaN values in the transition matrix. These NaN values corrupt all downstream matrix operations including generator matrix computation and credit curve generation.

### `AP-CREDIT-RISK-014` — Wrong matrix logarithm method producing invalid generator matrices <sub>(medium)</sub>

When implementing generator() method without using scipy.linalg.logm for matrix logarithm computation, using numpy.log or other approximation methods produces invalid generator matrices with row sums not equal to zero. This violates the mathematical definition of an infinitesimal generator, causing incorrect continuous-time Markov chain modeling.
