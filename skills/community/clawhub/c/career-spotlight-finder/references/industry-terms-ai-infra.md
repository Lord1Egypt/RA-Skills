# Industry Terms: AI Infrastructure

> **Usage note:** Use this file when the target direction is AI infrastructure, ML platform, training infrastructure, model serving, or LLM platform engineering. It captures terminology specific to the **infrastructure and systems side** of AI/ML — cluster management, serving platforms, resource optimization, cost engineering. For ML algorithmic work (model development, evaluation, training techniques), use the ML file instead. Both files may be loaded together for hybrid directions.

---

## Training Infrastructure

| User's description | Industry term |
|---|---|
| "managed GPU cluster scheduling for training jobs" | Training Job Orchestration / GPU Cluster Management |
| "optimized communication patterns across GPUs" | Collective Communication Optimization (AllReduce, Pipeline Flush) |
| "chose which parallelism strategy to use (data, tensor, pipeline)" | Parallelism Strategy Selection / Hybrid Parallelism (3D/4D) |
| "reduced idle time between training steps in pipeline parallelism" | Pipeline Bubble Reduction / Training Throughput Optimization |
| "compiled or fused model operations for hardware" | Graph Compilation / Operator Fusion (XLA, TorchInductor) |
| "offloaded data to CPU or disk to fit larger models in memory" | Memory Offloading / Activation Offloading |
| "saved and restored training state across interruptions" | Distributed Checkpointing / Fault-tolerant Training |
| "managed training on spot or preemptible instances" | Spot Instance Training / Preemptible Compute Management |
| "shared GPU resources across teams or experiments" | Multi-tenant GPU Scheduling / Compute Sharing |
| "benchmarked training or inference across different system setups" | ML Systems Benchmarking / Performance Characterization |

## Serving Infrastructure

| User's description | Industry term |
|---|---|
| "built the platform that other teams use to deploy and monitor models" | ML Platform Engineering / Model Deployment Infrastructure |
| "optimized GPU memory and compute utilization during inference" | Inference Resource Optimization / GPU Utilization Management |
| "handled model loading, version switching, and warm-up in production" | Model Lifecycle Management / Hot Model Swapping |
| "built auto-scaling for inference endpoints based on traffic patterns" | Inference Auto-scaling / Serving Capacity Planning |
| "designed the request routing and load balancing for model endpoints" | Inference Load Balancing / Request Routing |
| "built observability for model serving latency, throughput, and errors" | Serving Observability / Inference SLI/SLO |
| "optimized the model for specific hardware before deployment" | Hardware-specific Model Optimization / Target-aware Compilation |
| "managed model artifact storage, retrieval, and versioning" | Model Artifact Management / Model Repository |
| "ran the model on constrained hardware or edge devices" | Edge Inference / Hardware-efficient Deployment |

## Data Infrastructure for ML

| User's description | Industry term |
|---|---|
| "built and maintained feature stores for training and serving" | Feature Store Architecture / Feature Platform |
| "managed training data versioning and reproducibility" | Training Data Management / Data Versioning Infrastructure |
| "built data quality checks and validation for ML pipelines" | ML Data Validation / Training Data Quality Gates |
| "built pipelines that move data from raw sources into training-ready formats" | ML Data Pipeline / Training Data Preparation Infrastructure |
| "managed dataset catalogs so teams could discover and reuse data" | Dataset Discovery / ML Data Catalog |

## ML Platform & Workflow

| User's description | Industry term |
|---|---|
| "built reusable pipelines for training, evaluation, and deployment" | ML Pipeline Framework / End-to-end ML Workflow |
| "managed experiment configurations and training runs at scale" | Experiment Orchestration / Training Run Management |
| "built internal tools for non-ML engineers to use ML models" | ML Democratization Tooling / Self-serve ML Platform |
| "tested, debugged, or monitored the full ML application" | End-to-end ML Application Debugging / ML Application Observability |
| "standardized how teams package and ship models" | Model Packaging Standards / ML Deployment Conventions |

## Cost & Resource Management

| User's description | Industry term |
|---|---|
| "tracked and optimized GPU or compute costs" | ML Cost Optimization / Compute Cost Attribution |
| "right-sized GPU allocations for different workloads" | GPU Resource Right-sizing / Compute Capacity Planning |
| "chose between cloud providers or instance types to reduce cost" | Multi-cloud Compute Strategy / Instance Selection Optimization |
| "monitored utilization to find idle or wasted resources" | Resource Utilization Monitoring / Waste Detection |
