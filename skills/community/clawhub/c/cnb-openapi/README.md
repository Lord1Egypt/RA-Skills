[![Version](https://img.shields.io/badge/version-1.18.8-blue)](https://api.cnb.cool)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<a href="https://www.codebuddy.cn/"><img src="https://img.shields.io/badge/AI-Code%20Assist-EB9FDA"></a>

> 该 skills 由 [cnb-sdk-generator](https://cnb.cool/cnb/sdk/cnb-sdk-generator) 生成

# CNB OpenAPI Skills

一个用于与 CNB (Cloud Native Build) Open API 交互的技能包，提供完整的代码管理和开发协作功能。

## 功能特性

- 🚀 **完整 API 覆盖** - 支持 CNB 平台所有 API 接口
- 📝 **详细文档** - 每个 API 都有完整的使用说明和示例
- 🔐 **安全认证** - 基于 Bearer Token 的身份验证
- 🛠️ **开发友好** - 结构化的接口文档，便于集成和使用

## 快速开始

### 设置环境变量

#### Linux/Mac

```bash
export CNB_TOKEN="your_cnb_token_here"
# 可选：自定义 API 地址（默认为 https://api.cnb.cool）
export CNB_API_ENDPOINT="https://api.cnb.cool"
```

#### Windows

```powershell
$env:CNB_TOKEN = "your_cnb_token_here"
# 可选：自定义 API 地址（默认为 https://api.cnb.cool）
$env:CNB_API_ENDPOINT = "https://api.cnb.cool"
```

### 使用

- [作为 NPM 包使用](./docs/node.md)
- [作为 Golang Package 使用](./docs/go.md)
- [在 CodeBuddy 中使用](./docs/codebuddy.md)
- [在 Claude Code 中使用](./docs/claudecode.md)
- [在 OpenClaw 中使用](./docs/openclaw.md)

## API 服务分类与文档结构

```
references/
├── activities/      # 活动统计 - 用户和仓库活动数据
├── ai/             # AI 功能 - AI 辅助开发功能
├── assets/         # 资产管理 - 项目资产和文件管理
├── badge/          # 徽章系统 - 项目徽章管理
├── build/          # 构建系统 - CI/CD 构建相关功能
├── charge/         # 计费系统 - 费用和计费查询
├── event/          # 事件系统 - 系统事件和通知
├── followers/      # 关注系统 - 用户关注和粉丝管理
├── git/            # Git 管理 - 分支、标签、提交等 Git 操作
├── gitsettings/    # Git 设置 - 合并请求设置、分支保护等
├── issues/         # 问题管理 - Issue 创建、查询、更新等
├── knowledgebase/  # 知识库 - 知识库查询和管理
├── members/        # 成员管理 - 项目成员和权限管理
├── missions/       # 任务系统 - 任务和项目管理
├── organizations/  # 组织管理 - 组织信息和设置
├── pulls/          # 合并请求 - Pull Request 相关操作
├── registries/     # 镜像仓库 - 容器镜像仓库管理
├── releases/       # 发布管理 - Release 和版本管理
├── repocontributor/ # 仓库贡献 - 贡献者统计分析
├── repolabels/     # 仓库标签 - 标签创建和管理
├── repositories/   # 仓库管理 - 仓库信息和设置管理
├── security/       # 安全管理 - 安全扫描和报告
├── starring/       # 收藏功能 - 仓库收藏和关注
├── users/          # 用户系统 - 用户信息和配置
└── workspace/      # 工作空间 - 开发环境和工作空间
```

## 技能文档

完整的技能说明请查看 [SKILL.md](./SKILL.md) 文件。

## 许可证

本项目遵循相应的开源许可证。
