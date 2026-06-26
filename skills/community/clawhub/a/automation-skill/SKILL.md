---
name: automation-skill
description: 自动化综合技能包。提供多引擎并行搜索（百度/必应/Google/DuckDuckGo等）、每日复盘记录与分析两大实战脚本。当用户需要：1）高效批量搜索（"帮我搜XXX"、"多引擎搜索"）；2）自我反思与成长记录（"记录这次反思"、"生成复盘报告"）；3）搜索和安装技能（"安装XX技能"）时触发。
---

# automation-skill · 自动化综合技能包

> 让 AI Agent 真正能「干活」的可执行技能包
> 包含两个生产级 Python 脚本 + 完整的 CLI 接口

---

## 🧩 包含内容

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `scripts/search_workflow.py` | 多引擎并行搜索 + 去重 + 评分 | 需要快速获取多源信息 |
| `scripts/self_reflect.py` | 复盘记录 + 规律分析 + 报告生成 | 持续改进、记录教训 |
| `find-skills` 能力 | 搜索和安装 Agent 技能 | 扩展 AI 能力 |

---

## 🔍 多引擎并行搜索 `search_workflow.py`

### 快速开始

```bash
# 安装依赖
pip install requests

# 基本搜索（自动使用全部引擎）
python scripts/search_workflow.py "Python异步编程最佳实践"

# 指定引擎
python scripts/search_workflow.py "QClaw使用教程" -e baidu bing_cn google

# 输出到文件
python scripts/search_workflow.py "AI Agent开发教程" -o result.json
```

### 支持的引擎

**国内**: 百度、必应(中国)、搜狗、头条搜索
**国际**: Google、DuckDuckGo、Brave、WolframAlpha

### 核心特性

- ⚡ **并行搜索** — 多引擎同时请求，结果汇总更快
- 🔁 **智能去重** — URL 去重，避免重复结果
- 🏆 **结果评分** — 按来源权重和内容质量排序
- 📄 **JSON 输出** — 程序化调用的理想格式

### 输出示例

```
[14:32:05] 开始多引擎搜索: Python异步编程最佳实践
使用的引擎: ['百度', '必应', 'Google', 'DuckDuckGo']

✓ 搜索完成，耗时 3.21s
  总结果: 38 | 去重后: 24

  1. Python asyncio 异步编程完全指南
      🔗 https://realpython.com/async...
      💬 asyncio 是 Python 3.4 引入的标准库...
  2. ...

📄 完整结果已保存到: result.json
```

### JSON 输出格式

```json
{
  "keyword": "Python异步编程最佳实践",
  "total_results": 38,
  "engines_used": ["百度", "必应", "Google", "DuckDuckGo"],
  "deduped_count": 24,
  "top_results": [
    {
      "rank": 1,
      "title": "Python asyncio 完全指南",
      "url": "https://...",
      "snippet": "asyncio 是 Python 3.4...",
      "engine": "google"
    }
  ],
  "elapsed_seconds": 3.21
}
```

---

## 📊 自我复盘记录 `self_reflect.py`

### 快速开始

```bash
# 记录一次复盘
python scripts/self_reflect.py add \
  -c "用户问XX功能实现" \
  -w "我直接给了方案但没有先确认需求细节" \
  -l "遇到需求类问题，先反问确认，再给方案" \
  -s 3 \
  -t coding accuracy

# 查看复盘报告
python scripts/self_reflect.py report

# 列出最近记录
python scripts/self_reflect.py list -n 10

# 查看统计
python scripts/self_reflect.py stats
```

### 报告示例

```
# 📊 自我复盘报告
生成时间: 2026-04-12 14:30

## 📈 总体统计
- 总复盘次数: 15
- 最新记录: 2026-04-12 10:15 | 场景: 邮件发送

## 🏷️ 高频问题领域
- coding: ████ (12次)
- communication: ██ (5次)

## ⚠️ 严重程度分布
- 🔵 轻微(1-2): 3 次
- 🟡 一般(3): 8 次
- 🔴 严重(4-5): 4 次

## ♻️ 反复出现的问题（需重点关注）
- ⚠️ 遇到需求类问题，先反问确认，再给方案

## 💡 最新教训
> 与其给10个选项，不如给1个最优解+理由
```

### 记忆层级

| 层级 | 文件 | 说明 |
|------|------|------|
| HOT | `~/.qclaw/memory/memory.md` | 最新教训，随时可查 |
| WARM | `~/.qclaw/memory/projects/` | 按项目组织的经验 |
| COLD | `~/.qclaw/memory/archive/` | 历史归档 |

---

## 🔧 安装脚本依赖

```bash
# 搜索脚本
pip install requests

# 复盘脚本（纯标准库，无需额外安装）
# 无需依赖
```

---

## ⚙️ Skill 触发规则

| 用户说 | 触发 |
|--------|------|
| "帮我搜一下XXX" / "多引擎搜索" | `search_workflow.py` |
| "记录这次反思" / "生成复盘报告" | `self_reflect.py` |
| "有没有能做XX的技能" / "安装XX" | `find-skills` 能力 |
| "你学到了什么" / "你知道XX吗" | 搜索 `memory.md` |

---

## 🔄 Skill 自查清单（发布前必读）

- [x] `search_workflow.py` — 完整可执行，含错误处理
- [x] `self_reflect.py` — 完整可执行，纯标准库零依赖
- [x] 所有路径使用跨平台写法（`Path` / `sys.executable`）
- [x] 中文输出无乱码（`encoding="utf-8"` 显式指定）
- [x] `--help` 信息完整
- [x] 已在本地实测运行通过

---

## 📝 变现定价建议

| 方案 | 价格 | 说明 |
|------|------|------|
| 基础版 | 免费 | 基础搜索 + 简单复盘 |
| Pro 版 | ¥9.9/月 | 多引擎 + 去重评分 + 历史报告 |
| Team 版 | ¥29/月 | 团队共享记忆 + 多用户统计 |

---

*本 Skill 由 automation-skill 团队维护 · 版本 2.0.0*
