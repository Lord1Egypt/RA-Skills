# Redshift Serverless Workgroup Guide

## Overview

A workgroup is a collection of compute resources in Redshift Serverless. It defines the compute capacity (measured in RPUs) and network configuration for your queries.

## Workgroup Lifecycle

1. **CREATING** → Workgroup is being provisioned
2. **AVAILABLE** → Ready for queries
3. **MODIFYING** → Configuration change in progress
4. **DELETING** → Being deleted

## RPU (Redshift Processing Units)

- Measured in RPU: 8 to 512 (increments of 8)
- Default base capacity: 128 RPU
- **Base capacity**: Minimum RPU allocation
- **Max capacity**: Upper limit for auto-scaling (optional)
- Redshift Serverless automatically scales within the range
- You are billed per RPU-hour for the compute used

### RPU Sizing Guidelines

| Workload | Recommended RPU | Use Case |
|----------|----------------|----------|
| 8–32 | Light | Development, testing, small queries |
| 32–128 | Medium | Production dashboards, moderate concurrency |
| 128–256 | Heavy | Large-scale analytics, high concurrency |
| 256–512 | Intensive | Complex ETL, large data volumes |

## Creating a Workgroup

Key parameters:
- **workgroupName**: Unique name
- **namespaceName**: Must be associated with an existing namespace
- **baseCapacity**: Starting RPU capacity
- **maxCapacity**: Optional upper limit
- **publiclyAccessible**: Whether accessible from outside VPC
- **securityGroupIds**: VPC security groups
- **subnetIds**: VPC subnets (minimum 3 in different AZs)
- **enhancedVpcRouting**: Force traffic through VPC

## Updating a Workgroup

You can update:
- Base capacity (RPU)
- Max capacity
- Public accessibility
- Enhanced VPC routing
- Security groups and subnets

Changes take effect within minutes.

## Best Practices

1. Start with a moderate base capacity and adjust based on performance
2. Set max capacity to control costs
3. Use enhanced VPC routing for security-sensitive workloads
4. Place workgroups in private subnets with NAT for S3 access
5. Monitor RPU usage with CloudWatch metrics
6. Use multiple workgroups for workload isolation (dev vs prod)
