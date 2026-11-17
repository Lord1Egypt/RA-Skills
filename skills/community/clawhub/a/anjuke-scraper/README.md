# anjuke-scraper

安居客（58 系）房源数据采集与对比分析管线：抓取租房列表与详情、提取经纪人电话、高德坐标定位、haversine 距离计算，一键生成排序过滤后的 Excel 对比表。

> 实测案例：重庆两江新区互联网产业园附近整租，**87 套房源零验证码采集，44 套筛选交付**（14 列结构化数据，按 距离→房租 排序）。

## 特性

- 🚫 **零验证码反爬方案**：详情页带 referer + 随机延迟 3–6s，实测 87 条全程无验证码
- 📞 **电话提取三板斧**：房源 ID 内嵌手机号 → 卡片 HTML 全局电话库 → 详情页正文（排除编码误匹配）
- 🗺️ **免 API Key 坐标**：高德 poiInfo 页面上下文 fetch（复用登录 cookie），haversine 直线距离
- 📊 **Excel 交付**：14 列、租金过滤、距离→房租双排序、距离色阶标注、冻结表头 + 筛选
- ♻️ **可复用**：config.json 换城市/关键词/预算即可复跑，断点续抓（详情页进度自动保存）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动带远程调试端口的 Chrome（复用你的登录态）

```bash
google-chrome-stable --remote-debugging-port=9222 \
  --user-data-dir=$HOME/.config/google-chrome-debug --no-first-run
```

> 必须使用平时登录过安居客/58 的浏览器配置目录，避免额外验证。

### 3. 配置

```bash
cp config.example.json config.json
```

| 字段 | 说明 | 示例 |
|---|---|---|
| `city` | 城市中文名（用于高德搜索） | `重庆` |
| `city_pinyin` | 城市拼音（安居客子域） | `cq` |
| `keyword` | 搜索关键词 | `两江新区互联网产业园` |
| `max_pages` | 列表翻页数 | `8` |
| `target_places` | 目标地点搜索词（按序尝试，取第一个命中） | `["重庆两江数字经济产业园 互联网园一期", ...]` |
| `max_rent` | 预算上限（元/月，超出过滤） | `2000` |
| `cdp_port` | Chrome 调试端口 | `9222` |
| `output_dir` | 输出目录（默认 config.json 同目录下 `output/`） | `output` |

### 4. 运行管线

```bash
python3 scripts/grab_full.py       # ① 抓列表页卡片 → cards_full.json
python3 scripts/parse_final.py     # ② 离线精解析 → final_records.json
python3 scripts/fetch_details.py   # ③ 详情页补全 → detail_results.json
python3 scripts/amap_coords2.py    # ④ 高德坐标+距离 → coords.json
python3 scripts/make_excel3.py     # ⑤ 生成 Excel 对比表
```

每一步都可独立重跑；③ 支持断点续抓。结果在 `output/<关键词>附近房源.xlsx`。

> 非默认配置：`python3 scripts/grab_full.py --config /path/to/config.json`

## 输出示例（Excel 14 列）

```
地址 | 距目标(km) | 房租(元/月) | 交付类型 | 房型 | 联系人 | 电话 | 标题 | 朝向 | 楼层 | 装修 | 小区 | 区域 | 链接
金竹苑2区 两江新区... | 0.9 | 1300 | 付3押1 | 1室1厅1卫 47.00 | 谭世林 | 微信扫码联系 | ... | ... | ... | ... | ... | ... | https://cq.zu.anjuke.com/fangyuan/...
```

距离列 ≤2km 绿色、≤5km 黄色；表头冻结 + 自动筛选。

## 踩坑沉淀（都是实测过的坑）

- 安居客租房域名是 `{城市拼音}.zu.anjuke.com`，`{城市}.anjuke.com` 是二手房/新房站
- 搜索**不能** URL 直带 keywords（页面丢失），需页面搜索框提交；翻页 URL 是 `x1-p{n}`（**连字符**，不是斜杠）
- 58 antibot：goto 直访详情页必触发验证码；带 `referer` + 随机延迟 3–6s 可完全规避
- 房源 URL 的 ID 里**内嵌经纪人手机号**：`/fangyuan/4696133412380676` → 正则 `1[3-9]\d{9}` 直接提取
- 部分经纪人只留微信二维码（canvas 加密绘制，cv2 解不出）→ Excel 如实标注「微信扫码联系」
- 高德 `www.amap.com/service/poiInfo` 页面上下文 fetch 免 API key（需 Referer header）
- **百度地图 URL 坐标是墨卡托投影（非经纬度）**，且无搜索时返回默认中心点——不可靠，用高德
- Playwright 用 `connect_over_cdp` 直连用户 Chrome，绕开无头浏览器被反爬识别的问题

## 项目结构

```
anjuke-scraper/
├── config.example.json   # 配置模板
├── requirements.txt
├── scripts/
│   ├── grab_full.py      # ① 列表页抓取（文本+HTML）
│   ├── parse_final.py    # ② 离线精解析
│   ├── fetch_details.py  # ③ 详情页补全
│   ├── amap_coords2.py   # ④ 高德坐标 + 距离
│   └── make_excel3.py    # ⑤ Excel 生成
└── output/               # 运行产物（gitignore）
```

## 免责声明

本工具仅用于个人租房信息整理与学习研究。请遵守目标网站服务条款，控制请求频率，勿用于商业用途或大规模抓取。

## License

MIT
