# AI 回复指南 - 文件上传技能

## 何时触发

当用户询问以下问题时，使用本指南回复：

- "怎么上传文件？"
- "上传地址是什么？"
- "如何发送文件给你？"
- "能把文件传到哪里？"
- "有上传页面吗？"
- 类似的文件上传相关问题

---

## 回复原则

### ✅ 要做

1. **使用占位符** 隐藏敏感信息：
   - `<server-ip>` 代替真实 IP
   - `<port>` 代替真实端口
   - `<your-token>` 或 `<your-gateway-token>` 代替真实 token

2. **告诉用户如何获取 token**：
   - 路径：`~/.openclaw/openclaw.json`
   - 字段：`gateway.auth.token`

3. **提供完整的使用流程**：
   - 访问地址
   - 如何认证
   - 上传步骤
   - 上传后做什么

4. **保持友好和帮助性**

### ❌ 不要做

1. **不要暴露真实 token**（即使你知道）
2. **不要暴露服务器真实 IP**（如果在云端）
3. **不要假设用户知道配置路径**
4. **不要只给 URL 不给说明**

---

## 回复模板

### 模板 1: 标准回复

```
📁 你可以通过网页上传文件给我！

**上传地址：**
```
http://<server-ip>:<port>/?token=<your-token>
```

**🔐 获取 token：**
1. 查看配置文件：`~/.openclaw/openclaw.json`
2. 找到 `gateway.auth.token` 字段
3. 替换 URL 中的 `<your-token>`

**💡 使用步骤：**
1. 打开上传地址
2. 拖拽文件到上传区域（或点击选择文件）
3. 点击"上传文件"按钮
4. 上传成功后告诉我文件名

**📝 支持：**
- 中文文件名 ✅
- 多个文件 ✅
- 最大文件大小：50MB

上传完成后我就可以帮你分析文件内容了！
```

### 模板 2: 简洁回复

```
📤 文件上传地址：
```
http://<server-ip>:15170/?token=<your-gateway-token>
```

Token 在 `~/.openclaw/openclaw.json` 的 `gateway.auth.token` 字段。

上传成功后告诉我文件名即可！
```

### 模板 3: 首次使用引导

```
欢迎来到 OpenClaw！👋

想要上传文件给我，请按以下步骤操作：

**1️⃣ 获取你的 Gateway Token**
```bash
cat ~/.openclaw/openclaw.json | grep token
```

**2️⃣ 访问上传页面**
```
http://<server-ip>:15170/?token=<上一步获取的 token>
```

**3️⃣ 上传文件**
- 拖拽文件到页面
- 或点击选择文件
- 点击上传

**4️⃣ 告诉我文件名**
上传成功后，我会立即开始分析！

---

💡 **提示：**
- 上传页面支持中文文件名
- 单个文件最大 50MB
- 上传后文件保存在 `~/.openclaw/workspace/`

有任何问题随时问我！
```

### 模板 4: 安全提醒版

```
📁 文件上传功能已就绪！

**上传地址：**
```
http://127.0.0.1:15170/?token=<your-token>
```

**⚠️ 安全提示：**
- Token 是你的私密凭证，不要分享给他人
- 上传服务仅监听本地，不暴露到公网
- 上传的文件会保存在 `~/.openclaw/workspace/`

**🔐 查找 Token：**
```bash
grep '"token"' ~/.openclaw/openclaw.json
```

上传完成后告诉我文件名，我会帮你处理！
```

---

## 变量说明

| 变量 | 说明 | 示例值 |
|------|------|--------|
| `<server-ip>` | 服务器 IP 地址 | `127.0.0.1` 或 `<your-server-ip>` |
| `<port>` | 上传服务端口 | `15170` |
| `<your-token>` | 用户 Gateway Token | `<从配置获取>` |
| `<your-gateway-token>` | 同上 | `<从配置获取>` |

---

## 常见问题回复

### Q: token 在哪里？

```
🔐 Token 存储在你的 OpenClaw 配置文件中：

**位置：** `~/.openclaw/openclaw.json`

**查看命令：**
```bash
grep '"token"' ~/.openclaw/openclaw.json
```

**或手动打开：**
```bash
cat ~/.openclaw/openclaw.json
```

找到类似这样的内容：
```json
{
  "gateway": {
    "auth": {
      "token": "你的 token 在这里"
    }
  }
}
```

复制那个 token 值，替换上传 URL 中的 `<your-token>` 即可！
```

### Q: 上传失败怎么办？

```
上传失败可能有以下几个原因：

**1️⃣ 检查服务是否运行**
```bash
ps aux | grep upload-server
```

**2️⃣ 检查 token 是否正确**
- 确认 token 与 `~/.openclaw/openclaw.json` 中的一致
- 注意不要有多余空格

**3️⃣ 检查端口是否可访问**
```bash
netstat -tlnp | grep 15170
```

**4️⃣ 查看上传日志**
```bash
tail -f ~/.openclaw/workspace/upload-server.log
```

**5️⃣ 检查文件权限**
```bash
ls -la ~/.openclaw/workspace/
```

如果还是不行，把错误信息发给我，我帮你分析！
```

### Q: 支持哪些文件格式？

```
📝 支持任意文件格式！

上传服务不限制文件类型，常见的有：
- 📄 文档：PDF, DOCX, TXT, MD
- 📊 表格：XLSX, CSV
- 🖼️ 图片：JPG, PNG, GIF
- 💻 代码：JS, PY, JAVA, 等
- 📦 压缩包：ZIP, TAR, GZ

**限制：**
- 单个文件最大 50MB
- 文件名不能包含特殊字符（中文可以）

上传后我可以帮你：
- 分析文档内容
- 总结 PDF
- 检查代码
- 提取数据
- 等等...

试试上传一个文件吧！
```

---

## 示例对话

### 示例 1: 新用户

**用户**: 你好，我想上传一个 PDF 给你分析，怎么弄？

**AI**: 
```
👋 你好！上传 PDF 很简单：

📁 **上传地址：**
```
http://<server-ip>:15170/?token=<your-token>
```

**🔐 首次使用需要 token：**
1. 打开终端
2. 运行：`grep '"token"' ~/.openclaw/openclaw.json`
3. 复制输出的 token 值
4. 替换 URL 中的 `<your-token>`

**📤 上传步骤：**
1. 在浏览器打开上面的 URL
2. 拖拽 PDF 文件到页面
3. 点击"上传文件"
4. 成功后告诉我文件名

我收到后会立即帮你分析 PDF 内容！

有问题随时问我 😊
```

### 示例 2: 老用户

**用户**: 上传地址发我一下

**AI**: 
```
📤 文件上传地址：
```
http://<server-ip>:15170/?token=<your-token>
```

Token 还是从 `~/.openclaw/openclaw.json` 获取。

上传完告诉我就行！
```

### 示例 3: 安全敏感用户

**用户**: 上传安全吗？token 会不会泄露？

**AI**: 
```
🔐 很好的问题！上传服务采用了以下安全措施：

**✅ 安全特性：**
1. **Token 认证** - 复用 Gateway 的 token，不单独存储
2. **本地监听** - 默认仅监听本地，不暴露到公网
3. **HTTPS 可选** - 可通过反向代理启用 HTTPS
4. **文件名过滤** - 防止路径遍历攻击
5. **无日志存储** - 不记录文件内容

**⚠️ 注意事项：**
- 不要分享你的 token 给他人
- 确保防火墙未开放 15170 端口到公网
- 定期清理上传的文件

**🔒 最佳实践：**
```json
{
  "gateway": {
    "bind": "loopback",  // 仅本地访问
    "auth": {
      "mode": "token",
      "token": "强随机 token"
    }
  }
}
```

你可以放心使用！如果有额外安全需求，可以告诉我。
```

---

## 技能元数据

```json
{
  "name": "file-upload",
  "version": "1.0.0",
  "triggers": [
    "上传文件",
    "上传地址",
    "发送文件",
    "如何上传",
    "文件怎么传"
  ],
  "capabilities": [
    "file-upload",
    "workspace-write"
  ]
}
```
