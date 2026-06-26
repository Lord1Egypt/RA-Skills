# VPC (Virtual Private Cloud) Reference

## List VPCs

```bash
aliyun vpc DescribeVpcs --RegionId cn-hangzhou
```

Filter by name:
```bash
aliyun vpc DescribeVpcs --RegionId cn-hangzhou --VpcName my-vpc
```

Tabular output:
```bash
aliyun vpc DescribeVpcs --RegionId cn-hangzhou \
  --output 'cols=VpcId,VpcName,CidrBlock,Status' 'rows=Vpcs.Vpc[]'
```

## Create a VPC

```bash
aliyun vpc CreateVpc \
  --RegionId cn-hangzhou \
  --CidrBlock 10.0.0.0/16 \
  --VpcName my-vpc \
  --Description "Production VPC"
```

## Delete a VPC

> Requires all VSwitches inside to be deleted first.

```bash
aliyun vpc DeleteVpc --RegionId cn-hangzhou --VpcId vpc-xxxxxx
```

---

## VSwitches (Subnets)

### List VSwitches

```bash
aliyun vpc DescribeVSwitches --RegionId cn-hangzhou --VpcId vpc-xxxxxx
```

```bash
aliyun vpc DescribeVSwitches --RegionId cn-hangzhou \
  --output 'cols=VSwitchId,VSwitchName,CidrBlock,ZoneId,AvailableIpAddressCount' 'rows=VSwitches.VSwitch[]'
```

### Create a VSwitch

```bash
aliyun vpc CreateVSwitch \
  --RegionId cn-hangzhou \
  --VpcId vpc-xxxxxx \
  --ZoneId cn-hangzhou-g \
  --CidrBlock 10.0.1.0/24 \
  --VSwitchName my-vswitch
```

### Delete a VSwitch

```bash
aliyun vpc DeleteVSwitch --RegionId cn-hangzhou --VSwitchId vsw-xxxxxx
```

---

## EIP (Elastic IP)

### List EIPs

```bash
aliyun vpc DescribeEipAddresses --RegionId cn-hangzhou
```

```bash
aliyun vpc DescribeEipAddresses --RegionId cn-hangzhou \
  --output 'cols=AllocationId,IpAddress,Status,InstanceId' 'rows=EipAddresses.EipAddress[]'
```

### Allocate an EIP

```bash
aliyun vpc AllocateEipAddress \
  --RegionId cn-hangzhou \
  --Bandwidth 5 \
  --InternetChargeType PayByTraffic
```

### Bind EIP to an ECS Instance

```bash
aliyun vpc AssociateEipAddress \
  --RegionId cn-hangzhou \
  --AllocationId eip-xxxxxx \
  --InstanceId i-xxxxxx \
  --InstanceType EcsInstance
```

### Unbind EIP

```bash
aliyun vpc UnassociateEipAddress \
  --RegionId cn-hangzhou \
  --AllocationId eip-xxxxxx
```

### Release EIP

> ⚠️ This is irreversible — confirm the EIP is unbound and no longer needed.

```bash
aliyun vpc ReleaseEipAddress \
  --RegionId cn-hangzhou \
  --AllocationId eip-xxxxxx
```

---

## NAT Gateway

### List NAT Gateways

```bash
aliyun vpc DescribeNatGateways --RegionId cn-hangzhou --VpcId vpc-xxxxxx
```

### Create a NAT Gateway

```bash
aliyun vpc CreateNatGateway \
  --RegionId cn-hangzhou \
  --VpcId vpc-xxxxxx \
  --VSwitchId vsw-xxxxxx \
  --NatType Enhanced \
  --InternetChargeType PayByLcu \
  --Name my-nat
```

---

## Route Tables

### List Route Tables

```bash
aliyun vpc DescribeRouteTables --RegionId cn-hangzhou --VpcId vpc-xxxxxx
```

### Describe Route Entries

```bash
aliyun vpc DescribeRouteEntryList \
  --RegionId cn-hangzhou \
  --RouteTableId rtb-xxxxxx
```

---

## VPC Status Values

| Status | Meaning |
|--------|---------|
| `Pending` | Being created |
| `Available` | Ready to use |
