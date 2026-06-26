# Redshift Snapshot Guide

## Overview

Redshift snapshots are point-in-time backups of your cluster stored in Amazon S3. They can be used to restore clusters or create new ones.

## Snapshot Types

### Automated Snapshots
- Created automatically by Redshift
- Default retention: 1 day (configurable up to 35 days)
- Deleted when the cluster is deleted (unless copied to manual)
- Cannot be shared directly

### Manual Snapshots
- Created on-demand by users
- Retained until explicitly deleted
- Can be shared with other AWS accounts
- Can be copied to other regions

## Creating Snapshots

```python
from scripts.provisioned.redshift_provisioned_cli import create_snapshot

snapshot = create_snapshot(
    snapshot_id="my-cluster-backup-20260318",
    cluster_id="my-cluster",
    retention_period=30,  # days
)
```

## Restoring from Snapshots

When restoring:
- A new cluster is created from the snapshot
- You can change node type and count during restore
- The restored cluster has the same database and users
- Restore time depends on data size

```python
from scripts.provisioned.redshift_provisioned_cli import restore_from_snapshot

restored = restore_from_snapshot(
    cluster_id="my-cluster-restored",
    snapshot_id="my-cluster-backup-20260318",
    node_type="ra3.xlplus",
    number_of_nodes=4,
)
```

## Cross-Region Snapshots

To enable disaster recovery:
1. Create a manual snapshot
2. Copy it to another region using the AWS console or API
3. Restore from the copied snapshot in the target region

## Snapshot Sharing

Manual snapshots can be shared with other AWS accounts:
1. Authorize the target account to access the snapshot
2. The target account can then restore from the shared snapshot
3. For encrypted snapshots, you must also share the KMS key

## Best Practices

1. Create manual snapshots before major changes (resize, maintenance)
2. Use meaningful snapshot names with dates
3. Set appropriate retention periods
4. Enable cross-region snapshot copy for DR
5. Regularly test snapshot restores
6. Delete old manual snapshots to reduce storage costs
7. Use final snapshots when deleting clusters
