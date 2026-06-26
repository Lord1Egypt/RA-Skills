# OpenClaw fallback 日志判读参考

## 目的
用于判断一条请求到底是：

- 成功走了主模型
- 主模型失败后进入 fallback
- 只是打印了 fallback 配置
- 还是日志证据根本不足

这份参考重点补充**日志字段语义与证据强弱等级**。

---

## 证据强弱分级

### A 级：可直接证明发生过候选选择/切换
若日志中存在标准决策字段，证据最强，例如：

- `requested=...`
- `candidate_failed`
- `candidate_succeeded`

典型含义：

- `requested=<模型>`：本次路由目标/初始请求模型
- `candidate_failed ... reason=<原因>`：该候选尝试失败
- `candidate_succeeded ...`：某候选最终成功

如果能串出：

```text
requested=primary-model
candidate_failed ...
candidate_succeeded fallback-model
```

则可较高把握认定：

> 本次确实发生了 fallback 链尝试，并最终命中某候选。

---

### B 级：可证明某 provider/model 被调用过，但不能单独证明 fallback
例如：

- 成功/失败日志中直接带 `provider=local-router`
- `model=gpt-5.4`
- 某次 HTTP 调用明确指向对应 endpoint

这只能证明：

> 该 provider 或模型被请求过。

但**不能单独证明**：

- 它是主模型还是 fallback
- 前面有没有其他候选失败
- 这次调用在整条 fallback 链中处于第几位

---

### C 级：仅能说明配置或调试信息，不能证明本次请求切换
例如：

```text
OpenClaw fallback model: gpt-5.4 via http://localhost:8317/v1
```

这类信息更应先按“**配置值 / 调试打印**”理解，而不是按“本次请求刚刚发生了 fallback”理解。

它通常只能说明：

- 当前存在一个 fallback 模型配置
- 或程序把当前可用 fallback 目标打印出来了

**不能直接推出**：

- 本请求从主模型掉到了 fallback
- 前一个候选一定失败了
- 这次真的完成了候选切换

---

## 为什么“有 fallback model 日志”不等于“发生了 fallback”
这是最容易误判的点。

很多系统会在以下场景打印类似语句：

1. 启动时加载配置
2. 每轮请求前打印默认候选
3. debug 模式下打印当前路由表
4. 组装客户端时打印 endpoint 与 model

因此下面两件事必须分开：

- **打印了 fallback 配置**
- **真的执行了 fallback 决策**

只有看到 `candidate_failed` / `candidate_succeeded` 一类更接近决策链的字段，才更接近“真的发生过”。

---

## 推荐判读顺序

### 1. 先找主请求标识
优先搜索：

```bash
rg -n "requested=local-router/gpt-5.4" <log-path>
```

若完全没有，说明标准化决策日志可能未开启或未记录完整。

### 2. 再找失败候选

```bash
rg -n "candidate_failed.*local-router/gpt-5.4|candidate_failed" <log-path>
```

关注字段：

- `reason=rate_limit`
- `reason=timeout`
- `reason=5xx`
- `reason=EOF`

### 3. 再找成功候选

```bash
rg -n "candidate_succeeded.*local-router/gpt-5.4|candidate_succeeded" <log-path>
```

如果成功候选不是 primary，而是链中其他模型，fallback 证据就更强。

### 4. 单独检查 provider/model 的成功失败日志
比如：

```bash
rg -n "provider=local-router|model=gpt-5.4|EOF|backend-api/codex/responses" <log-path>
```

这一步用于回答：

- 这个模型是否真的被调用过
- 是否出现明确失败

但不要把这一步直接当成 fallback 证据。

---

## 常见结论模板

### 情况 1：存在明确失败记录
如果看到类似：

- `isError=true`
- `model=gpt-5.4`
- `provider=local-router`
- `error=500 ... EOF`

可下结论：

> 至少有一部分请求到 `local-router/gpt-5.4` 并非全部成功。

但若没有候选切换日志，仍只能说：

> 不能仅凭这条错误日志确认后续是否进入了 fallback 并成功。

---

### 情况 2：没有标准 fallback 决策字段
若检索结果类似：

- `requested=local-router/gpt-5.4` → 0 条
- `candidate_failed requested=local-router/gpt-5.4` → 0 条
- `candidate_succeeded requested=local-router/gpt-5.4` → 0 条

则合理结论是：

> 当前日志中缺少足以证明 fallback 决策过程的标准化证据，不能断言“绝对没有 fallback”，也不能断言“明确发生过 fallback”。

这是“**证据不足**”，不是“**事件未发生**”。

---

### 情况 3：只看到 `fallback model: ... via ...`
则应写成：

> 这更像 fallback 配置或调试打印，不能单独作为本次请求已进入 fallback 链的证据。

---

## 推荐输出措辞
为了避免过度断言，建议使用以下措辞：

### 当能证明失败但不能证明是否切换成功
> 已发现 `local-router/gpt-5.4` 的明确失败记录，因此“所有请求都成功”这一命题不成立；但当前日志缺少完整候选决策字段，无法据此确认失败后是否进入并完成了 fallback。

### 当只能证明 provider 被调用
> 可以确认请求打到了 `local-router` provider，但不能仅凭当前字段判断该次调用在主链还是 fallback 链中。

### 当只有 fallback 配置打印
> 日志显示了 fallback 模型配置，但这不足以证明本次请求实际发生了 fallback 切换。

---

## 一句话原则

> **先区分“调用过某模型”与“发生过 fallback”，再区分“有配置打印”与“有决策证据”。**

这是判读 OpenClaw 路由日志时最重要的防误判原则。