# Industry Terms: Machine Learning / AI

> **Usage note:** This file is for the machine learning / AI domain broadly, including model development, evaluation, algorithmic work, and applied model-building. Use it to catch colloquial or informal descriptions and map them to the recognized industry terms that belong on a resume or portfolio. If the user's story is more about training infrastructure, serving, or AI platform work, pair this with the AI infrastructure reference.

---

## Training & Optimization

| User's description | Industry term |
|---|---|
| "used less data to train" | Few-shot / Data-efficient Learning |
| "made training use less memory" | Mixed-precision Training / Gradient Checkpointing |
| "used human feedback" | RLHF (Reinforcement Learning from Human Feedback) |
| "made small model learn from big one" | Knowledge Distillation |
| "combined multiple models" | Ensemble Methods |
| "trained on multiple GPUs" | Distributed Training (Data/Model Parallelism) |
| "kept training on new data" | Continual / Incremental Learning |
| "made model smaller" | Quantization / Pruning / Model Compression |
| "stopped training early to avoid overfitting" | Early Stopping / Regularization |
| "tweaked learning rates during training" | Learning Rate Scheduling / Hyperparameter Tuning |

## Data & Pipelines

| User's description | Industry term |
|---|---|
| "cleaned messy data" | Data Curation / Data Quality Engineering |
| "labeled data" | Annotation Pipeline / Data Labeling |
| "handled streaming data" | Stream Processing (Kafka, Flink) |
| "built feature tables" | Feature Engineering / Feature Store |
| "dealt with imbalanced data" | Class Imbalance Handling (SMOTE, Re-sampling) |
| "versioned datasets" | Data Versioning (DVC, Delta Lake) |
| "generated fake training data" | Synthetic Data Generation / Data Augmentation |
| "combined data from many sources" | Data Integration / ETL Pipeline |
| "made data anonymous" | Data Anonymization / Privacy-preserving Preprocessing |
| "tracked where data came from" | Data Lineage / Data Provenance |

## Deployment & Production

| User's description | Industry term |
|---|---|
| "put model in production" | Model Serving / Model Deployment |
| "monitored model performance" | ML Monitoring / Observability |
| "model got worse over time" | Model Drift Detection (Data Drift, Concept Drift) |
| "auto-retrained" | Continuous Training / MLOps Pipeline |
| "A/B tested models" | Online Experimentation / Multi-armed Bandit |
| "served model via API" | Model-as-a-Service / Inference Endpoint |
| "rolled out model gradually" | Canary Deployment / Shadow Mode |
| "made inference faster" | Inference Optimization / Model Acceleration |
| "tracked model versions" | Model Registry / Model Versioning |
| "ran model on edge device" | Edge Inference / On-device ML |

## Research & Evaluation

| User's description | Industry term |
|---|---|
| "compared models fairly" | Benchmarking / Standardized Evaluation |
| "checked if model is biased" | Fairness / Bias Auditing |
| "explained model decisions" | Interpretability / Explainability (XAI) |
| "tested on unseen data" | Held-out Evaluation / Cross-validation |
| "measured multiple metrics" | Multi-objective Evaluation |
| "reproduced someone's results" | Reproducibility / Experiment Tracking |
| "tried many model configs" | Hyperparameter Search (Grid, Bayesian, Random) |
| "checked model on different groups" | Disaggregated / Subgroup Evaluation |
| "stress-tested the model" | Adversarial Robustness Testing |
| "ran ablation studies" | Ablation Analysis / Component Attribution |

## Foundation Models & LLMOps

| User's description | Industry term |
|---|---|
| "tuned prompts instead of retraining" | Prompt Engineering / In-context Learning |
| "adapted a base model with small updates" | Fine-tuning / Parameter-efficient Fine-tuning (PEFT, LoRA) |
| "connected the model to documents or search" | Retrieval-Augmented Generation (RAG) |
| "let the model use tools or APIs" | Tool Calling / Agentic Workflow Orchestration |
| "kept prompts and outputs versioned" | LLMOps / Prompt Versioning |
| "checked whether answers stayed grounded in sources" | Groundedness / Faithfulness Evaluation |
| "reduced hallucinations" | Hallucination Mitigation / Guardrailed Generation |
| "routed traffic to different models based on cost or speed" | Model Routing / Cost-performance Optimization |
| "served many requests with batching or cache reuse" | Continuous Batching / Inference Caching |
| "added safety filters before or after generation" | Safety Guardrails / Content Moderation Layer |

## Algorithms, Theory & Representation Learning

| User's description | Industry term |
|---|---|
| "learned useful features automatically" | Representation Learning |
| "used labels for some data but not all of it" | Semi-supervised Learning |
| "learned from unlabeled data first" | Self-supervised / Unsupervised Learning |
| "adapted quickly to new tasks with little data" | Meta-learning / Few-shot Learning |
| "transferred knowledge from one task to another" | Transfer Learning / Lifelong Learning |
| "generated new samples instead of only predicting labels" | Generative Modeling |
| "modeled uncertainty instead of one fixed answer" | Uncertainty Quantification / Probabilistic Modeling |
| "captured cause and effect rather than only correlation" | Causal Representation / Causal Inference |
| "analyzed why the model generalizes" | Generalization Analysis / Learning Theory |
| "studied what assumptions make the algorithm work" | Theoretical Guarantees / Assumption-driven Analysis |
| "used Bayesian or variational techniques" | Bayesian Methods / Variational Inference |
| "worked on graph-structured or non-Euclidean inputs" | Geometric Learning / Learning on Graphs |
| "studied kernels, metrics, or similarity functions" | Kernel Methods / Metric Learning |
| "focused on outputs with structure or constraints" | Structured Prediction / Compositional Modeling |
| "tested learned representations across modalities" | Multimodal Representation Learning |

## Sequential Decision-making

| User's description | Industry term |
|---|---|
| "learned by taking actions and observing rewards" | Reinforcement Learning |
| "planned over future outcomes before acting" | Planning / Model-based Decision-making |
| "studied multiple agents interacting" | Multi-agent Reinforcement Learning |
