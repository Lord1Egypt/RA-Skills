# Airline Info to Website — 参考手册

与 [SKILL.md](../SKILL.md) 配合使用：主文件写门禁、进度与阶段总览；本文件写**输出目录规范**、**各 Phase 命令**、**验收与复盘**。

## 路径与依赖

- **技能根目录**：`SKILL.md` 所在目录（含 `scripts/`）
- 命令中的 `--output` 可为绝对路径或相对于**当前工作目录**的路径
- Python 依赖：`pip install requests beautifulsoup4`

## 输出约定

### 目录结构（每个机型）

```
机型名称/
├── 机型详情.md          # 机型基本信息、舱位配置
├── 完整内容整理.md       # 详细内容汇总（可选）
└── images/
    ├── 0-原始数据/       # 首次抓取原文、原图（只追加、不删除）
    ├── 1-座椅布局/       # 座位图、舱位平面图
    ├── 2-座椅图片/       # 座椅实物照片
    ├── 3-机上餐食/       # 餐食、菜单相关
    ├── 4-娱乐设备/       # IFE、端口、Wi-Fi 等
    └── 5-其他信息/       # 外观、logo、杂项等
```

### 多版本机型

若 seatmap 显示某机型有 **N** 个类型，则创建 `V.1` ~ `V.N` 子目录：

```
Airbus A380/
├── 机型详情.md
├── 版本索引.md
├── V.1/
│   ├── 机型详情.md
│   └── images/（六项子目录齐全）
├── V.2/
│   └── ...
└── ...
```

## 主流程命令

### Phase 1 — 确认范围

明确：航司名称、单机型或全航司、输出目录（如 `FlightData/`）

### Phase 2 — 获取机型列表

航司列表入口：`https://seatmaps.com/zh-CN/airlines/`

### Phase 3 — 抓取机型数据

```bash
# 抓取整个航司
python scripts/scrape_seatmaps.py --airline "航空公司中英文名称" --output FlightData/

# 抓取单个机型 URL
python scripts/scrape_seatmaps.py "https://seatmaps.com/zh-CN/..." --output FlightData/
```

### Phase 5 — 语义分类

```bash
node scripts/classify-images.js --base-dir "FlightData/航司目录"
```

### Phase 6 — 去重

```bash
node scripts/dedup-images.js --base-dir "FlightData/航司目录"
```

### Phase 8 — 文档生成

生成或更新各机型的 `机型详情.md`、航司级 `README.md`

## 完成检查

- [ ] 航司/机型 `机型详情.md` 是否存在且可读
- [ ] 每个 `images/` 下是否存在 `0-原始数据` ~ `5-其他信息` 六个子目录
- [ ] 多类型机型的子目录数量是否与 seatmap 类型数一致
- [ ] 无多余重复图片/正文
- [ ] 临时文件已清理

## 自我学习机制（任务后复盘）

每轮任务结束后简要复盘，必查项：

- 是否漏做多类型或错误合并
- 每个 `images/` 六项子目录是否齐全
- `0-原始数据` 是否被误删或覆盖
- 是否重复下载或可合并的重复资源
