# 内容合规审核守卫 — 示例参考

> 本文档示例从 SKILL.md 提取并扩展，所有示例基于实际工作流场景。

---

## 示例1: 闲鱼商品文案审核（拦截+修改建议）

**场景**: 闲鱼商品文案包含导流词"微信"，触发三级审核拦截，并生成修改建议。

**输入**: （来源: SKILL.md§示例 示例1）
```json
{
  "text": "AI代写文案，加微信xxx获取",
  "platform": "xianyu"
}
```

**预期输出**: （来源: SKILL.md§示例 示例1, SKILL.md§工作流 步骤4）
```json
{
  "success": true,
  "data": {
    "result": "blocked",
    "risk_level": "HIGH",
    "level1": {
      "found": ["微信"],
      "count": 1,
      "library_status": "ok"
    },
    "level2": {
      "enabled": true,
      "llm_findings": ["导流行为"]
    },
    "level3": {
      "platform_violations": ["闲鱼禁止导流"]
    },
    "suggestion": "AI代写文案，联系客服获取",
    "daily_count": 3,
    "daily_limit": 50
  }
}
```

**审核过程说明**:
- **一级审核(敏感词)**: 检测到"微信"属于导流敏感词，count=1
- **二级审核(AI语义)**: 闲鱼严格度为4星(≥3)，启用LLM语义分析，检测到"导流行为"
- **三级审核(平台规则)**: 闲鱼平台规则禁止导流，记录违规"闲鱼禁止导流"
- **结果**: blocked + HIGH风险，suggestion为自动替换版本（"加微信xxx获取"→"联系客服获取"）
- **来源**: 02手册§八8.1-8.3, SKILL.md§工作流 步骤2-5

---

## 示例2: AI商品白名单豁免（通过）

**场景**: 闲鱼商品文案包含"AI代写"前缀，触发白名单自动豁免，审核通过。

**输入**: （来源: SKILL.md§示例 示例2）
```json
{
  "text": "AI代写文案，专业润色",
  "platform": "xianyu"
}
```

**预期输出**: （来源: SKILL.md§示例 示例2, SKILL.md§工作流 步骤2）
```json
{
  "success": true,
  "data": {
    "result": "pass",
    "risk_level": "SAFE",
    "level1": {
      "found": [],
      "count": 0,
      "library_status": "ok"
    },
    "level2": {
      "enabled": true,
      "llm_findings": []
    },
    "level3": {
      "platform_violations": []
    },
    "suggestion": null,
    "daily_count": 4,
    "daily_limit": 50
  }
}
```

**审核过程说明**:
- **一级审核(敏感词)**: "AI代写"命中白名单前缀豁免规则，found为空，count=0
- **二级审核(AI语义)**: 闲鱼严格度为4星(≥3)，启用LLM语义分析，无违规发现
- **三级审核(平台规则)**: 闲鱼平台规则无违规
- **结果**: pass + SAFE风险，无需修改建议
- **白名单豁免规则**: AI前缀("AI代写"/"AI代做"/"AI代答")自动豁免敏感词检测
- **来源**: 02手册§八8.3, SKILL.md§工作流 步骤2

---

## 示例3: U19管道合规检查

**场景**: content-orchestrator 管道执行到"合规风控(U19)"步骤，委托 risk-detector 对内容进行10类风险检测。

**输入**: （来源: SKILL.md§U19管道合规检查, SKILL.md§输入格式 U19管道合规模式）
```json
{
  "content": "本文介绍Python编程入门知识，包含基础语法和项目实战",
  "platform": "juejin",
  "content_type": "article"
}
```

**执行流程**:
1. 接收管道步骤参数(content, platform)
   - 执行: `python scripts/check_compliance.py --content "本文介绍Python编程入门知识..." --platform "juejin"`
   - 检查点: 参数非空验证通过
2. 委托risk-detector执行合规检测
   - 执行: 调用risk-detector的check_content action
   - 检查点: risk-detector返回有效结果
3. 返回合规检查结果

**预期输出**: （来源: SKILL.md§输出格式 U19管道合规模式, SKILL.md§U19管道合规检查）
```json
{
  "success": true,
  "data": {
    "risk_level": "SAFE",
    "score": 95,
    "passed": true,
    "block": false,
    "details": {
      "R01_sensitive_words": "pass",
      "R02_violation_tactics": "pass",
      "overall_compliance": "pass"
    }
  },
  "error": null,
  "code": null
}
```

**异常场景说明**:
- **CRITICAL级别**: risk-detector 检测到严重风险时，返回 block=True 阻断管道执行
- **risk-detector不可用**: 降级为基础模式检查，输出中标注 downgraded=true
- **来源**: SKILL.md§U19管道合规检查

**降级模式输出示例**:
```json
{
  "success": true,
  "data": {
    "risk_level": "LOW",
    "score": 80,
    "passed": true,
    "block": false,
    "downgraded": true,
    "details": {
      "R01_sensitive_words": "pass",
      "R02_violation_tactics": "skip",
      "overall_compliance": "pass(downgraded)"
    }
  },
  "error": "risk-detector不可用，降级为基础模式检查",
  "code": null
}
```
