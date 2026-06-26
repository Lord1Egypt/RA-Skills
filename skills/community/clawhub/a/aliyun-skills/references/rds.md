# RDS (ApsaraDB for RDS) Reference

RDS supports MySQL, PostgreSQL, SQL Server, MariaDB, and PolarDB-compatible engines.

## List DB Instances

```bash
aliyun rds DescribeDBInstances --RegionId cn-hangzhou
```

```bash
aliyun rds DescribeDBInstances --RegionId cn-hangzhou \
  --output 'cols=DBInstanceId,DBInstanceDescription,Engine,EngineVersion,DBInstanceStatus' \
  'rows=Items.DBInstance[]'
```

Filter by engine:
```bash
aliyun rds DescribeDBInstances --RegionId cn-hangzhou --Engine MySQL
```

## Get Instance Details

```bash
aliyun rds DescribeDBInstanceAttribute \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx
```

---

## Create a DB Instance

```bash
aliyun rds CreateDBInstance \
  --RegionId cn-hangzhou \
  --Engine MySQL \
  --EngineVersion 8.0 \
  --DBInstanceClass rds.mysql.s1.small \
  --DBInstanceStorage 20 \
  --DBInstanceStorageType cloud_essd \
  --DBInstanceNetType Intranet \
  --VPCId vpc-xxxxxx \
  --VSwitchId vsw-xxxxxx \
  --SecurityIPList "10.0.0.0/8" \
  --DBInstanceDescription "My MySQL instance" \
  --PayType Postpaid
```

## Delete a DB Instance

> ⚠️ Create a final backup before deleting. This action is irreversible.

```bash
# Create a final backup first
aliyun rds CreateBackup --RegionId cn-hangzhou --DBInstanceId rm-xxxxxx

# Then delete
aliyun rds DeleteDBInstance --RegionId cn-hangzhou --DBInstanceId rm-xxxxxx
```

---

## Databases

### List Databases in an Instance

```bash
aliyun rds DescribeDatabases \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx
```

### Create a Database

```bash
aliyun rds CreateDatabase \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --DBName mydb \
  --CharacterSetName utf8mb4 \
  --DBDescription "My application database"
```

### Delete a Database

```bash
aliyun rds DeleteDatabase \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --DBName mydb
```

---

## Accounts

### List Accounts

```bash
aliyun rds DescribeAccounts \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx
```

### Create an Account

```bash
aliyun rds CreateAccount \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --AccountName appuser \
  --AccountPassword "P@ssw0rd!" \
  --AccountType Normal \
  --AccountDescription "Application user"
```

### Grant Database Privileges

```bash
aliyun rds GrantAccountPrivilege \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --AccountName appuser \
  --DBName mydb \
  --AccountPrivilege ReadWrite
```

### Reset Account Password

```bash
aliyun rds ResetAccountPassword \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --AccountName appuser \
  --AccountPassword "NewP@ss!"
```

---

## Network & Security

### List IP Whitelists

```bash
aliyun rds DescribeDBInstanceIPArrayList \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx
```

### Modify IP Whitelist

```bash
aliyun rds ModifySecurityIps \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --SecurityIps "10.0.0.0/8,192.168.1.100"
```

### Get Connection Strings

```bash
aliyun rds DescribeDBInstanceNetInfo \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx
```

### Allocate a Public Endpoint

```bash
aliyun rds AllocateInstancePublicConnection \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --ConnectionStringPrefix my-rds-public \
  --Port 3306
```

---

## Backups

### Create a Manual Backup

```bash
aliyun rds CreateBackup \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --BackupMethod Physical
```

### List Backups

```bash
aliyun rds DescribeBackups \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx
```

### Modify Backup Policy (Automated Backups)

```bash
aliyun rds ModifyBackupPolicy \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --PreferredBackupTime "02:00Z-03:00Z" \
  --PreferredBackupPeriod "Monday,Wednesday,Friday" \
  --BackupRetentionPeriod 7
```

---

## Instance Spec Change

```bash
aliyun rds ModifyDBInstanceSpec \
  --RegionId cn-hangzhou \
  --DBInstanceId rm-xxxxxx \
  --DBInstanceClass rds.mysql.s2.large \
  --DBInstanceStorage 50
```

---

## Instance Status Values

| Status | Meaning |
|--------|---------|
| `Running` | Normal operation |
| `Creating` | Being provisioned |
| `Rebooting` | Restart in progress |
| `DBInstanceClassChanging` | Spec change in progress |
| `GuardSwitching` | HA failover in progress |
| `Deleting` | Being deleted |

---

## Common Engine Versions

| Engine | Supported Versions |
|--------|-------------------|
| MySQL | 5.7, 8.0 |
| PostgreSQL | 14, 15, 16 |
| SQL Server | 2019_std, 2019_ent |
| MariaDB | 10.3 |
