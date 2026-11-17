# 260919 AT32F415 学习板 Demo 索引

本索引把考试资料拆成可迁移的小样例。资料包只有题目、评分表、原理图和 BOM，没有完成态 PCB；
因此不能把题目示意图或下表当成已经布通、DRC 通过的黄金答案。完整参数见
[source-manifest.json](source-manifest.json)；69 个实例见
[bom-instances.json](bom-instances.json)，题图连接转录见
[source-connectivity.json](source-connectivity.json)；全部 36 个技术点的机器可读样例字段见
[example-catalog.json](example-catalog.json)。现场初始布局参数见
[initial-placement.json](initial-placement.json)，代表性步骤的真实回读和未完成项见
[live-validation.json](live-validation.json)；关键网络如何反向修正布局见
[晶振/CAN 规划样例](critical-routing.md)，晶振第一批实际布局见
[crystal-placement-live.json](crystal-placement-live.json)，CAN 第一轮现场负例见
[can-placement-iteration-live.json](can-placement-iteration-live.json)，晶振实际 TOP/8mil/0via 有序铜路见
[crystal-route-live.json](crystal-route-live.json)；该铜路事实仍有效，但用户复核后不再接受为最终晶振区，
替代验收要求见 [晶振护环模块要求](crystal-guard-requirement.json)，schema-v2 历史拒绝及
schema-v3 共同逃线候选见
[晶振模块离线搜索](crystal-guard-plan.md)；[完整候选记录](crystal-protection-search-positive.json)
仅为 `offline-verified`，现场保护对象和两轮验收仍待完成。CAN 实际主路径与保护支路见
[can-route-live.json](can-route-live.json)，USB-C 四个重复数据焊盘与 U4 的实际 TOP/8mil/0via 铜路见
[usb-route-live.json](usb-route-live.json)，LDO 第二轮可执行参数见
[LDO 布局候选](ldo-layout-candidate.json)，保存重开后的局部铜见
[LDO 实际路线](ldo-route-live.json)。LED 板边、MCU 逐脚去耦和 LDO 刚体变换的候选生成见
[模块候选 Layout](layout-candidates.md)；其中 CAN/SD/USB-UART/LCD 第二批外围的保存重载结果见
[现场快照](layout-after-peripherals-live.json)，用户重开浏览器后的只读复核见
[重开证据](layout-after-browser-reopen-verification-live.json)。U3 重绑定超时后的参数化恢复见
[原理图恢复证据](schematic-u3-recovery-live.json)，恢复后的 sch↔PCB uniqueId 对账见
[U3 identity 对账](u3-identity-reconcile-live.json)；工程库封装复制的两次现场失败与跳过决定见
[现场摘要](live-validation.json) 的 `lcdFootprintComponentKeepout.projectCopyNegative`。

## 来源与已确认事实

| 来源 | 已确认事实 | 证据边界 |
|---|---|---|
| `物料清单.xlsx`，BOM 表第 3-29 行 | 27 行物料，数量展开为 69 个唯一位号；位号、封装、值、商品编号和功能区见 `bom-instances.json` | `offline-verified`；尚未与 EasyEDA 实例逐件回读 |
| `原理图.pdf` 第 1 页 | 一张 A4 原理图，15 个功能区；`source-connectivity.json` 转录 69 个器件、233 个端子和 13 处明确 NC | `source-only`；蜂鸣器 NC 在图面未标数字号，派生局部网名可改，真实 symbol pin、pad 与 pin→pad 映射必须现场读取 |
| `考试说明.pdf` 第 1-8 页 | 原理图、规则、机械、布局、布线、丝印和评分要求 | 已逐页提取并视觉抽查；不是完成态设计 |

## 15 个原理图功能区

每区先核对器件身份和逐引脚连接，再迁移布局。共同来源为 `原理图.pdf` 第 1 页；BOM 身份来自
`物料清单.xlsx`。

| 区 | 器件 | 必须单独核对的点 |
|---|---|---|
| TYPE-C 输入 | USB1、R1、R2 | A6/B6 与 A7/B7 的重复 D+/D- 脚；CC1/CC2 各 5.1kΩ；VBUS、GND、外壳 |
| RGB-LED | U1、LED1、R3、C1、C2 | LED1 的 `3.7V~5.3V` 显示属性；C1→U1.5、C2→LED1.1 的去耦归属 |
| LDO-3V3 | U2、C3-C6 | VIN 输入大/小电容；VOUT/TAB 同属 +3V3；输出大/小电容；顶层 GND 回流 |
| LCD | U3、Q1、R4-R6、C7 | U3.1/.2/.9 NC；背光三极管驱动；封装外形内的元件禁放区 |
| 功能按键 | SW1-SW3、R7-R9、C8 | SW1 与 SW2/SW3 的上下拉方向不同；NRST、PA0/WKUP、PA1 丝印 |
| USB 转串口 | U4、C9、C10 | CH340N V3 与 VCC 的供电/去耦；RTS NC；TXD/RXD 对 PA9/PA10 |
| 光敏电阻 | R10、R11、C11 | 分压与滤波；靠板边并远离 RGB LED |
| CAN | U5、D1、R12、C12、C13、CN1 | VREF NC；H/L 各经 R12 对应焊盘再到端子，120Ω 跨接 H/L；ESD 靠端子；针脚丝印 |
| 主控 | U6、C14-C16 | C14→U6.1、C15→U6.5、C16→U6.17；EP 接地；本例按 footprint anchor 执行 |
| BOOT | R13、R14 | BOOT0、PB2 各自下拉，不把相邻网络合并 |
| 无源蜂鸣器 | D2、Q2、R15-R17、C17、BUZZER1 | 驱动电阻、续流二极管、下拉和去耦整体跟随 |
| MICRO-SD | CARD1、C18、C19、R18-R23 | DAT/CMD 上拉、VDD 去耦、外壳地及固定方向 |
| 晶振 | X1、C20、C21 | OSC_IN/OSC_OUT；四脚晶振接地脚；靠 MCU 且不贴板边 |
| SWD | H1、C22 | 3V3/DIO/CLK/GND 的真实针脚顺序与接口丝印 |
| M3 螺丝孔 | SCREW1-SCREW4 | 四角精确坐标、顶层实例和锁定状态 |

## 技术点到样例

### 原理图与器件

| ID | 来源 | 技术点 | 样例/观测 |
|---|---|---|---|
| SCH-01 | 说明 p1；BOM | 按位号和商品编号展开 69 个实例，核对符号与封装 | [bom-instances.json](bom-instances.json) 是离线基线；`sch read/connectivity` 后逐件比较 |
| SCH-02 | 说明 p1 | 原要求为工程名 `客户编号-AT32F415 学习板`，图签“绘制”填真实姓名；Demo 用脱敏占位值替代 | `sch titleblock-get` 确认字段 key → `sch titleblock --data ...` → 回读；保留原要求与 Demo 替代的映射 |
| SCH-03 | 说明 p1；原理图 p1 | LED1 显示 `3.7V~5.3V` 工作电压 | 回读自定义属性与官方导图；待现场验证 |
| SCH-04 | 说明 p1 | 15 区布局、连线和功能文本以 PDF 为来源 | 先做连接数据再计算几何，不按旧 Z 排版重排题图 |
| SCH-05 | 说明 p1 | 网络标识、标签、NC 与连接关系保持一致 | [source-connectivity.json](source-connectivity.json) 与现场 `connectivity`、`check`、NC 明细分别比较 |
| SCH-06 | 说明 p1-2 | 原理图使用默认规则并查看 DRC 警告/错误 | 记录官方 `sch drc` 聚合与 `sch check` 明细，二者不互相替代 |
| SCH-07 | 原理图 p1 | USB-C 重复数据脚与两个 CC 下拉 | 逐引脚黄金表；不能只检查同名网 |
| SCH-08 | 原理图 p1 | CH340N 的 V3/VCC、RTS NC | 逐脚连接与两只 100nF 去耦 |
| SCH-09 | 原理图 p1 | AMS1117 的 pin 2 与 TAB/pin 4 同属输出 | [LDO 样例](ldo-placement.md) |
| SCH-10 | 原理图 p1 | 晶振接地脚、LCD/CAN 的 NC、SD 上拉、SWD 针脚顺序 | 每项单独回读；缺一个都不能用“DRC 数字正常”替代 |

### 设计规则与机械

规则参数现在可直接用 [PCB 配置命令](../../pcb-config.md) 设置，无需手改整份 JSON。
2026-09-20 后续已完成新入口的写入、typed 保存/重载、幂等重放和恢复；具体范围见该样例。
6mil 只改导线到导线，24/12mil 是过孔最小值；规则设置不自动修改已有铜。

| ID | 来源 | 技术点 | 样例/观测 |
|---|---|---|---|
| PCB-01 | 说明 p2、p5 | 两层板 | `pcb layers` 回读真实铜层数 |
| PCB-02 | 说明 p2、p7 | 导线间距 6mil；信号默认/最小 8mil | 已按 Web 3.2.203 的 `{name,config}` 读取形态写裸 `config`，整页刷新后回读为 6/8/8mil |
| PCB-03 | 说明 p2、p7 | `PWR` 默认 20mil、最小 8mil；`PWR_Class` 绑定全部电源网 | 已实建 `PWR_Class=[+5V,+3V3,GND]`，父子 netRules 均绑定 `PWR`，刷新后保持 |
| PCB-04 | 说明 p2、p7 | 过孔最小外径/孔径 24/12mil | 已写入完整规则副本，整页刷新后回读 24/12mil |
| PCB-05 | 说明 p2 | 90×50mm、线宽 0.254mm、R3 真圆角、左下显示原点、锁定 | [固定机械样例](fixed-mechanics.md)；保存及整页刷新回读已 `live-verified` |
| PCB-06 | 说明 p2 | 四孔、U6、CARD1 的固定题面坐标、角度和锁定 | 现场确认本批输入为 footprint anchor；六件刷新后坐标、角度和锁定保持 |
| PCB-07 | 说明 p3 | CN1 只固定 y=42mm、180°，x 是自由参数 | 现场候选 x=69mm；题定 y/角度保持，rendered bbox 顶边约超 1.17mil 的冲突单独保留 |
| PCB-08 | 说明 p3 | LCD 封装轮廓内禁止其他元件 | `unsupported / skipped`。当前 U3 已实证绑定 C2890616、OLED-SMD_ST7735S 和既有 3D model，sch↔PCB identity 已恢复为同一 `gge60`。系统源库不可写；[现场摘要](live-validation.json) 记录带/不带分类的 `lib_Footprint.copy` 都被宿主拒绝且没有返回目标 UUID；[板级实例负例](u3-instance-region-negative-live.json) 又证明普通 top-level `no-components` region 会让 owner U3 自身违规并已完整回滚。本 Demo 跳过 region 写入，仅用实测 U3 外形作布局避让代理；该考点保持未满足，不得 GUI 兜底或记为通过。 |

### 布局关系

| ID | 来源 | 技术点 | 样例/观测 |
|---|---|---|---|
| LAY-01 | 说明 p3-4 | 按键板边等距；USB、SWD、端子面向可插拔方向 | 读真实 bbox、开口方向和板框距离，不只看中心点 |
| LAY-02 | 说明 p4 | RGB 靠 TYPE-C；光敏远离 RGB | [模块候选 Layout](layout-candidates.md)：按真实板框中心线和 pad 所有权生成 3 个板边候选，选择理由与铜限制分开记录 |
| LAY-03 | 说明 p4、p7 | LDO 输入/输出电容靠对应引脚，大电容在前、小电容在后 | [LDO 样例](ldo-placement.md)；第二轮布局与15段TOP/20mil局部铜已 `live-verified`，整板主干不在本条范围内 |
| LAY-04 | 说明 p4、p7 | MCU 等电源脚逐脚去耦，电源先经过电容再入芯片 | [模块候选 Layout](layout-candidates.md)：C14/C15/C16 分别绑定 U6.1/.5/.17；同一所有权表达已迁移到 CAN、SD、CH340N 与 LCD，布局只证明所属 pad 距离，实际铜路径另验 |
| LAY-05 | 说明 p4；用户 2026-09-22 复核 | 晶振靠 MCU 但保留受控间距；X1、负载电容、信号铜、GND 护环、禁铺区和外围地孔作为整体；蜂鸣器/背光驱动整体放置 | [晶振现场布局](crystal-placement-live.json) 只保留为次序修正证据；[晶振护环模块要求](crystal-guard-requirement.json) 已把现状标为需要重做。LCD 背光链已按候选保存重载，蜂鸣器实际铜仍待验证 |
| LAY-06 | 说明 p4 | 全部器件顶层、无重叠、外形不出板 | `pcb list --include-bbox`、`layout-lint` 和 LCD 禁放区分别观察 |

### 布线与收尾

| ID | 来源 | 技术点 | 样例/观测 |
|---|---|---|---|
| RTE-01 | 说明 p5 | 焊盘末端出线、线宽不大于焊盘、窄焊盘缩颈、无直角/锐角 | 读轨迹端点、宽度与角度；DRC 不覆盖全部观感规则 |
| RTE-02 | 说明 p5、p8 | 电源主干按电流加粗，过孔按载流能力，流向清楚 | PWR 规则 + 实际每段/过孔回读 |
| RTE-03 | 说明 p4–5、p8；用户 2026-09-22 复核 | 晶振靠 MCU 但不贴压；OSC 信号尽可能短直；TOP GND 护环；TOP/BOTTOM `no-pours` 禁铺区；护环外侧 GND 过孔围栏 | [晶振护环模块要求](crystal-guard-requirement.json) 是新的完成口径。[旧铜路](crystal-route-live.json) 的 TOP/8mil/0via、连通和持久化事实仍成立，但因缺护环、双层禁铺区、外围地孔且路径还可缩短，已降为最终设计负例；整组对象必须参数化联合重算和回读 |
| RTE-04 | 说明 p5、p8 | USB_D+/D- 顶层、无过孔、类差分，不额外要求等长 | [实际 USB 铜](usb-route-live.json) 已逐一证明 `USB1.A6/B6→U4.1` 与 `USB1.A7/B7→U4.2` 为 TOP/8mil/0via，保存重载后 14 个实际 track 均锁定；两版 USB_D- 候选分别因封装内 Slot Region 距离 0mil、10.6mil 而被官方 DRC 拒绝，最终提前绕到其外侧。当前 typed 快照看不见封装内嵌 Slot Region，离线零 finding 不能替代官方 DRC |
| RTE-05 | 说明 p5、p8 | CANH/CANL 顶层、无过孔；各先经过 R12 对应焊盘再到端子，120Ω 仍跨接；ESD 靠端子 | [CAN 现场迭代](can-placement-iteration-live.json) 保留最短飞线相交的历史反例；[实际 CAN 铜](can-route-live.json) 已证明 `U5.7→R12.1→CN1.2`、`U5.6→R12.2→CN1.1` 及 D1 两支路均为 TOP/8mil/0via，保存重载后锁定保持；D1.3 最终 GND 回流仍待 GND 阶段 |
| RTE-06 | 说明 p5、p8 | PA9/10、PA11/12、PA13/14 顶层且不换层 | 分网回读 layer 与 via count |
| RTE-07 | 说明 p5 | U6 EP 添加散热过孔；其他焊盘不允许 via-in-pad | EP 与普通焊盘使用不同判据 |
| RTE-08 | 说明 p6、p8 | 普通信号同网过孔不超过 2；GND 扇孔与缝合孔 | 按网计数并检查地回流，不以总 via 数判断 |
| FIN-01 | 说明 p6、p8 | Arial、字符高度 ≥45mil、顶层、朝向不超过两个方向、接口提示丝印 | `silk-add/set --font-family Arial`，`silk list` 回读；接口离线测试通过、现场待验证 |
| FIN-02 | 说明 p6、p8 | 顶底层 GND 铺铜且保持完整 | `pour-list`、`pour-rebuild`、连通与 DRC |
| FIN-03 | 说明 p6、p8 | 添加真实泪滴后重建铺铜 | 当前为 `unsupported`；走线圆角化不是泪滴，禁止手工补做 |
| FIN-04 | 说明 p6、p8 | 100% 布通、无断头、PCB DRC 无错误，保存并重开核查 | 连通、`pcb check`、官方 DRC 分开记录；最后 `pcb save` + `doc reload` |

## Demo 实施顺序

1. 以 `bom-instances.json` 的 69 个唯一位号和 `source-connectivity.json` 的题图连接为源基线，
   回读真实 symbol pin、footprint pad 与 pin→pad 映射；保留差异，不猜测补齐。
2. 用当前 `project create --help` 核对后建立工程容器；若当前版本未暴露该能力，先补齐并验证 typed 接口。
3. 按 PDF 的功能区和连线表达构建原理图，回读属性、连接、NC、`check` 与官方 DRC。
4. 转入正确绑定的 PCB，确认 69 件和焊盘网；设置两层及真实规则/网络类，让间距与线宽参与后续布局。
5. 建 90×50mm 板框和左下显示原点，放置并锁定孔、U6、CARD1；CN1 保留 x 自由。
6. LCD 封装禁放区的当前工程组合能力已标 `unsupported`，本 Demo 跳过实际 region 写入并保留
   未满足项；用 U3 实测 footprint bbox 作为候选计算的避让代理，安排屏幕与板边器件。再用
   `pcb layout-plan` 按模块生成完整候选，依据板框中心线、开口/关系、pad 距离和空隙选择，
   不能在现场逐件试摆，也不能把 bbox 代理记为封装 region 已完成。
7. 围绕明确所属引脚生成 MCU 去耦、晶振、LDO、CAN、蜂鸣器和 SD 模块候选，同时预留
   电源主干和顶层回流；同网多个供电脚必须在输入中逐脚绑定。LDO/DCDC 的输入/输出电容、
   局部 GND 回流及必要 EP/地过孔可作为参数化整体先完成并回读，移动模块时一起重算。
   晶振候选必须使用 `pcb dump --include-copper` 和 schemaVersion 3，把 X1/C20/C21、两条
   OSC 铜、TOP GND 护环与显式 GND 导线、TOP/BOTTOM no-pours regions、护环外侧 GND
   过孔围栏作为一个 `crystal-guard` 模块，不得只优化两条信号线。模块内部铜随局部几何
   变换；U6 固定，U6.2/U6.3 到模块入口的外部引线按每个候选重新求解，并与 U6 其它需连接
   焊盘的逃线需求同时占用通道。U6 EP 已有地孔用 `existingViasOnly` 按 PID、网络和焊盘归属
   复用，不能为通过检查虚构新孔或 GND 路径。
8. 全部 Layout 要求落实后用 typed `pcb stage-snapshot` 或等价 export 生成整板集成图，并连续
   自检两轮：第 1 轮检查空间、模块关系和视觉异常；无修正后第 2 轮执行 `save → reload → fresh
   dump → fresh render`。任一轮发现并修复就把连续计数清零，重新从第 1 轮开始。若属性文字妨碍
   观察，只能 typed 保存旧视图状态、临时隐藏、恢复并回读；当前无可恢复接口就标 `unsupported`，
   保持属性可见，禁止 GUI。两轮均无待修明显问题且无修正后向用户展示第 2 轮整板图、坐标/角度、机械与布局检查、
   预留通道和未完成项。用户提出调整就继续本步骤；用户自行调整并说“OK”时重新回读、固化现场
   参数并重新跑两轮。只有用户明确确认最新回读版本后才进入下一步。
9. 以用户确认后的 dump 为布线基线，先晶振和受限顶层网络，再连接跨模块电源主干及普通信号。
   组间次序按通道冲突调整，每组写后回读。
10. 用 typed 接口完成丝印、双面 GND、缝合孔；真实泪滴能力未实现时保持未完成。泪滴后重铺铜，复查连接、几何、DRC，保存重开。

固定考试板遵循“板框/固定件 → 机械空间 → 关键路径 → 外围”。另建的可调尺寸教学变体遵循
“功能模块/接口 → 关键路径 → 估算板框 → 合法化”，并明确标为自建变体，不能回写考试基准。
两种情况都在精细布局前确认制造规则。去耦 150mil、晶振守护区 200mil、装配间隙 12mil
都不是本题的数值要求；若作为搜索初值或工程建议使用，须记录来源和可调整性。
