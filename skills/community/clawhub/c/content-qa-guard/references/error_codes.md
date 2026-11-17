# 内容合规审核守卫 — 错误代码参考

> 来源: SKILL.md(content-qa-guard) + 05文档§七

> 本文档从 SKILL.md§异常处理 提取所有错误代码定义，禁止遗漏。

---

## 错误代码总表

| 错误代码 | 异常 | 处理方式 | 来源 |
|:---------|:-----|:---------|:-----|
| INVALID_INPUT | text为空 | 返回success:false | SKILL.md§异常处理 |
| INVALID_PLATFORM | platform无效 | 返回success:false | SKILL.md§异常处理 |
| LIBRARY_EXPIRED_BLOCKED | 词库过期≥14天 | 直接blocked | SKILL.md§异常处理 |
| LIBRARY_WARNING | 词库过期≥7天 | 继续但标记warning | SKILL.md§异常处理 |
| LLM_UNAVAILABLE | LLM调用失败 | 跳过二级审核，降级为warning | SKILL.md§异常处理 |
| DAILY_LIMIT_EXCEEDED | 每日限额超限 | 返回blocked | SKILL.md§异常处理 |
| MCP_TIMEOUT | MCP调用超时 | 返回success:false | SKILL.md§异常处理 |

---

## 错误代码详解

### INVALID_INPUT
- **触发条件**: text 参数为空
- **影响范围**: 流程在工作流步骤1参数验证阶段被拦截
- **处理方式**: 返回 success:false
- **业务影响**: 审核流程未启动，用户需提供待审文本后重新调用
- **来源**: SKILL.md§异常处理, SKILL.md§工作流 步骤1

### INVALID_PLATFORM
- **触发条件**: platform 参数无效，不在有效值列表内
- **有效平台**: xianyu/xiaohongshu/douyin/bilibili/weibo/default
- **影响范围**: 流程在工作流步骤1参数验证阶段被拦截
- **处理方式**: 返回 success:false
- **业务影响**: 审核流程未启动，用户需提供有效平台后重新调用
- **来源**: SKILL.md§异常处理, SKILL.md§工作流 步骤1

### LIBRARY_EXPIRED_BLOCKED
- **触发条件**: 敏感词库过期≥14天
- **影响范围**: 一级审核(敏感词扫描)无法可靠执行
- **处理方式**: 直接返回 blocked，拦截内容发布
- **业务影响**: 所有内容审核被拦截，需立即更新敏感词库
- **来源**: SKILL.md§异常处理, 02手册§八8.3, SKILL.md§工作流 步骤2

### LIBRARY_WARNING
- **触发条件**: 敏感词库过期≥7天但<14天
- **影响范围**: 一级审核(敏感词扫描)仍可执行但结果可靠性下降
- **处理方式**: 继续审核但标记 warning
- **业务影响**: 审核流程继续运行，但需尽快更新敏感词库以保证审核准确性
- **来源**: SKILL.md§异常处理, 02手册§八8.3, SKILL.md§工作流 步骤2

### LLM_UNAVAILABLE
- **触发条件**: LLM 调用失败(9Router和SiliconFlow均不可用)
- **影响范围**: 二级审核(AI语义检测)无法执行
- **处理方式**: 跳过二级审核，降级为 warning
- **业务影响**: 审核严格度下降，仅依靠一级(敏感词)和三级(平台规则)审核，语义级风险可能漏检
- **降级行为**: 严格度≥3的平台(5星/4星/3星)受影响最大，因为原本依赖LLM语义分析
- **来源**: SKILL.md§异常处理, SKILL.md§工作流 步骤3

### DAILY_LIMIT_EXCEEDED
- **触发条件**: 当日审核次数超过50条限额
- **影响范围**: 审核流程被拦截
- **处理方式**: 返回 blocked
- **业务影响**: 当日无法继续审核，需次日重试或申请提升限额
- **限额来源**: 01手册§十10.1 规定每日50条
- **来源**: SKILL.md§异常处理, 01手册§十10.1, SKILL.md§工作流 步骤5

### MCP_TIMEOUT
- **触发条件**: MCP 调用超时(如 sensitive-word-mcp 响应超时)
- **影响范围**: 相关审核步骤无法完成
- **处理方式**: 返回 success:false
- **业务影响**: 审核流程中断，需检查 MCP 服务响应时间和网络状况
- **来源**: SKILL.md§异常处理, SKILL.md§工作流 步骤2
