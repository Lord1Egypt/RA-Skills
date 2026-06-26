# Known Use Cases (KUC)

Total: **43**

## `KUC-1`
**Source**: `skorecard/bucketers/bucketers.py`

Automatically find optimal bucket boundaries that maximize predictive power while respecting monotonicity constraints

## `KUC-2`
**Source**: `skorecard/bucketers/bucketers.py`

Use supervised learning to find bucket boundaries based on target variable correlation

## `KUC-3`
**Source**: `skorecard/bucketers/bucketers.py`

Divide numerical features into N equally spaced intervals regardless of data distribution

## `KUC-4`
**Source**: `skorecard/bucketers/bucketers.py`

Divide numerical features into N buckets with equal number of observations (quantiles)

## `KUC-5`
**Source**: `skorecard/bucketers/bucketers.py`

Use agglomerative clustering to find natural groupings in numerical data

## `KUC-6`
**Source**: `skorecard/bucketers/bucketers.py`

Convert categorical variables into ordered ordinal numbers based on target rate or frequency

## `KUC-7`
**Source**: `skorecard/bucketers/bucketers.py`

Treat existing unique categories as pre-defined buckets without transformation

## `KUC-8`
**Source**: `skorecard/bucketers/bucketers.py`

Treat existing unique numerical values as bucket boundaries (for pre-bucketed data)

## `KUC-9`
**Source**: `skorecard/bucketers/bucketers.py`

Apply manually defined bucket boundaries from YAML or dictionary to new data

## `KUC-10`
**Source**: `skorecard/pipeline/bucketing_process.py`

First pre-bucket high-cardinality features, then apply final bucketing strategy

## `KUC-11`
**Source**: `skorecard/bucketers/base_bucketer.py`

Handle missing values by assigning them to specific buckets or treating separately

## `KUC-12`
**Source**: `skorecard/bucketers/base_bucketer.py`

Assign specific outlier or important values to their own dedicated buckets

## `KUC-13`
**Source**: `skorecard/bucketers/base_bucketer.py`

Visually explore and manually adjust bucket boundaries using Dash web app

## `KUC-14`
**Source**: `skorecard/preprocessing/_WoEEncoder.py`

Transform bucket IDs into Weight of Evidence values for logistic regression

## `KUC-15`
**Source**: `skorecard/metrics/metrics.py`

Measure the predictive power of individual features for credit risk

## `KUC-16`
**Source**: `skorecard/reporting/report.py`

Monitor distribution drift between training and production data

## `KUC-17`
**Source**: `skorecard/linear_model/linear_model.py`

Build logistic regression model with statistical significance for credit scoring

## `KUC-18`
**Source**: `skorecard/skorecard.py`

Build complete credit scoring scorecard in one step

## `KUC-19`
**Source**: `skorecard/rescale/rescale.py`

Convert model probabilities to traditional scorecard scale (e.g., 300-850)

## `KUC-20`
**Source**: `skorecard/reporting/report.py`

Generate detailed bucket tables with event rate, WoE, IV for documentation

## `KUC-21`
**Source**: `skorecard/reporting/plotting.py`

Visualize bucket distributions with event rate or WoE trends

## `KUC-22`
**Source**: `skorecard/bucket_mapping.py`

Export bucket mappings to YAML for production deployment

## `KUC-23`
**Source**: `skorecard/pipeline/pipeline.py`

Integrate skorecard bucketers into existing scikit-learn ML pipelines

## `KUC-24`
**Source**: `docs/tutorials/2_feature_selection.ipynb`

Select most predictive and stable features using IV and PSI metrics

## `KUC-25`
**Source**: `skorecard/utils/validation.py`

Detect suppressor effects and multicollinearity between features

## `KUC-26`
**Source**: `docs/tutorials/categoricals.ipynb`

Handle categorical variables with many categories in credit scoring

## `KUC-27`
**Source**: `docs/discussion/benchmark_with_EBM.ipynb`

Compare skorecard performance against Explainable Boosting Machines

## `KUC-101`
**Source**: `docs/discussion/benchmark_stats_feature.ipynb`

Compare performance of different machine learning classifiers on credit card default prediction using AUC metrics.

## `KUC-103`
**Source**: `docs/discussion/benchmarks.ipynb`

Run comprehensive benchmarks comparing multiple classifiers on credit card data with timing analysis.

## `KUC-104`
**Source**: `docs/howto/Optimizations.ipynb`

Find optimal bucketing parameters (max_n_bins, min_bin_size) using grid search with Information Value scoring.

## `KUC-105`
**Source**: `docs/howto/mix_with_other_packages.ipynb`

Combine skorecard bucketing with external packages like category_encoders and sklearn transformers in a pipeline.

## `KUC-106`
**Source**: `docs/howto/psi_and_iv.ipynb`

Calculate Population Stability Index (PSI) and Information Value (IV) to validate feature stability and predictive power.

## `KUC-107`
**Source**: `docs/howto/save_buckets_to_file.ipynb`

Persist bucketer configurations to YAML files for reuse and deployment across environments.

## `KUC-108`
**Source**: `docs/howto/using_manually_defined_buckets.ipynb`

Define custom bucket boundaries manually for specific business requirements without automatic binning.

## `KUC-109`
**Source**: `docs/tutorials/1_bucketing.ipynb`

Learn fundamental bucketing concepts for credit card data including categorical and numerical feature handling.

## `KUC-111`
**Source**: `docs/tutorials/3_skorecard_model.ipynb`

Build an end-to-end scorecard model combining bucketing with logistic regression for credit scoring.

## `KUC-113`
**Source**: `docs/tutorials/interactive_bucketing.ipynb`

Learn interactive bucketing approach for manual adjustment of bin boundaries in a pipeline.

## `KUC-114`
**Source**: `docs/tutorials/methods.ipynb`

Explore bucketer methods including summary statistics, bucket tables, plots, and YAML export.

## `KUC-115`
**Source**: `docs/tutorials/missing_values.ipynb`

Handle missing values in bucketing with various treatment strategies like neutral, similar, least_risky.

## `KUC-116`
**Source**: `docs/tutorials/reporting.ipynb`

Generate reports and visualizations for scorecard models including bucket tables and weight plots.

## `KUC-117`
**Source**: `docs/tutorials/specials.ipynb`

Define special values and ranges in bucketing that require separate treatment from regular bins.

## `KUC-118`
**Source**: `docs/tutorials/the_basics.ipynb`

Introduction to basic bucketing operations including DecisionTree and EqualWidth bucketers.

## `KUC-119`
**Source**: `docs/tutorials/using-bucketing-process.ipynb`

Learn the BucketingProcess workflow with pre-bucketing and bucketing stages for complex credit scoring.
