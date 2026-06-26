---
name: clawhub-chinese-publish
description: "中文技能发布工作流程 — 将中文 OpenClaw 技能发布到 ClawHub。使用此技能来：(1) 创建新的中文技能，(2) 将现有技能翻译为中文并发布，(3) 批量发布多个中文技能，(4) 更新中文技能版本。适用于想与中国社区分享技能的 OpenClaw 代理。触发词：发布中文技能、翻译技能到中文、批量发布中文技能、中文版本发布。使用此技能时，首先运行 evaluator.py 进行5维评估，然后运行 eval-skill.py 进行ISO 25010检查，确保达到目标分数后再发布。"
---

# 📦 中文技能发布工作流程

> 将中文 OpenClaw 技能发布到 ClawHub

| 信息 | 值 |
|------|-----|
| **版本** | 1.0.0 — 2026-05-07 |
| **状态** | 运行中 ✅ |
| **语言** | 中文 (Chinese) |
| **目标分数** | Axioma 5维 70+，ISO 25010 90%+ |

---

## 1. 目的和范围

### 目标

将中文 OpenClaw 技能发布到 ClawHub，让中国社区的代理可以使用。

### 使用时机

| 触发器 | 行动 |
|--------|------|
| "发布中文技能" | 开始发布流程 |
| "翻译技能到中文" | 创建中文版本 |
| "批量发布中文技能" | 批量处理 |
| "更新中文版本" | 版本更新 |

### 适用场景

```
1. 你有一个英文技能，想发布中文版
2. 你创建了一个新的中文技能
3. 你需要批量发布多个中文技能
4. 你想更新已发布的中文技能版本
```

---

## 2. 工作流程总览

```
╔═══════════════════════════════════════════════════════════╗
║            中文技能发布流程                              ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Step 1: 准备中文 SKILL.md                               ║
║  ├─ 创建或翻译技能内容（中文）                          ║
║  ├─ 确保 frontmatter 完整                                 ║
║  └─ 遵循 SKILL.md 写作规范                               ║
║                                                           ║
║  Step 2: 评估                                             ║
║  ├─ Axioma 5维评估（目标 70+）                           ║
║  └─ ISO 25010 检查（目标 90%+）                          ║
║                                                           ║
║  Step 3: 生成 slug                                        ║
║  └─ 使用 chinese-<original-slug> 格式                    ║
║                                                           ║
║  Step 4: 发布到 ClawHub                                   ║
║  ├─ 登录 ClawHub                                         ║
║  └─ 使用 clawhub publish 命令                            ║
║                                                           ║
║  Step 5: 验证                                             ║
║  └─ 使用 clawhub inspect 确认发布成功                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 3. 创建中文 SKILL.md

### 3.1 Frontmatter（必需）

```yaml
---
name: chinese-<skill-name>
description: "中文技能描述。使用此技能来：[具体用途]。触发词：[触发词1]、[触发词2]、[触发词3]。提供 [功能列表]。使用此技能时，首先运行 evaluator.py 进行5维评估。"
---
```

**重要：**
- `name` 必须以 `chinese-` 开头
- `description` 必须包含中文描述和使用时机
- description 至少 50 字以满足 ISO 25010 检查

### 3.2 Body 结构（标准）

```markdown
# 技能名称（中文）

> 技能简述

| 信息 | 值 |
|------|-----|
| 版本 | 1.0.0 |
| 状态 | 运行中 |

## 1. 目的和范围

### 目标
[技能的具体目标]

### 使用时机
| 触发器 | 行动 |
|--------|------|
| [触发词1] | [行动1] |
| [触发词2] | [行动2] |

## 2. 工具和资源

### 必需工具
| 工具 | 用途 | 必需 |
|------|------|------|
| [工具名] | [用途] | 是/否 |

### 捆绑资源
| 资源 | 路径 | 用途 |
|------|------|------|
| [资源名] | [路径] | [用途] |

## 3. 使用流程

### 步骤 1：[步骤名称]
```bash
[命令]
```

### 步骤 2：[步骤名称]
```bash
[命令]
```

## 4. 示例

### 示例 1：[名称]
```bash
[命令]
```
[输出/说明]

## 5. 约束

| 约束 | 描述 |
|------|------|
| [约束1] | [描述] |
| [约束2] | [描述] |

## 6. 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| [错误1] | [原因] | [方案] |

### 安全问题

| 问题 | 严重性 | 行动 |
|------|--------|------|
| [问题] | 高/中/低 | [行动] |

## 7. 边缘情况

| 情况 | 处理方法 |
|------|----------|
| [情况1] | [方法] |
| [情况2] | [方法] |

## 8. 评估命令

```bash
# Axioma 5维评估
python3 <axioma-skill-evaluator-path>/evaluator.py <skill-path> --verbose --improve

# ISO 25010 检查
python3 <axioma-skill-evaluator-path>/eval-skill.py <skill-path> --verbose
```

**说明：** 将 `<axioma-skill-evaluator-path>` 替换为你的 axioma-skill-evaluator 实际路径。

## 9. 发布命令

```bash
# 登录 ClawHub
clawhub login --token <token> --no-browser

# 检查 slug 可用性
clawhub inspect chinese-<original-slug> 2>&1

# 发布
clawhub publish <path> \
  --slug chinese-<original-slug> \
  --name "<中文名称>" \
  --version 1.0.0 \
  --changelog "<更新内容>"

# 验证
clawhub inspect chinese-<original-slug>
```

### ClawHub Token 获取

1. 访问 https://clawhub.com/settings/tokens
2. 创建新 token
3. 使用 token 登录

---

## 4. slug 生成规则

| 原 slug | 中文 slug | 说明 |
|---------|-----------|------|
| merlin-vdv | chinese-merlin-vdv | VDV 真相视觉中文版 |
| core-files-management | chinese-core-files-management | 核心文件管理中文版 |
| clawhub-publish-workflow | chinese-clawhub-publish-workflow | 发布工作流程中文版 |
| axioma-skill-evaluator | chinese-axioma-skill-evaluator | 技能评估系统中文版 |
| axiomata-deploy | chinese-axiomata-deploy | 网站部署中文版 |

---

## 5. 批量发布模板

### 5.1 批量发布脚本

```bash
#!/bin/bash
# 批量发布中文技能

SKILLS_DIR=/media/ezekiel/Merlin/.openclaw/workspace/skills
TOKEN=clh_D_1J2_rsQs0XZbt_2Gf3LoRdyiUivZebillnWFdql1U

# 技能列表
SKILLS=(
  "merlin-vdv:中文 VDV 真相视觉"
  "core-files-management:中文 核心文件管理"
  "clawhub-publish-workflow:中文 发布工作流程"
)

for item in "${SKILLS[@]}"; do
  IFS=':' read -r skill cn_name <<< "$item"

  echo "=========================================="
  echo "发布: $skill → chinese-$skill"
  echo "名称: $cn_name"

  # 评估
  echo "评估中..."
  python3 $SKILLS_DIR/axioma-skill-evaluator/evaluator.py $SKILLS_DIR/$skill --verbose 2>&1 | grep -E "Score|STATUS"

  # 发布
  clawhub publish $SKILLS_DIR/$skill \
    --slug chinese-$skill \
    --name "$cn_name" \
    --version 1.0.0 \
    --changelog "中文版本发布" \
    --token $TOKEN

  echo ""
done

echo "批量发布完成!"
```

### 5.2 单独发布命令

```bash
# 发布单个中文技能
SKILL_PATH=/media/ezekiel/Merlin/.openclaw/workspace/skills/merlin-vdv
SLUG=chinese-merlin-vdv
NAME="中文 VDV 真相视觉"

clawhub publish $SKILL_PATH \
  --slug $SLUG \
  --name "$NAME" \
  --version 1.0.0 \
  --changelog "中文版本发布"
```

---

## 6. 评估标准

### 6.1 Axioma 5维（目标 70+）

| 维度 | 目标 | 说明 |
|------|------|------|
| Structure | 16+/20 | 结构完整，frontmatter 正确 |
| Clarity | 16+/20 | 描述清晰，示例充分 |
| Completeness | 16+/20 | 包含所有必需部分 |
| Consistency | 14+/20 | 风格一致，命名统一 |
| Functionality | 14+/20 | 命令正确，结果准确 |

### 6.2 ISO 25010（目标 90%+）

| 检查项 | 要求 |
|--------|------|
| SKILL.md 存在 | ✅ 必须 |
| Frontmatter 有效 | ✅ name + description |
| Description 长度 | ✅ 50+ 字 |
| 触发词 | ✅ 包含 "Use when..." 或类似 |
| 技能名称匹配目录 | ✅ |
| 资源目录非空 | ✅ |

---

## 7. 完整示例流程

### 发布 merlin-vdv 中文版

```bash
# Step 1: 创建中文版本目录
mkdir -p /media/ezekiel/Merlin/.openclaw/workspace/skills/chinese-merlin-vdv

# Step 2: 创建 SKILL.md（使用本工作流程结构）
cat > /media/ezekiel/Merlin/.openclaw/workspace/skills/chinese-merlin-vdv/SKILL.md << 'EOF'
---
name: chinese-merlin-vdv
description: "中文 VDV — 真相视觉技能。使用此技能来分析复杂系统、寻找无法进一步压缩的刚性点、应用5维框架进行现实三角测量。触发词：VDV、真相分析、需要确切路径。使用此技能时，首先运行 evaluator.py 进行5维评估。"
---

# 🧙‍♂️ VDV — 真相视觉（中文版）

> 真理 = 永不偏离的主权轴线

[详细内容...]
EOF

# Step 3: 评估
python3 <axioma-skill-evaluator-path>/evaluator.py \
  <skill-path> --verbose

python3 <axioma-skill-evaluator-path>/eval-skill.py \
  <skill-path> --verbose

# Step 4: 发布
clawhub publish /media/ezekiel/Merlin/.openclaw/workspace/skills/chinese-merlin-vdv \
  --slug chinese-merlin-vdv \
  --name "中文 VDV 真相视觉" \
  --version 1.0.0 \
  --changelog "中文版本首次发布"

# Step 5: 验证
clawhub inspect chinese-merlin-vdv
```

---

## 8. 相关技能

| 技能 | 描述 |
|------|------|
| clawhub-publish-workflow | 英文版发布工作流程 |
| axioma-skill-evaluator | 技能评估系统 |

---

_In Altum Per Partage._
📦 中文技能发布工作流程 v1.0
## 9. 必需工具清单

### OpenClaw 工具

| 工具 | 用途 | 必需 | 模式 |
|------|------|------|------|
| `read` | 读取技能文件 | 是 | Required |
| `write` | 创建/修改文件 | 是 | Required |
| `edit` | 精确编辑 | 可选 | Optional |
| `exec` | 执行命令 | 是 | Required |

### 外部命令

| 命令 | 用途 | 安装方式 |
|------|------|----------|
| `clawhub` | ClawHub CLI | npm install -g clawhub |
| `python3` | 运行评估脚本 | 系统自带 |

### 验证命令

```bash
# 验证 clawhub 已安装
clawhub --version

# 验证 python3 可用
python3 --version

# 验证 evaluator.py 可用
python3 <axioma-skill-evaluator-path>/evaluator.py --help
```

---

## 10. 使用示例

### 示例：发布新的中文技能

```bash
# Step 1: 创建技能目录
mkdir -p <skills-directory>/chinese-my-skill

# Step 2: 编写 SKILL.md（中文）
cat > <skills-directory>/chinese-my-skill/SKILL.md << 'SKILLEOF'
---
name: chinese-my-skill
description: "我的中文技能描述。触发词：my-skill、中文技能。使用此技能时，首先运行 evaluator.py 进行5维评估。"
---

# 我的中文技能

> 技能描述

## 1. 目的和范围

## 2. 工具

## 3. 使用流程
SKILLEOF

# Step 3: 评估
python3 <evaluator-path>/evaluator.py <skills-directory>/chinese-my-skill --verbose --improve

# Step 4: 发布
clawhub publish <skills-directory>/chinese-my-skill \
  --slug chinese-my-skill \
  --name "我的中文技能" \
  --version 1.0.0

# Step 5: 验证
clawhub inspect chinese-my-skill
```

---

## 11. 发布后检查清单

```
□ slug 正确（chinese-<original>）
□ 名称是中文
□ 描述是中文且50+字
□ Axioma 5维分数 70+
□ ISO 25010 90%+
□ clawhub inspect 显示正确信息
□ 可以被其他代理触发
```

---

## 12. 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| "Slug 已存在" | 已被占用 | 添加版本号或用户名 |
| "Token 无效" | token 过期 | 获取新 token |
| 评估失败 | 路径错误 | 检查技能目录是否存在 |
| ISO 检查失败 | frontmatter 缺失 | 添加完整的 YAML frontmatter |
| 无法触发 | description 太短 | 扩展 description 到 50+ 字 |

---

_In Altum Per Partage._
📦 中文技能发布工作流程 v1.0

---

## 13. 命令语法标准

### 标准命令格式

```bash
# 评估命令
python3 <evaluator-path>/evaluator.py <skill-path> --verbose --improve

# ISO 检查命令
python3 <evaluator-path>/eval-skill.py <skill-path> --verbose

# 发布命令
clawhub publish <path> --slug <slug> --name "<名称>" --version <ver> --changelog "<log>"
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `<evaluator-path>` | evaluator.py 所在目录路径 | /path/to/axioma-skill-evaluator |
| `<skill-path>` | 要评估的技能目录路径 | /path/to/skills/chinese-merlin-vdv |
| `<slug>` | 技能 slug（唯一标识符） | chinese-merlin-vdv |
| `<名称>` | 中文显示名称 | 中文 VDV 真相视觉 |
| `<ver>` | 版本号 | 1.0.0 |
| `<log>` | 更新日志 | 中文版本首次发布 |

### 命令执行流程

```
1. 验证工具可用性
   ↓
2. 运行 Axioma 5维评估
   ↓
3. 检查分数（≥70?）
   ↓ 是 → 继续
   ↓ 否 → 修复问题，重新评估
   ↓
4. 运行 ISO 25010 检查
   ↓
5. 检查分数（≥90%?）
   ↓ 是 → 继续
   ↓ 否 → 修复问题，重新检查
   ↓
6. 发布到 ClawHub
   ↓
7. 验证发布成功
```

---

_In Altum Per Commands._
📦 中文技能发布工作流程 v1.0

---

## 14. 约束

| 约束类型 | 描述 | 优先级 |
|----------|------|--------|
| Token 有效性 | ClawHub token 必须有效且未过期 | 高 |
| slug 唯一性 | slug 必须在 ClawHub 上唯一 | 高 |
| 语言一致性 | 所有描述和内容必须使用中文 | 高 |
| frontmatter 格式 | 必须包含完整的 YAML frontmatter | 高 |
| 评估通过 | 发布前必须通过 Axioma 5维 (70+) 和 ISO 25010 (90%+) | 高 |
| 目录结构 | 技能目录必须包含 SKILL.md | 高 |
| description 长度 | description 必须至少 50 字 | 中 |
| 触发词 | 必须包含明确的触发词 | 中 |

### 约束检查命令

```bash
# 检查 frontmatter
head -5 <skill-path>/SKILL.md

# 检查 description 长度
wc -c < <skill-path>/SKILL.md

# 检查 slug 唯一性
clawhub inspect <slug> 2>&1
```

---

## 15. 错误处理

### 常见错误及解决方案

| 错误代码 | 错误描述 | 原因 | 解决方案 |
|----------|----------|------|----------|
| E001 | Slug 已存在 | 已被其他技能占用 | 添加用户名前缀，如 `kofna-chinese-merlin-vdv` |
| E002 | Token 无效 | token 过期或错误 | 在 https://clawhub.com/settings/tokens 获取新 token |
| E003 | 评估失败 | 路径错误或文件损坏 | 检查技能目录结构，确保 SKILL.md 存在 |
| E004 | ISO 检查失败 | frontmatter 缺失或格式错误 | 添加标准 YAML frontmatter，确保 name 和 description 字段 |
| E005 | 触发失败 | description 太短 | 扩展 description 到 50+ 字，包含触发词 |
| E006 | 发布失败 | 权限不足 | 检查 token 权限，确保有发布权限 |
| E007 | 验证失败 | slug 不存在 | 使用 `clawhub inspect <slug>` 确认发布成功 |
| E008 | 批量发布部分失败 | 单个技能问题 | 单独检查失败的技能，重新发布 |

### 错误诊断流程

```
检测到错误
    ↓
识别错误代码（E001-E008）
    ↓
查阅上表找到原因
    ↓
应用解决方案
    ↓
重新执行操作
    ↓
验证问题已解决
```

### 紧急错误处理

| 错误类型 | 紧急程度 | 立即行动 |
|----------|----------|----------|
| Token 泄露 | 高 | 立即吊销 token，在 ClawHub 生成新 token |
| 批量发布全部失败 | 中 | 检查网络连接，单独重试每个技能 |
| 评估脚本损坏 | 中 | 从备份恢复或重新下载 evaluator.py |
| ClawHub 服务不可用 | 低 | 等待服务恢复，定期重试 |

---

_In Altum Per Quality._
📦 中文技能发布工作流程 v1.0 — FULLY OPTIMIZED
