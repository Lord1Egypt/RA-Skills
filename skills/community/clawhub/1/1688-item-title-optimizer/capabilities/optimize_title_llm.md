# optimize_title_llm — LLM 深度重写

## 功能说明

基于大语言模型的智能标题重写方式。LLM 深度理解商品特征后全面改写标题，生成更自然流畅的标题，自动更新年份、融入热词。支持用户偏好定制（如"加入'防潮'单词"）。

## 前置条件

- 已配置 AK（通过 `cli.py configure YOUR_AK` 或设置环境变量 `ALI_1688_AK`）

## CLI 调用

```bash
# 基础调用
python3 {baseDir}/cli.py optimize_title_llm --item_id <商品ID>

# 带用户偏好
python3 {baseDir}/cli.py optimize_title_llm --item_id <商品ID> --preference "加入防潮单词"
```

**参数说明**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--item_id` | int | 是 | 商品ID |
| `--preference` | str | 否 | 用户偏好，自然语言描述优化偏好 |

## 用户偏好参数 (preference)

`preference` 参数允许用户通过自然语言指定优化偏好，LLM 会在优化标题时考虑这些偏好。

**支持的偏好类型**：

- **关键词偏好**："加入'防潮'单词"、"添加'防摔'和'耐用'关键词"
- **特点强调**："突出材质特点"、"强调便携性"、"体现性价比"
- **风格偏好**："标题要简洁"、"面向年轻消费者"
- **组合偏好**："加入'防潮'单词，同时突出材质特点"

**Agent 偏好提取关键词**：

| 用户表述 | 偏好类型 |
|---------|---------|
| "加入xxx"、"添加xxx"、"包含xxx" | 关键词偏好 |
| "突出xxx"、"强调xxx"、"体现xxx" | 特点强调 |
| "要xxx风格"、"面向xxx" | 风格偏好 |

## 返回数据说明

成功时返回 `data` 对象，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| item_id | int | 商品ID |
| old_title | String | 原标题（⚠️ 必须展示） |
| new_title | String | 优化后的标题（⚠️ 必须展示） |
| new_title_words | Array | 标题词列表，包含每个词的标签和描述 |
| other_words | Array | 推荐词列表，未使用的高价值热词 |

## 输出格式

### 成功输出

```json
{
  "success": true,
  "markdown": "✅ 标题优化完成（LLM深度重写）",
  "data": {
    "item_id": 831034165952,
    "old_title": "304不锈钢水杯",
    "new_title": "2026新款304不锈钢保温杯便携大容量运动水杯",
    "new_title_words": [
      {"word": "2026", "tag": "时间词", "type": null, "description": "自动更新至当前年份"},
      {"word": "新款", "tag": "修饰词", "type": null},
      {"word": "304", "tag": "属性词", "type": null},
      {"word": "不锈钢", "tag": "材质词", "type": null},
      {"word": "保温杯", "tag": "热词", "type": null, "description": "类目热搜词"},
      {"word": "便携", "tag": "热词", "type": null, "description": "类目热搜词"},
      {"word": "大容量", "tag": "热词", "type": null, "description": "类目热搜词"},
      {"word": "运动", "tag": "热词", "type": null, "description": "类目热搜词"},
      {"word": "水杯", "tag": "品类词", "type": null}
    ],
    "other_words": [
      {"word": "户外", "tag": "热词", "weight": 8.5, "min_rnk": 12, "description": "类目热搜词，排名12，建议添加"}
    ]
  }
}
```

### 失败输出

```json
{
  "success": false,
  "markdown": "❌ AK 未配置\n\n运行: `cli.py configure YOUR_AK`",
  "data": {}
}
```

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| AK 未配置 | 提示用户配置 AK |
| 商品ID 未提供 | 提示用户提供 --item_id 参数 |
| 签名无效（401） | 提示用户检查 AK 是否有效 |
| 请求被限流（429） | 建议用户等待 1-2 分钟后重试 |
| 服务异常（500） | 提示用户稍后重试 |

## 展示规范

展示时必须：
1. **必须同时显示**原标题（old_title）和新标题（new_title）
2. **禁止只显示新标题**
3. 如有推荐词（other_words），可一并展示供参考
4. 如用户提供了偏好，需在展示中标注"已考虑您的偏好"

## 与 optimize_title 的对比

| 特性 | optimize_title_llm | optimize_title |
|------|-------------------|---------------|
| 优化方式 | LLM 深度重写 | 规则 + 统计 |
| 优化质量 | ★★★★★ | ★★★★☆ |
| 优化速度 | 2-5 秒 | < 1 秒 |
| 标题自然度 | 非常自然 | 较自然 |
| 成本 | 较高 | 低 |
| 偏好支持 | ✅ 支持 preference | ❌ 不支持 |
