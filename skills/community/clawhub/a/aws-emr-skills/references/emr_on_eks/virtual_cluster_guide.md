# EMR On EKS Virtual Cluster Management Guide

## Overview

EMR on EKS runs Spark workloads on Amazon EKS (Elastic Kubernetes Service). A **virtual cluster** is the EMR abstraction that maps to a Kubernetes namespace on an EKS cluster.

## Available Operations

All operations are available via `@tool` functions in `scripts/on_eks/emr_on_eks_cli.py`.

### 1. List Virtual Clusters

```python
list_eks_virtual_clusters(
    states=["RUNNING"],                              # optional
    container_provider_id="my-eks-cluster-id",       # optional, filter by EKS cluster
    max_results=50                                    # optional
)
```

**Returns:** List of virtual cluster dicts with keys: `id`, `name`, `arn`, `state`, `container_provider_type`, `container_provider_id`, `namespace`, `created_at`, `tags`.

### 2. Describe Virtual Cluster

```python
describe_eks_virtual_cluster(virtual_cluster_id="abc123def456")
```

**Returns:** Detailed virtual cluster dict.

### 3. Create Virtual Cluster

```python
create_eks_virtual_cluster(
    name="my-virtual-cluster",
    eks_cluster_id="my-eks-cluster",
    namespace="spark-jobs",
    tags={"env": "production"}                       # optional
)
```

**Returns:** `{"id": "...", "name": "...", "arn": "..."}`

> **Prerequisites:** The EKS cluster must have the EMR on EKS namespace configured with appropriate RBAC roles. See [AWS EMR on EKS Setup Guide](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/setting-up.html).

### 4. Delete Virtual Cluster

```python
delete_eks_virtual_cluster(virtual_cluster_id="abc123def456")
```

**Returns:** `{"id": "...", "status": "delete_requested"}`

## Virtual Cluster States

| State | Description |
|---|---|
| `RUNNING` | Virtual cluster is active and can accept job runs |
| `TERMINATING` | Virtual cluster is being deleted |
| `TERMINATED` | Virtual cluster has been deleted |
| `ARRESTED` | Virtual cluster is in an error state |

## Configuration

| Environment Variable | Description | Required |
|---|---|---|
| `AWS_REGION` | AWS region | No (default: us-east-1) |
| `EMR_EKS_VIRTUAL_CLUSTER_ID` | Default virtual cluster ID | No (pass per-call) |

AWS credentials are resolved via boto3 default credential chain.
