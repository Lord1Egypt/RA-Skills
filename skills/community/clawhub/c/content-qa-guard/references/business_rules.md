# 内容合规审核守卫 — 业务规则参考

> 本文档从 SKILL.md 提取业务规则，所有规则标注来源章节，禁止凭记忆改写。

---

## 一、三级审核流程

内容审核采用三级递进审核机制，逐层过滤风险内容。（来源: SKILL.md§工作流 步骤1-6）

### 一级审核：敏感词库扫描（来源: 02手册§八8.3, SKILL.md§工作流 步骤2）
- 调用 sensitive-word-mcp `check_sensitive_words(text, platform, context)`
- 白名单自动豁免机制（详见第四节）
- 词库过期检查（详见第五节）

### 二级审核：AI语义级检测（来源: 02手册§八8.2, SKILL.md§工作流 步骤3）
- 严格度≥3时：调用LLM语义分析(9Router优先+SiliconFlow降级)
- 严格度≥4时：额外调用 `check_fortune_words` 执行算命合规检测
- 严格度≤2：跳过LLM语义分析

### 三级审核：平台规则合规检查（来源: 02手册§八8.1, SKILL.md§工作流 步骤4）
- 对照 PLATFORM_RULES 检查平台特有规则
- 闲鱼：禁止导流/虚假宣传/虚拟商品违禁/金融风险/侵权
- 小红书：严格禁止导流和营销/种草套路词/医疗美容/减肥瘦身/代购违规
- 抖音：禁止导流/直播间特有违规/短视频引流词/金融风险/低俗
- 微博：禁止导流和营销/热搜操控/政治敏感/虚假宣传

---

## 二、平台严格度分级

不同平台适用不同审核严格度，决定是否启用二级LLM审核。（来源: 02手册§八8.2, SKILL.md§工作流 步骤3）

| 严格度等级 | 平台 | 审核行为 |
|:-----------|:-----|:---------|
| **5星** | 小红书、微信公众号 | 启用全量审核(敏感词+LLM语义+算命合规+平台规则) |
| **4星** | 抖音、闲鱼、快手、知乎、视频号 | 启用LLM语义+算命合规+平台规则 |
| **3星** | B站、微博、百家号、头条 | 启用LLM语义(无算命合规)+平台规则 |
| **2星** | CSDN | 跳过LLM语义分析，仅敏感词+平台规则 |

---

## 三、每日审核限额

每日审核次数限制。（来源: 01手册§十10.1, SKILL.md§工作流 步骤5）

- 每日限额：**50条**
- 超出限额返回 blocked，错误码 DAILY_LIMIT_EXCEEDED

---

## 四、白名单豁免规则

以下内容自动豁免敏感词检测，允许通过。（来源: 02手册§八8.3, SKILL.md§工作流 步骤2）

### 1. AI前缀豁免
- "AI代写"
- "AI代做"
- "AI代答"

### 2. AI展示声明豁免
- "AI全自动"
- "AI辅助"

### 3. 发货上下文豁免
- context="delivery" 时，导流词允许（发货场景需要提供联系方式）

---

## 五、词库过期规则

敏感词库需要定期更新，过期会影响审核策略。（来源: 02手册§八8.3, SKILL.md§工作流 步骤2）

| 过期时长 | 处理方式 | 错误码 |
|:---------|:---------|:-------|
| ≥14天 | 直接拦截(blocked) | LIBRARY_EXPIRED_BLOCKED |
| ≥7天 | 继续审核但标记warning | LIBRARY_WARNING |

---

## 六、U19管道合规检查步骤

管道步骤"合规风控(U19)"由 check_compliance.py 执行，委托 risk-detector 进行10类风险检测。（来源: SKILL.md§U19管道合规检查）

### 执行流程
1. 接收管道步骤参数(content, platform)
   - 执行：`python scripts/check_compliance.py --content "<content>" --platform "<platform>"`
   - 检查点：参数非空验证
2. 委托risk-detector执行合规检测
   - 执行：调用risk-detector的check_content action
   - 检查点：risk-detector返回有效结果
3. 返回合规检查结果
   - 输出：JSON {success, data: {risk_level, score, passed, block, details}, error, code}
   - CRITICAL级别返回block=True阻断管道执行
   - risk-detector不可用时降级为基础模式检查(标注downgraded=True)

---

## 七、审核结果与风险等级

### 审核结果（来源: SKILL.md§工作流 步骤5）
- pass：通过
- warning：警告（可发布但需关注）
- blocked：拦截（不可发布）

### 风险等级（来源: SKILL.md§工作流 步骤5）
- SAFE：安全
- LOW：低风险
- MEDIUM：中风险
- HIGH：高风险
- CRITICAL：严重风险

---

## 八、发布后端到端验证（可选）

审核通过后的可选验证步骤。（来源: SKILL.md§工作流 步骤6）

- pass/warning时：调用 xianyu-agent-mcp send_message 发测试消息
- chat_id：QA_TEST_CHAT_ID 环境变量
- 失败→降级为warning，记录 data/qa_verification_log/

---

## 九、参数验证规则

接收审核请求时的验证要求。（来源: SKILL.md§工作流 步骤1）

| 参数 | 类型 | 必填 | 验证规则 |
|:-----|:-----|:----:|:---------|
| text | string | 是 | 非空，text为空返回INVALID_INPUT |
| platform | string | 是 | 有效值: xianyu/xiaohongshu/douyin/bilibili/weibo/default，无效返回INVALID_PLATFORM |
| context | string | 否 | 上下文信息，如"delivery"触发发货豁免 |
