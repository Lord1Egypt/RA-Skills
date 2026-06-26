# 阿里云 OpenClaw Browser Relay 配置手册

## ⚠️ 重要说明

**Browser Relay (@openclaw/browser-relay) 是 OpenClaw 内部包，不在 npm 公开仓库中。**

目前有两种方案：

### 方案 A：本地 Browser Relay（推荐）✅
- 在本地 Mac 运行 Browser Relay
- 连接本地 Gateway
- 通过 SSH 隧道转发远程浏览器控制命令

### 方案 B：远程 Browser Relay（需要内部包）❌
- 需要 OpenClaw 团队提供内部包
- 或从 OpenClaw 源码编译

---

## 📊 配置信息（方案 A）

| 项目 | 值 |
|------|-----|
| 阿里云 IP | `47.115.54.84` |
| SSH 用户 | `root` |
| SSH 密码 | `Davinci@1984` |
| Gateway 端口（本地） | `18789` |
| Browser Relay 端口（本地） | `18792` |
| Gateway Token | `f9df2ba3bd91e46e81d186b5f74457c7043085cb9a1df4a3` |

---

## 🎯 方案 A：本地 Browser Relay（推荐）

### 步骤 1：检查本地是否已安装

```bash
# SSH 登录阿里云
ssh root@47.115.54.84
# 密码：Davinci@1984

# 在容器内安装 Browser Relay
docker exec openclaw sh -c 'cd /app && npm install @openclaw/browser-relay'

# 或者一次性执行
ssh root@47.115.54.84 "docker exec openclaw sh -c 'cd /app && npm install @openclaw/browser-relay'"
```

等待安装完成（约 2-5 分钟）。

---

### 步骤 2：启动 Browser Relay 服务

```bash
# 在容器内启动 Browser Relay（后台运行）
docker exec -d openclaw sh -c 'cd /app && npx @openclaw/browser-relay --port 18792 &'

# 或者通过 SSH 一次性执行
ssh root@47.115.54.84 "docker exec -d openclaw sh -c 'cd /app && npx @openclaw/browser-relay --port 18792 &'"
```

---

### 步骤 3：验证服务是否运行

```bash
# 检查端口是否监听
ssh root@47.115.54.84 "docker exec openclaw ss -tlnp | grep 18792"

# 或查看进程
ssh root@47.115.54.84 "docker exec openclaw ps aux | grep browser-relay"
```

应看到：
```
LISTEN  0  128  0.0.0.0:18792  0.0.0.0:*
```

---

### 步骤 4：建立 SSH 隧道（本地 Mac 执行）

```bash
# 先杀掉旧隧道（如果有）
pkill -f "ssh.*18792"

# 建立新的 SSH 隧道
ssh -f -N -L 18792:localhost:18792 root@47.115.54.84
# 密码：Davinci@1984
```

---

### 步骤 5：配置 Browser Relay 扩展

1. **点击 Chrome 扩展图标** 🦀
2. **打开设置** ⚙️
3. **填写配置：**

| 配置项 | 值 |
|--------|-----|
| **Port** | `18792` |
| **Gateway token** | `f9df2ba3bd91e46e81d186b5f74457c7043085cb9a1df4a3` |

4. **点击 Save**

---

### 步骤 6：验证连接

- ✅ 扩展图标变 **橙色 ON** → 成功
- ❌ 扩展图标显示 **!** 或红色 → 检查故障排查

---

## 🧪 测试浏览器控制

### 方式 A：通过飞书机器人

1. 在飞书中打开与 `阿里云 OpenClaw` 的聊天
2. 发送：
   ```
   打开 https://www.baidu.com
   截图
   ```

### 方式 B：通过阿里云 OpenClaw 网页版

1. 访问：`http://localhost:18790/#token=f9df2ba3bd91e46e81d186b5f74457c7043085cb9a1df4a3`
2. 在聊天中发送：
   ```
   打开 https://www.bing.com
   点击搜索框
   输入"OpenClaw"
   ```

### 方式 C：通过 Browser Relay 扩展

1. 打开任意网页（如 `https://www.github.com`）
2. 点击扩展图标 → **附加此标签页**
3. 在聊天中发送：
   ```
   截图
   点击第一个链接
   ```

---

## 🐛 故障排查

### 问题 1：扩展显示 "Gateway token rejected"

**原因**：Token 不匹配或服务未启动

**解决**：
```bash
# 1. 检查远程 Token
ssh root@47.115.54.84 "docker exec openclaw cat /home/node/.openclaw/openclaw.json | grep token"

# 2. 检查服务是否运行
ssh root@47.115.54.84 "docker exec openclaw ss -tlnp | grep 18792"

# 3. 重启 Browser Relay
ssh root@47.115.54.84 "docker exec -d openclaw sh -c 'pkill -f browser-relay; cd /app && npx @openclaw/browser-relay --port 18792 &'"

# 4. 重启 SSH 隧道
pkill -f "ssh.*18792"
ssh -f -N -L 18792:localhost:18792 root@47.115.54.84
```

---

### 问题 2：SSH 隧道无法建立

**错误**：`bind [127.0.0.1]:18792: Address already in use`

**解决**：
```bash
# 1. 查找占用端口的进程
lsof -i :18792

# 2. 杀掉进程
kill -9 <PID>

# 3. 或使用其他端口
ssh -f -N -L 18793:localhost:18792 root@47.115.54.84
# 扩展 Port 改为 18793
```

---

### 问题 3：Browser Relay 未运行

**检查**：
```bash
ssh root@47.115.54.84 "docker exec openclaw ps aux | grep browser-relay"
```

**解决**：
```bash
# 重新启动
ssh root@47.115.54.84 "docker exec -d openclaw sh -c 'cd /app && npx @openclaw/browser-relay --port 18792 &'"

# 查看日志
ssh root@47.115.54.84 "docker logs openclaw | grep browser"
```

---

### 问题 4：扩展无法连接

**检查 SSH 隧道**：
```bash
ps aux | grep "ssh.*18792"
curl -s -o /dev/null -w "%{http_code}" http://localhost:18792/
```

**重新建立隧道**：
```bash
pkill -f "ssh.*18792"
ssh -f -N -L 18792:localhost:18792 root@47.115.54.84
```

---

## 📝 快速命令汇总

```bash
# 安装 Browser Relay
ssh root@47.115.54.84 "docker exec openclaw sh -c 'cd /app && npm install @openclaw/browser-relay'"

# 启动 Browser Relay
ssh root@47.115.54.84 "docker exec -d openclaw sh -c 'cd /app && npx @openclaw/browser-relay --port 18792 &'"

# 建立 SSH 隧道
ssh -f -N -L 18792:localhost:18792 root@47.115.54.84

# 检查状态
ssh root@47.115.54.84 "docker exec openclaw ss -tlnp | grep 18792"

# 重启 Browser Relay
ssh root@47.115.54.84 "docker exec -d openclaw sh -c 'pkill -f browser-relay; cd /app && npx @openclaw/browser-relay --port 18792 &'"

# 查看日志
ssh root@47.115.54.84 "docker logs openclaw | grep -i browser"
```

---

## ✅ 配置完成检查清单

- [ ] Browser Relay 已安装 (`/app/node_modules/@openclaw/browser-relay`)
- [ ] Browser Relay 服务已启动 (端口 18792 监听)
- [ ] SSH 隧道已建立 (18792 → 18792)
- [ ] 扩展配置正确 (Port: 18792, Token: 正确)
- [ ] 扩展图标显示橙色 ON
- [ ] 可以附加标签页
- [ ] 浏览器控制命令正常执行

---

## 🎯 使用示例

### 基础命令

```
打开 https://www.baidu.com
截图
关闭标签页
```

### 页面交互

```
点击搜索框
输入"OpenClaw 教程"
按回车
点击第一个搜索结果
```

### 高级操作

```
滚动到页面底部
获取页面标题
提取所有链接
```

---

## 📞 技术支持

### 查看完整日志

```bash
ssh root@47.115.54.84 "docker logs openclaw --tail 100"
```

### 检查所有服务

```bash
ssh root@47.115.54.84 "docker exec openclaw ss -tlnp"
```

### 重启所有服务

```bash
ssh root@47.115.54.84 "docker restart openclaw"
```

---

**配置完成！享受远程浏览器控制的便利！** 🎉
