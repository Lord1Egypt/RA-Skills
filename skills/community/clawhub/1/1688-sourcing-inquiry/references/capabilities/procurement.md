# 采购数字人使用指南

## 功能说明

采购数字人 Skill，支持用户通过自然语言描述采购需求，自动解析为结构化数据并发起采购任务。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）

## Agent 处理流程（核心）

```
1. 用户输入自然语言采购需求（如"帮我采购10件衣服，要求价格便宜"）
2. Agent 从用户消息中提取以下字段：
   - offerName: 商品名称（如"衣服"）
   - count: 采购数量（如"10"）
   - demand: 采购需求描述（如"价格便宜"）
3. 如果有字段缺失，Agent 需要主动询问用户补充：
   - 缺 offerName → "请问您要采购什么商品？"
   - 缺 count → "请问您要采购多少件？"
   - 缺 demand → "请问您对商品有什么要求？（如价格、质量、发货速度等）"
4. 所有字段齐全后，执行 CLI 命令
5. 检查输出：success=true → 告知用户采购任务已创建；success=false → 原样输出错误信息
```

### 自然语言解析示例

| 用户输入 | offerName | count | demand |
|---------|-----------|-------|--------|
| 采购10件衣服要求价格便宜 | 衣服 | 10 | 价格便宜 |
| 帮我买500个螺丝，要304不锈钢的 | 螺丝 | 500 | 304不锈钢 |
| 我需要采购一批手机壳 | 手机壳 | （需询问） | （需询问） |
| 200件T恤，纯棉的，要便宜 | T恤 | 200 | 纯棉，价格便宜 |

## CLI 调用

```bash
python3 {baseDir}/cli.py procurement --offerName "衣服" --count "10" --demand "价格便宜"
```

### 参数说明

| 参数 | 缩写 | 是否必填 | 说明 |
|------|------|----------|------|
| `--offerName` | `-n` | ✅ 是 | 商品名称 |
| `--count` | `-c` | ✅ 是 | 采购数量（纯数字，不含单位） |
| `--demand` | `-d` | ✅ 是 | 采购需求描述 |

### 调用示例

```bash
python3 {baseDir}/cli.py procurement -n "衣服" -c "10" -d "价格便宜"
python3 {baseDir}/cli.py procurement --offerName "螺丝" --count "500" --demand "304不锈钢，要求包邮"
```

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "✅ 采购任务已创建\n\n- **商品名称**: 衣服\n- **采购数量**: 10\n- **采购需求**: 价格便宜",
  "data": {
    "data": { ... }
  }
}
```

### 失败 — AK 未配置

```json
{
  "success": false,
  "markdown": "❌ AK 未配置，无法创建采购任务。\n\n运行: `cli.py configure YOUR_AK`",
  "data": { "data": {} }
}
```

### 失败 — 参数缺失

```json
{
  "success": false,
  "markdown": "❌ 参数错误：商品名称（offerName）不能为空",
  "data": { "data": {} }
}
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 参数缺失（offerName/count/demand） | 主动询问用户补充缺少的信息 |
| 用户输入模糊无法解析 | 逐一询问商品名称、数量、需求 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
