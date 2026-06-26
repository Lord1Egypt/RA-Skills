# 🐘 大象沟通日报 (Daxiang Daily Report)

> 自动获取并分析大象（美团内部通讯工具）的沟通记录，生成每日沟通汇总报告。

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://openclaw.com)
[![Version](https://img.shields.io/badge/Version-V19-blue)](./SKILL.md)

## 📋 目录

- [功能特性](#-功能特性)
- [前置要求](#-前置要求)
- [快速开始](#-快速开始)
- [使用方法](#-使用方法)
- [定时任务设置](#-定时任务设置)
- [报告输出说明](#-报告输出说明)
- [配置说明](#-配置说明)
- [故障排除](#-故障排除)
- [版本历史](#-版本历史)

---

## ✨ 功能特性

| 功能 | 说明 |
|:-----|:-----|
| 📊 **数据概览** | 统计个人对话数、群聊数、系统通知数、消息总数 |
| ⏰ **时间精力分布** | 按上午/下午/晚间/凌晨时段分析沟通情况 |
| 👤 **单人沟通分析** | 提取关键对话内容、主题和洞察，完整沟通记录表格展示 |
| 💬 **群聊汇总** | 群消息统计、@我的消息、群内容摘要 |
| 💡 **整体洞察** | 关键人/群分析、各方向分析、精力分布 |
| ✅ **todo清单** | 自动识别待办事项、来源、时间、备注 |

---

## 🛠 前置要求

### 必需

| 依赖 | 版本 | 说明 |
|:-----|:-----|:-----|
| **Python** | 3.8+ | 脚本运行环境 |
| **OpenClaw** | 最新版 | 浏览器自动化（用于获取大象数据） |

### 可选

| 依赖 | 说明 |
|:-----|:-----|
| **DX CLI** | 大象命令行工具（可选，用于获取历史消息） |
| **Chrome** | 浏览器（通过OpenClaw控制） |

### 安装 DX CLI（可选）

```bash
# TODO: 添加DX CLI安装说明
# 具体安装方法请参考美团内部文档
```

---

## 🚀 快速开始

### 1. 手动生成昨日日报

```bash
python3 ~/.openclaw/skills/daxiang-daily-report/scripts/daxiang_daily_report.py
```

### 2. 生成指定日期的日报（测试用）

```bash
python3 ~/.openclaw/skills/daxiang-daily-report/scripts/daxiang_daily_report.py --date 20260309
```

### 3. 设置定时任务（每天早上6点自动执行）

```bash
# 编辑crontab
crontab -e

# 添加以下行
0 6 * * * /Users/hongfei/.openclaw/skills/daxiang-daily-report/scripts/run_daxiang_report.sh
```

---

## 📖 使用方法

### 命令行参数

| 参数 | 说明 | 示例 |
|:-----|:-----|:-----|
| 无参数 | 生成昨天的日报 | `python3 daxiang_daily_report.py` |
| `--date YYYYMMDD` | 生成指定日期的日报 | `python3 daxiang_daily_report.py --date 20260309` |

### 通过 OpenClaw 触发

当您在对话中提到以下关键词时，OpenClaw 会自动触发日报生成：

- "大象日报"
- "沟通日报"
- "daxiang daily"
- "report"

### 生成报告示例

```bash
$ python3 ~/.openclaw/skills/daxiang-daily-report/scripts/daxiang_daily_report.py

=== 大象沟通日报生成任务开始 ===
执行时间: 2026-03-13 06:00:01
报告已生成: /Users/hongfei/.openclaw/workspace-taizi/data/daxiang_20260312_v1.md
=== 大象沟通日报生成任务完成 ===
```

---

## ⏰ 定时任务设置

### 方式一：使用 Crontab

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天早上6点执行）
0 6 * * * /Users/hongfei/.openclaw/skills/daxiang-daily-report/scripts/run_daxiang_report.sh >> /tmp/daxiang_report.log 2>&1
```

### 方式二：使用 OpenClaw Cron

OpenClaw 内置了定时任务功能，可以通过配置 `~/.openclaw/cron` 来设置：

```json
{
  "jobs": [
    {
      "skill": "daxiang-daily-report",
      "schedule": "0 6 * * *",
      "enabled": true
    }
  ]
}
```

### 定时任务日志

日志文件位置：`/tmp/daxiang_report.log`

---

## 📁 报告输出说明

### 输出路径

报告文件保存在：`~/.openclaw/workspace-taizi/data/daxiang_YYYYMMDD_v1.md`

例如：
- 2026年3月12日的报告：`~/.openclaw/workspace-taizi/data/daxiang_20260312_v1.md`

### 报告结构

```
📊 YYYY年MM月DD日大象沟通汇总分析
├── 一、今日数据概览
│   └── 个人对话数、群聊数、系统通知数、消息总数
├── 二、时间精力分布
│   ├── 上午时段（9:00~14:00）
│   ├── 下午时段（14:00~19:00）
│   ├── 晚间时段（19:00~23:00）
│   └── 凌晨时段（23:00~次日凌晨9:00）
├── 三、单人沟通分析
│   ├── 关键对话1（星级评分、主题、主要沟通内容、一句话洞察）
│   ├── 关键对话2
│   └── ...
├── 四、群聊汇总
│   ├── 群1统计（消息数、@我次数、主题、群聊摘要）
│   ├── 群2统计
│   └── ...
├── 五、整体洞察
│   ├── 沟通重心
│   ├── 协同场域
│   ├── 时间投入
│   └── 待办压力
└── 六、todo清单
    └── 待办事项、来源、时间、备注
```

### 报告预览

```markdown
# 📊 2026年3月12日大象沟通汇总分析

---

## 📈 一、今日数据概览

| 指标 | 数值 |
|:-----|-----:|
| 个人对话 | **17 人** |
| 活跃群聊 | **17** |
| 系统通知 | **1** |
| 消息总数 | **495 条** |

---

## ⏰ 二、时间精力分布

### ☀️ 上午时段（9:00~14:00）

| 沟通对象 | 类型 | 消息数 | 主要沟通方向和内容 |
|:---------|:-----|-------:|:------------------|
| **孙文琼** | 个人 | 16 | 中午约人了吗；那一期吃饭，哈哈 |
| **吴昱** | 个人 | 15 | 你说这事怎么办？... |

> 📝 **时段总结**: 上午以 **孙文琼** 为最活跃沟通对象

### 🌤️ 下午时段（14:00~19:00）
> （暂无数据）

---

## 🗣️ 三、单人沟通分析

### ⭐⭐⭐⭐⭐ 孙文琼（44条）

- **主题**: AI/工具协作
- **对话背景**: 为撒点赞；哈哈哈
- **沟通要点**: 为撒点赞
- **角色洞察**: 孙文琼在"AI/工具协作"上呈现高频对齐

| 时间 | 说话人 | 具体内容 |
|:-----|:-------|:---------|
| 07:04 | 孙文琼 | 为撒点赞 |
| 07:05 | 你 | 怎么了 |
| ... | ... | ... |

---

## 💬 四、群聊汇总

| 群名 | 消息数 | @我次数 | 主题 | 群聊摘要 |
|:-----|-------:|--------:|:-----|:---------|
| **1024 Agent用户群②** | 69 | 0 | AI/工具协作 | ... |

---

## 💡 五、整体洞察

- **沟通重心**: 单人沟通以 **孙文琼** 最活跃
- **协同场域**: 群聊中 **1024 Agent用户群②** 最活跃
- **时间投入**: **下午** 是消息峰值时段
- **待办压力**: 共识别出 **8** 条潜在待办

---

## ✅ 六、todo清单

| 待办事项 | 来源 | 时间 | 备注 |
|:---------|:-----|:-----|:-----|
| 青云-业务反馈问题... | **青云研发群** | 09:50 | AI/工具协作 |
| 会议ID... | **未来编码实验室** | 10:06 | 行政流程 |
```

---

## ⚙️ 配置说明

### 主要配置项

在 `scripts/daxiang_daily_report.py` 中可以修改以下配置：

```python
# 技能目录
SKILL_DIR = "/Users/hongfei/.openclaw/skills/daxiang-daily-report"

# 工作空间目录
WORKSPACE = "/Users/hongfei/.openclaw/workspace-taizi"

# 数据存储目录
DATA_DIR = f"{WORKSPACE}/data"

# 报告输出目录
REPORT_DIR = f"{DATA_DIR}"
```

### 报告文件名格式

默认格式：`daxiang_YYYYMMDD_v1.md`

- `YYYYMMDD`：日期（如 20260312）
- `v1`：版本号

---

## 🔧 故障排除

### 问题1：报告生成失败

**症状**：运行脚本时提示错误

**排查步骤**：
1. 检查 Python 版本：`python3 --version`（需 3.8+）
2. 检查目录权限：`ls -la ~/.openclaw/workspace-taizi/data/`
3. 查看错误日志

### 问题2：无法获取大象数据

**症状**：报告内容为空

**原因**：当前版本需要通过浏览器手动获取大象数据

**解决方案**：
1. 打开大象网页版：https://x.sankuai.com/
2. 手动导出聊天记录
3. 或配置 DX CLI 自动获取

### 问题3：定时任务不执行

**症状**：cron 任务没有运行

**排查步骤**：
1. 检查 cron 服务是否运行：`ps aux | grep cron`
2. 检查 crontab 配置：`crontab -l`
3. 查看系统日志：`tail -f /var/log/syslog`

---

## 📝 版本历史

| 版本 | 日期 | 说明 |
|:-----|:-----|:-----|
| **V19** | 2026-03-18 | 完整沟通记录展示：去掉对话回溯，改用完整表格（时间\|说话人\|具体内容），完整展示所有消息 |
| **V18** | 2026-03-13 | 当前版本，6大板块完整输出（数据概览、时间精力分布、单人沟通分析、群聊汇总、整体洞察、todo清单） |
| **V7** | 2026-03-13 | 优化报告结构和格式 |
| **V6** | 2026-03-06 | 初始版本，基础功能实现 |

---

## 📞 支持

- **Issue**: https://github.com/openclaw/openclaw/issues
- **文档**: https://openclaw.com/docs

---

## 🔗 相关链接

- [大象官网](https://x.sankuai.com/)
- [OpenClaw 官网](https://openclaw.com)
- [美团内部文档](https://wiki.sankuai.com)

---

*本 skill 由 OpenClaw 提供支持*
