# 钉钉文档企业版技能 (dingtalk-doc-enterprise)

通过钉钉开放平台企业 API 管理钉钉文档，支持多用户场景，自动从钉钉连接器获取当前用户身份。

> 背景：我在使用openclaw和钉钉的官方连接器，但是他们不支持这些功能（最新版本0.8.13）。
>
> 这是我的issue： https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/issues/456
>
> 网上找遍了资源，也加入了钉钉开发群，都说不支持、还说没有操作文档的API。
>
> 连接器的文档说["钉钉文档能力依赖 MCP（Model Context Protocol）提供底层 tool"](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector?tab=readme-ov-file#%E9%92%89%E9%92%89%E6%96%87%E6%A1%A3docs%E4%B8%8E-mcpdocs) ，这种方案全是权限问题。
>
> [于是有了这个玩具。](https://clawhub.ai/shyzhen/dingtalk-doc-enterprise)

---

## 🚀 快速开始

### 1. 配置钉钉凭证

**推荐方式：编辑 `~/.openclaw/.env` 文件**

OpenClaw 会在启动时自动加载此文件中的环境变量，无需手动设置。

```bash
# ~/.openclaw/.env
DINGTALK_CLIENTID=dingxxxxxx
DINGTALK_CLIENTSECRET=your_secret
```

**获取凭证：**
1. 登录 [钉钉开放平台](https://open.dingtalk.com/)
2. 进入「应用开发」→「企业内部开发」
3. 创建或选择已有应用
4. 在「应用详情」页面获取 `AppKey` (ClientId) 和 `AppSecret` (ClientSecret)

**注意：** 修改 `.env` 文件后需要重启 OpenClaw Gateway 才能生效。

---

### 2. 申请应用权限

在钉钉开放平台「权限管理」中申请以下权限：

| 权限码 | 用途 | 必需 |
|--------|------|------|
| `qyapi_get_member` | 获取用户信息 | ✅ |
| `Storage.File.Read` | 读取文档内容 | ✅ |
| `Storage.File.Write` | 编辑/创建文档 | ✅ |

**申请步骤：**
1. 进入应用管理页面
2. 点击「权限管理」
3. 搜索上述权限码并申请
4. 等待管理员审批通过

### 3. 验证配置

重启 OpenClaw Gateway 后，可以通过以下方式验证配置是否生效：

```bash
# 检查环境变量是否加载
openclaw env | Select-String DINGTALK

# 或查看 Gateway 日志
openclaw logs --grep DINGTALK
```

---

## ✨ 核心特性

- ✅ **自动身份识别** - 从钉钉连接器消息自动获取发送者身份
- ✅ **多用户支持** - 企业内所有用户均可使用
- ✅ **权限隔离** - 每个用户只能操作自己有权限的文档
- ✅ **文档读取与修改** - 支持读取概览、查询块结构、覆写整篇内容、追加文本、删除块元素

---

## 📖 使用方式

### 自动触发（推荐）

**发送钉钉文档链接即可自动读取：**
```
https://alidocs.dingtalk.com/i/nodes/xxx
```

**文档链接 + 操作指令：**
```
帮我总结这篇文档：https://alidocs.dingtalk.com/i/nodes/xxx
在这篇文档里添加一段测试数据：https://alidocs.dingtalk.com/i/nodes/xxx
```

### 指令触发

| 操作 | 指令示例 |
|------|---------|
| 读取文档 | `读取钉钉文档 <链接>` |
| 总结文档 | `总结这篇文档：<链接>` |
| 更新文档 | `更新文档 <链接> 内容为...` |
| 追加内容 | `在文档指定段落后追加：<链接> 内容...` |
| 删除块元素 | `删除文档第 X 段：<链接>` |
| 查询结构 | `列出文档结构：<链接>` |

---

## 🔧 工作原理

```
用户发送消息 
    ↓
钉钉连接器接收
    ↓
OpenClaw 提取 sender_id
    ↓
查询用户 unionId
    ↓
作为 operatorId 调用钉钉 API
    ↓
返回结果给用户
```

---

## ⚠️ 注意事项

### 权限说明
- 每个用户只能操作**自己有权限访问**的文档
- 企业公开文档对所有用户可见
- 私有文档需要单独授权

### 限制
- 当前版本**不支持创建新文档**
- `read` 更适合快速概览；如果要总结文档或定位块，请先使用 `blocks`
- 追加和删除操作依赖 `blockId`，通常需要先查询结构
- 单次内容最大长度：50000 字符
- 频率限制：100 次/分钟/文档
- 块元素更新：目前仅支持段落类型

---

## 🐛 常见问题

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `forbidden.accessDenied` | 无文档权限 | 确认用户对文档有访问权限 |
| `docNotExist` | 文档不存在 | 检查文档 ID 是否正确 |
| `operatorId invalid` | 用户身份无效 | 检查钉钉连接器配置 |
| `paramError` | 参数错误 | 检查文档链接格式 |
| 缺少 `DINGTALK_CLIENTID` / `DINGTALK_CLIENTSECRET` | 未配置应用凭证 | 在 `~/.openclaw/.env` 中补齐并重启 Gateway |

---

## 📚 CLI 参考

脚本文件为同目录下的 `doc-enterprise.js`，常用命令如下：

```bash
node doc-enterprise.js read <docKey|url>
node doc-enterprise.js blocks <docKey|url>
node doc-enterprise.js update <docKey|url> "<markdown>"
node doc-enterprise.js append-text <docKey|url> <blockId> "<text>"
node doc-enterprise.js delete <docKey|url> <blockId>
```

- `read`：输出块列表和文本预览，适合快速查看
- `blocks`：输出完整块结构，适合总结文档或定位 `blockId`
- `update`：整篇覆写 Markdown 内容
- `append-text` / `delete`：需要已知 `blockId`

## 📚 API 参考

支持的钉钉文档 API 端点：

| 操作 | 端点 | 方法 |
|------|------|------|
| 覆写文档 | `/v1.0/doc/suites/documents/{docKey}/overwriteContent` | POST |
| 查询块元素 | `/v1.0/doc/suites/documents/{dentryUuid}/blocks` | GET |
| 插入块元素 | `/v1.0/doc/suites/documents/{dentryUuid}/blocks` | POST |
| 更新块元素 | `/v1.0/doc/suites/documents/{dentryUuid}/blocks/{blockId}` | PUT |
| 删除块元素 | `/v1.0/doc/suites/documents/{dentryUuid}/blocks/{blockId}` | DELETE |

---

**最后更新：** 2026-04-10  
**版本：** 1.0  
**作者：** Ash · ShyZhen
