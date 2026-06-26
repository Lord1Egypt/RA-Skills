# Known Use Cases (KUC)

Total: **22**

## `KUC-101`
**Source**: `examples/notebooks/Adjust_NotRated_State.ipynb`

Credit rating transition matrices often contain 'not-rated' (NR) observations that need to be redistributed to rated states for downstream risk calculations and regulatory reporting.

## `KUC-102`
**Source**: `examples/notebooks/Matrix_Operations.ipynb`

Users need to understand how to initialize, validate, and work with transition matrices for credit risk modeling.

## `KUC-103`
**Source**: `examples/notebooks/Monthly_from_Annual.ipynb`

Credit risk models require transition matrices at different time horizons (monthly, quarterly, annual) but only annual matrices may be available; matrix exponentiation of generators enables temporal scaling.

## `KUC-104`
**Source**: `examples/python/adjust_nr_state.py`

Corporate credit rating migration data contains NR (not-rated) states that must be removed using noninformative redistribution method before calculating regulatory capital requirements.

## `KUC-105`
**Source**: `examples/python/characterize_datasets.py`

Data scientists need to understand the characteristics of credit rating transition datasets before applying estimation methods or building models.

## `KUC-106`
**Source**: `examples/python/compare_estimators.py`

Different transition matrix estimation methods produce different results; researchers need to compare cohort-based vs duration-based (Aalen-Johansen) estimators to choose appropriate methods for their data.

## `KUC-107`
**Source**: `examples/python/credit_curves.py`

Credit risk management requires visualization of how default probabilities and credit quality evolve over time through multi-period transition matrices.

## `KUC-108`
**Source**: `examples/python/data_cleaning_example.py`

Raw credit rating data requires preprocessing including column renaming, state validation, and absorbing state verification before it can be used for matrix estimation.

## `KUC-109`
**Source**: `examples/python/deterministic_paths.py`

Testing and validation of transition matrix estimators requires reproducible deterministic transition paths with known outcomes.

## `KUC-110`
**Source**: `examples/python/empirical_transition_matrix.py`

Credit risk modeling requires empirical transition matrix estimation from continuous-time duration data where observation times vary across entities.

## `KUC-111`
**Source**: `examples/python/estimate_matrix.py`

Complete workflow for estimating credit rating transition matrices from historical data using multiple estimation approaches with generator extraction.

## `KUC-112`
**Source**: `examples/python/fix_multiperiod_matrix.py`

Historical credit migration matrices may have structural issues (non-square, missing states, negative probabilities) that must be corrected before use in risk models.

## `KUC-113`
**Source**: `examples/python/generate_full_multiperiod_set.py`

Risk models require complete transition matrices across each time horizons; sparse historical observations must be expanded using matrix exponentiation.

## `KUC-114`
**Source**: `examples/python/generate_synthetic_data.py`

Development and testing of transition matrix estimators requires synthetic data with known properties for validation and benchmarking.

## `KUC-115`
**Source**: `examples/python/generate_visuals.py`

Stakeholders require visual representations of credit migration patterns including Sankey diagrams, heatmaps, and step plots for reporting and presentations.

## `KUC-116`
**Source**: `examples/python/matrix_from_cohort_data.py`

Credit rating agencies publish migration data in cohort format; estimation from this data format requires cohort-based transition matrix estimation.

## `KUC-117`
**Source**: `examples/python/matrix_from_duration_data.py`

Individual credit observations with varying timestamps require duration-based transition matrix estimation using time-to-event methodology.

## `KUC-118`
**Source**: `examples/python/matrix_lendingclub.py`

Peer-to-peer lending platforms like LendingClub have unique grade states; requires specialized transition matrix estimation from loan performance data.

## `KUC-119`
**Source**: `examples/python/matrix_operations.py`

Transition matrices require various mathematical operations including power, validation, printing, and generator extraction for risk calculations.

## `KUC-120`
**Source**: `examples/python/matrix_set_lendingclub.py`

P2P lending risk models require transition matrix sets across multiple periods to capture evolving loan portfolio behavior over time.

## `KUC-121`
**Source**: `examples/python/matrix_set_operations.py`

Multi-period risk models require operations on collections of transition matrices including copying, power-based cumulation, and validation.

## `KUC-122`
**Source**: `examples/python/state_space_operations.py`

Different credit rating agencies use different rating scales; users need to convert between S&P, Moody's, DBRS and other rating systems for portfolio analysis.
