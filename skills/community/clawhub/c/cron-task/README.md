# cron-task

[![Stars](https://img.shields.io/github/stars/EdwardWason/cron-task?style=flat-square)](https://github.com/EdwardWason/cron-task)
[![许可证](https://img.shields.io/badge/license-MIT--0-green?style=flat-square)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-cron--task-orange?style=flat-square)](https://clawhub.ai/skills/cron-task)
[![Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue?style=flat-square)](SKILL.md)

🌍 English version: [README.en.md](README.en.md)

_「调试完了，说一句话，还你一个每天自动跑、9项就绪检查、三端归档、飞书卡片提醒的定时任务。」_

**cron-task** 不是又一个任务编排器，是从"调试完成"到"稳定每日运行"的最后一公里自动化。

[看效果](#示例) · [装上就能用](#30-秒开始) · [核心机制](#核心特性) · [已知限制](#已知限制) · [License](#license)

## 30 秒开始

```bash
# ClawHub 安装
clawhub install cron-task

# 或 GitHub 克隆
git clone https://github.com/EdwardWason/cron-task.git
```

安装后，在任务/技能调试接近完成时说：**"创建定时任务"**

## 核心特性

- **9项就绪检查** — 脚本独立性/环境变量/数据源/IM凭证/归档路径/幂等性/回退链路/调度频率/输出质量，任一项未过先报告不硬创
- **执行器脚本生成** — 自动生成可独立运行的 Python 脚本，含环境检查+主逻辑+三端归档+IM通知
- **Schedule 提示词撰写** — 自包含的 Schedule message，含执行命令+失败回退+归档指令+IM提醒要求
- **三端归档** — 飞书云盘 + Obsidian inbox + IMA知识库（两步API），统一 Markdown + YAML 元数据头
- **飞书 IM 卡片** — 通过 lark-im skill 发送 Interactive Card，含任务名/状态/摘要/详情链接

## 适合 / 不适合

### 适合
- 数据抓取/分析项目调试完成，需要转为每日自动运行
- 技能开发完成，需要定期执行并推送结果
- 多步骤工作流，需要定时触发并归档结果

### 不适合
- 一次性脚本执行
- 手动触发的任务
- 非周期性工作流
- Cron 故障诊断（用 cron-doctor 代替）

## 示例

```
用户: 创建定时任务

AI: [扫描上下文...]
    [执行9项就绪检查...]

## 就绪检查报告
| # | 检查项 | 状态 | 说明 |
|---|--------|------|------|
| 1 | 脚本可独立运行 | ✅ | executor.py 测试通过 |
| 5 | 归档路径存在 | ⚠️ | 飞书云盘文件夹待确认 |

⚠️ #5: 飞书云盘文件夹未指定
→ 建议: 使用 lark-drive 创建文件夹

[用户确认补全后...]

✅ 脚本已生成: scripts/clawhub_daily_executor.py
✅ Schedule 提示词已撰写
✅ Schedule 任务已创建 (cron: 0 9 * * *, timezone: Asia/Shanghai)
```

## 目录结构

```
cron-task/
├── SKILL.md                          # Agent 工作流定义
├── references/
│   ├── readiness-checklist.md        # 9项就绪检查详细方法论
│   ├── schedule-prompt-template.md   # Schedule message 提示词模板
│   └── archiving-guide.md            # 三端归档指南
├── assets/
│   ├── executor_template.py          # 执行器脚本模板
│   └── metadata_header.md            # 归档元数据头模板
├── README.md                         # 中文文档
├── README.en.md                      # 英文文档
├── CHANGELOG.md                      # 版本记录
├── LICENSE                           # MIT-0
└── .gitignore
```

## 核心设计原则

1. **就绪才创建** — 9项检查不过不创建任务，先报告缺失要素。避免"创建了但跑不起来"
2. **脚本自包含** — 生成的执行器不依赖会话上下文，agent 在调度时可直接调用
3. **归档不中断** — 任一端归档失败只记录日志，不中断主流程
4. **IM 只用飞书** — 通过 lark-im skill 发卡片，不混用通道

## 已知限制

- **TRAE Schedule 限制**：最小间隔 10 分钟，不支持秒级，只支持 5 字段 cron 格式
- **飞书 IM 为主**：当前只支持飞书 Interactive Card，邮件/微信为未来扩展
- **需预配置环境变量**：FEISHU_APP_ID/SECRET/USER_OPEN_ID、IMA 凭证需提前配置
- **Python 3.10+**：执行器脚本使用现代 Python 特性
- **Windows 优先**：在 Windows + PowerShell 5.1 测试，Linux/macOS 可能需调整路径

## License

MIT-0 © 2026 EdwardWason
