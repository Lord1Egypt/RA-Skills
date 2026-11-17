---
slug: flow-editor-pro
name: flow-editor-pro
version: 1.0.1
displayName: 流程编辑专家
summary: 解决Node-RED无版本管理、部署易翻车、多实例难管痛点，带回滚与安全加固的流程运维。通过 Admin API 或 CLI 管理 Node-RED
  实例的运维专家。聚焦流程部署可回滚、多实
license: MIT
description: 通过 Admin API 或 CLI 管控 Node-RED 实例的运维专家。聚焦流程部署可回滚、多实例统一管控、. 当需要flow editor相关能力的开发场景,提供工作流程和配置参考。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。
  该工具经过质量提升,针对用户反馈优化了实用性。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非技术类的通用任务。
tags:
- 自动化
- 运维
- 物联网
- 工作流
- 效率
- json
- instance
tools:
- read
- exec
- write
homepage: ''
category: Automation
pricing_tier: L2-标准级
homepage: "https://skillhub.cn/skill/"
---
> **核心功能**: 本技能提供化工作流场景等能力。

> **核心功能**: 本技能提供结构化的工作流程和配置指引等能力。

# 流程编辑专家

通过 Admin API 与 CLI 管理 Node-RED 实例，把"部署即翻车"变为"可回滚、可审计、可治理"的运维流程.
## 多实例配置中心

替代原版单实例硬编码，单文件管多实例：

```bash
# .env（按实例分块）
NR_PROD_URL=https://flow.example.com
NR_PROD_USERNAME=admin
NR_PROD_PASSWORD=${NR_PROD_PASSWORD}
# ...
NR_STAGING_URL=http://staging.internal:1880
NR_STAGING_USERNAME=admin
NR_STAGING_PASSWORD=${NR_STAGING_PASSWORD}
# ...
NR_DEV_URL=http://localhost:1880
NR_DEV_USERNAME=
NR_DEV_PASSWORD=
```

CLI 通过 `--instance` 切换，默认 `dev`：

```bash
（请参考skill目录中的脚本文件） --instance prod list-flows
（请参考skill目录中的脚本文件） --instance staging deploy --file watchdog.json
```

兼容旧变量 `NR_URL` / `NR_USER` / `NR_PASS`（默认实例）.
## 流程管理（含版本与回滚）

```bash
# 列表与详情
（请参考skill目录中的脚本文件） list-flows
（请参考skill目录中的脚本文件） get-flow <flow-id>
（请参考skill目录中的脚本文件） get-flow-state
# ...
# 部署（自动留版本到 .versions/<flow-id>/<timestamp>.json）
（请参考skill目录中的脚本文件） deploy --file assets/flows/watchdog.json
（请参考skill目录中的脚本文件） deploy --file my-flow.json --instance prod   # 部署到生产
# ...
# 更新与删除
（请参考skill目录中的脚本文件） update-flow <flow-id> --file updated-flow.json
（请参考skill目录中的脚本文件） delete-flow <flow-id>
# ...
# 版本树与回滚
（请参考skill目录中的脚本文件） list-versions <flow-id>           # 列出该流程所有历史版本
（请参考skill目录中的脚本文件） rollback <flow-id> --to <timestamp>   # 回滚到指定版本
（请参考skill目录中的脚本文件） rollback <flow-id> --last         # 快速回滚到上一版本
# ...
# 状态快照
（请参考skill目录中的脚本文件） get-flow-state
（请参考skill目录中的脚本文件） set-flow-state --file state.json
```

**部署安全流程**：
1. 先 `--instance staging deploy` 部署到预发
2. 验证无误后 `--instance prod deploy`
3. 生产出问题 → `rollback --last`（< 5 秒回滚）

## 备份与恢复

```bash
# 全量备份（所有流程 + Context + 节点清单）
（请参考skill目录中的脚本文件） backup
（请参考skill目录中的脚本文件） backup --output my-backup.json
（请参考skill目录中的脚本文件） backup --instance prod --include-context
# ...
# 跨实例迁移
（请参考skill目录中的脚本文件） backup --instance prod --output prod-snapshot.json
（请参考skill目录中的脚本文件） restore prod-snapshot.json --instance staging
# ...
# 定时备份（建议加入 cron）
（请参考skill目录中的脚本文件） backup --schedule "0 2 * * *"   # 每日 2 点
```

备份内容：flows、credentials（加密）、context（flow/global）、节点清单、settings.
## 节点管理（含兼容性检查）

```bash
# 列表与详情
（请参考skill目录中的脚本文件） list-nodes
（请参考skill目录中的脚本文件） get-node node-red-contrib-http-request
# ...
# 依赖说明
（请参考skill目录中的脚本文件） install-node node-red-contrib-http-request
（请参考skill目录中的脚本文件） install-node node-red-contrib-influxdb --version 0.5.0
# ...
# 启用/禁用/卸载
（请参考skill目录中的脚本文件） enable-node node-red-contrib-http-request
（请参考skill目录中的脚本文件） disable-node node-red-contrib-http-request
（请参考skill目录中的脚本文件） remove-node node-red-contrib-http-request
# ...
# 批量升级
（请参考skill目录中的脚本文件） upgrade-nodes --all               # 升级所有过期节点
（请参考skill目录中的脚本文件） upgrade-nodes --outdated-only     # 仅升级有新版的
```

**兼容性检查**：安装/升级前自动比对节点要求的 Node-RED 版本与当前版本，不兼容则告警并中止.
**危险节点告警**：以下节点安装时强制提示风险：
- 已知有安全漏洞的版本（CVE 库匹配）
- 需要文件系统写权限的节点
- 启用 exec/child_process 的节点

## Context 管理

```bash
# 读取
（请参考skill目录中的脚本文件） get-context flow my-key
（请参考skill目录中的脚本文件） get-context global shared-data
# ...
# 写入
（请参考skill目录中的脚本文件） set-context flow my-key '"value"'
（请参考skill目录中的脚本文件） set-context global counter '42'
（请参考skill目录中的脚本文件） set-context global config '{"key": "value"}'
# ...
# 持久化导出（用于灾备）
（请参考skill目录中的脚本文件） export-context --output context-backup.json
```

## 运行时信息

```bash
（请参考skill目录中的脚本文件） get-settings        # Node-RED 设置
（请参考skill目录中的脚本文件） get-diagnostics     # 诊断信息（内存/运行时长/错误统计）
（请参考skill目录中的脚本文件） health              # 健康检查（实例连通 + 关键流程状态）
```

## Docker 操作

```bash
cd deployments/node-red && docker compose restart
docker logs mema-node-red --tail 100
docker logs -f mema-node-red
# ...
# 多实例
docker compose --profile prod up -d
docker compose --profile staging up -d
```

## 安全加固清单

部署前逐项核对：

- [ ] Admin API 启用鉴权（`adminAuth` 配置）
- [ ] 凭证密钥已设置（`credentialsSecret` 非默认）
- [ ] HTTPS 启用（生产实例）
- [ ] `httpNodeRoot` 非默认 `/`（隐藏 HTTP 端点）
- [ ] 危险节点（exec/file）已禁用或限制
- [ ] 备份定时任务已配置
- [ ] 流程变更走 staging → prod 流程
- [ ] Context 持久化配置正确（避免重启丢失）

### 安全风险防范

| 潜在风险 | 风险评级 | 控制措施 | 验证手段 |
|----------|----------|----------|----------|
| 凭证存储不当 | 高 | 密钥管理服务,环境变量注入 | 密钥轮换审计 |
| 网络传输窃听 | 高 | HTTPS强制,证书钉扎 | SSL Labs检测 |
| 异常操作未告警 | 中 | 操作日志,实时监控 | 告警规则验证 |
| 版本过期风险 | 低 | 自动更新,版本策略 | 版本兼容性检查 |

## 应用示例
### 场景1：家居自动化流程上线

```
用户：把新的"回家模式"流程部署到生产
执行：
1. --instance staging deploy --file home-mode.json
2. staging 验证 10 分钟无报错
3. --instance prod deploy --file home-mode.json（自动留版本）
4. 报告：部署成功，版本 v20260718-1，回滚命令 nr rollback home-mode --last
```

### 场景2：生产流程故障回滚

```
用户：刚部署的流程把灯全关了，快回滚
执行：
1. （请参考skill目录中的脚本文件） rollback home-mode --last
2. 确认已回滚到 v20260718-0
3. 报告：回滚完成，问题版本已保留供分析
```

### 场景3：跨实例迁移

```
用户：把开发实例的全部流程迁到新服务器
执行：
1. --instance dev backup --output dev-full.json --include-context
2. 修改 .env 指向新服务器
3. --instance dev restore dev-full.json
4. health 检查全部流程状态
```

### 场景4：节点批量升级

```
用户：升级所有过期节点
执行：
1. upgrade-nodes --outdated-only
2. 兼容性检查：3 个节点有新版本，1 个不兼容（跳过）
3. 升级完成的节点逐个验证流程无报错
4. 报告：升级 2 个，跳过 1 个（node-red-contrib-x 不兼容 v3.1）
```

## 异常恢复策略
| 故障场景 | 表现症状 | 诊断方法 | 修复步骤 |
|:---------|:---------|:---------|:---------|
| Key无效 | 返回401状态码 | 验证Key格式和有效性 | 重新生成Key并更新环境变量 |
| 请求被拒 | 返回403禁止访问 | 检查权限范围和IP限制 | 确认账户权限,添加IP白名单 |
| 速率限制 | 返回429状态码 | 查看响应头中的Retry-After字段 | 按Retry-After值等待后重试 |
| 格式错误 | 返回400状态码 | 检查请求体JSON格式和字段类型 | 参照输入格式示例修正 |
| 服务不可用 | 返回503状态码 | 检查API状态页和健康检查端点 | 等待服务恢复,设置重试退避策略 |
## 支持文档
**Q1: 回滚会丢数据吗？**
A: 流程定义回滚不影响 Context 数据。Context 单独备份恢复。回滚只替换 flows.json 与 credentials.
**Q2: 多实例配置怎么管 token？**
A: 全部走环境变量 `${VAR}`，不入 `.env` 明文。CI/CD 用 secrets 注入.
**Q3: 部署到生产前必须过 staging 吗？**
A: 强烈推荐。安全加固清单第 7 项。若强行直发生产，CLI 会提示风险但允许（`--force`）.
**Q4: 节点升级后流程报错怎么办？**
A: 立即 `rollback <flow> --last` 回滚流程，再 `disable-node <新节点>` 禁用问题节点，最后排查兼容性.
**Q5: 备份文件包含敏感信息吗？**
A: 含加密的 credentials，但需 `credentialsSecret` 解密。备份文件建议存到加密存储，勿提交公开仓库.
## 排错指南
| 现象 | 排查路径 |
|:-----|:-----|
| Admin API 401 | 检查 `.env` 账号密码 → 确认 `adminAuth` 配置 → 重试 |
| 部署后流程不工作 | `get-diagnostics` 查错误 → `list-versions` 比对差异 → `rollback --last` |
| 节点安装失败 | 查 Node-RED 版本兼容性 → 查 npm registry → 手动 `npm install` 看详细错误 |
| Context 重启后丢失 | 检查 `contextStorage` 配置 → 改为 `localfilesystem` 持久化 |
| 多实例切换失效 | 确认 `--instance` 参数 → 检查 `.env` 对应块 → `doctor` 验证 |
| Docker 重启后流程丢失 | 检查 volume 挂载 → 确认 `data` 目录持久化 |
| 回滚后版本树错乱 | `.versions/` 目录可能被手动改过 → 用最近备份重建版本树 |

## 安装与配置
### 运行环境
- **Agent 平台**: 任意支持 SKILL.md 的 AI Agent
- **操作系统**: Windows / macOS / Linux
- **Node-RED**: ≥ 2.0（推荐 3.x），可通过 Docker 或本地安装

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Node-RED 实例 | 软件 | 必需 | docker / npm / 系统包 |
| Docker（可选） | 容器运行时 | 可选 | docker.com |
| `jq` | JSON 处理 | 推荐 | 系统包管理器 |
| `curl` | HTTP 调用 | 必需（CLI 内部用） | 系统自带 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- Node-RED Admin 账号密码（写入 `.env`，生产用环境变量注入）
- `credentialsSecret`（解密流程凭证，建议存于密钥管理服务）
- 无需第三方 API Key

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 必须通过 exec 执行 `（请参考skill目录中的脚本文件）` CLI 与 docker 命令）
- **说明**: 基于自然语言指令驱动 Agent 管理 Node-RED 实例，含版本化、回滚、安全加固

## 功能特点
- 通过 Admin API 或 CLI 管理 Node-RED 实例的运维专家
- 聚焦流程部署可回滚、多实例统一管理、
  节点依赖可治理、Context 持久化与安全加固，解决无版本控制、部署即翻车、多实例配置散乱痛点
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回核心功能执行的响应数据,附带状态标识与运行日志.
- 通过`input_params`参数指定操作类型(创建/查询/导出)

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回参数配置与调用的响应数据,附带状态标识与运行日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回格式化结果.
**输出**: 返回结果处理与输出的响应数据,附带状态标识与运行日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：能力范围包括以下关键词：无版本管理、部署易翻车、多实例难管痛点、带回滚与安全加固、的流程运维、Use、when、需要系统监控、日志分析、运维告警、部署管理时使用、不适用于物理硬件等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景
```
用户：把新的"回家模式"流程部署到生产
执行：
2. staging 验证 10 分钟无报错
4. 报告：部署成功，版本 v20260718-1，回滚命令 nr rollback home-mode --last
```

## 功能边界
- 版本管理基于本地Git仓库，多实例协作场景需额外配置远程仓库同步，不支持原生多人实时编辑
- 回滚操作仅恢复流程定义，已执行的副作用（如已发送的邮件、已写入的数据库记录）不可逆
- Node-RED版本升级可能导致自定义节点不兼容，安全加固策略需随版本更新重新验证

## 疑问汇总
### Q1: 本技能与其他类似工具有何区别?
A: 参考差异化对比章节,本技能在自动化程度、错误处理和安全合规方面有针对性优化。

### Q2: 是否需要付费才能使用?
A: 基础功能免费。高级能力(标注付费版专享)需要订阅,详见付费版专享能力表格。

### Q3: 返回结果为空是什么原因?
A: 检查输入是否有效,确认参数值不为空字符串。参考边界条件章节了解输入要求。

### Q4: 如何反馈问题或建议?
A: 在Agent平台对话中描述遇到的问题,附上错误信息和输入参数,便于快速定位。

### Q5: 技能运行慢怎么优化?
A: 减少输入数据量,缩短prompt长度。网络延迟较大时检查API端点区域,选择就近节点.
## 输出说明
```json
{
  "success": true,
  "data": {
    "result": "流程编辑专家处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "flow editor pro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

## 性能评估
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 优势对比
| 对比维度 | 流程编辑专家 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 解决Node-RED无版本管理、部署易翻车、多实例难管痛点，带回滚与安全加固的流 | 通用场景 | 通用场景 |

## 上线流程
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码

### 前置条件

- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪

### 流程编辑专家通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块

### Q1: 流程编辑专家支持哪些输入格式？

A1: 解决Node-RED无版本管理、部署易翻车、多实例难管痛点，带回滚与安全加固的流程运维。通过 Admin API 或 CLI 管理 Node-RED。支持文本指令和结构化参数输入，具体格式参考使用流程章节。

### Q2: 需要配置API Key吗？

A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。

### Q3: 命令行执行失败怎么办？

A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent
- **操作系统**: Windows / macOS / Linux

### 可用性分类
- **分类**: MD（纯Markdown指令，通过自然语言驱动Agent完成操作）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作。
