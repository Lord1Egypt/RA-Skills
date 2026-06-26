# Control Mirror Test Prompts

Use these prompts for Darwin-style evaluation of the skill.

```json
[
  {
    "id": "generic_platform_stability",
    "prompt": "请用工程控制论视角审查一个微服务平台：服务很多、告警很多、重试很多，但故障时经常级联雪崩。",
    "expected": "Must map controller/object/sensor/feedback, identify retry storm or positive feedback, delay/noise, damping/backpressure/circuit breaker, and give P0/P1/P2 actions with verification."
  },
  {
    "id": "agentos_kernel_review",
    "prompt": "请用 control-mirror 审查一个 AgentOS 架构：有执行内核、模型路由、Token压缩、工作流门禁和自动记忆。判断它是不是形成了闭环。",
    "expected": "Must keep engineering cybernetics as main lens, then use AgentOS add-on scorecard, identify feedback-to-policy gaps, memory pollution risk, token damping observability, and maturity level."
  },
  {
    "id": "memory_pollution_loop",
    "prompt": "一个AI系统把所有运行日志都写入长期记忆，后来召回越来越乱、成本越来越高，请用工程控制论分析。",
    "expected": "Must identify noise pollution and positive feedback amplification, propose layered memory, promotion gates, rollback/quarantine, and measurable verification."
  },
  {
    "id": "workflow_oscillation",
    "prompt": "一个自动化工作流经常在计划、执行、审查之间反复循环，输出越来越长但没有真正完成。请诊断。",
    "expected": "Must identify oscillation, weak convergence criteria, missing gates or damping, delayed/noisy feedback, and recommend loop limits/evidence gates/done criteria."
  }
]
```
