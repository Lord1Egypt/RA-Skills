---
name: ctyun-cli
description: "天翼云CLI工具 - 企业级命令行工具，帮助您轻松管理天翼云资源。支持ECS、VPC、EBS、ELB、CCE、Redis、MySQL、Kafka、CSS、EMR、监控、账务、IAM、Aone、CloudPC、AIServer、Audit、IMS、APM应用性能监控、LTS、SFS、OceanFS、ZOS、DPS物理机、安全卫士、云间高速EC、微服务引擎MSE、云防火墙CFW等32+服务模块，覆盖943+个API，898+个命令。"
homepage: https://github.com/fengyucn/ctyun-cli
pypi: https://pypi.org/project/ctyun-cli/
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["ctyun-cli"]},"install":[{"id":"pip","kind":"pip","package":"ctyun-cli","bins":["ctyun-cli"],"label":"Install ctyun-cli (pip)"}]}}
---

# 天翼云 CLI (ctyun-cli)

天翼云 CLI 工具，功能强大的企业级命令行工具，帮助您轻松管理天翼云资源。支持云服务器(ECS)、监控告警、安全防护、Redis分布式缓存、弹性负载均衡(ELB)、容器引擎(CCE)、VPC网络、费用查询等核心功能。

**规模统计：** 61,000+行代码，943+个API，898+个命令，32+大服务模块

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

### 资源续订询价
```bash
ctyun-cli ecs renew-price --region-id REGION_ID --resource-type VM --resource-uuid RESOURCE_UUID --cycle-type MONTH --cycle-count 1
```

## 虚拟私有云 (VPC) 管理

终端节点 `ctvpc-global.ctapi.ctyun.cn`。共 96 个命令，覆盖 VPC/子网/路由表/安全组/EIP/NAT/SNAT/DNAT/网卡/对等连接/流日志/共享带宽/共享流量包/终端节点/内网DNS/网络ACL/前缀列表/流量控制/GWLB/L2GW/HaVip/网络诊断/DHCP-VPC绑定/IPv6/IPv4网关/标签。

### VPC 与子网
```bash
ctyun-cli vpc list                              # 查询VPC列表
ctyun-cli vpc new-list                          # 新查询VPC列表（支持游标分页）
ctyun-cli vpc show --vpc-id VPC_ID              # 查询VPC详情
ctyun-cli vpc subnet list                       # 子网列表
ctyun-cli vpc subnet new-list                   # 新查询子网列表
ctyun-cli vpc subnet show --subnet-id SUBNET_ID # 子网详情
ctyun-cli vpc subnet used-ips --subnet-id SUBNET_ID  # 子网已使用IP
```

### 路由表
```bash
ctyun-cli vpc route-table list                                  # 路由表列表
ctyun-cli vpc route-table new-list                              # 新查询路由表列表
ctyun-cli vpc route-table rules --route-table-id RTB_ID         # 路由表规则列表
ctyun-cli vpc route-table new-rules --route-table-id RTB_ID     # 新查询路由表规则列表
```

### 安全组
```bash
ctyun-cli vpc security list                                # 安全组列表
ctyun-cli vpc security new-query                           # 新查询安全组列表
ctyun-cli vpc security show --security-group-id SG_ID      # 安全组详情（含规则）
ctyun-cli vpc security rules                               # 获取安全组规则列表
ctyun-cli vpc security vms --security-group-id SG_ID       # 获取安全组绑定机器列表
```

### 弹性公网 IP EIP（9 个命令）
```bash
ctyun-cli vpc eip list                                  # EIP列表
ctyun-cli vpc eip detail --eip-id EIP_ID                # EIP详情
ctyun-cli vpc eip shared-bandwidths                     # 共享带宽列表（旧）
ctyun-cli vpc eip realtime-monitor                      # EIP实时监控（旧版）
ctyun-cli vpc eip new-realtime-monitor                  # EIP实时监控（新版）
ctyun-cli vpc eip history-monitor --device-ids IP1,IP2 --metric-names ingress_throughput --start-time '2026-07-22 00:00:00' --end-time '2026-07-23 00:00:00'
ctyun-cli vpc eip new-history-monitor                   # EIP历史监控（新版）
ctyun-cli vpc eip filing-status --eip-id EIP_ID         # 端口备案状态
ctyun-cli vpc eip check-address --eip-address 1.1.1.1   # 检查EIP是否可用
```

### 共享带宽 / 共享流量包
```bash
ctyun-cli vpc bandwidth show --bandwidth-id BW_ID       # 共享带宽详情
ctyun-cli vpc bandwidth new-list                        # 新查询共享带宽列表
ctyun-cli vpc flow-package list                         # 共享流量包列表
ctyun-cli vpc flow-package show --sdp-id SDP_ID         # 共享流量包详情
ctyun-cli vpc flow-package metric --sdp-id SDP_ID --start-time '...' --end-time '...'  # 流量包监控
```

### NAT 网关 / SNAT / DNAT
```bash
ctyun-cli vpc nat-gateway list                          # NAT网关列表
ctyun-cli vpc nat-gateway show --nat-gateway-id NAT_ID  # NAT网关详情
ctyun-cli vpc nat-gateway snat list                     # SNAT规则列表
ctyun-cli vpc nat-gateway snat show --snat-id SNAT_ID   # SNAT规则详情
ctyun-cli vpc nat-gateway dnat list --nat-gateway-id NAT_ID      # DNAT规则列表
ctyun-cli vpc nat-gateway dnat show --nat-gateway-id NAT_ID --dnat-id DNAT_ID  # DNAT规则详情
```

### 网卡
```bash
ctyun-cli vpc port list                # 网卡列表
ctyun-cli vpc port new-list            # 新查询网卡列表
```

### 对等连接与流日志
```bash
ctyun-cli vpc peering list                              # 对等连接列表
ctyun-cli vpc peering show --peering-connection-id P_ID # 对等连接详情
ctyun-cli vpc flow-log list                             # 流日志列表
```

### VPC 终端节点（VPCE）
```bash
ctyun-cli vpc vpce list                                 # 终端节点列表
ctyun-cli vpc vpce new-list                             # 新查看终端节点列表
ctyun-cli vpc vpce service list                         # 终端节点服务列表
ctyun-cli vpc vpce service new-list                     # 新查看终端节点服务列表
ctyun-cli vpc vpce service backends --endpoint-service-id EPS_ID  # 终端节点服务后端列表
```

### 内网 DNS
```bash
ctyun-cli vpc dns list                                  # 内网DNS列表
ctyun-cli vpc dns new-list                              # 新内网DNS列表
ctyun-cli vpc dns record list                           # DNS记录列表
ctyun-cli vpc dns record new-list                       # 新DNS记录列表
```

### 网络 ACL
```bash
ctyun-cli vpc acl list                          # ACL列表（旧）
ctyun-cli vpc acl new-list                      # 新ACL列表
ctyun-cli vpc acl rules --acl-id ACL_ID         # ACL规则列表
```

### 前缀列表
```bash
ctyun-cli vpc prefix-list list                          # 前缀列表
ctyun-cli vpc prefix-list show --prefix-list-id PL_ID   # 前缀列表详情
ctyun-cli vpc prefix-list associations --prefix-list-id PL_ID  # 关联资源
```

### 流量控制（镜像流）
```bash
ctyun-cli vpc flow filters                                    # 过滤条件列表
ctyun-cli vpc flow filter-rules --mirror-filter-id MF_ID --direction in  # 过滤规则列表
ctyun-cli vpc flow sessions                                   # 流量会话列表
```

### 网关负载均衡 GWLB
```bash
ctyun-cli vpc gwlb list                                # GWLB 列表
ctyun-cli vpc gwlb ip-listener-list                    # IP监听器列表
```

### 二层网关 L2GW
```bash
ctyun-cli vpc l2gw list                                # L2GW 列表
ctyun-cli vpc l2gw connection-list                     # L2GW connection 列表
```

### 高可用虚拟 IP HaVip
```bash
ctyun-cli vpc havip list                               # HaVip 列表（自动生成 clientToken）
ctyun-cli vpc havip list --filter vpcID=vpc-xxx        # 按 vpcID 筛选（支持多次 --filter）
```

### 网络诊断 VNIA
```bash
ctyun-cli vpc diagnose instances                      # 实例诊断列表（支持按 resourceID/type 过滤）
ctyun-cli vpc diagnose records                        # 实例诊断记录列表
ctyun-cli vpc diagnose paths                          # 网络路径列表
ctyun-cli vpc diagnose analyses --network-path-id NP_ID  # 网络路径分析列表
ctyun-cli vpc diagnose reports --analysis-id NPA_ID   # 网络路径分析报告列表
```

### DHCP 与 VPC 绑定关系
```bash
ctyun-cli vpc dhcp bound-vpcs --dhcp-option-sets-id DHCP_ID    # DHCP 已绑定的 VPC 列表
ctyun-cli vpc dhcp unbound-vpcs                                # 未绑定 DHCP 的 VPC 列表
ctyun-cli vpc dns vpcs --zone-id ZONE_ID                       # zone 绑定的 VPC 列表
```

### IPv6 网关 / 地址 / 带宽
```bash
ctyun-cli vpc ipv6 gateways                          # IPv6 网关列表
ctyun-cli vpc ipv6 list                              # IPv6 地址列表
ctyun-cli vpc ipv6 new-list                          # 新查询 IPv6 地址列表
ctyun-cli vpc ipv6 bw-list                           # IPv6 带宽列表
ctyun-cli vpc ipv6 bw-new-list                       # 新查询 IPv6 带宽列表
```

### IPv4 网关
```bash
ctyun-cli vpc ipv4-gw list                           # IPv4 网关列表
```

### 标签查询（7个）
```bash
ctyun-cli vpc label-query-resources                  # 根据标签获取资源列表
ctyun-cli vpc label-query-by-resource --resource-type TYPE --resource-id ID
ctyun-cli vpc label-vpc-peer --vpc-peer-id PEER_ID
ctyun-cli vpc label-vpce-endpoint --endpoint-id EP_ID
ctyun-cli vpc label-vpce-service --endpoint-service-id EPS_ID
ctyun-cli vpc label-private-dns --zone-id ZONE_ID
```

## 云硬盘 (EBS) 管理

终端节点 `ebs-global.ctapi.ctyun.cn`。共 7 个查询命令。

### 云硬盘查询
```bash
ctyun-cli ebs list                                    # 云硬盘列表
ctyun-cli ebs info --disk-id DISK_ID                  # 云硬盘详情（基于diskID）
ctyun-cli ebs info-by-name --disk-name NAME           # 云硬盘详情（基于名称）
ctyun-cli ebs list-by-name --disk-name NAME           # 云硬盘列表（基于名称）
```

### 快照查询
```bash
ctyun-cli ebs snapshots                               # 快照列表（支持多种过滤）
ctyun-cli ebs snapshot-size                           # 快照使用量
ctyun-cli ebs snapshot-policy                         # 自动快照策略
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

### 保障型负载均衡询价
```bash
# 创建询价
ctyun-cli elb pgelb-create-price --region-id REGION_ID --subnet-id SUBNET_ID --name my-elb --sla-name elb.s2.small --resource-type internal --cycle-type month --cycle-count 1

# 续订询价
ctyun-cli elb pgelb-renew-price --region-id REGION_ID --elb-id ELB_ID --cycle-type month --cycle-count 1

# 变配询价
ctyun-cli elb pgelb-modify-price --region-id REGION_ID --elb-id ELB_ID --sla-name elb.s3.small
```

### ELB 查询类 API（19个）
```bash
# 访问控制
ctyun-cli elb list-access-controls --region-id REGION_ID
ctyun-cli elb show-access-control --region-id REGION_ID --access-control-id AC_ID

# 规格/证书
ctyun-cli elb list-sla --region-id REGION_ID
ctyun-cli elb list-certificates --region-id REGION_ID
ctyun-cli elb show-certificate --region-id REGION_ID --certificate-id CERT_ID
ctyun-cli elb list-domain-cert-links --region-id REGION_ID

# 转发规则/健康检查
ctyun-cli elb list-rules --region-id REGION_ID --listener-id LISTENER_ID
ctyun-cli elb show-rule --region-id REGION_ID --policy-id POLICY_ID
ctyun-cli elb list-health-checks --region-id REGION_ID

# 旧版监控
ctyun-cli elb legacy-history-monitor --region-id REGION_ID --device-ids '["ID"]' --metric-names '["metric"]' --start-time 2026-07-01 --end-time 2026-07-17
ctyun-cli elb legacy-realtime-monitor --region-id REGION_ID

# GWLB 网关负载均衡
ctyun-cli elb list-gwlb --region-id REGION_ID
ctyun-cli elb show-gwlb --region-id REGION_ID --gwlb-id GWLB_ID
ctyun-cli elb gwlb-list-targets --region-id REGION_ID
ctyun-cli elb gwlb-show-target --region-id REGION_ID
ctyun-cli elb gwlb-list-target-groups --region-id REGION_ID
ctyun-cli elb gwlb-show-target-group --region-id REGION_ID

# IP 监听器
ctyun-cli elb list-ip-listeners --region-id REGION_ID
ctyun-cli elb show-ip-listener --region-id REGION_ID

# 标签
ctyun-cli elb list-labels --region-id REGION_ID --elb-id ELB_ID
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

### 节点列表查询
```bash
ctyun-cli redis node-list --prod-inst-id INSTANCE_ID --region-id REGION_ID
```

### 日志下载
```bash
ctyun-cli redis log-download --prod-inst-id INSTANCE_ID --node-name NODE_NAME --date 2026-06-23
```

### 副本状态查询
```bash
ctyun-cli redis replication-state --prod-inst-id INSTANCE_ID --fragment-name redis-0
```

### 租户标签查询
```bash
ctyun-cli redis labels --region-id REGION_ID
ctyun-cli redis labels -r REGION_ID --label-key APPNAME
```

### 运行日志查询
```bash
ctyun-cli redis running-logs --prod-inst-id INSTANCE_ID --node-name NODE_NAME
```

### 实例账号查询
```bash
ctyun-cli redis accounts --prod-inst-id INSTANCE_ID
```

### 费用查询（询价）
```bash
# 订购询价
ctyun-cli redis price --order-type BUY --charge-type PrePaid --period 1 --edition DirectCluster --shard-mem-size 1 --shard-count 3 --engine-version 6.0 --capacity 3

# 变配询价
ctyun-cli redis price --order-type EXPANSION --prod-inst-id INSTANCE_ID
```

### Redis 查询类 API 扩展（52+ 个）

#### 实例生命周期与统计
```bash
# 回收站实例
ctyun-cli redis recycle-bin --region-id REGION_ID
ctyun-cli redis running-statistics --region-id REGION_ID
ctyun-cli redis quota --region-id REGION_ID
ctyun-cli redis dedicated-cluster-instances --region-id REGION_ID
ctyun-cli redis export-task --task-id TASK_ID --region-id REGION_ID
ctyun-cli redis auto-renew -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis can-expand -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis maintain-time -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis maintain-az -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis port-modify-range -i INSTANCE_ID --region-id REGION_ID
```

#### 备份恢复
```bash
ctyun-cli redis backups -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis backup-tasks -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis backup-policy -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis backup-download-url -i INSTANCE_ID --restore-name BACKUP_NAME --ip-type publicIp --region-id REGION_ID
ctyun-cli redis data-flashback -i INSTANCE_ID --region-id REGION_ID
```

#### 安全与 SSL
```bash
ctyun-cli redis ssl -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis security-ips -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis rename-command -i INSTANCE_ID --region-id REGION_ID
```

#### 命令与日志监控
```bash
ctyun-cli redis slow-log -i INSTANCE_ID --node-name NODE_NAME --region-id REGION_ID
ctyun-cli redis slow-log-history -i INSTANCE_ID --node-name NODE_NAME --start-time '2026-07-20 08:00:00' --end-time '2026-07-20 10:00:00' --region-id REGION_ID
ctyun-cli redis command-audit-status -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis monitor-items-v2 -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis node-monitor-values -i INSTANCE_ID --type string --node-name NODE_NAME --start-time '...' --end-time '...' --region-id REGION_ID
ctyun-cli redis node-command-list -i INSTANCE_ID --node-name NODE_NAME --start-time '...' --end-time '...' --region-id REGION_ID
ctyun-cli redis node-command-monitor -i INSTANCE_ID --node-name NODE_NAME --start-time '...' --end-time '...' --type redis_latency_insight_max --region-id REGION_ID
ctyun-cli redis hit-rate -i INSTANCE_ID --node-name NODE_NAME --region-id REGION_ID
```

#### 会话与客户端
```bash
ctyun-cli redis client-map -i INSTANCE_ID --node-name NODE_NAME --region-id REGION_ID
```

#### 参数与模板管理
```bash
ctyun-cli redis instance-config-v3 -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis param-history -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis templates --type sys --region-id REGION_ID
ctyun-cli redis templates --type custom --region-id REGION_ID
ctyun-cli redis template-detail --template-id TEMPLATE_ID --region-id REGION_ID
```

#### Key 管理与分析
```bash
ctyun-cli redis dbkey-count -i INSTANCE_ID --groups 1 --region-id REGION_ID
ctyun-cli redis auto-scan-conf -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis scan-logs -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis eviction-strategy -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis big-and-hot-keys -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis big-hot-key-history -i INSTANCE_ID --node-name NODE_NAME --start-time '...' --end-time '...' --region-id REGION_ID
```

#### 大key/热key 分析工具
```bash
ctyun-cli redis big-key-tasks -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis hot-key-tasks -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis big-key-policy -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis hot-key-policy -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis key-task-record -i INSTANCE_ID --task-id TASK_ID --region-id REGION_ID
ctyun-cli redis diagnosis-tasks -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis offline-key-analysis-list -i INSTANCE_ID --region-id REGION_ID
ctyun-cli redis offline-key-analysis-info -i INSTANCE_ID --task-id TASK_ID --region-id REGION_ID
```

#### 数据迁移与任务中心
```bash
ctyun-cli redis transfer-tasks --page-num 1 --page-size 10 --region-id REGION_ID
ctyun-cli redis transfer-task-info --task-id TASK_ID --region-id REGION_ID
ctyun-cli redis transfer-progress --task-id TASK_ID --region-id REGION_ID
ctyun-cli redis transfer-running-log --task-id TASK_ID --search-date 2026-07-20 --region-id REGION_ID
ctyun-cli redis task-center-list --start-time 20260701 --end-time 20260720 --status -1 --region-id REGION_ID
ctyun-cli redis task-center-info --task-id TASK_ID --region-id REGION_ID
```

#### 混沌工程故障查询
```bash
ctyun-cli redis experiments -i INSTANCE_ID --region-id REGION_ID
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

### 数据导出任务管理
```bash
# 查询数据导出任务列表
ctyun-cli monitor data-export-tasks --region-id REGION_ID

# 创建数据导出任务
ctyun-cli monitor create-data-export-task --region-id REGION_ID --task-name my-task

# 删除数据导出任务
ctyun-cli monitor delete-data-export-task --region-id REGION_ID --task-ids TASK_ID1,TASK_ID2

# 下载导出文件
ctyun-cli monitor download-data-export-task --region-id REGION_ID --task-id TASK_ID
```

### 拨测管理
```bash
# 查询拨测点列表
ctyun-cli monitor query-detection-point

# 查询即时拨测任务结果
ctyun-cli monitor query-instant-detection-task --task-id TASK_ID --detect-type http
```

## 账务中心管理

### 消费类型汇总
```bash
ctyun-cli billing bill-summary 202606
```

### 账户账单（按账户ID）
```bash
ctyun-cli billing account-bill 202606 --account-id ACCOUNT_ID
```

### 账单详情（按账单ID）
```bash
ctyun-cli billing bill-detail BILL_ID
```

### 包周期流水账单
```bash
ctyun-cli billing cycle-flow 202606 --page-size 10
```

### 包周期订单账单详情
```bash
ctyun-cli billing cycle-bill 202606 --page-size 10
```

### 包周期账单明细（按产品汇总）
```bash
ctyun-cli billing cycle-product 202606
```

### 按需流水账单
```bash
ctyun-cli billing ondemand-flow 202606 --page-size 10
```

### 按需账单明细（按产品汇总）
```bash
ctyun-cli billing ondemand-product 202606
```

### 按需账单明细（资源+明细）
```bash
ctyun-cli billing bill-list 202606 --page-size 10
```

### 按需账单明细（资源+账期）
```bash
ctyun-cli billing ondemand-resource-cycle 202606
```

### 按需账单明细（使用量类型+账期）
```bash
ctyun-cli billing ondemand-usage 202606
```

### 按需账单明细（使用量类型+明细）
```bash
ctyun-cli billing ondemand-detail 202606
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

## 服务器安全卫士（原生版）

### 服务器管理
```bash
# 服务器列表
ctyun-cli csscn list --size 20

# 服务器详情
ctyun-cli csscn describe --agent-guid AGENT_GUID
```

### 安全总览统计
```bash
# 待处理风险统计
ctyun-cli csscn risk-stats

# 服务器统计
ctyun-cli csscn server-stats

# Agent防护状态统计
ctyun-cli csscn agent-stats

# Agent在线/离线分布
ctyun-cli csscn agent-distribution

# 漏洞统计
ctyun-cli csscn vuln-stats
```

### 安全事件查询
```bash
# 告警列表
ctyun-cli csscn alarms --time-type LAST_ONE_WEEK --severity 3

# 病毒事件列表
ctyun-cli csscn viruses --os-type 3 --time-type LAST_ONE_MONTH
```

### 配额管理
```bash
ctyun-cli csscn quotas --version 3 --size 20
```

## 关系数据库MySQL版 (RDS)

### 查询实例列表
```bash
ctyun-cli ctmysql list --region-id REGION_ID --page-size 10
ctyun-cli ctmysql list --region-id REGION_ID --engine 8.0 --name mysql-prod
```

### 实例标签管理
```bash
# 绑定标签
ctyun-cli ctmysql batch-label --region-id REGION_ID --action bind --instance-ids ID1,ID2 --label env=prod

# 解绑标签
ctyun-cli ctmysql batch-label --region-id REGION_ID --action unbind --instance-ids ID1 --label env=prod
```

### 监控数据查询
```bash
ctyun-cli ctmysql batch-monitor --region-id REGION_ID --instance-ids ID1,ID2 --metric mysql_monitor_tcp_states --period 60 --last-hours 1
```

### 询价
```bash
# 新建实例询价
ctyun-cli ctmysql inquiry --region-id REGION_ID --project-id 0 --bill-mode 1 --prod-version 5.7 --host-type S7 --period 1 --count 1 --auto-renew 0 --prod-id 10001003 --node-type master --inst-spec 1 --storage-type SATA --storage-space 100 --perf-spec 2C4G --az-name AZ_NAME

# 变更实例询价（磁盘扩容）
ctyun-cli ctmysql inquiry-upgrade --region-id REGION_ID --project-id 0 --inst-id INSTANCE_ID --disk-volume 200 --node-type master

# 续费询价
ctyun-cli ctmysql inquiry-renew --region-id REGION_ID --inst-id INSTANCE_ID --month 1
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
ctyun-cli oceanfs renew-price --region-id REGION_ID --sfs-uid FS_ID --cycle-type month --cycle-cnt 1
ctyun-cli oceanfs upgrade-price --region-id REGION_ID --sfs-uid FS_ID --sfs-size 100
```

## 对象存储 (ZOS) 管理

### 桶管理查询
```bash
# 查询所有桶
ctyun-cli zos list-buckets --region-id REGION_ID

# 桶信息/位置/统计
ctyun-cli zos get-bucket-info --region-id REGION_ID --bucket BUCKET
ctyun-cli zos get-bucket-location --region-id REGION_ID --bucket BUCKET
ctyun-cli zos get-bucket-statistics --region-id REGION_ID --bucket BUCKET

# 桶配置查询
ctyun-cli zos get-bucket-acl --region-id REGION_ID --bucket BUCKET
ctyun-cli zos get-bucket-encryption --region-id REGION_ID --bucket BUCKET
ctyun-cli zos get-bucket-lifecycle --region-id REGION_ID --bucket BUCKET
ctyun-cli zos get-bucket-logging --region-id REGION_ID --bucket BUCKET
ctyun-cli zos get-bucket-policy --region-id REGION_ID --bucket BUCKET
ctyun-cli zos get-bucket-versioning --region-id REGION_ID --bucket BUCKET
ctyun-cli zos get-bucket-tagging --region-id REGION_ID --bucket BUCKET
ctyun-cli zos head-bucket --region-id REGION_ID --bucket BUCKET
```

### 对象管理查询
```bash
# 对象列表/版本/分段
ctyun-cli zos list-objects --region-id REGION_ID --bucket BUCKET
ctyun-cli zos list-object-versions --region-id REGION_ID --bucket BUCKET
ctyun-cli zos list-multipart-uploads --region-id REGION_ID --bucket BUCKET
ctyun-cli zos list-all-parts --region-id REGION_ID --bucket BUCKET
ctyun-cli zos list-parts --region-id REGION_ID --bucket BUCKET --key OBJECT_KEY --upload-id UPLOAD_ID

# 对象详情/ACL/标签
ctyun-cli zos head-object --region-id REGION_ID --bucket BUCKET --key OBJECT_KEY
ctyun-cli zos get-object-acl --region-id REGION_ID --bucket BUCKET --key OBJECT_KEY
ctyun-cli zos get-object-tagging --region-id REGION_ID --bucket BUCKET --key OBJECT_KEY
ctyun-cli zos get-object-retention --region-id REGION_ID --bucket BUCKET --key OBJECT_KEY

# 碎片/数量
ctyun-cli zos get-fragment-num --region-id REGION_ID --bucket BUCKET
ctyun-cli zos get-object-num --region-id REGION_ID --bucket BUCKET
```

### IAM/资源/服务管理
```bash
ctyun-cli zos get-keys --region-id REGION_ID
ctyun-cli zos get-endpoint --region-id REGION_ID
ctyun-cli zos list-regions --region-id REGION_ID
ctyun-cli zos get-service-status --region-id REGION_ID
ctyun-cli zos list-policies --region-id REGION_ID
ctyun-cli zos get-policy-detail --region-id REGION_ID --policy-id POLICY_ID
ctyun-cli zos list-roles --region-id REGION_ID
ctyun-cli zos get-role-detail --region-id REGION_ID --role-id ROLE_ID
ctyun-cli zos get-user-event-bridge --region-id REGION_ID
ctyun-cli zos get-object-lock-conf --region-id REGION_ID --bucket BUCKET
```

### 标签管理
```bash
# 设置/查询/删除桶标签
ctyun-cli zos put-bucket-tagging --region-id REGION_ID --bucket BUCKET --tag key1=value1 --tag key2=value2
ctyun-cli zos get-bucket-tagging --region-id REGION_ID --bucket BUCKET
ctyun-cli zos delete-bucket-tagging --region-id REGION_ID --bucket BUCKET

# 设置/查询/删除对象标签
ctyun-cli zos put-object-tagging --region-id REGION_ID --bucket BUCKET --key OBJECT_KEY --tag env=prod
ctyun-cli zos get-object-tagging --region-id REGION_ID --bucket BUCKET --key OBJECT_KEY
ctyun-cli zos delete-object-tagging --region-id REGION_ID --bucket BUCKET --key OBJECT_KEY
```

### 询价
```bash
ctyun-cli zos query-price --region-id REGION_ID --pkg-type zosSize --pkg-spec-type ...
```

## 应用性能监控 (APM) 管理

终端节点 `arms-global.ctapi.ctyun.cn`，regionId 通过 header 传递。共 44 个查询类命令，分 8 个子组。

### 基础配置与元数据
```bash
ctyun-cli apm meta project-metadata --region-id REGION_ID
ctyun-cli apm meta env-types --region-id REGION_ID
ctyun-cli apm meta envs --region-id REGION_ID
ctyun-cli apm meta app-conf --region-id REGION_ID --service-name APP --project-code PROJ --deployment ENV
ctyun-cli apm meta license-key --region-id REGION_ID
ctyun-cli apm meta monitor-status --region-id REGION_ID --environment-code ENV_CODE
ctyun-cli apm meta default-jobs --region-id REGION_ID --environment-code ENV_CODE
ctyun-cli apm meta common-labels --region-id REGION_ID --environment-code ENV_CODE
```

### 应用与实例管理
```bash
ctyun-cli apm app list --region-id REGION_ID
ctyun-cli apm app transaction-types --region-id REGION_ID
ctyun-cli apm app agents --region-id REGION_ID --agent-status 1
ctyun-cli apm app env-instances --region-id REGION_ID --env-type CS
ctyun-cli apm app tasks --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --deployment ENV --env-uuid ENV_UUID
ctyun-cli apm app instances-stat --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
```

### 调用链与拓扑
```bash
ctyun-cli apm trace detail --region-id REGION_ID --trace-id TRACE_ID
ctyun-cli apm trace span-detail --region-id REGION_ID --trace-id TRACE_ID --span-id SPAN_ID
ctyun-cli apm trace list --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm trace topology --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
```

### 性能监控数据
```bash
ctyun-cli apm perf overview --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf request-curve --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf http-code-curve --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf slow-transactions --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf exceptions --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf sql-stat-page --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP --db-types mysql
ctyun-cli apm perf sql-stat-histogram --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf nosql-stat-histogram --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf nosql-stat-page --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf mq-stat-page --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf transaction-stat --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf jvm-info --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf app-instance-curve --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf jvm-gc-count --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
ctyun-cli apm perf jvm-thread-count --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --service-name APP
```

### 用量统计
```bash
ctyun-cli apm usage total-view --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201
ctyun-cli apm usage span-report --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --step 3600
ctyun-cli apm usage agent-hour --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --step 3600
ctyun-cli apm usage span-store --region-id REGION_ID --start-time 1715656183201 --end-time 1716174583201 --step 3600
```

### 告警/通知/Webhook 管理
```bash
# 告警规则
ctyun-cli apm alert rules --region-id REGION_ID --obj-type ctgcache
ctyun-cli apm alert rule-templates --region-id REGION_ID --obj-type ctgcache
ctyun-cli apm alert send-history --region-id REGION_ID --page-num 1 --page-size 10

# 通知管理
ctyun-cli apm notify contacts --region-id REGION_ID --page-num 1 --page-size 10
ctyun-cli apm notify contact-groups --region-id REGION_ID --page-num 1 --page-size 10
ctyun-cli apm notify strategies --region-id REGION_ID --page-num 1 --page-size 10

# Webhook
ctyun-cli apm webhook list --region-id REGION_ID --page-num 1 --page-size 10
```

## 物理机 (DPS) 管理

### 查询操作系统列表
```bash
ctyun-cli dps list-os --region-id REGION_ID --az-name AZ_NAME
```

### 批量查询物理机列表
```bash
ctyun-cli dps list --region-id REGION_ID --az-name AZ_NAME
ctyun-cli dps list --region-id REGION_ID --az-name AZ_NAME --status RUNNING --page-size 20
```

### 查询单台物理机详情
```bash
ctyun-cli dps describe --region-id REGION_ID --az-name AZ_NAME --instance-uuid INSTANCE_UUID
```

### 查询物理机网卡信息
```bash
ctyun-cli dps interfaces --region-id REGION_ID --az-name AZ_NAME --instance-uuid INSTANCE_UUID
```

### 查询挂载卷ID列表
```bash
ctyun-cli dps volumes --region-id REGION_ID --az-name AZ_NAME --instance-uuid INSTANCE_UUID
```

### 查询镜像信息
```bash
ctyun-cli dps image --region-id REGION_ID --az-name AZ_NAME --instance-uuid INSTANCE_UUID
```

### 查询元数据
```bash
ctyun-cli dps metadata --region-id REGION_ID --az-name AZ_NAME --instance-uuid INSTANCE_UUID
```

### 查询物理机库存
```bash
ctyun-cli dps stock --region-id REGION_ID --az-name AZ_NAME
ctyun-cli dps stock --region-id REGION_ID --az-name AZ_NAME --device-type physical.t3.large --count 2
```

## 边缘安全加速平台 (Aone) 管理

```bash
ctyun-cli aone --help
```

## 微服务引擎 (MSE) 管理

覆盖实例、Nacos 注册配置中心、云原生 API 网关，共 48 个命令。

### 实例管理
```bash
ctyun-cli mse instance list --region-id REGION_ID
ctyun-cli mse instance detail --region-id REGION_ID --instance-id INSTANCE_ID
ctyun-cli mse instance node-status --region-id REGION_ID --instance-id INSTANCE_ID
ctyun-cli mse instance metrics --region-id REGION_ID --instance-id INSTANCE_ID
```

### Nacos 服务与配置管理
```bash
# 服务管理
ctyun-cli mse nacos service list --region-id REGION_ID --instance-id INSTANCE_ID
ctyun-cli mse nacos service detail --region-id REGION_ID --instance-id INSTANCE_ID --service-name SERVICE
ctyun-cli mse nacos service instances --region-id REGION_ID --instance-id INSTANCE_ID --service-name SERVICE

# 配置管理
ctyun-cli mse nacos config list --region-id REGION_ID --instance-id INSTANCE_ID
ctyun-cli mse nacos config content --region-id REGION_ID --instance-id INSTANCE_ID --data-id DATA_ID --group GROUP
ctyun-cli mse nacos config history-list --region-id REGION_ID --instance-id INSTANCE_ID --data-id DATA_ID --group GROUP

# 命名空间 / 用户 / AKSK
ctyun-cli mse nacos namespace list --region-id REGION_ID --instance-id INSTANCE_ID
ctyun-cli mse nacos user list --region-id REGION_ID --instance-id INSTANCE_ID
ctyun-cli mse nacos aksk list --region-id REGION_ID --instance-id INSTANCE_ID
ctyun-cli mse nacos blackwhite-list --region-id REGION_ID --instance-id INSTANCE_ID
```

### 云原生 API 网关
```bash
ctyun-cli mse gateway list --region-id REGION_ID
ctyun-cli mse gateway detail --region-id REGION_ID --spu-inst-id INST_ID
ctyun-cli mse gateway route list --region-id REGION_ID --inst-id INST_ID
ctyun-cli mse gateway upstream list --region-id REGION_ID --inst-id INST_ID
ctyun-cli mse gateway domain list --region-id REGION_ID --inst-id INST_ID
ctyun-cli mse gateway elb bound --region-id REGION_ID --inst-id INST_ID
```

## 云防火墙 (CFW) 管理

云防火墙原生版，共 66 个查询命令。

### 防火墙与概览
```bash
ctyun-cli cfw list --region-id REGION_ID
ctyun-cli cfw show --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw overview --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw protection-overview --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw asset-overview --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw acl-overview --region-id REGION_ID --firewall-id FIREWALL_ID
```

### 资产与防护规则
```bash
ctyun-cli cfw asset list --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw asset statistics --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw policy list --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw blackwhite list --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw address-book list --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw ips rules --region-id REGION_ID --firewall-id FIREWALL_ID
```

### 告警 / 日志 / 报表
```bash
ctyun-cli cfw alarm list --region-id REGION_ID --firewall-id FIREWALL_ID --start-time 2026-07-01T00:00:00Z --finish-time 2026-07-28T00:00:00Z
ctyun-cli cfw log flow-list --region-id REGION_ID --firewall-id FIREWALL_ID --start-time 2026-07-01T00:00:00Z --finish-time 2026-07-28T00:00:00Z
ctyun-cli cfw log storage --region-id REGION_ID --firewall-id FIREWALL_ID
ctyun-cli cfw report list --region-id REGION_ID --firewall-id FIREWALL_ID --start-time 2026-07-01T00:00:00Z --end-time 2026-07-28T00:00:00Z --report-type DAY
```

### 询价
```bash
# C100 型：新购 / 续订 / 升配
ctyun-cli cfw price new --region-id REGION_ID --cycle-type MONTH --cycle-cnt 1 --spec Advanced --protection-ip-num 20 --flow-processing-capacity 10
ctyun-cli cfw price renew --region-id REGION_ID --firewall-id FIREWALL_ID --cycle-type MONTH --cycle-cnt 1
# N100 型（orders 数组 JSON）
ctyun-cli cfw price new-n100 --region-id REGION_ID --orders-json '[{...}]'
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

## 询价 / 价格查询

支持 8 个模块共 41+ 个询价 API（不同 URI 视为独立 API）。

### ECS 弹性云主机询价
```bash
ctyun-cli ecs query-price --resource-type EBS --disk-type SATA --disk-size 100 --disk-mode VBD  # 旧版订单询价
ctyun-cli ecs renew-price --resource-type VM --resource-uuid xxx --cycle-type MONTH --cycle-count 1  # 旧版续订询价
ctyun-cli ecs new-order-price --resource-type EBS --disk-type SATA --disk-size 100 --disk-mode VBD --cycle-type MONTH --cycle-count 1  # 新订单询价
ctyun-cli ecs upgrade-order-price --region-id REGION_ID --resource-id xxx --resource-type VM --flavor-name s2.small.1  # 订单升级询价
ctyun-cli ecs renew-order-price --region-id REGION_ID --resource-id xxx --resource-type VM --cycle-type MONTH --cycle-count 1  # 订单续订询价
ctyun-cli ecs upgrade-by-uuid-price --region-id REGION_ID --resource-uuid xxx --resource-type VM --flavor-name s2.small.1  # UUID升级询价
```

### Redis 询价
```bash
ctyun-cli redis price --order-type BUY --charge-type PrePaid --period 1 --edition DirectCluster --shard-mem-size 1 --shard-count 3 --engine-version 6.0 --capacity 3
```

### Kafka 询价
```bash
ctyun-cli kafka create-price -r REGION_ID --spec-name kafka.8u16g.cluster --node-num 3 --zone-list AZ1 --disk-type SSD --disk-size 300 --cycle-type 3 --cycle-cnt 1
ctyun-cli kafka renew-price -r REGION_ID -i INSTANCE_ID --cycle-cnt 1
ctyun-cli kafka spec-change-price -r REGION_ID -i INSTANCE_ID --spec-name kafka.16u32g.cluster
ctyun-cli kafka disk-change-price -r REGION_ID -i INSTANCE_ID --disk-size 600
ctyun-cli kafka node-change-price -r REGION_ID -i INSTANCE_ID --node-num 5
```

### VPC 询价（18 个命令）
```bash
ctyun-cli vpc price eip create --region-id REGION_ID --cycle-type month --name test --bandwidth 5
ctyun-cli vpc price eip modify --region-id REGION_ID --eip-id EIP_ID --bandwidth 10
ctyun-cli vpc price eip renew --region-id REGION_ID --eip-id EIP_ID --cycle-type month --cycle-count 1
ctyun-cli vpc price nat create --region-id REGION_ID --vpc-id VPC_ID --name nat --spec 1 --az-name AZ --cycle-type month --cycle-count 1
ctyun-cli vpc price nat modify --region-id REGION_ID --nat-gateway-id NAT_ID --spec 2
ctyun-cli vpc price nat renew --region-id REGION_ID --nat-gateway-id NAT_ID --cycle-type month --cycle-count 1
ctyun-cli vpc price bw create --region-id REGION_ID --bandwidth 10 --cycle-type month --cycle-count 1 --name bw
ctyun-cli vpc price bw modify --region-id REGION_ID --bandwidth-id BW_ID --bandwidth 20
ctyun-cli vpc price bw renew --region-id REGION_ID --bandwidth-id BW_ID --cycle-type month --cycle-count 1
ctyun-cli vpc price flow-package --region-id REGION_ID --cycle-type MONTH --cycle-count 1 --count 1 --spec 10
ctyun-cli vpc price ipv6 create/modify/renew  # IPv6 带宽创建/变配/续订
ctyun-cli vpc price vpce --region-id REGION_ID --endpoint-service-id EPS_ID --endpoint-name test --subnet-id SUBNET_ID --vpc-id VPC_ID
ctyun-cli vpc price l2gw create/renew  # L2GW 订购/续订询价
ctyun-cli vpc price to-cycle --region-id REGION_ID --resource-id EIP_ID --resource-type eip --cycle-type month --cycle-count 1  # 按需转包周期
ctyun-cli vpc price to-ondemand --region-id REGION_ID --resource-id EIP_ID --resource-type eip  # 包周期转按需
```

### CloudPC 云电脑询价
```bash
ctyun-cli cloudpc volume-price --bill-mode Cycle --disk-type uhio --count 1 --volume-size 50 --encryption false
ctyun-cli cloudpc ecs-price --bill-mode Cycle --os-type Windows --template-oid OID --image-oid OID --subnet-oid OID --security-group-oid OID --sys-disk-type uhio --sys-disk-size 50 --instance-num 1
ctyun-cli cloudpc expand-price --cycle-type Month --cycle-cnt 1 --volume-oid OID --volume-size 100
ctyun-cli cloudpc renew-ecs-price --cycle-type Month --cycle-cnt 1 --desktop-oids OID1,OID2
ctyun-cli cloudpc renew-volume-price --cycle-type Month --cycle-cnt 1 --volume-oid OID
ctyun-cli cloudpc resize-sysdisk-price --desktop-oid OID --disk-size 100
```

### SFS / OceanFS 询价
```bash
ctyun-cli sfs create-price --region-id REGION_ID --order-num 1 --cycle-type year --sfs-size 500 --volume-type hdd --cycle-cnt 3
ctyun-cli sfs expand-price --region-id REGION_ID --sfs-uid FS_ID --sfs-size 1000
ctyun-cli sfs renew-price --region-id REGION_ID --sfs-uid FS_ID --cycle-type year --cycle-cnt 1
ctyun-cli oceanfs create-price --region-id REGION_ID --order-num 1 --sfs-size 500 --sfs-type massive --on-demand
```

### 云间高速 EC 询价（新模块）
```bash
ctyun-cli ec price new --region-id REGION_ID --ec-id EC_ID --bandwidth 5 --cycle-type month --cycle-count 1
ctyun-cli ec price upgrade --region-id REGION_ID --ec-id EC_ID --bandwidth 10 --resource-id RES_ID
ctyun-cli ec price renew --region-id REGION_ID --ec-id EC_ID --resource-id RES_ID --cycle-type month --cycle-count 1
```

### 微服务引擎 MSE 询价（新模块）
```bash
ctyun-cli mse create-price --engine-type nacos --cycle-type 3 --cycle-cnt 1 --auto-pay false --auto-renew-cycle-type 3 --auto-renew-cycle-count 1 --instance-num 3 --cpu-num 4 --region-id REGION_ID
```

## 相关链接

- **PyPI 包**: https://pypi.org/project/ctyun-cli/
- **GitHub 仓库**: https://github.com/fengyucn/ctyun-cli
- **问题反馈**: https://github.com/fengyucn/ctyun-cli/issues
- **作者邮箱**: popfrog@gmail.com

## 版本信息

- **当前版本**: v1.30.0 (2026-07-27)
- **开源协议**: MIT
- **Python 要求**: Python 3.8+
- **API 覆盖**: 943+ 个 API
- **命令数量**: 898+ 个命令
- **服务模块**: 32+ 大服务模块
- **最新功能**:
  - 🆕 **新增 CFW 云防火墙模块**（v1.30.0）：66 个查询命令，终端节点 `ctcfw-global.ctapi.ctyun.cn`
    - 防火墙/概览/版本配额/网络工具/资产/防护规则/黑白名单/地址簿/IPS/应用/告警/日志/报表/询价（C100+N100）
    - excel 模板导出支持二进制文件下载（`--output` 指定保存路径）
  - 🚀 **MSE 微服务引擎大扩展**（v1.29.0~v1.29.2）：从 1 个扩展到 48 个命令
    - Nacos 注册配置中心（服务/配置/命名空间/用户/AKSK，21+8 个命令）
    - 云原生 API 网关（网关/路由/服务/域名/ELB，18 个命令）
  - 🆕 **全量询价/报价 API 完成**：8 个模块共 41+ 个询价命令（不同 URI 视为独立 API）
    - ECS（6 个）、Kafka（5 个）、VPC（18 个）、CloudPC（6 个）、SFS（3 个）、OceanFS（1 个）
    - 新建 EC 云间高速模块（3 个命令，终端节点 `ec-global.ctapi.ctyun.cn`）
    - 新建 MSE 微服务引擎模块（1 个命令，终端节点 `mse-global.ctapi.ctyun.cn`）
  - 🔧 **ID 截断修复**：修复 `ecs regions` regionID 被截断为 30 位、DPS subnetID 被截断等 4 处 ID 截断问题
  - 🔧 **ECS 命令注册修复**：注册 `ecs console`（VNC 终端）、`ecs get-availability-zones-details`（可用区详情）；删除 3 个半成品命令
  - 🎉 **VPC 模块查询列表类 API 全部完成**（v1.27.2）：96 个命令
  - 🚀 **VPC 模块扩展（第 3 波）**（v1.27.1）：从 68 个扩展到 82 个命令
    - **网络 ACL**：ACL 列表（旧/新）、ACL 规则列表
    - **前缀列表**：前缀列表、详情、关联资源
    - **流量控制（镜像流）**：过滤规则、过滤条件、流量会话列表
    - **GWLB**：GWLB 列表、IP 监听器列表
    - **L2GW**：L2GW 列表、L2GW connection 列表
    - **HaVip**：高可用虚拟 IP 列表（自动生成 clientToken）
  - 🚀 **VPC 模块大扩展（第 2 波）**：从 42 个扩展到 68 个命令（v1.27.0）
    - **EIP 监控**：实时监控（旧/新版）、历史监控（旧/新版）、端口备案状态、EIP 地址可用性检查
    - **共享带宽/流量包**：共享带宽详情、新查询共享带宽列表、共享流量包列表/详情/监控
    - **VPC 终端节点（VPCE）**：终端节点列表（旧/新）、终端节点服务列表（旧/新）、后端列表
    - **内网 DNS**：DNS 列表（旧/新）、DNS 记录列表（旧/新）
    - 新增 `_simple_post` 通用 POST 辅助方法
  - 🚀 **VPC 模块扩展（第 1 波）**：从 23 个扩展到 42 个命令（v1.26.2）
    - NAT网关详情、SNAT/DNAT规则列表与详情、对等连接详情
    - 新查询路由表列表、路由表规则列表、新查询路由表规则列表
    - 安全组规则列表、安全组绑定机器列表、网卡列表/新查询网卡列表
    - 修复 NAT网关列表/对等连接列表/流日志列表 的 TODO 桩代码实现
  - 🆕 **EVS 云硬盘模块扩充**：从 1 个扩展到 7 个查询命令
    - 云硬盘详情（基于diskID/名称）、列表（基于名称）、快照列表/使用量、自动快照策略
  - 🚀 **Redis 查询类 API 全面扩充**：新增 52 个查询命令，Redis 模块从 33 个扩展到 85 个命令
    - 实例生命周期/回收站/配额/专属集群、备份恢复/数据闪回、SSL/IP白名单/危险命令重命名
    - 慢日志/审计日志/节点命令监控/命中率分析、参数模板(V3)/修改历史
    - 大key/热key/离线全量key分析、过期key扫描、淘汰策略、数据迁移进度/日志、任务中心、混沌工程故障
  - 🆕 **APM（应用性能监控）模块**：终端节点 `arms-global.ctapi.ctyun.cn`，实现 44 个查询类 API
    - 基础配置(项目/环境/LicenseKey/采集状态)、应用与实例、调用链与拓扑、性能监控(SQL/NoSQL/MQ/JVM)、用量统计、告警/通知/Webhook
  - 🚀 **ZOS（对象存储）全面增强**：从仅询价扩展到 39 个命令（桶/对象/IAM/服务/标签管理）
  - 🚀 **ELB 查询类 API**：新增 19 个查询命令（访问控制/规格/证书/转发规则/健康检查/GWLB/IP监听器/旧版监控/标签）
  - 🆕 ctmysql（关系数据库MySQL版）模块：实例列表、标签管理、监控查询、询价（新建/变更/续费）
  - 🆕 csscn（服务器安全卫士原生版）模块：10个命令，服务器/风险/漏洞/告警/病毒/配额查询
  - 🔧 billing 模块清理：移除全部 mock 数据逻辑，删除失效的 balance/arrears 命令
  - 🆕 DPS（物理机）模块：8个命令，实例/网卡/镜像/元数据/库存查询
  - 🚀 ELB 新增3个PGELB询价API（创建/续订/变配）
  - 🚀 ECS 新增资源续订询价（支持VM/EBS/IP/NAT/BMS等9种资源类型）
  - 🚀 Monitor 新增拨测点查询和拨测任务结果查询
  - 🚀 OceanFS 新增续订询价和扩容询价
  - 🚀 Redis 新增7个API：Proxy监控、读写分离、分片管理、节点状态、可用区查询
  - 🆕 Aone（边缘安全加速平台）/ AIServer（模型推理服务）/ CloudPC（云电脑）模块
