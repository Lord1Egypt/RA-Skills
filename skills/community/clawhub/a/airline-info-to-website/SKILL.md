---
name: airline-info-to-website
description: 抓取航空公司机型座位图数据，自动分类整理图片，生成网站展示航司信息。支持 seatmaps.com 数据源，自动处理机型详情、舱位配置、座椅图片和机上设施信息。
---

# Airline Info to Website

系统化收集航空公司机型资料，自动整理归类，为网站展示提供标准化数据结构。

## 技能包结构

| 文件 / 目录 | 说明 |
|-------------|------|
| `SKILL.md` | 主入口：权限配置、阶段总览、触发场景 |
| `references/reference.md` | 路径与依赖、输出目录规范、各 Phase 命令、完成检查 |
| `references/examples.md` | 典型用法与命令示例 |
| `references/template.md` | 机型详情文档模板 |
| `scripts/` | 可执行脚本（抓取、分类、去重） |

## 路径约定

- **技能根目录**：本文件所在目录（含 `scripts/`）
- Python 依赖：`pip install requests beautifulsoup4`
- 输出目录：默认为 `FlightData/`，可自定义

## 权限配置

本 skill 默认全程按「危险 / 免逐条确认」执行。启动方式：

```bash
claude --dangerously-skip-permissions --permission-mode bypassPermissions
```

或配置 `~/.claude/settings.json`：

```json
{
  "permissions": {
    "allow": [
      "Bash",
      "Read(~/Desktop/**)",
      "Read(~/skills/**)",
      "Edit",
      "Write",
      "MultiEdit"
    ]
  }
}
```

## 执行阶段

| 阶段 | 名称 | 命令 |
|------|------|------|
| 1 | 确认范围 | 明确航司名称、机型范围、输出目录 |
| 2 | 获取机型列表 | 访问 seatmaps.com 航司页面 |
| 3 | 抓取机型数据 | `python scripts/scrape_seatmaps.py --airline "航司名" --output FlightData/` |
| 4 | 原始归档 | 确认数据已保存到 `images/0-原始数据/` |
| 5 | 语义分类 | `node scripts/classify-images.js --base-dir "FlightData/航司目录"` |
| 6 | 去重 | `node scripts/dedup-images.js --base-dir "FlightData/航司目录"` |
| 7 | 多版本处理 | 检查机型是否有多个类型版本 |
| 8 | 文档生成 | 生成 `机型详情.md`、`README.md` |
| 9 | 清理 | 删除临时文件 |

## 何时使用

以下场景优先按本 skill 执行：

- 抓取某航司的全部或部分机型数据
- 获取机型的 seatmap、舱位、座椅图片
- 建立航司机型数据库用于网站展示
- 整理飞机图片并分类归档

## 快速开始

```bash
# 1. 抓取数据
python scripts/scrape_seatmaps.py --airline "新加坡航空 Singapore Airlines SQ" --output FlightData/

# 2. 语义分类
node scripts/classify-images.js --base-dir "FlightData/新加坡航空 Singapore Airlines SQ"

# 3. 去重
node scripts/dedup-images.js --base-dir "FlightData/新加坡航空 Singapore Airlines SQ"
```

详细说明见 [references/reference.md](references/reference.md)，示例见 [references/examples.md](references/examples.md)。
