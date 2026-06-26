---
name: evernote-note
description: |
  印象笔记 API skill，用于管理用户的印象笔记。支持搜索笔记、浏览笔记本、获取笔记内容、新建笔记和追加内容。
  v2.0 新增：通过印象笔记官方 RESTful API 调用网页剪藏（Web Clipper），将任意 URL 的页面正文抓取并存入笔记。
  当用户提到印象笔记、Evernote、笔记、备忘录、记事、知识库，或者想要查找、阅读、创建、编辑笔记内容时，使用此 skill。
  即使用户没有明确说"笔记"，只要意图涉及个人文档的存取（如"帮我记一下"、"我之前写过一个关于XX的东西"、"把这段内容保存下来"），也应触发此 skill。
  当用户发送一个 URL 并说"剪藏"、"收藏到笔记"、"保存到印象笔记"时，使用本 skill 的剪藏工作流。
homepage: https://www.yinxiang.com
metadata:
  {
    "openclaw":
      {
        "emoji": "📔",
        "requires": { "env": ["EVERNOTE_TOKEN"] },
        "primaryEnv": "EVERNOTE_TOKEN"
      },
  }
---

# evernote-note

通过印象笔记 API 管理用户个人笔记，支持读取（搜索、列表、获取内容）和写入（新建、追加、剪藏）。

完整的数据结构和接口参数详见 `references/api.md`（EDAM 接口）和 `references/api-restful.md`（RESTful 接口，v2.0 新增）。

## 引擎与 Token（v2.0 新增）

本 skill 默认使用 **EDAM Python SDK**（Engine A），覆盖 95% 场景。
仅一个工作流（**网页剪藏**）走印象笔记 2026 年新发布的 **RESTful API**（Engine B），需要单独的 Token。

| 引擎 | Token 环境变量 | 走哪个工作流 | Token 来源 |
|---|---|---|---|
| **A（默认）** Python EDAM | `EVERNOTE_TOKEN` | 搜索 / 列出 / 读取 / 创建 / 追加 / 标签 | https://app.yinxiang.com/api/DeveloperToken.action |
| **B** RESTful curl | `YX_AUTH_TOKEN` | **仅网页剪藏** | https://app.yinxiang.com/third/skills-oauth/ |

> **不需要剪藏功能的用户**：只配 `EVERNOTE_TOKEN` 即可，与 v1.x 完全兼容。
> **需要剪藏的用户**：另去 OAuth Skills 页面拿一个 `YX_AUTH_TOKEN`（格式同样以 `S=s` 开头但发放主体不同，两套 token 不通用，已在 2026-06-08 实测验证）。

## Setup

### 选择认证方式

印象笔记支持两种认证方式，**推荐使用开发者令牌（更简单）**：

| 方式 | 适用场景 | 复杂度 | 说明 |
|------|---------|--------|------|
| **开发者令牌**（推荐） | 个人使用、测试脚本 | ⭐ 简单 | 直接使用，无需申请，只能访问自己的账户 |
| **API Key + OAuth** | 面向多用户的第三方应用 | ⭐⭐⭐ 复杂 | 需申请，支持多用户和高级功能 |

#### 方式一：开发者令牌（推荐）

1. **获取印象笔记开发者令牌**：
   - 国内版访问：https://app.yinxiang.com/api/DeveloperToken.action
   - 国际版访问：https://www.evernote.com/api/DeveloperToken.action
   - 点击"Create a developer token"生成令牌
   - 复制生成的 token（格式类似 `S=s1:U=8f219:E=154308dc976:C=14cd8dc9cd8:P=1cd:A=en-devtoken:V=2:H=1e4d28c7982faf6222ecf55df3a2e84b`）

2. **配置环境变量**：

```bash
# 国内版用户（默认）
export EVERNOTE_TOKEN="your_developer_token"
export EVERNOTE_HOST="app.yinxiang.com"

# 国际版用户（如使用的是国际版印象笔记）
export EVERNOTE_TOKEN="your_developer_token"
export EVERNOTE_HOST="www.evernote.com"
```

> 建议将上述 export 语句写入 `~/.zshrc` 或 `~/.bashrc`，避免每次重开终端失效。

#### 方式二：API Key + OAuth（可选）

如果需要开发面向多用户的第三方应用，需要：

1. **申请 API Key**：
   - 访问 https://dev.yinxiang.com/support/（需登录印象笔记账户）
   - 填写应用信息（名称、描述、权限等）
   - 等待审核（通常 1-5 个工作日）
   - 收到邮件后获取 Consumer Key 和 Consumer Secret

2. **实现 OAuth 流程**：
   - 参考 [OAuth 认证文档](https://dev.yinxiang.com/doc/articles/authentication.php)
   - 使用印象笔记 Python SDK 的 OAuth 功能

> **注意**：当前 skill 只支持开发者令牌方式。如需使用 OAuth，需要修改 skill 代码实现完整的 OAuth 流程。

### 安装 Python 依赖

**首次使用前**安装 Python 依赖：

```bash
pip3 install evernote2 oauth2
```

## 凭证预检

每次调用 API 前，先确认凭证可用。如果环境变量未设置，停止操作并提示用户按 Setup 步骤配置。

```bash
if [ -z "$EVERNOTE_TOKEN" ]; then
  echo "缺少印象笔记凭证，请按 Setup 步骤配置环境变量 EVERNOTE_TOKEN"
  exit 1
fi

# 检查 Python 依赖
python3 -c "import evernote2" 2>/dev/null || {
  echo "缺少 Python 依赖，请运行: pip3 install evernote2 oauth2"
  exit 1
}
```

## Python 初始化模板

所有操作前都需要初始化 EvernoteClient：

```python
import sys
import os
from evernote2.api.client import EvernoteClient
import evernote2.edam.notestore.ttypes as NoteStoreTypes
import evernote2.edam.type.ttypes as Types

# 从环境变量读取配置
developer_token = os.environ.get('EVERNOTE_TOKEN')
service_host = os.environ.get('EVERNOTE_HOST', 'app.yinxiang.com')

# 连接印象笔记
client = EvernoteClient(token=developer_token, service_host=service_host)
note_store = client.get_note_store()
```

> **注意**：根据实际 Python 环境调整 `sys.path.insert` 的路径，可通过 `pip3 show evernote2` 查看 `Location`。

## 辅助函数

```python
import re

def enml_to_text(enml):
    """将 ENML 转换为纯文本"""
    text = re.sub(r'<!DOCTYPE[^>]+>', '', enml)
    text = re.sub(r'<\?xml[^>]+\?>', '', enml)
    text = re.sub(r'<[^>]+>', '\n', enml)
    text = re.sub(r'\n+', '\n', text)
    return text.strip()

def text_to_enml(text):
    """将纯文本转换为 ENML 格式"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('\n', '<br/>')
    enml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>{text}</en-note>'''
    return enml
```

## 接口决策表

| 用户意图 | 引擎 | 调用 API | 关键参数 |
|---------|------|---------|---------|
| 搜索/查找笔记 | A (Python) | `findNotesMetadata()` | `NoteFilter.words` |
| 查看笔记本列表 | A (Python) | `listNotebooks()` | - |
| 浏览某笔记本里的笔记 | A (Python) | `findNotesMetadata()` | `NoteFilter.notebookGuid` |
| 读取笔记正文 | A (Python) | `getNoteContent()` | `note_guid` |
| 新建一篇笔记 | A (Python) | `createNote()` | `Note.title` + `Note.content`（ENML） |
| 往已有笔记追加内容 | A (Python) | `updateNote()` | 先 `getNote()` 获取，再 `updateNote()` 保存 |
| **从 URL 剪藏网页**（v2.0 新增）| **B (curl)** | `clipper-gateway/clipAndSaveNote` | `url`，可选 `notebookGuid` |

## 常用工作流

### 查找并阅读笔记

先搜索获取 `note_guid`，再用 `getNoteContent()` 读取正文：

```python
# 1. 按标题搜索
filter = NoteStoreTypes.NoteFilter()
filter.words = 'intitle:"会议纪要"'
result = note_store.findNotesMetadata(developer_token, filter, 0, 20, 
                                     NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True))

# 2. 读取正文
note_guid = result.notes[0].guid
content = note_store.getNoteContent(developer_token, note_guid)
text = enml_to_text(content)
```

### 浏览笔记本里的笔记

先拉笔记本列表获取 `notebookGuid`，再拉该笔记本下的笔记：

```python
# 1. 列出笔记本
notebooks = note_store.listNotebooks()

# 2. 拉取指定笔记本的笔记
filter = NoteStoreTypes.NoteFilter()
filter.notebookGuid = notebooks[0].guid  # 选择第一个笔记本
result = note_store.findNotesMetadata(developer_token, filter, 0, 20,
                                     NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True))
```

### 新建笔记

```python
# 新建到默认位置
note = Types.Note()
note.title = "笔记标题"
note.content = text_to_enml("笔记内容")
created = note_store.createNote(developer_token, note)

# 新建到指定笔记本
note = Types.Note()
note.title = "笔记标题"
note.content = text_to_enml("笔记内容")
note.notebookGuid = "笔记本_GUID"
created = note_store.createNote(developer_token, note)
```

### 追加内容到已有笔记

```python
# 获取笔记
note = note_store.getNote(developer_token, note_guid, True, False, False, False)

# 追加内容
note.content = note.content + "<br/><br/>" + text_to_enml("追加的内容")
note_store.updateNote(developer_token, note)
```

### 按关键词全文搜索

```python
filter = NoteStoreTypes.NoteFilter()
filter.words = 'SuccessFactors'
result = note_store.findNotesMetadata(developer_token, filter, 0, 20,
                                     NoteStoreTypes.NotesMetadataResultSpec(includeTitle=True))
```

### 网页剪藏（v2.0 新增，走 Engine B）

**触发词：** 用户消息含 URL + "剪藏" / "保存到笔记" / "收藏到印象笔记"

**前置检查：** 先确认 `YX_AUTH_TOKEN` 已配置（**与 EVERNOTE_TOKEN 不通用**）。如果未配置，提示用户：

> 网页剪藏需要单独的 Skills OAuth Token。请访问：
> https://app.yinxiang.com/third/skills-oauth/
> 生成 Token 后保存为 `YX_AUTH_TOKEN` 环境变量。

**实现：** 用 Bash 工具直接 curl 印象笔记 RESTful API（不需要 Python，零依赖）：

```bash
# 检查 token
if [ -z "$YX_AUTH_TOKEN" ]; then
  echo "缺少 YX_AUTH_TOKEN，剪藏不可用。请按上述提示配置。"
  exit 1
fi

# 剪藏（同步等待返回，确认成功）
curl -s -X POST \
  "https://app.yinxiang.com/third/clipper-gateway/restful/v1/clipAndSaveNote" \
  -H "Content-Type: text/plain" \
  -H "auth: $YX_AUTH_TOKEN" \
  -H "clipper-c-auth: $YX_AUTH_TOKEN" \
  -d "{\"url\":\"$URL\"}"
```

**指定笔记本时**，body 中追加 `"notebookGuid":"GUID"`：

```bash
-d "{\"url\":\"$URL\",\"notebookGuid\":\"$NOTEBOOK_GUID\"}"
```

**结果判断：**

- `status.code == 8200` 且 `data.noteGuid` 非空 → 剪藏成功，告诉用户笔记 GUID
- 其它 → 取 `status.msg` 反馈失败

**响应示例（成功）：**

```json
{
  "status": { "code": 8200, "msg": "" },
  "data": { "noteGuid": "b71d4021-d4a9-4337-98ea-51cf04afc004" }
}
```

**为什么这条走 curl 不走 Python：** 印象笔记的 EDAM SDK（`evernote2`）不提供 Web Clipper 接口。剪藏必须走 2026-05 新发布的 RESTful 通道（`clipper-gateway`），且该通道**只接受新 OAuth Skills Token**（`YX_AUTH_TOKEN`），不接受旧 Developer Token（实测 `EVERNOTE_TOKEN` 在此接口返回 `8403 Invalid authToken`）。

## 搜索语法

印象笔记支持丰富的搜索语法，可通过 `NoteFilter.words` 设置：

| 语法 | 说明 | 示例 |
|------|------|------|
| `关键词` | 全文搜索 | `SuccessFactors` |
| `intitle:关键词` | 标题包含 | `intitle:"项目管理"` |
| `-关键词` | 排除关键词 | `项目 -会议` |
| `关键词A OR 关键词B` | 或条件 | `SuccessFactors OR Workday` |
| `notebook:"笔记本名"` | 在指定笔记本 | `notebook:"工作"` |
| `created:yyyyMMdd` | 创建日期 | `created:20260301` |
| `updated:day-7` | 最近7天更新 | `updated:day-7` |
| `tag:标签名` | 包含标签 | `tag:重要` |

## 核心响应字段

**搜索结果**（`NoteMetadata`）：
- `guid`: 笔记 GUID
- `title`: 标题
- `updated`: 更新时间戳（毫秒）
- `notebookGuid`: 所属笔记本 GUID

**笔记本**（`Notebook`）：
- `guid`: 笔记本 GUID
- `name`: 名称
- `created`: 创建时间戳（毫秒）
- `defaultNotebook`: 是否为默认笔记本

完整字段定义见 `references/api.md`。

## 分页

**笔记搜索**（`findNotesMetadata`）：
- 首次：`offset: 0, maxNotes: 20`
- 翻页：递增 `offset`
- 建议每次最多获取 50 条，避免 API 频率限制

## 注意事项

- **API 频率限制**：印象笔记对 API 调用有频率限制，建议：
  - 搜索时限制返回数量（如 20-50 条）
  - 避免短时间内大量请求
  - 使用 `findNotesMetadata()` 进行元数据搜索，而非 `findNotes()`
- **开发者令牌安全**：开发者令牌可完全访问账户，请勿泄露
- **ENML 格式限制**：
  - 不支持所有 HTML 标签和属性
  - 媒体资源需单独处理
  - 嵌入的 HTML 标签会被清理
- **搜索限制**：搜索结果最多 1000 条，建议使用分页
- **UTF-8 编码**：笔记内容必须为 UTF-8 编码，从外部文件读取时需确保正确转码

> **隐私规则**：笔记内容属于用户隐私，在群聊场景中只展示标题和摘要，禁止展示笔记正文。

## 错误处理

| 错误类型 | 说明 | 建议处理 |
|---------|------|---------|
| `EDAMUserException` | 用户相关错误 | 检查令牌是否有效、权限是否足够 |
| `EDAMSystemException` | 系统错误 | 稍后重试 |
| `EDAMNotFoundException` | 资源不存在 | 检查 GUID 是否正确 |
| `EDAMDataConflictException` | 数据冲突 | 使用最新数据重试 |
| `EDAMPermissionDenied` | 权限不足 | 检查令牌权限 |

### EDAM errorCode 速查

| code | 含义 | 排查 |
|------|------|------|
| 2 | BAD_DATA_FORMAT | 参数格式错误 |
| 3 | PERMISSION_DENIED | 令牌权限不足 |
| 8 | INVALID_AUTH | 令牌无效 / **host 选错**（如 s12 token 用了 www.evernote.com） |
| 9 | AUTH_EXPIRED | **开发者令牌已过期**,需重新生成 |
| 11 | ENML_VALIDATION | ENML 内容不合规 |
| 12 | SHARD_UNAVAILABLE | shard 暂时不可达 |

### 令牌过期速查

开发者令牌到期日嵌在 token 的 `E=` 字段中(16 进制毫秒时间戳)。怀疑过期时先解码再判断,不要瞎试:

```python
# token: S=s12:U=321a48:E=19e5fd1a8b1:C=...:A=en-devtoken:V=2:H=...
import datetime
exp_hex = "19e5fd1a8b1"  # E= 字段
print(datetime.datetime.fromtimestamp(int(exp_hex, 16) / 1000))
# → 2027-04-08 ... 即过期日
```

EDAM errorCode=9 时,99% 是 token 过期,去 https://app.yinxiang.com/api/DeveloperToken.action 重新生成。

### Host 选择

token 中 `S=s12` 这类 shard 标识**不能**直接用来推断使用 yinxiang 还是 evernote,需要试错:

- 在 `app.yinxiang.com` 返回 **errorCode=9** → 说明 host 正确(token 被识别),只是过期
- 在 `www.evernote.com` 返回 **errorCode=8** → 说明 host 不对(token 不属于该服务)

中国大陆用户大多数情况下 host 应为 `app.yinxiang.com`,即使 token 看起来是 s12 等"海外样式"的 shard。

### Python 3.14 兼容性

`evernote2` 库依赖已被 Python 3.12+ 移除的 `inspect.getargspec`,在 Python 3.14 上 `client.get_note_store()` 会直接报 `AttributeError: module 'inspect' has no attribute 'getargspec'`。两种办法:

**办法 A(推荐):** 用 Python 3.12 跑(homebrew 上 `python3.12` 通常已装):

```bash
/opt/homebrew/bin/python3.12 your_script.py
```

**办法 B:** 在脚本最前面打猴子补丁(import evernote2 之前):

```python
import inspect
if not hasattr(inspect, 'getargspec'):
    from collections import namedtuple
    ArgSpec = namedtuple('ArgSpec', 'args varargs keywords defaults')
    def _getargspec(func):
        spec = inspect.getfullargspec(func)
        return ArgSpec(spec.args, spec.varargs, spec.varkw, spec.defaults)
    inspect.getargspec = _getargspec

from evernote2.api.client import EvernoteClient  # 必须在补丁之后
```

> 注意 Python 3.14 系统自带的 SSL 证书有时还会触发 `CERTIFICATE_VERIFY_FAILED`。一并切到 python3.12 通常最省事。

```python
from evernote2.edam.error.ttypes import EDAMUserException, EDAMSystemException

try:
    notebooks = note_store.listNotebooks()
except EDAMUserException as e:
    print(f"用户错误: {e}")
except EDAMSystemException as e:
    print(f"系统错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

## 参考资料

- 印象笔记开发者文档：https://dev.yinxiang.com/doc/
- ENML 规范：https://dev.yinxiang.com/doc/articles/enml.php
- 搜索语法：https://help.evernote.com/hc/zh-cn/articles/209005987
- Python SDK：https://github.com/yinxiang-dev/evernote-sdk-python
- evernote2 库：https://github.com/JackonYang/evernote2
