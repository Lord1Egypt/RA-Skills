---
name: baijimu-bundle-development
description: 使用 `baijimu` CLI 开发、冻结、审核、发布、安装、升级或卸载 Bundle，以及在 Bundle 内开发 Module、Skill、Agent 和平台应用资源。用于 Bundle-first 公开产品生命周期；不用于 Hosted Service 后端构建、数据库迁移或平台内部发布。
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

# 百积木 Bundle 开发

Bundle 是生态资源公开审核、市场分发和 Runtime 安装的唯一交付单元。Module 是 Bundle 内部资源，不能
独立审核、上架、安装或升级。数据库及 `databaseType` 不是 Module 声明，Hosted Service 数据库迁移也
不进入 Bundle。

## 开始前

1. 先使用 `$baijimu-platform` 完成 CLI 版本、认证、工作区和项目确认。
2. 运行 `baijimu capabilities --offline --json`（旧版不支持时使用各级 `--help`），读取与本机版本绑定的
   命令结构和官方文档入口。
3. 打开 <https://docs.baijimu.com/development/bundle-development/>；执行参数仍以固定版本入口和本机
   `baijimu <command> --help` 为准。

固定版本页面缺失时报告 CLI/文档版本不匹配，不得借用其他版本参数、旧独立 Module 流程或服务器内部 API。

## 产品不变量

- 模块源码项目可以独立存在；Module 定义必须在 Bundle 内创建。
- Module 冻结只生成不可变内部版本；Bundle Manifest 必须引用精确 Module 版本。
- Module 方法、类型和资源声明不拥有数据库。需要数据库的后端逻辑应放入独立 Hosted Service Project，
  数据库变更使用 `$baijimu-hosted-service-development`。
- HTTP 方法 `methodBody` 的可修改生产者必须按官方源契约写 `snake_case`。历史别名只允许在受控读取边界
  转换；规范字段与历史别名冲突时拒绝。
- 发布、审核、市场分发、安装、升级和卸载均以不可变 Bundle 版本为对象。
- 发布者和审核者是不同权限边界；不得用同一身份自行批准或修改服务器状态绕过审核。

## 完整工作流

修改 Bundle 或其资源时，完整执行
<https://docs.baijimu.com/development/bundle-development/change-and-release/>：

1. 读取当前 Bundle、Project Git、资源定义、精确版本和工作区权限。
2. 修改源码并验证差异、类型契约和引用闭包。
3. 提交 Project Git，创建模块版本、冻结所需资源不可变版本并更新 Manifest。
4. 发布不可变 Bundle 版本，回查工作区审核状态。
5. 提交并回查市场审核；人工审核未完成时只能报告“已提交”。
6. 在准确 Runtime 上安装或升级 Bundle。
7. 回查 Bundle installation、资源台账，并对真实 Runtime service/method 做端到端调用验证。

任何一步失败都保留原错误码、对象 ID 和状态源；不能用缓存态、独立 Module 安装、Rules 同步或手工数据库
修改替代 Bundle 生命周期。

## 完成标准

代码提交、不可变资源版本、Bundle 版本、审核、市场状态、目标 Runtime installation 和真实运行时调用必须
与请求目标一致。权限或人工审核阻塞时，准确停在对应阶段，不把“已冻结”“已提交”或“已安装”互相替代。
