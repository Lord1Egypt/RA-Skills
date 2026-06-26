# Citywalk Map Skill | 城市步行路线图生成器

> 无需API！零成本生成真实 OSM 地图 + OSRM 步行路线的精美 Citywalk 路线图，一行命令搞定自定义主题色、全屏布局、详细步行数据

---

## 为什么选择我们？| Why Us?

| 对比项 | 其他方案（API/MCP）| 我们的方案 |
|--------|-------------------|-----------|
| 成本 | 需申请 API Key、付费、限流 | **零成本**，curl + OSM 公开接口 |
| 部署 | 需服务器中转、签权 | **直接本地生成**，文件输出 |
| 地图 | 商业地图 API（有水印/限制）| **OSM 真实地图**，无水印 |
| 截图 | 需额外截图服务 | **OpenClaw browser** 一键截图 |
| 定制 | API 返回固定样式 | **HTML/CSS 完全可控** |
| 上手 | 写代码调用 API | **一行命令就搞定** |

---

## 功能 | Features

- 🌏 **零成本**：无 API Key，无付费，无限流
- 🚶 **真实路线**：OSRM 步行导航，不穿墙不穿海
- 🖥️ **全屏适配**：横向全屏布局，电脑手机都完美
- 🎨 **主题色**：一行命令切换任意主题色（国家/城市/品牌色）
- 📊 **详细数据**：总距离、步行时长、游览时长、站点列表
- ⚡ **零依赖**：Python 内置库 + curl，无需 pip install

---

## 使用 | Usage

```bash
python3 skills/citywalk-map/scripts/generate.py "路线标题" "lat1,lon1,name1,desc1|lat2,lon2,name2,desc2|..."
```

### 示例 | Examples

**巴黎 | Paris**
```bash
COLOR=#0055A4 python3 skills/citywalk-map/scripts/generate.py \
  "巴黎卢浮宫Citywalk" \
  "48.8606,2.3376,卢浮宫|48.8641,2.3276,杜乐丽花园|48.8656,2.3211,协和广场|48.8637,2.3130,亚历山大三世桥|48.8738,2.2950,凯旋门|48.8595,2.3122,荣军院|48.8584,2.2945,埃菲尔铁塔"
```

**海口 | Haikou**
```bash
python3 skills/citywalk-map/scripts/generate.py \
  "海口万绿园 → 观海台" \
  "20.0352,110.3104,万绿园|20.0315,110.2468,观海台"
```

### 主题色 | Theme Colors

| 国家 | 颜色 |
|------|-------|
| 🇨🇳 中国 | `#DE2910` |
| 🇫🇷 法国 | `#0055A4` |
| 🇬🇧 英国 | `#012169` |
| 🇯🇵 日本 | `#BC002D` |
| 🇺🇸 美国 | `#3C3B6E` |
| 默认 | `#e94560` |

### 截图流程 | Screenshot

```bash
python3 -m http.server 18767 --directory /tmp &
# 等待 20 秒 → browser screenshot → 飞书发送
pkill -f "http.server 18767"
```

---

## 坐标获取 | Coordinates

打开 [Nominatim](https://nominatim.openstreetmap.org/ui/search.html?q=地点名)，点击 **"detail"** 获取精确坐标。

---

## 输出 | Output

- 横向全屏 HTML 地图卡片
- OSM 真实地图底图 + OSRM 步行路线
- 主题色虚线路径 + 景点标记
- 统计区：总距离、步行时长、游览时长、站点数
- 途经景点列表 + 实用贴士

---

## 文件 | Files

```
skills/citywalk-map/
├── SKILL.md           # 本文档
├── scripts/generate.py # 地图生成（输出 /tmp/citywalk_map.html）
├── README.md           # 中文说明
├── README.en.md       # English
├── package.json
└── LICENSE            # MIT
```

## 开源许可 | License

MIT License
