```markdown
# 微信通知发送指南

## 功能说明

通过 CLI 调用微信通知接口，向用户发送微信通知消息。

## 前置条件

- 已配置 AK（未配置时会提示运行 `cli.py configure YOUR_AK`）

## CLI 调用

```bash
python3 {baseDir}/cli.py wx_push --text "通知内容"
```

### 参数说明

| 参数 | 缩写 | 是否必填 | 说明 |
|------|------|----------|------|
| `--text` | `-x` | ✅ 是 | 微信通知内容（纯文本） |

### 调用示例

```bash
python3 {baseDir}/cli.py wx_push -x "您的订单已发货，请注意查收"
```

## 输出格式

### 成功

```json
{
  "success": true,
  "markdown": "微信通知发送成功",
  "data": {
    "data": { ... }
  }
}
```

### 失败 — AK 未配置

```json
{
  "success": false,
  "markdown": "❌ AK 未配置，无法发送微信通知。\n\n运行: `cli.py configure YOUR_AK`"
}
```

## Agent 处理流程

```
1. 从用户消息中提取：通知内容
2. 执行 python3 {baseDir}/cli.py wx_push --text <内容>
3. 检查输出：
   - success=true → 告知用户"微信通知已发送成功"
   - success=false → 原样输出错误信息
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| AK 未配置 | 引导用户执行 `cli.py configure YOUR_AK` 配置 AK |
| 参数缺失（text） | 提示用户补充通知内容 |
| 该用户没有与AI业务类型机器人的有效好友关系 | 提示用户到1688AI版工作台绑定微信账号 |
| 接口返回格式异常 | 提示"格式异常，请稍后重试" |
| 其他运行时异常 | 原样输出错误信息 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。
```
