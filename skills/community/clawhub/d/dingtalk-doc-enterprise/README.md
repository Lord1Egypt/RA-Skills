# 钉钉文档企业版技能（dingtalk-doc-enterprise）

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
>
> 20260422 最新说明：支持白名单写入控制的使用这个skill https://clawhub.ai/shyzhen/dingtalk-doc

---

## 能力范围

- 根据钉钉文档 URL 读取文档内容和块结构
- 覆写已有文档内容
- 在已有文档中插入、修改、删除内容块
- 根据 OpenClaw 钉钉连接器提供的当前用户身份调用 API
- 不提供任何文档创建能力，包括创建空白文档
- 不删除文档实体；`delete` 只删除内容块
- 不列出或搜索用户文档

## 配置

在 OpenClaw 环境中配置：

```bash
# ~/.openclaw/.env
DINGTALK_CLIENTID=dingxxxxxx
DINGTALK_CLIENTSECRET=your_secret
```

修改配置后重启 OpenClaw Gateway。

在钉钉开放平台为企业内部应用申请：

| 权限码 | 用途 |
|---|---|
| `qyapi_get_member` | 将连接器提供的 sender_id 查询为 unionId |
| `Storage.File.Read` | 读取已有文档内容 |
| `Storage.File.Write` | 修改已有文档内容和内容块 |

`Storage.File.Write` 可能同时覆盖其他写入能力，但本 skill 的脚本和命令白名单均不实现创建文档接口。

## 当前用户身份

身份解析优先级：

1. `OPENCLAW_SENDER_ID`
2. `DINGTALK_SENDER_ID`
3. `DINGTALK_OPERATOR_ID`，仅用于本地调试回退

线上不要配置 `DINGTALK_OPERATOR_ID`。脚本会把当前 sender_id 查询为 unionId，并作为 `operatorId` 调用文档 API，因此最终权限由钉钉按照当前用户对目标文档的权限判定。

## CLI

```bash
node doc-enterprise.js read <docKey|url>
node doc-enterprise.js blocks <docKey|url>
node doc-enterprise.js update <docKey|url> "<markdown>"
node doc-enterprise.js insert <docKey|url> <position> "<text>"
node doc-enterprise.js modify <docKey|url> <blockId> "<text>"
node doc-enterprise.js delete <docKey|url> <blockId>
```

| 命令 | 含义 |
|---|---|
| `read` | 输出已有文档的内容块概览 |
| `blocks` | 输出完整块结构，用于总结或定位块 ID |
| `update` | 用 Markdown 覆写已有文档正文 |
| `insert` | 在已有文档中插入段落块，位置支持 `0` |
| `modify` | 替换已有段落块的文本 |
| `delete` | 删除已有文档中的指定内容块 |

脚本没有 `create`、`create-doc`、`create-workspace`、`copy` 等命令。未知命令会直接拒绝。

## 推荐操作流程

块级修改或删除前先读取结构：

```bash
node doc-enterprise.js blocks "https://alidocs.dingtalk.com/i/nodes/xxx"
node doc-enterprise.js modify "https://alidocs.dingtalk.com/i/nodes/xxx" <blockId> "新文本"
node doc-enterprise.js delete "https://alidocs.dingtalk.com/i/nodes/xxx" <blockId>
```

用户要求“追加一段”时，根据 `blocks` 返回的位置调用 `insert`。不再使用 `POST /paragraphs/{blockId}/text`：仓库中的 `dingtalk-doc` 已记录该接口在真实测试中返回 `InvalidAction.NotFound`。

## API 范围

| 操作 | 端点 | 方法 |
|---|---|---|
| 查询内容块 | `/v1.0/doc/suites/documents/{docKey}/blocks` | GET |
| 覆写已有文档 | `/v1.0/doc/suites/documents/{docKey}/overwriteContent` | POST |
| 插入内容块 | `/v1.0/doc/suites/documents/{docKey}/blocks` | POST |
| 修改内容块 | `/v1.0/doc/suites/documents/{docKey}/blocks/{blockId}` | PUT |
| 删除内容块 | `/v1.0/doc/suites/documents/{docKey}/blocks/{blockId}` | DELETE |

不包含创建或删除文档实体的 API。

## 常见错误

| 错误 | 处理 |
|---|---|
| 缺少 `DINGTALK_CLIENTID` / `DINGTALK_CLIENTSECRET` | 配置企业内部应用凭证并重启 Gateway |
| 缺少当前用户身份 | 检查连接器是否传入 `OPENCLAW_SENDER_ID` |
| `forbidden.accessDenied` | 检查当前用户的目标文档权限和应用权限 |
| `docNotExist` / `nodeNotExist` | 检查文档 URL 或 docKey |
| `blockNotExist` | 重新调用 `blocks` 获取当前块 ID |
| `paramError` | 检查 URL/docKey、blockId 和 position |

最后更新：2026-08-18
