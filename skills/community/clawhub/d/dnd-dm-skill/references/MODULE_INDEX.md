# 📖 模组索引（由 init.py 自动生成）

> 目标：运行模组时快速定位所需信息，减少上下文浪费。
> 每次切换模组时由 `code/module/init.py:init_module()` 重建此文件。

---

## 一、模组文件结构

各章节文件放置于 `modules/` 目录下。命名格式：
- `{模组名} - Ch.{章节号} {标题}.md`
- `{模组名}_{章节号} {标题}.md`
- 或 `{模组名} - {章节号}.md`

| 文件 | 用途 |
|------|------|
| `Ch.1 ...` | 第一章全文 |
| `Ch.2 ...` | 第二章全文 |
| ... | 后续章节依次列出 |

---

## 二、当前场景参考（动态加载）

详细数据通过场景索引按需加载，不在此处全文保留。
当前章节的场景数据见 `srd/scenes_index.json`。

### 场景索引

```
srd/scenes_index.json — 场景级行号索引（由 build_scene_index() 生成）
  每个场景包含：标题、起止行号、子节列表、关键词标签

加载规则：
  → 每次只加载 `_current_scene` 对应的场景原文行
  → 场景切换时调用 scene_index.set_current_scene() 更新
  → 同一章节内的场景切换不触发章节过渡协议

章节过渡时流程：
  1. builder.build_chapter_content(chapter_filepath, "Ch.N", module_name)
  2. → 内部调用 build_scene_index() 建立新章节的场景索引
  3. → save_scene_index() 保存到 srd/scenes_index.json
  4. → set_current_scene() 设置章节默认起始场景
```

---

## 三、章节过渡条件

章节过渡由存档中的 `completedNodes` 驱动。完成当前章节所有关键节点后，城主根据规则8.7（章节过渡协议）执行：

| 步骤 | 操作 |
|:----:|------|
| 1 | 确认章节结束条件（验证节点完成 + 存档） |
| 2 | 加载新章节文件 |
| 3 | `build_chapter_content()` — 构建场景索引 + 更新 MODULE_ARC.md |
| 4 | 开始新章节叙事 |
| 5 | 存档 |

> 所有操作不依赖特定模组名，通过 `scan_modules()` 自动发现模块文件。

---

## 四、玩家信息

角色状态 → `live_party.json`（由 `code/party/live.py` 管理）
世界状态 → `world_state.json`（由 `code/state/world.py` 管理）
剧情摘要 → `plot_summary.json`（由 `code/summary/generate.py` 管理，存档时自动生成）

以上内容在每次对话时动态摘要，不在此硬编码。
