# BUG02: Netty 间歇性 eventLoop 终止后又自恢复 —— 动态编译打爆堆 × 重连放大

## 案例摘要

测试桩在压测/持续上报过程中，日志先出现 `RejectedExecutionException: event executor terminated`、`Force-closing a channel whose registration task was not accepted by an event loop`，随后又出现 `JdkCompiler` / `ProtobufProxy` 相关 `OutOfMemoryError: Java heap space`，但服务节点和 JVM 进程都**没有重启**，过一小段时间后连接又自动恢复、重新登录成功。根因不是远端服务彻底不可用，而是**本地进程在高频 protobuf 动态编译、重复 connect、重复心跳调度叠加下发生瞬时堆内存耗尽和连接风暴**，之后依靠 GC 回收和新连接重建表现出“自愈”。

---

## 症状 / 特征速查（用于匹配）

> 下列特征命中 **4 条及以上** 时，高概率是本案例；命中 **2-3 条** 也值得优先按本案例思路排查。

### 表面现象

- [ ] 日志先报 `event executor terminated` / `registration task was not accepted by an event loop`
- [ ] 同一时间窗内又出现 `OutOfMemoryError: Java heap space`
- [ ] OOM 没有把整个 JVM 打死，进程和节点都没重启
- [ ] 过几十秒到几分钟后，连接又自动恢复，后续还能看到“连接成功 / 登录成功”
- [ ] 故障看起来像“远端网络偶发失败”，但并不是所有连接都失败到底

### 日志特征（最诊断性！）

- [ ] 栈里同时出现 `com.baidu.bjf.remoting.protobuf`、`JdkCompiler.doCompile`、`ProtobufProxy.create`
- [ ] 业务栈里同时出现 `NettyUtil.encode(...)`
- [ ] `channelInactive -> reconnect -> connect` 调用链频繁出现
- [ ] 在 `connect()` 失败/关闭附近，能看到多次重复 `Connect to <host>,<port>`
- [ ] 同一个进程里既有 `RejectedExecutionException`，后面又有成功登录日志

### 代码特征

- [ ] 编码工具方法里每次都直接调用 `ProtobufProxy.create(cls)`，没有 `Codec` 缓存
- [ ] 同一个 `NettyClient` 可能被多个线程同时调用 `connect()`
- [ ] `channelInactive` 会直接触发重连
- [ ] 登录成功后会 `scheduleAtFixedRate(...)` 发心跳，但旧任务没有显式取消
- [ ] 测试桩/模拟器存在多个线程持续高频发送不同 protobuf 消息

### 关键日志指纹

```text
WARN  ... AbstractChannel - Force-closing a channel whose registration task
was not accepted by an event loop
java.util.concurrent.RejectedExecutionException: event executor terminated

ERROR ... rejectedExecution - Failed to submit a listener notification task.
Event loop shut down?
java.util.concurrent.RejectedExecutionException: event executor terminated

An exception has occurred in the compiler (17.0.12)
java.lang.OutOfMemoryError: Java heap space

java.lang.IllegalStateException: Compilation failed. class:
com.xxx.$$JProtoBufClass, diagnostics: []
    at com.baidu.bjf.remoting.protobuf.utils.compiler.JdkCompiler.doCompile(...)

INFO  ... NettyClient - Connect to <host>,<port>
INFO  ... NettyProxyClientHandler - result login ...
```

### 反向排除项

- 如果 JVM **直接退出**、进程被重启、容器有 OOMKilled 记录 → 不是本案例，是“进程级 OOM”
- 如果只有 `event executor terminated`，**没有任何** `JdkCompiler` / `ProtobufProxy` / `Java heap space` 痕迹 → 先排查网络、显式 shutdown、线程池生命周期
- 如果从头到尾都**无法重新登录** → 更像远端服务不可用或网络彻底中断，不是本案例
- 如果只在单次启动初始化阶段出现一次编译慢、之后完全稳定 → 只是冷启动开销，不一定是本案例

---

## 详细说明 / 根因链路

### 四层因素拆解

| 层 | 内容 | 单独看是否必然出 bug |
|---|---|---|
| **编码层** | `NettyUtil.encode()` 每次都调用 `ProtobufProxy.create(cls).encode(t)`，触发 JProtobuf 动态生成/编译 `$$JProtoBufClass` | 有风险，但不一定立刻出 bug |
| **消息模型层** | 某些消息类字段很多、嵌套深，首次动态编译成本高，内存峰值明显 | 有风险，但需要压力触发 |
| **连接层** | `getClient()`、`channelInactive()`、失败回调都可能继续 `connect()`，缺少单飞保护 | 会放大故障 |
| **调度层** | 登录成功后定时发心跳，重连多次成功时可能累计出多个心跳任务 | 会持续制造额外流量和编码压力 |

### 典型故障流程

```text
测试线程持续发消息
    │
    ├─► 反复调用 NettyUtil.encode(...)
    │      └─► ProtobufProxy.create(...)
    │             └─► JdkCompiler.doCompile(...)
    │
    ├─► 某个重消息/首编译时瞬时堆占用过高
    │      └─► Java heap space
    │
    ├─► 编译失败后，部分发送/连接回调继续执行
    │      └─► connect() / addListener() / register() 仍在尝试提交任务
    │
    ├─► 原 event loop 已不可用
    │      └─► RejectedExecutionException: event executor terminated
    │
    ├─► 但 JVM 没死，后续：
    │      1. 某些发送线程异常退出或节奏放缓
    │      2. GC 回收了一部分堆
    │      3. 新连接重新建立
    │
    └─► 日志上表现为：没重启，却“自己恢复”
```

### 为什么“节点没重启却自己好了”

这是本案例最容易让人误判的点：

1. **OOM 不等于 JVM 立刻退出**  
   本次 `OutOfMemoryError` 发生在 `JdkCompiler.doCompile(...)` 业务线程里，很多情况下只会让当前线程/当前任务失败，不会马上让整个进程退出。

2. **坏掉的是当时那个 eventLoop / channel，不是整个节点**  
   `event executor terminated` 说明那次连接依赖的事件循环不能再接任务了，不代表后续不能新建别的连接。

3. **压力是瞬时的，不一定持续**  
   某些消息类型第一次动态编译最贵；一旦高峰过去、GC 生效、部分线程停止，进程可能恢复到“还能继续跑”的状态。

4. **代码会不断尝试重连**  
   只要远端服务实际上可用，后面某次重连总可能成功，于是日志里会同时出现“刚才炸过”和“现在又登录成功”。

### 代码级证据链（当前项目）

#### 1. 每次编码都动态创建 protobuf codec

`cuavcloudcbb/CuavCloudBasicCBB/BasicToolsAdapterCBB/src/main/java/com/cuav/basictools/util/NettyUtil.java`

- `encode(Class<T> cls, T t)` 直接 `return ProtobufProxy.create(cls).encode(t);`
- 没有 `ConcurrentHashMap<Class<?>, Codec<?>>` 之类的缓存层

#### 2. 连接入口缺少并发保护

`cuavcloudservice/CuavCloudApplyService/CuavCloudTestService/src/main/java/com/cuav/cloud/test/application/netty/NettyInstantService.java`

- `getClient()` 在 `!client.getConnectStatus()` 时直接 `client.connect()`
- 多个业务线程同时发现“未连接”时，可能并发触发 connect

`cuavcloudcbb/CuavCloudBasicCBB/BasicToolsAdapterCBB/src/main/java/com/cuav/basictools/config/netty/heart/NettyClientHeartHandler.java`

- `channelInactive()` 里直接 `this.clientReconnect.reconnect()`

`cuavcloudcbb/CuavCloudBasicCBB/BasicToolsAdapterCBB/src/main/java/com/cuav/basictools/config/netty/client/NettyClient.java`

- `connect()` 没有 `synchronized` / CAS / inFlight 标记
- 失败回调里还会 `eventLoop.schedule(() -> connect(), 40, TimeUnit.SECONDS)`

#### 3. 心跳调度会在每次成功登录后继续注册

`cuavcloudcbb/CuavCloudBasicCBB/BasicToolsAdapterCBB/src/main/java/com/cuav/basictools/config/netty/client/NettyProxyClientHandler.java`

- 登录成功后 `scheduleAtFixedRate(...)` 发心跳
- 没看到旧 `ScheduledFuture` 的保存和取消
- 如果多次重连成功，容易积累多个心跳任务

#### 4. 测试桩存在多线程高频报文

`cuavcloudservice/CuavCloudApplyService/CuavCloudTestService/src/main/java/com/cuav/cloud/test/application/sfl210/Sfl210TestService.java`

- `threadHeart`、`threadChildeHeart`、`threadUav` 三条线程持续发不同消息
- `sendDph120Heart(...)` 还会继续串发 posture / beam config

`cuavcloudservice/CuavCloudApplyService/CuavCloudTestService/src/main/java/com/cuav/cloud/test/application/groundstation/GroundStationRadarTestService.java`

- 心跳线程循环里连续发 `RadarHeart`、`RadarPosture`、`RadarBeamConfig`、`RadarUav`

---

## 排查方法论

### 使用到的核心技术

- **时间线对齐**：把 OOM、Netty 重连、登录成功日志放到同一秒级时间线看先后关系
- **堆内存证据收集**：GC 日志、堆 dump、容器内存曲线
- **连接风暴识别**：统计同一分钟内 `Connect to ...` 和 `result login` 的次数
- **热点消息定位**：找是哪一种 protobuf 消息的首次编码最容易触发编译/OOM
- **代码路径审计**：梳理 `getClient -> connect -> channelInactive -> reconnect -> scheduleAtFixedRate` 的闭环

### 诊断步骤（按顺序）

#### 1. 先确认是不是“自恢复型 OOM”

看故障时间窗内是否满足：

- 先有 `Java heap space`
- 再有 `event executor terminated`
- 后面又有连接/登录成功
- 期间没有进程重启、没有容器重建

如果是，优先按本案例走。

#### 2. 定量化连接风暴

在日志里统计 1 分钟窗口：

- `Connect to <host>,<port>` 出现多少次
- `result login` 出现多少次
- `channelInactive` / `close ...remoteAddress` 出现多少次

如果异常窗口里这些数字明显飙升，说明不是单次断线，而是“重连放大”。

#### 3. 锁定最重的 protobuf 类型

搜这些关键词：

- `Compilation failed. class:`
- `$$JProtoBufClass`
- `NettyUtil.encode(`

看 OOM 前最后一个失败的消息类型是谁。  
如果总是集中在字段很多、嵌套复杂的消息模型上，强烈支持本案例。

#### 4. 看进程是否真的没死

验证：

- 容器/进程 uptime 没变化
- 没有 OOMKilled / restart count 增长
- 线程 dump 或日志里还能看到老线程继续工作

这一步能把“进程级 OOM”与“线程级/业务级 OOM”区分开。

#### 5. 审计 connect 入口是否可重入

重点检查：

- `getClient()` 是否可能被多个线程并发调用
- `channelInactive()` 是否直接 reconnect
- 失败 listener 是否延迟再次 connect
- 这些入口之间有没有“只允许一个 connect in flight”的保护

#### 6. 审计心跳任务生命周期

重点检查：

- 登录成功后是否每次都 `scheduleAtFixedRate`
- 旧 channel 关闭时是否取消旧心跳任务
- 是否存在“连接虽然换了，旧任务还在往旧 ctx/channel 发包”

---

## 修复方案

### 根治（P0，必做）

1. **为 `ProtobufProxy.create(...)` 增加 codec 缓存**  
   避免每次 encode/decode 都走动态编译。

2. **给 `NettyClient.connect()` 增加单飞保护**  
   任意时刻只允许一个连接建立流程在飞，避免多个线程同时 connect。

3. **心跳任务绑定连接生命周期**  
   登录成功后保存 `ScheduledFuture`；连接关闭/重连前先取消旧任务，再注册新任务。

### 兜底 / 防御（P1，推荐）

1. **对高风险消息做预热**  
   应用启动或测试启动前，主动对重消息模型调用一次 codec 初始化，避免首次真实发送时冷编译。

2. **在 OOM 后快速熔断发送**  
   某段时间内如果连续出现 `Compilation failed` / `Java heap space`，暂停发送新报文，避免继续放大。

3. **重连退避**  
   加指数退避、最大重试间隔和去抖，防止断链时把 event loop 和堆一起打满。

### 加固 / 清理（P2，长期）

- 把测试桩里所有 `while + sleep + getClient().send(...)` 的发包线程统一纳入调度器，避免裸线程失控
- 对“字段很多、嵌套重”的 protobuf 消息建立专门的预编译清单
- 为 Netty 连接管理增加观测指标：当前连接状态、重连次数、活跃心跳任务数、最近一次 OOM 时间
- 把 `connectStatus` 从“是否登录成功”拆成“连接中 / 已连接 / 已登录 / 已关闭”等更细粒度状态

---

## 预防清单（Checklist）

开发阶段：

- [ ] 凡是 `ProtobufProxy.create(...)` 高频调用点，都评估过是否需要缓存
- [ ] 首次发送成本高的消息类型，已经做过启动预热
- [ ] `connect()` 有并发保护，不会被多个线程同时打穿
- [ ] 定时任务与 channel 生命周期绑定，旧任务能被取消
- [ ] 裸线程循环发送前，评估过异常退出和背压策略

部署阶段：

- [ ] JVM `-Xms/-Xmx` 与压测峰值匹配，不靠默认堆大小裸跑
- [ ] 有 GC 日志、堆内存曲线和重启次数监控
- [ ] 能区分“进程重启恢复”与“进程未重启自恢复”

Review 阶段：

- [ ] 看到“偶发 Netty 断线”时，是否反查了同时间窗有没有 OOM/GC 异常
- [ ] 看到“自动恢复”时，是否警惕这是瞬时资源耗尽而非网络抖动
- [ ] 看到 `scheduleAtFixedRate` 时，是否检查了取消逻辑

---

## 同类间歇性 bug 的 Playbook

遇到“Netty 偶发断线但又自己恢复”的现象时，按此顺序走：

1. 定时间线（10 分钟）  
   把 `OOM`、`RejectedExecutionException`、`Connect to ...`、`result login` 对齐。

2. 看进程是否重启（5 分钟）  
   没重启却恢复，优先怀疑本案例这种“瞬时资源耗尽”。

3. 查堆和 GC（15 分钟）  
   看故障前后堆使用率、Full GC、停顿时间。

4. 统计重连和登录次数（15 分钟）  
   判断是不是连接风暴。

5. 查动态编译热点（20 分钟）  
   grep `$$JProtoBufClass` / `JdkCompiler.doCompile` / `Compilation failed`。

6. 审计连接闭环代码（30 分钟）  
   把所有 `connect` 入口、失败回调、`channelInactive`、定时任务注册点画成图。

7. 先做最小修复验证（1 小时）  
   优先试 `codec 缓存 + connect 单飞 + 取消旧心跳`，再看故障是否消失。

---

## 参考资料

### 本案例相关文件路径（项目：`d:\SpotterProNew\IdeaProjects`）

- 编码入口：`cuavcloudcbb/CuavCloudBasicCBB/BasicToolsAdapterCBB/src/main/java/com/cuav/basictools/util/NettyUtil.java`
- Netty 客户端：`cuavcloudcbb/CuavCloudBasicCBB/BasicToolsAdapterCBB/src/main/java/com/cuav/basictools/config/netty/client/NettyClient.java`
- 重连桥接：`cuavcloudcbb/CuavCloudBasicCBB/BasicToolsAdapterCBB/src/main/java/com/cuav/basictools/config/netty/client/NettyClientReconnect.java`
- 心跳/断链重连：`cuavcloudcbb/CuavCloudBasicCBB/BasicToolsAdapterCBB/src/main/java/com/cuav/basictools/config/netty/heart/NettyClientHeartHandler.java`
- 登录后心跳调度：`cuavcloudcbb/CuavCloudBasicCBB/BasicToolsAdapterCBB/src/main/java/com/cuav/basictools/config/netty/client/NettyProxyClientHandler.java`
- 测试桩连接入口：`cuavcloudservice/CuavCloudApplyService/CuavCloudTestService/src/main/java/com/cuav/cloud/test/application/netty/NettyInstantService.java`
- 高压发送样例 1：`cuavcloudservice/CuavCloudApplyService/CuavCloudTestService/src/main/java/com/cuav/cloud/test/application/sfl210/Sfl210TestService.java`
- 高压发送样例 2：`cuavcloudservice/CuavCloudApplyService/CuavCloudTestService/src/main/java/com/cuav/cloud/test/application/groundstation/GroundStationRadarTestService.java`
- 重消息示例：`cuavcloudcbb/CuavCloudBasicCBB/InterfaceDefineCBB/src/main/java/com/cuav/cloud/protobuf/model/Dph120HeartList.java`

### 关键概念

- JProtobuf / `ProtobufProxy` 动态生成 `$$JProtoBufClass`
- `JdkCompiler.doCompile(...)` 的运行时编译开销
- Netty `EventLoop` 生命周期
- `RejectedExecutionException: event executor terminated`
- 瞬时 OOM 与进程未退出的“假性自恢复”

### 一句话总结

> **当测试桩把“高频动态 protobuf 编译”、“可重入 connect”、“未回收的心跳任务”叠在一起时，进程会先表现为 Netty event loop 终止和连接失败，随后暴露出 `JdkCompiler` 的堆 OOM；因为 JVM 未必退出、重连仍在继续，所以外在现象常常是“节点没重启，过一会儿又自己好了”。**
