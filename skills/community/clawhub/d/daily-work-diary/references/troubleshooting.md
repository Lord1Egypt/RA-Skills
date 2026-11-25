# 排错与坑位

## 通用

- **IMA OpenAPI 必须用 curl 子进程调用**，不要用 Python `urllib`/`requests`——header 会被大小写规范化，导致 403。`archive_diary.py` 已内置 curl 子进程封装。
- 接口有频率限制，报错 `code 200001` 时退避重试（3s/6s/9s…）。
- 凭据来自环境变量 `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`。
- **查重必须用实时列表接口**（`list_note` / `get_knowledge_list`），**不要用** `search_note` / `search_knowledge`：搜索接口有索引延迟，刚写入的内容短时间检索不到，会导致查重失效、产生重复件。
- **笔记标题取 md 首个非空行去掉 `#`**，不是文件名；笔记端查重按此标题比对。

## 笔记端

| 现象 | 原因 | 处理 |
|------|------|------|
| `210005 NOTE_NOT_OWNER` | 不是该笔记作者 | 不能改别人的笔记，跳过或新建 |
| `210009 CONTENT_SIZE_OVERLOAD` | 单篇过大 | 拆分写入 |
| `210035 FOLDER_NOT_EXIST` | 笔记本 ID 失效 | 用 `list_notebook` 重新取 `folder_id`（folder_type=0），更新 `config.json` |
| 追加变成新建 | 标题未精确命中 | 脚本按"标题完全相等"判断；标题变了会被视为新篇 |

> 笔记 API **不支持删除**，写错只能在客户端手动删。

## 知识库端

| 现象 | 原因 | 处理 |
|------|------|------|
| 上传后重复出现 | 用了搜索接口，索引延迟导致漏判 | 改用 `get_knowledge_list` 列目录实时比对；脚本已内置 |
| 目标文件夹不存在 | folder_id 与 kb 不匹配 | 用 `create_folder` 重建后更新 `config.json` |
| 返回结构取错层 | 业务字段在 `data` 下 | 知识库类接口返回体统一为 `{code,msg,data:{...}}` |

## 素材检索

- 取不到当天内容时：先按日期检索会话记录，再退回取当日摘要。
- 仍为空 → 如实告知用户，请其口述，**不要编造**。
