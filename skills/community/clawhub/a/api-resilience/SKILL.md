---
name: api-resilience
display_name: API 韧性（API Resilience）
display_name_en: "API Resilience"
description: "当用户说『调外部API老超时』『被限流了』『接口抖一动就挂』『怎么给agent加重试退避』，或 agent 依赖的第三方服务(模型/搜索/数据库)不稳定、需要限流/退避/熔断/降级时使用。把外部调用当『会失败的对象』：指数退避+抖动重试、限流计数、熔断降级，失败可恢复不雪崩。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：API重试、限流、退避、熔断、降级、接口抖动、resilience、超时、调用不稳定。"
version: 1.0.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, WebSearch
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - agent 依赖的模型/搜索/数据库接口偶发超时或 429
  - 一次失败就让整条链路崩
  - 想加指数退避/抖动/熔断/降级
  - 用户问「怎么让外部调用更稳」
tags: [API韧性, 重试退避, 限流, 熔断, 降级, resilience, 可靠性, 故障恢复, agent优化]
slug: api-resilience
title: API 韧性（API Resilience）
copyright: SynomosAI
description_zh: "当用户说『调外部API老超时』『被限流了』『接口抖一动就挂』『怎么给agent加重试退避』，或 agent 依赖的第三方服务(模型/搜索/数据库)不稳定、需要限流/退避/熔断/降级时使用。把外部调用当『会失败的对象』：指数退避+抖动重试、限流计数、熔断降级，失败可恢复不雪崩。"
description_en: "Treat external API calls as failure-prone: retry with backoff, rate limiting, circuit breaking and graceful degradation patterns for agents relying on third-party services."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/resilience_demo.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: fail-rate
    type: float
    description: 模拟失败率默认0.5
    required: false
  - name: max-retry
    type: int
    description: 最大重试默认5
    required: false
  - name: breaker
    type: int
    description: 熔断触发连续失败数默认3
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 重试/熔断行为演示结论
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - resilience
  - retry
  - circuit_breaker
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
- Frequent timeouts, 429 TooManyRequests or jittery responses from external deps (model/search/DB).
- Build a "failure-prone object" model for unreliable external services to prevent cascading collapse.
- The user asks "external API keeps timing out" / "how to add retry backoff".
- Complex calls needing exponential backoff, rate limiting, circuit breakers or degradation.

### Usage
- Call the core function in `resilience_demo.py` with `policy='exponential'`, `jitter=True`.
- Configure limiter and max retries: `max_retries=5`, `initial_retry_delay=1000ms`.
- Enable circuit breaker: `enable_circuit_breaker=true`, `failure_rate_threshold=0.8`.
- Load `resilience_demo.py` classes for current backoff algorithm config.

### Flow
1. **Init**: bind request context to the external object (LGD registered).
2. **Verify**: first request; record status code and latency (LGD evidenced).
3. **Judge**: compute backoff from rate-limit/timeout evidence; decide whether to retry.
4. **Retry**: apply exponential backoff + jitter.
5. **Circuit-break**: on consecutive failures, open the breaker; stop further calls.
6. **Recover**: after a cooldown / error reduction, re-validate and auto-close the breaker.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
- 当外部依赖（模型/搜索/数据库）出现频繁超时、返回 RateLimit-TooManyRequests 或响应异常抖动时。
- 当 Agent 需要在不可靠的外部服务上建立"会失败的对象"模型，防止系统雪崩效应时。
- 当用户明确提出『调外部 API 老超时』『怎么给 agent 加重试退避』等请求时。
- 在需要实施指数退避、限流计数或熔断降级策略的复杂调用场景下。

### 用法
- 调用脚本 `resilience_demo.py` 中的核心函数，设置参数 `policy='exponential'`, `jitter=True`。
- 配置限流计数器与最大重试次数，例如 `max_retries=5`, `initial_retry_delay=1000ms`。
- 启用熔断机制开关 `enable_circuit_breaker=true`，并设定失败阈值 `failure_rate_threshold=0.8`。
- 若技能需读取逻辑，直接加载 `resilience_demo.py` 类定义以获取当前退避算法配置。

### 流程
1. **初始化**：识别外部对象属性并绑定请求上下文（LGD 有籍）。
2. **验证**：执行首次请求并记录状态码与耗时，积累失败证据（LGD 有证）。
3. **判断**：基于限流或超时证据计算退避时间，判断是否触发重试。
4. **重试**：应用指数退避 + 抖动公式重新发送请求（LGD 有籍·有证·有门禁）。
5. **熔断**：连续失败达标则激活熔断状态，停止进一步调用以保护主系统。
6. **恢复**：等待熔断半冷却期过或错误减少，验证后可自动解除限制并恢复连接。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
