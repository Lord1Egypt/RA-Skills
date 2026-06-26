---
name: feishu-quickstart-cn
version: 1.0.0
description: |
  飞书快速集成配置 - 5分钟连接 OpenClaw 与飞书，解锁文档管理、知识库、自动化工作流。适合：企业用户、团队协作、飞书生态。
metadata:
  openclaw:
    emoji: "🚀"
    version: 1.0.0
    requires:
      bins: ["curl"]
---

# 飞书快速集成配置

**目标**：5 分钟内完成 OpenClaw + 飞书集成，开始自动化办公。

---

## 🚀 快速开始（3 步）

### 第一步：创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 点击「创建企业自建应用」
3. 填写信息：
   - **应用名称**：OpenClaw Assistant
   - **应用描述**：AI 助手，自动化办公
4. 创建后记录：
   - `App ID`
   - `App Secret`

### 第二步：配置权限

在应用后台 → 「权限管理」→ 添加以下权限：

**文档权限（必选）**：
- `docx:document` - 读写文档
- `docx:document:readonly` - 读取文档
- `docx:document.block:convert` - 转换文档块
- `drive:drive` - 云空间访问

**知识库权限（可选）**：
- `wiki:wiki:readonly` - 读取知识库
- `wiki:wiki` - 读写知识库

**多维表格权限（可选）**：
- `bitable:bitable` - 读写多维表格
- `bitable:bitable:readonly` - 读取多维表格

### 第三步：配置 OpenClaw

在 OpenClaw 配置文件 `~/.openclaw/config.yml` 添加：

```yaml
channels:
  feishu:
    enabled: true
    appId: "cli_xxxxxxxxxxxx"      # 你的 App ID
    appSecret: "xxxxxxxxxxxxxxxx"  # 你的 App Secret
```

然后重启 OpenClaw：
```bash
openclaw gateway restart
```

---

## ✅ 验证集成

在 OpenClaw 对话中测试：

```
读取飞书文档 https://xxx.feishu.cn/docx/ABC123
```

如果成功返回文档内容，集成完成！

---

## 📋 常见使用场景

### 场景 1：自动生成周报

**指令**：
```
读取飞书文档 [项目文档链接]，提取本周进展，生成周报并保存到 [周报文档]
```

**OpenClaw 会自动**：
1. 读取项目文档
2. 提取关键信息
3. 生成周报 Markdown
4. 写入周报文档

### 场景 2：知识库管理

**指令**：
```
在飞书知识库 [空间名] 创建新页面「产品 FAQ」，内容如下：
[FAQ 内容]
```

**OpenClaw 会自动**：
1. 调用 `feishu_wiki` 创建页面
2. 调用 `feishu_doc` 写入内容
3. 返回页面链接

### 场景 3：多维表格自动化

**指令**：
```
读取飞书多维表格 [表格链接]，统计销售额，更新到汇总表
```

**OpenClaw 会自动**：
1. 调用 `feishu_bitable_list_records` 读取数据
2. 计算统计结果
3. 调用 `feishu_bitable_update_record` 更新汇总

---

## 🔧 高级配置

### 多租户支持（企业版）

如果需要管理多个飞书租户：

```yaml
channels:
  feishu:
    enabled: true
    tenants:
      - name: "公司A"
        appId: "cli_xxx"
        appSecret: "xxx"
      - name: "公司B"
        appId: "cli_yyy"
        appSecret: "yyy"
```

### Webhook 事件订阅（可选）

配置飞书事件推送，实现实时响应：

1. 在飞书应用后台 → 「事件订阅」
2. 配置 Request URL：`https://your-openclaw-domain/webhook/feishu`
3. 订阅事件：
   - `contact.user.created_v3` - 用户创建
   - `docx.document.created_v1` - 文档创建
   - `im.message.receive_v1` - 消息接收

---

## 🐛 故障排查

### 问题 1：权限不足

**错误**：`permission denied: docx:document`

**解决**：
1. 检查飞书应用权限配置
2. 确保已发布应用版本
3. 等待 5 分钟权限生效

### 问题 2：文档链接无法识别

**错误**：`invalid doc_token`

**解决**：
1. 确认链接格式：`https://xxx.feishu.cn/docx/ABC123`
2. 提取 `doc_token`：`ABC123`（/docx/ 后的部分）
3. 确保文档对应用可见

### 问题 3：表格写入失败

**错误**：`field type mismatch`

**解决**：
1. 使用 `feishu_bitable_list_fields` 查看字段类型
2. 确保数据格式匹配：
   - Text → `"string"`
   - Number → `123`
   - SingleSelect → `"Option"`
   - MultiSelect → `["A", "B"]`
   - DateTime → `timestamp_ms`

---

## 📚 相关 Skills

- `feishu-doc` - 文档读写操作
- `feishu-wiki` - 知识库管理
- `feishu-drive` - 云存储管理
- `feishu-perm` - 权限管理

---

## 💰 定价参考

- **基础集成**：¥99（环境检查 + 配置指导）
- **企业定制**：¥299（多租户 + Webhook + 培训）
- **全托管服务**：¥999/月（OpenClaw 托管 + 飞书集成 + 技术支持）

---

## 🆘 获取帮助

- **文档**：https://docs.openclaw.ai
- **社区**：https://discord.com/invite/clawd
- **飞书开放平台**：https://open.feishu.cn/document

---

**创建时间**：2026-03-21
**作者**：OpenClaw 中文生态
**版本**：1.0.0
