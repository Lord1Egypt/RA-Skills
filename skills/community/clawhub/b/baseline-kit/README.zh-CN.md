# Baseline Kit

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> 一个用于生成和审计 OpenClaw 配置基线的工具，帮助团队从更安全的默认值开始。

| 项目 | 内容 |
| --- | --- |
| 包名 | `@mike007jd/openclaw-baseline-kit` |
| 运行环境 | Node.js 18+ |
| 接口形态 | CLI + JavaScript 模块 |
| 主要命令 | `generate`、`audit` |

## 为什么需要它

很多 OpenClaw 事故其实不是代码问题，而是配置问题。Baseline Kit 的作用是先提供更安全的基线配置，再对现有配置文件做离线审计，找出网络暴露、控制缺失和明显的密钥卫生问题。

## 它能做什么

- 为 `development`、`team`、`enterprise`、`airgapped` 生成配置基线
- 输出可直接 review 的 JSON 文件
- 审计已有的 `openclaw.json` 风格配置
- 标记认证限流缺失、来源放得过宽、审计日志缺失等问题
- 将问题关联到 SOC2、ISO27001、NIST CSF 等合规标签组

## 典型工作流

1. 根据环境生成一个合适的 profile。
2. review 并提交生成出的 JSON。
3. 在上线前或变更后审计现有配置。
4. 根据 findings 收紧暴露面、日志和来源控制。

## 快速开始

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/baseline-kit
npm install
node ./bin/baseline-kit.js generate --profile enterprise --out /tmp/openclaw.json
node ./bin/baseline-kit.js audit --config ./fixtures/insecure-openclaw.json
```

## 命令说明

| 命令 | 作用 |
| --- | --- |
| `baseline-kit generate --profile <development|team|enterprise|airgapped> --out <path>` | 生成一份基线 JSON 配置 |
| `baseline-kit audit --config <path>` | 审计一份已有配置文件 |

## Profiles

| Profile | 侧重点 |
| --- | --- |
| `development` | 面向本地开发速度，保留更轻的限流与保留期 |
| `team` | 面向小团队共享环境的默认值 |
| `enterprise` | 更严格的认证窗口、更长的审计保留期和恢复提示 |
| `airgapped` | 偏向 loopback-only 与本地镜像来源 |

## 审计覆盖面

- Gateway 绑定地址与网络暴露
- 认证限流配置是否完整
- Skill 来源限制是否合理
- 审计日志是否开启
- 备份提示是否存在
- 配置树中是否含有疑似 secret 值

## 项目结构

```text
baseline-kit/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 当前状态

Baseline Kit 当前聚焦于 JSON 配置生成与离线审计。它更适合作为起步基线和策略 lint 工具，而不是完整的配置管理平台。
