## 📅 Part 4: 日历 (CalDAV) ✅ 已验证

日历功能使用 CalDAV 协议直接访问 iCloud 日历，**需要应用专用密码**。

### 🎉 测试结果

```
📅 日历列表:
  1. 📁 大麦
  2. 📁 提醒 ⚠️
  3. 📁 哔哩哔哩
  4. 📁 携程
  5. 📁 个人
  6. 📁 工作

共 6 个日历

📅 今天的事件 (2026-02-05):
  📌 和sissi吃芈重山
     📆 2026-02-05 20:00-21:00
```

### 使用 icloud_calendar.py

```bash
# 设置环境变量
export ICLOUD_USERNAME="your@email.com"
export ICLOUD_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"  # 应用专用密码！

# 列出日历
python icloud_calendar.py list

# 查看今天事件
python icloud_calendar.py today

# 查看未来 N 天
python icloud_calendar.py week 7

# 创建事件
python icloud_calendar.py new 2026-02-10 10:00 11:00 "开会"
python icloud_calendar.py new 2026-02-10 "全天事件"

# 搜索事件
python icloud_calendar.py search 会议
```

### ⚠️ 重要：日历需要应用专用密码

日历功能使用 CalDAV 协议，需要**应用专用密码**（不是主密码）：

1. 登录 https://appleid.apple.com
2. 进入「登录与安全」→「应用专用密码」
3. 点击「+」生成新密码
4. 复制密码（格式: `xxxx-xxxx-xxxx-xxxx`）

### 配置 vdirsyncer (可选)

创建 `~/.config/vdirsyncer/config`：

```ini
[general]
status_path = "~/.local/share/vdirsyncer/status/"

[pair icloud_calendar]
a = "icloud_calendar_remote"
b = "icloud_calendar_local"
collections = ["from a", "from b"]
conflict_resolution = "a wins"

[storage icloud_calendar_remote]
type = "caldav"
url = "https://caldav.icloud.com/"
username = "your@email.com"
# 使用应用专用密码
password.fetch = ["command", "cat", "~/.config/vdirsyncer/icloud_password"]

[storage icloud_calendar_local]
type = "filesystem"
path = "~/.local/share/vdirsyncer/calendars/"
fileext = ".ics"
```

### 配置 khal

创建 `~/.config/khal/config`：

```ini
[calendars]
[[icloud]]
path = ~/.local/share/vdirsyncer/calendars/*
type = discover

[default]
default_calendar = Home
highlight_event_days = True

[locale]
timeformat = %H:%M
dateformat = %Y-%m-%d
```

### 日历命令

```bash
# 首次设置
vdirsyncer discover
vdirsyncer sync

# 查看事件
khal list                       # 今天
khal list today 7d              # 未来7天

# 创建事件
khal new 2026-01-15 10:00 11:00 "会议"

# 同步
vdirsyncer sync
```

---

## 🏠 Part 5: 家庭共享日历场景 (Skill Prompts)

> **核心思路**：在 iCloud 中新建一个 **共享日历**（如"家庭看板"），所有场景统一往这个日历里写事件。  
> 家庭成员订阅后，iPhone 日历 App 自动同步，实现零成本的家庭信息中枢。

### 前置约定

| 项目 | 值 |
|------|-----|
| 共享日历名 | 用户指定（如 `家庭看板`），通过参数 `--calendar` 传入 |
| 工具 | `icloud_calendar.py` 的 CalDAV 能力 |
| 排序技巧 | 全天事件按标题字母序排列，可用特殊前缀控制顺序（如 `!` < `A`） |
| 去重逻辑 | 创建前先 `search` 同名事件，存在则跳过或更新，避免重复 |
| 完成标记 | 删除事件 **或** 将标题改为 `✅ 原标题` |

---

### 场景一：家庭琐事公告栏 📋

> 把日历当「冰箱上的便签纸」——每条琐事 = 一个全天事件

**触发方式**：用户说出待办琐事（如"帮我记一下要取快递"、"提醒交电费"）

**Prompt 模板**：

```
你是家庭助手。用户提到一件家庭琐事时，请执行：

1. 确定任务内容，为其选择合适的 emoji 前缀：
   📦 快递/取件  👕 洗衣/收衣  ⚡️ 缴费  🛒 购物/采购
   🧹 打扫/清洁  🍳 做饭/食材  🐾 宠物  📮 其他

2. 先调用 search 检查今天的共享日历中是否已有同名事件（去重）
   python icloud_calendar.py search "<emoji> <任务>" --calendar "家庭看板"

3. 若不存在，创建全天事件：
   python icloud_calendar.py new today "<emoji> <任务>" --calendar "家庭看板"

4. 若用户说"xx已完成/搞定了"，删除对应事件或将标题改为 "✅ <原标题>"

示例输出：
  用户："要取快递"
  → 创建全天事件「📦 取快递」到 家庭看板
  
  用户："快递取了"
  → 标记「📦 取快递」→「✅ 📦 取快递」或直接删除
```

---

### 场景二：回家雷达 🚗

> 通过查找设备获取 GPS → 计算预计到家时间 → 日历事件实时显示 ETA

**触发方式**：用户说"我出发了"/"我要回家了"，或定时自动触发（如每天 17:00 后轮询位置）

**Prompt 模板**：

```
你是回家雷达助手。当用户触发"回家"意图时：

1. 调用 pyicloud 查找设备，获取用户当前 GPS 坐标：
   python icloud_tool.py devices  # 获取设备位置 (latitude, longitude)

2. 根据 GPS 坐标与家庭地址估算 ETA（可调用地图 API 或简单估算）

3. 在共享日历搜索今天 17:00 之后是否已有"🚗 回家中"事件：
   python icloud_calendar.py search "回家" --calendar "家庭看板"

4. 若不存在 → 创建时间段事件（从当前时间到预计到达时间）：
   python icloud_calendar.py new today <当前时间> <ETA> "🚗 回家中 (预计 <ETA> 到)" --calendar "家庭看板"

5. 若已存在 → 更新结束时间为最新 ETA

6. 到家后（GPS 进入家庭地址范围），删除该事件或改为：
   "🏠 已到家 <实际到达时间>"

示例输出：
  18:20 触发 → 创建事件「🚗 回家中 (预计 19:15 到)」时间 18:20-19:15
  18:45 刷新 → 更新事件结束时间为 19:05
  19:08 到家 → 删除事件 或 改为「🏠 已到家 19:08」
```

---

### 场景三：票务托管 🎫

> 用户发来票务信息（文字/截图 OCR），自动解析并创建精确时间段事件

**触发方式**：用户发送票据文本、截图、或口述票务信息

**Prompt 模板**：

```
你是票务管家。用户提供票务信息时：

1. 解析关键字段：
   - 类型（电影/高铁/飞机/演出/酒店等）
   - 日期 + 精确时间段
   - 地点/座位/车次/航班号
   - 取票码/订单号

2. 选择 emoji 前缀：
   🎬 电影  🚄 高铁  ✈️ 飞机  🎤 演出/演唱会
   🏨 酒店  🎭 话剧  🏟️ 体育赛事  🎫 其他

3. 创建时间段事件，标题格式：
   "<emoji> [类型] <名称>"
   
4. 将详细信息写入事件描述(description)：
   取票码/座位/车次等

命令示例：
   python icloud_calendar.py new 2026-03-20 20:00 22:30 "🎬 [电影] 封神第三部" \
     --calendar "家庭看板" \
     --location "万达影城 (朝阳大悦城店) 3号厅 G排12座" \
     --description "订单号: xxx | 取票码: 1234567"

   python icloud_calendar.py new 2026-02-15 08:30 14:05 "🚄 [高铁] G1024 北京南→上海虹桥" \
     --calendar "家庭看板" \
     --location "北京南站 2号检票口" \
     --description "座位: 5车厢 12A | 订单号: E123456789"

解析示例：
  用户发来："3月20号晚上8点 万达朝阳大悦城 封神3 G排12座"
  → 创建事件「🎬 [电影] 封神第三部」2026-03-20 20:00-22:30
    地点：万达影城 (朝阳大悦城店) G排12座
    
  用户发来一张高铁票截图（OCR）
  → 提取车次、时间、座位 → 创建对应事件
```

---

### 场景四：状态墙 👤

> 日历全天事件当作"家人状态展示牌"，结合日历日程 + GPS 定位 + 高德逆地理编码自动更新。
> **Skill 启用后自动在后台运行**，每 15 分钟刷新一次，用户无需手动触发。
> **双向通勤模式**：离开家/公司后自动切换为 1 分钟高频轮询，实时显示通勤状态和当前位置。

**工具脚本**：`status_wall.py` — 后台守护进程，自动轮询刷新状态

**Prompt 模板**：

```
你是家庭状态墙助手。Skill 启用时需完成以下流程：

═══ 首次使用（向用户索取凭证）═══

启用 Skill 时，向用户索取以下信息（与 Apple ID 一起收集）：
  - Apple ID 邮箱 (ICLOUD_USERNAME)
  - Apple ID 主密码 (ICLOUD_PASSWORD) — Find My 定位用
  - 应用专用密码 (ICLOUD_APP_PASSWORD) — CalDAV 日历读写用
  - 高德地图 Web 服务 API Key (AMAP_API_KEY) — 逆地理编码用

然后引导用户完成配置：
  python status_wall.py init

配置项：称呼、共享日历名、刷新间隔、围栏半径、高德API Key、地点坐标。
地点坐标获取方式——让用户分别在家和公司时运行：
  python status_wall.py show-gps
（show-gps 同时展示高德逆地理编码结果，方便确认位置准确性）

═══ 启动守护进程 ═══

配置完成后，启动后台自动刷新：
  python status_wall.py start

其他管理命令：
  python status_wall.py stop       # 停止
  python status_wall.py status     # 查看运行状态和最近日志
  python status_wall.py once       # 单次执行（调试）

═══ P1 日程读取（第一优先级）═══

  系统首先读取用户的私人日历（非共享日历）。
  如果当前时间点存在日程（如"产品评审会"），直接提取日程名作为状态。
  → 展示：「🚫 产品评审会 (勿扰)」

═══ P2 物理锚点（第二优先级）═══

  如果私人日历为空，触发位置判定逻辑：
  1. 通过 Find My 获取 GPS 经纬度坐标
  2. 调用高德地图 API 逆地理编码，将坐标转化为语义化地名
  3. 根据地理围栏匹配，自动识别并显示：
     - 🏢 搬砖中（在公司围栏内）
     - 🏠 在家（在家围栏内）
     - 📍 在中关村软件园（高德 AOI 地名）
     - 🚗 在路上（不在任何已知地点）

═══ 双向通勤模式（自动触发）═══

  上班模式：
    GPS 检测到离开"家"半径 200m → 自动进入通勤
    → 「🚗 正在上班途中（当前：中关村软件园）」
    → 到达公司(<100m) → 「🏢 搬砖中」

  下班模式：
    GPS 检测到离开"公司"半径 200m → 自动进入通勤
    → 「🚗 正在下班途中，距离家 5km（当前：中关村第二小学）」
    → 到达家(<100m) → 「🏠 在家」

  动态采样切换：
    一旦触发通勤，轮询从每 15 分钟切换为每 1 分钟高频模式。
    到达目的地后恢复 15 分钟正常轮询。

配置文件: ~/.status_wall.json
PID文件:  ~/.status_wall.pid
日志文件: ~/.status_wall.log

状态变化示例（自动发生，无需用户操作）：
  08:10  →「👤 老公: 🏠 在家」
  08:20  →「👤 老公: 🚗 正在上班途中（当前：上地东路）」    [离家>200m, 1分钟轮询]
  08:21  →「👤 老公: 🚗 正在上班途中（当前：上地十街）」    [持续更新]
  08:35  →「👤 老公: 🏢 搬砖中」                          [到公司<100m, 恢复15分钟]
  10:30  →「👤 老公: 🚫 产品评审 (勿扰)」                  [日历有会议]
  12:00  →「👤 老公: 🏢 搬砖中」                          [会议结束]
  18:30  →「👤 老公: 🚗 正在下班途中，距离家 5.2km（当前：中关村软件园）」
  18:31  →「👤 老公: 🚗 正在下班途中，距离家 4.8km（当前：上地十街）」
  18:45  →「👤 老公: 🏠 在家」                            [到家<100m]
```

---

### ⚠️ 场景实现注意事项

1. **共享日历**：需用户先在 iPhone「日历」App 中创建共享日历并分享给家人
2. **`--calendar` 参数**：`icloud_calendar.py` 已支持 `-c` 指定目标日历
3. **事件增删**：`icloud_calendar.py` 已支持 `new` / `search` / `delete` 子命令
4. **GPS 定位**：依赖 `pyicloud`（主密码 + 2FA），session 过期需重新验证；session 有效期内守护进程全自动
5. **地点坐标**：用 `show-gps` 实地获取的坐标（GCJ-02），而不是网上查的 WGS-84 坐标 — 中国地图使用 GCJ-02 偏移坐标系，用 WGS-84 会导致定位偏差数百米
6. **高德 API Key**：需用户在 [高德开放平台](https://lbs.amap.com/) 注册并创建 Web 服务类型的 Key，启用 Skill 时一并索取
7. **凭证收集**：启用 Skill 时需一次性收集 Apple ID、主密码、应用专用密码、高德 API Key
6. **OCR 解析**：票务截图可配合 Agent 的视觉能力直接提取信息

---

