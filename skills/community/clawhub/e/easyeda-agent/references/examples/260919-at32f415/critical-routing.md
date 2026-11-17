# 样例：关键网络离线规划如何反向修正布局

## 来源与状态

- `考试说明.pdf` 第 4–5、8 页：晶振靠 MCU、不在板边、短直、避免底层及顶层包地净空；
  CAN 明确要求顶层无换层，分别先经过 120Ω 电阻对应焊盘再到端子，ESD 靠端子。
- `原理图.pdf` 第 1 页：`OSC_IN/OSC_OUT`；R12 跨 CANH/CANL，D1 分别连接 H/L 并回地。
- 输入为第一轮参数化布局保存并整页刷新后的真实 pads/bbox，以及 6mil 间距、8mil 信号线宽。

状态：`live-verified`（历史晶振铜事实与 CAN 铜范围）。晶振布局之后的 TOP/8mil/0via 铜已经通过 typed 写入、
保存重载、有序 `pcb net-path`、`pcb check`、官方 DRC 和锁定持久化验证，见
[crystal-route-live.json](crystal-route-live.json)。用户在 2026-09-22 复核后明确指出该晶振区不是
最佳完成态：还需要受控 MCU 间距、更短直的信号、TOP GND 护环、双层 no-pours 禁铺区和外围
GND 过孔围栏。因此旧铜路只保留为事实已验证的负例，新的最终要求见
[crystal-guard-requirement.json](crystal-guard-requirement.json)。CAN 又完成了一轮真实布局迭代：
D1/CN1 的 H/L 支路已改成对称关系，但 R12 候选暴露两处 H/L 飞线相交，作为负例保留在
[can-placement-iteration-live.json](can-placement-iteration-live.json)。随后 CANH/CANL 主路径与 D1
保护支路也完成联合规划、typed 写入、保存重载、有序路径证明和锁定，见
[can-route-live.json](can-route-live.json)。
USB_D+/D- 随后也按同一证据链完成；USB-C 的四个重复数据焊盘分别证明连到 U4，详见
[usb-route-live.json](usb-route-live.json)。这组现场迭代还暴露了精确 pad/器件/独立 region
快照的覆盖边界：USB1 封装内嵌 Slot Region 没有出现在当前快照里，必须由官方 DRC 兜底。
后续原文复核发现旧 CAN 计划未证明 R12 主路径顺序；离线 passed 或布局命令成功都不表示完整题目拓扑已验证。
结果证明“几何上能布通”仍可能是差布局；本样例的完成动作是把绕行原因反馈给布局参数，而不是
为了让工程看起来更完整而落下 77 段不理想走线。

## 开始状态与参数

目标 PCB 以 UUID 定位，不依赖 Board 显示名。开始时无走线，使用本轮读取的 pad 中心和矩形，
旧计划把其他网络 pad、器件和已规划轨迹统一按 6mil 膨胀；这是简化模型，不是题目对所有
间距的规定。正式规划须按对象类型读取实际规则并计入线宽，器件占地与铜层障碍也要区分。

| 参数 | 晶振 | CAN |
|---|---|---|
| 网络 | OSC_IN、OSC_OUT | CANH、CANL |
| 层/线宽/过孔 | TOP / 8mil / 0 | TOP / 8mil / 0 |
| 必达拓扑 | U6.2 ↔ X1.1/C21；U6.3 ↔ X1.3/C20 | H/L 各自 U5 → R12 对应焊盘 → CN1；R12 跨 H/L，D1 靠 CN1 |
| 转角 | 0/45/90/135° | 0/45/90/135° |
| 计划哈希 | `2bdf39440d2d1a47dfb2e0de87dc5a5ec09f10e2f82a449a887478e0f6e6d92f` | 同一批 |

晶振 TOP/0via 是本例的推荐策略，原题没有对晶振单列绝对零过孔禁令。转角表中的数字是
线段方向，不是允许相邻线段形成直角；实际转折仍遵守本题无直角/锐角要求。

完整离线计划为本次开发记录，不随 Skill 打包；样例只保留能迁移的参数、结论和修法，避免把
58KB 的一次性绝对坐标塞进入口。迁移时必须从当前板重新读取 pads/bbox 并重算。

## 计划、观察与决定

离线规划先做 pad-normal escape，再在 45°格点上避开膨胀障碍，最后检查真实 pad 端点、板内、
异网轨迹间距、层和过孔数。检查覆盖 14 个必达端点，共 77 段、0 过孔、0 离线违规。

| 组 | 离线结果 | 观察 | 下一步 |
|---|---|---|---|
| 晶振 | 28 段；OSC_IN 882.7mil、OSC_OUT 269.4mil | U6.2/.3 与 X1.1/.3 左右次序反转，OSC_IN 被迫绕晶振区一大圈 | 旋转/重排 X1、C20、C21，保持两网引脚次序后重新求短解 |
| CAN | 49 段；保持 H/L 网表跨接，但未证明主路径先过 R12 | D1 未对齐端子信号 pad，CANL 绕行 1422.4mil；旧计划还遗漏 R12 必经顺序 | H/L 各显式经过 R12 对应焊盘再到 CN1；D1 对齐端子且保留短地支路，重新规划 |

这一步没有把 `passed=true` 解释为“应该执行”。离线 passed 只证明给定障碍和检查器下没有已知
几何违规；短直、回流、EMC 和人工布局质量仍需看长度、拓扑与局部关系。

## 晶振第一批现场修正：只改次序，不落铜

第一批把“布局导致绕线”拆成一个独立步骤。U6 保持题定 anchor、0°和锁定；X1 只从 180°
改为 0°，C20/C21 复用彼此原有占位并把信号 pad 朝向 X1、GND pad 朝外。两只电容交换时
先把 C20 放到一个经实时 bbox 确认的临时空位，避免中间态重叠；临时点和 primitiveId
只属于本次现场，迁移时必须重新计算。实际命令与回读见
[crystal-placement-live.json](crystal-placement-live.json)。执行形态为：

```bash
easyeda pcb modify --id <C20_ID> --center --x <TEMP_FREE_X> --y <TEMP_FREE_Y> \
  --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <C21_ID> --center --x <OLD_C20_CENTER_X> --y <OLD_C20_CENTER_Y> \
  --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <C21_ID> --patch '{"rotation":180}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <C20_ID> --center --x <OLD_C21_CENTER_X> --y <OLD_C21_CENTER_Y> \
  --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <C20_ID> --patch '{"rotation":0}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb modify --id <X1_ID> --patch '{"rotation":0}' --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb save --doc <PCB_DOC_UUID> --project ceshi
easyeda doc reload <PCB_DOC_UUID> --project ceshi --json
```

保存重开后的事实：

- U6 未移动且仍锁定；X1/C20/C21 都在 TOP，69 件仍为 0 overlap、0 outside、0 tight-spacing。
- U6 侧从左到右为 OSC_IN/OSC_OUT；X1 侧也改为 OSC_IN/OSC_OUT。两条 U6↔X1 直连从
  相交变为不相交，整板 ratsnest 从 27058.07mil 降到 27045.82mil，crossing 从 58 降到 57。
- U6.2→X1.1 的直距从 99.81mil 增至 148.23mil，U6.3→X1.3 从 151.73mil 降至
  91.07mil；四个信号关系的直距合计只减少 12.25mil。因此本批的主要价值是消除交叉和
  纠正负载电容方向，不能声称两网都缩短。
- OSC_IN/OSC_OUT 仍各为 0 track、0 arc、0 via；官方 DRC 仍含这六个信号端点的
  Connection Error。本批状态只覆盖布局，不能外推为晶振布线通过。

随后在 connector 1.5.3-dev.3 下读取 235 个顶层/通孔焊盘的真实 `shape/rotation/specialPad`
并确认 `arcsAvailable=true`。第一版 OSC_IN 铜虽通过保守净距检查，但现场 `pcb check` 暴露
45°锐角，且分支位于 X1 前方，无法用不重复铜路径证明电容先到 X1 再到 MCU；该版只删除
OSC_IN 本批 9 个实际图元，OSC_OUT 保留。第二版令 C21.1 先到 X1.1，再从 X1.1 以 90°节点
离开至 U6.2。保存重载后两条有序路径分别为 `C21.1 → X1.1 → U6.2` 与
`C20.1 → X1.3 → U6.3`，均为 TOP/8mil/0via，`acute-angle=0`，15 个关键铜图元锁定后再次
保存重载仍保持。正式事实见 [crystal-route-live.json](crystal-route-live.json)。

本轮还修正了数据入口认知：集成 `pcb dump` 面向板级规划，可能不保留 pad 的原始形状字段；
正式几何与 `pcb net-path` 应读取 `pcb components-list --include-pads` 返回的真实 pad 数据，
不能因 dump 中字段缺失就降级到 bbox。

## 用户复核后的晶振护环完成口径

2026-09-22 的参考图只用于学习拓扑与空间关系，不复制其中坐标、线宽或过孔节距。可迁移要求为：

- X1 与 C20/C21 保持紧凑，靠近 U6 的 OSC 引脚但留出受控间距，不能贴压 MCU 外形和相邻引脚逃线；
- OSC_IN/OSC_OUT 在两端保持同序，TOP、0via，并按“拓扑正确 → 不交叉 → 短直 → 少转折”选择候选；
- 用真实 GND track 在顶层围绕敏感区形成护环，只留必要的信号入口，护环必须实际接地；
- 在 TOP 与 BOTTOM 分别创建 `no-pours` region，覆盖晶振、负载电容和敏感信号包络；
- 沿护环外侧或禁铺区边界之外放置 GND 过孔围栏，连接顶底 GND。不能用 `pcb via-stitch`
  的满矩形网格把地孔填进晶振禁铺区，应使用 perimeter-only 的 `pcb via-fence`；
- 器件、信号铜、护环、regions 和围栏孔组成一个参数化模块。任何成员移动后整组重算，不能
  只拖器件或局部补铜。

验收必须分别证明两条 OSC 有序铜路、GND 护环连通、两层 region 持久化、围栏孔全部绑定 GND，
并在 `pour-rebuild` 后确认禁铺区无铺铜残留，再执行 `pcb check`、官方 DRC 和 fresh render。
旧结果虽满足连通/层/via/基础几何检查，但缺少上述对象，不能继续称作晶振区最终通过。

## CAN 第一批现场迭代：保留局部改善，拒绝整组候选

第一轮保持 U5 和题定 `CN1 y=42mm / 180°` 不动，把 D1 旋转到 270°并令其 H/L 与 CN1
信号脚中心对齐；R12 候选移动到中心 `(2630,1510)mil`、0°。所有动作经 typed CLI 写入，
保存、`doc reload` 后同一 primitive 和 pads 保持。完整命令、原始回读哈希和两轮独立核查见
[can-placement-iteration-live.json](can-placement-iteration-live.json)。

这轮得到一个可保留的局部关系和一个必须拒绝的结论：

- D1.1→CN1.2 与 D1.2→CN1.1 都约 `168.94mil`，比修改前约 `217/295mil` 对称；D1 与
  CN1 的 bbox 净距约 `10.06mil`，只说明器件未重叠，不能把这条缝当走线通道。
- R12.1=CANH 在左、R12.2=CANL 在右，仍是跨接 120Ω；但纯 MST 飞线出现两处 H/L
  相交。最初“预计不会先天交叉”的离线候选被真实回读否定。
- 将 R12 的 y 对齐到 D1 信号 pad 的 `1488.8mil` 也不是修法：它会让 R12.2 落在
  CANH 水平段、D1.1 落在 CANL 水平段，把点交叉变成异网共线穿越。
- U5.6 右侧还有 U5.5 NC。按 8mil 线和 6mil 净距膨胀后，该 pad 的禁入矩形为
  `x=2402.6..2447.4, y=1408.9..1502.3mil`；只分别给两网找最短路会漏掉相互穿越。

因此该第一轮最短飞线只作为负例，不凭单一 crossing 数直接落铜；R12 的零位移布局后来由
完整模块候选接受，并在下述第二批布线中以有序主路径实证。
H/L 双线联合寻路保留为历史待研究方向：每网带 R12 必经节点，D1 作为靠端子的短支路，
统一检查 pad/track/NC/板框/既有铜、8mil 线宽、6mil 净距和 45°转折。本轮暂停 CAN
专用路由器扩张，只处理器件位置与方向；这组历史实验不作为 Layout 候选的拒绝门禁。

## CAN 第二批现场布线：有序主路径与保护支路

最终候选保持 R12/D1/CN1 的用户确认布局不动，同时联合规划 H/L。每条主路径把对应 R12
焊盘作为显式 waypoint；D1.1/.2 从实测外侧焊盘端出线并在端子侧主干形成声明的 T 点。
两条竖向主干分别从 D1/CN1 组合体的左、右外侧进入端子，没有尝试利用两者仅
`10.056mil` 的体间隙。精确焊盘来自 `pcb list --include-bbox --include-pads`，其内容哈希与
`pcb dump`、tracks/vias/pours/fills/regions 哈希共同绑定候选。

第一版写后暴露一个中心线检查盲区：R12.2 后的过渡只有 `2mil`，两条非相邻 `8mil` 斜线的
物理铜面积重叠。官方 DRC 和 `pcb check` 均未报错，但严格 `pcb net-path` 返回 topology
unknown。该批只 rip-up CANH/CANL，拉长过渡并同步调整 H 支路，再次离线通过后重写。
校验器现已新增 `same_net_copper_overlap`，并接受可选 `--components` 精确焊盘输入；以后不再
依赖 `pcb dump` 的 legacy pad hull，也不再把中心线分离误当成规范铜拓扑。

保存重载后的四项证明均通过：

- `U5.7 → R12.1 → CN1.2`：TOP/8mil/0via；
- `U5.6 → R12.2 → CN1.1`：TOP/8mil/0via；
- `D1.1 → CN1.2` 与 `D1.2 → CN1.1`：TOP/8mil/0via；
- `pcb check` 为 0 dangling/acute/non-orthogonal/track-over-pad/clearance/duplicate，官方 DRC
  只有未布线 Connection Error，数量从 210 降到 202。CANH/CANL 的两条 generic 3W WARN
  属于成对同向短并行段；实际 6mil 规则满足，原题没有另加 3W 分离要求。

33 个 CAN 铜图元锁定后再次保存重载仍保持。D1.3 的 GND 回路留到局部 GND 与双面铺铜阶段，
因此本节只称 CAN 信号铜通过，不外推为 CAN 模块供电/回流或整板 DRC 完成。

## USB 现场布线：封装内 Slot Region 是独立障碍

USB_D+/D- 使用 TOP、8mil、0via，并把 USB-C 的 A/B 重复数据焊盘分别汇合后接到 U4。
第一版离线检查读取了 235 个焊盘的真实 shape/rotation/specialPad，并覆盖器件、既有轨迹、
vias、pours、fills 与顶层 regions；报告为零 finding。写入后官方 DRC 仍在 USB_D- 上报两处
`Slot Region to Track`：距离 0mil，规则要求至少 11.8mil。第二版把路线向外推后仍为
10.6mil，继续不合格。最终只 rip-up USB_D-，在 USB1 外侧更早下沉到 `y=220mil` 再返回
U4.2，官方 DRC 才只剩未布线 Connection Error。

这个结果形成新的机械边界：当前 typed `components-list` 与独立 `region-list` 看不见某些
footprint 内嵌 Slot Region。离线候选必须在报告里显式保留该限制，并在每次真实写入后运行
官方 `pcb drc`；不能把精确 pad 检查或零 finding 外推为已经覆盖封装内部铣槽/开窗对象。

保存重载后的四条路径均成立：`USB1.A6→U4.1`、`USB1.B6→U4.1`、
`USB1.A7→U4.2`、`USB1.B7→U4.2`，均为 TOP/8mil/0via。`pcb check` 的铜相关项目为零，
官方 DRC 从 CAN 里程碑的 202 个 Connection Error 降到 196，且没有其他违规类型。
平台在重复焊盘汇合的 T 接点拆分了实际图元，所以 12 个计划动作回读为 14 个 track；
14 个图元锁定并再次保存重载后全部保持 `locked=true`。

## 执行形态与回读

重排后重新生成段。每段映射到现有 typed CLI；下面只展示数据形态，不复制本轮绝对坐标：

```bash
easyeda pcb track --x1 <PAD_ESCAPE_X> --y1 <PAD_ESCAPE_Y> \
  --x2 <NEXT_X> --y2 <NEXT_Y> --layer 1 --width 8 --net OSC_IN \
  --doc <PCB_DOC_UUID> --project ceshi
```

按网络小批执行，每批后读取该网 tracks/vias；超时或部分写入时先回读，只 rip-up 当前失败网并
从新状态重算，不重放整组。晶振先于 CAN，二者通过后保存并做持久化回读：

```bash
easyeda pcb track-list --net OSC_IN --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb track-list --net OSC_OUT --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb via-list --doc <PCB_DOC_UUID> --project ceshi
easyeda pcb check --strict --doc <PCB_DOC_UUID> --project ceshi --json
easyeda pcb drc --doc <PCB_DOC_UUID> --project ceshi --json
easyeda pcb save --doc <PCB_DOC_UUID> --project ceshi
```

若 `doc reload` 在 Web 版持续显示加载动画，停止重试和现场写入，保存故障与当前对象证据，
将持久化验证标为 `incomplete`。先修复 typed reload/open，再重复 tracks/vias/check/DRC 读取；
禁止通过浏览器或工程树手工恢复。

## 暴露的工具缺口

- 当前 `route-short` 的 MST 只理解“同网端点”，不理解 H/L 各自 `U5 → R12 对应焊盘 → CN1`
  的先后关系。R12 仍跨接两网，不能串入单根信号线；D1 是靠近端子的保护支路。
  后续接口需要显式 topology anchors 与 forbidden shortcuts，不能按最近距离偷连。
- 关键网需要每网 `topOnly`、`noVia`、pad-normal escape 等约束；这些应是计划输入与回读断言，
  不能靠 Agent 看完题目后记住。
- `pcb.line.create` 没有多段事务，超时可能已经写入前几段。工具必须返回部分执行证据；样例按
  net-scope 回读与删除，避免整板重放。
- DRC 规则配置、网络类成员及成员到 Track 规则的关联是三类事实，要分别回读。

## 验证边界

- 已验证：旧晶振方案的三件次序与两网实际铜；精确 pad 形状输入、TOP/8mil/0via 有序路径、
  无断头/锐角/铜越焊盘/净距 finding、官方 DRC 无新增非 Connection Error、保存重载及关键铜锁定。
  这些是可复现事实，不再代表最终设计已接受。
- 未验证：新的 `crystal-guard` 完整模块、D1.3 局部 GND 回路，以及整板最终布通后的 DRC。
- 修法的验收不是“段数变少”本身：还要重新核对端点、拓扑、长度、净距、via 数和保存后对象。
