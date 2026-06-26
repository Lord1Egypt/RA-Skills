# Citywalk Map Generator 🗺️

> 一行命令生成精美的步行路线图，基于真实 OSM 地图底图，横向全屏设计。

[English](README.en.md) | 中文

---

## ✨ 功能特点

- 🌏 **真实地图** - 基于 OpenStreetMap 数据，不穿墙不穿海
- 🚶 **真实路线** - 使用 OSRM 步行导航，获取实际道路几何
- 🇨🇳 **国内适配** - OSM 加载失败自动切换高德地图（国内秒开）
- 🖥️ **横向全屏** - 横向全屏布局，电脑和手机都完美展示
- 🎨 **自定义主题** - 一行命令切换任意主题色（支持国家/城市主题色）
- 🌦️ **天气查询** - 自动查终点城市当前天气（wttr.in 免费，无需 API Key）
- 🌐 **双语界面** - 支持中文 / English 切换
- 🖼️ **离线渲染** - `render.py` 纯 Python 生成路线图图片（无需浏览器）
- ⚡ **零依赖** - generate.py 仅需 Python 标准库 + curl，无需 pip install

---

## 🚀 快速开始

### 安装

```bash
# 克隆或下载后直接运行
python3 scripts/generate.py "我的路线" "lat1,lon1,起点,描述|lat2,lon2,终点,描述"
```

### 生成地图

```bash
# 基本用法
python3 scripts/generate.py "海口一日游" \
  "20.0352,110.3104,万绿园,起点-热带海滨公园|20.0315,110.2468,观海台,终点-百年钟楼"

# 自定义主题色
COLOR=#1a3a5c python3 scripts/generate.py "海边路线" "..."
```

### 查看结果

```bash
# macOS
open /tmp/citywalk_map.html

# Linux
xdg-open /tmp/citywalk_map.html

# 或启动本地服务（截图用）
python3 -m http.server 18767 --directory /tmp
# 访问 http://localhost:18767/citywalk_map.html
```

---

## 📖 使用说明

### 输入格式

```
lat,lon,名称,描述
```

- `lat,lon` - 必填，地点坐标（用逗号分隔）
- `名称` - 必填，地点显示名称
- `描述` - 可选，弹窗中的详细说明

多个地点用 `|` 分隔。

### 获取坐标

推荐使用 [Nominatim](https://nominatim.openstreetmap.org/ui/search.html) 搜索地点，点击结果中的 "details" 获取精确坐标。

### 常用主题色

| 国家/城市 | 颜色代码 | 说明 |
|---------|---------|------|
| 中国 | `#DE2910` | 中国红 |
| 法国 | `#0055A4` | 法国蓝 |
| 英国 | `#012169` | 英国蓝 |
| 日本 | `#BC002D` | 日本红 |
| 美国 | `#3C3B6E` | 美国蓝 |
| 默认 | `#e94560` | 活力粉 |

### 截图流程

```bash
# 1. 启动 HTTP server
python3 -m http.server 18767 --directory /tmp &

# 2. 用浏览器打开 http://localhost:18767/citywalk_map.html
# 3. 等待 20 秒让 OSM tiles 全部加载
# 4. 截图
# 5. 停掉 server
pkill -f "http.server 18767"
```

### 🖼️ 离线渲染（无需浏览器）

直接生成 PNG 图片，使用高德地图底图（国内可访问）：

```bash
# 需要 Pillow: pip install Pillow requests
python3 scripts/render.py \
  --accent "#228B22" \
  --zoom 13 \
  output.png \
  /tmp/citywalk_map.html
```

常用参数：
- `--accent #hex` 主题色
- `--zoom 13` 缩放级别（数字越大越清晰，但 tile 越多）
- `--help` 查看完整帮助

---

## 🗺️ 效果预览

```
┌────────────────────────────────────────────────────────────┐
│ 🚶 CITYWALK  │         路线标题                    │      │
│              ├────────────────────────────────────────────┤
│  9.4km      │                                            │
│  步行距离    │                                            │
│  5h23m      │           [OSM 地图]                        │
│  游览时长    │           显示完整路线                      │
│  7站        │           + 景点标记                        │
│  途经景点    │                                            │
│  1h53m      │                                            │
│  纯步行      ├────────────────────────────────────────────┤
│              │  途经景点              │  实用贴士         │
│              │  ① 起点               │  • 建议1          │
│              │  ② 途经点             │  • 建议2          │
│              │  ③ 终点               │  • 建议3          │
└────────────────────────────────────────────────────────────┘
```

---

## 🌍 巴黎示例（含天气查询）

```bash
python3 scripts/generate.py \
  --color "#0055A4" \
  --weather \
  "巴黎卢浮宫Citywalk" \
  "48.8606,2.3376,卢浮宫玻璃金字塔,世界最大博物馆之一|48.8641,2.3276,杜乐丽花园,法式皇家园林|48.8656,2.3211,协和广场,法国大革命时期著名广场|48.8637,2.3130,亚历山大三世桥,塞纳河上最华丽金桥|48.8738,2.2950,凯旋门,香榭丽舍尽头地标|48.8595,2.3122,荣军院,拿破仑陵墓所在|48.8584,2.2945,埃菲尔铁塔,巴黎最高点，日落最佳观景点"
```

---

## 🔧 技术栈

- **地图**: Leaflet.js + OpenStreetMap
- **路线**: OSRM Walking Routing (router.project-osrm.org)
- **地理编码**: Nominatim (OpenStreetMap)
- **生成**: Python 3 (无第三方依赖，用 curl 调用 OSRM)

---

## 📄 License

MIT License - 自由使用、修改、分发

---

## 🙏 致谢

- [OpenStreetMap](https://www.openstreetmap.org/) - 地图数据
- [Leaflet.js](https://leafletjs.com/) - 地图库
- [OSRM](https://project-osrm.org/) - 路线规划
- [Nominatim](https://nominatim.openstreetmap.org/) - 地理编码
