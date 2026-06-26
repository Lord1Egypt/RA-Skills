---
name: evidence-report
description: RumorChecker 统一报告标准。确保证据链可追溯、多元交叉验证可视化、误解来源可解释，培养用户辨别能力。
---

# RumorChecker 统一报告标准

## 核心原则

1. **这是 Rumor Checker，不是 Rumor Guard** — 辅助核查工具，不替用户判断
2. **报告是"信息核查参考"** — 不是权威判定，最终判断权在用户手里
3. **系统不对结果负责** — 明确免责声明
4. **授人以渔** — 培养用户自主辨别能力，不只给结论

## 最终报告格式（Reporter 使用）

```
══════════════════════════════════
信息核查参考报告
══════════════════════════════════

📌 核查问题：[用户原始问题的精确复述]

⚠️ 免责声明：本报告仅为信息核查参考，基于公开可查信息整理，不构成权威判定。最终判断权在您手中。

━━━ 1. 系统参考意见 ━━━
参考意见：[真实可信 / 存疑待证 / 多处矛盾 / 证据不足]
参考信心度：[XX%]（仅代表系统基于现有证据的倾向，供参考）

━━━ 2. 证据链（每条可追溯）━━━

📎 证据 #1
  内容：[事实摘要，一句话]
  来源：[完整 URL，必须可点击访问]
  来源类型：[官方 / 学术 / 主流媒体 / 社交媒体 / 自媒体]
  发布时间：[YYYY-MM-DD]
  可信度评级：[高 / 中 / 低] — [一句话评级原因]
  验证状态：[✅ 已被多源交叉验证 / ⚠️ 仅单一来源 / ❌ 与其他来源矛盾]
  搜索者：[哪个 agent/worker 找到的]

📎 证据 #2
  ...

[按可信度从高到低排列]

━━━ 3. 多元交叉验证 ━━━

验证矩阵：
  证据 #1 ←→ 证据 #3：✅ 互相印证（核心事实一致，独立来源）
  证据 #1 ←→ 证据 #4：⚠️ 部分矛盾（时间描述存在差异）
  证据 #2 ←→ 证据 #5：❌ 直接矛盾（结论完全相反）

验证方法：
  · 事实核查：[哪些具体事实被多个独立来源证实]
  · 逻辑检验：[推理链条是否自洽，有无跳跃]
  · 时间线验证：[事件的时间线是否合理，有无时间错位]
  · 信息回音室检测：[是否存在多个来源引用同一原始来源的假象]
  · 数据一致性：[引用的数字/统计是否被原始来源证实]

━━━ 4. 误解来源分析 ━━━

这条信息为什么会被误传或误信？

🧠 认知因素：
  · [确认偏误 / 权威效应 / 从众心理 / 恐惧诉求 / ...]
  · [具体解释为什么这个因素在此场景中起作用]

📱 传播因素：
  · [标题党 / 断章取义 / 过时信息翻新 / 数据脱离语境 / ...]
  · [具体解释传播路径]

🔍 信息缺口：
  · [公众缺少哪些背景知识，导致容易被误导]
  · [如果了解了什么信息，就不会轻信]

━━━ 5. 正反分析摘要 ━━━

支持"可信"的论据：
  · [论据 1]（参见证据 #N）
  · [论据 2]（参见证据 #N）

支持"存疑"的论据：
  · [论据 1]（参见证据 #N）
  · [论据 2]（参见证据 #N）

关键争议点（目前无法确定）：
  · [具体描述哪些部分证据不足以做出判断]

━━━ 6. 辨别技巧（供您参考）━━━

针对这类信息，您可以这样自行核实：
  ✅ 查来源：[具体建议，如"检查文章是否引用了原始研究论文"]
  ✅ 交叉验证：[具体建议，如"搜索权威机构的官方声明"]
  ✅ 识别信号：[这类信息的常见特征，如"使用绝对化措辞'肯定致癌'"]
  ✅ 推荐工具：[用户可以自行使用的公开核查工具/网站]

━━━ 7. 参与团队 ━━━

本次核查参与的所有 Agent 和 Worker：
  [emoji] [名称]（[常驻/临时]）— [具体工作内容] — [耗时 N 秒]

══════════════════════════════════
```

## 各 Agent 中间报告格式要求

### Searcher 输出格式

每条搜索结果必须包含：
```json
{
  "id": "evidence-N",
  "content": "事实摘要",
  "source_url": "完整URL（必须可访问）",
  "source_type": "official|academic|mainstream_media|social|self_media",
  "publish_date": "YYYY-MM-DD",
  "credibility": "high|medium|low",
  "credibility_reason": "一句话评级原因",
  "searcher": "哪个agent/worker找到的",
  "initial_misinfo_signal": "如果这条信息与谣言相关，初步分析为什么容易被误传"
}
```

**禁止出现的表述：**
- "研究表明" → 必须写 "根据[具体来源]的研究(URL)"
- "专家认为" → 必须写 "[具体姓名/机构]认为(URL)"
- "据说"/"据传" → 必须写明信息来源或标注"来源不明"

### Verifier 输出格式

```json
{
  "verification_summary": "验证概述",
  "cross_reference_matrix": [
    {"pair": ["evidence-1", "evidence-3"], "relation": "confirm|partial_conflict|conflict", "detail": "具体说明"}
  ],
  "echo_chamber_check": "是否存在信息回音室，具体说明",
  "verification_methods_used": ["事实核查", "逻辑检验", "时间线验证", "数据一致性"],
  "verified_facts": [{"fact": "...", "supporting_evidence": ["evidence-1", "evidence-3"], "confidence": 95}],
  "disputed_facts": [{"fact": "...", "pro_evidence": ["evidence-1"], "con_evidence": ["evidence-5"], "detail": "矛盾具体描述"}],
  "excluded_items": [{"evidence_id": "evidence-2", "reason": "排除原因", "hallucination_signal": "如有"}],
  "overall_reliability": "high|medium|low"
}
```

### Debater 输出格式

注意：Debater 不输出 "verdict: true/false"，而是输出分析摘要。

```json
{
  "mode": "self_debate|ping_pong",
  "topic": "分析主题",
  "pro_arguments": [
    {"point": "论点", "evidence_refs": ["evidence-1"], "strength": "strong|moderate|weak"}
  ],
  "con_arguments": [
    {"point": "论点", "evidence_refs": ["evidence-5"], "strength": "strong|moderate|weak"}
  ],
  "analysis_summary": "正反双方论据力度的综合对比分析",
  "key_uncertainties": ["目前无法确定的具体方面"],
  "reference_confidence": 85,
  "confidence_explanation": "信心度计算依据"
}
```

### Reporter 输出格式

**完全遵循上方"最终报告格式"，逐项填充，不得省略任何 section。**

特别注意：
- 结论用"参考意见"而非"判定"
- 信心度标注"仅供参考"
- 必须包含"辨别技巧"section
- 必须包含"误解来源分析"section
- 必须包含"参与团队"section

## 绝对禁止

- ❌ 使用"我们判定""结论是""官方认定"等权威性表述
- ❌ 省略来源 URL
- ❌ 使用模糊引用（"有研究""专家说"）
- ❌ 在报告中增添上游 agent 未提供的信息
- ❌ 省略交叉验证矩阵
- ❌ 省略误解来源分析
- ❌ 省略辨别技巧
- ❌ 省略参与团队信息
