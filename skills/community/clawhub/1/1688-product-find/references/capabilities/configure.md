# Capability: configure (AK配置和管理)

## 使用示例

```bash
# 自动获取 AK（启动浏览器授权流程）
python3 {baseDir}/cli.py get_ak

# 配置 AK
python3 {baseDir}/cli.py configure YOUR_AK_HERE

# 查看 AK 配置状态（无参数等同于 --status）
python3 {baseDir}/cli.py configure
python3 {baseDir}/cli.py configure --status

# 重置 AK（清除旧 Token + 配置新 AK）
python3 {baseDir}/cli.py configure --reset NEW_AK_HERE

# 清除 AK（同时清除关联的 OAuth Token）
python3 {baseDir}/cli.py configure --clear

```

## 命令参数

| 参数形式 | 说明 |
|---------|------|
| `<AK>` | 直接配置新 AK。若已有旧 AK 且不同，自动清除旧 Token |
| `--status` | 查看当前 AK 配置状态（无参数调用时默认行为） |
| `--clear` | 清除 AK 并同步清除关联的 OAuth Token |
| `--reset <AK>` | 重置 AK：清除旧 Token → 写入新 AK |
| （无参数） | 等同于 `--status` |

## ⚠️ AK 检查机制（Agent 必读）

**判断 AK 是否已配置，不应仅依据用户消息或对话历史。** 正确做法：

1. **直接执行用户请求的搜索命令**（text_search / image_search / link_search / compare）
2. 如果 AK 未配置，CLI 会返回 `success: false` + "AK 未配置" 提示
3. 此时按下方「AK 缺失时的处理流程」应对

也可主动查询状态：`python3 {baseDir}/cli.py configure`（无参数）

**禁止以下行为**：
- ❌ 仅因对话中没出现过 AK 就认为未配置（AK 可能已持久化在配置文件中）
- ❌ 仅因之前配置过就认为仍有效（AK 可能已过期或被清除）
- ❌ 跳过 CLI 检查直接要求用户提供 AK
- ❌ 在搜索前主动调用 configure 检查（应直接执行搜索，让 CLI 自动判断）

## AK 缺失时的处理流程

当 CLI 返回 "AK 未配置" 错误时，Agent **按顺序**执行：

**第一步：自动获取（优先）**

```bash
python3 {baseDir}/cli.py get_ak
```

- 启动本地回调服务器 + 打开浏览器授权页面
- 用户在浏览器完成登录后，AK 自动保存
- `success: true` → 配置成功，**立即继续执行用户的原始请求**
- `success: false` → 进入第二步

**第二步：引导手动配置（回退）**

输出以下话术：

> 自动获取 AK 失败。请手动提供您的 AK（Access Key），用于接口调用的鉴权。
> 如果还没有 API_KEY，请前往 https://clawhub.1688.com/ 获取。

用户提供 AK 后执行：

```bash
python3 {baseDir}/cli.py configure <用户提供的AK>
```

配置成功后，**继续执行用户的原始请求**（如搜索商品）。

## 输出格式

所有输出为标准 JSON：

```json
{"success": bool, "markdown": "...", "data": {"configured": bool, "ak": "..."}}
```

| 场景 | success | markdown |
|------|---------|----------|
| 配置成功 | `true` | `✅ AK 设置成功` |
| 配置成功（替换旧 AK） | `true` | `✅ AK 设置成功\n\n旧的 1688 OAuth Token 已同步清除` |
| 重置成功 | `true` | `✅ AK 已重置\n\n旧的 1688 OAuth Token 已同步清除。` |
| 清除成功 | `true` | `AK 已清除，关联的 1688 OAuth Token 也已同步清除。` |
| 无需清除 | `true` | `当前未配置 AK，无需清除。` |
| 状态：已配置 | `true` | `AK 已配置。\n\n**AK**: \`xxx\`` |
| 状态：未配置 | `true` | `AK 未配置。` |
| AK 格式错误 | `false` | `❌ AK 长度不足（当前 N，需要至少 32 位）` |
| 写入失败 | `false` | `❌ AK 写入失败，请检查文件权限` |
| 缺少参数 | `false` | `缺少参数：\`--reset\` 后需要提供新的 AK` |

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| configure 输出 success=false | 原样输出 markdown 错误信息 |
| 配置成功但后续命令仍报 AK 未配置 | 提示用户新开会话或执行 `openclaw secrets reload`，必要时再重试 configure |
| 用户问"我的 AK 在哪" | 输出获取 AK 引导话术，引导前往 https://clawhub.1688.com/ 获取 |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。

---

## 附录：内部机制（Agent 无需主动操作）

以下为系统内部实现细节，Agent 了解即可，**不需要手动执行这些逻辑**。

### AK 校验规则

configure 内部会自动校验 AK 格式：
- 不能为空
- 长度至少 32 位
- 仅允许字母、数字及 `_-=` 字符

校验失败时 CLI 会返回明确的 `success: false` 错误信息。

### AK 读取优先级

系统内部按以下优先级自动读取 AK（Agent 无需关心路径细节）：

1. 环境变量 `ALI_1688_AK`（OpenClaw 平台注入，最高优先级）
2. 配置文件 `{workspace}/.1688-AK/.ak_store.json`（多个候选路径自动遍历）

配置文件格式：`{"ak": "..."}`

### Token 联动清除

以下操作会自动清除关联的 OAuth Token（Agent 无需手动清 Token）：

| 操作 | Token 清除条件 |
|------|--------------|
| `configure <AK>` | 仅当新旧 AK 不同时 |
| `--reset <AK>` | 始终清除 |
| `--clear` | 始终清除 |

Token 清除失败时静默忽略，不影响主流程。
