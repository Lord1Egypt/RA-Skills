# 印象笔记 RESTful API 参考（Engine B）

> v2.0 新增。仅用于网页剪藏工作流。其他工作流仍走 EDAM Python SDK（见 `api.md`）。

## 鉴权

所有请求都需要 HTTP Header：

```
auth: $YX_AUTH_TOKEN
```

剪藏接口额外需要：

```
clipper-c-auth: $YX_AUTH_TOKEN
```

`YX_AUTH_TOKEN` 来源：https://app.yinxiang.com/third/skills-oauth/

格式：以 `S=s` 开头，例 `S=s12:U=...:E=...:C=...:P=...:A=yinxiang-skill:V=2:H=...`。

注意 `A=yinxiang-skill` 字段——这是与 EDAM Developer Token（`A=en-devtoken`）的关键区别。**两套 token 不通用**：旧 EVERNOTE_TOKEN 在 RESTful API 上返回 `8403 Invalid authToken`。

## 基础 URL

```
https://app.yinxiang.com
```

国际版 evernote.com 是否也提供同名 RESTful 通道未实测，建议中国大陆用户固定使用 `app.yinxiang.com`。

## 接口：网页剪藏

```
POST /third/clipper-gateway/restful/v1/clipAndSaveNote
Content-Type: text/plain
auth: <YX_AUTH_TOKEN>
clipper-c-auth: <YX_AUTH_TOKEN>

Body:
{
  "url": "https://example.com",
  "notebookGuid": "可选——指定笔记本"
}
```

**响应（成功）：**

```json
{
  "status": { "code": 8200, "msg": "" },
  "data": { "noteGuid": "b71d4021-d4a9-4337-98ea-51cf04afc004" }
}
```

**响应（鉴权失败，如用错 token 类型）：**

```json
{
  "status": { "code": 8403, "msg": "Invalid authToken" }
}
```

## 状态码速查（部分）

| code | 含义 |
|---|---|
| 8200 | 成功 |
| 8403 | 鉴权失败（token 无效/过期/通道不对）|
| 1107 | 搜索无结果（仅出现在 search API） |

## 其他可用接口（非本 skill 目前使用，仅供参考）

| 路径 | 用途 |
|---|---|
| `/third/ai-chat-note/grpc-api/search/searchNotesByFilter` | 列出/搜索笔记（支持 `keyword`） |
| `/third/ai-chat-note/grpc-api/search/listNoteBooks` | 列出笔记本 |
| `/third/ai-chat-note/grpc-api/search/listTags` | 列出标签 |
| `/third/ai-chat-note/grpc-api/search/getNoteDetail` | 获取笔记完整内容 |
| `/third/third-party-note-service/restful/v1/createNoteFromMCP` | 创建笔记（JSON body）|

> 这些接口本 skill 默认走 EDAM Python 引擎。仅当未来想完全移除 Python 依赖时才会切到 RESTful。

## 印象笔记官方 Skill 包

印象笔记官方 OpenClaw Skill 包包含本文所述全部 7 个 RESTful 接口的调用模板：

```
https://cdn.yinxiang.com/ai/yinxiang-skill-v1.0.2.zip
```

本 skill v2.0 的剪藏实现参照该 zip 内 SKILL.md 的"场景二：网页剪藏"段落，并做了 Claude Code 适配（环境变量注入而非 `openclaw config set`）。

---

*基于 2026-06-08 实测验证。所有响应示例为真实 API 返回。*
