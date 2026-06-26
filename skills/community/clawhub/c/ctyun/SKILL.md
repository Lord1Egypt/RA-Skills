---
name: ctyun-cli
description: "天翼云CLI工具 - 企业级命令行工具，帮助您轻松管理天翼云资源。支持ECS、VPC、EBS、ELB、CCE、Redis、Kafka、CSS、EMR、监控、账务、IAM、Aone、CloudPC、AIServer等17大服务模块，覆盖397+个API，383+个命令。"
homepage: https://github.com/fengyucn/ctyun-cli
pypi: https://pypi.org/project/ctyun-cli/
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["ctyun-cli"]},"install":[{"id":"pip","kind":"pip","package":"ctyun-cli","bins":["ctyun-cli"],"label":"Install ctyun-cli (pip)"}]}}
---

# 天翼云 CLI (ctyun-cli)

天翼云 CLI 工具，功能强大的企业级命令行工具，帮助您轻松管理天翼云资源。支持云服务器(ECS)、监控告警、安全防护、Redis分布式缓存、弹性负载均衡(ELB)、容器引擎(CCE)、VPC网络、费用查询等核心功能。

**规模统计：** 43,000+行代码，397+个API，383+个命令，17大服务模块

## 安装

### 使用 pip 安装（推荐）
```bash
pip install ctyun-cli
```

### 使用 pipx 安装（隔离环境）
```bash
pipx install ctyun-cli
```

### 从源码安装
```bash
git clone https://github.com/fengyucn/ctyun-cli.git
cd ctyun-cli
pip install -e .
```

### 验证安装
```bash
ctyun-cli --version
ctyun-cli --help
```

## 配置与认证

### 方式一：环境变量（推荐，更安全）
```bash
export CTYUN_ACCESS_KEY=your_access_key
export CTYUN_SECRET_KEY=your_secret_key
```

将上述命令添加到 `~/.bashrc` 或 `~/.zshrc` 以实现永久配置。

### 方式二：交互式配置
```bash
ctyun-cli configure --access-key YOUR_ACCESS_KEY --secret-key YOUR_SECRET_KEY --region cn-north-1
```

### 查看当前配置
```bash
ctyun-cli show-config
```

### 列出所有配置文件
```bash
ctyun-cli list-profiles
```

### 测试 API 连接
```bash
ctyun-cli test
```

## 全局选项

所有命令都支持以下全局选项：
- `--profile TEXT`: 指定配置文件名称
- `--access-key TEXT`: 访问密钥
- `--secret-key TEXT`: 密钥
- `--region TEXT`: 区域
- `--endpoint TEXT`: API 端点
- `--output [table|json|yaml]`: 输出格式（默认 table）
- `--debug`: 启用调试模式

## 云服务器 (ECS) 管理

### 列出云主机实例
```bash
ctyun-cli ecs list
ctyun-cli ecs list --region cn-north-1 --output json
```

### 查询云主机详情
```bash
ctyun-cli ecs detail --instance-id YOUR_INSTANCE_ID
```

### 查询多台云主机详细信息
```bash
ctyun-cli ecs multidetail --instance-ids ID1,ID2,ID3
```

### 查询云主机统计信息
```bash
ctyun-cli ecs statistics
```

### 查询资源池列表
```bash
ctyun-cli ecs regions
```

### 订单询价
```bash
ctyun-cli ecs query-price --flavor-id FLAVOR_ID --quantity 1
```

## 虚拟私有云 (VPC) 管理

### 列出 VPC
```bash
ctyun-cli vpc list
ctyun-cli vpc new-list
```

### 查询 VPC 详情
```bash
ctyun-cli vpc show --vpc-id YOUR_VPC_ID
```

### 子网查询
```bash
ctyun-cli vpc subnet --vpc-id YOUR_VPC_ID
```

### 安全组查询
```bash
ctyun-cli vpc security --vpc-id YOUR_VPC_ID
```

### 路由表查询
```bash
ctyun-cli vpc route-table --vpc-id YOUR_VPC_ID
```

### 弹性公网 IP 查询
```bash
ctyun-cli vpc eip
```

### NAT 网关查询
```bash
ctyun-cli vpc nat-gateway
```

### VPC 对等连接查询
```bash
ctyun-cli vpc peering
```

### 流日志查询
```bash
ctyun-cli vpc flow-log
```

## 云硬盘 (EBS) 管理

### 列出云硬盘
```bash
ctyun-cli ebs list
ctyun-cli ebs list --region cn-north-1 --output json
```

## 弹性负载均衡 (ELB) 管理

### 负载均衡器管理
```bash
ctyun-cli elb loadbalancer --help
ctyun-cli elb loadbalancer list
```

### 监听器管理
```bash
ctyun-cli elb listener --help
```

### 目标组管理
```bash
ctyun-cli elb targetgroup --help
```

### 健康检查管理
```bash
ctyun-cli elb health-check --help
```

### 监控数据管理
```bash
ctyun-cli elb monitor --help
```

## 容器引擎 (CCE) 管理

### 列出集群
```bash
ctyun-cli cce list-clusters
```

### 查询集群详情
```bash
ctyun-cli cce describe-cluster --cluster-id YOUR_CLUSTER_ID
```

### 获取 Kubeconfig
```bash
ctyun-cli cce get-kubeconfig --cluster-id YOUR_CLUSTER_ID
```

### 列出节点
```bash
ctyun-cli cce list-nodes --cluster-id YOUR_CLUSTER_ID
```

### 查询节点详情
```bash
ctyun-cli cce get-node-detail --cluster-id CLUSTER_ID --node-id NODE_ID
```

### 列出 Pod
```bash
ctyun-cli cce list-pods --cluster-id CLUSTER_ID
```

### 列出 Deployment
```bash
ctyun-cli cce list-deployments --cluster-id CLUSTER_ID
```

### 列出 Service
```bash
ctyun-cli cce list-services --cluster-id CLUSTER_ID
```

### 集群日志管理
```bash
ctyun-cli cce logs --help
```

### 节点池管理
```bash
ctyun-cli cce nodepool --help
```

### 弹性伸缩管理
```bash
ctyun-cli cce autoscaling --help
```

### ConfigMap 管理
```bash
ctyun-cli cce configmap --help
```

### 标签管理
```bash
ctyun-cli cce tag --help
```

### Namespace 命名空间管理
```bash
# 列出命名空间
ctyun-cli cce namespace list --cluster-id CLUSTER_ID --region-id REGION_ID

# 查询命名空间详情
ctyun-cli cce namespace show --cluster-id CLUSTER_ID --namespace-name default --region-id REGION_ID

# 创建命名空间
ctyun-cli cce namespace create --cluster-id CLUSTER_ID --region-id REGION_ID --namespace-yaml "apiVersion: v1
kind: Namespace
metadata:
  name: my-namespace"

# 更新命名空间
ctyun-cli cce namespace update --cluster-id CLUSTER_ID --namespace-name my-namespace --region-id REGION_ID --namespace-yaml "apiVersion: v1
kind: Namespace
metadata:
  name: my-namespace
  labels:
    env: production"

# 删除命名空间
ctyun-cli cce namespace delete --cluster-id CLUSTER_ID --namespace-name my-namespace --region-id REGION_ID
```

## Redis 分布式缓存服务

### 列出 Redis 实例
```bash
ctyun-cli redis list
```

### 查询实例详情
```bash
ctyun-cli redis describe --instance-id YOUR_INSTANCE_ID
ctyun-cli redis describe -i YOUR_INSTANCE_ID -f table
```

### 查询实例网络信息
```bash
ctyun-cli redis network --instance-id YOUR_INSTANCE_ID
ctyun-cli redis network -i YOUR_INSTANCE_ID --region-id RESOURCE_POOL_ID
```

### 查询实例逻辑拓扑
```bash
ctyun-cli redis topology --instance-id YOUR_INSTANCE_ID
```

### 批量查询集群节点信息
```bash
ctyun-cli redis cluster-nodes
ctyun-cli redis cluster-nodes --page 1 --size 20
```

### 创建 Redis 实例
```bash
ctyun-cli redis create-instance --help
```

### 查询可用区
```bash
ctyun-cli redis zones
```

### 查询引擎版本
```bash
ctyun-cli redis engine-version --instance-id INSTANCE_ID
ctyun-cli redis instance-version --instance-id INSTANCE_ID
```

### 监控数据查询
```bash
ctyun-cli redis monitor-history --instance-id INSTANCE_ID
```

### 诊断服务
```bash
ctyun-cli redis diagnose --instance-id INSTANCE_ID
```

### 客户端连接管理
```bash
ctyun-cli redis clients --instance-id INSTANCE_ID
```

## 云监控服务管理

### 查询监控数据
```bash
ctyun-cli monitor list
```

### 查询告警规则
```bash
ctyun-cli monitor query-alarm-rules
```

### 查询告警历史
```bash
ctyun-cli monitor query-alert-history
```

### 查询资源组
```bash
ctyun-cli monitor query-resource-groups
```

### 自定义监控指标查询
```bash
ctyun-cli monitor query-custom-trend
```

### CPU Top 排名
```bash
ctyun-cli monitor cpu-top
```

### 内存 Top 排名
```bash
ctyun-cli monitor mem-top
```

### 磁盘 Top 排名
```bash
ctyun-cli monitor disk-top
```

### 数据订阅管理
```bash
ctyun-cli monitor query-message-subscription
ctyun-cli monitor describe-message-subscription
```

### 通知套餐管理
```bash
ctyun-cli monitor notice-pack-list
ctyun-cli monitor notice-pack-used
ctyun-cli monitor notice-pack-limit-detail
```

### 监控看板
```bash
ctyun-cli monitor list-monitor-board
ctyun-cli monitor query-monitor-board-sys-services
ctyun-cli monitor query-monitor-board-view-data
```

### 监控对象资源列表
```bash
ctyun-cli monitor query-ecs-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-pms-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-evs-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-eip-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-traffic-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-elb-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-listener-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-scaling-group-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-zos-user-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-zos-bucket-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-vpc-endpoint-list --region-id RESOURCE_POOL_ID
ctyun-cli monitor query-vpc-endpoint-service-list --region-id RESOURCE_POOL_ID
```

### 设备类型监控项查询
```bash
ctyun-cli monitor query-monitor-items-by-device --region-id RESOURCE_POOL_ID
```

## 账务中心管理

### 查询账户余额
```bash
ctyun-cli billing balance
```

### 查询欠费信息
```bash
ctyun-cli billing arrears
```

### 查询账户账单
```bash
ctyun-cli billing account-bill --bill-cycle 202503
```

### 查询消费类型汇总
```bash
ctyun-cli billing bill-summary --bill-cycle 202503
```

### 查询按需流水账单
```bash
ctyun-cli billing ondemand-flow --bill-cycle 202503
```

### 查询包周期流水账单
```bash
ctyun-cli billing cycle-flow --bill-cycle 202503
```

### 查询消费明细
```bash
ctyun-cli billing consumption
```

## 统一身份认证 (IAM) 管理

### 查询企业项目列表
```bash
ctyun-cli iam list-projects
```

### 查询企业项目详情
```bash
ctyun-cli iam get-project --project-id PROJECT_ID
```

### 分页查询资源信息
```bash
ctyun-cli iam list-resources
```

## 服务器安全卫士

### 查看使用示例
```bash
ctyun-cli security examples
```

### 主机防护
```bash
ctyun-cli security wrapper --help
```

### 防篡改更新
```bash
ctyun-cli security tamper-update --help
```

## 云专线 (CDA) 管理

### 物理专线管理
```bash
ctyun-cli cda physical-line --help
```

### 专线网关管理
```bash
ctyun-cli cda gateway --help
```

### VPC 管理
```bash
ctyun-cli cda vpc --help
```

### BGP 路由管理
```bash
ctyun-cli cda bgp-route --help
```

### 静态路由管理
```bash
ctyun-cli cda static-route --help
```

### 健康检查和链路探测管理
```bash
ctyun-cli cda health-check --help
```

### 跨账号授权管理
```bash
ctyun-cli cda account-auth --help
```

## 分布式消息服务 (Kafka) 管理

### 查询实例列表
```bash
ctyun-cli kafka list --region-id RESOURCE_POOL_ID
ctyun-cli kafka list -r xxx --name test --exact-match
ctyun-cli kafka list -r xxx --status 1 --page 1 --size 20
```

### 查看实例节点状态
```bash
ctyun-cli kafka node-status --region-id RESOURCE_POOL_ID --instance-id INSTANCE_ID
```

### 查询弹性IP列表
```bash
ctyun-cli kafka floating-ips --region-id RESOURCE_POOL_ID
```

### 获取实例配置
```bash
ctyun-cli kafka config --region-id RESOURCE_POOL_ID --instance-id INSTANCE_ID
```

## 云搜索服务 (CSS) 管理

### 查询实例列表
```bash
ctyun-cli css list --region-id RESOURCE_POOL_ID --type 1
ctyun-cli css list -r xxx --name test
```

### 查询实例详情
```bash
ctyun-cli css describe --cluster-id CLUSTER_ID
```

### 查询 Logstash 实例列表
```bash
ctyun-cli css logstash-list --region-id RESOURCE_POOL_ID
```

## 翼 MapReduce (EMR) 管理

### 查询集群列表
```bash
ctyun-cli emr list --region-id RESOURCE_POOL_ID
ctyun-cli emr list -r xxx --name test --v2
```

### 查询集群详情
```bash
ctyun-cli emr describe --cluster-id CLUSTER_ID
ctyun-cli emr describe --cluster-id CLUSTER_ID --v2
```

### 查询节点组信息
```bash
ctyun-cli emr node-groups --cluster-id CLUSTER_ID
ctyun-cli emr node-groups --cluster-id CLUSTER_ID --v2
```

### 查询节点组详情
```bash
ctyun-cli emr node-detail --cluster-id CLUSTER_ID
ctyun-cli emr node-detail --cluster-id CLUSTER_ID --node-state 8
```

### 查询 Hive 元数据概览
```bash
ctyun-cli emr meta-overview --cluster-id CLUSTER_ID
```

### 查询 Hive 表元数据
```bash
ctyun-cli emr meta-table --cluster-id CLUSTER_ID --database test_db --table test_table
```

## 云日志服务 (LTS) 管理

```bash
ctyun-cli lts --help
```

## 弹性文件服务 (SFS) 管理

```bash
ctyun-cli sfs --help
```

## 海量文件服务 (OceanFS) 管理

```bash
ctyun-cli oceanfs --help
```

## 边缘安全加速平台 (Aone) 管理

```bash
ctyun-cli aone --help
```

## 网络管理

```bash
ctyun-cli network --help
```

## 存储管理

```bash
ctyun-cli storage --help
```

## 缓存管理

### 清空所有缓存
```bash
ctyun-cli clear-cache
```

## 使用技巧

### JSON 输出便于脚本处理
```bash
ctyun-cli ecs list --output json | jq '.[] | select(.status=="running")'
```

### YAML 输出便于阅读
```bash
ctyun-cli vpc show --vpc-id vpc-xxx --output yaml
```

### 调试模式排查问题
```bash
ctyun-cli ecs list --debug
```

### 使用指定配置文件
```bash
ctyun-cli ecs list --profile production
```

## 注意事项

1. 首次使用前必须先配置认证信息（推荐使用环境变量方式）
2. 大部分命令需要指定资源 ID（如 instance-id、vpc-id 等）
3. 建议使用 `--help` 查看具体子命令的详细参数
4. 使用 JSON 输出格式便于与其他工具集成
5. 按需查询大量数据时建议分页或使用过滤参数

## 相关链接

- **PyPI 包**: https://pypi.org/project/ctyun-cli/
- **GitHub 仓库**: https://github.com/fengyucn/ctyun-cli
- **问题反馈**: https://github.com/fengyucn/ctyun-cli/issues
- **作者邮箱**: popfrog@gmail.com

## 版本信息

- **当前版本**: v1.18.5 (2026-05-14)
- **开源协议**: MIT
- **Python 要求**: Python 3.8+
- **API 覆盖**: 397+ 个 API
- **命令数量**: 383+ 个命令
- **服务模块**: 17 大服务模块
- **最新功能**:
  - 🚀 监控模块新增 21 个 API：数据订阅、套餐管理、监控看板、资源列表查询(12类)
  - 🚀 ECS 模块新增 12 个 API：资源池(3)、云助手(4)、宿主机(3)、网卡(2)
  - 🆕 AIServer（模型推理服务）模块：预置模型/订单/服务组/报表共 19 个 API
  - 🆕 CloudPC（云电脑/政企版）模块：实例/镜像/磁盘/用户/组织共 10 个 API
  - 🆕 IAM 全面扩展：从 3 个 API 扩展至 34 个（用户/权限/策略/委托/AK-SK/MFA等）
  - 🆕 Aone（边缘安全加速平台）模块：域名/证书/缓存/安全防护共 45 个 API
  - 🆕 EMR/CSS/Kafka 模块
