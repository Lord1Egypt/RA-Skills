# Known Use Cases (KUC)

Total: **5**

## `KUC-101`
**Source**: `train_DKG_run.py`

Training a knowledge graph-based transformer model for temporal/dynamic knowledge graph embedding tasks to learn entity and relation representations over time.

## `KUC-102`
**Source**: `DKG/train.py`

Training dynamic knowledge graph models to learn temporal entity and relation embeddings for link prediction and event time prediction tasks.

## `KUC-103`
**Source**: `DKG/utils/train_utils.py`

Preventing overfitting during model training by automatically stopping training when validation performance stops improving, with checkpoint management.

## `KUC-104`
**Source**: `DKG/eval.py`

Evaluating trained knowledge graph models on link prediction and time prediction tasks to measure model performance using various metrics.

## `KUC-105`
**Source**: `DKG/utils/eval_utils.py`

Computing standard ranking metrics (MRR, recall) and regression metrics (MAE, MSE, RMSE) for evaluating machine learning model performance.
