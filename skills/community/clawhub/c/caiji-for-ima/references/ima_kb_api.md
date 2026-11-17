# IMA MCP 工具签名与 ID 基线

## 工具清单（ima-mcp 连接器）
- `get_knowledge_base_list(types)` — types 为数组，元素取：
  `KBT_MINE_KB` / `KBT_SHARED_KB` / `KBT_SUBSCRIBED_JOIN_KB` / `KBT_SUBSCRIBED_CREATE_KB`
- `get_knowledge_list(knowledge_base_id, folder_id, limit, cursor)` — limit≤50；folder_id 为空串=根目录。
- `import_urls(knowledge_base_id, folder_id, urls)` — urls 数组，**每批 ≤10**；返回 results 每项含 ret_code（0=成功）与 media_id。
- `search_knowledge(knowledge_base_id, query, limit, folder_id?)` — folder_id 参数**不生效**（返回全库命中）；固定返回 top 100 条、is_end 恒 true、无 total_size；超 token 时自动落盘到 `~/.workbuddy/projects/<proj>/<session>/tool-results/`。
- 无删除 / 移动 / 复制（跨库）等写后管理接口。

## 知识库 ID 基线（琰辉老师，2026-08-31）
- 大学教师科研知识库 `7477193097634530`
  - 01 素材区 → 文章素材 `folder_7477306851341586`（科研痛点/误区素材）
  - 02 建构区 `folder_7477193294757754`（科研方法论素材）
- 教发老兵的个人知识库 `0019f0753dc07a84`（主力库，3.7 万篇）
- 大学教师课程知识库 `7462522072338318`

## 检索 / 导入命中判定
- `import_urls` 回执：每个 URL 对应 `{ret_code, media_id, ...}`；ret_code==0 即成功入库。
- 核验净增量：用子文件夹 `folder_info.file_number`（稳），知识库级 `total_size` 受并发写入干扰勿用。
- 幂等：同 URL 重复导同一 folder 折叠为同一条（media_id 由 URL 派生）；PDF 走文件哈希不折叠，会留多份。
- 220001：先查 URL 裸空格 → `%20` 重试；瞬时失败也常见，单条重试多成功。
- 220030：跨库 add_knowledge 权限不足，无法程序化跨库复制。
