# Aliyun CLI — ECS (Elastic Compute Service)

## Listing & Querying Instances

### List all instances in a region
```bash
aliyun ecs DescribeInstances \
  --RegionId cn-hangzhou \
  --output cols=InstanceId,InstanceName,Status,InstanceType,PublicIpAddress
```

### Filter by instance name (fuzzy match)
```bash
aliyun ecs DescribeInstances \
  --RegionId cn-hangzhou \
  --InstanceName "web-*" \
  --output cols=InstanceId,InstanceName,Status
```

### Get details of a specific instance
```bash
aliyun ecs DescribeInstanceAttribute \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx
```

### List instances with full pagination (up to 100 per page)
```bash
aliyun ecs DescribeInstances \
  --RegionId cn-hangzhou \
  --PageSize 100 \
  --PageNumber 1
```

### Check instance status
```bash
aliyun ecs DescribeInstanceStatus \
  --RegionId cn-hangzhou \
  --InstanceId.1 i-bp1xxxxxxxxxxxxxxx
```

---

## Start / Stop / Reboot

### Start an instance
```bash
aliyun ecs StartInstance \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx
```

### Stop an instance (graceful shutdown)
```bash
aliyun ecs StopInstance \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx \
  --StoppedMode KeepCharging
```
- `StoppedMode=KeepCharging` — instance keeps billing (resumes faster)
- `StoppedMode=StopCharging` — stops billing (takes longer to resume, not available for all instance types)

### Force stop (equivalent to power off)
```bash
aliyun ecs StopInstance \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx \
  --ForceStop true
```

### Reboot
```bash
aliyun ecs RebootInstance \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx
```

### Reboot with force (if OS is unresponsive)
```bash
aliyun ecs RebootInstance \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx \
  --ForceReboot true
```

---

## Disk Operations

### List disks for an instance
```bash
aliyun ecs DescribeDisks \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx \
  --output cols=DiskId,DiskName,Size,Category,Status,Type
```
- `Type=system` — system disk
- `Type=data` — data disk

### List all disks in a region
```bash
aliyun ecs DescribeDisks \
  --RegionId cn-hangzhou \
  --output cols=DiskId,DiskName,Size,Status,InstanceId
```

### Expand (resize) a disk — online resize (no reboot needed for Linux ≥ kernel 3.6)
```bash
# Step 1: Resize the cloud disk
aliyun ecs ResizeDisk \
  --RegionId cn-hangzhou \
  --DiskId d-bp1xxxxxxxxxxxxxxx \
  --NewSize 200 \
  --Type online
```
- `NewSize` is in GiB, must be larger than current size
- After resize, you still need to extend the filesystem inside the OS:
  ```bash
  # For Linux with ext4
  sudo resize2fs /dev/vdb
  # For Linux with xfs
  sudo xfs_growfs /mount/point
  # For system disk with growpart
  sudo growpart /dev/vda 1 && sudo resize2fs /dev/vda1
  ```

### Offline resize (requires stopping the instance first)
```bash
aliyun ecs ResizeDisk \
  --RegionId cn-hangzhou \
  --DiskId d-bp1xxxxxxxxxxxxxxx \
  --NewSize 200 \
  --Type offline
```

### Create and attach a new data disk
```bash
# Create disk
aliyun ecs CreateDisk \
  --RegionId cn-hangzhou \
  --ZoneId cn-hangzhou-i \
  --Size 100 \
  --DiskCategory cloud_essd \
  --DiskName "my-data-disk"

# Attach to instance
aliyun ecs AttachDisk \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx \
  --DiskId d-bp1xxxxxxxxxxxxxxx
```

### Detach a disk
```bash
aliyun ecs DetachDisk \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx \
  --DiskId d-bp1xxxxxxxxxxxxxxx
```

---

## Snapshots

### Create a snapshot
```bash
aliyun ecs CreateSnapshot \
  --RegionId cn-hangzhou \
  --DiskId d-bp1xxxxxxxxxxxxxxx \
  --SnapshotName "before-upgrade-2024"
```

### List snapshots
```bash
aliyun ecs DescribeSnapshots \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx \
  --output cols=SnapshotId,SnapshotName,Status,CreationTime,SourceDiskSize
```

### Delete a snapshot
```bash
aliyun ecs DeleteSnapshot \
  --RegionId cn-hangzhou \
  --SnapshotId s-bp1xxxxxxxxxxxxxxx
```

---

## Instance Type & Spec Changes

### List available instance types (filtered by CPU/memory)
```bash
aliyun ecs DescribeInstanceTypes \
  --MinimumCpuCoreCount 4 \
  --MinimumMemorySize 8 \
  --output cols=InstanceTypeId,CpuCoreCount,MemorySize,NetworkMaximumBandwidth
```

### Change instance type (instance must be stopped)
```bash
# Stop first
aliyun ecs StopInstance --RegionId cn-hangzhou --InstanceId i-bp1xxx

# Modify spec
aliyun ecs ModifyInstanceSpec \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx \
  --InstanceType ecs.c6.2xlarge

# Start again
aliyun ecs StartInstance --RegionId cn-hangzhou --InstanceId i-bp1xxx
```

---

## Security Groups

### List security groups
```bash
aliyun ecs DescribeSecurityGroups \
  --RegionId cn-hangzhou \
  --output cols=SecurityGroupId,SecurityGroupName,Description
```

### View rules in a security group
```bash
aliyun ecs DescribeSecurityGroupAttribute \
  --RegionId cn-hangzhou \
  --SecurityGroupId sg-bp1xxxxxxxxxxxxxxx
```

### Add an inbound rule (allow SSH from a specific IP)
```bash
aliyun ecs AuthorizeSecurityGroup \
  --RegionId cn-hangzhou \
  --SecurityGroupId sg-bp1xxxxxxxxxxxxxxx \
  --IpProtocol tcp \
  --PortRange 22/22 \
  --SourceCidrIp 203.0.113.0/24 \
  --Description "Allow SSH from office"
```

### Add an outbound rule
```bash
aliyun ecs AuthorizeSecurityGroupEgress \
  --RegionId cn-hangzhou \
  --SecurityGroupId sg-bp1xxxxxxxxxxxxxxx \
  --IpProtocol tcp \
  --PortRange 443/443 \
  --DestCidrIp 0.0.0.0/0
```

### Revoke (remove) a rule
```bash
aliyun ecs RevokeSecurityGroup \
  --RegionId cn-hangzhou \
  --SecurityGroupId sg-bp1xxxxxxxxxxxxxxx \
  --IpProtocol tcp \
  --PortRange 22/22 \
  --SourceCidrIp 203.0.113.0/24
```

---

## Images

### List available system images (official)
```bash
aliyun ecs DescribeImages \
  --RegionId cn-hangzhou \
  --ImageOwnerAlias system \
  --OSType linux \
  --output cols=ImageId,ImageName,OSName,CreationTime \
  --PageSize 50
```

### List your custom images
```bash
aliyun ecs DescribeImages \
  --RegionId cn-hangzhou \
  --ImageOwnerAlias self \
  --output cols=ImageId,ImageName,Status,CreationTime
```

### Create a custom image from an instance
```bash
aliyun ecs CreateImage \
  --RegionId cn-hangzhou \
  --InstanceId i-bp1xxxxxxxxxxxxxxx \
  --ImageName "my-app-image-v2" \
  --Description "Production app server snapshot"
```

---

## Key Pairs (SSH)

### List key pairs
```bash
aliyun ecs DescribeKeyPairs \
  --RegionId cn-hangzhou \
  --output cols=KeyPairName,KeyPairFingerPrint,CreationTime
```

### Create a key pair (private key returned once — save it!)
```bash
aliyun ecs CreateKeyPair \
  --RegionId cn-hangzhou \
  --KeyPairName my-key-pair
```

### Attach key pair to instance (takes effect on next boot)
```bash
aliyun ecs AttachKeyPair \
  --RegionId cn-hangzhou \
  --KeyPairName my-key-pair \
  --InstanceIds '["i-bp1xxxxxxxxxxxxxxx"]'
```

---

## Common Instance States

| Status | Description |
|--------|-------------|
| `Running` | Instance is running |
| `Stopped` | Instance is stopped |
| `Starting` | Instance is starting up |
| `Stopping` | Instance is shutting down |
| `Pending` | Instance is being created |

Operations that require `Stopped`: `ResizeDisk` (offline), `ModifyInstanceSpec`
Operations that require `Running`: `RebootInstance`, terminal connections
