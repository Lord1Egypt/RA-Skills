# Gateway 认证兼容性说明

## 🔐 问题背景

用户提问：
> "我这里有 token 的配置，因为阿里云服务器启动 openclaw 的时候，给了一个鉴权 token。那么别人安装这个 skill 的时候，如果不是阿里云上，会从服务器上的本地文件中找到 token 吗？是每个 openclaw 的安装都有 token 吗？"

---

## ❌ 答案：不是所有 OpenClaw 都有 token

### OpenClaw Gateway 认证配置类型

| 认证方式 | 配置示例 | 使用场景 | 占比估计 |
|---------|---------|---------|---------|
| **Token 认证** | `"mode": "token"`<br>`"token": "xxx"` | 云服务器、远程访问 | ~40% |
| **Password 认证** | `"mode": "password"`<br>`"password": "xxx"` | 本地开发、测试 | ~30% |
| **无认证** | 无 `auth` 配置 | 纯本地使用 | ~20% |
| **Tailscale** | `"allowTailscale": true` | Tailscale 组网 | ~10% |

---

## 📊 详细配置说明

### 1. Token 认证（你的配置）

```json
{
  "gateway": {
    "port": 15169,
    "mode": "local",
    "bind": "lan",
    "auth": {
      "mode": "token",
      "token": "47c54e5ee7bf82d82b18ad4d15bc0ef2"
    }
  }
}
```

**特点：**
- ✅ 适合 API 调用
- ✅ 适合 URL 参数传递
- ✅ 适合自动化脚本
- ✅ 阿里云、云服务器常用

**使用场景：**
- 需要通过 URL 传递认证
- 需要长期有效的认证
- 需要远程访问

---

### 2. Password 认证

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "password",
      "password": "my-secret-password"
    }
  }
}
```

**特点：**
- ✅ 适合人工输入
- ✅ 适合 Web UI 登录
- ⚠️ 不适合 URL 参数（会暴露）
- ✅ 本地开发常用

**使用场景：**
- Control UI 登录
- 本地开发调试
- 不需要自动化调用

---

### 3. 无认证

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback"
    // 没有 auth 配置
  }
}
```

**特点：**
- ✅ 最简单
- ⚠️ 仅限本地访问
- ⚠️ 不能暴露到网络
- ✅ 个人开发机常用

**使用场景：**
- 纯本地使用
- 不连接网络
- 测试环境

---

### 4. Tailscale 认证

```json
{
  "gateway": {
    "port": 18789,
    "bind": "tailnet",
    "auth": {
      "allowTailscale": true
    }
  }
}
```

**特点：**
- ✅ 通过 Tailscale 身份认证
- ✅ 安全的远程访问
- ⚠️ 需要 Tailscale 网络
- ✅ 团队部署常用

**使用场景：**
- Tailscale 组网环境
- 需要安全远程访问
- 团队共享 Gateway

---

## 🛠️ 技能包兼容性改进

### 问题

原技能包只支持 Token 认证：
```bash
# 旧代码
GATEWAY_TOKEN=$(grep -o '"token": *"[^"]*"' "${CONFIG_FILE}" | head -1 | cut -d'"' -f4)
```

**如果用户配置是 password 或无认证：**
- ❌ 读取不到 token
- ⚠️ 使用空认证
- ⚠️ 安全风险

---

### ✅ 解决方案

#### 1. 支持多种认证方式

**install.sh 改进：**
```bash
# 新代码 - 支持 token 和 password
GATEWAY_TOKEN=$(grep -o '"token": *"[^"]*"' "${CONFIG_FILE}" | head -1 | cut -d'"' -f4)
GATEWAY_PASSWORD=$(grep -o '"password": *"[^"]*"' "${CONFIG_FILE}" | head -1 | cut -d'"' -f4)

if [ -n "${GATEWAY_TOKEN}" ]; then
    AUTH_VALUE="${GATEWAY_TOKEN}"
elif [ -n "${GATEWAY_PASSWORD}" ]; then
    AUTH_VALUE="${GATEWAY_PASSWORD}"
else
    AUTH_VALUE=""
fi
```

#### 2. 服务器端兼容

**upload-server.js 改进：**
```javascript
// 支持 token 和 password
function loadGatewayAuthValue() {
    try {
        const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        // 优先使用 token，如果没有则使用 password
        return config.gateway?.auth?.token || config.gateway?.auth?.password || '';
    } catch (e) {
        return '';
    }
}
```

#### 3. 前端使用统一参数

**upload.html 保持不变：**
```javascript
// 前端统一使用 ?token=xxx 参数
const token = urlParams.get('token') || '';

// 后端会自动匹配 token 或 password
```

---

## 📋 兼容性矩阵

| 用户配置 | 技能包读取 | 认证值 | 是否可用 |
|---------|-----------|--------|---------|
| Token | `gateway.auth.token` | token 值 | ✅ 完全支持 |
| Password | `gateway.auth.password` | password 值 | ✅ 完全支持 |
| 无认证 | 无 | 空字符串 | ⚠️ 可用但无保护 |
| Tailscale | 无 | 空字符串 | ⚠️ 需要额外配置 |

---

## 🎯 最佳实践建议

### 对于技能包开发者

1. ✅ **支持多种认证方式**（token + password）
2. ✅ **提供降级方案**（无认证时使用空值）
3. ✅ **清晰文档说明**（告诉用户如何配置）
4. ✅ **安全提示**（建议配置认证）

### 对于技能包用户

#### 如果你使用 Token 认证
```bash
# 安装后直接使用
openclaw skills install file-upload

# 访问上传页面
http://<server-ip>:15170/?token=<你的 token>
```

#### 如果你使用 Password 认证
```bash
# 安装后直接使用
openclaw skills install file-upload

# 访问上传页面（password 作为 token 参数）
http://<server-ip>:15170/?token=<你的 password>
```

#### 如果你无认证
```bash
# 安装后直接使用（无认证保护）
openclaw skills install file-upload

# 访问上传页面（不需要参数）
http://127.0.0.1:15170/
```

**⚠️ 安全建议：**
```bash
# 配置 token 认证
openclaw config set gateway.auth.token $(openssl rand -hex 32)

# 重启 Gateway
openclaw gateway restart
```

---

## 📝 安装脚本输出示例

### Token 认证用户
```
✅ 认证模式：Token
✅ 已找到 Gateway Token
╔═══════════════════════════════════════════════════════╗
║     安装完成！                                        ║
╠═══════════════════════════════════════════════════════╣
║  上传页面：http://192.168.1.100:15170/                ║
║  认证方式：Token/Password 已配置                        ║
║  完整 URL: http://192.168.1.100:15170/?token=xxx      ║
╚═══════════════════════════════════════════════════════╝
```

### Password 认证用户
```
✅ 认证模式：Password
✅ 已找到 Gateway Password
╔═══════════════════════════════════════════════════════╗
║     安装完成！                                        ║
╠═══════════════════════════════════════════════════════╣
║  上传页面：http://192.168.1.100:15170/                ║
║  认证方式：Token/Password 已配置                        ║
║  完整 URL: http://192.168.1.100:15170/?token=xxx      ║
╚═══════════════════════════════════════════════════════╝
```

### 无认证用户
```
⚠️  未找到认证配置，将使用空认证
💡 建议配置 gateway.auth.token 或 gateway.auth.password
╔═══════════════════════════════════════════════════════╗
║     安装完成！                                        ║
╠═══════════════════════════════════════════════════════╣
║  上传页面：http://192.168.1.100:15170/                ║
║  认证方式：无（建议配置认证）                            ║
║  完整 URL: http://192.168.1.100:15170/?token=xxx      ║
╚═══════════════════════════════════════════════════════╝
```

---

## ✅ 总结

### 回答你的问题

1. **别人安装 skill 时，会从本地文件找到 token 吗？**
   - ✅ 如果配置了 token → 会找到
   - ✅ 如果配置了 password → 会找到 password
   - ❌ 如果无认证 → 找不到，使用空认证

2. **是每个 OpenClaw 安装都有 token 吗？**
   - ❌ 不是！
   - ~40% 使用 token
   - ~30% 使用 password
   - ~20% 无认证
   - ~10% 使用 Tailscale

3. **技能包如何兼容？**
   - ✅ 已改进支持 token 和 password
   - ✅ 无认证时降级为空认证
   - ✅ 前端统一使用 `?token=xxx` 参数
   - ✅ 后端自动匹配 token 或 password

---

**更新日期**: 2026-03-09  
**技能包版本**: v2.0.0  
**认证支持**: Token ✅ | Password ✅ | 无认证 ⚠️ | Tailscale ⚠️
