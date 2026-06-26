---
name: baidudisk-mcp
description: Use Baidu Netdisk via mcporter + stdio MCP server with hot-reload token file credentials. Triggers when you need Baidu Netdisk operations (official 2.0 toolset + legacy aliases) from OpenClaw without storing access_token in repo files.
---

# baidudisk-mcp

Use this skill to run Baidu Netdisk tools through `mcporter`.

## 1) Enable server in mcporter

Run:

```bash
bash scripts/baidudisk_mcporter.sh register
```

This writes a `baidudisk` stdio server entry into `config/mcporter.json` with:

- command: `/home/linuxbrew/.linuxbrew/bin/uv`
- args: `--directory <workspace>/skills/baidudisk-mcp/server run netdisk.py`
- env: `BAIDU_NETDISK_TOKEN_FILE=~/.openclaw/credentials/baidudisk.json`

Check status:

```bash
bash scripts/baidudisk_mcporter.sh check
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json list baidudisk
```

## 2) Credential file and hot update

Credential file (local only):

`~/.openclaw/credentials/baidudisk.json`

Expected keys:

- `access_token` (required)
- `default_dir` (recommended)

Example (do not commit real token):

```json
{
  "access_token": "<redacted>",
  "default_dir": "/Openclaw/baidudisk"
}
```

The MCP server reads this file on **every tool call**.
So token rotation only needs editing this file; no server restart is required.

## 3) 2.0 tools

### 3.1 Official-aligned tools (主推)

四个基础列表接口与 MCP tool 对应关系：

- `/rest/2.0/xpan/file?method=list` → `file_list(dir?, limit?, order?, desc?, start?)`
- `/rest/2.0/xpan/file?method=imagelist` → `file_image_list(parent_path?, recursion?, page?, num?, order?, desc?, web=1)`
- `/rest/2.0/xpan/file?method=doclist` → `file_doc_list(parent_path?, recursion?, page?, num?, order?, desc?)`
- `/rest/2.0/xpan/file?method=videolist` → `file_video_list_api(parent_path?, recursion?, page?, num?, order?, desc?, web=1)`

另保留一个历史兼容视频工具（非官方 videolist 参数模型）：

- `file_video_list(dir?, recursion?, start?, limit?, order?, desc?)`（基于 `xpanfilelistall` 过滤视频）

其他工具：

- `category_info(category, parent_path='/', recursion=1)`
- `category_info_multi(categories, parent_path='/', recursion=1)`
- `image_gettags(type=1)`
- `image_gettags_summary(type=1, top=50)`
- `image_search(search_type, keyword, start=0, limit=100, size?)`
- `recent_list(category=3, start=0, limit=100, sortby?, order?, stime?, etime?, resolution='off')`
- `file_meta(fsids, dlink?, thumb?, extra?, needmedia?, path?)`
- `make_dir(path, parent_dir?)`
- `file_copy(src_path, dest_dir, new_name?, ondup?)`
- `file_copy_batch(items, ondup='newcopy', async_mode=1, chunk_size=100, dry_run=false, allow_dest_prefixes=['/Openclaw'])`
- `file_del(path, confirm)`
- `file_move(src_path, dest_dir, new_name?, ondup?)`
- `file_move_batch(items, ondup='fail', async_mode=1, chunk_size=100, dry_run=false, allow_dest_prefixes=['/Openclaw'])`
- `file_rename(path, new_name)`
- `file_rename_batch(items, async_mode=1, chunk_size=100, dry_run=false)`
- `file_upload_stdio(local_file_path, remote_dir?, remote_name?)`
- `file_upload_by_url(url, remote_dir?, remote_name?, timeout_s?, max_bytes?)`
- `file_upload_by_text(text, remote_dir?, remote_name?, max_chars?, max_bytes?)`
- `file_keyword_search(keyword, dir?, recursion?, num?, page?)`
- `file_semantics_search(...)`（当前 `unsupported` stub）
- `file_sharelink_set(...)`（当前 `unsupported` stub）
- `user_info()`
- `get_quota(checkexpire?, checkfree?)`

### 3.2 Legacy aliases (兼容保留)

- `list`
- `search`
- `mkdir`
- `move`
- `rename`
- `delete`
- `upload`
- `download`

## 4) mcporter examples

```bash
# 对齐 list：/rest/2.0/xpan/file?method=list
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_list dir=/ limit=3

# 对齐 imagelist：/rest/2.0/xpan/file?method=imagelist
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_image_list parent_path='/来自：iPhone' recursion=0 page=1 num=3 order=time desc=1

# 对齐 doclist：/rest/2.0/xpan/file?method=doclist
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_doc_list parent_path='/Openclaw' recursion=1 page=1 num=3 order=time desc=1

# 对齐 videolist：/rest/2.0/xpan/file?method=videolist
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_video_list_api parent_path='/' recursion=1 page=1 num=3 order=time desc=1
# 若根目录返回 count=0，可改 parent_path='/来自：iPhone' 或 '/Openclaw'

# 官方同名：关键词搜索
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_keyword_search keyword=invoice num=20

# 分类统计（单分类：图片=3）
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.category_info category=3 parent_path=/ recursion=1

# 分类统计（多分类：JSON array）
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.category_info_multi categories='[1,3,4,6]' parent_path=/ recursion=1

# 图片智能标签
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.image_gettags type=1

# 图片智能标签摘要（按 count 取前 20）
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.image_gettags_summary type=1 top=20

# 图片关键字检索（search_type=2 表示汉字）
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.image_search \
  search_type=2 keyword=截图 limit=20 size='c256_u256,c512_u512'

# 图片列表（imagelist，默认 web=1 返回缩略图字段）
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_image_list \
  parent_path='/Openclaw' recursion=1 page=1 num=10 order=time desc=1

# 按上传时间拉取最近图片
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.recent_list \
  category=3 limit=20 resolution=off

# 官方同名：创建目录
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.make_dir path=reports/2026

# 批量移动（默认 ondup=fail，不覆盖；dest 限制在 /Openclaw）
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_move_batch \
  items='[{"src_path":"/Openclaw/inbox/a.txt","dest_dir":"/Openclaw/archive"},{"src_path":"/Openclaw/inbox/b.txt","dest_dir":"/Openclaw/archive"}]' \
  chunk_size=100 async_mode=1

# 批量复制（显式冲突策略 newcopy：冲突时自动副本，不覆盖原文件）
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_copy_batch \
  items='[{"src_path":"/Openclaw/inbox/a.txt","dest_dir":"/Openclaw/archive"}]' \
  ondup=newcopy async_mode=1

# 批量重命名（dry_run 先演练）
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_rename_batch \
  items='[{"path":"/Openclaw/archive/a.txt","new_name":"a-20260228.txt"}]' \
  dry_run=true

# 官方同名：本地文件上传
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_upload_stdio local_file_path=/tmp/demo.txt

# 官方同名：按 URL 上传（HTTP/HTTPS，带大小/超时限制）
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_upload_by_url url=https://example.com/demo.txt remote_dir=/Openclaw/baidudisk

# 官方同名：文本上传
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.file_upload_by_text text='hello world' remote_name=hello.txt

# 官方同名：配额
mcporter --config /home/ubuntu/.openclaw/workspace/config/mcporter.json call baidudisk.get_quota
```

## 5) Batch return envelope（8.2）

`file_move_batch / file_copy_batch / file_rename_batch` 统一返回：

- `status`, `tool`, `dry_run`, `async_mode`, `ondup`, `chunk_size`
- `total_items`, `chunks`
- `summary`（`ok_chunks/failed_chunks/ok_items_est/failed_items_est`）
- `results`（每个 chunk：`chunk_index/items/request_preview/response(errno/taskid/info)`）
- `errors`（失败 chunk 的 `chunk_index/message/items_preview`）

## 6) Minimal self-check（不含 delete）

> 请不要直接用 `python3`（容易缺 `mcp` 依赖）。

```bash
cd /home/ubuntu/.openclaw/workspace/skills/baidudisk-mcp
server/.venv/bin/python server/selfcheck_batch_filemanager.py
server/.venv/bin/python server/selfcheck_misc_readonly.py
# 下两项为真实只读联网检查（需要 token）
BAIDU_NETDISK_TOKEN_FILE=~/.openclaw/credentials/baidudisk.json server/.venv/bin/python server/selfcheck_image_recent_readonly.py
BAIDU_NETDISK_TOKEN_FILE=~/.openclaw/credentials/baidudisk.json server/.venv/bin/python server/selfcheck_lists_readonly.py

# 等价写法（如果你用 uv）
# uv run --directory server python selfcheck_batch_filemanager.py
# uv run --directory server python selfcheck_misc_readonly.py
```

覆盖点：

- `file_move_batch`（10 条 + 分片降级）
- `file_copy_batch`（`ondup=fail` 与 `ondup=newcopy`）
- `file_rename_batch`
- `category_info(category=3, parent_path='/', recursion=1)`
- `image_gettags(type=1)`
- 四个列表基础能力（只读）：
  - `file_list(dir='/', limit=3)`
  - `file_image_list(parent_path='/来自：iPhone', recursion=0, page=1, num=3, order='time', desc=1)`
  - `file_doc_list(parent_path='/Openclaw', recursion=1, page=1, num=3, order='time', desc=1)`
  - `file_video_list_api(parent_path='/', recursion=1, page=1, num=3, order='time', desc=1)`（根目录为空时回退 `/来自：iPhone` / `/Openclaw`）

## 7) Safety defaults

- Never store `access_token` in repo files.
- Error messages sanitize `access_token` patterns.
- `delete/file_del` rejects by default unless `confirm="DELETE"`.
- Batch move/copy restricts destination by `allow_dest_prefixes`（默认 `['/Openclaw']`）。
- `file_move_batch` 默认 `ondup=fail`（不覆盖）；`file_copy_batch` 默认 `ondup=newcopy`（冲突产出副本，不覆盖）。
- `file_upload_by_url` only allows `http(s)` and rejects localhost / 内网 / 保留地址；并限制下载大小与超时。
