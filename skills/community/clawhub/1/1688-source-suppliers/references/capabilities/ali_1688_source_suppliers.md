# 1688供应商查询指南

## 功能说明

通过 CLI 调用1688供应商查询接口，返回匹配到的供应商及工厂信息。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）

## CLI 调用

```bash
python3 cli.py ali_1688_source_suppliers --query "供应商名称"
```

### 参数说明

| 参数        | 缩写   | 是否必填 | 说明    |
|-----------|------|----------|-------|
| `--query` | `-q` | ✅ 是 | 供应商名称或关键字 |

### 调用示例

```bash
# 查询灯具供应商
python3 cli.py ali_1688_source_suppliers -q "灯具供应商"

# 查询常州地区的工厂
python3 cli.py ali_1688_source_suppliers -q "常州工厂"
```

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "供应商信息查询成功",
  "data": {
    "data": {
      // 供应商详细信息
    }
  }
}
```

### 失败 — AK 未配置

```json
{
  "success": false,
  "markdown": "❌ AK 未配置，无法查询1688供应商信息。\n\n运行: `cli.py configure YOUR_AK`"
}
```

### 失败 — 其他异常

```json
{
  "success": false,
  "markdown": "❌ 错误描述信息"
}
```

## Agent 处理流程

```
1. 从用户消息中提取：供应商名称或关键字
2. 执行 cli.py ali_1688_source_suppliers --query <供应商名称>
3. 检查输出：
   - success=true → 告知用户"供应商信息查询成功"
   - success=false → 原样输出错误信息
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 参数缺失（query） | 提示用户补充供应商名称或关键字 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。