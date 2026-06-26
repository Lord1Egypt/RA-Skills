# CostLens

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> 一个面向 OpenClaw 工作流的 token 成本监控 CLI，把原始使用事件转成带预算感知的成本摘要。

| 项目 | 内容 |
| --- | --- |
| 包名 | `@mike007jd/openclaw-costlens` |
| 运行环境 | Node.js 18+ |
| 接口形态 | CLI + JavaScript 模块 |
| 主要命令 | `monitor`、`report`、`budget check` |

## 为什么需要它

Token 成本问题往往在工作流已经放大之后才暴露出来。CostLens 的作用就是更早把花费显性化：它会汇总模型使用量、计算成本、检查预算阈值，并把事件流整理成运维可读的输出。

## 它能做什么

- 读取包含 prompt / completion token 数的 JSON 事件数组
- 使用内置模型费率，也支持按事件覆盖费率
- 按模型、按日期汇总成本
- 安全跳过非法事件，并明确说明跳过了什么
- 检查预算使用率并给出 warning / critical 状态
- 导出结构化报告，便于交接或审计

## 典型工作流

1. 从工作流日志导出 token 事件。
2. 使用 `costlens monitor` 查看快速运行摘要。
3. 加上 `--budget` 和 `--threshold` 做预算守护。
4. 用 `costlens report` 输出正式报告文件。

## 快速开始

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/costlens
npm install
node ./bin/costlens.js monitor --events ./fixtures/events.json --budget 0.1 --threshold 75
```

## 命令说明

| 命令 | 作用 |
| --- | --- |
| `costlens monitor --events <path>` | 输出快速摘要表格或 JSON |
| `costlens report --events <path> --out <path>` | 保存完整 JSON 报告 |
| `costlens budget check --events <path> --budget <amount>` | 返回预算状态，并在严重超支时给出关键退出码 |

## 事件格式

```json
{
  "model": "gpt-4.1",
  "promptTokens": 1200,
  "completionTokens": 300,
  "timestamp": "2026-03-10T10:00:00Z"
}
```

## 输出行为

- `monitor` 在正常或 warning 状态下返回 `0`，在严重超预算时返回 `2`
- `report` 会写出包含总量、按模型拆分、按日期拆分和预算状态的 JSON 文件
- 非法事件会被跳过，而不是直接让整次执行失败

## 项目结构

```text
costlens/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 当前状态

当前实现适合离线事件分析，内置了常见模型费率和预算判断能力。它是一个实用的成本报告层，而不是实时计费系统。
