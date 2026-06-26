# AK 配置指南

## 获取 AK（引导用户）

当用户没有 AK 时，Agent 输出以下引导：

> 请先执行 `cli.py get_ak` 自动获取 AK；如果自动获取失败，请前往 https://clawhub.1688.com/ 登录后右上角点击🔑复制获取 AK 内容，然后执行 `python3 cli.py configure YOUR_AK`。

## AK 存储机制

AK 存储在本地文件 `{workspace}/.1688-AK/.ak_store.json` 中，不再依赖环境变量或 OpenClaw 配置文件。

## Agent 配置流程（核心）

用户告知 AK 后，Agent 按以下步骤执行：

```
1. 从用户消息中提取 AK 字符串
2. 执行 cli.py configure <AK>
3. 检查输出：success=true → 继续；success=false → 原样输出 markdown 错误信息
4. AK 配置后立即生效（存储在本地文件中，无需重启会话）
5. 继续用户的原始请求；若用户仅提供了 AK 没有其他请求，告知"配置成功"
```

## CLI 调用

### 配置 AK

```bash
python3 {baseDir}/cli.py configure YOUR_AK_HERE
```

### 查看配置状态

```bash
python3 {baseDir}/cli.py configure --status
```

### 重置 AK（清除旧 Token + 配置新 AK）

```bash
python3 {baseDir}/cli.py configure --reset NEW_AK_HERE
```

### 清除 AK（同时清除关联的 OAuth Token）

```bash
python3 {baseDir}/cli.py configure --clear
```

## 异常处理

| 场景 | Agent 应对 |
|------|-----------|
| configure 输出 success=false | 原样输出 markdown 错误信息 |
| 配置成功但后续命令仍报 AK 未配置 | 检查 AK 文件是否存在，必要时重新执行 configure |
| 用户问"我的 AK 在哪" | 输出上方获取 AK 引导话术 |
| 更换 AK 后旧 Token 仍生效 | 使用 `--reset` 参数重置 AK，会自动清除旧 Token |

通用 HTTP 异常（400/401/429/500）处理见 `references/common/error-handling.md`。