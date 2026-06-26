# 标题优化

## 功能说明

基于商品信息和用户意图，生成优化后的商品标题。

## 触发关键词

> 优化标题、生成标题、改标题

## CLI 调用

```bash
python3 {baseDir}/cli.py title_optimize \
  --offer_id "商品ID" \
  --prompt "用户原始query"
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--offer_id` / `-o` | 是 | 1688 商品 ID（纯数字） |
| `--prompt` / `-p` | 是 | 用户原始 query，**必须原封不动传入** |

## 输入来源

商品 ID 的提取规则参见商品信息查询（`references/20_product_info.md`）。

## prompt 原则

**必须严格遵守：**
- 用户的 query **原封不动**传入 `--prompt` 参数
- 不要去掉任何词语
- 不要改写、精简或翻译用户问题

## 输出格式

```json
{
  "success": true,
  "markdown": "标题优化完成！...",
  "data": {
    "title_result": "优化后的标题"
  }
}
```

## 结果展示

```
标题优化完成！

**优化后标题：**
{title_result}
```

## 异常处理

| 错误场景 | 处理方式 |
|----------|----------|
| success=false + "AK 未配置" | 触发 AK 配置流程（`references/10_ak_configure.md`） |
| "参数缺失" 或 "offer_id" | 提示用户提供商品 ID |
| 其他错误 | 原样输出 markdown 错误信息 |
