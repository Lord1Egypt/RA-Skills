# baidu-ai-search Skill

百度 AI 搜索（智能搜索生成）：联网搜索 + AI 智能总结 + 带来源引用。

## 功能

基于百度千帆平台的「智能搜索生成」API，输入问题返回 AI 联网总结后的答案及参考来源。

## API 详情

- **Endpoint**: `POST https://qianfan.baidubce.com/v2/ai_search/chat/completions`
- **鉴权**: `Authorization: Bearer <BAIDU_API_KEY>`
- **与 baidu-search 的区别**: baidu-search 返回原始搜索结果；本 API 返回 AI 联网总结 + 引用来源

## 核心参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `messages` | array | ✅ | 消息列表，role=user，content=问题 |
| `model` | string | ✅ | 模型名，如 `ernie-4.5-turbo-32k`、`deepseek-v3` |
| `search_source` | string | 可选 | 搜索引擎版本，默认 `baidu_search_v2` |
| `stream` | bool | 可选 | 是否流式，默认 false |
| `enable_deep_search` | bool | 可选 | 深度搜索（最多100个结果），默认 false |
| `enable_corner_markers` | bool | 可选 | 是否显示来源角标，默认 true |
| `search_recency_filter` | string | 可选 | 时间筛选：week/month/semiyear/year |
| `resource_type_filter` | array | 可选 | 资源类型过滤，如 `[{"type":"web","top_k":10}]` |

## 使用方式

```bash
# 基础搜索
python3 baidu-ai-search/scripts/search.py '{"query":"今日股市行情","count":5}'

# 带时间筛选
python3 baidu-ai-search/scripts/search.py '{"query":"杭州房价","count":5,"freshness":"month"}'

# 带深度搜索
python3 baidu-ai-search/scripts/search.py '{"query":"北京旅游攻略","count":5,"deep_search":true}'
```

## 返回格式

```json
{
  "answer": "AI总结的答案",
  "references": [
    {
      "id": 1,
      "title": "网页标题",
      "url": "https://...",
      "content": "相关内容片段",
      "date": "2025-01-01",
      "type": "web"
    }
  ],
  "request_id": "...",
  "is_safe": true
}
```

## 注意事项

- 使用 `BAIDU_API_KEY` 环境变量（与 baidu-search 相同）
- 每日免费额度 1000 次
- 默认使用 `deepseek-v3.2-think` 模型
