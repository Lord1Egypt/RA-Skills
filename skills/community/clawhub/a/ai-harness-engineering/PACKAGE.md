# AI Harness Engineering - AI驾驭工程错题本

## 简介

OpenClaw 的自省机制：记录所有被验证的错误、幻觉、缺陷，形成可追溯错误台账，驱动模型自省与进化。

**核心功能**：
- ✅ 错误记录 + 学习记录 + 功能请求跟踪
- ✅ 回答前自检 + 错误摘要注入
- ✅ 定时自动提升 + 定期回顾
- ✅ 统计面板 + 错误模式库

---

## 安装方法

### 方法一：导入 .skill 文件（推荐）

```bash
# 1. 下载 harness-engineering.skill 文件
# 2. 在 OpenClaw 中导入
/install harness-engineering.skill
```

### 方法二：手动安装

```bash
# 1. 复制 skill 目录
cp -r harness-engineering/ ~/.qclaw/skills/

# 2. 创建数据目录
mkdir -p ~/.qclaw/skills/harness-engineering/data/

# 3. 创建空数据文件
touch ~/.qclaw/skills/harness-engineering/data/error_ledger.jsonl
touch ~/.qclaw/skills/harness-engineering/data/feature_ledger.jsonl
touch ~/.qclaw/skills/harness-engineering/data/learnings_ledger.jsonl
touch ~/.qclaw/skills/harness-engineering/data/error_index.json
```

---

## 快速命令参考

### 记录错误
```bash
python3 "{SKILL_DIR}/scripts/record_error.py" \
  --scene "问答" \
  --error-type "事实错误" \
  --question "用户问题" \
  --wrong-answer "错误回答" \
  --correct-answer "正确答案" \
  --reason "错误原因" \
  --level "高"
```

### 记录学习
```bash
python3 "{SKILL_DIR}/scripts/record_learning.py" \
  --category correction \
  --summary "一句话摘要" \
  --details "详细上下文" \
  --suggested-action "建议行动" \
  --priority high
```

### 记录功能请求
```bash
python3 "{SKILL_DIR}/scripts/record_feature.py" \
  --name "功能名称" \
  --context "用户场景" \
  --complexity "中等"
```

### 查询台账
```bash
python3 "{SKILL_DIR}/scripts/query.py" --type all
python3 "{SKILL_DIR}/scripts/query.py" --type errors --keywords "Python"
python3 "{SKILL_DIR}/scripts/query.py" --type errors --status pending
```

### 统计面板
```bash
python3 "{SKILL_DIR}/scripts/stats_panel.py" --period week
python3 "{SKILL_DIR}/scripts/stats_panel.py" --period all --format json
```

### 自动提升
```bash
python3 "{SKILL_DIR}/scripts/promote.py" --action auto_promote
```

### 定期回顾
```bash
python3 "{SKILL_DIR}/scripts/review.py" --action status
python3 "{SKILL_DIR}/scripts/review.py" --action full_review
```

### 回答前自检
```bash
python3 "{SKILL_DIR}/scripts/pre_answer_check.py" --question "用户问题"
```

### 错误摘要注入
```bash
python3 "{SKILL_DIR}/scripts/inject_summary.py" --action session_start
```

---

## 自动进化机制

### 定时任务（可选配置）

```bash
# 每2小时自动提升高频学习
/cron add --schedule "every 2h" --task "python3 {SKILL_DIR}/scripts/promote.py --action auto_promote"

# 每周自动回顾
/cron add --schedule "cron 0 9 * * 1" --task "python3 {SKILL_DIR}/scripts/review.py --action full_review"
```

---

## 文件结构

```
harness-engineering/
├── SKILL.md                    # 主文档
├── scripts/
│   ├── record_error.py         # 记录错误
│   ├── record_learning.py      # 记录学习
│   ├── record_feature.py       # 记录功能请求
│   ├── query.py                # 查询台账
│   ├── stats_panel.py          # 统计面板
│   ├── promote.py              # 自动提升
│   ├── review.py               # 定期回顾
│   ├── pre_answer_check.py     # 回答前自检
│   ├── inject_summary.py       # 错误摘要注入
│   └── update_status.py        # 更新状态
├── data/
│   ├── error_ledger.jsonl      # 错误台账
│   ├── feature_ledger.jsonl    # 功能请求台账
│   ├── learnings_ledger.jsonl  # 学习台账
│   └── error_index.json        # 错误索引
└── references/
    └── error_patterns.md       # 错误模式库
```

---

## 版本

- **v2.0.0** - 2026-04-01
  - 新增自动进化机制（Cron + 自动提升）
  - 新增回答前自检
  - 新增错误摘要注入
  - 新增功能请求跟踪
  - 新增统计面板
  - 新增错误模式库

---

*让每一个错误都成为进化的机会*