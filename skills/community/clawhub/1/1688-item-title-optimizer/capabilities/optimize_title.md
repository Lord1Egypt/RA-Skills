# optimize_title — 添加热词优化（规则版）

## 功能说明

基于规则和统计的标题优化方式。保留原标题结构，通过删除低效词和添加高价值热搜词来优化标题。成本低、速度快，适合快速批量处理。

## 前置条件

- 已配置 AK（通过 `cli.py configure YOUR_AK` 或设置环境变量 `ALI_1688_AK`）

## CLI 调用

```bash
python3 {baseDir}/cli.py optimize_title --item_id <商品ID>
```

**参数说明**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--item_id` | int | 是 | 商品ID |

## 返回数据说明

成功时返回 `data` 对象，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| item_id | int | 商品ID |
| old_title | String | 原标题（⚠️ 必须展示） |
| new_title | String | 优化后的标题（⚠️ 必须展示） |
| optimize_reason | String | 优化说明 |
| new_title_words | Array | 标题词列表，包含每个词的标签和类型 |
| other_words | Array | 推荐词列表，未使用的高价值热词 |

## 输出格式

### 成功输出

```json
{
  "success": true,
  "markdown": "✅ 标题优化完成（添加热词方式）",
  "data": {
    "item_id": 831034165952,
    "old_title": "304不锈钢水杯",
    "new_title": "304不锈钢保温杯便携大容量",
    "optimize_reason": "添加热词:保温杯,便携,大容量",
    "new_title_words": [
      {"word": "304", "tag": "属性词", "type": null},
      {"word": "不锈钢", "tag": "属性词", "type": null},
      {"word": "保温杯", "tag": "热词", "type": "add"}
    ],
    "other_words": [
      {"word": "大容量", "tag": "热词", "description": "类目热搜词，排名5"}
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
1. 同时显示原标题（old_title）和新标题（new_title）
2. 显示优化说明（optimize_reason）
3. 如有推荐词（other_words），可一并展示供参考
