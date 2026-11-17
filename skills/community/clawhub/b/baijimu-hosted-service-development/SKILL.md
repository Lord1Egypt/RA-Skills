---
name: baijimu-hosted-service-development
description: 使用 `baijimu` CLI 开发和部署 Hosted Service 后端，包括独立 Project/Git、Rust BuildJob、统一 Artifact 目录、数据库迁移 Artifact、Environment、Slot、Deployment、Endpoint、配置和服务鉴权。用于普通后端应用交付；不用于 Bundle/Module 生命周期、平台服务发布或基础设施变更。
version: 1.6.1
author: Baijimu
license: MIT-0
platforms: [openclaw, hermes]
metadata:
  openclaw:
    requires:
      bins: [baijimu]
    install:
      - kind: node
        package: "@baijimu/cli"
        bins: [baijimu]
    homepage: https://github.com/momoplan/baijimu-platform-skill
  hermes:
    tags: [baijimu, lowcode, automation, cli]
    requires_toolsets: [terminal]
---

# 百积木 Hosted Service 后端开发

Hosted Service 是托管构建与运行能力，不是独立产品资源。Project 是后端应用唯一身份；Environment、
Deployment、Endpoint、配置、鉴权和迁移执行都通过真实 `projectId` 关联，不存在并列的
`hostedServiceId`。

## 开始前

1. 先使用 `$baijimu-platform` 完成 CLI 版本、认证、工作区、Project 和 Git 分支策略确认。
2. 运行 `baijimu capabilities --offline --json`（旧版不支持时使用各级 `--help`），读取与本机版本绑定的
   命令结构和官方文档入口。
3. 打开 <https://docs.baijimu.com/development/backend-development/>；构建、迁移和部署参数以本机
   `baijimu rust-build --help`、`baijimu hosted-service --help` 及固定版本文档为准。

固定版本文档缺失或帮助中没有目标参数时，报告版本不匹配，不得直接调用内部服务、借用其他版本参数或
改走 Jenkins。

## 所有权边界

- `project-service` 拥有 Project、文件和 Git。
- `rust-build-service` 从 Project 的完整 Git commit 创建 BuildJob，并在构建成功后向 `artifact-service`
  登记不可变运行/迁移 Artifact。
- `artifact-service` 拥有统一 Artifact 目录、workspace/Project 归属及 Artifact 查询；CLI 把查询放在
  `rust-build artifact` 命令组下只是工作流分组，不改变服务所有权。
- `db-service` 拥有 Database Instance、Logical Database、Profile、Allocation 和连接配置解析。
- Hosted Service 能力拥有 Project Environment、Deployment、Endpoint、配置/鉴权绑定和数据库迁移
  Operation/Attempt；它只消费已有 `artifactId`，不在部署时构建。
- Bundle、Module、App Runtime、`baijimu-agent`、Control Plane、`release-control` 和 Rules 不参与 Hosted
  后端数据库迁移或部署。

## 构建与部署

1. 提交源码并取得完整 Git commit ID。
2. 用该 commit 创建运行 BuildJob；成功后从统一 Artifact 目录读取真实 `artifactId`，不要把
   `buildJobId` 当制品。
3. 创建或读取 Project Environment，按需绑定 Slot、Logical Database 和配置 Provider。
4. 部署明确的运行 Artifact；部署后查询 deployment，验证 Endpoint、健康、鉴权和真实业务请求。

同一个运行 Artifact 应能部署到多个 Environment。环境差异、密钥、数据库连接和第三方凭据必须来自
Environment 或 Config Provider，不能打进 Artifact。

## 数据库迁移

完整协议见 <https://docs.baijimu.com/development/backend-development/database-migrations/>。

- Schema 使用 `liquibase_bundle`；Data 使用一个或多个有序 `data_migration_bundle`。
- 运行、Schema 和 Data Artifact 必须属于同一 workspace、同一 Project，并来自同一个非空完整
  `sourceCommitId`。
- 部署请求最多携带一个 Schema Artifact 和按参数出现顺序执行的多个 Data Artifact。
- Hosted Service 在目标 Allocation 上按 Schema → Data 串行迁移，全部成功后才部署运行 Artifact 和切换
  Endpoint。
- Deployment 中的 Migration Operation 和只追加 Attempt 是状态源；请求被接受不代表迁移成功。
- 迁移失败不会自动反向已提交的数据库变更。应用必须采用 expand/contract 和向前恢复，不能把程序
  Artifact 回滚误认为数据库回滚。

不得在应用启动脚本、Bundle 安装钩子、Agent、Jenkins 或手工生产 SQL 中补跑标准迁移。

## 完成标准

BuildJob 成功且返回预期 Artifact；所有 Artifact 的 workspace、Project、类型和精确 commit 一致；迁移
Operation/Attempt、Deployment、Endpoint、健康检查、服务鉴权和业务请求全部通过。任何失败都从对应
owner 的公开状态源继续定位，不增加跨边界兜底或隐藏失败。
