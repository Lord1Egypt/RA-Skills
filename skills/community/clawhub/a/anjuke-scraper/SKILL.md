---
name: anjuke-scraper
description: "安居客（58 系）房源数据采集与对比分析：抓取租房列表与详情、提取经纪人电话、高德 poiInfo 获取小区坐标、haversine 计算距目标地点距离、生成排序过滤后的 Excel 对比表。适用：找房对比、房源数据分析、换城市/关键词复用采集管线。"
version: "1.0.0"
---

# 安居客房源采集与对比分析 Skill

将「爬虫采集房源 → 坐标定位 → 距离对比 → Excel 交付」完整流程封装为可复用管线。
已验证：重庆两江新区互联网产业园附近整租，87 套房源零验证码采集，44 套筛选交付（2026-08-13）。

## 什么时候用

- 用户要「某地附近租房/房源对比表」
- 需要批量采集安居客/58 系房源并结构化整理
- 需要计算房源小区距某个目标地点（公司/学校）的距离并排序

## 前置条件

1. **用户调试 Chrome 已启动**：`google-chrome-debug` 配置目录（`~/.config/google-chrome-debug`），远程调试端口 **9222**
   - 启动方式（需用户在场确认浏览器窗口）：
     `google-chrome-stable --remote-debugging-port=9222 --user-data-dir=/home/yax/.config/google-chrome-debug --no-first-run`
   - 必须用**用户登录态**（复用电商/地图等站点的登录与验证状态）
2. **Python 依赖**：`playwright`（async API）、`openpyxl`；`python3.11` 已验证
3. **终端代理**：默认不走 GNOME 代理，需 `export HTTP_PROXY=http://127.0.0.1:7897 HTTPS_PROXY=http://127.0.0.1:7897`

## 管线流程（scripts/ 按序执行）

```
grab_all.py      → 列表页全页抓取 + 解析卡片 → final_records.json（含 phone_from_id 提取的电话）
fetch_details.py → 批量详情页补全（交付方式/地址/装修/电话）→ detail_results.json
amap_coords2.py  → 高德 poiInfo 定位公司 + 各小区坐标 → coords.json（含 haversine 距离）
make_excel3.py   → 合并数据 → Excel（过滤租金、按 距离→房租 排序、14 列）
```

中间产物：`cards.json / all_cards.json / records.json / final_records.json / detail_results.json / coords.json`。
数据文件默认输出到 `anjuke_scraper/` 工作目录（各脚本顶部 `OUT` 变量可改）。

## 换城市 / 关键词复用

改各脚本顶部常量（已标注 `# CONFIG` 区）：

1. **关键词**：`KW_ENC` 为关键词的 URL 编码（`python3 -c "import urllib.parse; print(urllib.parse.quote('关键词'))"`）
2. **域名**：重庆租房是 `cq.zu.anjuke.com`；其他城市换 `xx.zu.anjuke.com`（xx=城市拼音，如 sh/bj/gz）
3. **目标地点**：`amap_coords2.py` 里公司搜索词列表
4. **过滤条件**：`make_excel3.py` 里租金阈值 `>=2000` 与排序列

## 踩坑大全（实测沉淀，2026-08-13）

### 站点结构
- 安居客**租房**域名是 `cq.zu.anjuke.com`（`chongqing.anjuke.com` 是二手房/新房站）；首页「租房」频道链接指向的才是 zu 子域
- 搜索不能 URL 直带 keywords（会「页面丢失」），必须**页面搜索框提交**；翻页 URL 格式是 **`x1-p{n}`（连字符）**，不是 `x1/p{n}`

### 反爬与验证码
- 58 antibot 验证码：**goto 直访详情页必触发**；带 `referer`（列表页 URL）+ 随机延迟 **3–6s** 可完全规避（实测 87 条零验证码）
- 触发验证码特征：URL 含 `verifycode` / `antibot`；脚本已内置检测 + 截图留存

### 数据提取
- **房源 ID 内嵌经纪人手机号**：`/fangyuan/4696133412380676` → 正则 `1[3-9]\d{9}` 直接从 ID 提取，无需进详情页
- 部分经纪人只留「微信扫码联系」二维码：canvas 加密绘制，cv2 QRCodeDetector 解不出 → Excel 如实标注「仅微信」，不硬解

### 坐标与距离
- 高德 `www.amap.com/service/poiInfo`：**页面上下文 fetch 带登录 cookie 免 API key**（需 Referer header），返回 `data.poi_list[].longitude/latitude`
- **百度地图 URL 坐标是墨卡托投影（非经纬度）**且搜索不触发时返回默认中心点，不可靠 → 一律用高德
- 距离计算用 haversine 公式（`make_excel3.py` 内实现），直线距离即可满足「距公司 X km」需求

### 环境
- Playwright 用 `connect_over_cdp("http://127.0.0.1:9222")` 直连用户调试 Chrome——绕开 OpenClaw browser 工具 user profile 连接 bug（DevToolsActivePort 路径错误）
- 二维码截图用 `page.screenshot` 后 ImageMagick 转换；Wayland rootless 下 mss/xwd-root 黑屏，`xwd -id` 可用

## 验证方式

- 采集数量核对：列表页翻页总数 vs `final_records.json` 条数一致
- 零验证码确认：`fetch_log.txt` 无 verify 记录
- Excel 抽查：随机 3 条房源 URL 手动打开，电话/地址/租金一致
