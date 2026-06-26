# ClawdGo 场景文件格式规范

本文件定义 ClawdGo 训练场景的标准格式。所有场景文件必须严格遵循此规范。

## 文件命名

`{维度ID}-{序号:02d}.md`

- 维度ID：S1-S4（守护自身）、O1-O4（守护主人）、E1-E4（守护组织）
- 序号：两位数字，从 01 开始（按 difficulty 字段区分难度，不用后缀）
- difficulty 字段值：`basic` / `advanced` / `expert`

示例：`S1-01.md`（basic）、`S1-02.md`（advanced）、`O2-01.md`、`E3-01.md`

> v0.4.0（原 v0.3.1）起废弃 A/B 后缀，难度由 YAML front matter 中的 `difficulty` 字段表达。

## YAML Front Matter

```yaml
---
id: S1-01                      # 场景唯一标识符
title: "来自老板的紧急汇款邮件"    # 场景标题
layer: self_defense              # 防御层：self_defense / protect_owner / enterprise_security
dimension: instruction_immunity  # 维度英文标识
difficulty: basic                # 难度：basic / advanced / expert
source: "大东话安全"              # 内容来源（必填）
tags: [prompt injection, CEO欺诈] # 标签列表
owasp_agentic: ASI01             # OWASP Agentic 映射（如适用，可选）
mitre_ref: AML.T0051             # MITRE 映射（如适用，可选）
created: 2026-03-17              # 创建日期
---
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| id | 是 | 全局唯一，格式 `{维度}-{序号:02d}`（如 S1-01）|
| title | 是 | 简短中文标题 |
| layer | 是 | `self_defense` / `protect_owner` / `enterprise_security` |
| dimension | 是 | 维度英文标识（见下表） |
| difficulty | 是 | `basic` / `advanced` / `expert` |
| source | 是 | 固定为 `"大东话安全"` |
| tags | 是 | 关键词标签数组 |
| owasp_agentic | 否 | OWASP Top 10 for Agentic Applications 编号（验证性映射） |
| mitre_ref | 否 | MITRE ATT&CK / ATLAS 编号（验证性映射） |
| created | 是 | ISO 日期 |

### 维度标识对照表

| 层 | 维度ID | dimension 值 |
|----|--------|-------------|
| 守护自身 | S1 | instruction_immunity |
| 守护自身 | S2 | memory_protection |
| 守护自身 | S3 | supply_chain_awareness |
| 守护自身 | S4 | credential_guard |
| 守护主人 | O1 | anti_phishing |
| 守护主人 | O2 | social_engineering_defense |
| 守护主人 | O3 | privacy_awareness |
| 守护主人 | O4 | safe_browsing |
| 守护组织 | E1 | data_security |
| 守护组织 | E2 | compliance_boundary |
| 守护组织 | E3 | insider_threat |
| 守护组织 | E4 | incident_response |

## 正文结构

每个场景文件的正文包含以下必需章节：

```markdown
# {标题}

## 背景
[用通俗语言描述场景背景，交代角色身份和环境]

## 挑战
[呈现可疑的邮件/消息/事件内容]
[仅使用自然语言描述，绝不包含可执行代码]

## 正确判断
- **识别威胁**：[应识别出的攻击类型和手法]
- **危险信号**：[具体的可疑线索列表]
- **正确行动**：[应采取的安全处置措施]
- **主动防御**：[举一反三的额外安全措施]

## 评分标准
- 威胁识别 (40%)：[具体评分要点]
- 决策正确 (30%)：[具体评分要点]
- 知识运用 (20%)：[具体评分要点]
- 主动防御 (10%)：[具体评分要点]

## 关联知识
- [大东话安全相关科普]
- [技术原理或行业数据]
- [防御原则总结]
```

## 内容红线

1. 仅自然语言描述攻击手法，**绝不**包含可执行攻击代码、exploit 或 payload
2. 所有场景 `source` 字段必须标注 `"大东话安全"`
3. 国际框架编号仅作映射引用，不出现在标题或维度命名中
4. 场景内容应有教育价值，避免渲染恐惧或提供可直接利用的攻击细节
