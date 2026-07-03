# 事前快速摸底(可选,不是门禁)

> 动手布局前**花几分钟读懂设计**能少返工——但这是**轻量摸底,不是"不出计划不落坐标"的硬门禁**。
> 布局智能交给 AI 用数据 + 截图自调(见 [`auto-layout-sop.md`](./auto-layout-sop.md))。
> 大板 / 陌生板多看几眼,小板 / 熟板直接上。

## 读什么(只读,零 mutation)
| 想知道 | 读哪个 | 用来 |
|---|---|---|
| 有哪些件、pin、bbox | `sch list`(designator/name/pins) | 认锚点(大 IC/连接器/RF/晶振)、估面积 |
| 现有页 / 纸张 | `sch pages` / `sch titleblock-get` | 幅面基线(默认 A4 1170×825)→ 够不够,不够多页 |
| 能不能下单 | `sch bom` + `scripts/bom-enrich.py` | 补 LCSC C 号、找孤儿件 |
| 选型 / 补料 | `lib search` / `parts-select.py` / 查 `standard-parts.json` | 标准件优先;新选型**写回 standard-parts.json** |

## 摸清这几样(够用就行,别写成大计划)
- **电源树**:每条轨 源→稳压器→负载;每个 VCC 焊盘配 100nF(漏了是真问题)。
- **功能分组 + 信号流**:哪些件一组(电源/MCU/RF/模拟…),大致左→右=输入→处理→输出;四域(RF/模拟/数字/电源)别交织。
- **锚点**:大件(IC/连接器/RF/晶振)先定位,辅助件后挂;最大簇先占板边/角。
- **幅面**:`Σ主器件bbox + 辅助×~80×80 + 余量`,>~80 件考虑多页(电源 / MCU+数字 / RF+4G)。

## 几个真问题(碰到先解决)
- 件无 LCSC C 号 / 孤儿封装 → 不可下单,换标准件;
- IC 的 VCC 焊盘漏去耦 → 补 100nF;
- 差分 / 等长 / 隔离网没成对成组命名 → PCB 认不出(net 名 + 线宽 + designator 是原理图传给 PCB 的唯一信道,该标的标好);
- 极性件 / 钽电容没标方向 / 降额。

> 详细分区 / 间距 / 去耦 / 命名约定查 [`schematic-layout-conventions.md`](./schematic-layout-conventions.md);
> 选型 [`part-selection.md`](./part-selection.md);PCB 侧 [`pcb-layout-conventions.md`](./pcb-layout-conventions.md)。
