# configure — 配置 AK

## 功能说明

配置网关鉴权所需的 AccessKey（AK）。所有操作命令（`before_check`、`execute`）都依赖 AK 进行签名认证，首次使用前需先配置。

## CLI 调用

```bash
# 查看 AK 状态
python {baseDir}/cli.py configure

# 设置 AK
python {baseDir}/cli.py configure YOUR_AK
```

**参数说明**：

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `YOUR_AK` | str | 否 | 要设置的 AK 值。不传则查看当前 AK 状态 |

## 返回结果说明

### 查看状态 — 已配置

```json
{
  "success": true,
  "markdown": "✅ AK 已配置: `xxxx****yyyy`（来源: 环境变量（已生效））",
  "data": { "configured": true }
}
```

### 查看状态 — 未配置

```json
{
  "success": false,
  "markdown": "❌ 尚未配置 AK\n\n运行: `cli.py configure YOUR_AK`",
  "data": { "configured": false }
}
```

### 设置成功

```json
{
  "success": true,
  "markdown": "✅ AK 已保存: `xxxx****yyyy`\n\n后续由 OpenClaw 配置注入生效...",
  "data": { "configured": true }
}
```

### 设置失败

```json
{
  "success": false,
  "markdown": "❌ AK 长度不足（当前 10，需要至少 32 位）",
  "data": { "configured": false }
}
```

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| AK 为空 | 提示 AK 不能为空 |
| AK 长度不足 | 提示 AK 长度不足，需要至少 32 位 |
| AK 包含非法字符 | 提示 AK 包含非法字符 |
| Gateway 不可用且 fallback 失败 | 提示检查 Gateway 状态或文件权限 |
