# BUG03: EMQX 集群单节点路由表"同步死亡" —— 持久化数据 × mria 增量复制断链 × 重启不愈

## 案例摘要

设备/客户端持续发送 MQTT 报文（如 `thing/product/<sn>/register`），但订阅在另一节点的服务（access-service）**完全收不到**消息，业务层表现为"设备一直注册不上、收不到 register_reply"。集群 `cluster status` 看起来正常（所有节点 `running`），ACL 默认全开，从健康节点 publish 测试也都正常——**唯独从某一个特定节点 publish 的消息会被该节点本地直接丢弃**（`dropped.no_subscribers` 异常高），而该节点的路由表条目数显著少于其他节点。

根因是 EMQX（5.x）那个节点的 **mria（mnesia 复制层）路由表与集群其他节点失同步**：节点视图里只有自己本地客户端的订阅，看不到远端节点的订阅，导致跨节点 publish 被本地判定为"无订阅者"丢弃。**单纯重启该节点并不能修复**——因为 hostPath 持久化的 mnesia 数据会让节点"自认为是老成员"跳过全量 bootstrap，必须通过 `cluster leave` + `cluster join` 强制全量重同步。

---

## 症状 / 特征速查（用于匹配）

> 下列特征命中 **4 条及以上** 时，高概率是本案例；命中 **2-3 条** 也值得优先按本案例思路排查。

### 业务层现象

- [ ] 设备 publish MQTT 报文（register / heart / report 等），订阅服务**完全没有日志记录**收到该报文
- [ ] 同一个设备的同类报文，**有时通有时不通**（取决于设备/客户端被 LB hash 到哪个 broker 节点）
- [ ] 服务侧的其它 topic（osd / events / state）**仍然在持续收消息**，唯独某些 topic 收不到 → 容易让人误以为"是这个 topic 的代码问题"
- [ ] 切换 client 重新连接（断开 → 重连）有概率"突然就好了"，但用户复盘不出规律
- [ ] 应用层 ACL / 鉴权 / topic 拼写都查过，确认没问题

### Broker 端指标特征（最诊断性！）

- [ ] `emqx_ctl broker metrics` 显示**单一节点**的 `messages.dropped.no_subscribers` 占接收消息的比例**异常高**（>30%）
- [ ] 其他节点同一指标**几乎为 0**或极低（<1%）
- [ ] 故障节点 `messages.received` 不为 0，说明 publish 确实进了 broker
- [ ] HTTP API publish 到故障节点会显式返回 `{"message":"no_matching_subscribers","reason_code":16}`
- [ ] 同一条消息 publish 到健康节点立刻被订阅者收到

### 集群路由表特征

- [ ] `emqx_ctl cluster status` 显示**所有节点都 running、没有 stopped 节点**（看起来一切正常！）
- [ ] `emqx_ctl topics list | wc -l` 在不同节点结果**差异巨大**（如 3 vs 41）
- [ ] 故障节点的 `topics list` 里只有**本节点客户端**的订阅
- [ ] 健康节点的 `topics list` 里能看到**所有节点**客户端的订阅（包含跨节点的 wildcard 订阅）
- [ ] `emqx_ctl mnesia` 显示三个节点都在 `running db nodes` 里（mria 元数据看起来同步）

### 部署 / 架构特征

- [ ] EMQX **集群部署**（3 节点及以上）
- [ ] 部署在 **k8s StatefulSet**，使用 **hostPath / PV** 持久化 mnesia 数据目录（`/opt/emqx/data/mnesia/...`）
- [ ] Service 用普通 ClusterIP/LoadBalancer，客户端通过 LB hash 到任意节点
- [ ] 订阅者（服务侧）和发布者（设备）**不一定连在同一节点**
- [ ] 集群里至少有一个节点曾经经历过**异常重启 / OOM / 网络抖动**

### 关键日志/指标指纹

```text
# 故障节点 broker metrics（异常）
messages.dropped              : 320863
messages.dropped.no_subscriber: 320863    # 跟 received 比 ~64%
messages.publish              : 501240
messages.received             : 501240

# 健康节点 broker metrics（正常）
messages.dropped              : 1358
messages.dropped.no_subscriber: 1358      # 跟 received 比 ~0.03%
messages.received             : 4079734

# HTTP API publish 到故障节点的响应
{"message":"no_matching_subscribers","reason_code":16}

# 故障节点的 topics list（残缺）
thing/product/SN-XXX/register -> emqx-1   # 只有本节点客户端的订阅
（缺失 wildcard 订阅 thing/product/+/register -> emqx-2）

# 健康节点的 topics list（完整）
thing/product/+/register -> emqx-2        # 能看到 wildcard 订阅
thing/product/+/osd -> emqx-2
thing/product/+/state -> emqx-2
... 数十条
```

### 反向排除项

- 如果 `cluster status` 里有 `stopped_nodes` → 不是本案例，先恢复节点本身
- 如果**所有节点**的 `dropped.no_subscribers` 都很高 → 不是本案例，是订阅者真的没起来或都崩了
- 如果故障节点的 `topics list` 跟健康节点**完全一致**（条数相同、内容相同）→ 不是本案例，去查订阅者侧（client 是否已断开）
- 如果是**共享订阅 `$queue/`** 且只是某个组员崩了 → 不是本案例，是组成员问题
- 如果故障是**所有 topic 全都收不到**（包括同节点客户端互发）→ 不是本案例，是节点本身彻底坏了

---

## 详细说明 / 根因链路

### 三层因素拆解

| 层 | 内容 | 单独看是否必然出 bug |
|---|---|---|
| **集群层** | EMQX 5.x 用 mria（mnesia + 复制层）做集群元数据同步，路由表 `emqx_route` 是 `ram_copies` 类型，靠 mria 实时复制 | 不是 bug（标准设计） |
| **持久化层** | 节点 mnesia 元数据持久化到 hostPath `/opt/emqx/data/mnesia/<node>/`，节点重启时会读取本地元数据 | 不是 bug（保留集群成员关系用） |
| **同步链路层** | 节点重启 / 网络抖动 / OOM 后，mria 增量复制链路损坏，但**节点本地数据让它"自认为已经在集群里"，跳过全量 bootstrap**；后续增量也补不上 | **这是真正的 bug** |

### 为什么 `cluster status` 看起来是健康的

- `cluster status` 检查的是 **ekka 成员关系**（基于 erlang distribution 的 `net_kernel:nodes()`）
- 节点间 erlang RPC 通信正常 → ekka 认为成员关系健康 → `running_nodes` 列表完整
- 但 **mria 的路由表复制是另一个独立机制**：基于 `mria_lib:rpc_to_core_node/3` + 监听 `mnesia` 事件
- mria 复制断链时不会反映到 `cluster status`，但路由表会停留在断链时刻的快照（甚至更糟，只有本地数据）

### 故障节点的"假同步"状态

```text
emqx-0 节点视角：
  ├─ ekka 成员：[emqx-0, emqx-1, emqx-2]  ✓ "我在集群里"
  ├─ mria running_nodes: [emqx-0, emqx-1, emqx-2]  ✓ "数据库节点都在"
  └─ emqx_route 表内容：
        thing/product/SN-X/register -> emqx-0     ← 本地客户端订阅的（自己往里写的）
        thing/product/SN-Y/osd -> emqx-1          ← 偶然同步过来的少量条目
        （缺失大量 wildcard 订阅、其他节点客户端订阅）

emqx-1 / emqx-2 节点视角：
  └─ emqx_route 表内容：完整 41 条
        thing/product/+/register -> emqx-2  ← access-service 的订阅
        thing/product/+/osd -> emqx-2
        ... 等所有节点客户端的订阅
```

### Publish 路由判定流程

```text
client publish thing/product/SN-X/register (QoS 1) → emqx-0
    │
    ├─► emqx-0 的 broker 模块查询本节点 emqx_route 表
    │      └─► 匹配 wildcard 订阅 thing/product/+/register
    │             └─► ❌ 表里没有这条订阅！
    │
    ├─► emqx-0 判定 no_matching_subscribers
    │      ├─► 直接丢弃消息
    │      ├─► messages.dropped.no_subscribers++
    │      └─► HTTP API 返回 {"message":"no_matching_subscribers","reason_code":16}
    │
    └─► 设备 / MQTTX 视角：publish 成功（broker 回了 PUBACK，QoS 1 网络层 OK）
                            但 register_reply 永远不来（消息根本没到 access-service）
```

### 为什么"重启 pod 不修复"

这是本案例最坑的点：

1. **mnesia 数据持久化在 hostPath**  
   pod 重启后，`/opt/emqx/data/mnesia/<node>/` 还在
2. **节点启动时读取本地 mnesia schema**  
   发现自己已经是集群成员、有历史数据 → 跳过全量 bootstrap，进入"增量同步"模式
3. **但增量同步链路本身就是坏的**（这正是当初触发故障的根因）  
   → 路由表保持残缺状态
4. 表象上：节点正常启动、`cluster status` 显示 running、表面上一切如常 → **bug 持续存在**

正确的修复流程必须**显式 leave 集群再 join**，触发 mria 全量 bootstrap：

```text
emqx_ctl cluster leave
   └─► mria 主动断开复制链路、清空本地路由表
emqx_ctl cluster join <other-node>
   └─► mria 触发全量 bootstrap：从 core node 拉取所有表的完整快照
```

### 为什么"客户端重连有时能好"

- 如果客户端重连时 LB hash 到健康节点 → publish 经健康节点路由 → 正常
- 如果重连仍 hash 到故障节点 → publish 仍被丢弃
- 用户感知"运气好就好了"，没法稳定复现 → 误诊为客户端问题或网络抖动

---

## 排查方法论

### 使用到的核心技术

| 技术 | 用途 | 何时用 |
|---|---|---|
| **跨节点指标对照** | `emqx_ctl broker metrics` 在每个节点跑一遍，对比 `dropped.no_subscribers` 比例 | 第一步必做，5 分钟见效 |
| **跨节点路由表条数对照** | `emqx_ctl topics list \| wc -l` 看每个节点路由表大小差异 | 强烈指向单节点同步问题 |
| **跨节点 publish 实验** | 用 EMQX HTTP API 从每个节点 publish 同一条消息，看哪个失败 | 隔离问题节点的"金标准" |
| **HTTP API publish 错误码识别** | `no_matching_subscribers` (reason_code 16) 是路由表残缺的强信号 | 看到这个错误码立刻怀疑本案例 |
| **客户端在线指标 + 订阅对照** | `clients/{id}/subscriptions` 看订阅者实际订阅的 topic 和 QoS | 排除"订阅者根本没订阅"的可能 |
| **mnesia 状态审计** | `emqx_ctl mnesia` 看 mria 各表状态、节点角色（core / replicant） | 怀疑 mria 同步问题时 |

### 诊断步骤（按顺序）

#### 1. 业务侧确认现象（5 分钟）

- 在订阅服务的入口 logger（如 access-service 的 `InboundMessageRouter`）grep 目标 topic
- 确认：**某些 topic 完全收不到消息**，但**其他 topic 仍持续在收**
- 这一步排除"服务整体挂了"的可能

#### 2. broker 端跨节点指标对照（5 分钟）

```bash
# 对每个 emqx 节点跑：
for i in 0 1 2; do
  echo "=== emqx-$i ==="
  kubectl exec -n cuav-cloud cuav-base-emqx-$i -- \
    emqx_ctl broker metrics 2>/dev/null | grep -E 'dropped|received|publish' | head -10
done
```

看 `messages.dropped.no_subscribers / messages.received` 比例：
- 所有节点 <1% → 不是本案例
- **某一个节点 >30% 而其他节点接近 0%** → 强烈指向本案例

#### 3. 跨节点路由表条数对照（2 分钟）

```bash
for i in 0 1 2; do
  echo "=== emqx-$i topics count ==="
  kubectl exec -n cuav-cloud cuav-base-emqx-$i -- \
    emqx_ctl topics list 2>/dev/null | wc -l
done
```

如果差距 >5 条（尤其是出现 3 vs 41 这种数量级差距）→ **基本确认本案例**

#### 4. 跨节点 publish 实验（金标准，10 分钟）

通过 EMQX HTTP API（`/api/v5/publish`）**直接访问每个节点的 dashboard 端口** publish 同一条消息（同 topic / 同 payload，加唯一 tid 区分），同时在订阅者侧 grep tid：

```bash
# 通过 headless service 直连每个 pod
for i in 0 1 2; do
  EMQX_HOST="cuav-base-emqx-$i.cuav-base-emqx-headless.cuav-cloud.svc.cluster.local"
  TOKEN=$(curl -sS -X POST http://${EMQX_HOST}:18083/api/v5/login \
    -H 'Content-Type: application/json' \
    -d '{"username":"admin","password":"<dashboard-pwd>"}' \
    | sed -E 's/.*"token":"([^"]+)".*/\1/')
  echo "--- publish to emqx-$i ---"
  curl -sS -X POST "http://${EMQX_HOST}:18083/api/v5/publish" \
    -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' \
    -d '{"topic":"<target-topic>","payload":"VEVTVA==","payload_encoding":"base64","qos":1,"retain":false}'
done
```

观察响应：
- `{"id":"..."}` → 消息成功路由
- `{"message":"no_matching_subscribers","reason_code":16}` → **该节点路由表残缺，铁证！**

再去订阅侧日志 grep tid，确认哪些节点的 publish 真的到达了。

#### 5. 直接审计故障节点的路由表（5 分钟）

```bash
# 在故障节点上：
emqx_ctl topics list | head -50
emqx_ctl topics list | grep -E 'thing/product/\+/'  # 看 wildcard 订阅
```

对比健康节点：
- 故障节点缺失大部分 wildcard 订阅
- 故障节点只有少量本节点客户端的订阅

#### 6. 审计 mria 状态（10 分钟）

```bash
emqx_ctl mnesia
```

关注：
- `running db nodes` 是否完整
- `master node tables` 是否为空（空是正常的）
- `emqx_route` 表的 `ram_copies` 节点列表

通常 mria 状态看起来"正常"——这正是 bug 的迷惑性。

---

## 修复方案

### 根治（P0，必做）

**对故障节点执行 cluster leave + cluster join，强制 mria 全量重新同步**：

```bash
# 在故障节点（如 emqx-0）上执行：
emqx_ctl cluster leave
# 输出：Leave the cluster successfully.
# 此时该节点 cluster status 只剩自己

emqx_ctl cluster join cuav-base@cuav-base-emqx-1.cuav-base-emqx-headless.cuav-cloud.svc.cluster.local
# 输出：Join the cluster successfully.
# mria 会触发全量 bootstrap，从 core node 拉取所有表
```

**关键**：
- `cluster leave` 不会清掉本地数据文件，但会让节点"忘记自己是老成员"
- 重新 `join` 时 mria 会做全量 bootstrap，路由表会从 core node 完整复制过来
- 影响面：连在该节点的客户端会断线重连一次（约 1-2 秒），重连后 LB 可能分到任意节点

**不要做的事**：
- ❌ 直接 `kubectl delete pod` —— 持久化数据导致重启不修复
- ❌ 直接清掉 `/opt/emqx/data/mnesia/<node>/` 后重启 —— 风险大，可能丢配置（认证表、admin 账户等是 disc_copies）
- ⚠️ 实在不行才用：先 `cluster leave`，停 pod，清 hostPath，再启动 → 等价于全新加入

### 兜底 / 防御（P1，推荐）

1. **加监控告警（最重要）**  
   - 各节点 `messages.dropped.no_subscribers / messages.received` 比例（>5% 告警）
   - 各节点 `emqx_ctl topics list | wc -l` 的两两差值（差值 >5 告警）
   - 这两个指标是本案例的**唯一可靠预警信号**，cluster status 完全不可靠

2. **客户端侧自动重连 + 退避**  
   万一节点路由表残缺，客户端断线重连有机会落到健康节点，缓解业务影响

3. **关键 publish 加 ACK 验证**  
   重要业务消息（如 register）publish 后等待 reply，超时未到则告警/重试

### 加固 / 清理（P2，长期）

1. **EMQX 升级**  
   5.1.3 是相对早期的 5.x 版本，mria 同步在后续版本（5.4+）有大量稳定性修复。评估升级到 5.4+ / 5.6+
2. **运维剧本固化**  
   把"路由表残缺诊断 + leave/join 修复"固化为 runbook，让运维能 5 分钟内独立处理
3. **避免使用 hostPath**  
   改用 PVC + 标准 StorageClass。hostPath 会让节点漂移时数据丢失/错位，加剧 mria 同步问题
4. **集群拓扑审计**  
   评估是否需要拆分 core/replicant 角色（5.x 支持），避免所有节点都是 core 时同步链路过于复杂

---

## 预防清单（Checklist）

### EMQX 部署/运维阶段

- [ ] 部署 EMQX 5.x 集群时使用 PVC 而非 hostPath
- [ ] 监控 `messages.dropped.no_subscribers` 占比，单节点 >5% 告警
- [ ] 监控各节点 `topics list` 条数差异，差值 >5 告警
- [ ] 不要只靠 `cluster status` 判断集群健康（它不能反映 mria 同步状态）
- [ ] 节点异常重启 / OOM / 网络抖动后，主动跑一次跨节点 publish 验证

### 服务接入 EMQX 时

- [ ] 服务侧 MQTT client 配置自动重连 + 指数退避
- [ ] 关键 publish（register / 命令下发）加 ACK 验证机制，不要 fire-and-forget
- [ ] 服务侧关键 topic 的"过去 N 分钟收到消息数"做指标，0 持续 N 分钟告警

### Review / 上线阶段

- [ ] 看到"某 topic 设备一直发但服务收不到、其他 topic 正常" → 立刻怀疑 broker 路由问题
- [ ] 看到"重启某 broker 节点后问题没好" → 不要继续重启，跑跨节点指标对照
- [ ] 看到"客户端重连一下就好了，但又会复发" → 强烈怀疑某个节点路由表问题，做跨节点 publish 实验

---

## 同类间歇性 bug 的 Playbook

遇到"MQTT 设备发了消息服务收不到 / 收消息时灵时不灵 / 某些 topic 通某些不通"的现象时，按此顺序走：

### Step 1：业务侧确认是哪一类"收不到"（5 分钟）

订阅服务的入口 logger（统一打印 received topic 那种）grep 目标 topic：
- 完全 0 条 → 消息没到服务侧，问题在 broker 路由 / 订阅链路
- 有部分能收 → 问题更可能在 publisher 侧（QoS、断连、重发等）

### Step 2：跨节点 broker 指标对照（5 分钟）

每个节点跑 `emqx_ctl broker metrics`，对比 `dropped.no_subscribers` 比例：
- 单节点异常高 → **强烈指向本案例**（路由表同步故障）
- 全节点都低 → 问题不在 broker 路由，去查订阅者

### Step 3：跨节点路由表条数对照（2 分钟）

`emqx_ctl topics list | wc -l` 在每个节点跑一遍。差异巨大 → **基本确认本案例**。

### Step 4：跨节点 publish 实验确认故障节点（10 分钟）

用 HTTP API 从每个节点 publish 同一条消息，看哪个返回 `no_matching_subscribers`。

### Step 5：执行 cluster leave + join 修复（2 分钟）

在故障节点上：`emqx_ctl cluster leave` → `emqx_ctl cluster join <healthy-node>`。

### Step 6：再次跨节点 publish 验证修复（5 分钟）

重复 Step 4，确认所有节点 publish 都成功。

### Step 7：补告警 + 写复盘（30 分钟）

- 加监控指标（dropped 比例、topics 条数差）
- 写故障复盘，固化排查 runbook

---

## 参考资料

### 本案例相关 K8S 资源（项目：cuav-cloud）

- StatefulSet：`cuav-base-emqx`（namespace `cuav-cloud`）
- Pod：`cuav-base-emqx-0` / `cuav-base-emqx-1` / `cuav-base-emqx-2`
- Service：`cuav-base-emqx`（普通 ClusterIP）+ `cuav-base-emqx-headless`（headless，按 pod 直连）
- 持久化：`hostPath: /opt/cloud/hostPath/emqx-ha/emqx-data`
- EMQX 版本：5.1.3
- Dashboard 端口：18083；MQTT 端口：1883

### 服务侧相关代码

- 入站消息统一入口（确认是否真没收到）：`cuavcloudcbb/CuavCloudBasicCBB/AccessAdapterCBB/src/main/java/com/cuav/access/adapter/mqtt/InboundMessageRouter.java`
- MQTT 调用日志：`/logs/ms_log/cuav-cloud-access-service/mqtt_call.log`
- 日志配置：`cuavcloudopensource/CuavCloudOpenSource/OpenSourceDependency/src/main/resources/logback-spring.xml`（`MQTT_LOG` appender）

### 关键 EMQX 命令速查

```bash
# 集群成员关系（不可靠：mria 同步问题时也显示正常）
emqx_ctl cluster status

# mria 状态（看 ram_copies / disc_copies 节点分布）
emqx_ctl mnesia

# 路由表（关键诊断指标）
emqx_ctl topics list | wc -l
emqx_ctl topics list | grep '<topic-pattern>'

# broker 全局指标
emqx_ctl broker metrics | grep -E 'dropped|received|publish'

# 客户端订阅清单
curl -H "Authorization: Bearer $TOKEN" \
  http://emqx:18083/api/v5/clients/<clientid>/subscriptions

# HTTP API publish（绕过 client，直接走 broker 内部路由）
curl -X POST http://emqx:18083/api/v5/publish \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"topic":"...","payload":"<base64>","payload_encoding":"base64","qos":1}'

# 修复命令（在故障节点执行）
emqx_ctl cluster leave
emqx_ctl cluster join <healthy-node-name>
```

### 关键概念

- EMQX 5.x mria（mnesia + 复制层）架构
- mnesia `ram_copies` vs `disc_copies` vs `null_copies`
- `emqx_route` 表（路由表）的全集群复制机制
- core node vs replicant node 角色
- ekka 集群成员管理 vs mria 数据复制（两套独立机制）
- HTTP API publish 的 `no_matching_subscribers` (reason_code 16)
- StatefulSet hostPath 持久化对集群一致性的副作用

### 一句话总结

> **EMQX 集群"看起来健康"`cluster status` 全 running、ACL 全开，但某节点 publish 全部被吞、其他节点正常——铁证是 `dropped.no_subscribers` 单节点 >30% 且 `topics list` 条数异常少。这不是连接问题、不是订阅问题、不是 ACL 问题，而是 mria 路由表与集群失同步。重启 pod 因为持久化数据会跳过全量 bootstrap 而无效，必须 `cluster leave` + `cluster join` 强制重同步才能修复。**
