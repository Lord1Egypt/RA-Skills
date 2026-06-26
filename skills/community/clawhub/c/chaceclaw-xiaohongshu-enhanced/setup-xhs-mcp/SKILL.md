---
name: setup-xhs-mcp
description: 小红书 MCP 服务部署和配置。首次使用或 MCP 连接失败时使用此 skill 完成部署。
emoji: 🔧
version: "1.0.0"
triggers:
  - 安装
  - 部署
  - 配置
  - 连不上
  - 第一次用
  - MCP
  - setup
---

# 🔧 setup-xhs-mcp

> 小红书 MCP 服务部署与配置指南

## 何时触发

用户提到以下任意表述时激活：
- "安装小红书 MCP"
- "部署配置"
- "连不上"
- "第一次用"
- "MCP 服务"
- `/setup-xhs-mcp`

---

## 前置检查

### Step 1: 确认 MCP 工具可用性

执行以下命令检查 `check_login_status` 是否在可用工具列表中：

```
/tools 查看可用 MCP 工具列表
```

查找是否存在：
- `check_login_status` ✅ 必备
- `search_feeds` ✅ 搜索
- `post_note` ✅ 发布

### Step 2: 判断状态

**工具存在** → MCP 服务已就绪，进入登录验证阶段

**工具不存在** → MCP 服务未配置，按下方部署流程执行

---

## 部署流程

### 方案一：npx 快速启动（推荐）

```bash
# 1. 安装 xiaohongshu-mcp
npx xiaohongshu-mcp@latest

# 2. 验证安装
npx xiaohongshu-mcp --version

# 3. 配置 OpenClaw MCP 集成
# 在 openclaw 配置文件中添加：
/openclaw config set mcp.services.xiaohongshu "npx xiaohongshu-mcp"
```

### 方案二：Docker 部署（生产环境）

```bash
# 1. 创建容器
docker pull xiaohongshu-mcp:latest

# 2. 运行容器（后台）
docker run -d \
  --name xhs-mcp \
  -p 3100:3100 \
  -v ~/.config/xhs-mcp:/data \
  xiaohongshu-mcp:latest

# 3. 验证运行状态
curl http://localhost:3100/health

# 4. 配置 OpenClaw 连接
/openclaw config set mcp.endpoints.xiaohongshu "http://localhost:3100"
```

---

## 认证配置

### Cookie 获取方法

**方式 A：浏览器插件（推荐）**
1. 安装 Chrome 扩展 "EditThisCookie"
2. 打开小红书网页并登录
3. 点击扩展图标 → 导出 Cookie
4. 复制 Cookie 字符串

**方式 B：开发者工具**
1. 打开小红书网页并登录
2. 按 F12 打开开发者工具
3. Application → Cookies → 复制全部 Cookie 值

### Token 配置

```bash
# 创建配置文件
mkdir -p ~/.config/xiaohongshu

# 写入认证信息
cat > ~/.config/xiaohongshu/config.json << 'EOF'
{
  "cookies": "你的Cookie字符串",
  "device_id": "设备ID（可选）",
  "update_interval": 43200
}
EOF

# 权限设置（防止泄露）
chmod 600 ~/.config/xiaohongshu/config.json
```

---

## 登录验证

### 验证 MCP 连接

```python
# 调用 check_login_status 验证
result = await mcp.check_login_status()

# 返回格式示例
{
  "logged_in": true,
  "user_id": "xxxxxxxx",
  "nickname": "用户名",
  "avatar_url": "https://...",
  "expires_at": "2026-05-01T00:00:00Z"
}
```

### 验证完整工具链

```python
# 按优先级逐一验证
tools_to_test = [
  ("check_login_status", "登录状态"),
  ("search_feeds", "搜索"),
  ("get_note_detail", "笔记详情"),
  ("get_user_profile", "博主主页"),
  ("post_note", "发布图文"),
  ("like_note", "点赞"),
  ("collect_note", "收藏"),
  ("comment_note", "评论"),
]

for tool_name, desc in tools_to_test:
    try:
        result = await mcp.call(tool_name)
        print(f"✅ {desc} ({tool_name}) 可用")
    except Exception as e:
        print(f"❌ {desc} ({tool_name}) 失败: {e}")
```

---

## 常见错误与解决

### 错误 1：MCP 服务未启动
```
Error: MCP service not available
```
**解决**：
```bash
# 检查进程
ps aux | grep xiaohongshu-mcp

# 重启服务
docker restart xhs-mcp

# 或重新安装
npx xiaohongshu-mcp --restart
```

### 错误 2：Cookie 已过期
```
Error: Cookie expired (10003)
```
**解决**：
1. 重新从浏览器获取最新 Cookie
2. 更新配置文件
3. 重启 MCP 服务

### 错误 3：Token 无效
```
Error: Unauthorized (401)
```
**解决**：
1. 确认 Cookie 格式正确（URL编码）
2. 检查 Cookie 是否包含必要的 `web_session`
3. 尝试重新扫码登录

### 错误 4：IP 被限制
```
Error: IP restricted
```
**解决**：
- 小红书对 IP 有风控，新 IP 需要 2-3 天适应期
- 避免使用数据中心 IP，用家庭宽带
- 减少操作频率，等待自动解封

### 错误 5：设备风控
```
Error: Device risk detected
```
**解决**：
- 首次使用建议使用手机热点
- 避免在公共场所 WiFi 下操作
- 使用浏览器插件获取的 Cookie 稳定性更高

---

## Token 自动刷新机制

### 配置自动刷新

```json
// ~/.config/xiaohongshu/config.json
{
  "cookies": "...",
  "auto_refresh": true,
  "refresh_threshold_hours": 12,
  "webhook_url": "可选：刷新成功通知URL"
}
```

### 手动刷新

```bash
# 调用刷新接口
curl -X POST http://localhost:3100/refresh \
  -H "Content-Type: application/json" \
  -d '{"force": true}'
```

### 刷新后验证

```python
# 刷新后必须重新验证
new_status = await mcp.check_login_status()
if new_status.logged_in:
    print("✅ Token 刷新成功")
else:
    print("❌ Token 刷新失败，请重新配置 Cookie")
```

---

## 多账号配置

```json
// ~/.config/xiaohongshu/accounts.json
{
  "accounts": [
    {
      "id": "account_1",
      "name": "主账号",
      "cookies": "主账号Cookie",
      "enabled": true
    },
    {
      "id": "account_2", 
      "name": "小号",
      "cookies": "小号Cookie",
      "enabled": false
    }
  ],
  "active_account": "account_1"
}
```

### 切换账号

```python
# 切换到指定账号
await mcp.switch_account("account_2")

# 验证切换
status = await mcp.check_login_status()
print(f"当前账号: {status.nickname}")
```

---

## 部署完成检查清单

```markdown
- [ ] npx xiaohongshu-mcp 安装成功
- [ ] MCP 服务运行正常（curl http://localhost:3100/health 返回 200）
- [ ] Cookie 已配置且有效
- [ ] check_login_status 返回 logged_in: true
- [ ] 所有核心 MCP 工具可用（至少验证 4 个）
- [ ] 限流文件 xhs-rate-limits.md 已加载
- [ ] 合规文件 xhs-compliance.md 已加载
```

---

*Version: 1.0.0 | Updated: 2026-04-23*