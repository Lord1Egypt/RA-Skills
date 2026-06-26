# BUG04: MQTT 客户端凭空 `reason=7` 频繁断开 —— 同 ClientID 抢连接触发 broker 端 session takeover

## 案例摘要

嵌入式设备 / MQTT 客户端在没有任何明显网络故障、没有任何"有毒消息"的情况下，频繁报 `reason=7 (Unknown reason)` 断开，且断开后 ~1 秒内自动重连成功，呈现"几秒一次的 ping-pong"模式。逐条 publish 时间线对比发现 **3 次 disconnect 前一刻的 publish 互不相同**（osd / heartbeat / services_reply 都有），断开都发生在 broker **已经 ACK 完上一条 publish 之后**——说明断开**不是设备 publish 的任何一条特定消息触发的**。后端业务侧依然能持续收到该 SN 的消息（甚至同 SN 的 osd 消息频率从 60/min 突增到 131/min）。

根因是**两个 MQTT 客户端用了同一个 ClientID 同时连 broker**：MQTT 协议规定同一 ClientID 只能存在一个会话，broker 在新连接进来时会立刻断掉旧连接，**且按 EMQX 实现是直接 close TCP socket、不发 MQTT DISCONNECT 包**。设备侧的 `libmosquitto` / paho 等客户端只看到 TCP 被切，没收到协议层断开包，于是统一报为 `MOSQ_ERR_CONN_LOST = 7 / Unknown reason`——这就是 reason=7 与"具体 topic / 消息内容无任何因果关系"的根本原因。

---

## 症状 / 特征速查（用于匹配）

> 下列特征命中 **4 条及以上** 时，高概率是本案例；命中 **2-3 条** 也值得优先按本案例思路排查。

### 设备侧（MQTT client）现象

- [ ] 客户端报 `reason=7` 或 `MOSQ_ERR_CONN_LOST` 或 `Unknown reason` 断开（libmosquitto）；paho 报 `cause = "connection lost"`
- [ ] **断开后 1 秒内**就成功自动重连，紧接着几秒到几十秒后**再次以相同 reason 断开**，循环往复（ping-pong）
- [ ] 断开发生时设备**正常 publish 中**，没有任何"我刚发了一条特殊消息"的特征
- [ ] 把 disconnect 前最后几条 publish 列出来对比：**几次 disconnect 前的最后一条 publish 互不相同**（osd / heartbeat / services_reply 都有可能）
- [ ] 设备 publish 都已经 OnMessagePublished 成功（broker 回过 ACK），断开发生在 ACK 完成**之后**几十~几百毫秒
- [ ] 设备上没有任何 keepalive timeout / network unreachable 等明确的网络异常日志
- [ ] 设备所在网络环境（局域网 / 4G / wifi）平时使用 ssh / curl 都正常，没有 TCP 异常

### 后端业务侧现象（最容易被忽略的关键证据）

- [ ] 同一个设备 SN 在断开期间，**后端依然在持续收到该 SN 的消息**
- [ ] 该 SN 的某类高频消息（如 osd / heartbeat）在某段时间内**计数显著翻倍**（如平时 60/min → 突增到 100+/min）
- [ ] 同一个主设备 SN 的 `register` 报文里，**`sub_device_list` 在不同时段不一致**（早上是一份子设备清单，下午同一 SN 的报文里却是另一份清单）
- [ ] 同一个 SN 上报的 location / temperature / version 等"应当稳定"的字段，在不同时段呈现互相矛盾的值

### EMQX 端指标特征（铁证级！）

- [ ] `emqx_ctl broker metrics` 里 **`packets.disconnect.sent = 0`** 而 `packets.disconnect.received` 不为 0 → broker 完全不走 MQTT 协议层踢人，所有断开都是"硬切 TCP"
- [ ] **`session.discarded` 持续快速增长**，体量远大于 `client.connected`（如 client.connected=9075 但 session.discarded=8778，比例接近 1:1）
- [ ] `session.takenover` 也在累加（虽然数值通常远小于 discarded）
- [ ] `emqx_ctl clients show <clientid>` 此刻可能只能看到 **0 个或 1 个** 该 ClientID 的连接（因为两边在抢，瞬时只能一方在线）
- [ ] EMQX 日志里能看到 `terminate_session` / `kicked` / `discarded` 关键字伴随同一 ClientID 反复出现

### 反向排除项

- 如果设备日志里出现明确的 `keepalive timeout` / `socket error: ETIMEDOUT` → 不是本案例，是真网络断
- 如果 broker `packets.disconnect.sent > 0` 且与 reason=7 频次接近 → 不是本案例，broker 是走协议层踢的（认证失败 / ACL 拒绝 / 协议错误），需要看具体 reason code
- 如果设备的 disconnect 频次和 keepalive 周期严格对齐（每隔 keepalive 秒数恰好断一次）→ 不是本案例，是 keepalive 网络抖动
- 如果 broker 端 `session.discarded` 长期为 0 或增长极慢 → 不是本案例，没有同 ClientID 抢连接
- 如果只有 1 个物理设备实例在运行、确认全网没有第二个客户端用同 ClientID → 不是本案例，转查网络层 / NAT / 防火墙
- 如果断开伴随 broker 节点的负载暴涨 / OOM / GC stop-the-world → 不是本案例，是 broker 自身故障

### 关键日志/指标指纹

```text
# 设备侧（libmosquitto，典型 ping-pong 模式）
2026-04-27 12:15:33:576 WARN  [OnDisconnected:182] mosquitto disconnected (reason=7: Unknown reason).
2026-04-27 12:15:33:576 WARN  [OnStateChange:306] MQTT disconnected (reason=7), auto-reconnect pending.
2026-04-27 12:15:33:577 DEBUG [Publish:102] drop publish while disconnected: topic=thing/product/<sn>/osd
... ~900ms 后 ...
2026-04-27 12:15:34:593 INFO  [OnConnected:xxx] mosquitto reconnected.
... 又持续 ~3.8s ...
2026-04-27 12:15:38:458 WARN  [OnDisconnected:182] mosquitto disconnected (reason=7: Unknown reason).
... 1s 后又连上 ...
2026-04-27 12:15:41:613 WARN  [OnDisconnected:182] mosquitto disconnected (reason=7: Unknown reason).
（9 秒内断 3 次）

# EMQX broker metrics（关键指纹：sent=0 + discarded 巨量）
packets.connect.received   : 9075
packets.disconnect.received: 272      # client 主动断（含 ping-pong 重连前的 DISCONNECT）
packets.disconnect.sent    : 0        # 关键！broker 完全不发 DISCONNECT，全部硬切
session.created            : 9074
session.discarded          : 8778     # 关键！约等于 created → 每个 session 都被踢过
session.takenover          : 1
session.terminated         : 294

# 后端业务侧（某 SN 的消息频率突变）
12:14 cuav-cloud-access-service: SN=SSF200-SN-zOwR7ZaN2YXy osd messages = 60/min   ← 正常
12:15 cuav-cloud-access-service: SN=SSF200-SN-zOwR7ZaN2YXy osd messages = 131/min  ← 翻倍！
12:16 cuav-cloud-access-service: SN=SSF200-SN-zOwR7ZaN2YXy osd messages = 60/min   ← 一方退出后恢复

# 同一 SN 的 register 报文 sub_device_list 不一致（最容易忽略的金线索）
# 上午：
"sub_devices":[{"sn":"SUB_SN_PTZ"},{"sn":"SUB_SN_DPH130_1"},{"sn":"SUB_SN_DPH130_2"},
                {"sn":"SUB_SN_DPH130_3"},{"sn":"SUB_SN_DPH130_4"},{"sn":"SUB_SN_STF200"}]
# 下午（同 SN 不同 register）：
"sub_devices":[{"sn":"PTZ-SN-8bBAhBnqcrjJ"},{"sn":"DPH100-SN-CQNcSOrJ7S"},
                {"sn":"DPH100-SN-yojteUlDwe"}]
```

---

## 详细说明 / 根因链路

### 三层因素拆解

| 层 | 内容 | 单独看是否必然出 bug |
|---|---|---|
| **协议层** | MQTT 规范要求"同一 ClientID 全局唯一"；broker 收到新 CONNECT 时若发现旧 session 存在，**必须**断掉旧连接以保证唯一性 | 不是 bug（标准设计） |
| **broker 实现层** | EMQX 在 takeover 时直接 close TCP socket，**不向旧连接发 MQTT DISCONNECT 包**——MQTT spec 允许这种实现，但客户端无法分辨"被踢"和"网络断" | 不是 bug（性能优化） |
| **业务/运维层** | 多个客户端实例（设备 / MQTTX / 测试程序 / 烧错 SN 的另一台设备）实际使用了同一个 ClientID 连接同一个 broker | **这是真正的 bug 触发条件** |

### MQTT Session Takeover 的精确机制

```text
[Client A] ─ TCP ─→ broker：用 clientid="X" 连接，状态正常
[Client A] 持续 publish/subscribe ...

[Client B] ─ TCP ─→ broker：用 clientid="X" 也来连接（CONNECT 包）
       │
broker 收到新 CONNECT(clientid="X")：
       ├─► 查内部 session 表，发现 clientid="X" 已经有 session（属于 Client A）
       ├─► 触发 session takeover 流程
       │      ├─► [关键] 直接 close Client A 的 TCP socket
       │      │   （不构造 MQTT DISCONNECT packet 发出去！）
       │      ├─► session.discarded ++（如果新 client 是 clean_start=true）
       │      └─► session.takenover ++（如果新 client 是 clean_start=false）
       └─► 接受 Client B 的连接，回 CONNACK

[Client A] 视角：
       ├─► socket recv() 返回 0 / EPIPE / ECONNRESET
       ├─► libmosquitto 把 TCP 层错误统一映射为 MOSQ_ERR_CONN_LOST = 7
       ├─► OnDisconnected callback(reason=7, "Unknown reason")
       ├─► 触发自动重连机制（默认 1 秒后）
       └─► 重连成功后再次用 clientid="X" 连接 broker
                ↓
       [现在反过来，Client B 被踢，看到的也是 reason=7]
                ↓
       Client B 也开始重连 → 又把 Client A 踢掉 → ping-pong 死循环
```

### 为什么 `reason=7` 是个"看不出真因"的报错

`reason=7` 是 libmosquitto 内部的 `MOSQ_ERR_CONN_LOST` 错误码，**不是 MQTT 协议层的 reason code**。它涵盖了所有"TCP 层突然断开"的情况：

| TCP 层事件 | mosquitto 看到的 |
|---|---|
| 对端 close socket | recv() = 0 → MOSQ_ERR_CONN_LOST (7) |
| 对端 RST | recv() = -1, errno=ECONNRESET → MOSQ_ERR_CONN_LOST (7) |
| keepalive 超时主动断 | 内部计时器触发 → MOSQ_ERR_KEEPALIVE，但有些版本仍归到 7 |
| broker takeover 关连接 | recv() = 0 → MOSQ_ERR_CONN_LOST (7) |
| 网络中间件超时回收 | 同上 → MOSQ_ERR_CONN_LOST (7) |

所以**在设备侧的日志里，reason=7 永远无法区分"被 broker 踢"和"真断网"**，必须**反推 broker 端**才能确认真因。

### 为什么 broker 不发 MQTT DISCONNECT 包

- MQTT 5 spec 允许 broker 在某些场景**直接关闭 TCP** 而不发 DISCONNECT（"Server is allowed to disconnect a client without notice"）
- EMQX 的 takeover 实现就是走这条快路径——节省 1 个 packet 的开销
- **副作用**：客户端无法通过协议层得知"我被踢了"，只能靠 TCP 层错误猜测
- **诊断侧**的判别方式：看 broker 端的 **`packets.disconnect.sent`**——如果它一直为 0 但客户端却频繁断，就是 broker 在硬切 TCP

### 为什么会出现"同 ClientID 抢连接"

实际生产中常见诱因：

| 诱因 | 典型场景 |
|---|---|
| **多台设备烧了同一个 SN** | 出厂烧录脚本 bug、克隆固件忘改 SN、测试设备和现场设备共用 SN |
| **MQTTX / 测试工具用了和真实设备相同的 ClientID** | 排查问题时手动改 MQTTX 的 ClientID 配成真实设备 SN，没改回来 |
| **同一物理设备的多个进程都在连 broker** | 设备上跑了两份 nexus_gateway（一个是手动启的、一个是 systemd 守护的） |
| **container/pod 漂移导致两个实例共存** | 旧 pod 还没完全死、新 pod 已经起来，两个都在连 |
| **CI / 自动化测试和真实业务环境共用 SN** | 测试用例里直接用了线上设备的 SN 做端到端测试 |

### 为什么后端业务侧的 osd 消息频率会突增

这是最容易被忽略但**最有诊断价值**的现象：

```text
正常情况：
  Device A (clientid=X) → broker → access-service
  访问频率 = 60 osd msg/min（设备的固定上报频率）

发生 takeover 期间：
  Device A (clientid=X) ─┬→ broker → access-service
  Device B (clientid=X) ─┘
  
  虽然两个 client 在 broker 那里互踢、各自只能保持 ~1 秒在线，
  但每个 client 都在持续 publish 自己的 osd（清醒着的那 1 秒里）
  
  叠加效果 = 设备 A 的 60/min × 在线时间占比 + 设备 B 的 60/min × 在线时间占比
            ≈ 总量翻倍（约 100~130/min）

一方退出后：
  只剩 Device A 持续在线
  访问频率回到 60 osd msg/min
```

如果后端有按 SN 维度的消息频率监控，**这个突增是判断"两个客户端同 ID 抢连接"的最佳遥感信号**。

### 为什么 sub_device_list 不一致是"金线索"

主设备 `register` 报文里的 `sub_device_list` 反映的是**该物理设备真实接入的下属硬件**——这个清单**不应该在同一台设备上随时间变化**。如果同一个主设备 SN 上报的 `sub_device_list` 在不同时段呈现完全不同的内容（如 `SUB_SN_PTZ / SUB_SN_DPH130_*` vs `PTZ-SN-xxx / DPH100-SN-xxx`），**这就是两台不同的物理设备共用同一主设备 SN 的铁证**——不是同一台设备的状态变化，而是不同设备在用同一个身份各报各的。

---

## 排查方法论

### 使用到的核心技术

| 技术 | 用途 | 何时用 |
|---|---|---|
| **设备侧 disconnect 时间序列分析** | 把所有 disconnect 时间点拉出来，看间隔是否固定（固定 → 偏向 keepalive；不固定且都跟着自动重连 → 偏向 takeover） | 第一步必做 |
| **disconnect 前 publish 序列对比** | 把每次 disconnect 前一刻的 publish topic / mid 列出来，看是否有共性（无共性 → 排除"有毒消息"假设） | 反驳"是某条特定消息触发"的快速手段 |
| **broker 端 packets.disconnect.sent 对照** | 看 broker 是否真有发 MQTT DISCONNECT 包（=0 → 走 TCP 硬切，强烈指向 takeover） | 区分协议层踢 vs TCP 硬切的金标准 |
| **broker 端 session.discarded / takenover 监控** | 这两个计数的快速增长是 takeover 的直接遥感 | 判断 ClientID 冲突频度 |
| **跨时间段 register 内容对比** | 同一 SN 不同时段的 register 报文 `sub_device_list` 是否一致 | 物理设备共用 SN 的金线索 |
| **后端按 SN 维度的消息频率监控** | 某 SN 的 osd / heartbeat 频率是否突然翻倍 | 双客户端共存的旁证 |
| **抓取 broker 端的连接审计日志** | EMQX hook / webhook 监听 `client.connected` / `client.disconnected` 事件，记录 ClientID + 来源 IP | 反查"哪个 IP 在抢连接" |

### 诊断步骤（按顺序）

#### 1. 设备侧 disconnect 时间序列与 publish 序列分析（10 分钟）

收集设备日志中所有 `disconnected (reason=7)` 的时间点，列出每次断开**前 1 秒内**的所有 publish：

- 看断开间隔：是固定周期（疑似 keepalive） vs 不固定（疑似外部事件触发）
- 看 publish 序列：每次断开前的最后一条 publish 是否一致（一致 → 怀疑有毒消息；不一致 → 排除有毒消息）
- 看断开后的重连耗时：极快（<2 秒）→ 网络通路正常，倾向于"被主动断"

**判定：如果断开间隔不固定 + 每次断前 publish 不一致 + 重连极快 → 强烈指向 takeover**

#### 2. broker 端 disconnect.sent / disconnect.received 对照（2 分钟）

```bash
for i in 0 1 2; do
  echo "=== emqx-$i ==="
  kubectl exec -n cuav-cloud cuav-base-emqx-$i -- \
    emqx_ctl broker metrics 2>/dev/null | grep -E 'disconnect|takeover|discarded|takenover'
done
```

判断：
- `packets.disconnect.received > 0` 而 **`packets.disconnect.sent = 0`** → broker 在硬切 TCP，强烈指向 takeover
- `packets.disconnect.sent` 有数值且与 received 大致相当 → broker 走协议层踢（看具体 reason code，不是本案例）

#### 3. broker 端 session.discarded / takenover 量级评估（2 分钟）

继续看上一步的输出，关注：

- `session.discarded` 与 `session.created` 的比例：接近 1:1 → 几乎每个 session 都被踢过，说明 ClientID 抢连接非常普遍
- `session.takenover` 持续增长 → clean_start=false 的 takeover 在发生

#### 4. 锁定具体冲突的 ClientID（10 分钟）

启动 EMQX 的连接事件 webhook（或者临时打开 `client.connected` / `client.disconnected` 的 audit log），记录每次连接的 `clientid + src_ip + src_port + connected_at`，然后：

```bash
# 把目标 SN 在过去 1 小时内的所有连接事件拉出来
grep '"clientid":"<target-sn>"' audit.log | jq -r '[.event, .src_ip, .src_port, .ts] | @tsv'
```

判断：
- 同一 ClientID **来源 IP 有 2 个以上** → 100% 确认有多客户端共用 ID
- 同一 ClientID 来源 IP 只有 1 个但 src_port 频繁变化 + 频次极高 → 同一台机器多个进程

#### 5. 跨时间段 register 内容对比（5 分钟）

从 `mqtt_call.log` 里把同一 SN 的 register 报文按时间排序，重点对比 `sub_device_list`：

```bash
grep '"method":"device_register".*"<target-sn>"' mqtt_call.log \
  | jq -r '[.timestamp, (.data.sub_devices | map(.sn) | join(","))] | @tsv'
```

判断：
- 不同时段 `sub_device_list` 完全不同 → 不同物理设备共用 SN
- 一直一致 → 单一物理设备，但可能与 MQTTX 等测试工具冲突

#### 6. 后端按 SN 维度的消息频率监控（5 分钟）

查 access-service 的 `mqtt_call.log`（或 broker metrics 的 topic 维度数据），统计目标 SN 的 osd / heartbeat 频率，按分钟分桶：

```bash
grep '/<target-sn>/osd' mqtt_call.log | awk '{print substr($1,1,16)}' | sort | uniq -c
```

判断：
- 某段时间频率明显高于基线（如 60/min → 130/min） → 双客户端在线的旁证

---

## 修复方案

### 根治（P0，必做）

**核心动作：彻底消除 ClientID 冲突**

实施路径要根据 step 4 / 5 / 6 的诊断结果分场景处理：

| 诊断结果 | 处理动作 |
|---|---|
| 多个物理设备烧了同一 SN | 排查烧录流程；停用其中一台或重新烧入唯一 SN |
| MQTTX / 测试工具用了真实设备 SN | 立刻停掉 MQTTX 或改 ClientID 加专属后缀（如 `-mqttx-<random>`） |
| 同一台设备多个进程在连 | 排查启动流程，确保只有一份 nexus_gateway 在运行（systemd / supervisord） |
| 容器漂移多实例并存 | k8s 侧排查 StatefulSet pod 是否真的全部就绪、有无残留 pod；调整 podManagementPolicy |

**不要做的事**：

- ❌ 直接重启 broker —— 治标不治本，冲突的两边只要在重启完成后还都活着，问题立刻复发
- ❌ 仅在 broker 侧调大 keepalive、放宽 idle —— 与本 bug 无关，反而掩盖问题
- ❌ 给设备做"自动避让 / 退避重连" —— 治标不治本，会从 ping-pong 变成"间歇性失联"
- ❌ 关掉 EMQX 的 takeover 强制策略 —— 违反 MQTT 协议规范，会引入更深的状态一致性问题

### 兜底 / 防御（P1，推荐）

1. **MQTT 客户端侧改造**  
   - 连接时显式带 `clean_start=false` + 持久化 session，能保证 takeover 后不丢未确认消息
   - `OnDisconnected` 回调里**记录 reason 之外，再记录"距上次 disconnect 的时间间隔" + "上次成功连接时长"**，方便后续运维区分 takeover vs 真网络断
   - 重连退避策略**不要用纯 1 秒固定退避**——这会在 ClientID 冲突时形成完美的 ping-pong；改用指数退避 + 抖动（jitter），能让两个冲突方更快失衡，让其中一个最终长期失败，从而暴露问题而不是隐藏问题

2. **broker 端连接审计常驻**  
   - 启用 EMQX 的 webhook（或 hook plugin）持续记录 `client.connected` / `client.disconnected` 事件
   - 提供"按 ClientID 反查所有连接来源 IP"的运维接口（最好做成 dashboard 一键查询）

3. **关键 publish 加端到端 ACK 验证**  
   - 重要业务消息（register / 命令下发）publish 后等待 reply，超时未到则告警 + 记录"当时是否被 takeover"

### 加固 / 清理（P2，长期）

1. **ClientID 唯一性强约束**  
   - SN 烧录流程加入"全局唯一性校验"（出厂前查中心化 SN 数据库）
   - broker 侧开启 `prevent_duplicate_clientid`（如有此类插件 / 配置）或自研 hook：相同 ClientID 第二次连接时直接拒绝并告警，而不是默默 takeover

2. **监控告警体系**  
   - `session.discarded` 增长率告警（如 5 分钟内增量 > 100 → 告警）
   - `packets.disconnect.sent / packets.disconnect.received` 比值长期为 0 → 告警（意味着所有断开都是硬切）
   - **业务侧**按 SN 维度的消息频率监控，超过基线 1.5 倍 → 告警（强烈预示 ClientID 冲突）

3. **运维剧本固化**  
   - "看到 reason=7 频繁断开 + 后端业务正常" → 进入本剧本
   - "看到某 SN 消息频率突增" → 进入本剧本
   - 把 step 1~6 的诊断流程固化为运维 runbook

4. **测试工具治理**  
   - 团队内禁用"用真实设备 SN 做 MQTTX 客户端 ID"的实践
   - 提供 MQTTX 的 ClientID 模板（如 `<sn>-mqttx-<user>-<rand>`），从源头杜绝冲突

---

## 预防清单（Checklist）

### 设备 / 客户端开发阶段

- [ ] MQTT 客户端连接配置项里 ClientID 来源唯一（建议 = 设备 SN，且 SN 全局唯一）
- [ ] `OnDisconnected` 回调记录 reason、上次连接时长、距上次断开间隔，便于事后分析
- [ ] 重连退避使用指数退避 + 随机抖动，避免和冲突方形成完美 ping-pong
- [ ] 客户端启动时自检"本进程是否已有另一份在运行"（pid 文件 / systemd）

### SN / ClientID 管理

- [ ] 出厂烧录 SN 全局唯一，烧录脚本支持唯一性校验
- [ ] 测试 / 排查工具（MQTTX / 自研脚本）的 ClientID 必须带专属后缀，禁止与真实设备 SN 重复
- [ ] CI / 自动化测试不得复用真实生产设备 SN

### 部署 / 运维阶段

- [ ] EMQX 启用 `client.connected` / `client.disconnected` 事件审计（webhook 或 hook 插件）
- [ ] 监控 `session.discarded` / `session.takenover` 增长率，5 分钟内突增告警
- [ ] 监控 `packets.disconnect.sent` 是否为 0 + `packets.disconnect.received` 是否非零（"全 TCP 硬切"特征告警）
- [ ] 业务侧按 SN 维度监控关键 topic 消息频率，超基线 1.5 倍告警

### Review / 排查阶段

- [ ] 看到"客户端 reason=7 频繁断 + 后端业务依然在收同 SN 消息" → 立刻按本案例排查 ClientID 冲突
- [ ] 看到"同 SN 不同时段 register 内容不一致" → 立刻确认是否多设备共用 SN
- [ ] 看到"某 SN 消息频率突增近 2 倍" → 立刻按本案例排查
- [ ] 不要被 reason=7 的"Unknown reason"字面误导成"网络问题/未知错误"，**它不能反映真因**

---

## 同类间歇性 bug 的 Playbook

遇到"MQTT 客户端反复断开但网络看起来又正常 / 设备 publish 完就被踢 / 后端业务依然在收同 SN 消息"现象时，按此顺序走：

### Step 1：设备侧 disconnect 时间序列分析（10 分钟）

把所有 reason=7 的时间点列出来，看间隔是否固定 + 看每次断前的 publish 序列。
- 间隔不固定 + publish 序列无共性 → 强烈倾向 takeover
- 间隔固定（如恰好 = keepalive） → 倾向 keepalive 网络抖动

### Step 2：broker 端 packets.disconnect.sent 对照（2 分钟）

`emqx_ctl broker metrics | grep disconnect`：
- `sent = 0` 而 `received > 0` → broker 在硬切 TCP，**强烈指向本案例**
- `sent > 0` 且 ≈ received → broker 走协议层踢，去看 reason code，不是本案例

### Step 3：broker 端 session.discarded 量级评估（2 分钟）

继续看 metrics：
- `session.discarded / session.created ≈ 1` → 几乎每个 session 都被踢过，**基本确认本案例**
- 这个比例长期很低 → 否定本案例

### Step 4：锁定具体冲突的 ClientID（10 分钟）

打开连接审计日志，按 ClientID 拉所有连接的来源 IP / 端口：
- 来源 IP 有 2 个以上 → 100% 确认多客户端共用 ID
- 同 IP 但多 src_port 高频 → 同机器多进程

### Step 5：跨时间段 register 对比 + 业务消息频率验证（5 分钟）

- register 的 sub_device_list 不一致 → 多物理设备共用 SN 的铁证
- 业务侧某 SN 消息频率突增近 2 倍 → 双客户端在线的旁证

### Step 6：根治（视场景定）

按 step 4 / 5 的诊断结果定位冲突源（多设备 / MQTTX / 多进程 / 容器漂移），分别处理。

### Step 7：补告警 + 写复盘（30 分钟）

- 加 session.discarded 增长率监控、disconnect.sent=0 异常告警、按 SN 消息频率监控
- 把诊断流程固化为运维 runbook

---

## 参考资料

### 本案例相关 K8S 资源（项目：cuav-cloud）

- StatefulSet：`cuav-base-emqx`（namespace `cuav-cloud`）
- Pod：`cuav-base-emqx-0` / `cuav-base-emqx-1` / `cuav-base-emqx-2`
- Service：`cuav-base-emqx`（普通 ClusterIP）+ `cuav-base-emqx-headless`（headless，按 pod 直连）
- EMQX 版本：5.1.3
- Dashboard 端口：18083；MQTT 端口：1883

### 服务侧相关代码

- 入站消息统一入口（按 SN 看消息频率）：`cuavcloudcbb/CuavCloudBasicCBB/AccessAdapterCBB/src/main/java/com/cuav/access/adapter/mqtt/InboundMessageRouter.java`
- MQTT 调用日志：`/logs/ms_log/cuav-cloud-access-service/mqtt_call.log`
- 日志配置：`cuavcloudopensource/CuavCloudOpenSource/OpenSourceDependency/src/main/resources/logback-spring.xml`（`MQTT_LOG` appender）

### 关键 EMQX 命令速查

```bash
# 全局指标 - 关键指纹（disconnect.sent / discarded / takenover）
emqx_ctl broker metrics | grep -E 'disconnect|takeover|discarded|takenover'

# 当前是否有目标 ClientID 在线（多个 broker 节点都查）
emqx_ctl clients show <clientid>

# 列出某节点所有当前连接（找疑似共用同 ClientID 的连接）
emqx_ctl clients list | grep <clientid>

# 用 HTTP API 拉某 ClientID 的最近连接历史（需打开审计）
curl -H "Authorization: Bearer $TOKEN" \
  http://emqx:18083/api/v5/clients/<clientid>

# 启用连接事件 webhook（持续记录 connected / disconnected）
# 在 emqx.conf 或 dashboard 配置 webhook，订阅 client.connected / client.disconnected
```

### MQTT 协议层 / 库层相关

- MQTT 5 spec §4.1 (Session State): "The Server MUST allow only one active connection per Client Identifier"
- libmosquitto 错误码定义：`mosquitto.h` 中的 `MOSQ_ERR_CONN_LOST = 7`，描述 "The client is not currently connected"，覆盖大部分 TCP 层断开
- paho 等价错误：`MQTTAsync_disconnected` 的 `cause = "connection lost"`

### 关键概念

- MQTT Session Takeover：同 ClientID 新连接进来时 broker 必须断开旧连接的协议要求
- broker "硬切 TCP" vs "协议层 DISCONNECT"：前者不发 packet，后者会发；前者让客户端无法判别真因
- libmosquitto MOSQ_ERR_CONN_LOST 的"歧义性"：reason=7 是一组 TCP 事件的统一映射，不能反推具体原因
- EMQX `session.discarded` vs `session.takenover`：前者对应 clean_start=true 的踢人，后者对应 clean_start=false 的接管
- `packets.disconnect.sent = 0` 作为"broker 走 TCP 硬切"的强信号

### 一句话总结

> **MQTT 客户端报 `reason=7` 频繁断开但网络看起来正常 + 后端业务依然在收同 SN 消息——铁证是 broker 端 `packets.disconnect.sent = 0` 而 `session.discarded` 持续暴涨。这不是网络问题、不是 broker 故障、不是设备发了"有毒消息"，而是有两个客户端用了同一个 ClientID 在 broker 那里互相把对方踢下线（session takeover）。`reason=7` 只是 libmosquitto 把"TCP 被 broker 硬切"误报成"未知原因"，必须反推 broker 端指标和连接审计才能识别真因。根治方法是消除 ClientID 冲突（停用冲突方 / 修烧录流程 / 测试工具加专属后缀），重启 broker 无效。**
