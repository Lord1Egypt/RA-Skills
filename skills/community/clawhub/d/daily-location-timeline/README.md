# 时光梳理 · 每日行程梳理（daily-location-timeline）

把几年甚至十几年的支付账单、机票/火车票、导航/打车 GPS、OTA 订单、**照片 EXIF GPS**，
还原成一份**「每一年、每一天我大概在哪个城市」**的可信逐日地理轨迹。

> 适用于个人时间线归档、报销/居住佐证、「我到底去过哪些地方」的记忆还原。
> 同时适配**中国大陆用户**（微信/支付宝/12306）与**海外用户**（银行账单/Google Timeline/Trainline）。

## 为什么需要它

账单里的「消费地」≠「你人在哪」：

- 商户**注册地/总部**混进账单（国内：订票平台注册在天津而你从没去过；海外：Uber 显示 San Francisco 而人在 London）
- **菜系名**被当城市（「淄博烧烤(深圳店)」→ 淄博）
- 账单滞后的时段（当年账单未出）完全空白

本 skill 用一套**证据分级 + 时间感知判定**的方法论，把这些噪声还原成可信轨迹。

## 核心特性

- **8 阶段流水线**：账单合并 → 城市归一 → 消费基线 → 出行腿 → 实地证据 → **照片 GPS** → 时间感知整合 → 校验迭代
- **时间感知引擎（v2.0）**：每日有效时段（07:00–24:00，排除睡眠）内停留最久的城市为主城市，在途不计；替代早期「到达优先」判定
- **照片 EXIF GPS 判定**：账单缺失时段的主力证据，附三道保险（距离审计/单点飞地检测/时区口径）
- **安全闸体系**：chain-gap 双闸（链不断 + MAX_GAP 上限）、transit_leg 防陈旧到达污染、中转城市约束
- **国内海外双适配**：方法论全球通用，数据源映射表 + 城市命名规范按地区取用
- **全程可复现**：个人常量集中在一个配置块，换人只改配置；先备份再改，非破坏性迭代

## 目录结构

```
daily-location-timeline/
├── SKILL.md                     # 给执行智能体的精简行动指南（入口）
├── manifest.yaml                # ClawHub 发布元数据
├── README.md                    # 本文件
├── LICENSE                      # MIT-0
├── references/
│   ├── sop.md                   # 完整 SOP（8 阶段 + 地区适配 + 附录 A–D）
│   ├── travel_legs_schema.md    # travel_legs.json 字段定义与国内外示例
│   └── photo_gps_method.md      # 照片 GPS 判定方法 + 实战教训
└── scripts/
    ├── rebuild_final.py         # 整合+纠错脚本（时间感知引擎，核心资产）
    ├── photo_gps_judge.py       # 照片 GPS 逐日判定（反查+时间感知+三道保险）
    ├── travel_legs.json         # 出行腿示例模板（国内跨夜经停/口述 + 海外红眼航段）
    └── city_coords.json         # 城市坐标库模板（国内+海外，按到访地扩充）
```

## 快速开始

### 1. 准备环境

```bash
pip install openpyxl        # xlsx 读写
# exiftool 单独安装（照片 GPS 提取用）：https://exiftool.org
```

### 2. 导出你的数据

- 支付账单（微信/支付宝/云闪付，或银行月结单 PDF→CSV）
- 出行订单（12306/航旅，或 Trainline/航司 App）
- 照片视频目录（含 GPS 的最好）

### 3. 填写个人常量

打开 `scripts/rebuild_final.py` 顶部的配置块，填写（完整说明见 `references/sop.md` 附录 A）：

```python
MAX_GAP = 14                        # 行程连续填充阈值(天)
HOME_CITIES = {'Region/City'}       # 老家/长居地
TRANSIT_CITIES = set()              # 中转站(真实停留≤2天)
CORRECTIONS = {}                    # 用户核实校正
```

### 4. 结构化出行腿

把机票/火车票录成 `travel_legs.json`（格式见 `references/travel_legs_schema.md`，含跨夜/经停/口述/海外跨时区写法）。

### 5. 照片 GPS 判定（可选但强烈建议）

```bash
exiftool -json -DateTimeOriginal -GPSLatitude -GPSLongitude -r /照片目录/ > photo_gps_raw.json
python3 scripts/photo_gps_judge.py photo_gps_raw.json -o photo_daily_judge.json
```

复核所有 ⚠️ 警告日（距离超限/单点飞地），按需扩充 `city_coords.json`。

### 6. 整合输出

把脚本与输入文件放进同一干净目录，运行 `rebuild_final.py`，产出：

- `每日所在城市_最终整合版.xlsx`（每日城市/停留段/城市汇总/飞机明细/火车明细）
- `每日所在城市_逐日明细.csv`

### 7. 校验迭代

按 `references/sop.md` 附录 D 清单自查 → 用户逐日核对 → 补 `CORRECTIONS`/补腿/扩坐标库 → 重跑（先备份）。

## 两类典型用户场景

**中国大陆用户**：微信+支付宝账单导出 → `省/市` 短格式 → 商户注册地清洗（同程→天津式误判）→ 12306/航旅出行腿 → 高德/滴滴 GPS → 照片 EXIF GPS 补账单空白期。

**海外用户**：银行/信用卡月结单 PDF→CSV → `国家/城市` 格式 → 商户总部清洗（Uber→SF 式误判）→ Trainline/航司出行腿（当地时间口径）→ Google Maps Timeline/Uber 行程 → 照片 EXIF GPS；留意跨时区日期漂移与币种突变（出境信号）。

## 实战规模

本方法论由一次真实的「2013–2026 跨十三年」梳理实践沉淀而来：约 **4800 个日期、70+ 城市**，
含跨境（港澳）、海外（东南亚）、青藏铁路夜车、大环线自驾、疫情封城滞留等复杂场景。

## License

MIT-0 —— 可自由使用、修改、分发，无需署名。
