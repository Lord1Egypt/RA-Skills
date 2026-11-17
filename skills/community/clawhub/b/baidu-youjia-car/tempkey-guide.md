# 百度有驾 API Key 申请流程（临时 Key 完整指南）

当用户未配置 Key 时，按本文件完整流程引导用户申请 Key。

## 脚本说明

三个封装脚本位于本 skill 的 `scripts/` 目录：

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `send_code.py` | 校验手机号格式 + 发送短信验证码 | `youjia-send-code <phone>` |
| `create_key.py` | 校验验证码格式 + 创建 Key | `youjia-create-key <phone> <verify_code>` |
| `save_config.py` | 持久化写入本地配置，并覆盖环境变量 / `.env` | `youjia-save-config <phone> <key>` |

**本地配置文件路径：**
- macOS / Linux：`~/.youjia/key.json`
- Windows：`%USERPROFILE%\.youjia\key.json`

**覆盖规则（重要）：**
短信校验通过、接口返回新 Key 后，`save_config.py` 会：
1. 写入 / 覆盖 `~/.youjia/key.json` 中该手机号对应的 Key
2. **覆盖** 当前进程环境变量 `YOUJIA_API_KEY`
3. **覆盖** skill 包内 `.env` 中的 `YOUJIA_API_KEY`

避免旧 Key 因解析优先级（环境变量 → `.env` → key.json）继续生效。

---

## 执行流程

### 第一步：展示协议，引导输入手机号

向用户展示以下内容，**不得跳过**：

```
根据百度有驾的流程，我需要先向您展示相关协议，然后协助您创建 API Key。

📋 申请 Key 前，请阅读并同意以下协议：
《百度有驾用户服务协议》：https://m.yoojia.com/pages/my/statement?_swebfr=620011

提供手机号即视为已阅读并同意以上协议。

请输入您的手机号：
```

### 第二步：调用 `send_code.py`

收到手机号后立即调用，无需二次确认：

```bash
youjia-send-code <phone>
```

**脚本返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `error` | int | 0=成功，其他=失败 |
| `query_id` | string | 成功时返回 |
| `msg` | string | 失败时返回错误描述 |

**成功处理：** 向用户展示：
```
✅ 验证码已发送至 <手机号掩码，如 138****0000>，请注意查收。
请输入收到的 4 位验证码：
```

**失败处理（查下表）：**

| error | 向用户说的话 | 后续动作 |
|-------|-------------|----------|
| -1 | "网络连接异常，请检查网络后重试。" | 等待用户操作 |
| 其他 | "{msg}" | 等待用户操作 |

### 第三步：等待用户输入验证码

用户在对话框中回复 4 位验证码。

### 第四步：调用 `create_key.py`

```bash
youjia-create-key <phone> <verify_code>
```

**脚本返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `error` | int | 0=成功，其他=失败 |
| `key` | string | 成功时返回 Key（格式 sk-xxx） |
| `query_id` | string | 成功时返回 |
| `msg` | string | 失败时返回错误描述 |

**失败处理：**

| error | 向用户说的话 | 后续动作 |
|-------|-------------|----------|
| 53008 | "验证码错误，请重新输入（还可尝试 X 次）："（X = 3 - verify_error_count，见下方计数规则） | AI 上下文计数；达到上限后停止调脚本，提示"验证码已连续错误 3 次，请重新发送验证码"，清除计数器，引导回第二步 |
| -1 | "网络连接异常，请检查网络后重试。" | 等待用户操作 |
| 其他 | "{msg}" | 等待用户操作 |

> **模型不对任何错误码做自动重试，所有失败均将控制权交还用户。**

**`verify_error_count` 计数规则（AI 在对话上下文中维护）：**

```
初始值：0（流程开始时或重新发送验证码后重置）

收到 error == 53008 时：
  verify_error_count += 1
  剩余次数 = 3 - verify_error_count

  if 剩余次数 > 0:
    提示："验证码错误，请重新输入（还可尝试 {剩余次数} 次）："
    等待用户输入新验证码
  else:
    提示："验证码已连续错误 3 次，请重新发送验证码。"
    verify_error_count = 0
    引导回第二步

重新发送验证码后（无论何种原因触发）：
  verify_error_count = 0（必须重置）
```

### 第五步：调用 `save_config.py` 并输出结果

`create_key.py` 成功拿到 Key 后**必须**调用本步骤。无论是否为新 Key，都会覆盖本地环境变量与 `.env`，确保后续查询使用最新 Key。

```bash
youjia-save-config <phone> <key>
```

**脚本返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `is_new` | bool | `true`=新建/更新为新 Key，`false`=复用已有 Key |
| `write_success` | bool | `~/.youjia/key.json` 是否写入成功 |
| `env_updated` | bool | 环境变量 `YOUJIA_API_KEY` 与 skill 包内 `.env` 是否覆盖成功 |
| `msg` | string | 失败时返回原因 |

- `is_new=true` → 使用「申请成功」模板
- `is_new=false` → 使用「复用已有 Key」模板
- `write_success=false` → 正常展示结果，在输出末尾附加：
  `⚠️ 本地记录保存失败，请检查文件权限：~/.youjia/key.json`
- `env_updated=false` → 在输出末尾附加：
  `⚠️ 环境变量 / .env 覆盖失败，后续查询可能仍使用旧 Key`

---

## 输出模板

### 申请成功（`is_new=true`）

```
🎉 您的百度有驾 API Key 已创建成功！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 您的 Key
<key>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 使用方式
Key 已自动保存到本地配置，并已覆盖环境变量 `YOUJIA_API_KEY` 与 skill 包内 `.env`，之后查询汽车价格时将自动使用最新 Key。

📌 百度有驾官网：https://www.yoojia.com/

⚠️ 重要提示
   本 Key 已开通汽车价格查询能力（品牌、车系、车型详情、价格行情、经销商信息等）。
```

### 复用已有 Key（`is_new=false`）

```
ℹ️ 您已有一个有效的 Key，无需重复申请。

🔑 您的 Key
<key>
```

---

## 注意事项

1. **协议展示不可跳过**：无论何种触发场景，必须先展示协议后再收集手机号。
2. **禁止自动重试**：所有脚本调用失败（任何 error 码）均立即告知用户，将控制权交还用户，不做任何静默重试。
3. **验证码错误次数由 AI 维护**：`create_key.py` 不计数，AI 在对话上下文中用 `verify_error_count` 追踪；达到 3 次后停止调用脚本，引导用户重新发送验证码。
4. **手机号掩码展示**：对话中展示手机号时使用 `138****0000` 格式；本地文件中以明文手机号为 key（用于查询匹配）。
5. **持久化失败不阻断主流程**：`write_success=false` 时静默追加提示，Key 正常展示。
6. **新 Key 必须覆盖本地环境**：验证码校验通过后接口返回的 Key，经 `save_config.py` 写入时会强制覆盖 `YOUJIA_API_KEY` 环境变量与 skill 包内 `.env`，防止旧 Key 因解析优先级继续生效。`env_updated=false` 时追加提示，但不阻断展示。
