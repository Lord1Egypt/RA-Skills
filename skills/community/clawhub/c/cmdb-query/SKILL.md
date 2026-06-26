---
name: cmdb-query
description: "查询 CMDB 资产数据。支持按主机、应用、数据库等资源类型查询，支持名称过滤。"
homepage: https://10.255.227.233/cmdb
metadata: { "openclaw": { "emoji": "💾", "requires": { "bins": ["curl", "jq"] } } }
---

# CMDB Query Skill

查询内部 CMDB 系统中的资产数据。

## 认证方式

通过 username/password 获取 Token，Token 有效期 8 小时。

- **登录接口**: `POST /cmdb/v1/api/oauth/token`
- **用户名**: `openclaw_read`
- **密码**: `JzXCxTaDxE`

## 资源类型 (label)

从文档中识别出的主要资源类型：

### 基础资源
- `host` - 主机
- `ali_host` - 阿里云主机
- `qingcloud_host` - 青云主机
- `hudong_host` - 互动 - 阿里云主机
- `hlw_qingcloud_host` - 互联网 - 青云主机

### 应用相关
- `application` - 应用
- `productline` - 产品线
- `product` - 产品
- `project` - 项目
- `application_site` - 站点

### 网络相关
- `balancing` - 负载均衡
- `qingcloud_slb` - 青云负载均衡
- `vpc` - VPC
- `public_IP` - 公网 IP
- `shared_bandwidth` - 共享带宽
- `nat_gateway` - NAT 网关
- `vpn_gateway` - VPN 网关
- `security_group` - 安全组
- `virtual_switch` - 虚拟交换机
- `DNS_analysis` - 云解析
- `domain` - 云资源_域名
- `CDN_domain_name` - CDN_加速域名
- `expose_networkpolicy` - 互联网暴露面资产

### 数据库
- `RDS_database` - RDS_关系型数据库
- `hudong_RDS_database` - 互动 - 阿里云 RDS
- `mongoDB` - MongoDB
- `hudong_mongoDB` - 互动 - 阿里云 MongoDB
- `polardb` - PolarDB
- `redis` - Redis
- `hudong_redis` - 互动 - 阿里云 Redis

### 缓存/消息队列
- `kafka` - Kafka
- `Hbase` - HBase
- `MQlist` - MQ 队列
- `hudong_MQlist` - 互动 - rocketMQ
- `hudong_rabbit_MQ` - 互动 - rabbitMQ
- `hudong_MQTT` - 互动 - MQTT

### 存储服务
- `oss_storage` - OSS_对象存储
- `hudong_oss_storage` - 互动 - OSS
- `Bucket_huawei` - 华为 Bucket
- `NAS_storage` - NAS 文件存储
- `cloud_disk` - Disk 云硬盘
- `hudong_cloud_disk` - 互动 - 云硬盘
- `disk_snapshot` - 硬盘快照

### 计算/容器
- `csk` - 容器服务 ACK
- `hudong_csk` - 互动 - ACK
- `E_MapReduce` - E-MapReduce
- `hudong_E_MapReduce` - 互动 - EMR

### 其他服务
- `cloud_image` - 云镜像
- `k8s` - K8S
- `Elasticsearch` - 检索分析 Elasticsearch
- `hudong_opensearch` - 互动 - Opensearch
- `SSL_ficate` - SSL_证书
- `certificate` - 证书详情
- `gateway_application` - 统一网关应用
- `centers` - 项目中心平台
- `domain_details` - 域名详情

### 堡垒机/账号
- `baolj_data` - 非强国堡垒机资源
- `Y_baolj_data` - 强国_堡垒机资源
- `sshprivatekey` - 堡垒机远程登陆私钥
- `jw_front_computer` - 经纬前置机账号
- `ziyuan_models` - 资源账号申请模型
- `ziyuan_users` - 资源账号平台用户表单
- `yewu_model` - 业务账号申请模型
- `yewu_users` - 业务账号平台用户表单

### 财务/厂商
- `bill` - 分账模型
- `manufacturer` - 厂商
- `public_manufacturer` - 公网项目云机厂商
- `public_cloudstorage` - 公网项目云存厂商

## 查询示例

### 1. 列出所有主机
```bash
curl -s -X POST "https://10.255.227.233/cmdb/v1/api/cloudresources/resource/instance/host" \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query_filter": {}, "format_user_field": "true"}' | jq '.data.items[] | {name, ip, env}'
```

### 2. 按名称模糊查询应用（含 cmdb 字样）
```bash
curl -s -X POST "https://10.255.227.233/cmdb/v1/api/cloudresources/resource/instance/application" \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query_filter": {
      "$or": [
        {"name": {"$options": "i", "$regex": "cmdb"}}
      ]
    },
    "format_user_field": "true"
  }' | jq '.data.items[] | {name, ip, env}'
```

### 3. 查询特定环境的数据库
```bash
curl -s -X POST "https://10.255.227.233/cmdb/v1/api/cloudresources/resource/instance/RDS_database" \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query_filter": {
      "$and": [
        {"environment": {"$regex": "prod"}}
      ]
    },
    "format_user_field": "true"
  }' | jq '.data.items[] | {name, env, status}'
```

## 查询语法说明

**支持的操作符**：
- `$regex` - 模糊匹配，支持正则
- `$options` - 正则选项，`i` 表示忽略大小写
- `$and` - 与条件（所有条件需满足）
- `$or` - 或条件（满足任一即可）

**示例**：
```json
{
  "query_filter": {
    "$and": [
      {"name": {"$regex": "web", "$options": "i"}},
      {"environment": "production"}
    ]
  }
}
```

## 注意事项

1. **Token 有效期 8 小时**，超过需重新登录
2. **分页**：每次查询最多返回 `page_size` 条记录，通过 `page` 参数翻页
3. **性能**：建议限制 `page_size`（默认 10），大数据量查询时分页处理
