# file-upload-skill

OpenClaw 文件上传技能 - 通过网页上传文件到**本地 workspace**供 AI 分析

## 🎯 与其他上传技能的区别

**❌ 我们不是：**
- ❌ 云存储服务（不是上传到云端）
- ❌ 图床服务（不是获取外链）
- ❌ 文件分享工具（不是分享给他人）

**✅ 我们是：**
- ✅ **本地上传** - 文件保存在你的机器上
- ✅ **AI 分析** - 上传后让 AI 帮你分析文件内容
- ✅ **私有安全** - 文件不离开你的服务器
- ✅ **OpenClaw 集成** - 与你的 AI 助手无缝协作

**典型使用场景：**
```
1. 上传 PDF → AI 总结内容
2. 上传截屏 → AI 提取文字
3. 上传日志 → AI 分析问题
4. 上传代码 → AI 审查优化
```

---

## 功能

- 📁 网页端文件上传（支持拖拽）
- 🔐 **智能认证**：自动适配 Token/Password/无认证
- 🇨🇳 支持中文文件名
- 🚀 一键安装，自动配置
- 📦 独立服务，不影响 Gateway
- 🤖 AI 自动回答上传地址
- 📂 文件列表展示与管理
- 🗑️ 支持文件删除

## 快速开始

### 安装

```bash
# 方式 1: 从 ClawHub 安装（推荐）
openclaw skills install file-upload

# 方式 2: 本地安装
git clone <repo-url> ~/.openclaw/workspace/skills/file-upload
cd ~/.openclaw/workspace/skills/file-upload
./install.sh
```

### 使用

安装后自动启动上传服务，访问：

```
http://<server-ip>:15170/?token=<your-auth-value>
```

**🔐 认证说明：**
- 如果你的 Gateway 配置了 **token** → 使用 token
- 如果你的 Gateway 配置了 **password** → 使用 password
- 如果 **无认证** → 直接访问（建议配置认证）

**💡 如何获取认证值：**
```bash
# 查看你的认证配置
cat ~/.openclaw/openclaw.json | grep -A3 '"auth"'
```

### 询问 AI

用户可以直接问：
- "怎么上传文件给你？"
- "上传地址是什么？"
- "如何发送文件？"

AI 会自动回复正确的上传地址（隐藏敏感信息）

## 配置

### 环境变量

```bash
# 可选配置，默认值如下
export UPLOAD_PORT=15170           # 上传服务端口（可自定义）
export UPLOAD_PATH="/upload"       # 上传页面路径
export WORKSPACE="~/.openclaw/workspace"  # 文件保存目录
```

### 自定义端口

如果 15170 端口被占用，可以在安装前设置：

```bash
export UPLOAD_PORT=18888
openclaw skills install file-upload
```

### openclaw.json 配置

```json5
{
  "skills": {
    "file-upload": {
      "enabled": true,
      "port": 15170,
      "workspace": "~/.openclaw/workspace",
      "maxFileSize": "50MB",
      "autoStart": true
    }
  },
  "agents": {
    "defaults": {
      "env": {
        "UPLOAD_PORT": "15170",
        "UPLOAD_PATH": "/upload"
      }
    }
  }
}
```

## 🔐 认证兼容性

技能包支持所有 OpenClaw 认证方式：

| 认证方式 | 配置示例 | 技能包行为 |
|---------|---------|-----------|
| **Token 认证** | `"mode": "token"`<br>`"token": "xxx"` | ✅ 自动读取 token |
| **Password 认证** | `"mode": "password"`<br>`"password": "xxx"` | ✅ 自动读取 password |
| **无认证** | 无 `auth` 配置 | ⚠️ 空认证（建议配置） |
| **Tailscale** | `"allowTailscale": true` | ⚠️ 空认证 |

**前端统一使用：**
```
http://<server-ip>:15170/?token=<认证值>
```

后端会自动匹配 `gateway.auth.token` 或 `gateway.auth.password`。

详见：[docs/AUTH-COMPATIBILITY.md](docs/AUTH-COMPATIBILITY.md)

---

## AI 集成

### SKILL.md 指令

AI 会读取本文件，了解如何回答上传相关问题。关键指令：

```markdown
## 如何回答上传地址问题

当用户询问上传文件、发送文件、上传地址时：

1. **不要直接暴露 token/password**
2. **使用占位符**：`<your-auth-value>` 代替真实认证值
3. **提示用户从配置获取**：告诉用户在 `~/.openclaw/openclaw.json` 查找

标准回复模板：
```
📁 文件上传地址：
http://<server-ip>:15170/?token=<your-auth-value>

获取认证值：
1. 查看 ~/.openclaw/openclaw.json
2. 找到 gateway.auth.token 或 gateway.auth.password
3. 替换 URL 中的 <your-auth-value>

或者直接访问：http://<server-ip>:15170/
（无认证配置时不需要参数）
```
```

### 示例对话

**用户**: 怎么上传文件给你？

**AI**: 
```
📁 你可以通过网页上传文件给我！

上传地址：
http://<server-ip>:15170/?token=<your-auth-value>

🔐 获取认证值：
1. 查看配置文件：~/.openclaw/openclaw.json
2. 找到 gateway.auth.token 或 gateway.auth.password
3. 替换 URL 中的 <your-auth-value>

💡 使用步骤：
1. 打开上传地址
2. 拖拽文件到上传区域
3. 点击"上传文件"
4. 上传成功后告诉我文件名

支持中文文件名，最大 50MB。
```

**用户**: 上传地址是什么？

**AI**: 
```
📤 文件上传服务已启动！

访问地址：http://<server-ip>:15170/

认证方式：
- URL 参数：?token=<your-auth-value>
- 认证位置：~/.openclaw/openclaw.json → gateway.auth

上传的文件会保存到：~/openclaw/workspace/uploads/
上传成功后告诉我文件名，我可以帮你分析！
```

**用户**: 我没有配置 token，怎么办？

**AI**: 
```
🔐 没关系！如果你没有配置认证：

**临时使用（不推荐）：**
- 直接访问：http://127.0.0.1:15170/
- 不需要认证参数

**建议配置认证：**
```bash
# 生成随机 token
openclaw doctor --generate-gateway-token

# 或手动配置
openclaw config set gateway.auth.token $(openssl rand -hex 32)
```

配置后重启 Gateway 即可使用认证保护。
```

## 目录结构

```
file-upload/
├── SKILL.md                 # 技能说明（本文件）
├── package.json             # 技能元数据
├── install.sh               # 安装脚本
├── uninstall.sh             # 卸载脚本
├── src/
│   ├── upload-server.js     # 上传服务器
│   └── upload.html          # 上传页面
├── templates/
│   └── openclaw.json.template  # 配置模板
└── docs/
    └── README.md            # 详细文档
```

## 安全说明

### 认证安全
- ✅ **智能认证适配**：自动读取 token 或 password
- ✅ 认证值不在技能包中硬编码
- ✅ 认证值不在日志中明文显示
- ✅ 支持无认证降级（会提示警告）

### 文件系统安全
- ✅ 独立 `uploads/` 目录，与工作文件隔离
- ✅ 文件名 sanitization，防止路径遍历攻击
- ✅ 仅允许访问 uploads 目录
- ✅ 删除操作需要认证

### 网络安全
- ✅ CORS 头配置
- ✅ 仅监听指定端口
- ✅ 不自动暴露到公网
- ⚠️ 建议配合防火墙规则使用

详见：[SECURITY-AUDIT.md](SECURITY-AUDIT.md)

## 开发

```bash
# 本地测试
cd ~/.openclaw/workspace/skills/file-upload
node src/upload-server.js

# 查看日志
tail -f ~/.openclaw/workspace/upload-server.log
```

## 故障排查

### 无法访问上传页面

1. 检查服务是否运行：
```bash
ps aux | grep upload-server
```

2. 检查端口是否监听：
```bash
netstat -tlnp | grep 15170
```

3. 检查防火墙：
```bash
sudo iptables -L -n | grep 15170
```

### 上传失败

1. 查看日志：
```bash
tail -f ~/.openclaw/workspace/upload-server.log
```

2. **检查认证值是否正确：**
   - Token 用户：`cat ~/.openclaw/openclaw.json | grep '"token"'`
   - Password 用户：`cat ~/.openclaw/openclaw.json | grep '"password"'`

3. 检查文件权限：
```bash
ls -la ~/.openclaw/workspace/uploads/
```

4. **检查认证配置：**
```bash
# 查看当前认证模式
cat ~/.openclaw/openclaw.json | grep -A3 '"auth"'
```

### 认证问题

**问题**: 提示 "Invalid authentication"

**解决**:
1. 确认 URL 中的 token/password 与配置一致
2. 检查是否有空格或特殊字符
3. 重启上传服务：`systemctl restart openclaw-upload`

**问题**: 我没有配置认证

**解决**:
```bash
# 配置 token
openclaw config set gateway.auth.token $(openssl rand -hex 32)

# 重启 Gateway
openclaw gateway restart
```

## 许可证

MIT

## 更新日志

### v2.0.0 (2026-03-09)
- ✨ **新增：智能认证适配**（Token/Password/无认证）
- ✨ 新增：独立用户文件目录 `uploads/`
- ✨ 新增：Web 页面文件列表展示
- ✨ 新增：文件删除功能
- ✨ 新增：自动/手动刷新
- 🎨 改进：UI 美化，文件图标
- 🔐 安全：通过完整安全审计
- 📚 文档：新增认证兼容性说明

### v1.0.0 (2026-03-09)
- 初始版本
- 支持网页上传
- 支持中文文件名
- AI 自动回答上传地址
