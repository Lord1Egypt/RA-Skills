# airline-info-to-website

系统化收集航空公司机型资料，自动整理归类，为网站展示提供标准化数据结构。

## 功能

- **数据抓取**：从 seatmaps.com 抓取航司机型、座位图、座椅图片
- **自动分类**：按语义将图片分类到 5 个标准目录
- **去重处理**：基于 MD5 哈希自动删除重复图片
- **文档生成**：自动生成机型详情 Markdown 文档

## 快速开始

```bash
# 1. 安装依赖
pip install requests beautifulsoup4

# 2. 抓取数据
python scripts/scrape_seatmaps.py --airline "新加坡航空 Singapore Airlines SQ" --output FlightData/

# 3. 语义分类
node scripts/classify-images.js --base-dir "FlightData/新加坡航空 Singapore Airlines SQ"

# 4. 去重
node scripts/dedup-images.js --base-dir "FlightData/新加坡航空 Singapore Airlines SQ"
```

## Skill 结构

```
airline-info-to-website/
├── SKILL.md                    # 主入口文档
├── README.md                   # 项目说明
├── scripts/                    # 核心脚本
│   ├── scrape_seatmaps.py     # 数据抓取
│   ├── classify-images.js     # 图片分类
│   ├── dedup-images.js        # 去重处理
│   └── README.md              # 脚本说明
└── references/                # 参考文档
    ├── reference.md           # 详细参考手册
    ├── examples.md            # 使用示例
    └── template.md            # 机型详情模板
```

## 输出目录结构

```
FlightData/
└── 航司名称/
    └── 机型名称/
        ├── 机型详情.md
        ├── 完整内容整理.md
        └── images/
            ├── 0-原始数据/      # 首次抓取原文原图
            ├── 1-座椅布局/      # 座位图、舱位平面图
            ├── 2-座椅图片/      # 座椅实物照片
            ├── 3-机上餐食/      # 餐食、菜单
            ├── 4-娱乐设备/      # IFE、Wi-Fi 等
            └── 5-其他信息/      # 外观、logo 等
```

## 文档

- [SKILL.md](SKILL.md) - 主入口，权限配置，阶段总览
- [references/reference.md](references/reference.md) - 详细参考手册
- [references/examples.md](references/examples.md) - 使用示例
- [scripts/README.md](scripts/README.md) - 脚本说明

## 支持航司

常见航司名称映射：
- 新加坡航空 / Singapore Airlines / SQ
- 阿联酋航空 / Emirates / EK
- 国泰航空 / Cathay Pacific / CX
- 日本航空 / Japan Airlines / JL

## License

MIT
