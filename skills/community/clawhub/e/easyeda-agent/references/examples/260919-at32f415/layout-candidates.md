# 260919 模块候选 Layout 样例

本例把“AI 理解关系”和“算法计算坐标”分开。来源为 `考试说明.pdf` 第 3–4、7 页、
`原理图.pdf` 第 1 页和 BOM；题目没有完成态 PCB，所以下面的坐标来自 `ceshi` 当前 69 件
实板快照与有限枚举，不是题目标准答案。

## 开始状态与共同参数

- PCB 文档：`2e719e9419653c72`，69 个顶层器件，90×50mm R3 圆角板框。
- 坐标单位：mil；写入坐标是 footprint anchor，bbox 与 pad 坐标只作测量。
- 输入快照：[current-board-live.json](current-board-live.json)，板框为 184 点
  `polygon-centerline`；写入前现场重抓的原始文件 SHA256 为
  `8c90926484f3d408a406c7bc4c2713d3ad8c358106873865afbeec3873cbed09`，并写入每个
  manifest 和 apply 描述。除 `capturedAt` 外，它与上一份基线完全一致。
- 第二批四组外围以第一批保存后的
  [layout-after-led-mcu-live.json](layout-after-led-mcu-live.json) 为 board 输入，SHA256 为
  `cb388635cadbb6c689e7fb3a8555375a307a92d90b2a1df726855d340f21a65f`；第二批保存重载后的
  [layout-after-peripherals-live.json](layout-after-peripherals-live.json) SHA256 为
  `4731eb7ea2cbade3cb025fa8646e85563849da555c8df5e46e5a08aa07453b63`。
- 当前已有 15 段 TOP/20mil 铜。typed `track-list` 证据见
  [layout-prewrite-tracks-live.json](layout-prewrite-tracks-live.json)：所有线段端点都位于
  U2/C3/C4/C5/C6 外包络外扩 30mil 内；这能排除 LED/MCU 模块已有铜，不替代逐焊盘
  `net-path` 电气证明。
- 本轮只做 Layout。候选观察引脚出口和空间，不生成布线路径，也不以布通率或布线 DRC
  作为布局完成条件。
- 例外是已经参数化并现场验证的 LDO 模块内部 15 段 TOP/20mil 铜：输入/输出电容、芯片与
  局部 GND 回路直接决定电源布局，所以允许随模块先完成并作为不可破坏约束。它不授权提前
  连接跨模块电源主干、普通信号、全局铺铜或缝合孔。
- 生成、选择并执行各模块候选只代表对应局部布局完成。整板还要解决全部机械/禁区项目，
  生成整板集成图并连续通过两轮 Agent 自检：第 1 轮检查空间/模块关系/视觉异常，第 2 轮严格
  save → reload → fresh dump → fresh render。任一轮修正都清零重来；两轮无修正后才称 Layout
  完成并向用户展示复核包。只有用户对该回读版本明确回复“OK”才能进入上述电源模块例外以外的布线。
- 本 Demo 当前没有已验证的逐元件属性 typed 视图开关，因此不隐藏属性。将来接口可用时也必须
  先保存旧可见性、只改视图、观察后恢复并回读；接口缺失保持 `unsupported`，禁止 GUI 操作。
- 用户可以继续描述器件关系和空间调整，也可以自己调整后确认。后一种情况先重新 dump，将
  实际 anchor/rotation 固化为新参数基线，再从第 1 轮重新执行两轮自检。

统一命令：

```bash
easyeda pcb layout-plan \
  --from <layout.json> --board current-board-live.json \
  --module <module-id> --candidates 3 --out <candidate-dir>
```

输出目录采用整体替换；同一路径从 3 个候选重算为 1 个时不会残留旧
`candidate-02/03.apply.json`。布局输入和 board 均按原始文件字节计算 SHA256；候选不访问
EDA，也没有综合分数。

## 样例一：RGB LED 板边模块

题目要求 RGB 靠 TYPE-C、光敏远离 RGB。输入
[layout-plan-led-edge.json](layout-plan-led-edge.json) 明确 LED1 是底边 anchor，U1/R3/C1/C2
是 follower；四条关系分别绑定真实 pad primitiveId：

- `U1.4 → LED1.4`（RGB_DATA）
- `C2.1 → LED1.1`（+5V）
- `C1.1 → U1.5`（+5V）
- `R3.2 → U1.2`（RGB_BUF_IN）

板边间隙以 polygon 中心线计算。早期实现误用了包含 10mil 描边的 outline bbox，报告
20mil 时实际只有 15mil；修正后 LED1 bbox 到真实底边为 20mil。

输入还把 U3 的现场 rendered bbox
`(379.151,410.751)–(920.903,1552.738)mil` 声明为顶层机械禁放代理。题面来源是
`考试说明.pdf` 第 3 页“按 LCD 外形轮廓丝印大小建立元件禁止区”；U3 是 C2890616，
规格书名义外形 13.5×27.95mm，公开 footprint 的丝印几何与该现场 bbox 相符。这个代理能
验证候选不进入 LCD 外形，不能证明封装级 region 已保存并绑定。

[候选 bundle](layout-candidates-led/manifest.json) 中三个合法结果：

| 候选 | 变化 | 最近外部器件间隙（对象对） | 取舍 |
|---|---|---:|---|
| 01 | 对齐 USB1−550mil，follower gap 8mil | R3↔U3：35.6755mil | 四个所属 pad 距离最短，且保持靠近 USB |
| 02 | 同一 LED 坐标，gap 20mil | R3↔U3：23.6755mil | follower 更松，但 pad 距离更长且更靠近 U3 |
| 03 | 相对 01 整体向左 50mil | R3↔U3：35.6755mil | 略远离光敏，也离 USB 更远 |

选择 **candidate-01**：它满足真实 20mil 板边间隙，四条 pad 所有权不变，且在三个合法
方案中更靠近 USB、pad 距离更短。它到 U3 禁放代理的最小净距也是 **35.6755mil**。
题目对 RGB LED 的关系要求是靠近 TYPE-C，并未给出侧向开口方向；manifest 因而保留
`localFacing is not declared` 限制，不把 20mil 板边距离外推成光学朝向证明。
`copperPolicy: ignore` 只表示不因全板 15 段 LDO 铜拒绝；
manifest 明确记录未做铜几何碰撞证明，写前用上面的 typed track 证据补足本模块范围。

## 样例二：MCU 逐脚去耦

输入 [layout-plan-mcu-decoupling.json](layout-plan-mcu-decoupling.json) 固定 U6 的 x/y/rotation，
把同属 +3V3 的三只电容绑定到不同物理供电脚：

- `C14.1 → U6.1`
- `C15.1 → U6.5`
- `C16.1 → U6.17`

[候选 bundle](layout-candidates-mcu/manifest.json) 的 U6 均保持
`(1771.654, 984.252)mil @ 0°`，apply 也不包含 U6。

| 候选 | C14/C15/C16 到所属 U6 pad | 最近外部器件间隙（对象对） | 取舍 |
|---|---|---:|---|
| 01，8mil | 75.618 / 122.926 / 52.024mil | C14↔X1：10.451mil | 三只均最靠近自己的供电脚 |
| 02，20mil | 87.618 / 134.926 / 64.024mil | C14↔X1：10.451mil | 距离变长，最差外部间隙没有改善 |
| 03，40mil | 107.618 / 154.926 / 84.024mil | C14↔R3：14.026mil | 给晶振方向更多空间，但去耦距离增加 32mil |

选择 **candidate-01**：本轮优先逐脚去耦，10.451mil 外部间隙仍高于输入的 6mil；如果后续
晶振通道的真实几何证明该空间不足，应修改 gap/方位重算，而不是现场拖动 C14。

## 样例三：LDO 整体变换被当前铜拒绝

[layout-plan-ldo-rigid.json](layout-plan-ldo-rigid.json) 用 `rigid` 同时变换 U2/C3/C4/C5/C6，
AMS1117 输出电容以 `ownerPads:["2","4"]` 表达 VOUT/TAB 等电位组。当前板声明
`copperPolicy: require-board-empty`；[诊断 bundle](layout-candidates-ldo-current-board/manifest.json)
的 8 个平移/直角旋转变体全部被 15 段已有铜拒绝，因此没有 apply 文件。

这不是算法无解，也不允许拆铜后现场试摆。正向迁移实验必须复制到独立无铜测试页，再验证
anchor、非对称 bbox、pads 和角度整体变换；考试板上的已验证 LDO 保持原位。

## 样例四：CAN 收发器大/小电容

[layout-plan-can-decoupling.json](layout-plan-can-decoupling.json) 把 U5 固定为核心，并明确两级
供电归属：`C13.1 → U5.3`，`C12.1 → C13.1`。这里表达的是“小电容靠芯片、大电容在外侧”
的布局关系；CANH/CANL、R12 与 D1 的有序信号路径不在这个候选中。

[候选 bundle](layout-candidates-can-decoupling/manifest.json) 的 candidate-01 采用 8mil 内部间隙：
U5 保持 `(2350,1350)mil @ 0°`，C13 为 `(2375,1136.6035)mil @ 270°`，C12 为
`(2375,988.5715)mil @ 270°`。C13→U5.3、C12→C13.1 的焊盘距离分别为
80.1965/136.232mil，模块到外部器件的最小间隙为 105.744mil。选择 candidate-01 的理由是
它保持明确的大/小电容次序，并在合法候选中使所属焊盘距离最短。内部最近对象是
C12↔C13（8mil）；外部最小值来自固定核心 U5↔CN1（105.744mil），不是两只移动电容到外部
器件的间隙。不能据此声称 CAN 信号布局或布线已经完成。

## 样例五：Micro-SD 电源入口

[layout-plan-sd-decoupling.json](layout-plan-sd-decoupling.json) 保持题定 CARD1 anchor/角度不动，
声明 `C19.1 → CARD1.4`、`C18.1 → C19.1`。candidate-01 使用 20mil 搜索间隙，得到
C19 `(2806.104,942.9)mil @ 180°`、C18 `(2833.704,809.636)mil @ 270°`；两段所属焊盘
距离为 83.596/93.864mil，模块内部和外部最小间隙分别为 13.546/26.502mil。
最近对象对分别是 C18↔CARD1 与 CARD1↔R9；外部最小值来自固定核心 CARD1，不应误读成
移动电容的外部间隙。

选择 [candidate-01](layout-candidates-sd-decoupling/manifest.json) 是因为它在不移动 CARD1 的
前提下保持 100nF 靠 VDD、10µF 位于外侧；被拒变体和剩余候选保留在 manifest，不能现场
逐件试摆来绕过拒绝原因。

## 样例六：CH340N 逐脚去耦

[layout-plan-usb-uart-decoupling.json](layout-plan-usb-uart-decoupling.json) 不把同为 +3V3 的两只
100nF 重新按最近距离分配，而是固定 `C9.1 → U4.8 V3`、`C10.1 → U4.5 VCC`。选择
[candidate-01](layout-candidates-usb-uart-decoupling/manifest.json)：U4 不动，C9 为
`(1315.2525,655.6)mil @ 180°`，C10 为 `(1672.143,655.6)mil @ 0°`；对应焊盘距离
82.1475/69.543mil，内部/外部最小间隙为 8/12.003mil。这个例子证明“同网不同 pin 仍需
显式所有权”。最近对象对分别是 C10↔U4 与固定核心 U4↔C3；12.003mil 不是移动电容到
外部器件的最小值，也不证明 TXD/RXD 或 USB 信号通道已经布线。

## 样例七：LCD 供电与背光驱动链

[layout-plan-lcd-peripherals.json](layout-plan-lcd-peripherals.json) 保持 U3 不动，并显式声明：

- `C7.1 → U3.10`，不因 U3.12 同网而改派；
- `R6.2 → U3.11`；
- `Q1.3 → R6.1`；
- `R4.2 → Q1.1`、`R5.1 → Q1.1`。

选择 [candidate-01](layout-candidates-lcd-peripherals/manifest.json) 后，C7/R6/Q1/R4/R5 分别为
`(1000.624,980)@0°`、`(998.434,820)@180°`、`(1136.013,820)@0°`、
`(1273.592,782.6)@180°`、`(1175.013,682.39)@270°`。模块内部最小间隙为
18.217mil，到外部器件为 35.6755mil，到声明的 LCD 机械禁放代理为 20mil。C7/R6 到 U3
焊盘的距离仍较长，分别为 413.5359/436.3306mil；这是当前 U3 大外形与禁放代理下的真实
取舍。三个最近对象对分别是 R4↔R5、固定核心 U3↔R3、C7↔LCD 禁放代理；外部最小值不是
移动外围之间的间隙，后续应通过走线通道继续判断，不能用总分掩盖。

U3 本来就有完整的正式绑定：[只读回读](u3-existing-model-binding-live.json) 证明它是
`C2890616 / N096-1608TBBIG11-H13`，绑定 `OLED-SMD_ST7735S` 封装和 3D model
`55cc08024bd249a298d835f2dd067767`。这些都不是 Agent 绘制的；增加 LCD 本体禁放区必须保持
现有 device、footprint 和 3D model 关联，不应把“加 region”实现成“换模型”。

此前新增的几何只有个人库可写副本
`EA_AGENT__U3_LCD_COMPONENT_KEEPOUT_DEMO`（footprint UUID
`5e1662059e174644a40d45f813b437d5`，library UUID
`f60b2174579745258ada9b72bbe2f52b`）已保存一个 layer 12、`ruleType:[2]`、locked 的
`no-components` region（primitiveId `74049f69b7f01501`）；宿主没有保留可选 name。这个事实只
证明 region typed 接口能在副本持久化，副本没有也不应默认绑定到 U3。直接向现有 source
footprint 添加同一区域的尝试因 `pcb_Document.save returned false` 返回 partial，没有证明保存。
随后 typed `lib libraries` 证明 `0819f05c4eef4c71ace90d822a990e87` 正是 EasyEDA
`systemLibraryUuid`，因此失败根因是系统封装不可写。`library.footprint.region_create` 现已增加
前置识别：遇系统库时在打开编辑器和创建几何前拒绝，不能再把这类失败当成可重试保存问题。

一次 `schematic.rebind.footprint` 超时在删除原 U3 后没有完成重建。随后通过参数化 `sch place`
恢复原器件并保存、typed reload；[恢复证据](schematic-u3-recovery-live.json) 显示原理图回到
69 件，U3 的 13 个 pin/net、位置和原 footprint 一致，但 primitiveId 与 uniqueId 都已变化。
这次事故说明不应为禁放区重绑已有正确模型。之后只用 typed `sch modify` 把原理图 U3 的
uniqueId 从 `gge70` 恢复为 PCB U3 的 `gge60`；保存、真实重载后仍为 69 件、13 个 pin/net
完全一致，device、symbol、footprint 与属性均未变化，[对账证据](u3-identity-reconcile-live.json)
显示两侧 `gge60` 都只有 U3 一个拥有者。本次没有运行 PCB `import-changes`；先前因 identity
不一致而设的禁令已经解除。禁放区仍是独立未完成项：不得写系统封装，也不得默认重绑个人副本，
需补齐并现场验证保持现有绑定的实例级/工程级 typed region 能力。

随后对现有 U3 bbox 做了一次完全 typed 的板级 region 负例：创建 layer 12、`ruleType:[2]`
的 top-level 区域后，DRC 从 216 个既有 Connection Error 增加为 217 个，并新增
`Device to Prohibited Region`，对象正是该 region 与 owner U3。该候选随即 typed 删除，保存、
真实重载后 region 数回到 0，DRC 也精确恢复为 216。完整输入、对象 ID 与前后哈希见
[u3-instance-region-negative-live.json](u3-instance-region-negative-live.json)。因此普通板级区域不是
封装内禁放区的合格替代；后续接口必须能表达 owner 豁免，否则继续 `incomplete`。

## 样例八：CAN 终端电阻与 ESD 保留当前关系

[layout-plan-can-rigid.json](layout-plan-can-rigid.json) 把 R12/D1 作为刚体模块比较，同时固定
R12 为 0°、D1 为 270°，并保留 D1 靠 CN1、R12 位于 U5 与 CN1 通道的题意关系。
[candidate-01](layout-candidates-can-current-board/candidate-01.json) 是“保持当前 pad 顺序”的零位移
候选：R12 `(2630,1510)@0°`、D1 `(2791.5,1528.151)@270°`；两件内部净距
40.882mil，D1 到 CN1 的最近 bbox 净距 10.056mil，均高于 6mil 输入间隙。该候选没有器件
修改 action，仅保存检查点，说明当前位置/方向已被参数化基线接受。

这里不再用 ratsnest 的最短直线相交、长度比或段数比否定 Layout。R12 两个焊盘保持
CANH 在左、CANL 在右，D1/CN1 的 H/L 顺序也一致，但这只说明器件出口顺序和空间关系；
实际铜仍须在布线阶段证明 `U5 → R12 对应焊盘 → CN1` 的两条有序主路径以及 D1 近端支路。
历史最短飞线相交继续作为布线反例，不升级成新的 Layout 门禁。

## 执行与验证记录

执行队列只能来自所选 `candidate-01.apply.json`。主 Agent 串行写入同一 Web EDA 窗口，随后：

1. `pcb save`；
2. 有界 `doc reload 2e719e9419653c72`；
3. 新 `pcb dump` 核对 69 件、所选 anchor/rotation、固定器件、板框和 15 段 LDO 铜；
4. 另读 `track-list`，确认没有新增布局阶段铜。

第一批 LED/MCU 现场执行结果为 **`live-verified`**：

- 2026-09-20 在 Web EDA 的 `ceshi/PCB1_1` 串行执行两个 candidate-01；没有 GUI 手摆和
  `debug.exec_js`。
- 保存并真实重载后，[回读快照](layout-after-led-mcu-live.json) 仍为 69 件；恰好只有
  C1/C2/LED1/R3/U1/C14/C15/C16 八件位置或角度变化，均在 `1e-6mil` 容差内对应候选。
- SCREW1–4、U6、CARD1、CN1、184 点板框和规则保持不变；
  [typed track 回读](layout-after-led-mcu-tracks-live.json) 仍是同一批 15 段 TOP/20mil
  LDO 铜，primitiveId、网络、端点和线宽逐项不变。
- 用保存后快照重新计算，LED/MCU 的 candidate-01 仍与现场坐标一致。实际 EDA 焊盘回读
  会按 0.1mil 量化，逐脚距离分别变为 LED `71.1/86.5/78.5644/81.9mil`、MCU
  `75.7/123.0/52.1mil`，不影响 8mil 内部间隙、35.6755mil LCD 净距与候选选择。
- [整板 layout-lint](layout-after-led-mcu-lint-live.json) 报告 0 overlap、0 off-board、
  0 tight-spacing。55 个 ratsnest crossing 是后续模块/布线路径观察项，分数不作为布局许可。

封装级 keepout 仍没有出现在当前 `pcb dump` 中，因此这里只证明声明的矩形代理与器件
bbox 关系；个人库副本 region 的实证也不能外推成当前 U3 实例已绑定。

第二批 CAN/SD/USB-UART/LCD 外围同样为 **`live-verified`**：

- 四组均选择 candidate-01，按顺序通过 typed apply 写入；核心 U5、CARD1、U4、U3 没有移动。
- 保存并真实重载后，[回读快照](layout-after-peripherals-live.json) 仍为 69 件，恰好只有
  C12/C13、C18/C19、C9/C10、C7/R6/Q1/R4/R5 共 11 件位置或角度变化，均对应候选。
- [typed track 回读](layout-after-peripherals-tracks-live.json) 仍是同一批 15 段 TOP/20mil
  LDO 铜，primitiveId、网络、端点和线宽逐项不变；四组到这些铜的最小净距分别为
  364.884/727.738/88.132/477.821mil。对应最近对象对依次是 C12↔GND 线段
  `369544daea524190`、C19↔同一线段、C10↔GND 线段 `1b08f7dee26a2bc8`、
  R4↔GND 线段 `a76f0b60f508dff4`；这里按移动外围计算，不把固定核心混入该比较。
- 四组一起放置后的跨模块最小间隙是 C9↔R5 的 51.5065mil；用保存后快照重新计算，四个 candidate-01
  仍与现场坐标一致。
- [整板 layout-lint](layout-after-peripherals-lint-live.json) 仍为 69 件、0 overlap、0 off-board、
  0 tight-at-6mil；55 个 ratsnest crossing 只用于后续通道观察，不形成总分或布线许可。
- 用户两次重开内置浏览器后都用 typed CLI 只读复核；第二次连接曾短暂消失，恢复前没有执行
  写入或编辑器恢复动作；
  [重开证据](layout-after-browser-reopen-verification-live.json) 显示 69 件 primitiveId 集合、器件
  几何、板框和 15 段 LDO 铜仍逐项不变，且没有执行 PCB `import-changes`。

这批实证完成的是外围坐标、角度、逐脚归属和持久化；R12/D1 的当前位置/方向也通过零位移
刚体候选收敛。CAN 有序主路径的实际铜、LCD 封装实例绑定和各模块实际铜路仍属于后续步骤；
不引入 CAN 长度比、段数比或综合评分门槛。
