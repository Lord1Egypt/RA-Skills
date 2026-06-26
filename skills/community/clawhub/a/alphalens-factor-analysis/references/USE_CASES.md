# Known Use Cases (KUC)

Total: **6**

## `KUC-101`
**Source**: `docs/deploy.py`

Automated build and deployment of project documentation to ensure consistent and reproducible documentation releases.

## `KUC-102`
**Source**: `docs/source/conf.py`

Configures the Sphinx documentation system with extensions for Python API documentation, Jupyter notebooks, and mathematical expressions.

## `KUC-103`
**Source**: `docs/source/notebooks/event_study.ipynb, src/alphalens/examples/event_study.ipynb`

Identifies and analyzes specific market events (e.g., price crossing thresholds) to study their predictive power and forward return characteristics.

## `KUC-104`
**Source**: `docs/source/notebooks/intraday_factor.ipynb, src/alphalens/examples/intraday_factor.ipynb`

Analyzes factors across multiple market sectors (11 GICS sectors) to evaluate cross-sector factor performance and sector-specific factor behavior.

## `KUC-105`
**Source**: `docs/source/notebooks/overview.ipynb, src/alphalens/examples/overview.ipynb`

Provides a comprehensive introduction to Alphalens capabilities for factor analysis, including data preparation, factor computation, and performance visualization.

## `KUC-106`
**Source**: `docs/source/notebooks/pyfolio_integration.ipynb, src/alphalens/examples/pyfolio_integration.ipynb`

Combines Alphalens factor analysis with PyFolio portfolio analytics to evaluate factor-derived portfolio performance, risk metrics, and tearsheet generation.
