---
name: douyin-favorites-batch-add
description: "Use when 把抖音作品批量收藏并放入指定收藏夹（建夹、入夹、逐条回读、断点续跑）。"
version: 1.0.1
author: Hermes
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [douyin, favorites, cdp, automation, xlsx]
    category: social-media
---

# 抖音批量入收藏夹

把一份作品清单（XLSX 导出的 ID/标题/作者/发布时间）逐条收藏并放进指定抖音收藏夹。支持新建私密夹、复用已有夹、逐条回读验证、写日志、断点续跑。

不读 Cookie、不依赖 MyLike：用独立 Chrome 配置目录（CDP 9333）让页面自己带上登录态与签名。

## 前置条件

- Windows + Chrome + Node（需 `ws`）
- 首次运行要在弹出的 Chrome 里扫码登录一次，登录态保存在独立 profile，之后复用
- 清单文件 `items.json`，字段：`id,title,author,published,type,link`

## 目录

```
D:\Tools\mylike-fav-import\
├─ run2.mjs            主脚本
├─ items.json          待处理清单
├─ log.csv             逐条结果日志
└─ chrome-profile\     独立浏览器配置（含登录态）
```

脚本顶部的 `DIR` 常量指向该目录；换目录时同时改 `DIR` 和浏览器 `--user-data-dir`。

## 启动浏览器

Hermes 的工具进程可能跑在 session 0，直接 `Start-Process` 打开的窗口用户看不见。必须用「交互式登录」计划任务把它投到桌面会话：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File D:\Tools\mylike-fav-import\launch_visible.ps1
```

需要把窗口置前时：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File D:\Tools\mylike-fav-import\run_front.ps1
```

窗口标题带 “Google Chrome”，登录后不要关闭它，后续命令都复用同一个浏览器。

## 命令

```bash
cd D:/Tools/mylike-fav-import

node run2.mjs status                       # 登录态与昵称
node run2.mjs folders                      # 现有收藏夹（id/名称/数量/可见性）
node run2.mjs add --folder "2022年4月" --limit 2   # 试跑两条
node run2.mjs add --folder "2022年4月"             # 全量
node run2.mjs verify --folder "2022年4月"          # 复核缺失
node run2.mjs shot --out proof.png         # 页面截图
node run2.mjs eval --js "<表达式>"          # 页面内取值/调试
node run2.mjs move-test --id <作品ID> --folder "<夹名>"   # 单条入夹探路，回显 in_folder
```

`add` 在收藏夹不存在时直接失败（`FOLDER_MISSING`），脚本不会自动建夹。需要新夹时先在抖音收藏页手工建，或按下面记录的建夹接口自行调用一次。

## 接口约定（脚本内置，改动前先核对）

- 读：页面同源 `fetch`，带 `aid=6383&device_platform=webapp`
- 写：必须走页面自己的 `window.axiosInstance`（它会附加 CSRF 与签名；裸 fetch 一律返回 `status_code 5 参数不合法`）
- 收藏：`POST /aweme/v1/web/aweme/collect/`，body `aweme_id / action=1 / aweme_type`
- 入夹：`POST /aweme/v1/web/collects/video/move/`，参数全在 query：`item_ids=<id>&item_type=2&to_collects_id=<夹ID>&update_collects_sort=true`，body 为空
- 建夹：`POST /aweme/v1/web/collects/maintain/`，body `action=1 / collects_name / secret=1`（1=私密）
- 读夹：`/aweme/v1/web/collects/list/` → 键 `collects_list`
- 读夹内：`/aweme/v1/web/collects/video/list/` → 键 `aweme_list`，分页用 `cursor` + `has_more`

## 每条的处理顺序

1. 读详情取 `collect_stat` 与 `aweme_type`；`collect_stat` 缺失即跳过（不可判定）
2. 未收藏则先收藏（`collect_stat=0`）
3. 入夹
4. 翻夹内列表回读该 ID，确认到位才记为成功
5. 写一行 `log.csv`，间隔 1.8~3 秒随机

## 验收

- `folders` 里目标夹的 `count` 等于清单条数
- 翻完夹内全部页面取到的 `aweme_id` 集合与 `items.json` 完全一致（缺失 0）
- `log.csv` 全部记录 `verified=yes`

## 运行纪律

- 先 `--limit 2` 试跑，确认 `verified=yes` 再全量
- 单批不超过 200 条；完成后抽样回读
- 只添加不删除：脚本不提供取消收藏、移出夹、删夹
- 遇到登录失效、验证码、风控提示：停下来人工处理，不自动重试
- 撤销只能在抖音页面手动操作，脚本没有回滚功能

## 定时批量（队列式、无人值守）

适用于成百上千条、跨多个收藏夹、分多天跑完的场景。

### 文件

```
D:\Tools\mylike-fav-import\
├─ douyin-queue\state.json      总进度：每夹 cursor/ok/failed/folder_id/status
├─ douyin-queue\items\*.json   每夹一份清单
├─ run_batch.mjs               批量入口（缺夹自建、逐条回读、断点续跑）
├─ rounds.jsonl                每轮汇总
├─ log.csv                    逐条日志（首列 folder）
├─ keepalive.ps1             Chrome 巡检（掉了自动重拉）
└─ register_keepalive.ps1    注册计划任务 MyLikeFavChromeKeepalive
```

cron 入口脚本放在 `%LOCALAPPDATA%/hermes/scripts/douyin_fav_batch.py`（包装 `node run_batch.mjs run`，默认 200 条；`MAX=2 python douyin_fav_batch.py` 可小样），队列、日志、chrome-profile 仍在 `D:\Tools\mylike-fav-import`。

### 命令

```bash
node run_batch.mjs plan                                     # 剩余条数、已完成夹数、下三个夹进度
node run_batch.mjs run --max 5 --dry                       # 只看本轮处理哪些夹，不写
node run_batch.mjs run --max 5 --folder "01-01-孩子玩耍"    # 指定夹小样
python "$LOCALAPPDATA/hermes/scripts/douyin_fav_batch.py"        # 正式一轮（默认 200 条，cron 调的就是它）
MAX=2 python "$LOCALAPPDATA/hermes/scripts/douyin_fav_batch.py"  # 小样测试
python reorder_state.py "C:/path/MyLike_分类结果_<日期>.xlsx"      # 表改了之后按新表重排 state 顺序，保留进度
```

### 当前采用节奏

- 每天 09:00 / 15:00 / 21:00 各一轮，单轮 200 条，单日 600 条（cron 任务 f865fddb2072，表达式 `0 9,15,21 * * *`）
- 条间隔三档随机：70% 8~13 秒，25% 13~22 秒，5% 30~60 秒（平均约 14 秒，含校验约 22~23 秒/条）
- 每 30~50 条（随机）插一次 2.5~6 分钟长停；收藏→入夹 2.5~5 秒；入夹→回读 1.2~2.5 秒；建夹后停 30~90 秒
- 每轮开跑前随机延后 0~12 分钟（`NO_JITTER=1` 可跳过，测试用）
- 单轮约 95~105 分钟，最坏不超过 150 分钟；连续 5 条失败即停轮（验证码、`参数不合法` 这类风控会表现为连续失败，靠这条兜底；脚本不单独识别验证码）
- 全量 19,139 条按 600/天约 32 天；cron 脚本超时要抬到 9000 秒（config.yaml 的 `cron.script_timeout_seconds`）

### 夹命名与建夹

- 直接用表格里的文件夹名，保留 `01-01-` 编号前缀（收藏夹列表可按序排）
- 统一建私密夹（secret=1），缺夹时本轮自动建，建完回读确认 id
- 不删夹、不改名、不取消收藏；脚本只增不删
- 图文作品先后用 item_type 2 / 1 尝试入夹，log 的 move 列记 `img:<code>`

### 保活与定时

- 计划任务 `MyLikeFavChromeKeepalive` 每 10 分钟巡检 9333 端口，掉了就拉起 `MyLikeFavChrome`（注册脚本 `register_keepalive.ps1`）
- 任务动作必须是 `C:\Windows\System32\wscript.exe` 加参数 `//B //Nologo "D:\Tools\mylike-fav-import\keepalive_hidden.vbs"`；VBS 用 `Run(..., 0, False)` 隐藏启动 `keepalive.ps1`。不要把 `powershell.exe -WindowStyle Hidden` 直接写进任务动作——它仍会每轮闪一次控制台窗口
- `keepalive.ps1` 已内联窗口隐藏（`Add-Type WinApiKH` + `EnumWindows`/`ShowWindow`），一轮只起一个进程；`hide_chrome_window.ps1` 仅留作手工单跑
- 改任务动作用 `update_task_action.ps1`；改前先 `schtasks /query /tn MyLikeFavChromeKeepalive /xml > keepalive_task_backup.xml` 备份，回滚用 `schtasks /create /tn MyLikeFavChromeKeepalive /xml keepalive_task_backup.xml /f`
- 改完自检：`Start-ScheduledTask` 手跑一次，`hide_chrome.log` 应新增一行 `done visible_before=…`、任务 `LastTaskResult=0`、期间扫不到控制台窗口（`test_keepalive.ps1`）
- Hermes cron 写法：`cronjob_manage(script='douyin_fav_batch.py', schedule='0 9,15,21 * * *')`，脚本 stdout 自动注入 prompt，由 agent 汇成简报
- cron 的 script 必须是 `.py`：调度器进程 PATH 里没有 bash，`.sh` 会直接报 bash not found

### 每轮验收与简报

- `SUMMARY` 行的 ok/failed；`plan` 的 remaining 与 done_folders
- 简报三条数字：本轮成功/失败、累计与剩余、预计完成日（今天 + ceil(剩余/200)）
- 每周抽一个夹跑 `verify`，核 count 与清单条数、缺失 0

### 异常处理

- `NOT_LOGGED_IN` / `no douyin page open`：登录态失效，人工在 Chrome 窗口扫码
- `CDP_DOWN` / `RUN_TIMEOUT`：看 `keepalive.log`，确认 Chrome 是否在用户会话里跑起来
- 失败条目 note 出现 `move-failed` / `参数不合法`：疑似风控，停几天再跑，不自动重试

## 清单来源

来源表是 MyLike 的分类结果 `MyLike_分类结果_<日期>.xlsx`，三张工作表：

- `文件夹清单`（每行一个夹）：A 序号、B 文件夹名（即抖音夹名，保留 `01-01-` 这类前缀）、C 大类、D 条数、E/F/G 内容示例。D 列是该夹应有的条数。
- `分类明细`（作品逐条）：A 序号、B 文件夹名、C 大类、D 小类、E 作品标题、F 作者、G 内容类型、H 发布时间、I 作品链接、J 作品ID。同一夹的行在表中连续成块。
- `汇总`：作品总数、文件夹总数、待归类条数。

建队列时按 `文件夹清单` 的行顺序，每个夹生成一份 `douyin-queue/items/<文件夹名>.json`，每条形如 `{id,title,author,type,published,link}`：`id` 取 J 列作品ID，`title/author/type/published/link` 取 E/F/G/H/I，顺序照明细表。

生成后核对三项：每夹 items 条数 = 清单表 D 列；全部合计数 = 汇总表「作品总数」；同一夹的 ID 集合与明细表该夹块一致。

### 表格改版后同步队列（不丢进度）

表格顺序调整（例如把某个大类整块前移）或重新分类后，只改 state 的顺序，不重建 state.json：

1. 逐夹比对：新表该夹的作品ID集合与已有 `items/<夹名>.json` 一致时保留状态；不一致时只替换该夹 items 文件，并把该夹 `cursor/ok/failed` 归零重跑（旧夹内已入的条目不会自动移出）。
2. 按新表 `文件夹清单` 的行顺序重排 `state.json` 的 `folders` 数组，每条逐字段保留 `cursor / ok / failed / folder_id / status`，只动数组顺序。
3. 夹名不变时已入夹进度继续有效，`status=done` 的夹不再处理。
4. 改完跑 `node run_batch.mjs plan`：`total_folders` 应等于清单表行数，`remaining` 应等于改前剩余量（除非有条目集合变化）。
5. 夹名本身改了等于新建夹：旧夹内容留在旧夹（脚本只增不删），需人工在抖音处理。
6. 文件名带日期的表若有多个版本，以最新版本为准，并把 `state.json` 的 `source` 改成新表文件名。

## 文件清单（随技能发布）

```
douyin-favorites-batch-add/
├─ SKILL.md
├─ package.json / package-lock.json     node 依赖（ws）
└─ scripts/
   ├─ run2.mjs              单夹：status / folders / add / verify / shot / eval / move-test
   ├─ run_batch.mjs         队列：plan / run（缺夹自建、断点续跑、按夹重排）
   ├─ reorder_state.py      表格改版后按新表重排 state.json 顺序，保留进度
   ├─ wait_then_reorder.py  等一轮跑完后自动重排（配合手工改表）
   ├─ keepalive.ps1         每 10 分钟巡检 CDP，掉了重拉 Chrome，并内联隐藏窗口
   ├─ keepalive_hidden.vbs  以 wscript 静默启动 keepalive.ps1（避免控制台闪窗）
   ├─ register_keepalive.ps1  注册计划任务 MyLikeFavChromeKeepalive（登录时 + 每 10 分钟）
   ├─ update_task_action.ps1  把计划任务动作改成 wscript + VBS
   ├─ test_keepalive.ps1    保活自检：手跑一次、查日志、查 LastTaskResult、扫控制台窗口
   ├─ launch_visible.ps1    把 Chrome 投到交互会话（解决 session 0 看不见窗口）
   ├─ front.ps1 / run_front.ps1  把 Chrome 窗口置前
   ├─ show_chrome_window.ps1 / hide_chrome_window.ps1  显式显示/隐藏 Chrome 窗口
   ├─ find_window.ps1       按标题找窗口句柄（调试用）
   ├─ kill_chrome.ps1 / close_chrome.mjs  只关本 profile 的 Chrome
   ├─ make_shortcut.ps1     生成桌面快捷方式
   ├─ progress.ps1 / progress.cmd  进度看板（读 state.json 汇总剩余）
   ├─ click_login.js        首次登录时点"扫码登录"入口
   ├─ probe_move.js         入夹接口探路（单条试跑，打印响应）
   └─ legacy/run.mjs        第一版单夹脚本（已被 run2.mjs 取代，保留备查）
```

工作目录约定（脚本内 `DIR` 常量 / `$DIR`）：`D:\Tools\mylike-fav-import`。换目录要同时改脚本里的路径与浏览器 `--user-data-dir`。

不含：登录态（`chrome-profile/`）、作品清单（`items.json`、`douyin-queue/`、`scan.json`）、运行日志与截图。这些都是账号私有数据，自行在本地保留。
