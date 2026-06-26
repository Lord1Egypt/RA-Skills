# 工具使用指南

## ask_user_question 工具

用于收集用户信息的交互式提问工具。

**调用格式**：
```json
{
  "questions": [
    {
      "question": "问题内容？",
      "header": "短标签（最多12字符）",
      "options": [
        { "label": "选项1", "description": "选项说明" },
        { "label": "选项2", "description": "选项说明" }
      ],
      "multiSelect": false
    }
  ]
}
```

**使用场景**：
- 收集出发城市、出行日期、人数预算
- 确认解析结果是否正确
- 让用户选择酒店/航班方案
- 询问是否需要省钱版/品质版

**注意事项**：
- 每次最多问 4 个问题
- 系统自动添加"其他"选项
- 优先使用 Memory 中的已知信息，减少重复追问

---

## FlyAI 核心能力

四大搜索命令：

| 命令 | 用途 | 在本场景中的作用 |
|------|------|------------------|
| `keyword-search` | 自然语言搜索 | 模糊匹配攻略中的描述 |
| `search-flight` | 机票搜索 | 验证/替换航班信息 |
| `search-hotel` | 酒店搜索 | 验证酒店可用性，查找替代 |
| `search-poi` | 景点搜索 | 验证景点信息，补充门票/开放时间 |

> ⚠️ **SSL 证书问题**：所有命令前加 `NODE_TLS_REJECT_UNAUTHORIZED=0`

**调用示例**：
```bash
# 自然语言搜索
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai keyword-search --query "大理洱海边无边泳池民宿"

# 机票搜索
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-flight \
  --origin "上海" --destination "大理" \
  --dep-date 2026-08-10 --back-date 2026-08-14 --sort-type 3

# 酒店搜索
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-hotel \
  --dest-name "大理" --key-words "云隐山房" \
  --check-in-date 2026-08-10 --check-out-date 2026-08-12

# 景点搜索
NODE_TLS_REJECT_UNAUTHORIZED=0 flyai search-poi --city-name "大理"
```

---

## fetch_content 工具

获取网页实时信息，用于：
- 解析小红书/抖音/携程等平台的攻略链接
- 补充 FlyAI 搜不到的内容
- 验证最新旅行政策

```python
fetch_content(url="[攻略链接]", query="行程 景点 酒店")
```

**链接解析降级处理**：
如果链接无法直接访问（平台限制），提示用户：
> "这个链接我暂时读不了，你可以把攻略内容复制粘贴给我，或者发截图也行～"

---

## Browser Agent 工具

当 `fetch_content` 无法获取动态页面内容时的备选方案。

**使用场景**：
- 携程移动端（m.ctrip.com）
- 需要 JS 渲染的页面
- `fetch_content` 返回导航菜单/版权信息而非实际内容

**调用示例**：
```python
Agent(
  subagent_type="Browser",
  description="获取攻略内容",
  prompt="""
  请打开 [URL] 这个攻略页面。
  页面加载后，向下滚动阅读完整内容，提取出：
  1. 目的地是哪里
  2. 玩几天
  3. 每天的行程安排
  4. 推荐的景点
  5. 住宿信息
  6. 交通方式
  7. 费用预算
  请把所有信息整理成文字返回。
  """
)
```
