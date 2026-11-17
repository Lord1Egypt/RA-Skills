---
name: daily-location-timeline
version: 2.0.0
description: "This skill should be used when a user wants to reconstruct their day-by-day city / location timeline across multiple years from payment and travel records (bills from WeChat Pay / Alipay / UnionPay / bank & credit-card statements, flight and train tickets, navigation / ride-hailing GPS, OTA bookings, Google Maps Timeline, and photo EXIF GPS). It turns noisy consumption locations into a verified per-day geography, correcting merchant-HQ and product-origin mislabels with travel legs, on-site evidence, photo GPS, and safety gates. Works for both mainland-China users (省/市 naming, WeChat/Alipay sources) and international users (country/city naming, bank statements, Google Timeline). Trigger phrases: 梳理我的行程, 还原每日所在城市, 跨多年每日所在地, 微信支付宝账单 还原 我在哪, 行程地点记录, 把多年账单整理成我在哪, 照片GPS还原轨迹, daily location timeline, reconstruct where I was, location history from bank statements."
agent_created: true
license: MIT-0
tags: [行程梳理, 所在地还原, 时间线归档, GPS轨迹, 照片定位, travel, timeline, location-history, productivity]
---

# 跨多年每日所在地点梳理（Daily Location Timeline）

把几年甚至十几年的支付账单、机票/火车票、导航/打车 GPS、OTA 订单、**照片 EXIF GPS**，还原成一份
**「每一年、每一天我大概在哪个城市」**的可信逐日地理轨迹。适用于个人时间线归档、报销/居住佐证、
「我到底去过哪些地方」的记忆还原。

> 完整操作规范见 `references/sop.md`；出行腿字段定义见 `references/travel_legs_schema.md`；
> 照片GPS方法与实战教训见 `references/photo_gps_method.md`。本文件是给执行智能体的精简行动指南，
> 遇到细节分歧以 `references/sop.md` 为准。

## 何时使用

- 用户有多年支付账单（微信/支付宝/云闪付，或银行/信用卡月结单），想还原逐日所在地。
- 账单缺失或滞后的时段（如今年账单未出），但有大量带 GPS 的照片/视频。
- 用户要证明某段时间在某地（报销/税务/居住证明/签证记录/个人时间线归档）。
- 用户想把自己的「消费地」清单整理成「真实所在地」清单。

## 核心认知（贯穿全程）

1. **支付地点 ≠ 你本人在哪。** 商户注册地（订票平台总部/分公司）、商品产地、连锁门店分支地、
   线上商户都会把错误城市塞进账单——国内典型如「订票平台注册在天津」，海外典型如
   「Uber 账单显示 San Francisco 总部而人在 London」。所有「城市」都必须经证据校验。
2. **GPS 类证据比消费更硬。** 导航/打车轨迹、App 签到、**照片 EXIF GPS** 直接锚定物理位置，
   作为 L0 级证据优先采信。
3. **判定要「时间感知」。** 一天可能跨多个城市（早晨在 A 出发、傍晚到 B），
   有效的判定是：**每日有效时段（07:00–24:00，排除睡眠段）内停留最久的城市为主城市，
   在途时间不计入任何城市**。这是 v2.0 相对早期「到达优先」判定的关键改进。

## 地区适配（先确认用户所在地区，其余流程完全一致）

核心方法论全球通用，仅「数据源」与「城市命名」按地区取用：

| 环节 | 中国大陆用户 | 海外用户 |
|------|------------|---------|
| 支付账单 | 微信/支付宝/云闪付导出 Excel | 银行/信用卡月结单 PDF→CSV（Chase/Amex/Wise/Revolut 等） |
| 出行票务 | 12306、航旅纵横/航司 App | 航司 App、Trainline/Amtrak/Eurostar/Rail Europe |
| 导航/打车 GPS | 高德/百度、滴滴/曹操、哈啰 | **Google Maps Timeline**、Uber/Lyft/Bolt/Grab 行程记录 |
| 实地订单 | 美团/携程/华住 | Booking/Agoda/Airbnb/酒店会员体系 |
| 照片 EXIF GPS | 相册照片（同一全球标准） | 相同（Photos/iCloud/Google Photos 导出均可） |
| 城市命名 | `省/市` 短格式（如 `新疆/阜康`） | `国家/城市`（如 `Thailand/Bangkok`），同两级结构 |
| 高频误判源 | 商户注册地、菜系名、商品产地 | 商户总部所在地、清关地、免税店注册地、**跨时区日期漂移** |
| 币种线索 | — | 账单币种突变（USD→THB）可辅助定位出境日 |

> 表达习惯跟随用户：国内用户用中文交流与中文表头；海外用户可用英文/当地语言。
> 交付表格列名建议与用户日常语言一致（脚本默认中文列名，可在配置中改）。

## 数据源分级（按可靠性 × 获取难易度）

- **一级（必须）**：支付账单（国内：微信/支付宝/云闪付；海外：银行/信用卡账单）；
  票务（12306/航旅，或 Trainline/航司）。低难度、主干证据。
- **二级（强烈建议）**：带 GPS 的记录——导航/打车/骑行（高德/滴滴，或 Google Timeline/Uber）、
  **照片 EXIF GPS**。纠偏最强，账单缺失时的主力。
- **三级（按需）**：OTA/酒店/门票等「线上买线下用」订单（美团/携程，或 Booking/Agoda）。
- **记忆（随时）**：相册、日记、工作地变迁，逐日核对时调用；模糊日期直接问用户。

> 原则：先一级打底 → 二级纠偏 → 三级填空。不必一次集齐；账单缺什么就用照片 GPS 补什么。

## 处理流水线（8 阶段）

1. **账单导出与合并**：各平台导出表格，对齐字段，标注「消费性质 / 判定层级」，去重，
   输出合并明细表。海外用户：PDF 账单先转 CSV，字段映射到「时间/对方/商品(描述)/金额/城市」。
2. **字段标准化与城市归一化**：统一成 `region/city` 两级短格式。国内「浙江省/杭州市」→`浙江/杭州`；
   海外自由文本城市（如账单 merchant 字段）→ `国家/城市`。同一城市因写法不同被拆行是大坑。
3. **消费地逐日梳理（梳理版）**：按日分组，写「当日全部城市」与主城市。
   **铁律：城市只从「商品/描述」字段提取，绝不从「交易对方/merchant」提取**（防注册地误判）。
4. **出行腿结构化（travel_legs.json）**：把票务变成机器可读的「出行腿」——最硬的位置证据。
   结构见 `references/travel_legs_schema.md`。要点：
   - 跨夜腿：`arr_date` 写到达日，中间天标为到达城市（在途）；
   - 经停站用 `stops` 记入到达日；同日多段靠 `dep_min` 排序；
   - **时刻用当地时间记录**（海外跨时区航班：出发写起飞地时间、到达写落地地时间的分钟数）；
   - 缺订单的行程（朋友代订/现金票/口述）标 `status: 用户口述` 补腿。
5. **实地证据提取**：筛选「酒店/民宿/门票/景区」类订单，升级为与票务同权重硬证据。
   排除：酒店用品（=网购）、外卖/买菜、菜系名误判（「淄博烧烤」「Sichuan Cuisine」是风味不是城市）、
   公司注册名（含 Ltd/Inc/股份 等字样）。
6. **照片 EXIF GPS 判定**（账单缺失时段的主力，见 `references/photo_gps_method.md`）：
   `exiftool` 批量提取 → `photo_gps_judge.py` 反向地理编码 + 时间感知聚合。
   三道保险：**距离审计**（匹配>0.3°≈33km 需复核，防城市库缺目的地——实战教训：缺「阜康」，
   天池两天被错配到 40km 外省会）、**单点飞地检测**（当天仅 1-2 点且远离邻日 → 不可直接采信）、
   **时区口径**（EXIF 时间为拍摄设备本地时间，与票务口径一致）。
7. **每日城市推算与整合（最终整合版）**：跑 `scripts/rebuild_final.py`，时间感知合成每天主城市：
   **物理轨迹（时间感知）> 实地(onsite) > 消费层 > 兜底**。安全机制：
   - chain-gap 双闸：链不断（前腿到达==后腿出发）且 `1<=gap<=MAX_GAP`；超长空档回落消费层；
   - transit_leg 跟踪：只接受当前在途腿的到达事件，过滤陈旧到达污染；
   - 中转城市约束、特殊滞留时期（封城等）、用户核实 `CORRECTIONS`——均为可选配置，默认关闭。
8. **校验与纠错迭代**：自查清单（首末城市符合记忆、邻日连续、中转段≤2天、⚠️备注冲突日）；
   导出→用户逐日核对→改配置/补腿/加 CORRECTIONS→重跑（先备份）。模糊日期列清单直接问用户，
   口述结果标注 `[用户确认]` 写入备注。

## 打包脚本（核心资产）

- `scripts/rebuild_final.py`：整合+纠错脚本（时间感知引擎）。读「梳理版消费层」+「合并明细」+
  `travel_legs.json`，产出 6 表整合版 xlsx 与逐日明细 csv。**顶部是个人常量配置块**
  （文件名 / HOME_CITIES / MAX_GAP / TRANSIT_CITIES / LOCKDOWN / MERCHANT_CITY_BLACKLIST /
  CORRECTIONS / CITY_HINT_RULES / CITY_ALIAS），换人只改这一块。
- `scripts/photo_gps_judge.py`：照片 GPS 逐日判定（反查+时间感知+距离审计+飞地检测）。
  附 `scripts/city_coords.json` 坐标库模板（国内+海外示例，按到访地扩充）。
- `scripts/travel_legs.json`：出行腿示例模板（含国内跨夜经停/口述/自驾 + 海外航段/铁路）。

> **运行方式**：脚本读取「与脚本同目录」的输入文件。把 scripts/ 下脚本与你的输入 xlsx/json
> 放进同一个干净工作目录运行（依赖 `openpyxl`：`pip install openpyxl`；exiftool 需单独安装）。

## 关键坑（高频，详见 references/sop.md 附录 C）

- 商户注册地/总部误当所在地 → 城市只从「商品/描述」提（国内同程→天津；海外 Uber→SF）。
- 菜系/风味名误判城市（「淄博烧烤」「Sichuan Cuisine」）→ 排除菜系词。
- 大环线/长途缺腿 → 中间天被标回老家 → 补中间腿 + 调大 MAX_GAP（但绝不无限顺延）。
- 跨夜出行腿中间天漏标 → 在途天标为到达城市。
- **城市反查库缺目的地** → GPS 被就近匹配到错误城市（实战：天池→40km 外省会）→ 距离审计 + 扩充坐标库。
- **单点飞地** → 孤立 GPS 点（他人照片/水印定位）→ 飞地检测，不直接采信。
- **海外跨时区** → 红眼航班日期漂移、EXIF 时区口径 → 出行腿用当地时间、按设备时区归日。

## 参考资料

- `references/sop.md`：完整 SOP（准备、8 阶段、地区适配、交付物、附录 A–D）。
- `references/travel_legs_schema.md`：`travel_legs.json` 字段定义、国内外写法示例、常见错误。
- `references/photo_gps_method.md`：照片 GPS 判定方法、exiftool 用法、实战教训（阜康案例）。
- `scripts/`：三个可复用脚本 + 坐标库/出行腿模板。
