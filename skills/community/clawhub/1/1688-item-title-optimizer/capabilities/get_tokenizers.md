# get_tokenizers — 获取分词器列表

## 功能说明

获取所有可用的分词器列表及说明。根据用户需求或 prompt 选择合适的分词器。如果用户没有指定，选择默认分词器（列表第一个）。

## 前置条件

- 已配置 AK（通过 `cli.py configure YOUR_AK` 或设置环境变量 `ALI_1688_AK`）

## CLI 调用

```bash
python3 {baseDir}/cli.py get_tokenizers
```

**无参数**，返回所有可用分词器列表。

## 返回数据说明

成功时返回 `data` 对象，包含 `tokenizers` 数组：

| 字段 | 类型 | 说明 |
|------|------|------|
| tokenizer | String | 分词器类型标识 |
| desc | String | 分词器描述 |

## 输出格式

### 成功输出

```json
{
  "success": true,
  "markdown": "✅ 分词器列表获取成功",
  "data": {
    "tokenizers": [
      {"tokenizer": "qwen-flash", "desc": "使用qwen-flash模型进行分词"}
    ]
  }
}
```

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| AK 未配置 | 提示用户配置 AK |
| 签名无效（401） | 提示用户检查 AK 是否有效 |
| 请求被限流（429） | 建议用户等待 1-2 分钟后重试 |

## 使用说明

1. 获取分词器列表后，根据用户需求选择合适的分词器
2. 如果用户没有指定，默认使用列表中的第一个分词器
3. 选定的分词器类型可传入 `optimize_title` 的 `--tokenizer_type` 参数
