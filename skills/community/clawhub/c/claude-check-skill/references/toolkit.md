# 浏览器扩展与对话查找

体检脚本（`scripts/check.py`）已覆盖出口 IP、地区、类型、风险分、时区、评分和配置。下面两样按需使用，不随体检自动运行。

## 浏览器扩展（KYC + 浏览器出口）

`tools/ai-tools/extension/` 是完整的 Chrome MV3 扩展，默认未安装。安装流程见 [KYC 检查](kyc.md)。它提供：

- KYC 状态查询（用当前已登录的 Claude 页面，同源请求，不读 Cookie）。
- 浏览器 IPv4 / IPv6 出口、语言、时区——浏览器单独设代理时，这层出口可能与终端不同。
- WebRTC 候选，每次需手动确认才发请求。

权限仅 `activeTab`、`scripting` 和两个 ipify 域名；无后台进程、无存储、无遥测。结果只留在弹窗。KYC 的真实账号接口尚未验收，HTTP 403 只表示请求被拒，不等于审核被拒。

## 对话查找与导出（菜单第 5 项）

纯 Python，无第三方依赖：

```bash
python3 scripts/sessions.py --root ~/.claude/projects --q 关键词
python3 scripts/sessions.py --root ~/.claude/projects --key <上面列出的 key> --export 对话.md
```

支持 `--project`、`--since`、`--until`、`--json`。只读；跳过符号链接；最多 5000 个文件、单文件 50 MiB、合计 128 MiB；拒绝家目录和磁盘根目录。只解析 user / assistant 的文本，忽略工具调用内容，导出不含密钥。只在用户要求时运行，不随体检自动读取聊天；不上传，不修改原记录。导出的 Markdown 含对话原文，分享前自行脱敏。
