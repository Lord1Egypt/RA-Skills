---
name: beijing-signed-price-tracker
description: Track configured Beijing Housing Commission new-home projects from bjjs.zjw.beijing.gov.cn project-detail URLs, read project signed-unit counts, signed area, and average price, crawl building tables including “查看更多” and paginated lists, treat both “已签约” and “网上联机备案” as signed units, estimate the implied average price per m² of newly signed rooms from changes between the previous and current project summaries, cache unsold room metadata locally, persist rows into a Feishu spreadsheet as the single source of truth, and send Feishu DM notifications after each run. Use when asked to monitor one or more Beijing pre-sale projects, update a project mapping, sync newly signed rooms into a Feishu sheet, infer newly signed average price, verify duplicate insertion behavior, or notify on updates.
---

# Beijing Signed Price Tracker

使用 `scripts/tracker.js` 维护多个地块名到北京住建委项目详情链接的映射，并把新发现的“已签约 / 网上联机备案”房屋写入**飞书表格**。

## 核心文件

- `projects.json`：项目映射 + 飞书表格配置
- `scripts/tracker.js`：抓取、解析、估算、写入、排序主脚本
- `room-cache.json`：本地房源缓存（缓存未签约房屋的建筑面积/户型，供后续签约时补齐）

## 满足的规则

1. 允许配置多个地块名到北京住建委项目详情链接的映射；同一地块名也可以绑定多个项目详情链接，并在同步时合并处理。
2. 从项目详情页提取：
   - 已签约套数
   - 已签约面积(M2)
   - 成交均价（￥/M2）
3. 从楼盘表页提取每套房的：
   - 销售楼号
   - 自然楼层
   - 房号
   - 销售状态
4. 如果项目详情页有“查看更多”，继续抓取 `pageId=411612` 楼盘表列表页。
5. 如果楼盘表列表页有多页，依次处理全部页。
6. 将 `已签约` 与 `网上联机备案` 统一视为签约房屋。
7. 账本仍以飞书表格为唯一真实历史来源；但会额外维护本地 `room-cache.json`，缓存未签约房屋的 `建筑面积` 与 `户型`。
8. 同步时会先扫描整盘楼盘表；对可访问房屋详情页的未签约房源补缓存；对已签约 / 网上联机备案房号，判断其是否已经存在于飞书表格中。
9. 上次查询基线按**地块名**从飞书表格中反向解析；如果不存在，则 `已签约套数`、`已签约面积(M2)`、`项目成交均价` 都视为 `0`。
10. 新签约均价按面积差公式估算：

   `估计新签约均价 = (本次已签约面积 * 本次项目成交均价 - 上次已签约面积 * 上次项目成交均价) / (本次已签约面积 - 上次已签约面积)`

11. 飞书表格列固定为：

   `地块名,销售楼号,自然楼层,房号,建筑面积,户型,估计成交价,项目已签约套数,已签约面积(M2),项目成交均价,更新时间`

12. 写入时只在表格底部追加新行；历史行内容不回写、不改单元格值。允许统一排序，也允许从旧版 8 列表头迁移到新版 11 列表头（旧数据新增列会留空）。
13. 追加完成后，对整张表按以下优先级排序：
    - 地块名
    - 更新时间
    - 销售楼号
    - 自然楼层
    - 房号
14. 更新时间统一使用 `YYYY-MM-DD HH:MM:SS`。
15. 每次执行结束后都发飞书私聊通知：
    - 有新增签约：通知内容为本次新增行，按窄屏友好格式分组展示
    - 无新增签约：发送“本次无新增签约”摘要

## 飞书表格约束

- 飞书表格是**唯一真实数据源**。
- 首次使用时，如果表格为空，脚本会自动写入表头。
- 如果表格首行是旧版 8 列表头，脚本会自动迁移为新版 11 列表头，并保留历史行。
- 如果表格首行既不是新版也不是旧版表头，脚本会报错停止，避免破坏历史数据。
- 如果飞书应用没有该表格权限，脚本会提示你在文档右上角添加文档应用。

## 本地缓存约束

- 本地缓存文件：`room-cache.json`
- 缓存 key：`地块名 + 销售楼号 + 自然楼层 + 房号`
- 仅用于补充签约后无法再读取的 `建筑面积` 与 `户型`
- 如果房屋在签约前未曾成功缓存，则签约入表时对应列会为空，并在同步报告中给出警告

## 状态颜色

`scripts/tracker.js` 按楼盘表颜色识别状态：

- `#FF0000` → 已签约
- `#d2691e` → 网上联机备案
- `#FFCC99` → 已预订
- `#33CC00` → 可售
- `#CCCCCC` → 不可售
- `#ffff00` → 已办理预售项目抵押
- `#00FFFF` → 资格核验中

只有 `已签约` 和 `网上联机备案` 会写入飞书表格；未签约状态会用于刷新本地缓存。

## 配置文件格式

`projects.json` 示例：

```json
{
  "feishu": {
    "sheetUrl": "https://my.feishu.cn/sheets/Y944sbj2khtLcNtb7jec7MIrnxd",
    "spreadsheetToken": "Y944sbj2khtLcNtb7jec7MIrnxd",
    "sheetId": "eee767",
    "sheetTitle": "Sheet1",
    "appId": "cli_xxx",
    "appSecret": "xxx",
    "notifyUserOpenId": "ou_xxx"
  },
  "projects": [
    {
      "name": "清樾府04地块",
      "url": "http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=320794&projectID=8138177&systemID=2&srcId=1"
    }
  ]
}
```

也可以通过环境变量覆盖：

- `FEISHU_SHEET_URL`
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_NOTIFY_USER_OPEN_ID`

## 命令

```bash
node scripts/tracker.js set-feishu --sheet-url "https://my.feishu.cn/sheets/Y944sbj2khtLcNtb7jec7MIrnxd" --app-id "cli_xxx" --app-secret "xxx" --notify-user-open-id "ou_xxx"
node scripts/tracker.js add --name "清樾府04地块" --url "http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=320794&projectID=8138177&systemID=2&srcId=1"
# 同一地块名重复 add 新链接时，脚本会把链接追加到该地块配置下
node scripts/tracker.js list
node scripts/tracker.js sync
node scripts/tracker.js sync --name "清樾府04地块"
```

也可以临时同步一个未写入配置的项目：

```bash
node scripts/tracker.js sync --name "临时项目" --url "http://bjjs.zjw.beijing.gov.cn/eportal/ui?pageId=320794&projectID=8138177&systemID=2&srcId=1" --sheet-url "https://my.feishu.cn/sheets/Y944sbj2khtLcNtb7jec7MIrnxd" --app-id "cli_xxx" --app-secret "xxx"
```

## 实施要求

- 先使用项目详情页统计值作为总量基准，再扫描楼盘表找具体房号。
- 必须处理“查看更多”和分页，不能只依赖项目详情页第一页展示的部分楼栋。
- 同步时顺带刷新可访问房屋详情页的未签约房源缓存。
- 如果 `签约套数变化` 与 `本次发现的新房号数` 不一致，输出警告，但仍按当前楼盘表结果判断哪些房号需要新增。
- 如果项目总签约套数或签约面积下降，不回滚历史数据，只报告异常。
- 如果楼盘表出现历史没有的新房号，但项目签约面积没有增加，则跳过这些房号并给出警告，避免估价失真。
- 默认顺序抓取，避免高频并发请求。
- 排序通过脚本在读取全部账本后统一重写已排序区间完成。

## 通知规则

- 每次执行结束都会发飞书私聊通知。
- 有新增时，通知内容就是新增行本身，按地块分组并适配手机窄屏阅读。
- 没有新增时，发送简短摘要，说明“本次无新增签约”。
- 通知目标由 `feishu.notifyUserOpenId`（或环境变量 `FEISHU_NOTIFY_USER_OPEN_ID`）控制。
