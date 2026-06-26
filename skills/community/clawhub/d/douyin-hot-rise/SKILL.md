---
name: douyin-billboard-fetch-hot-rise-list
description: "调用抖音上升热点榜接口，获取实时热点上升趋势数据。使用此技能当用户需要：获取抖音热榜/上升热点/热点趋势数据、调用 /douyin/billboard/fetch_hot_rise_list 接口、使用 azt_api_key 调用热榜接口、用 Python 脚本拉取抖音热点上升榜单。Use this skill for Douyin hot rise billboard, trending topics, douyin billboard API calls."
argument-hint: "可选：page, page_size, order, sentence_tag, keyword"
user-invocable: true
---

# 抖音上升热点榜 Skill

调用接口：
- `POST https://coze-js-api.devtool.uk/douyin/billboard/fetch_hot_rise_list`

执行随附的 Python 脚本来完成请求，不要在回复中内联构造 curl 命令（除非用户明确要求）。

## 使用场景

以下情况触发本技能：
- 用户想获取抖音当前上升热点/热榜数据
- 用户想批量拉取抖音热点趋势
- 用户需要按关键词或分类筛选上升热点
- 用户想用 Python 调用热榜接口

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `azt_api_key` | **必填** | — | 调用接口的鉴权 Key |
| `page` | 可选 | `1` | 页码 |
| `page_size` | 可选 | `10` | 每页条数 |
| `order` | 可选 | `rank` | 排序方式，可选 `rank` / `hot` |
| `sentence_tag` | 可选 | — | 话题分类标签筛选 |
| `keyword` | 可选 | — | 关键词筛选 |

## API Key 获取方式

**必须提供 `azt_api_key`**，解析顺序如下：

1. 读取环境变量 `AZT_API_KEY`。
2. 用户在参数中直接传入。
3. 如果两者均未提供，**停止执行**并提示：

说明：脚本对外输入使用 `azt_api_key`（或 `AZT_API_KEY`），实际请求接口时会映射为 payload 字段 `api_key`。

> 未检测到 API Key。请前往 **https://devtool.uk/plugin** 购买或查看使用说明后重试。

## 执行方式

```bash
# 先设置环境变量（或在脚本参数中传入）
export AZT_API_KEY="your_key_here"

python3 scripts/fetch_hot_rise_list.py
```

带可选参数示例：

```bash
python3 scripts/fetch_hot_rise_list.py --page 1 --page_size 20 --order hot --keyword 明星
```

## 响应处理

1. 显示请求结果状态（`code: 200` 为成功，`code: -1` 为失败）。
2. 列出返回的热点条目（标题、热度值、排名等）。
3. 如果失败，给出可能原因及修正建议。

常见失败原因：
- `azt_api_key` 无效或已过期 → 前往 https://devtool.uk/plugin 重新购买
- `azt_api_key` 积分已用完 → 联系作者续费
- 网络问题或服务器错误 → 稍后重试

## 输出格式

```markdown
# 抖音上升热点榜请求结果

- 接口：POST https://coze-js-api.devtool.uk/douyin/billboard/fetch_hot_rise_list
- 页码：<page>
- 每页条数：<page_size>
- API Key 来源：<env: AZT_API_KEY | 用户传入>

## 返回数据
<热点条目列表，含排名/标题/热度等字段>

## 状态
<成功/失败信息及剩余积分>
```
