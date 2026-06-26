# Redshift Provisioned Cluster Guide

## Overview

Amazon Redshift provisioned clusters provide dedicated compute nodes for your data warehouse workloads. You manage the cluster configuration, including node type and count.

## Cluster Lifecycle

1. **Creating** → Cluster is being provisioned
2. **Available** → Cluster is ready for queries
3. **Modifying** → Configuration change in progress
4. **Paused** → Cluster is paused (no compute charges)
5. **Resuming** → Cluster is being resumed from paused state
6. **Resizing** → Cluster resize in progress
7. **Deleting** → Cluster is being deleted

## Node Types

| Node Type | vCPU | Memory | Storage | Use Case |
|-----------|------|--------|---------|----------|
| **ra3.xlplus** | 4 | 32 GiB | 32 TB managed | Small-medium workloads |
| **ra3.4xlarge** | 12 | 96 GiB | 128 TB managed | Medium-large workloads |
| **ra3.16xlarge** | 48 | 384 GiB | 128 TB managed | Large-scale analytics |
| **dc2.large** | 2 | 15 GiB | 160 GB NVMe | Development/testing |
| **dc2.8xlarge** | 32 | 244 GiB | 2.56 TB NVMe | High-performance local storage |

**Recommendation**: Use RA3 nodes for production workloads. They use managed storage (RMS) which separates compute from storage, allowing independent scaling.

## Resize Options

### Elastic Resize
- Changes number of nodes within the same node type
- Completes in minutes
- Brief unavailability during migration
- Preferred for most resize operations

### Classic Resize
- Can change both node type and count
- Takes hours (data is redistributed)
- Cluster is read-only during resize
- Use when changing node types

## Pause and Resume

- **Pause**: Stops compute billing; storage charges continue
- **Resume**: Restarts the cluster (takes a few minutes)
- Use for dev/test clusters that don't need 24/7 availability
- Cannot pause clusters with HSM encryption or those in VPC with no public access

## Creating a Cluster

Key parameters:
- **ClusterIdentifier**: Unique name (lowercase, alphanumeric, hyphens)
- **NodeType**: Compute node type
- **NumberOfNodes**: 1 (single-node) or 2+ (multi-node)
- **MasterUsername**: Admin user name
- **MasterUserPassword**: Must contain uppercase, lowercase, and number
- **DBName**: Default database (default: "dev")
- **IamRoles**: IAM roles for S3 access (COPY/UNLOAD)

## Best Practices

1. Use RA3 nodes for production (managed storage enables independent scaling)
2. Enable encryption at rest
3. Use IAM roles instead of access keys for S3 access
4. Pause dev/test clusters when not in use
5. Use elastic resize for quick scaling
6. Monitor with CloudWatch and Redshift console
7. Enable audit logging for compliance
