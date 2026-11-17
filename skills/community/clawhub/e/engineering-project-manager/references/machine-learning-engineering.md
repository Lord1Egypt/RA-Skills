# Machine Learning Engineering Conventions

# IDs

DS-###  : dataset
EXP-### : experiment
MDL-### : model
MLE-TST-### : model test
FEAT-### : feature when necessary

# Dataset identity

Every important dataset must have:
- dataset ID;
- version;
- source;
- owner;
- license/rights;
- creation/extraction date;
- schema;
- transformations;
- inclusion/exclusion criteria;
- known limitations.

# Dataset naming

Example:

<project-slug>_DS-001_training_v1.2

TRAIN, VALIDATION and TEST datasets must be separately identifiable.

# Experiments

Every substantial experiment must record:
- EXP ID;
- objective;
- hypothesis;
- dataset versions;
- code commit;
- model architecture;
- hyperparameters;
- random seed when relevant;
- environment;
- metrics;
- results;
- conclusion.

# Model identity

Every released model must allow tracing:

MODEL
↕
training code
↕
configuration
↕
datasets
↕
environment
↕
metrics
↕
tests

# Model naming

Example:

tajer-ai_MDL-003_classifier_v1.4

# Model Card

For an important model, maintain:
- purpose;
- intended use;
- prohibited/unsupported use;
- architecture;
- inputs/outputs;
- training data;
- evaluation data;
- metrics;
- limitations;
- known failure modes;
- runtime constraints;
- model version.

# Data Card

For important datasets, maintain a card describing:
- origin;
- composition;
- acquisition;
- transformations;
- representativeness;
- limitations;
- rights.

# Test discipline

The test set must not be used as a normal tuning loop.

Performance must be evaluated on:
- overall metric;
- relevant segments;
- important edge cases;
- runtime constraints when applicable.

# Reproducibility

When reasonably possible, keep:
- environment lock;
- dependencies;
- seeds;
- dataset IDs;
- code commit;
- configuration.

A metric without the corresponding model and data version is not sufficient evidence.
