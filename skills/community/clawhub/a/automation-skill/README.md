# 🤖 automation-skill · 自动化综合技能包

> 让 AI Agent 真正能「干活」的可执行技能包

[English](README.md) | **中文**

---

## ✨ 这个 Skill 能做什么？

一个完整的**自动化工作流技能包**，包含两个生产级脚本 + 搜索发现能力：

### 1. 🔍 多引擎并行搜索
一键同时搜索**百度 / 必应 / Google / DuckDuckGo 等 8 个引擎**，自动去重、评分、输出 JSON。

**单条命令 vs 手动操作：**
```
❌ 手动：打开8个浏览器标签 → 逐个搜索 → 复制粘贴去重 → 30分钟
✅ automation-skill: python search_workflow.py "关键词" → 3分钟搞定
```

### 2. 📊 每日复盘记录
记录每一次教训 → 自动分析高频问题 → 生成可视化报告。

适合：开发者自我提升、内容创作者复盘、运营人员总结。

### 3. 🔧 技能发现
接入 skills.sh 技能生态，随时搜索和安装新能力。

---

## 🚀 快速安装

### 方式一：ClawHub 市场（推荐）
在 QClaw / OpenClaw 中直接搜索 `automation-skill` 安装。

### 方式二：手动安装
```bash
# 克隆或下载此目录到你的 skills 目录
git clone <repo-url> ~/.qclaw/skills/automation-skill

# 安装 Python 依赖
pip install requests
```

---

## 📌 使用示例

### 多引擎搜索
```bash
# 搜索 + 去重 + 评分，3秒出结果
python scripts/search_workflow.py "Python异步编程最佳实践"

# 指定引擎 + 输出 JSON
python scripts/search_workflow.py "QClaw技能开发" -e baidu google -o result.json

# 查看帮助
python scripts/search_workflow.py --help
```

### 复盘记录
```bash
# 记录教训
python scripts/self_reflect.py add \
  -c "用户提问" \
  -w "给了方案但没确认需求" \
  -l "需求类问题先反问再给方案"

# 生成复盘报告
python scripts/self_reflect.py report

# 查看统计
python scripts/self_reflect.py stats
```

---

## 📂 目录结构

```
automation-skill/
├── SKILL.md                  # Skill 元数据（必需）
├── README.md                 # 说明文档
├── scripts/
│   ├── search_workflow.py    # 多引擎搜索脚本
│   └── self_reflect.py       # 复盘记录脚本
└── rules/                    # 可选规则文件
```

---

## 🔧 系统要求

- Python 3.8+
- `requests` 库（仅搜索脚本需要）
- 网络连接（用于搜索引擎请求）

---

## 📄 许可证

MIT-0（免费商用，无需署名）

---

## 📈 变现版本

如需获取 Pro 版（含团队协作、API 接口、统计分析面板），
请访问 [ClawHub 商店页面](https://clawhub.ai)。

---

*维护者: automation-skill 团队 · 反馈: 提交 Issue*
