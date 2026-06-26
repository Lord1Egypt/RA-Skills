# 排坑指南 / Troubleshooting

> Claude Code + 第三方 API 的常见坑点与解决方案。

---

## 1. `command not found: claude`

**原因**: Claude Code CLI 未安装，或安装后 PATH 未刷新。

**解决**:
```bash
npm install -g @anthropic-ai/claude-code
claude --version   # 验证
```

如果安装后仍然 `command not found`：
- **Mac / Linux**: 重新打开终端或运行 `source ~/.bashrc` / `source ~/.zshrc`
- **Windows (CMD)**: 关闭重新打开 CMD
- **Windows (PowerShell)**: 关闭重新打开 PowerShell，或运行 `refreshenv`

如果 npm 全局包路径不在 PATH 中：
```bash
npm config get prefix      # 查看 npm 全局路径
export PATH="$PATH:$(npm config get prefix)/bin"   # 临时加入 PATH
```

---

## 2. 401 Unauthorized — 认证失败

**最可能原因**: 用了错误的认证变量名。

**诊断**: 检查你用的是 `ANTHROPIC_AUTH_TOKEN` 还是 `ANTHROPIC_API_KEY`：

| Provider | 正确变量 |
|---|---|
| DeepSeek | `ANTHROPIC_AUTH_TOKEN` |
| Kimi | `ANTHROPIC_AUTH_TOKEN` |
| OpenRouter | `ANTHROPIC_API_KEY` |
| SiliconFlow | `ANTHROPIC_API_KEY` |

**另一个可能**: API Key 本身无效。到 Provider 的控制台重新生成一个试试。

---

## 3. 403 Forbidden — 权限拒绝

**原因**: API Key 有效但余额不足，或账户未激活。

**解决**:
- 去对应 Provider 控制台检查余额
- DeepSeek: https://platform.deepseek.com → 充值
- Kimi: https://platform.moonshot.cn → 充值

---

## 4. 上下文被截断（只显示 64K 而非 1M）

**原因**: 模型名后面没加 `[1m]` 后缀。

**解决**: 修改环境变量或 settings.json 中的模型名为 `deepseek-v4-pro[1m]`（注意是方括号，不是圆括号）。

**检查**:
```bash
echo $ANTHROPIC_MODEL       # Mac/Linux
echo $env:ANTHROPIC_MODEL    # Windows PowerShell
```
应该输出 `deepseek-v4-pro[1m]`。

如果输出是 `deepseek-v4-pro`（没有 `[1m]`）→ 加上后缀。

---

## 5. 模型列表里没有 DeepSeek 模型

**原因**: `ANTHROPIC_BASE_URL` 没设置对，Claude Code 还在用 Anthropic 官方端点。

**解决**:
```bash
# 检查当前设置
echo $ANTHROPIC_BASE_URL

# 应该输出:
# https://api.deepseek.com/anthropic
```

如果输出为空或 `https://api.anthropic.com` → 环境变量没设对。

**特别注意**: 在 Claude Code 里运行 `/status` 看当前连接的 Provider。

---

## 6. WSL2 中配置不生效

**原因**: settings.json 放在了 Windows 路径而非 WSL2 路径。

**解决**: WSL2 内的配置路径是 Linux 的 `~/.claude/settings.json`（即 `/home/用户名/.claude/settings.json`），不是 Windows 的 `C:\Users\...`。

**验证**:
```bash
# 在 WSL2 终端中
ls -la ~/.claude/
# 应该能看到 settings.json
```

---

## 7. 已有 Anthropic 登录时配置被覆盖

**原因**: Claude Code 检测到你曾经登录过 Anthropic 账号，优先使用账号 Token 而非环境变量。

**解决**:
```bash
# 清除已保存的 Anthropic 登录凭证
rm -rf ~/.claude/credentials.json   # 清除登录 Token
```

或者使用 `ANTHROPIC_BASE_URL` 指向非 Anthropic 端点——Claude Code 会自动切换为第三方认证方式。

---

## 8. npm 全局安装失败（Windows）

**原因**: Windows 缺少编译工具链，或者 npm 权限问题。

**解决**:
- 确保安装了 Git for Windows
- 使用 Windows Terminal 或 CMD（管理员模式）
- 如果报 `EACCES` 错误，检查 npm 全局路径权限：
  ```cmd
  npm config get prefix
  ```
  如果路径在 `C:\Program Files\` 下，改到用户目录：
  ```cmd
  npm config set prefix "%USERPROFILE%\AppData\Roaming\npm"
  ```

---

## 9. Claude Code 连接超时

**原因**: 国内网络访问部分 Provider 可能超时。

**解决**:
- 使用国内 Provider（DeepSeek/Kimi/Qwen）速度更快
- 如果使用 OpenRouter，可能需要代理
- 确认代理设置：
  ```bash
  export HTTP_PROXY="http://127.0.0.1:7890"
  export HTTPS_PROXY="http://127.0.0.1:7890"
  ```

---

## 10. Sub-agent 使用错误模型

**原因**: `CLAUDE_CODE_SUBAGENT_MODEL` 没设或设错了。

**解决**: 确保设置了 `CLAUDE_CODE_SUBAGENT_MODEL` 指向 Flash 级别的轻量模型（便宜且快）：

```bash
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
```
