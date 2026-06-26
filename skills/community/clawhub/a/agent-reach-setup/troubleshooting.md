# Agent Reach 故障排除指南

## 常见问题

### 1. 权限问题

**症状**: `externally-managed-environment` 错误
```bash
error: externally-managed-environment
```

**解决方案**:
```bash
# 使用 --break-system-packages 参数
pip install https://github.com/Panniantong/agent-reach/archive/main.zip --break-system-packages
```

**原因**: Python 3.13+ 默认启用外部包管理保护

### 2. GitHub CLI 安装失败

**症状**: 权限不足或安装失败
```bash
[!] gh CLI install failed
```

**解决方案**:
- 手动安装: https://cli.github.com
- 或使用Snap: `sudo snap install gh`

### 3. Exa 搜索未配置

**症状**: mcporter已装但Exa未配置
```bash
[X] 全网语义搜索 — mcporter 已装但 Exa 未配置
```

**解决方案**:
```bash
mcporter config add exa https://mcp.exa.ai/mcp
```

### 4. 代理问题

**症状**: Reddit 或其他服务无法访问
```bash
-- Reddit 帖子和评论 — 无代理。服务器 IP 可能被 Reddit 封锁
```

**解决方案**:
```bash
agent-reach configure proxy http://user:pass@ip:port
```

### 5. 渠道配置问题

**症状**: 某些渠道显示为 `--` 或 `[X]`

**解决方案**:
1. 检查网络连接
2. 验证依赖是否安装
3. 参考具体渠道的配置指南

## 诊断命令

### 检查系统状态
```bash
agent-reach doctor
```

### 监控更新
```bash
agent-reach watch
```

### 检查版本
```bash
agent-reach check-update
```

## 系统要求

- **Python**: 3.13+
- **Node.js**: 22+
- **操作系统**: Linux, macOS, Windows (WSL)
- **权限**: 用户主目录写入权限

## 支持渠道

### ✅ 装好即用
- YouTube 视频和字幕
- RSS/Atom 订阅源
- 全网语义搜索
- 任意网页
- Twitter/X 推文
- B站视频和字幕
- 微信公众号文章

### 🔧 需要额外配置
- GitHub 仓库和代码
- Reddit 帖子和评论
- 小红书笔记
- 抖音短视频
- LinkedIn 职业社交
- Boss直聘职位搜索

## 获取帮助

- GitHub: https://github.com/Panniantong/agent-reach
- Issues: https://github.com/Panniantong/agent-reach/issues
- 文档: https://github.com/Panniantong/agent-reach/tree/main/docs