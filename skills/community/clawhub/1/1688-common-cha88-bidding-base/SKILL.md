---
name: 88查-招投标基础
version: 0.1.0
description: 88查招投标基础搜索
---

# cha88-bidding-search

88查招投标搜索工具 —— 根据关键词搜索招投标公告信息，返回完整的搜索结果。

统一入口：`python3 {baseDir}/cli.py <命令> [参数]`

## 命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `bidding_search` | 招投标搜索 | `cli.py bidding_search -k "智慧城市" --provinces "浙江省" --cities "杭州市"` |
| `configure` | 配置 AK | `cli.py configure YOUR_AK` |

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

**展示时直接输出 `markdown` 字段，Agent 分析追加在后面，不得混入其中。**

---

## 使用流程

1. 用户提出搜索招投标的需求
2. Agent 从用户消息中提取搜索参数（关键词必填，区域/时间/分页可选）
3. 执行 `bidding_search` 命令
4. 直接输出返回的 `markdown` 字段

> 完整参数说明见 [references/capabilities/bidding_search.md](references/capabilities/bidding_search.md)。

---

## 区域参数格式规则

Agent 传入 provinces/cities/regions 参数时，**必须使用带行政后缀的全称**：
- 省份：浙江省、广东省、四川省（非"浙江"、"广东"）
- 城市：杭州市、深圳市、成都市（非"杭州"、"深圳"）
- 区县：西湖区、南山区（非"西湖"、"南山"）

如果用户说的是简称，Agent 应自动补全后缀再传入。

---

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|-----------|
| **只读** | bidding_search | 搜索为只读操作，关键词明确时直接执行 |

**全局规则**：
1. 搜索为只读操作，不涉及数据写入。
2. 当关键词明确时，可直接执行搜索。
3. 当关键词不明确时，先向用户追问确认后再执行。

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。发布到不同环境时可直接替换该文件中的变量值。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_NAME` | `cha88-bidding-search` | skill 名称 |
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

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" 或 "签名无效" 或 "401" | 提示用户当前搜索能力所需鉴权未就绪，请补充有效 AK 或检查鉴权配置后重试 |
| "参数缺失" 或 "keyword 不能为空" | 提示用户补充搜索关键词后重试 |
| "限流" 或 "429" | 建议用户等待 1-2 分钟后重试 |
| 其他 | 仅输出 markdown 即可 |
