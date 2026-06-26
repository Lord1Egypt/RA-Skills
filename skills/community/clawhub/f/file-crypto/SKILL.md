---
name: file-crypto
description: 使用来布公司内置的 file-crypto SDK 对服务器本地文件进行加密或解密处理，以及获取 Agent 身份令牌（authId）。当用户提到"加密文件"、"解密文件"、"文件加密"、"文件解密"、"获取authId"、"获取鉴权"、"encrypt file"、"decrypt file"，或者提供了服务器文件路径并希望对其进行加解密操作时，必须使用此 skill。适用于单文件加密、单文件解密、批量加解密（多次调用）、获取 Agent 身份令牌等场景。只要涉及到 file-crypto 或来布文件加解密，都应优先触发此 skill。
---

# file-crypto — 文件加解密 Skill

## 关于本 Skill

本 skill 是来布公司内部 `file_crypto` SDK 的命令行使用封装，用于对**服务器本地文件**执行加密或解密处理，以及获取 Agent 身份令牌。

- **运行环境**：仅在来布公司服务器本地执行，不访问任何外部网络
- **数据流向**：文件读写均在服务器本地完成，不上传至第三方
- **身份令牌**：authId 是来布内部系统的用户身份标识，由公司自有后台签发，不涉及第三方凭证

---

## 前置知识

`file_crypto` SDK 已预装在服务器上，**必须在指定目录下调用**，且该目录下须存在 `file-crypto.json` 配置文件：

```
/data/endecode-win-linux
```

命令格式：

```bash
cd /data/endecode-win-linux
python3 -m file_crypto --action <encrypt|decrypt|getAuth> [业务参数]
```

### 参数说明

| 参数 | 必填条件 | 说明 |
|------|---------|------|
| `--action` | 必填 | 操作类型：`encrypt` / `decrypt` / `getAuth` |
| `--filePath` | `encrypt` / `decrypt` 时必填 | 待处理文件的完整物理路径 |
| `--authId` | `encrypt` / `decrypt` 时必填 | 用户身份令牌，最长 64 字符 |
| `--outputPath` | 可选 | 自定义输出文件路径；不传时自动生成（加密追加 `_encrypt`，解密追加 `_decrypt`） |
| `--expireTime` | 可选，仅 `encrypt` 生效 | 过期时间戳，必须为正整数 |
| `--agentId` | `getAuth` 时必填 | Agent 唯一标识，用于获取身份令牌 |

> **典型流程**：首次使用时，先执行 `getAuth` 获取 authId（有效期 15 天），再用该 authId 执行加解密操作。

---

## 执行流程

### 情况一：加密 / 解密文件

#### 第一步：确认参数

从用户输入中获取以下必填项：

1. **操作类型**：加密（`encrypt`）还是解密（`decrypt`）？
2. **文件路径**（`--filePath`）：完整的服务器物理路径
3. **用户身份令牌**（`--authId`）：由 `getAuth` 获取，最长 64 字符

可选项按需询问：
- 是否需要**自定义输出路径**（`--outputPath`）？
- 加密时是否需要设置**过期时间**（`--expireTime`，正整数时间戳）？

如果用户没有 authId，引导其先执行 `getAuth`（见情况二）。

#### 第二步：构造并执行命令

**加密（基础）：**
```bash
cd /data/endecode-win-linux && python3 -m file_crypto --action encrypt --filePath <文件路径> --authId <身份令牌>
```

**加密（含可选参数）：**
```bash
cd /data/endecode-win-linux && python3 -m file_crypto --action encrypt --filePath <文件路径> --authId <身份令牌> --outputPath <输出路径> --expireTime <时间戳>
```

**解密：**
```bash
cd /data/endecode-win-linux && python3 -m file_crypto --action decrypt --filePath <文件路径> --authId <身份令牌>
```

#### 第三步：解析结果

**✅ 成功**（`"code": 0`，`"success": true`）：

```json
{
  "code": 0,
  "message": "处理成功",
  "success": true,
  "data": {
    "sourceFilePath": "/data/upload/test.pdf",
    "targetFilePath": "/data/output/test_encrypt.pdf",
    "action": "encrypt"
  }
}
```

向用户报告原始路径（`sourceFilePath`）和处理后路径（`targetFilePath`）：

> ✅ 加密成功！
> - 原始文件：`/data/upload/test.pdf`
> - 处理后文件：`/data/output/test_encrypt.pdf`

**❌ 失败** — 优先使用 `errorType` 字段判断错误类型：

| errorType | code | message 示例 | 说明 | 建议提示 |
|-----------|------|-------------|------|---------|
| `param_error` | 400 | 请求参数非法 | 缺少必填参数，或 `--expireTime` 非正整数 | 检查 `--filePath`、`--authId` 是否传入，`--expireTime` 是否为正整数 |
| `path_error` | 400 | 文件路径非法 / 输出路径非法 | `filePath` 指向目录、`outputPath` 非法、输出目录不存在 | 确认路径是文件而非目录，输出目录是否存在 |
| `file_not_found` | 404 | 源文件不存在 | 文件路径不存在 | 确认文件路径是否正确，文件是否已上传至服务器 |
| `unsupported_format` | 400 | 非支持的加密格式 | 解密时无法从文件头读取有效 fileId，或文件头解析失败，该文件不是支持的加密格式 | 确认待解密文件是否由本工具加密生成，文件是否完整未损坏 |
| `permission_error` | 403 | 文件权限不足 | 文件读写权限不足，或后端返回会话失效 / 密钥不存在 | 检查文件权限，或重新执行 `getAuth` 获取新令牌 |
| `auth_error` | 401 | 鉴权失败 | authId 无效或已过期 | 确认 authId 是否正确，或重新执行 `getAuth` 获取新令牌（有效期 15 天） |
| `process_error` | 500 | 文件处理失败 | 底层处理失败、超时或后端返回异常 | 联系管理员查看服务器日志 |
| `config_error` | 500 | 配置文件错误 | `file-crypto.json` 缺失、格式错误或字段值非法 | 检查执行目录下 `file-crypto.json` 是否存在且格式正确 |

错误响应示例（`permission_error`）：
```json
{
  "code": 403,
  "message": "文件权限不足",
  "success": false,
  "errorType": "permission_error"
}
```

---

### 情况二：获取 Agent 身份令牌（getAuth）

当用户需要初次获取 authId，或令牌已过期时执行。

#### 第一步：确认参数

获取用户的 **Agent 标识**（`--agentId`）：由来布公司内部系统分配的唯一标识字符串。

#### 第二步：构造并执行命令

```bash
cd /data/endecode-win-linux && python3 -m file_crypto --action getAuth --agentId <Agent标识>
```

#### 第三步：解析结果

**✅ 成功**（`"code": "200"`，注意为字符串）：

```json
{
  "code": "200",
  "message": "success",
  "data": {
    "authId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  }
}
```

向用户返回 `data.authId` 的值：

> ✅ 获取成功！您的身份令牌为：
> `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
> 有效期 **15 天**，请保存备用，用于后续文件处理操作。

**❌ 失败**（透传后端返回，`code` 为字符串）：

```json
{
  "code": "500",
  "message": "agentId未绑定用户",
  "data": null
}
```

> ❌ 获取失败：agentId 未绑定用户。
> 请确认 agentId 是否正确，或联系管理员完成绑定。

---

## 批量处理

对多个文件逐一执行命令，汇总结果：

```
文件处理完成（3/3）：
✅ /data/upload/a.pdf → /data/output/a_encrypt.pdf
✅ /data/upload/b.pdf → /data/output/b_encrypt.pdf
❌ /data/upload/c.pdf → 失败（file_not_found：源文件不存在）
```

---

## 配置文件

执行目录下须存在 `file-crypto.json`，格式如下：

```json
{
  "endecode_path": "endecode",
  "api_base_url": "http://47.98.150.16:52027",
  "timeout_seconds": 30
}
```

如果命令返回 `config_error`，优先检查该文件是否存在及格式是否正确。

---

## 注意事项

- 本工具仅处理**服务器本地文件**，不支持本地桌面文件，不访问外部网络
- 命令**必须在 `/data/endecode-win-linux` 目录下执行**
- 文件路径区分大小写，请原样传入
- 身份令牌（authId）有效期为 **15 天**，过期后重新执行 `getAuth` 获取
- 错误处理时**优先判断 `errorType` 字段**，再参考 `code`
- `getAuth` 返回的 `code` 字段为**字符串**（`"200"`/`"500"`），与加解密的整数 code 不同
- 处理后的文件路径以实际 `targetFilePath` 返回值为准
