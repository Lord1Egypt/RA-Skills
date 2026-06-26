---
name: byted-security-skillsscanner
description: 审计和扫描技能的安全性。当用户希望对工作区中的其他技能进行安全扫描时使用。
---

# Volcengine技能安全扫描器 (Volcengine Skills Scanner)

通过将技能目录打包并上传火山引擎安全扫描服务进行扫描，审计工作区中的其他技能是否存在潜在的安全风险。

## 何时使用

- **审计**：定期扫描所有技能以确保符合安全策略。
- **开发**：在开发过程中检查自己的技能。
- **要求**：必须确保目标技能包含 `SKILL.md` 文件，因为它是扫描的主要输入。

## 用法

使用 `scripts/scan.py` 脚本执行扫描。**必须使用绝对路径，不要使用~**，因为运行目录不是 skill 目录。

脚本会自动打包目录（如果提供的是目录）并上传，始终输出包含扫描结果的 JSON 数组。解析此JSON并以易读的格式（中文）向用户展示结果（风险等级、详细信息、建议）。

### 扫描技能（目录或压缩包）

脚本通过环境变量读取配置(推荐)

```bash
python3 ~/.openclaw/workspace/skills/byted-security-skillsscanner/scripts/scan.py --name "bad_skills1" --path "/root/.openclaw/workspace/skills/bad_skills1"
```

**重要**：
- 脚本路径必须是**绝对路径**
- 目标路径也必须是**绝对路径**
- 确保已设置必要的环境变量（`VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`）

## 报告格式

向用户展示结果时，**必须**使用以下格式（中文）：

### 🛡️ 安全扫描报告：[SkillName]

**扫描时间**: [将 ScanEndTime 时间戳转换为可读日期格式]
**整体状态**: [✅ 通过 / ❌ 发现风险]

| 风险等级 | 规则名称 | 风险详情 |
| :--- | :--- | :--- |
| **[High/Medium/Low]** | [RuleName] | [RiskDetail] |

**发现的风险列表：**
（仅列出 High 和 Medium 级别的风险）

1. **[RuleName] (ID: [RuleID])**
   - **等级**: [RiskLevel]
   - **文件**: [FileName]
   - **详情**: [RiskDetail]
   - **建议**: 请检查上述文件中的代码，移除可疑的网络请求或敏感操作。

---

## 环境变量配置

1. 获取火山引擎访问凭证：参考 [用户指南](https://www.volcengine.com/docs/6291/65568?lang=zh) 获取 AK/SK

2. 配置以下环境变量:

```bash
export VOLC_ACCESS_KEY="your-access-key"
export VOLC_SECRET_KEY="your-secret-key"
export VOLC_REGION="cn-north-1"  # 可选，默认 cn-north-1
```