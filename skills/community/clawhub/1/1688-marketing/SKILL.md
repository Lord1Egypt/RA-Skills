---
name: 1688-marketing
description: |
  1688营销 Skill —— 帮助商家进行招商活动报名、查看商机推荐等营销操作。
  核心工具能力：招商活动查询、商品建议价查询、活动报名提交、商机推荐查询。
  触发词：报名活动、招商活动、查询活动、提报、报名、活动报名、查看建议价、商机推荐、商机、市场机会、找商机、查商机，不要在用户仅询问非1688业务（如闲聊、天气、翻译等无关话题）时触发。
metadata: {"openclaw": {"emoji": "🏷️","version": "1.0.0", "requires": {"bins": ["python3"]}, "primaryEnv": "ACCESS_KEY"}}
---

# 1688-marketing-skill

统一入口：`python3 {baseDir}/cli.py <command> [options]`

## 环境准备

> **重要**：本 skill 所在的整个目录文件需要先拷贝到 ${AGENT_WORK_ROOT}/workspace 目录下，再执行后续操作。
统一入口：`python3 {baseDir}/cli.py <command> [options]` 尽量使用绝对路径执行脚本

### Windows 权限问题（仅 Windows 用户需要）

若 skills 目录缺少执行权限（提示"拒绝访问"），需先将目录拷贝到 workspace 再操作：

```cmd
xcopy /E /I /Y "<skills目录路径>" "%USERPROFILE%\workspace\1688-auth-skill-for-wukong"
cd /d "%USERPROFILE%\workspace\1688-auth-skill-for-wukong"
```

> `/E` 递归复制所有子目录，`/I` 目标不存在时自动创建，`/Y` 覆盖时不询问确认。
> 拷贝完成后，后续所有命令均在 workspace 路径下执行。

首次使用前，在项目根目录执行：

```bash
pip install -r requirements.txt
# 若上述命令不可用，尝试：
pip3 install -r requirements.txt
```
依赖列表：仅使用 Python 标准库，无需额外安装第三方包。

## AK 安全说明

> ⚠️ **AK 是访问 1688 接口的唯一凭证，请妥善保管，避免泄漏。**

- AK 在本地以**设备绑定加密**方式存储（PBKDF2 派生密钥 + 流加密 + HMAC 校验），加密文件拷贝到其他机器后**无法解密**
- 不要将 AK 明文粘贴到聊天记录、截图、日志或版本控制中
- 不要将 `ak_store.json` 或 `.device_id` 上传到任何云端或共享目录
- 如怀疑 AK 已泄漏，立即执行 `cli.py configure --clear` 清除本地存储，并前往 [clawhub.1688.com](https://clawhub.1688.com/) 重新获取


## 意图判断

### 触发场景
当用户表达以下意图时，应触发本技能：
- **招商活动报名**: 报名活动、招商活动、查询活动、提报、报名、活动报名
- **商品建议价查询**: 查看建议价、查询价格、提报价
- **商机推荐查询**: 商机推荐、商机、市场机会、找商机、查商机

### 不触发场景
当用户仅询问以下非 1688 业务话题时，不应触发本技能：
- 闲聊（如：今天天气怎么样）
- 通用编程问题（如：帮我写一个 Python 排序算法）
- 翻译请求（如：帮我把这段话翻译成英文）
- 其他与 1688 营销无关的话题

## Tool 总览

| 工具名称 | 用途 | 调用方式                                                                                                                        |
|----------|------|-----------------------------------------------------------------------------------------------------------------------------|
| `1688_enroll_activity_query` | 查询招商活动列表 | `python3 {baseDir}/cli.py 1688_enroll_activity_query [--keyword <关键词>] [--pageNo <页码>] [--pageSize <条数>]`                   |
| `1688_enroll_offer_query` | 查询商品建议提报价 | `python3 {baseDir}/cli.py 1688_enroll_offer_query --activityId <活动ID> --itemId <商品ID>`                                      |
| `1688_enroll_submit_item` | 提交活动报名（⚠️写入） | `python3 {baseDir}/cli.py 1688_enroll_submit_item --activityId <活动ID> --itemId <商品ID> --fillFormDataList '<JSON>'`          |
| `1688_opp_recommend` | 查询商机推荐列表 | `python3 {baseDir}/cli.py 1688_opp_recommend [--keyword <关键词>] [--categoryId <类目>] [--pageNo <页码>] [--pageSize <条数>]`       |
| `configure` | 配置 AK（支持 --status / --clear / --reset） | `python3 {baseDir}/cli.py configure YOUR_AK`                                                                                           |
| `get_ak` | 获取AK | `cli.py get_ak` |


## 输出格式

所有命令统一输出 JSON 格式，结构如下：

```json
{
  "success": true,
  "markdown": "可选的用户可读描述",
  "data": {},
  "error_code": "可选的错误码（仅失败时）",
  "required_scope": "可选的所需 OAuth Scope（仅授权错误时）"
}
```

> 仅包含非空字段。`error_code` 和 `required_scope` 用于 Agent 自动识别网关授权错误并触发恢复流程。

## 使用流程

Agent 根据用户意图**识别所属功能模块**，按对应流程执行：

### 流程一：招商活动报名

1. **查询活动**：用户表达报名意图时，先调用 `1688_enroll_activity_query` 查询招商活动，展示活动列表供用户选择
2. **查询建议价**：用户选定活动和商品后，调用 `1688_enroll_offer_query` 查询商品信息和建议提报价，展示给商家确认，此接口返回的价格单位为分。当建议价为空时，中断流程，提示商家无法报名此活动
3. **确认价格**：**必须等商家明确确认建议价后**，才能进入报名步骤
4. **提交报名**：商家确认后，根据商品是否有 SKU 构造 `fillFormDataList`，调用 `1688_enroll_submit_item` 提交报名，此接口入参价格单位为元

### 流程二：商机推荐查询

1. **明确意图**：用户表达查看商机、市场机会的意图
2. **收集筛选条件**：从用户消息中提取关键词、类目等筛选条件（均为可选）
3. **执行查询**：调用 `1688_opp_recommend` 查询商机推荐列表
4. **展示结果**：将商机列表以易读格式展示（标题、类目、求购数、参考价格等），如有更多结果提示用户可翻页

各命令在 AK 缺失等情况下会自行返回明确错误，Agent 按下方「异常处理」应对即可。

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|-----------|
| **只读** | 1688_enroll_activity_query | 直接执行 |
| **只读** | 1688_enroll_offer_query | 直接执行 |
| **只读** | 1688_opp_recommend | 直接执行 |
| **写入** | 1688_enroll_submit_item | **必须在商家确认建议价后才能执行**，不得自动提交 |

**全局写入规则（适用于所有写操作）**：
1. 所有写入操作必须经过商家明确确认，不得自动执行。
2. 提交报名前，必须先查询建议价并展示给商家；商家明确确认价格后，方可提交报名。
3. 不擅自修改商家确认的任何参数。

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。发布到不同环境时可直接替换该文件中的变量值。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_NAME` | `1688-marketing` | skill 名称 |
| `SKILL_VERSION` | `1.0.0` | skill 版本号 |
| `SKILL_CHANNEL` | `clawhub` | 发布渠道 |

> 已存在的系统环境变量优先级高于 `.env`，CI/CD 注入的变量不会被覆盖。

## 埋点上报

每次 CLI 命令执行时，自动向 skill 网关上报一次调用记录，用于统计 skill 调用次数。

- **实现位置**：`scripts/_tracker.py` → `report_skill_usage()`，在 `cli.py` 的 `main()` 中每次命令执行后自动调用
- **上报接口**：`POST /api/reportSkillsUsage/1.0.0`
- **上报参数**：

  | 参数 | 值来源 | 说明 |
  |------|--------|------|
  | `apiName` | 固定 `null` | 固定传 null |
  | `skillsName` | `.env` `SKILL_NAME` | skill 名称 |
  | `version` | `.env` `SKILL_VERSION` | skill 版本号 |
  | `scene` | 固定 `CLI` | 固定值 |
  | `channel` | `.env` `SKILL_CHANNEL` | 发布渠道 |

- **失败处理**：上报失败静默忽略，不影响主流程

## 执行前置（首次命中能力时必须）

- 首次执行 `1688_enroll_activity_query` 前：先完整阅读 `references/capabilities/1688_enroll_activity_query.md`
- 首次执行 `1688_enroll_offer_query` 前：先完整阅读 `references/capabilities/1688_enroll_offer_query.md`
- 首次执行 `1688_enroll_submit_item` 前：先完整阅读 `references/capabilities/1688_enroll_submit_item.md`
- 首次执行 `1688_opp_recommend` 前：先完整阅读 `references/capabilities/1688_opp_recommend.md`
- 首次执行 `configure` 前：先完整阅读 `references/capabilities/configure.md`
- 同一会话内后续重复调用可复用已加载知识；仅在规则冲突或文档更新时重读。

## 授权链接处理（browser_use）

`get_ak` 和 `authorize` 命令输出一条 JSON 后**立即退出**，回调服务器作为独立后台进程继续运行（最长 300 秒）。

**输出格式**：
```json
{
  "pending": true,
  "action": "browser_use",
  "url": "https://...",
  "markdown": "授权链接已生成！请使用 browser_use 工具打开以下链接完成授权..."
}
```

> ⚠️ **强制动作**：输出中只要出现 `"action": "browser_use"`，Agent **必须立即**调用 `browser_use` 工具打开 `url` 字段中的链接，不得跳过、延迟或用其他方式替代。

**Agent 处理流程**：
1. 读到 `"action": "browser_use"` → **立即**用 `browser_use` 工具导航到 `url`，并向用户展示 `markdown` 字段内容。
2. 在页面中完成登录和授权操作（AK 模式：复制 AK；OAuth 模式：点击授权确认）。
3. 授权完成后，浏览器页面会自动将结果回调给后台服务器（`localhost`），服务器直接将 AK/Token 写入本地存储。
4. browser_use 返回后，调用 `python3 cli.py configure --status` 确认 AK 是否已保存成功。

**注意事项**：
- 命令本身只输出这一条 JSON，**不会有第二条结果 JSON**，无需继续等待命令输出。
- 授权回调目标是 `localhost`，browser_use 执行环境必须能访问本机回调端口（8080–8089）。
- 若 300 秒内未完成授权，后台服务进程自动退出，下次运行 `get_ak` 时会自动清理并重新启动。
- **禁止**调用系统浏览器、`open` 命令或任何其他方式替代 browser_use。

## 异常处理

任何命令输出 `success: false` 时：

1. **`markdown`不为空时先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 / error_code | Agent 额外动作 |
|------------------------------|--------------|
| "AK 未配置" 或 "AK 未就绪" | **停止一切搜索尝试**，优先执行 `python3 cli.py get_ak` 自动获取 AK；如自动获取失败，引导用户前往 https://clawhub.1688.com/ 登录后右上角点击🔑复制获取ak内容后执行 `python3 cli.py configure YOUR_AK`。**禁止浏览器替代** |
| "参数缺失" 或 "参数错误" | 提示用户补充缺失参数后重试 |
| "限流" 或 "429" | 建议用户等待 1-2 分钟后重试 |
| "报名失败" | 展示失败原因，引导用户检查商品或活动状态 |
| "格式错误" | 提示用户检查 fillFormDataList 的 JSON 格式 |
| "投放类型" 或 "cpxObjEvent" | 提示用户投放类型仅支持 ENQUIRY（询盘）、FEEDBACK（线索）、PAYMENT（订单） |
| "无法识别的类目" | 提示用户输入正确的类目 ID 或中文名称 |
| 其他 | 仅输出 markdown 即可 |

## 参数补齐引导话术

Agent 根据用户意图选择对应的引导话术：

### 招商活动报名

> "要进行招商活动报名，我需要以下信息：
> 1. 您想报名哪个活动？（我可以帮您查询当前有效的活动）
> 2. 您要提报的商品ID是什么？
> 查询到建议价后，需要您确认提报价格，我再帮您提交报名。"

### 商机推荐

> "我可以帮您查看商机推荐，您可以告诉我：
> 1. 想搜索什么关键词？（可选，如：连衣裙、运动鞋）
> 2. 想看哪个类目的商机？（可选，如：女装、鞋、童装）
> 也可以直接查看默认推荐。"