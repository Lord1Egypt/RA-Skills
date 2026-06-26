# Redshift Serverless Namespace Guide

## Overview

A namespace is a collection of database objects and users in Redshift Serverless. It contains the database, schemas, tables, and user credentials. Namespaces are associated with workgroups for compute.

## Namespace Lifecycle

1. **CREATING** → Namespace is being provisioned
2. **AVAILABLE** → Ready for use
3. **MODIFYING** → Configuration change in progress
4. **DELETING** → Being deleted

## Namespace vs Workgroup

| Component | Namespace | Workgroup |
|-----------|-----------|-----------|
| Contains | Database, users, schemas, tables | Compute resources (RPU) |
| Billing | Storage costs | Compute costs (RPU-hours) |
| Relationship | One namespace → one or more workgroups | One workgroup → one namespace |

## Creating a Namespace

Key parameters:
- **namespaceName**: Unique name
- **dbName**: Default database name (default: "dev")
- **adminUsername**: Admin user name
- **adminUserPassword**: Admin user password
- **iamRoles**: IAM roles for S3 access
- **defaultIamRoleArn**: Default IAM role
- **kmsKeyId**: KMS key for encryption at rest
- **logExports**: Log types to export to CloudWatch

### Log Export Types

- `useractivitylog` — Logs each query before it's run
- `userlog` — Logs user connection/disconnection and changes
- `connectionlog` — Logs authentication attempts

## IAM Roles

Namespaces need IAM roles for:
- COPY/UNLOAD operations (S3 access)
- Spectrum (querying S3 directly)
- Federated queries (accessing RDS/Aurora)
- Zero-ETL integrations
- ML model creation (SageMaker access)

## Encryption

- Encryption at rest is always enabled for Redshift Serverless
- Default: AWS managed key
- Optional: Customer managed KMS key (specified via kmsKeyId)
- Cannot change encryption key after namespace creation

## Best Practices

1. Use meaningful namespace names that reflect the workload
2. Always set an admin user with a strong password
3. Attach IAM roles at namespace creation for S3 access
4. Enable log exports for audit and debugging
5. Use customer managed KMS keys for sensitive data
6. Create snapshots before deleting namespaces
