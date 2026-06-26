---
name: astrmap-voc
description: 星图AI·客户洞察（VOC），帮助全球电商卖家进行产品改进、新品开发、市场调研！核心能力：获取亚马逊评论、AI深度分析差评、精准量化高频问题、挖掘高星隐性差评、生成改进建议、追踪评论趋势、增量更新。
metadata:
  openclaw:
    requires:
      env:
        - CUSTOMER_INSIGHTS_API_KEY
    dependencies:
      python:
        - requests>=2.28.0
---

# AstrMap Review Insights Skill

## 语言使用规范

- 若用户使用**中文**输入，以**中文**回复
- 若用户使用**非中文**（如英文）输入，以**英文**回复

## 配置

### API Key

所有 API 调用均需要 API Key 进行身份认证。

**说明**：API 端点固定为 `https://api.astrmap.com`，不可配置。

**推荐方式**：在 `~/.zshrc` 或 `~/.bashrc` 中设置环境变量：

```bash
export CUSTOMER_INSIGHTS_API_KEY="your-api-key-here"
```

> API Key 获取方式：前往 https://www.astrmap.com/ 下载并安装AstrMap桌面客户端，登录后点击**左下角用户菜单** → **接口密钥**页面，创建并复制 API Key。

**重要**：若 `CUSTOMER_INSIGHTS_API_KEY` 环境变量为空，或用户未提供 API Key，**请先询问用户**：
> 「请提供您的 AstrMap API Key（可前往 https://www.astrmap.com/ 下载桌面客户端，登录后在左下角用户菜单 → 接口密钥 页面创建获取）」
>
> 获取后，通过 `--api-key` 参数传入后续所有命令。

**安全提示**：本 Skill 将 API Key 发送至 AstrMap 服务器（api.astrmap.com）进行身份认证，用于分析您指定的亚马逊产品评论数据。API Key 不会用于访问其他服务。

### 功能分层说明

| 功能 | 需要桌面客户端 | 需要 API Key |
|------|---------------|-------------|
| 查询已完成任务的分析结果 | ❌ | ✅ |
| 创建仅采集任务 | ✅ | ✅ |
| 创建自动分析任务 | ✅ | ✅ |
| 增量获取 | ✅ | ✅ |
| 手动触发分析 | ❌ | ✅ |

> 提示：如果您只需要查询已完成的分析结果，可以直接使用 API Key，无需下载和安装桌面客户端。

### 桌面客户端

创建任务需要 AstrMap 桌面客户端在线运行。

**设备不在线时处理流程**（`check_device` 返回 1001 错误）：

1. **询问用户**：「桌面客户端未运行，请问您是否已安装桌面客户端？」
2. **若用户未安装**：询问是否需要帮助下载，获取下载链接后引导用户解压和启动
3. **若用户已安装但未运行**：提示用户启动桌面客户端，重新检测设备在线状态

### 桌面客户端下载与安装

#### 1. 获取下载链接

```bash
python scripts/api_client.py --action get_download_links
```

#### 2. 解压注意事项

> 重要：解压时请勿使用 Windows 自带的解压工具（会导致问题），建议使用 7-Zip、WPS解压 等工具。

#### 3. 启动指引

**macOS**：将整个文件夹移动到「应用程序」目录，右键点击 Astrmap.app 选择「打开」，若提示「无法打开」请前往「系统设置 → 安全性与隐私 → 通用」选择「仍要打开」确认。

**Windows**：右键点击 "launch.vbs" 选择「用 PowerShell 运行」或直接双击启动。

#### 4. 首次使用配置

桌面客户端启动后，需要：
1. 登录 AstrMap 账号
2. 登录亚马逊买家账号（请勿使用正在做业务的卖家账号）
3. 确保亚马逊访问畅通

### 安全与验证

详细的安全验证说明、隐私风险声明、Amazon 账号安全和 API Key 安全建议，**请阅读** `{baseDir}/references/security.md`。

### 依赖安装

```bash
pip install -r requirements.txt
```

## 重要说明

### 积分规则

- **创建任务（自动模式）**：免费获取亚马逊评论，AI 分析会扣除账户积分
- **创建任务（仅采集模式）**：免费获取亚马逊评论，不扣除积分
- **增量获取**：获取最新评论并重新分析，扣除积分
- **查询结果**：查看已完成任务的分析结果，不扣积分

### 前置条件（仅创建任务时需要）

1. AstrMap 桌面客户端已登录
2. 桌面客户端已登录亚马逊买家账号（勿使用正在做业务的卖家账号）
3. 确保亚马逊访问畅通

> 查询已完成任务的分析结果无以上限制，可直接调用。

## Workflow

### 调用方式

```bash
python scripts/api_client.py --action <操作> [--参数...]
```

### 1. 检查设备在线

```bash
python scripts/api_client.py --action check_device --api-key "your-key"
```

返回：`{online: true, device_id: "xxx", status: "idle"}`

### 2. 创建任务

> 注意：创建任务会扣除积分。在执行创建任务命令前，必须先告知用户并等待确认：
> 「即将为您创建任务，当前账户剩余积分：{points}。本次任务将扣除积分，是否继续？」

**创建任务流程**：
1. `--action check_device` → 检查设备在线状态
2. `--action get_points` → 检查账户积分
3. **告知用户积分消耗，等待用户确认**
4. 确认前置条件满足后，执行 `--action create_task --asin <ASIN> --site <站点> [--is-auto false]`

**运行模式**：
| 参数 | 说明 |
|------|------|
| `--is-auto true`（默认） | 自动模式：采集完成后自动执行 AI 分析 |
| `--is-auto false` | 仅采集模式：采集完成后停在"待分析"状态 |

**站点映射**：US/CA/UK(英语)、DE(德语)、FR(法语)、IT(意大利语)、ES(西班牙语)、JP(日语)

**命令示例**：
```bash
python scripts/api_client.py --action create_task --api-key "your-key" --asin "B09V3KXJPB" --site US
```

### 3. 轮询任务状态

任务提交后，每隔 **6 分钟** 执行一次查询：

```bash
python scripts/api_client.py --action get_task_detail --api-key "your-key" --task-id "TSK_xxx"
```

**状态流转**：

**自动模式** (`is_auto=true`)：`PENDING` → `DISPATCHING` → `COLLECTING` → `PROCESSING` → `ANALYZING` → `SUCCESS/FAILED/CANCELLED`

**仅采集模式** (`is_auto=false`)：`PENDING` → `DISPATCHING` → `COLLECTING` → `COLLECTED`

**各状态的提示语**：

| 状态 | 向用户展示 |
|------|-----------|
| PENDING | 「任务已提交，等待调度中...」 |
| DISPATCHING | 「正在分配设备...」 |
| COLLECTING | 「正在获取亚马逊评论数据，请耐心等待（通常需要 20~120 秒）」 |
| PROCESSING | 「评论数据获取完成，正在处理中...」 |
| ANALYZING | 「数据处理完成，AI 正在分析中...」 |
| SUCCESS | 「分析完成！正在为您获取结果...」 |
| FAILED | 「任务失败，请检查设备状态和网络连接后重试」 |
| CANCELLED | 「任务已取消」 |
| COLLECTED | 「采集完成！已进入待分析状态」 |

> 若任务长时间（超过 18 分钟）未完成，提示用户检查桌面客户端是否在线。

### 4. 获取分析结果

```bash
# AI 洞察摘要
python scripts/api_client.py --action get_ai_insights --api-key "your-key" --task-id "TSK_xxx"
# 分类标签分布
python scripts/api_client.py --action get_category_tag_distribution --api-key "your-key" --task-id "TSK_xxx"
# 基础统计
python scripts/api_client.py --action get_basic_statistics --api-key "your-key" --task-id "TSK_xxx"
# 差评列表
python scripts/api_client.py --action get_negative_reviews --api-key "your-key" --task-id "TSK_xxx" --page 1 --page-size 20
```

> 注意：查询已完成任务的结果不扣积分，也无前置条件限制。

### 5. 增量获取

> 注意：增量获取会扣除积分。在执行前必须先告知用户并等待确认。

**增量获取流程**：
1. 检查设备和积分
2. 告知用户积分消耗，等待确认
3. `--action create_incremental --task-id <task_id>`
4. 轮询任务状态（与创建任务相同）

### 6. 手动触发分析（仅采集模式）

仅采集模式 (`is_auto=false`) 的任务，采集完成后停在 COLLECTED 状态，需要手动触发 AI 分析：

```bash
python scripts/api_client.py --action trigger_analysis --api-key "your-key" --task-id "TSK_xxx"
```

状态流转：`COLLECTED` → `PROCESSING` → `ANALYZING` → `SUCCESS`

## 所有可用操作

| action | 说明 | 必需参数 |
|--------|------|----------|
| get_download_links | 获取桌面客户端下载链接 | - |
| check_device | 检查设备是否在线 | - |
| create_task | 创建任务 | --asin, --site |
| create_incremental | 增量获取 | --task-id |
| trigger_analysis | 手动触发分析 | --task-id |
| get_task_detail | 查询任务详情 | --task-id |
| get_task_list | 获取任务列表 | - |
| get_ai_insights | 获取 AI 洞察 | --task-id |
| get_basic_statistics | 获取基础统计 | --task-id |
| get_representative_reviews | 获取代表性评论 | --task-id |
| get_category_tag_distribution | 获取分类标签分布 | --task-id |
| get_negative_reviews | 获取差评列表 | --task-id |
| get_trend | 获取评论趋势 | --task-id |
| get_related_comments | 获取关联评论 | --task-id, --association-type |
| get_comments | 获取原始评论 | --task-id |
| get_comments_overview | 获取评论概览 | --task-id |
| get_points | 查询积分余额 | - |

## 错误处理

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| 1001 | 设备不在线 | 桌面客户端未运行，询问用户是否安装或启动 |
| 1002 | 积分不足 | 提示用户充值积分 |
| 2001 | API Key 无效 | 检查 API Key 是否正确 |
| 2002 | API Key 已禁用 | 提示用户重新创建 |
| 2003 | API Key 已过期 | 提示用户重新创建 |
| 2004 | 权限不足 | 检查 API Key 权限配置 |
| 2005 | 请求频率超限 | 提示用户稍后重试 |
| InvalidTaskStatus | 任务状态不是 COLLECTED | 只有仅采集模式且状态为 COLLECTED 的任务才能触发分析 |

## 详细 API 文档

如需了解详细的 API 端点说明、请求参数、响应格式，请阅读 [API 参考文档](references/api_reference.md)。

## 使用示例

### 场景一：创建新任务

```
用户: 帮我获取 B09V3KXJPB 的评论并分析
AI Agent:
1. 检查 API Key → 若未配置，询问用户提供
2. 检查设备和积分
3. 告知积分消耗，等待确认
4. 创建任务
5. 每 6 分钟轮询状态，实时反馈进度
6. 分析完成后获取结果
```

### 场景二：仅采集模式 + 手动触发分析

```
用户: 帮我只采集评论，暂时不做分析
AI Agent:
1. 检查 API Key 和设备
2. 创建任务时使用 --is-auto false
3. 轮询状态直到 COLLECTED
4. 用户确认分析后，执行 trigger_analysis（仅需 API Key，无需桌面客户端）
```

### 场景三：查询已完成任务

```
用户: 查看 TSK_xxx 任务的分析结果
AI Agent:
1. 检查 API Key
2. 直接获取分析结果（无需设备和前置条件）
```
