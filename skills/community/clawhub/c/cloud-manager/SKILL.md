---
slug: "cloud-manager"
name: "cloud-manager"
version: 1.0.1
displayName: "云存储管家 专业版"
summary: "全功能云存储管理，支持多云统一视图、团队共享矩阵与自动化备份规则。"
license: "Proprietary"
edition: "pro"
description: |-
  Cloud Manager 专业版面向多设备用户与小团队，在免费版基础上解锁多云统一视图、家庭/团队共享权限矩阵、定时备份规则与存储深度分析。核心能力：跨盘统一文件视图、多云迁移向导、家庭/团队共享权限矩阵、定时备份与清理规则、存储用量深度报表、版本历史对比与去重、跨盘文件搜索。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理.
tags:
  - 集成工具
  - 云存储
  - 团队协作
  - 自动化
tools:
  - read
  - exec
homepage: "https://skillhub.cn"
# 定价元数据
suggested_price: "19.9 CNY/per_use"
pricing_tier: "L2-标准级"
pricing_model: "per_use"

---
# 云存储管家 专业版

## 付费版专享能力

| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| 云存储管家 专业版全功能云存储管理 | 不支持 | 支持 |
| 高清分辨率与无损输出 | 不支持 | 支持 |
| 批量生成与风格预设 | 不支持 | 支持 |
| 自定义模型微调 | 不支持 | 支持 |
| 商用版权授权 | 不支持 | 支持 |

## 核心能力

| 能力域 | 说明 | 专业版增强 |
|:-----|:-----|:-----|
| 多云统一视图 | 聚合多个云盘的文件列表与存储用量 | 专业版独有 |
| 跨盘迁移 | 云盘之间的文件迁移向导 | 专业版独有 |
| 家庭共享 | 家庭相册、共享文件夹、成员权限 | 专业版独有 |
| 团队协作 | 团队文档库、角色权限、版本控制 | 专业版独有 |
| 定时备份 | 配置自动备份规则与清理策略 | 专业版独有 |
| 存储分析 | 按类型/时间/所有者的深度报表 | 专业版独有 |
| 版本历史 | 文件版本对比与去重 | 专业版独有 |
| 跨盘搜索 | 跨多个云盘的统一文件搜索 | 专业版独有 |
| 选型决策 | 基于设备组合的选型矩阵 | 继承免费版 |
| 整理清理 | 存储清理步骤 | 继承免费版 |
| 安全基线 | 2FA、链接审计、敏感文件处理 | 继承免费版 |
### 能力域

针对能力域,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供能力域相关的配置参数、输入数据和处理选项.
**输出**: 返回能力域的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`能力域`的配置文档进行参数调优
### 多云统一视图

针对多云统一视图,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供多云统一视图相关的配置参数、输入数据和处理选项.
**输出**: 返回多云统一视图的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`多云统一视图`的配置文档进行参数调优
### 跨盘迁移

针对跨盘,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供跨盘迁移相关的配置参数、输入数据和处理选项.
**输出**: 返回跨盘迁移的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`跨盘迁移`的配置文档进行参数调优
#
## 适用场景

### 场景一：家庭多成员多设备统一管理（家庭管理员角色）

家庭成员分别使用 iPhone（iCloud）和 Android（Google Drive），照片散落在两个云盘。专业版提供多云统一视图：

```bash
# 添加云盘账户
cloud-manager account add --provider icloud --email "user@example.com"
cloud-manager account add --provider gdrive --email "user@gmail.com"
# ...
# 查看统一文件视图
cloud-manager files list --all-providers --sort-by date
# ...
# 查看存储用量聚合
cloud-manager storage summary --all-providers
```

### 场景二：家庭相册共享与权限控制（家庭管理员角色）

创建家庭相册共享文件夹，为不同成员设置不同权限：

```bash
# 创建家庭共享文件夹
cloud-manager share create --name "家庭相册" --type folder
# ...
# 邀请成员并设置权限
cloud-manager share invite --folder "家庭相册" \
  --member "spouse@example.com" --role editor
cloud-manager share invite --folder "家庭相册" \
  --member "child@example.com" --role viewer
# ...
# 查看共享权限矩阵
cloud-manager share matrix --folder "家庭相册"
```

### 场景三：小团队文档协作（团队管理员角色）

团队需要共享文档库，并按角色控制权限。专业版提供团队权限模型：

| 角色 | 权限 | 适用成员 |
|---:|---:|---:|
| owner | 全部权限（含删除、权限管理） | 团队负责人 |
| editor | 编辑、上传、下载、评论 | 核心成员 |
| contributor | 上传、下载、评论自己的文件 | 外部协作者 |
| viewer | 仅查看与下载 | 实习生/外部顾问 |

```bash
# 创建团队文档库
cloud-manager team create --name "产品文档库" --provider onedrive
# ...
# 批量设置成员权限
cloud-manager team members --library "产品文档库" --file members.csv
```

### 场景四：定时自动备份（注重数据安全的用户）

配置每日自动备份规则，无需手动触发：

```bash
# 配置每日照片自动备份
cloud-manager backup rule create \
  --source "~/Pictures" \
  --target "gdrive://Photos/$(date +%Y/%m)" \
  --schedule "daily 02:00" \
  --retain 90d
# ...
# 配置文档每周备份
cloud-manager backup rule create \
  --source "~/Documents" \
  --target "onedrive://Backup/Documents" \
  --schedule "weekly sunday 03:00" \
  --retain 12w
# ...
# 查看所有备份规则
cloud-manager backup rule list
```

### 场景五：存储用量深度分析（成本优化角色）

云盘存储成本上升，需要识别哪些文件占用空间并进行优化：

```bash
# 生成存储分析报表
cloud-manager storage analyze --provider all --format markdown --output report.md
# ...
# 按文件类型分析
cloud-manager storage analyze --group-by type --top 10
# ...
# 识别大文件
cloud-manager storage find --size ">500MB" --older-than "180d"
```

### 场景六：跨云盘迁移（更换主云盘的用户）

从 Dropbox 迁移到 OneDrive，专业版提供向导式流程：

```bash
# 启动迁移向导
cloud-manager migrate wizard \
  --source dropbox \
  --target onedrive \
  --path "/Work" \
  --strategy "copy-then-verify"
# ...
# 查看迁移进度
cloud-manager migrate status --job-id abc123
```

## 使用流程

### 前置准备（约 60 秒）

1. 确认已安装对应云盘的客户端或可访问网页版
2. 准备好各云盘的账户凭据
3. 配置专业版工作目录：

```bash
export CLOUD_MANAGER_HOME="$HOME/.cloud-manager"
export CLOUD_MANAGER_CONFIG="$CLOUD_MANAGER_HOME/config.yaml"
```

### 验证专业版能力（约 30 秒）

```bash
# 添加优秀个云盘账户
cloud-manager account add --provider gdrive --email "you@gmail.com"
# ...
# 查看存储聚合
cloud-manager storage summary
```

### 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Shell**：bash 4.0+ 或 PowerShell 5.0+
- **网络**：可访问对应云盘服务

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 | 版本要求 |
|:---:|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 | - |
| 云盘客户端 | 软件 | 必需 | 各厂商官方下载 | 最新版 |
| rclone | 命令行工具 | 可选 | `apt install rclone` / 官网下载 | 1.60+ |
| curl | 命令行工具 | 必需 | 系统自带 | 7.0+ |
| jq | JSON 处理工具 | 可选 | `apt install jq` | 1.6+ |

### API Key 配置

- **各云盘 OAuth Token**：存储于 `$CLOUD_MANAGER_HOME/credentials/`（已 gitignore）
- **禁止**：在 SKILL.md 或脚本中硬编码账户密码或 Token
- **轮换建议**：OAuth Token 建议每 90 天重新授权一次

### 可用性分类

- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 调用命令行工具完成任务

**API Key配置方式**:
```bash
export API_KEY="your_api_key_here"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
#
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|:------|------:|:------|:------|
| content | string | 否 | cloud-manager处理的内容输入 |, 默认: 全部维度 |
| strict_level | string | 否 | 审查严格度, 可选: strict/normal/loose, 默认: normal |

## 输出格式

```json
{
  "success": true,
  "data": {
    "overall_grade": "A",
    "total_score": 92,
    "max_score": 100,
    "summary": "处理完成",
    "details": [
      {
        "item": "代码风格",
        "status": "pass",
        "score": 95,
        "comment": "符合规范"
      },
      {
        "item": "安全合规",
        "status": "warn",
        "score": 80,
        "comment": "符合规范"
      }
    ],
    "improvements": [
      {
        "priority": "high",
        "suggestion": "建议优化",
        "expected_gain": "+5分"
      },
      {
        "priority": "medium",
        "suggestion": "建议优化",
        "expected_gain": "+3分"
      }
    ]
  },
  "error": null
}
```

## 异常处理

| 现象 | 可能原因 | 解决步骤 | 优先级 |
|---:|:---|---:|---:|
| 账户添加失败 | 凭据无效或网络问题 | 重新授权，
| 同步不生效 | sync_interval 过长或守护进程未运行 | 调整间隔，重启守护进程 | P1 |
| 共享权限不生效 | 客户端缓存 | 重新登录或刷新客户端 | P1 |
| 备份规则未触发 | 时区错误或设备休眠 | 校准时区，调整调度时间 | P1 |
| 迁移中断 | 网络波动或配额不足 | ，从检查点恢复 | P2 |
| 存储分析耗时过长 | 文件数量大 | 限制扫描深度或排除大目录 | P2 |
| 去重误删 | 哈希冲突（极罕见） | 从回收站恢复，反馈问题 | P0 |

## 依赖说明(补充)

| 依赖项 | 类型 | 必需 | 说明 |
|:------:|--------|:-------|:------:|
| LLM | 模型 | 是 | 需要LLM进行智能审查, 推荐GPT-4/智谱GLM-4/DeepSeek |
| API Key | 凭证 | 否 | 使用云端LLM时需要 |

**国内替代方案**:
- OpenAI GPT → 智谱GLM-4 / 百度文心一言 / 通义千问 / DeepSeek

## 案例展示

### 多云账户配置

在 `$CLOUD_MANAGER_HOME/config.yaml` 中配置多云账户：

```yaml
accounts:
  - provider: icloud
    email: user@example.com
    sync_interval: 3600
  - provider: gdrive
    email: user@gmail.com
    sync_interval: 1800
  - provider: onedrive
    email: user@outlook.com
    sync_interval: 3600
  - provider: dropbox
    email: user@dropbox.com
    sync_interval: 3600
# ...
backup:
  default_retain: 90d
  max_concurrent: 3
  checkpoint: true
# ...
sharing:
  default_role: viewer
  expire_default: 30d
```

### 家庭共享权限矩阵

| 成员 | 家庭相册 | 财务文档 | 旅行计划 |
|----|:--:|---:|----|
| 户主 | owner | owner | owner |
| 配偶 | editor | editor | editor |
| 子女 | viewer | 无权限 | viewer |
| 长辈 | viewer | 无权限 | viewer |

### 团队权限矩阵

| 角色 | 文档库 | 财务库 | 代码库 |
|----|----|----|----|
| owner | 全部 | 全部 | 全部 |
| editor | 编辑 | 查看 | 编辑 |
| contributor | 上传 | 无权限 | 上传 |
| viewer | 查看 | 无权限 | 查看 |

### 定时备份规则

| 备份目标 | 源路径 | 调度 | 保留期 |
|:-----|:-----|:-----|:-----|
| 照片 | ~/Pictures | 每日 02:00 | 90 天 |
| 文档 | ~/Documents | 每周日 03:00 | 12 周 |
| 代码 | ~/Projects | 每日 23:00 | 30 天 |
| 配置 | ~/.config | 每月 1 日 01:00 | 6 个月 |

## 常见问题

### Q1：多云账户添加后无法同步？

检查三项：账户凭据是否有效、网络是否可访问对应云盘、`sync_interval` 是否设置过短（建议至少 1800 秒）.
### Q2：家庭共享文件夹的配额怎么算？

共享文件夹的存储配额由所有者账户承担。例如户主创建的家庭相册，存储占用计入户主的 iCloud 配额，不计入子女的配额.
### Q3：团队权限矩阵修改后多久生效？

权限变更实时生效。但已登录的成员可能需要重新打开客户端才能看到最新权限。建议变更后通知成员刷新.
### Q4：定时备份规则没有按时触发？

检查三项：系统时区是否正确、`cloud-manager` 守护进程是否运行、调度时间是否与系统休眠冲突。建议备份时间设在设备常开时段.
### Q5：跨盘迁移中途失败怎么办？

专业版默认启用检查点。迁移失败后执行 `cloud-manager migrate resume --job-id <id>` 即可从断点恢复，已迁移的文件不会重复处理.
### Q6：存储分析报表显示的占用与云盘官方不一致？

部分云盘将"共享给我的文件"计入我的配额，部分不计入。专业版默认只统计"我拥有的文件"，可通过 `--include-shared` 参数包含共享文件.
### Q7：版本历史清理后能恢复吗？

不能。版本历史清理是物理删除，无法恢复。建议清理前先导出关键版本到本地归档.
### Q8：如何识别重复文件？

专业版提供去重命令，基于文件内容哈希识别重复：

```bash
cloud-manager dedup find --provider all --min-size "1MB"
```

去重结果输出到 CSV，确认后可批量删除.
### Q9：多个云盘的同一份文件如何同步？

专业版不提供"实时双向同步"（这会带来冲突风险）。建议使用"主从同步"：指定一个云盘为主，其他为从，定期单向同步.
### Q10：专业版与免费版可以共存吗？

可以。两个版本 slug 不同，可同时安装。日常单盘操作用免费版，多云管理与自动化用专业版.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | ，请求；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 依赖云服务，需要网络连接
- 需要有效的云服务凭证和配置好的CLI环境
- 产生的云资源可能产生费用，使用前请确认计费方式
- 不同区域的服务可用性和功能支持可能存在差异
