# 在本管线里用 MCP 执行

> 连接/安装/排障见 `blender-mcp` 技能；本文件只说**美术生产怎么用它**。
> 核验：2026-11-18 · 官方 add-on v1.0.3（20 个工具）

---

## 1. 工具选择表

| 要做的事 | 工具 | 注意 |
|---|---|---|
| 看场景里有什么 | `get_scene_info` / `get_objects_summary` | 先查再改，别假设 |
| 读对象细节 | `get_object_info` | 拿三角数/材质/变换 |
| 执行任意 bpy | `execute_blender_code` | 主力；**一次一段完整任务** |
| 视口截图 | `get_screenshot_of_window_as_image` | 比对循环用 |
| 渲染到文件 | `render_viewport_to_path` / `render_thumbnail_to_path` | 留证用 |
| 查文档 | `search_api_docs` / `get_python_api_docs` | 不确定 API 就查，别猜 |
| 批量重命名/整理 | `execute_blender_code`（自己写循环） | 不要一个个点 |

> ⚠️ README 里提到的 Poly Haven HDRI、Hyper3D/Hunyuan3D 生成**不在官方 add-on v1.0.3 的工具集里**（那是社区版附加）。别调用不存在的工具。

---

## 2. 执行协议（防翻车）

### 2.1 每次 `execute_blender_code` 的模板
```python
# 1) 幂等前置：不假设对象存在
import bpy
obj = bpy.data.objects.get("SM_Crate_01")
if obj is None:
    result = {"ok": False, "err": "not found"}
else:
    # 2) 做一件事
    ...
    # 3) 返回结构化结果（永远返回 dict）
    result = {"ok": True, "tris": ..., "mats": [...]}
```

**三条铁律**
1. **`result` 必须是 dict**（issue #64：返回非 dict 会断开）
2. **一段代码只做一件事**，便于定位；但也别细到每改一个属性一次调用（往返成本高）
3. **不写 `wm.quit_blender` / `wm.read_homefile`**（会断连接）

### 2.2 超时（已知坑）
- 症状：`execute_blender_code` 恒 120s 超时（issue **#72**；stdio 变体见 #58/#60/#48）
- 触发：MCP add-on 在 background 模式也起 server，抢 9876 并留非守护线程
- 处置：① 用 `--factory-startup` 对照一次；② 查 9876 占用；③ 长任务拆成多段（每段 < 60 s）；④ 已修分支 #48 实测 120s → 2.8s
- **本管线对策**：审计/批量操作拆批，每批 ≤ 500 对象 或 ≤ 30 s 估算耗时

### 2.3 保存纪律
```python
bpy.ops.wm.save_mainfile()                       # 覆盖
bpy.ops.wm.save_as_mainfile(filepath=r"C:\...")  # 另存（改结构前必须先另存）
```
**动结构前先 `save_as_mainfile` 到 `_backup_<时间戳>.blend`**。MCP 无撤销栈保证。

### 2.4 无头模式限制
无头（`--background`）时：**视口截图不可用**，只能 `bpy.ops.render.render(write_still=True)`。
所以在 MCP 交互式会话里做比对，在无头脚本里做批处理/审计 —— 两者别混。

---

## 3. 典型会话编排

### 3.1 新建资产（一次会话走完 Stage 2–3）
```
① get_scene_info                     → 确认空场景/已有内容
② execute: 建 COL_ 七层 + 导入 REF_Scale_Human
③ execute: 块面（或 primitive 拼）
④ get_screenshot_of_window_as_image  → 与参考并排看剪影
⑤ execute: 按差距改（一次改一处）
⑥ 重复 ④⑤ 最多 3 轮
⑦ execute: save_as_mainfile 到项目目录
⑧ get_objects_summary                → 汇报面数/对象数
```

### 3.2 审计现有资产
```
① execute: 跑 asset_qa 的核心逻辑（或本地跑脚本读 .blend）
② 按报告分级：Blocker 先改
③ execute: 批量修（重命名/apply scale/建 collection）
④ 复跑审计直到 PASS
⑤ get_screenshot 留证
```

### 3.3 导出前 gate
```
① 本地: asset_qa.py --tier hero --export-gate   → exit code
② exit != 0 → 不得导出
③ execute: 按 optimize-export.md 参数导出
④ 汇报导出路径 + 统计
```

---

## 4. 代码分段建议（避免巨型 payload）

| 任务 | 拆法 |
|---|---|
| 批量重命名 200 个对象 | 一次调用（纯字符串操作，快） |
| 批量 apply scale + 建 UV | 分批 50 个/次（bpy.ops 慢） |
| 逐对象渲染缩略图 | 每对象一次调用（渲染不可批量塞） |
| 全场景审计 | 一次调用（只读，快） |
| 高模重拓扑 | 不通过 MCP 做（交互操作，本地做） |

---

## 5. 与本地脚本的分工

| 场景 | 用 |
|---|---|
| 用户在 Blender 里开着场景，要即时改 | MCP `execute_blender_code` |
| 可复现的批处理（审计/转换/批量导出） | 本地脚本 + `blender --background --python` |
| 需要版本守卫的交付代码 | 本地写成 .py，5.3/5.2 双跑验证 |
| 一次性探索 | MCP |

**判据**：这件事明天还要再做一次吗？要 → 写脚本。不要 → MCP 直接干。

---

## 6. 报错速查

| 报错/症状 | 原因 | 处置 |
|---|---|---|
| 连接被拒 | add-on 未启用 / 端口被占 | 见 `blender-mcp` 技能 |
| 120s 超时 | #72 / #48 | 拆批 / `--factory-startup` 对照 / 打补丁 |
| `result` 报错 | 返回非 dict | 包成 dict |
| 执行后场景没变 | 代码在错误 context 下跑（如 edit mode） | 先 `bpy.ops.object.mode_set(mode='OBJECT')` |
| 截图黑屏 | 无头模式 / 视口未重绘 | 改用渲染到文件 |
| 中文路径失败 | 编码 | 用 `r"C:\..."` 原始字符串 + UTF-8 |
