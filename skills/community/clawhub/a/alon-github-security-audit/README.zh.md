[English](./README.md)

# Alon GitHub 安全审计 Skill

在默认不执行目标项目代码的前提下，对 GitHub 仓库或本地代码目录进行恶意代码、后门和供应链风险审计。

## 快速安装

```bash
npx skills add alondotsh/alon-skills --skill alon-github-security-audit
```

## 适用场景

适合用于：

- 安装或信任一个 GitHub 仓库前先做安全审查
- 对本地代码库做恶意行为排查
- 审查 agent skill、自动化工具或安装脚本
- 在进一步深入分析前先做静态优先的安全评估

典型触发语：

- `审计下 https://github.com/owner/repo`
- `审计当前目录`
- `audit this repo`
- `check repo security`

## 核心能力

- 默认执行离线静态审计
- 检查网络指纹、数据外传路径、混淆内容与安装链
- 检查目标仓库是否会修改 `USER.md`、`MEMORY.md`、`AGENTS.md`、`SOUL.md`、`IDENTITY.md`、`SKILL.md` 等长期 agent 控制文件；对 agent、skill、自动化仓库做更深一层的复核
- 区分潜在使用者的主安全结论、开发者暴露、未来供应链风险
- 输出 lockfile、浮动版本、需要关注的依赖包、已知高风险版本等供应链细节
- 对 skill 和自动化工具增加来源与权限预检
- 经用户确认后可补充联网依赖漏洞情报检查
- 输出结构化审计报告，写入本地报告目录，便于归档和复查

## 安全边界与限制

- 默认模式是只读静态分析
- 默认分析范围只限于目标仓库或当前工作目录
- 不执行目标仓库代码
- 不运行 `npm install`、`pip install` 等安装命令
- 未经用户明确同意，不访问外部漏洞情报源
- 未经用户明确扩展范围，不读取 `~/.ssh`、浏览器资料目录等无关 home 路径
- 对本地目录审计时不会删除用户文件

这个 skill 适合做审计和分诊，不负责证明运行时漏洞是否可利用。

## 输出结果

审计结果通常包括：

- 高危实体清单
- 逻辑风险分析
- 持久状态修改面，包括触及文件、写入机制、操作者确认、未来会话影响、用途匹配
- `Capability`、`Identity`、`Knowledge` 三类 CIK 风险归类
- 开发者暴露：`Low`、`Medium`、`High` 或 `Critical`
- 供应链风险：`Low`、`Medium`、`High` 或 `Critical`，必要时列出具体依赖包
- 补充安全检查结果
- 面向潜在使用者的主结论：`Safe`、`Risky` 或 `Dangerous`
- 写入本地报告目录的审计报告

## 项目结构

```text
alon-github-security-audit/
├── SKILL.md
├── README.md
├── README.zh.md
├── docs/
│   ├── audit-standard.md
│   └── post-audit-review-checklist.md
└── tools/
    ├── clone_repo.py
    └── cleanup.py
```

## 本地开发说明

- Python 3.6+
- Git

这个目录是私有 canonical source，可以保留宿主相关和个人工作流相关细节。真正公开发布时，再做 public-safe 导出和清洗。

当前私有工作流中，报告先写入本地报告目录，后续如需进入 Obsidian，再由单独工具链处理。

## 关于 Alon

这些公开 skills 来自 Alon 日常高频使用的真实工作流。

我长期看好 agent skills，也愿意和对 skill 制作感兴趣的人交流。

- GitHub：https://github.com/alondotsh
- ClawHub：https://clawhub.ai/u/alondotsh
- X：https://x.com/alondotsh
- 公众号：alondotsh

## License

MIT
