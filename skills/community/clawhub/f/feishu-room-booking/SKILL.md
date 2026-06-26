---
name: feishu-room-booking
description: |
  字节内部使用的飞书会议室查询与预订技能（覆盖全球130+工区、7300+会议室）。当用户提到"查会议室"、"订会议室"、"空闲会议室"、"预订会议室"、"开会"、"找个会议室"、"F4会议室"、"紫金会议室"、"哪个会议室有空"、或者创建会议时需要自动匹配空闲会议室时，必须使用此 skill。也适用于用户要求创建日程并指定楼栋/区域时自动完成会议室预订的场景。也适用于用户提到"会议室偏好"、"我的偏好"、"候补"、"补订会议室"、"自动订会议室"时。当用户未指定楼栋时，优先读取用户偏好中的默认楼栋；无偏好则主动询问城市/楼栋。
---

# 飞书会议室查询与预订

管理飞书会议室的忙闲查询、自动匹配、日程预订、偏好管理和候补轮询。

## 前置依赖

- `lark-cli` 已安装且 bot 身份可用
- 飞书应用已开通相关权限（calendar:calendar.free_busy:read, calendar:calendar.event:create 等）
- 数据文件：`references/room-mapping.json`（全球 130+ 工区、7300+ 会议室）、`references/user-preferences.json`、`references/room-waitlist.json`、`references/weekly-workspace.json`
- 脚本目录：`scripts/`
- 建筑匹配使用索引查找（O(1)），忙闲查询自动 10 线程并行

## 工具脚本

所有会议室操作**必须通过脚本**，不要手写 bash 循环。

### query_rooms.py — 会议室查询

```bash
# 列出所有楼栋
python3 scripts/query_rooms.py --list-buildings

# 列出指定楼栋的会议室
python3 scripts/query_rooms.py --list-rooms -b "丽金"

# 查询空闲会议室（表格输出，自动并行查询）
python3 scripts/query_rooms.py -b "丽金" \
  -s "2026-04-20T14:00:00+08:00" \
  -e "2026-04-20T15:00:00+08:00" -o table

# 按容量筛选
python3 scripts/query_rooms.py -b "丽金" \
  -s "2026-04-20T14:00:00+08:00" \
  -e "2026-04-20T15:00:00+08:00" \
  --capacity-gte 8 -o table

# 调整并行度（默认 10 线程）
python3 scripts/query_rooms.py -b "丽金" \
  -s "2026-04-20T14:00:00+08:00" \
  -e "2026-04-20T15:00:00+08:00" \
  --max-workers 20 -o table
```

### manage_preferences.py — 偏好管理

```bash
# 设置偏好
python3 scripts/manage_preferences.py --set \
  --user "ou_xxx" --building "丽金" --capacity-gte 8 \
  --preferred-rooms "F11-07,F11-15" --note "偏好靠近电梯"

# 读取偏好
python3 scripts/manage_preferences.py --get --user "ou_xxx"

# 记录用户选择（自动学习）
python3 scripts/manage_preferences.py --learn \
  --user "ou_xxx" --room "F11-15(8)" --building "丽金智地中心 B座"

# 列出所有偏好
python3 scripts/manage_preferences.py --list
```

### watch_waitlist.py — 候补管理

```bash
# 查看候补状态
python3 scripts/watch_waitlist.py --status

# 执行一轮轮询
python3 scripts/watch_waitlist.py --poll

# 添加候补
python3 scripts/watch_waitlist.py --add \
  --event-id "xxx" --summary "周会" \
  --start "2026-04-20T14:00:00+08:00" --end "2026-04-20T15:00:00+08:00" \
  --building "丽金" --capacity-gte 8

# 移除候补
python3 scripts/watch_waitlist.py --remove --event-id "xxx"

# 清理过期候补
python3 scripts/watch_waitlist.py --clean
```

### workspace_manager.py — 工区时间线管理

```bash
# 查看当前工区和下周工区
python3 scripts/workspace_manager.py --get

# 设置当前工区（默认从今天到本周日）
python3 scripts/workspace_manager.py --set --workspace "丽金智地中心 B座"

# 设置指定日期范围的工区
python3 scripts/workspace_manager.py --set --workspace "紫金数码园4号楼" \
  --from "2026-04-30" --to "2026-05-02"

# 设置下周工区
python3 scripts/workspace_manager.py --set-next --workspace "紫金数码园4号楼"

# 推荐下周工区 / 周五提醒检查 / 查看时间线
python3 scripts/workspace_manager.py --recommend
python3 scripts/workspace_manager.py --check-friday-reminder
python3 scripts/workspace_manager.py --timeline
```

## 数据文件

| 文件 | 用途 |
|------|------|
| `references/room-mapping.json` | 会议室资源 ID 映射 |
| `references/user-preferences.json` | 用户个人偏好 |
| `references/room-waitlist.json` | 候补预订队列 |
| `references/weekly-workspace.json` | 当前工区 / 下周工区时间线 |

## 核心流程

### 流程 A：查询空闲会议室

用户只想看哪些会议室有空。

1. **解析意图** — 时间段、楼栋、容量需求
2. **确定楼栋** —
   - 用户明确指定 → 直接使用
   - 用户未指定 → 先读取用户偏好获取默认楼栋（`manage_preferences.py --get`）
   - 用户无偏好 → 读取当前工区 / 下周工区（`workspace_manager.py --get`）作为默认楼栋
   - 仍然无法确定 → ⚠️ 必须询问城市/楼栋，不要猜测。可提示"北京/上海/深圳/杭州/..."等热门城市
3. **确定日期** — ⚠️ 严格验证星期几
4. **执行查询** — `python3 scripts/query_rooms.py -u "ou_xxx" -s ... -e ... -o table`
   - 用户已指定楼栋时仍优先传 `-b`
   - 未指定楼栋时，脚本会按“用户偏好 → 当前/下周工区”兜底
5. **呈现结果** — 直接转发脚本输出

### 流程 B：创建会议并自动预订

用户要开会，需要创建日程 + 匹配会议室。

1. **解析意图** — 标题、时间、楼栋、容量、参会人
2. **确定日期** — ⚠️ 严格验证星期几
3. **确定默认楼栋** —
   - 优先读取用户偏好：`python3 scripts/manage_preferences.py --get --user "ou_xxx"`
   - 无偏好时读取工区时间线：`python3 scripts/workspace_manager.py --get`
   - 用户显式指定楼栋时覆盖默认值
4. **查询空闲会议室** — 用脚本查询，带上容量筛选
5. **用户选择** — `feishu_ask_user_question` 弹卡片
6. **创建日程** — `feishu_calendar_event` create
7. **添加会议室+参会人** — `feishu_calendar_event_attendee` create
   - ⚠️ 字段名是 `attendee_id`，不是 `id`
8. **Reflection 二次校验** — 等 5 秒后查 attendee list / event detail
   - `confirmed`：resource 已 accept，才能对用户说“预订成功”
   - `pending`：resource 已出现但状态未定，只能说“已提交，等待确认”
   - `failed`：resource decline / 缺失，不能宣告成功
9. **Fallback** — `failed` 时自动换下一个空闲会议室
10. **记录选择** — 仅 `confirmed` 后调用 `python3 scripts/manage_preferences.py --learn --user "ou_xxx" --room "F11-15(8)" --building "..."`

### 流程 C：用户偏好管理

用户设置或修改会议室偏好，后续自动应用。

**设置偏好：**
- 用户说"我一般用丽金B座8人以上的会议室"
- 调用 `--set` 写入偏好

**自动学习：**
- 每次流程 B 完成后，调用 `--learn` 记录选择
- 连续 3 次选同一个会议室 → 自动标记为偏好会议室
- 最近 3 次选同一楼栋 → 自动设为默认楼栋

**应用偏好：**
- 流程 B 的 Step 3 自动读取偏好
- 偏好楼栋不匹配时，按偏好查；没空闲时追问是否换楼栋
- 容量需求自动带入查询

### 流程 D：扫描日程自动补订

自动检测用户日程中缺少会议室的会议并补订。

**触发方式：**
- **手动**：用户说"帮我检查一下有没有缺会议室的日程"、"补订会议室"
- **自动**：Heartbeat 定时任务

**扫描步骤：**
1. 调用 `feishu_calendar_event` list 获取用户近期日程（未来 24 小时）
2. 首轮检查当前用户是否已 accept：优先读事件级 `self_rsvp_status`，没有时再看 attendees 中当前用户的 `rsvp_status / status / response_status`
3. 对 resource 参会人做 reflection 分类，而不是只看“是否存在 resource”
   - `confirmed`：已有已确认会议室，直接跳过
   - `pending`：会议室状态待确认，先进入二次确认队列，不立即补订
   - `failed` / `missing`：视为当前没有成功会议室，可继续补订
4. 对首轮判定需要补订的事件，再做一次二次确认
5. 二次确认后仍为 `confirmed` 缺会议室的日程：
   - 先读取用户偏好确定默认楼栋和容量
   - 无默认楼栋时回退到当前工区 / 下周工区
   - 查询空闲会议室
   - 有空闲 → 自动预订（跳过用户确认，因为是补订场景）
   - 全满 → 加入候补队列

**判断是否需要会议室的逻辑：**
- ❌ 跳过：当前用户未 accept、已有 `confirmed` 会议室、日期型全天事件
- ⏳ 待确认：当前用户状态缺失，或 resource 已存在但 RSVP 未稳定
- ✅ 补订：当前用户已 accept，且当前没有 `confirmed` 会议室

### 流程 E：候补轮询

会议室满了时的自动候补机制。

**添加候补：**
- 流程 D 发现全满时，调用 `watch_waitlist.py --add` 加入队列
- 候补项应写入已经确定好的楼栋；默认楼栋的决策仍遵循“用户偏好 → 当前/下周工区”

**轮询检查：**
- Heartbeat 或手动触发 `watch_waitlist.py --poll`
- 对每个 waiting 状态的候补，查询当前时段空闲会议室
- 找到空闲 → 标记为 `ready`，通知 agent 执行预订
- agent 提交预订后进入 `verification_pending`，等待 5 秒后二次校验
- 仍然满 → 记录已尝试列表，等待下次轮询

**预订成功后：**
- `confirmed` → 从候补移除
- `pending` → 保持 `verification_pending`
- `failed / decline` → 回到 `waiting`，允许继续候补或 fallback

**清理：**
- 定期 `--clean` 清理已过期的候补（开始时间超过 1 小时）

### 流程 F：工区时间线管理

用户需要声明当前工区、设置下周工区，或让系统给出默认工区建议。

**支持动作：**
- `python3 scripts/workspace_manager.py --get` 查看当前工区 / 下周工区
- `python3 scripts/workspace_manager.py --set --workspace "丽金智地中心 B座"` 设置当前工区
- `python3 scripts/workspace_manager.py --set-next --workspace "紫金数码园4号楼"` 设置下周工区
- `python3 scripts/workspace_manager.py --recommend` 基于近期会议室选择推荐工区
- `python3 scripts/workspace_manager.py --check-friday-reminder` 检查是否需要周五提醒
- `python3 scripts/workspace_manager.py --timeline` 查看完整时间线

**默认楼栋决策优先级：**
1. 用户本次明确指定楼栋
2. 用户偏好中的 `default_building`
3. 当前工区 / 与查询日期匹配的下周工区
4. 仍然无法确定时追问用户

---

## 交互规范

### 自然语言解析
| 用户说 | 解析 |
|--------|------|
| "明天下午3点开会" | 明天 15:00，默认 1 小时。未指定楼栋时先查偏好，再查工区 |
| "找个会议室" | 读取偏好 → 用默认楼栋和容量。无偏好则读当前工区；仍无结果再问城市/楼栋 |
| "查一下丽金B座明天下午" | Flow A，匹配 "丽金B座" → 丽金智地中心 B座 |
| "帮我找丽金B座11楼的会议室" | Flow A，先匹配楼栋，再用楼层 `11` 缩小房间范围 |
| "查一下 F11-15 明天下午是否空闲" | Flow A，优先按房间号匹配楼栋，再按房间号缩小到单个候选 |
| "我这周在丽金B座" | 流程 F，设置当前工区时间线 |
| "下周回紫金" | 流程 F，设置下周工区 |
| "帮我设个偏好，丽金B座8人以上" | 流程 C，设置偏好 |
| "查一下我有没有缺会议室的会" | 流程 D，扫描日程 |
| "候补状态怎么样了" | 流程 E，查看候补 |
| "北京有哪些工区" | `--list-buildings` 筛选含"北京"的行 |

### 楼栋匹配提示

当前覆盖全球 130+ 工区。agent 匹配楼栋时：
- 中文关键词（"丽金"、"紫金"、"大钟寺"）→ 自动模糊匹配
- 英文缩写（"F4"、"F11"）→ 自动匹配别名
- 楼层 / 房间号差异表达（"11楼" / "11F" / "F11-15" / "11-15" / "DiscussionBooth A"）→ 自动抽取并缩小候选
- 城市筛选：用户说"北京的会议室" → 先 `--list-buildings` 再 grep "北京"
- 匹配到多个结果时 → 列出来让用户选，不要默认猜一个

### 用户确认原则
- 流程 B（主动创建）：必须确认时间、会议室、参会人
- 流程 D（自动补订）：不需要确认，直接执行
- 流程 E（候补预订）：不需要确认，直接执行

## 注意事项

1. **并行查询**：freebusy 查询自动 10 线程并行，大工区（200+ 间）可加 `--max-workers 20`
2. **会议室是 resource**：attendee type 为 `"resource"`，`attendee_id` 传 `omm_xxx`
3. **预订异步**：添加后等 5 秒再查 RSVP
4. **时区统一**：`Asia/Shanghai`（+08:00），ISO 8601
5. **日期验证**：涉及相对时间必须验证星期几
6. **脚本优先**：统一用 scripts/ 下的脚本
7. **时间修改风险**：patch 改时间后会议室可能 decline，必须重新验证
8. **偏好自动学习**：每次预订成功后调用 `--learn` 记录
9. **楼栋匹配**：使用索引查找（O(1)），支持模糊匹配 name 和所有 alias
10. **全球覆盖**：room-mapping.json 含 130+ 工区、7300+ 间会议室，未指定楼栋时优先使用用户偏好，再回退到当前/下周工区
11. **工区时间线**：weekly-workspace.json 只负责当前工区 / 下周工区，不替代用户个人偏好和自动学习
