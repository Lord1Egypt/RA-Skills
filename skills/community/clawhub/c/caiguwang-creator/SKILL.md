---
name: caiguwang-creator
slug: caiguwang-creator
displayName: 才谷网投票
version: 1.0.4
license: MIT
summary: AI 一句话创建微信投票活动：投票模板检索、批量添加选手、票数榜单与活动数据查询。
description: |
    才谷网投票创建助手：检索投票模板、上传图片、创建投票活动、查询投票数据。
    当用户需要制作投票、发起评选、组织投票活动、查询投票结果时使用此 Skill。

    核心功能：
    1. 检索投票模板——按关键词筛选，返回模板列表与图片
    2. 上传图片——本地图片文件或图片链接，返回素材 URL（用于选手图片/封面）
    3. 创建投票活动——支持 AI 一句话生成（描述活动需求自动生成标题/时间/规则并匹配模板），
       也支持手动参数创建（单选/多选、时间范围、分组、选手列表）
    4. 修改投票活动——对话直接修改已创建活动的标题/说明/时间/投票规则/分组，添加或修改选手
    5. 活动列表——分页查询我的投票活动（可按关键词/进行中/已结束筛选）
    6. 投票数据——查询活动选手榜单明细（名次/票数）
    7. 活动整体数据——参与人数、累计投票、浏览次数、TOP5
    8. 分组改名——对话直接修改活动分组名称（不改选手归属）
    9. 素材列表——查询账号素材库（图片 URL 可直接用于选手/封面）

    触发词：才谷网、制作投票、创建投票、发起投票、在线投票、投票模板、评选投票、微信投票、
    活动投票、投票系统、投票链接、二维码投票、投票活动怎么弄、怎么发起投票、
    投票工具、投票网站、免费投票、作品评选、摄影投票、美食投票、萌娃投票、绘画投票、
    AI 创建投票、一句话生成投票

read_when:
  - 用户提到投票、评选、投票活动、投票模板、才谷网
  - 用户想要创建投票链接/二维码投票/投票小程序
  - 用户想找一个免费投票工具/网站/小程序
  - 用户描述"我想做个投票让大家选…"

---

# 才谷网投票技能说明

## 前置条件

1. 依赖 `requests`：`pip install requests`
2. 获取访问令牌 `X-Caigu-Token`：
   登录网页管理后台 https://www.chinacaigu.com/mp/index.html → 左侧菜单「养虾Skill」→ **开启令牌开关**（默认停用，开启后才会显示令牌）→ 复制安装指令或令牌。泄露可随时重置，重置后旧令牌立即失效；平台有权冻结令牌，冻结时开关不可开启。
3. 令牌保存于 `~/.caiguwang/config.json`，后续命令自动复用；也可通过环境变量 `X_CAIGU_TOKEN` 提供。
4. 默认接口地址 `https://www.chinacaigu.com`，可用环境变量 `CAIGU_API_BASE` 覆盖（本地联调用）。

## 认证（推荐先做）

```bash
# 保存令牌（任选其一）
python scripts/caiguwang_cli.py login --token <你的令牌>
python scripts/caiguwang_cli.py login    # 不带参数则提示粘贴

# 验证令牌有效性
python scripts/caiguwang_cli.py auth status
```

返回 `{"success": true, "code": 200}` 表示有效；`code: 1002` 表示令牌无效/已停用/被冻结，请用户到后台「养虾Skill」页检查令牌开关，或联系平台客服。

## 检索投票模板

```bash
python scripts/caiguwang_cli.py search --kw "绘画比赛" --page 1 --size 10
```

返回模板列表（`template_id` / `title` / `image`）。创建活动时可将 `template_id` 传给 `create --template`。

## 创建投票活动

### 方式一：AI 一句话生成（推荐，无需手动拼参数）

```bash
python scripts/caiguwang_cli.py create --describe "给阳光幼儿园办一个国庆绘画比赛投票，10月1日到7日，每人每天投3票"
```

AI 自动生成活动标题、投票时间、投票规则（每天/总共可投次数、单选多选、是否开启报名），
并自动匹配合适模板。可叠加手动参数覆盖 AI 生成结果（如 `--multi --per-user-count 5`）。

### 方式二：手动参数

```bash
python scripts/caiguwang_cli.py create \
  --title "年度最佳作品评选" \
  --intro "本次评选由某某单位主办，欢迎参与投票。" \
  --start "2026-11-15 08:00" --end "2026-11-25 22:00" \
  --multi --per-user-count 3 --per-user-scope day \
  --groups "绘画组,书法组" \
  --template 123456 \
  --sponsor "某某单位" --sponsor-tel "13800000000"
```

带选手列表（**每个选手必须有图片**：本地图片请先经 upload 转成 URL；报名型活动可不传选手，由选手自主报名）：

```bash
python scripts/caiguwang_cli.py create \
  --title "摄影作品人气投票" \
  --intro "欢迎参与本次摄影作品人气投票。" \
  --items-file items.json
# items.json 示例：[{"name":"作品一","image":"https://example.com/p1.jpg"},{"name":"作品二","image":"https://example.com/p2.jpg"}]
```

### 参数说明

| 参数 | 说明 |
|---|---|
| `--describe` | 一段话描述活动需求（走 AI 生成，与手动参数可混用） |
| `--title` | 活动标题（≤50字，手动创建必填） |
| `--intro` | 活动说明（**必填**，面向参与者，长度不限，建议简明） |
| `--start` / `--end` | 时间，格式 `YYYY-MM-DD HH:MM`；不传默认当前开始、10 天后结束 |
| `--multi` | 开启多选投票（默认单选） |
| `--per-user-count` | 每人可投次数（1-20，默认 3） |
| `--per-user-scope` | `day` 每天 / `total` 活动期间总共（默认 day） |
| `--select-min` / `--select-max` | 多选时每次最少/最多选几个（min 1-999；max 0-999，0=不限） |
| `--groups` | 分组名，逗号分隔（2-100 组，单个名称 ≤20 字） |
| `--apply` | 开启选手报名 |
| `--template` | 模板 ID（search 返回的 template_id）；不传时 AI 自动匹配 |
| `--sponsor` / `--sponsor-tel` | 主办方名称/电话 |
| `--cover` | 活动封面图 URL（网页后台要求 750×464 比例；建议先 `upload --crop 750x464` 再传入） |
| `--items-file` / `--items` | 选手列表（JSON 文件路径或 JSON 字符串），name、image 均必填（图文投票）；分组活动可加 `"cat_id": 0` 指定分组序号（从 0 开始） |
| `--notice` | 报名须知（开启报名时展示） |

### 创建成功返回

```json
{
  "success": true, "code": 200,
  "data": {
    "id": "4HGZ7L0X",
    "title": "国庆绘画比赛投票",
    "start_time": "2026-11-12 08:00",
    "end_time": "2026-11-19 22:00",
    "edit_url": "https://www.chinacaigu.com/mp/edit.html?id=19630",
    "qrcode": "https://cdn.example.com/data/poster/xxxxxx/xxxx.jpg",
    "hint": "活动已创建并按投票时间生效；qrcode 为小程序码图片地址（为空时请到管理后台活动列表「地址」获取）；edit_url 用于调整配置"
  }
}
```

**关于活动 id（引用码）**：接口返回的 `id` 是**引用码**（字母数字，如 `4HGZ7L0X`），不是真实活动编号——对话展示时请使用引用码或活动标题，不要向用户展示真实数字 ID。所有命令的 `--id` 既接受引用码，也接受真实数字 ID（两者都有效）。`edit_url`/`qrcode` 中的链接是活动本身的固定访问地址，无法去除编号，属正常现象。

**分享与编辑（告知用户时用这两样）**：
- **分享投票**：把 `qrcode`（微信小程序码图片地址）给用户，可下载打印张贴；为空则引导用户到管理后台活动列表点「地址」获取；
- **调整配置**：`edit_url` 在浏览器打开（需微信扫码登录管理后台），可调整全部配置。

创建即按投票时间生效，对话时请复述活动标题、时间与规则要点，请用户确认。

## 修改活动与管理选手（对话修改）

用户对已创建活动说"改一下…"时用这些命令。所有修改均有归属校验，只对自己的活动生效。

### 修改活动配置（update，可选参数只传要改的）

```bash
# 延长活动时间 + 改标题
python scripts/caiguwang_cli.py update --id 19630 --title "年度最佳作品评选（延期）" --end "2026-12-01 22:00"

# 改投票规则：改为多选、每人总共投 5 票
python scripts/caiguwang_cli.py update --id 19630 --multi --per-user-count 5 --per-user-scope total

# 改分组（整体替换）
python scripts/caiguwang_cli.py update --id 19630 --groups "绘画组,书法组,摄影组"

# 关闭报名 / 开启报名
python scripts/caiguwang_cli.py update --id 19630 --no-apply
```

可改字段：`--title --intro --notice --start --end --multi/--no-multi --per-user-count
--per-user-scope --select-min --select-max --groups --apply/--no-apply --sponsor --sponsor-tel --cover`。
注意：改时间时结束时间必须晚于开始时间；`--groups` 传空串可清空分组；标题≤50 字。

### 添加选手（item-add）

```bash
# 单个添加（image 必填）
python scripts/caiguwang_cli.py item-add --id 19630 --name "张三的作品" --image "https://..."

# 批量添加（JSON，同 create 的选手格式；分组活动可在每个选手里加 "cat_id" 指定分组序号）
python scripts/caiguwang_cli.py item-add --id 19630 --items-file items.json
```

注意：活动若要求参赛图片（图文投票默认要求），每个选手都必须带 image；活动要求视频/音频/文件/手机号时，本命令会被拒绝，请引导用户到网页后台添加。
**单次最多 200 位选手**（可分多次追加）；选手更多时引导用户到网页后台「批量导入选手」上传。

### 修改选手（item-update）

```bash
# item_id 从 vote-data 的返回里取（每行选手有对应 ID 字段）
python scripts/caiguwang_cli.py item-update --id 19630 --item-id 881 --name "新名称" --image "https://..."
```

不提供选手删除——如需删除或下架选手，引导用户到网页后台操作。

### 分组改名（group-rename）

```bash
# 按分组序号改（从 0 开始）
python scripts/caiguwang_cli.py group-rename --id 19630 --index 1 --new-name "书法组"

# 按原分组名改
python scripts/caiguwang_cli.py group-rename --id 19630 --name "摄影组" --new-name "手机摄影组"
```

只改分组名称，**不改选手归属**（选手按分组序号挂组）；改名后返回完整分组列表。不提供分组的新增/删除/选手换组——请引导用户到网页后台操作。

### 我的素材列表（material）

```bash
python scripts/caiguwang_cli.py material            # 全部素材（最近上传在前）
python scripts/caiguwang_cli.py material --cate 0   # 仅未分组
python scripts/caiguwang_cli.py material --page 2 --size 20
```

返回素材 `url`（图片可直接用作选手图片或 `--cover`）、`type`（1图片 2视频 3音频 4文件）、上传日期。创建活动前若用户说"用我之前传过的图"，先用本命令列出素材再选用。

## 上传图片

选手图片/封面图支持两种来源：本地图片文件（multipart 上传）或图片链接（远程抓取）。

```bash
# 上传本地图片文件
python scripts/caiguwang_cli.py upload --file /path/to/photo.jpg

# 抓取图片链接（AI 生成的图片、图床链接均可）
python scripts/caiguwang_cli.py upload --url https://example.com/p1.jpg

# 封面图：加 --crop 750x464（与网页后台轮播图裁剪比例一致，CLI 本地裁剪）
python scripts/caiguwang_cli.py upload --file /path/to/cover.jpg --crop 750x464
python scripts/caiguwang_cli.py upload --url https://example.com/cover.jpg --crop 750x464
```

返回 `{"data": {"image_url": "https://..."}}`，把 `image_url` 用于 create 的选手图片或 `--cover`。

**限制（与网页后台一致）**：
- 图片：jpg/png/gif/webp，**10MB 以内**；
- **上传前自动压缩**（与网页后台上传行为一致）：宽 > 1000 缩到 1000；PNG→webp（缩放 0.82 / 仅压 0.88）、其他→jpg（0.8 / 0.9）；宽≤1000 且 ≤200KB 不压；**GIF 不压**；压缩结果更小才采用（需 Pillow，未装则原图上传）；
- 封面图：网页后台要求 **750:464 比例**。处理方式：
  - `upload --crop 750x464` 会**在本地**（CLI）用 Pillow 中心裁剪成 750×464 后上传，与后台裁剪效果一致；
  - 本地未装 Pillow 时，服务端只做**比例校验**（不依赖 GD）：比例符合直接存，不符则报错并提示先裁剪；
  - 可选依赖：`pip install pillow`（仅封面自动裁剪需要）；
- **视频/音频不支持**：Skill 只做图文投票，视频/音频请在网页后台「素材管理」或活动编辑页上传；
- 上传后自动进入该账号素材库。

## 活动列表

```bash
python scripts/caiguwang_cli.py list --page 1 --size 10 --status ongoing --kw "绘画"
```

`--status` 可选 `ongoing`（进行中）/ `ended`（已结束）/ `pending`（未开始）。
返回含每个活动的参与人数、累计投票、浏览次数。

## 投票数据（选手榜单）

```bash
python scripts/caiguwang_cli.py vote-data --id 19630 --page 1 --size 20
```

返回选手榜（`rank` 名次 / `name` 选手 / `votes` 票数），按票数降序。

## 活动整体数据

```bash
python scripts/caiguwang_cli.py view-data --id 19630
```

返回参与人数（`participants`）、累计投票（`votes`）、浏览次数（`visits`）、TOP5。

## 返回值与错误

统一形态：`{"success": true|false, "code": 200|1002|400|429|500, "msg": "...", "data": ...}`

| code | 含义 |
|---|---|
| 200 | 成功 |
| 1002 | 令牌无效/已停用/被冻结 → 引导用户到后台「养虾Skill」页检查开关或重置 |
| 400 | 参数错误（msg 有具体中文提示，可直接转述给用户） |
| 429 | 今日创建次数已达上限（手动创建每天 20 次；AI 生成单独配额） |
| 500 | 服务异常 → 建议稍后重试或到网页后台操作 |

## 边界说明（务必遵守）

1. **创建即生效**：活动按投票时间自动开启/结束；把小程序码（分享）和编辑链接（调整）告知用户；
2. **修改期限**：活动**结束后 1 天**起，修改活动/添加和修改选手会被拒绝（与网页后台一致），提示用户"活动已结束，超过修改期限，请重新创建活动"；
3. **不提供删除/清空数据等高危操作**：如用户要求删除活动，引导其到网页后台或小程序操作；
4. **选手图片/封面**：本地图片先经 `upload` 转为素材 URL 再传给 create；封面图用 `upload --crop 750x464` 裁剪后再 `--cover` 传入（后台轮播图强制该比例）；视频/音频不开放，引导用户到网页后台操作；
5. **内容规范**：活动标题与说明须积极健康，违法违规内容平台会拒绝；
6. 网页后台和小程序端功能更全（批量导入、防刷设置、海报等），复杂配置引导用户到对应端操作。
