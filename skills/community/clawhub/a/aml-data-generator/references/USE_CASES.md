# Known Use Cases (KUC)

Total: **13**

## `KUC-101`
**Source**: `scripts/convert_logs.py`

Convert transaction log files into synthetic AML simulation data for testing anti-money laundering detection systems

## `KUC-102`
**Source**: `scripts/split_accounts_bank.py`

Partition account CSV files by bank identifier for bank-specific analysis and processing

## `KUC-103`
**Source**: `scripts/combine_data.py`

Aggregate multiple AMLSim output files into a consolidated dataset for comprehensive analysis

## `KUC-104`
**Source**: `scripts/transaction_graph_generator.py`

Generate the base transaction network graph used as input for AML simulation, defining account relationships and transaction patterns

## `KUC-105`
**Source**: `scripts/generate_scalefree.py`

Generate scale-free network graphs using Kronecker graph algorithm for research on network topology and distribution analysis

## `KUC-106`
**Source**: `scripts/visualize/plot_alert_pattern_subgraphs.py`

Visualize alert pattern subgraphs showing which accounts and transactions are involved in each generated alert for debugging and validation

## `KUC-107`
**Source**: `scripts/visualize/plot_distributions.py`

Generate statistical distribution plots (degree, amount, frequency) from transaction graphs for analysis and reporting

## `KUC-108`
**Source**: `scripts/amlsim/random_amount.py`

Generate random transaction amounts within configurable min/max bounds for transaction simulation

## `KUC-109`
**Source**: `scripts/amlsim/nominator.py`

Select appropriate accounts for different transaction types (fan-in, fan-out, single, mutual, periodical) based on network degree thresholds

## `KUC-110`
**Source**: `scripts/amlsim/rounded_amount.py`

Generate rounded transaction amounts (e.g., 100, 500, 1000) to simulate realistic human transaction patterns

## `KUC-111`
**Source**: `scripts/amlsim/normal_model.py`

Define and manage normal (non-suspicious) account behavior models including main accounts and member accounts for transaction simulation

## `KUC-112`
**Source**: `scripts/validation/network_analytics.py`

Load AMLSim outputs and analyze transaction network characteristics including degree distribution, connected components, and graph properties

## `KUC-113`
**Source**: `scripts/validation/validate_alerts.py`

Validate generated alerts against expected alert parameters to ensure AML simulation produces correct alert patterns and amounts
