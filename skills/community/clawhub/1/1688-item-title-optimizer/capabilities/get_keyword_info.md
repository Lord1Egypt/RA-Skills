# get_keyword_info — 获取关键词信息

## 功能说明

获取标题优化所需的全部关键词数据，包括类目热搜词、高曝光词、类目信息和商品属性。支持用户自定义关键词输入。

## 前置条件

- 已配置 AK（通过 `cli.py configure YOUR_AK` 或设置环境变量 `ALI_1688_AK`）

## CLI 调用

```bash
# 基础调用
python3 {baseDir}/cli.py get_keyword_info --item_id <商品ID>

# 添加自定义关键词
python3 {baseDir}/cli.py get_keyword_info --item_id <商品ID> --custom_keywords "保温杯;不锈钢;便携"
```

**参数说明**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `--item_id` | int | 是 | 商品ID |
| `--include_expo_words` | flag | 否 | 包含高曝光词（默认 True） |
| `--include_hot_words` | flag | 否 | 包含类目热搜词（默认 True） |
| `--custom_keywords` | str | 否 | 自定义关键词，分号分隔 |

## 返回数据说明

| 字段 | 类型 | 说明 |
|------|------|------|
| item_id | int | 商品ID |
| cate_id | int | 类目ID |
| cate_name | String | 类目名称 |
| hot_words | Array | 类目热搜词列表 |
| expo_words | Object | 高曝光词及曝光量 |
| custom_keywords | Array | 用户自定义关键词 |
| cpv | String | 商品属性 |
| original_title | String | 原标题 |

## 输出格式

### 成功输出

```json
{
  "success": true,
  "markdown": "✅ 关键词信息获取成功",
  "data": {
    "item_id": 123456789,
    "cate_id": 50000001,
    "cate_name": "保温杯/保温瓶",
    "hot_words": ["不锈钢", "保温杯", "便携", "大容量"],
    "expo_words": {"保温": 150, "水杯": 120},
    "custom_keywords": ["保温杯", "不锈钢", "大容量", "便携"],
    "cpv": "材质:不锈钢;容量:500ml",
    "original_title": "304不锈钢水杯"
  }
}
```

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| AK 未配置 | 提示用户配置 AK |
| 商品ID 未提供 | 提示用户提供 --item_id 参数 |
| 签名无效（401） | 提示用户检查 AK 是否有效 |
| 请求被限流（429） | 建议用户等待 1-2 分钟后重试 |
