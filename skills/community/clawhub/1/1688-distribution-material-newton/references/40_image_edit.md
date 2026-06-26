# 图片编辑（异步提交 + 异步查询）

## 功能说明

使用 AI 对图片进行编辑优化，支持主图优化、背景替换、风格迁移等。该操作为**异步流程**：先提交任务，再自动轮询查询结果。

## CLI 调用

```bash
python3 {baseDir}/cli.py image_optimize \
  --image_urls "图片URL" \
  --prompt "用户原始query" \
  [--size "1:1"] \
  [--offer_id "商品ID"]
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--image_urls` / `-i` | 是 | 图片 URL 列表，英文逗号分隔。第 1 张为主图（待编辑图），后续为参考图 |
| `--prompt` / `-p` | 是 | 用户原始 query，**必须原封不动传入** |
| `--size` / `-s` | 否 | 输出比例：`1:1` / `2:3` / `9:16`，默认为空 |
| `--offer_id` / `-o` | 否 | 商品 ID |

## 异步机制

```
提交任务 → 获得 instance_id → 每 10 秒轮询一次 → 最长等待 3 分钟 → 返回结果
```

- 内部自动处理轮询，调用者无需额外操作
- 超时（3 分钟未完成）会抛出错误

## 多图传入规则

- **默认只传 1 张主图**
- **只有当用户明确说「以 XXX 为参考图」时**，才传入多张图片
- 参考图的 URL 放在主图**之后**
- 示例：`--image_urls "主图URL,参考图URL"`

## 并发调用

- 最多一次支持 **5 张图片**的并发优化
- 如需分别优化多张图片，Agent 可**并行**执行多个 `image_optimize` 命令
- 每个命令独立处理一张主图的优化

## prompt 原则

**必须严格遵守：**
- 用户的 query **原封不动**传入 `--prompt` 参数
- 不要去掉任何词语
- 不要改写、精简或翻译用户问题

## 输出格式

```json
{
  "success": true,
  "markdown": "图片优化完成！...",
  "data": {
    "gen_image_url": "生成的图片URL",
    "reasoning_context": "优化过程说明",
    "instance_id": "任务ID",
    "time_cost": "耗时（秒）",
    "raw_output": {}
  }
}
```

## 输出字段说明

- `gen_image_url`：最终生成的图片 URL
- `reasoning_context`：AI 生图过程的解释说明
- `instance_id`：异步任务 ID
- `time_cost`：耗时（秒）

## 结果展示

```
图片优化完成！

![优化后的图片](gen_image_url)

耗时：xx 秒

**优化说明：**
{reasoning_context}
```

## 异常处理

| 错误场景 | 处理方式 |
|----------|----------|
| success=false + "AK 未配置" | 触发 AK 配置流程（`references/10_ak_configure.md`） |
| "轮询超时" | 提示图片生成超时，建议稍后重试 |
| "限流" 或 "429" | 建议用户等待 1-2 分钟后重试 |
| 图片优化失败 | 展示失败原因（reasoning_context），建议调整 prompt 重试 |
