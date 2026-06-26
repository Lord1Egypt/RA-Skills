# BUG01: 多副本间歇性 NPE —— 有状态业务 × 无状态部署 × 身份上下文漏传

## 案例摘要

前端携带合法 token 调用某接口，连续请求**约 50% 成功、50% 返回 `errorCode: 10001,服务异常`**。服务端是 k8s 多副本部署（Deployment + round-robin Service），报错副本日志里是 `ChainContextHolder.getTokenPayload()` 返回 null 触发的 NPE（完整堆栈），而同一请求的"入口副本"日志里只有一行业务错误（无堆栈）。

根因是"**应用层有状态路由**（partition owner）"、"**k8s 无状态轮询分发**"、"**内部转发协议漏传 `x-token-payload` header**"三层因素交叉导致的间歇性故障。**任何单层修复都无法根治，但改对一层协议就能完全解决**。

---

## 症状 / 特征速查（用于匹配）

> 下列特征命中 **4 条及以上** 时，高概率是本案例；命中 **2-3 条** 也值得优先按本案例思路排查。

### 客户端现象

- [ ] 同一 token、同一 body，连续请求 N 次，成功率**约等于 `1/副本数`** 或 `(N-1)/N`（两副本时常见 ~50%）
- [ ] 失败时返回业务错误码（如 10001 / INTERNAL_SERVER_ERROR / "服务异常"），不是 401/403/超时
- [ ] 本地单副本环境 **100% 成功**，无法复现
- [ ] 错误提示**像 token 问题**（"未认证 / 身份缺失 / 用户不存在"），但客户端明明带了合法 token

### 服务端日志特征（最诊断性！）

- [ ] 同一个客户端请求，在**多个副本的日志里都有痕迹**（正常应该只在一个副本出现）
- [ ] 不同副本日志**信息不对称**：
  - A 副本：`ERROR` + 完整异常堆栈（NPE / ClassCastException / IllegalState 等底层异常）
  - B 副本：`ERROR` 或 `WARN` + 一行简短业务错误码，**无堆栈**
- [ ] 出现堆栈的副本里，NPE 指向**读取 ThreadLocal / MDC / 上下文存储**的代码（如 `ChainContextHolder.getXxx()`、`RequestContextHolder.getXxx()`、`MDC.get()`）
- [ ] 无堆栈的副本里，有类似 `response XXXX,XXX` 格式的错误日志（来自 RestTemplate / Feign 对内部 HTTP 响应的处理）

### 部署 / 架构特征

- [ ] 目标服务是 **k8s Deployment** 多副本（不是 StatefulSet）
- [ ] 服务内部使用 **Kafka Consumer Group** / **应用层分区路由** / **内存缓存 + partition 所有权**
- [ ] 代码里存在 `RestTemplate.exchange` / `Feign` 向**本服务的其它 pod IP** 发 HTTP 请求的代码
- [ ] 存在类似 "黄页表"（DB 或 Redis 里记录 `partition → ip:port`）

### 代码特征

- [ ] 接收端 Controller **硬解引用** ThreadLocal/上下文（如 `ChainContextHolder.getTokenPayload().getAccount()`）而未做 null-safe
- [ ] 存在内部调用用的 "feign_token" / "system_token" 字面量占位符（`Authorization: Bearer feign_token` 这类）
- [ ] 内部转发只传 `Authorization`，**没传** `x-token-payload` / `x-user-context` / `x-trace-id` 等身份 header

### 关键日志指纹（可直接 grep）

```text
# A 副本（接收端）典型日志
ERROR ... GlobalExceptionHandler - found system exception,null/<接口路径>
java.lang.NullPointerException: Cannot invoke "XxxPayload.getXxx()" because
    the return value of "XxxContextHolder.getPayload()" is null
    at <Controller>.<method>(<Controller>.java:NNN)

# B 副本（转发端）典型日志
ERROR ... <Service> - <methodName> response <errorCode>,<errorMessage>
（就这一行，后面没有 "at xxx.xxx" 的栈）
```

### 反向排除项

- 如果**单副本也 100% 失败** → 不是本案例，是纯代码 bug
- 如果**所有副本日志都有完整堆栈** → 不是本案例，是单机异常没有跨副本链路
- 如果**token 确实过期了**（日志里有 `token expired` / `invalid signature`）→ 不是本案例
- 如果故障时间段集中在**扩缩容/发版前后几分钟**内 → 可能是 Kafka rebalance 期间的瞬时问题，不是本案例

---

## 详细说明 / 根因链路

### 三层因素拆解

| 层 | 内容 | 单独看是否有问题 |
|---|---|---|
| **代码层** | 某业务接口的 Service 里有 partition 路由逻辑：`MonitorCacheMgr.send(tbCode)` 根据 `hash(tbCode)` 找到 partition owner pod，非 owner 通过内部 HTTP 转发到 owner | 不是 bug（有状态业务的合理设计） |
| **部署层** | k8s Deployment 部署 2+ 副本，Service 用 round-robin 分发外部请求。**副本对两个请求都是 50% 命中率，不考虑业务路由** | 不是 bug（k8s 标准用法） |
| **协议层** | 内部转发只带 `Authorization: Bearer feign_token`（字面量占位符），**没带 `x-token-payload`**。接收端 `AuthInterceptor` 只认 `x-token-payload`，取不到就让 `ChainContextHolder.TokenPayload = null` | **这是真正的 bug** |

### 请求"裂变"流程

前端视角发了 1 次请求，服务端实际处理了 2 次 HTTP 调用：

```text
前端 ──► 请求 #1 ──► k8s Service (round-robin)
                        │
            50%         │         50%
       ┌────────────────┴────────────────┐
       ▼                                 ▼
   Pod A (owner of tbCode)        Pod B (NOT owner)
   ──────────────────              ──────────────────
   1. AuthInterceptor              1. AuthInterceptor
      解析 x-token-payload ✓          解析 x-token-payload ✓
   2. Controller 取 account ✓      2. Controller 取 account ✓
   3. send() 自己是 owner          3. send() 算出 owner 是 Pod A
      → 本地 call()                   → 发起【请求 #2】转发到 Pod A
   4. 业务逻辑执行成功                 │
   5. 返回 ApiResponse(0) ✅           │ ❌ 漏传 x-token-payload
                                       ▼
                                  Pod A 作为接收端:
                                  5. AuthInterceptor 找不到
                                     x-token-payload
                                     → ChainContextHolder = null
                                  6. Controller 硬取 .getAccount()
                                     💥 NPE
                                  7. GlobalExceptionHandler 捕获
                                     → 打印完整 NPE 堆栈（日志 ①）
                                     → 返回 ApiResponse(10001)
                                       ▲
                                       │ HTTP 200 + body{errorCode:10001}
                                       │
                                  Pod B 收到响应:
                                  8. errorCode != 0
                                     log.error("...response 10001,服务异常")
                                     （日志 ②，仅一行、无堆栈）
                                  9. throw ServiceException
                                     → 返回 ApiResponse(10001) 给前端
```

### 为什么"有的成功有的失败"

k8s Service round-robin 每次请求独立决策落到哪个副本，和 token 内容无关：

- 运气好，直接落到 owner pod → 不触发内部转发 → 100% 成功
- 运气不好，落到非 owner pod → 触发内部转发 → 因为漏传 header → NPE → 失败

### 为什么"日志一个有栈一个没栈"

Spring 的 `GlobalExceptionHandler` 分两类处理异常：

| 异常类型 | 语义 | 日志级别 | 打堆栈 |
|---|---|---|---|
| `SystemException` / 未捕获 `Throwable` | 非预期系统异常（NPE、SQL 错等） | `ERROR` | ✅ 完整堆栈 |
| `ServiceException` / 业务异常 | 业务规则违反（预期内错误） | `WARN` 或 `ERROR` | ❌ 不打堆栈 |

- **Pod A**（接收端）：真正发生 NPE → 走 SystemException 路径 → **有栈**
- **Pod B**（转发端）：只是把 `errorCode` 包装成 `ServiceException` 再抛 → 业务异常路径 → **无栈**

### 为什么登录是无状态的，但还是有状态 bug

这是最容易混淆的点：

- **认证层（JWT token）确实无状态** —— 每个 pod 都能独立解析 token
- **业务层严重有状态** —— 因为：
  1. Kafka Consumer Group 协议规定：一个 partition 只能被 group 里一个 consumer 消费 → pod 和 partition 强绑定
  2. 高频设备数据必须在内存聚合（每秒几千上万条，写 Redis 扛不住）
  3. 聚合数据只在消费该 partition 的 pod 内存里有 → 查询必须路由到拥有者

所以项目不得不在"无状态 k8s 部署"之上**手搓一套应用层路由**（分区黄页表 + pod 间 HTTP 转发），而这个转发协议就是 bug 的温床。

---

## 排查方法论

### 使用到的核心技术

| 技术 | 用途 | 何时用 |
|---|---|---|
| **边界测试定量化** | 连续 100 次请求统计成功率，判断是确定 bug 还是间歇性 bug | 第一步必做 |
| **副本数比对** | 成功率 vs `1/N` 关系，快速指向副本间行为不一致 | 看到间歇性立即用 |
| **跨副本日志对照** | 把同一 traceId / 时间窗口在所有副本的日志拉出来**并排看** | 怀疑内部调用链路时 |
| **源码 vs 部署字节码比对** | `javap -c -p` 反编译部署 jar，diff 本地源码 | 怀疑部署了错误版本 |
| **画身份传播生命周期图** | 标出所有跨线程/进程/实例的边界，审计每个边界是否有补偿 | 怀疑上下文丢失 |
| **Header 抓包验证** | `tcpdump` / 接收端入口打印 `getHeaderNames()` | 怀疑 header 传递不对时 |
| **同类代码对比** | 项目里做同样事没出 bug 的代码 → diff 出差异 | 有多个相似实现时 |

### 诊断步骤（按顺序）

#### 1. 定量化现象（10 分钟）

```bash
# 连续打 100 次同一请求（替换 URL 和 token）
for i in $(seq 1 100); do
  curl -s -X POST "$URL" -H "Authorization: $TOKEN" -d "$BODY" \
    | jq -r '.errorCode' | head -1
done | sort | uniq -c
```

看成功率：
- 100% / 0% → 不是本案例，走其它排查路径
- **约 50%（2 副本）/ 约 33%（3 副本）/ ... → 强烈指向本案例**

#### 2. 确认副本拓扑（5 分钟）

```bash
kubectl get deploy <service-name> -o json | jq '.spec.replicas'
kubectl get pods -l app=<service-name>
```

- 副本数 > 1 且 Service 类型是普通 ClusterIP/LoadBalancer → 命中"多副本 round-robin"条件

#### 3. 跨副本日志对照（30 分钟）

```bash
# 对每个副本并行 tail 日志，加入副本名前缀方便区分
for pod in $(kubectl get pods -l app=<service> -o name); do
  kubectl logs -f "$pod" --tail=100 | sed "s/^/[$pod] /" &
done
wait
```

发起 1 次失败请求，观察：
- 是否**同时**在多个副本出现日志？
- 不同副本日志的**格式/详尽程度是否不对称**？

如果有以上特征 → 基本可以确认是本案例类型。

#### 4. 代码定位（30 分钟）

- 找到有堆栈的那个副本日志里指向的代码行（NPE 所在行）
- 找到无堆栈副本里 `log.error("...response XXX,XXX")` 的调用位置
- 看这段调用对应的 `restTemplate.exchange` / `Feign` 方法
- 检查 URL 是否形如 `http://<动态 IP>:<port>/...`（pod 间直连）
- 检查 Headers 是否缺失 `x-token-payload` / `x-user-context` 等身份 header

#### 5. 确认协议不一致（15 分钟）

- 抓 Gateway 经过的请求的完整 header 列表
- 抓内部转发时添加的 header 列表
- Diff 两者，找出缺失项
- 再看接收端 `AuthInterceptor` / `@PreAuthorize` / 上下文解析代码，确认依赖哪些 header

**Diff 差集就是要修复的 header 清单**。

---

## 修复方案

### 根治（P0，必做）

**在内部转发的出站 HTTP 代码里，补齐身份上下文 header**。参考实现：

```java
private Integer invokeRemoteDeviceOpt(JsonNode node, NodePartition nodePartition, RestTemplate restTemplate) {
    String newUrl = String.format("http://%s:%s/rest/v1/access/device/product/services",
            nodePartition.getIp(), nodePartition.getPort());
    HttpHeaders headers = new HttpHeaders();
    headers.add("Authorization", RequestHeaderConstant.HTTP_FEIGN_TOKEN_BEARER.getValue());
    headers.add("Content-Type", "application/json");
    headers.add("Accept", "application/json");

    // 核心修复：透传身份上下文
    TokenPayload tokenPayload = ChainContextHolder.getTokenPayload();
    if (tokenPayload != null) {
        TokenContext tokenContext = TokenContext.builder().payload(tokenPayload).build();
        headers.add(RequestHeaderConstant.HTTP_TOKEN_PAYLOAD_HEADER.getValue(),
                JSONUtil.INSTANCE.toJson(tokenContext));
    } else {
        log.warn("invokeRemoteDeviceOpt missing TokenPayload, forward to {} without x-token-payload", newUrl);
    }
    ChainContext ctx = ChainContextHolder.get();
    if (ctx != null) {
        if (StringUtils.isNotBlank(ctx.getRemoteIp())) {
            headers.add(RequestHeaderConstant.HTTP_REMOTE_IP_HEADER.getValue(), ctx.getRemoteIp());
        }
        if (StringUtils.isNotBlank(ctx.getLocale())) {
            headers.add(RequestHeaderConstant.HTTP_LANGUAGE.getValue(), ctx.getLocale());
        }
    }
    // ... 后面 restTemplate.exchange 调用保持原样
}
```

**关键**：序列化方法必须和 Gateway 入口一致（例如都用 `JSONUtil.INSTANCE.toJson(TokenContext)`），否则接收端反序列化会失败。

### 兜底（P1，推荐）

**接收端 Controller 的 ThreadLocal 硬解引用加 null-safe**：

```java
@PostMapping(value = "/rest/v1/access/device/product/services")
public ApiResponse<Integer> innerDeviceOptRequest(@RequestBody JsonNode jsonNode) {
    String tbCode = ChainContextHolder.getTbCode();
    TokenPayload payload = ChainContextHolder.getTokenPayload();
    String account = payload != null ? payload.getAccount() : null;
    String tid = payload != null ? payload.getTid() : null;
    // ...
}
```

防御意义：万一未来有新增调用方又漏传 header，不会直接崩，最坏是降级到 account=null。

### 加固（P2，长期）

- **抽公共工具方法** `forwardHeadersBuilder()`：统一"内部 HTTP 转发"的 header 组装，下次写类似代码不会再漏
- **清理死代码**：检查项目里是否有"意图处理内部调用但逻辑写错"的死代码（如 `url.startsWith("/inner/") && url.equals("feign_token")` 这种永远为 false 的条件）
- **新 `/inner/...` 专用路径**：长期看，让外部 API 和内部转发走**不同 URL 前缀**，接收端显式从 body 拿身份而不是依赖 header。参考已有的 `/inner/rest/...` 设计模式

---

## 预防清单（Checklist）

### 写"出站 HTTP 调用"时

- [ ] 这个调用**跨了网络边界**吗？（即使是同服务 pod 之间也算）
- [ ] 接收端是否依赖 `ThreadLocal` / `MDC` / 上下文存储？
- [ ] 我是否显式透传了身份 header（`x-token-payload` / `x-user-context`）、traceId、MDC？
- [ ] Header 组合是否和 **服务入口处**（Gateway / AuthFilter）注入的完全一致？
- [ ] 上下文为 null 时，降级策略清晰（log.warn + 继续 / 直接抛）

### 写"入站 Controller"时

- [ ] 本接口会被哪些调用方访问？外部？其它服务？自己的 pod？
- [ ] 所有调用方都能保证提供我依赖的 header 吗？
- [ ] 硬取 `ContextHolder.getXxx().getYyy()` 前，确认最坏情况下不会 NPE
- [ ] 或优先改用**显式参数** + `@Validated`，彻底避免依赖 ThreadLocal

### Review 有状态服务时

- [ ] 应用里有没有"会话状态 / partition 所有权 / 内存缓存"等隐性状态？
- [ ] 部署用 Deployment 还是 StatefulSet？匹配业务语义吗？
- [ ] 内部路由逻辑是否完整传播了所有必需的上下文？
- [ ] 能不能在**多副本环境**下，通过相同业务 key 连续请求 100 次测出故障？

### 部署阶段

- [ ] source 版本和 deployed 版本可校验？（镜像 tag、git commit hash）
- [ ] 灰度发布时有 canary pod 先跑？
- [ ] 有状态服务升级做过跨版本内部调用兼容测试？

---

## 同类间歇性 Bug 的 Playbook

遇到"偶发 NPE / 偶发 500 / 偶发 403"的模糊投诉时，按此顺序走：

### Step 1：定量复现（10 分钟）

连续 N 次请求，算成功率：
- 100% / 0% → 跳到 Step 5（稳定 bug 排查）
- 其它比例 → 继续

### Step 2：查副本数（5 分钟）

`kubectl get deploy` 看副本数。
- 成功率 ≈ `1/N` 或 `(N-1)/N`？ → 副本间行为不一致
- 单副本能否复现？不能 → **强烈指向本案例类型**

### Step 3：跨副本日志对照（30 分钟）

- 发 1 次失败请求，同时 tail 所有副本日志
- 找"同一请求在多副本留痕 + 日志不对称"证据
- 找出"有堆栈副本 + 无堆栈副本"各自的代码位置

### Step 4：源码 vs 部署比对（15 分钟）

- 抓一个线上 pod 的 jar 反编译关键类
- diff 本地源码
- 任何差异都是重大线索（先怀疑部署错了版本）

### Step 5：画上下文传播链（30 分钟）

- 标出所有跨线程/进程/实例的边界
- 每个边界是否有显式打包 → 解包的机制
- 用抓包 / 入口打印 header 验证实际传递内容

### Step 6：对比同类代码（15 分钟）

- 找 5-10 处做相似事情的代码
- diff 出 bug 代码和正常代码的差异

### Step 7：最小复现 + 固化测试（1 小时）

- 构造"最小副本数 + 最小前置条件"的复现用例
- **固化成集成测试用例**，避免复发

---

## 参考资料

### 本案例相关文件路径（项目：cuavcloudservice）

- 根因修复点：`CuavCloudApplyService/CuavCloudService/.../application/device/DeviceService.java` (`invokeRemoteDeviceOpt`)
- NPE 现场：`CuavCloudApplyService/CuavCloudService/.../api/device/DeviceAccessController.java:313`
- 上下文定义：`cuavcloudcbb/.../context/ChainContextHolder.java`, `ChainContext.java`
- Header 常量：`cuavcloudcbb/.../constant/RequestHeaderConstant.java`
- Gateway 注入点：`cuavcloudservice/.../gateway/filter/AuthorizationFilter.java`（第 133/274/338/345 行）
- 接收端解析：`cuavcloudcbb/.../authentication/application/interceptor/AuthInterceptor.java`
- Partition 路由：`CuavCloudService/.../domain/cache/MonitorCacheMgr.java` (`send`), `domain/merchmant/NodePartitionMgr.java`
- 分区映射表：`t_kafka_partition` (DB) + `access.partition.cache.v4.{id}` (Redis)

### 关键概念

- JWT 无状态认证
- Kafka Consumer Group partition assignment
- k8s Deployment vs StatefulSet
- ThreadLocal 跨网络边界丢失
- `GlobalExceptionHandler` 对 SystemException / ServiceException 的不对称处理

### 一句话总结

> **k8s 无状态部署哲学和应用层有状态业务逻辑冲突时，内部 pod 间 HTTP 转发漏传 `x-token-payload`，副本 round-robin 让这个 bug 变成薛定谔猫；两个 pod 的日志各拿一半证据（接收端有堆栈、转发端只有业务错误码），跨 pod 对照才能还原完整链路。**
