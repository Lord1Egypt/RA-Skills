# DescribeRCInstances API 参考

## API 信息

- **产品**: RDS (云数据库)
- **API 版本**: 2014-08-15
- **Endpoint**: rds.aliyuncs.com
- **HTTP Method**: POST

## CLI 调用方式

### 基本语法

```bash
aliyun rds DescribeRCInstances --region <地域 ID> [参数]
```

### 常用参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --region | String | 是 | 地域 ID，如 cn-beijing |
| --PageNumber | Integer | 否 | 页码，默认 1 |
| --PageSize | Integer | 否 | 每页数量，默认 500 |
| --InstanceId | String | 否 | 实例 ID 过滤 |

## 响应参数

### 根节点

| 参数 | 类型 | 说明 |
|------|------|------|
| RequestId | String | 请求 ID |
| TotalCount | Integer | 总记录数 |
| PageNumber | Integer | 页码 |
| PageSize | Integer | 每页数量 |
| RCInstances | Array | 实例集合 |

### RCInstances 结构

| 参数 | 类型 | 说明 |
|------|------|------|
| InstanceId | String | 实例 ID |
| InstanceName | String | 实例名称 |
| ClusterName | String | 集群名称 |
| Status | String | 实例状态 |
| Cpu | Integer | CPU 核数 |
| Memory | Integer | 内存 (MB) |
| RegionId | String | 地域 ID |
| ZoneId | String | 可用区 ID |
| GmtCreated | String | 创建时间 |
| ExpiredTime | String | 到期时间 |
| InstanceChargeType | String | 计费类型 |
| AutoRenew | Boolean | 是否自动续费 |
| VpcAttributes | Object | VPC 信息 |
| VpcId | String | VPC ID |
| PrivateIpAddress | Array | 私网 IP 列表 |

## 错误码

| 错误码 | 说明 |
|--------|------|
| InvalidAccessKeyId.NotFound | AccessKey ID 不存在 |
| InvalidRegionId.NotFound | 地域 ID 无效 |
| Forbidden.RiskControl | 风控限制 |
| InternalError | 内部错误 |

## 使用示例

### CLI 查询

```bash
# 基本查询
aliyun rds DescribeRCInstances --region cn-beijing

# 格式化输出
aliyun rds DescribeRCInstances --region cn-beijing --output cols=InstanceId,InstanceName,Status

# 使用 jq 过滤
aliyun rds DescribeRCInstances --region cn-beijing | jq '.RCInstances[] | {InstanceId, Status}'
```

### 脚本调用

```bash
#!/bin/bash
REGION="cn-beijing"
RESULT=$(aliyun rds DescribeRCInstances --region "$REGION")
TOTAL=$(echo "$RESULT" | jq '.TotalCount')
echo "共有 $TOTAL 台 RC 实例"
```

## 相关 API

- DescribeDBInstances - 查询 RDS 实例列表
- DescribeDBInstanceAttribute - 查询实例详细信息
- CreateDBInstance - 创建实例
- DeleteDBInstance - 删除实例

## 地域列表

| 地域 | 地域 ID |
|------|--------|
| 华北 1（青岛） | cn-qingdao |
| 华北 2（北京） | cn-beijing |
| 华北 3（张家口） | cn-zhangjiakou |
| 华东 1（杭州） | cn-hangzhou |
| 华东 2（上海） | cn-shanghai |
| 华南 1（深圳） | cn-shenzhen |
| 华南 2（河源） | cn-heyuan |
| 西南 1（成都） | cn-chengdu |
