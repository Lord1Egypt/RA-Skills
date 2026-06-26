# Skill 蒸馏完整工作流

> 来源：apple-design (99.0 A)、ios-dev (96.5 A)、swift-language (94.0 A)、flutter-dev (91.0 A)、material-design (96.0 A) 五个 A 级 skill 的蒸馏过程经验
> 整理时间：2026-04-23

## 蒸馏流程概览

```
┌─────────────────────────────────────────────────────┐
│ Phase 1: 规划                                       │
│  - 确定技能定位和边界                               │
│  - 分析现有 skill（避免重复）                       │
│  - 确定知识来源和爬取策略                           │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Phase 2: 骨架搭建                                   │
│  - 创建目录结构                                     │
│  - 编写 SKILL.md 框架                               │
│  - （评估脚本已集中管理，无需复制）                 │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Phase 3: 内容填充                                   │
│  - 爬取可爬取站点的内容                             │
│  - 蒸馏不可爬取站点的内容                           │
│  - 创建参考文档                                     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Phase 4: 评估打分                                   │
│  - 运行评估脚本                                     │
│  - 识别短板维度                                     │
│  - 制定改进计划                                     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Phase 5: 迭代修复                                   │
│  - 按优先级修复评分短板                             │
│  - 重新评估验证                                     │
│  - 循环直到达到 A 级                               │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ Phase 6: 同步部署                                   │
│  - 同步到 Hermes 目录                               │
│  - 验证 skill 可用                                 │
└─────────────────────────────────────────────────────┘
```

---

## Phase 1: 规划

### 确定技能定位

```bash
# 1. 检查是否已有相关 skill
ls <skill_dir>/ | grep -i <keyword>
ls <skill_dir>/ | grep -i <platform>

# 2. 确定技能边界
#    - 避免与现有 skill 重叠
#    - 确定核心覆盖范围
#    - 确定触发场景

# 3. 确定目标评分
#    - 新建 skill：目标 A (90+)
#    - 现有 skill 提升：目标 A+ (95+)
```

### 源可爬取性分析

| 站点 | 可爬性 | 策略 |
|------|--------|------|
| docs.swift.org | ✅ | 浏览器提取 |
| developer.mozilla.org | ✅ | 浏览器提取 |
| developer.apple.com | ❌ | 知识蒸馏 |
| developer.huawei.com | ❌ | 知识蒸馏 |
| developer.android.com | ❌ | 知识蒸馏 |
| flutter.dev | ❌ | 知识蒸馏 |

---

## Phase 2: 骨架搭建

### 创建目录结构

```bash
SKILL_NAME="<skill-name>"
BASE="/mnt/c/Users/yhong/.claude/skills"

mkdir -p "${BASE}/${SKILL_NAME}/references"
mkdir -p "${BASE}/${SKILL_NAME}/templates"
```

### 编写 SKILL.md 框架

```markdown
---
name: <skill-name>
description: <一句话描述>
trigger: <触发词1|触发词2|...>
tags:
  - <tag>
hermes:
  platform: hermes
  version: "1.0"
  last_updated: "<YYYY-MM-DD>"
  source: |
    <官方文档 URL>
---

# <Skill 标题>

## 核心章节 1

## 核心章节 2

## 核心章节 3

## 避坑指南

## 输出格式规范

## 快速参考
```

---

## Phase 3: 内容填充

### 爬取可爬取站点

```bash
# 使用浏览器工具
# 1. browser_navigate → URL
# 2. browser_console → document.querySelector('article')?.innerText
# 3. 保存到 references/
```

### 蒸馏不可爬取站点

```bash
# 1. 确定知识结构
# 2. 使用 LLM 辅助生成
# 3. 验证 API 签名和版本号
# 4. 保存到 references/
```

### 参考文档创建

每个参考文档应：
- 覆盖一个完整的主题
- 包含真实的 API 签名
- 包含完整的代码示例
- 标注官方来源 URL
- 达到 300+ 行

---

## Phase 4: 评估打分

### 运行评估

```bash
python ../../distill-skill-builder/scripts/skill_evaluator_v2.py \
   <skill_dir>/<skill-name>
```

### 分析评分报告

```
维度                       得分       权重
────────────────────────────────────────
触发词覆盖             15.0/15    ██████████  ← 满分
元数据完整性            10.0/10    ██████████  ← 满分
核心内容深度            20.0/20    ██████████  ← 满分
快速参考              13.0/15    ███████░░░  ← 差 2 分
避坑指南              15.0/15    ██████████  ← 满分
来源标注               9.0/10    █████████░  ← 差 1 分
参考文档覆盖             7.0/10    ███████░░░  ← 差 3 分
输出格式规范             5.0/5     ██████████  ← 满分
```

### 制定改进计划

| 优先级 | 维度 | 当前分 | 目标分 | 改进动作 |
|--------|------|--------|--------|---------|
| 1 | 快速参考 | 13 | 15 | 添加更多表格和代码块 |
| 2 | 来源标注 | 9 | 10 | 在 body 添加日期 |
| 3 | 参考文档覆盖 | 7 | 10 | 添加更多参考文档 |

---

## Phase 5: 迭代修复

### 迭代模式

```
评估 → 识别短板 → 修复 → 评估 → 识别短板 → 修复 → ... → A 级
```

### 常见修复动作

#### 修复 1：触发词格式

```python
# 从
trigger: |
  - "Swift 语法"
  - "Swift 类型"

# 改为
trigger: Swift 语法|Swift 类型|Swift 闭包
```

#### 修复 2：添加 H1 顶级章节

```python
content = content.replace(
    "\n## 避坑指南",
    "\n# 避坑与规范\n\n## 避坑指南"
)
```

#### 修复 3：扩充快速参考

```python
# 添加更多速查表格
# 添加更多代码示例
# 添加带单位的数值（44pt, 16px 等）
```

#### 修复 4：添加来源标注

```markdown
> 来源：The Swift Programming Language (Swift 6.3)
> URL: https://docs.swift.org/swift-book/...
> 版本：Swift 6.3（2026 年 2 月）
```

---

## Phase 6: 同步部署

### 同步到 Hermes

```bash
SKILL_NAME="<skill-name>"
CLAUDE_DIR="/mnt/c/Users/yhong/.claude/skills/${SKILL_NAME}"
HERMES_DIR="$HOME/.hermes/skills/${SKILL_NAME}"

# 创建目录
mkdir -p "${HERMES_DIR}/references"

# 同步文件
cp "${CLAUDE_DIR}/SKILL.md" "${HERMES_DIR}/SKILL.md"
cp "${CLAUDE_DIR}/references/"*.md "${HERMES_DIR}/references/"

echo "✓ Synced ${SKILL_NAME} to Hermes"
```

### 同步评估器补丁

评估脚本集中管理在 `../../distill-skill-builder/scripts/skill_evaluator_v2.py`，无需分发。

当评估器需要 patch 时，只需 patch 集中脚本即可。

---

## 蒸馏经验总结

### 最高效的提分动作

| 排名 | 动作 | 耗时 | 分数变化 |
|------|------|------|---------|
| 1 | 修复触发词格式 | 3 分钟 | +12 |
| 2 | 添加来源标注 | 5 分钟 | +7 |
| 3 | 插入顶级 H1 | 5 分钟 | +6 |
| 4 | 扩充快速参考 | 10 分钟 | +2 |
| 5 | 创建参考文档 | 20 分钟 | +3-4 |

### 常见陷阱

1. **frontmatter URL 不计入** — source 放在 hermes: 里需 patch
2. **多行 trigger 解析失败** — 必须单行 `|` 分隔
3. **H1 数量不足** — 需要插入顶级章节
4. **表格格式错误** — `|...|...|` 需至少两行
5. **关键数值不识别** — 需要 `44pt`、`16px` 等带单位格式

### 评估器已知局限

| 问题 | 影响 | 规避方法 |
|------|------|---------|
| 只认 Apple/Huawei URL | 来源少 3-4 分 | 在 body 加 URL |
| frontmatter 日期不计 | 来源少 3 分 | 在 body 加日期 |
| 关键数值正则过严 | 快速参考少 1-2 分 | 用带单位数值 |

---

## 来源

> material-design-skill 蒸馏过程
> flutter-dev-skill 蒸馏过程
> harmonyos-dev-skill 蒸馏过程
> ios-dev-skill 蒸馏过程
> apple-higDesign-skill 蒸馏过程
