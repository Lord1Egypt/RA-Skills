<!-- v5.6.0 起本文件为完整历史存档；changelog.md 只保留版本索引+最近三版详情。历史条目措辞保持原样，不做回改。 -->
<!-- v8.1.2 整理（2026-11-25）：按版本降序、每个版本一节。此前多次下沉造成的重复与乱序已合并——同一版本若有几份
     不同写法的稿子，几稿并存于该版本的一节之内（先 changelog.md 稿、后存档稿），原文一字未改。更早的旧格式双语
     历史原样保留在文末。结构锁：随包测试 TestV80102ChangelogLock。 -->

# Changelog / 版本历史（完整存档）

> **何时读我**：查某个版本改了什么。Ctrl-F 版本号。
> **最近三版**（在 changelog.md 的「最近版本详情」里）：v8.1.6、v8.1.5、v8.1.4。
> **回 INDEX**：SKILL.md「版本历史」。

## 8.1.3 — 2026-11-26

**流程图端点质量两项**：

- **箭头三角画在节点之下**：节点补丁 zorder=3、箭头三角 zorder=5，浅斜边上水平
  进入时翼片探入节点约 0.027in（mermaid 导入图的复查箭头，原尺寸放大实测）。
  箭头三角（实体头与双回头）降到 2.5——连线（2）之上、节点（3）之下，探入部分
  由节点填充盖住；箭头尖端按 EDGE_NIB 停在描边外沿，不受影响。连线穿节点本是
  路由硬禁，节点置顶不会遮住任何合法线段。
- **入列避开源尖顶点**：竖直入列距源节点（菱形/六边形/IO 等）左右顶点 <0.10in
  时外推到 0.10in（外推后仍落在目标边内才生效）。决策图「Low」边竖段离菱形左
  顶点 0.045→0.105in；scRNA-seq「pass」边出右顶点后的拐点外推，首段
  0.053→0.10in（拐点不再咬住顶点）。此前试过「离顶点过近计代价」——候选池里
  没有干净走法，被推向更差的候选（另一次交叉离拐角过近），已撤回；本版改的是
  端口列本身，一处修复两处受益。
- 13 张泳道/流程验收图：机械审计 A–L 全零；路由仅上述 2 处按预期移动、2 个标签
  跟随，其余逐边对账零变化。测试：TestV80103 三锁（箭头层级源级锁/入列净空/
  首段净空；变异验证：钳制或 zorder 改回旧值必败）；**659 测试**。

## 8.1.2 — 2026-11-25

**变更日志归档整理**：完整历史 `changelog-full.md` 经多次下沉后是乱的——11 个版本各有两份
不同写法的稿子、开头数节乱序。现按版本降序、每个版本一节；同一版本的两份稿并存于同一节
（原文不改），旧格式双语历史原样留在文末；对照整理前逐行核对，零丢失。8.0.0 与 7.9.2
此前只有索引行、没有详情节，据当版索引行补写；索引里 8.0.0 的测试数 596 更正为 601
（按该版包内 README 徽章核实）；存档里 8.0.2 的日期 11-15 更正为 11-16（按该版提交与包内
日期核实）。主文件 `changelog.md` 从此只留索引与最近三版。新增结构锁 `TestV80102ChangelogLock`（索引↔详情一一对应、每版本合计恰一节、
降序、主文件只留最近三版、旧格式尾段在；变异验证内置），旧的历史补全锁改为「6.9.0 与
7.0.0 两节在两份文件合计各出现一次」。发版加了新条目后跑一次整理器即滚动窗口。
**656 测试**。

## 8.1.1 — 2026-11-25

**流程图端口离框角余量**：箭头半宽 0.10in，旧余量 0.06in 下出入点贴近框角时箭头
翼片会探出框角或压在圆角上；现出入点离所在边的两端至少 0.12in（侧向与顶/底端口
同口径）。13 张泳道/流程验收图重审计，4 处端口变化逐处放大核对；52 个模板输出
尺寸零变化。未采用对「文件」形（波浪底）的侧向端口再按轮廓抬高（夹具看图会把
另一条入线挤成从下方戳进波浪底）。测试：TestV80101PortMargin（八套模板 CLI 边车
逐端点核对；变异验证：余量改回 0.06 必败）；**654 测试**。

## 8.1.0 — 2026-11-24

**泳道 LR+mermaid 直通+边样式图例+路由与标签系统重做**：

- **泳道 LR 横行带布局**（docstring v8.0.6 承诺落地）：lane 自上而下堆叠为
  横条带，lane 内节点自左向右按声明序排布；**标题=左侧深色竖条+旋转 90°**；
  行带纯内容化，行间隙成为水平走廊；分隔带方向感知（TB 垂直带/LR 行带缘）。
- **泳道期刊化配色**：泳道带底色由「向黑混合」改为同色浅色调（奇偶行微差
  +细分隔线+略深标题带+深色标题字）——近黑大色块根除。
- **通道轨道（泳道 LR）**：相邻行之间每条横穿边分到一条自己的轨道，带标签的
  边轨道更高，行间隙按需累加（旧版恒 0.30in，走线位置靠候选取样）。
- **路由评分制**：候选不再「取第一个合法」，全部合法候选按代价择优（共线
  重叠→贴近→近端口交叉→交叉→同角冲突→拐弯→长度）；候选取样按净空推导
  （按被穿线段两端预留直接推导交叉位）+障碍间自由区间中点（窄缝穿行）。
- **到达方式规范**：「顶/底出、侧入」候选的拐点改为先沿出段方向再转入段方向
  ——此前该族候选的末段沿目标侧边线下行，多套模板里出现「箭头沿框边滑下、
  箭头尖指着边」；镜像入槽（同一侧的第 2 条入线被挤到贴边滑行时，试中线
  另一侧的端口）；交叉点离出入口 ≥0.30in、离拐点 ≥0.20in；拐角咬合规避
  （两条线的拐角一上一下咬在一起=读起来像接线）。
- **对齐直落**：源节点中心列落在目标顶/底边内侧时，直接竖直落到目标边上——
  宽节点接收上方多个来源时各走各的竖线（此前各横到目标中线附近再折下，两条
  首段叠成一条贯通横线，读起来像两个互不相连的节点直接相连）；箭头所在的末段
  不足 0.225in 的候选让位（箭头翼片不再垂在拐角之外）。
- **边标签系统重做**：融底底垫（泳道内取所在泳道带底色）；按节点真实轮廓判
  碰撞；归属按标签框到线的距离算（离自己的边 ≤0.40in；别的边不得近于
  「自己的边+0.12in」）；沿线滑动步长加密；压线标签离交叉线 ≥0.14in。
- **边样式图例**：图含 dashed/thick/bidirectional 混合样式时自动出现
  （`"legend": true|false` 显式覆盖）——画布底部专用条带，线样+语义文字
  （语言随节点 CJK 检测），文字/线色随画布底色自适应反色。
- **mermaid 直通**：TB 方向 subgraph 直出泳道（LR/BT/RL→分组框诚实降级）；
  linkStyle stroke/dasharray/width→边 color/dashed/thick；classDef/class/
  style fill→节点 color。
- **诊断**：`--dump-flow-routes` 边车导出各边候选代价、被拒原因与标签放置
  轨迹（路由结果为什么是这样，可逐候选查证）；legend/lanes 入诊断字段表。
- **limits.md 诚实注记**：极端 DPI（--dpi 60）文本测量舍入可翻转路由决策
  （默认 600 稳定）；非相邻行跨行边走 lane 兜底（建议相邻行布局）。
- **测试类名固位规则**：版本化测试类名统一「主 1 位+次 2 位+修订 2 位」
  （如 TestV80100），套件内自检。
- 测试：TestV80100（泳道 LR/评分制路由/通道轨道/标签归属/类名规则）+
  TestV80100MermaidStyle（linkStyle/classDef/style 映射+styled E2E）+
  TestV80100EdgeLegend（三态渲染契约/legend 非布尔 fatal/E2E strict+图例
  条带像素在场）；泳道模板 52（+LR 期刊评审三泳道）；examples 三件；
  **653 测试**。

## 8.0.9 — 2026-11-21

**泳道路由批次 2+泳道转正**（judge 十轮像素证据驱动收官；机械几何闸八检
全零+CLI 真几何一致）：

- **轮廓公式根修**：diamond 四面入出点公式重推导（顶 `1-|fx-0.5|`、底
  `|fx-0.5|`，左右同构）——旧公式偏心错层处落多边形内部（轴线穿本体被
  填充遮蔽）或把「左侧进入」算到右顶点（横穿整个菱形）；document 波浪底
  贝塞尔数值反解（出点贴真实波线，浮空 0.10in 根除）。
- **软穿透检查**：路由候选补 src/dst 真实轮廓（多边形/椭圆）内部穿透
  测量——端点不贴轮廓时段穿本体的豁免盲区根除。
- **路由拥塞治理（R10 批）**：全局垂直总线区间避让（|Δx|<0.16 且 y 重叠
  即拒，共线树干根除）+ 头域矩形禁区（tip 后延 0.16/±0.08，压印根除）+
  attach 槽位改**物理侧**计数（跨键同侧出入错层，头/出点重合根除）+ 强制
  键错槽重试 + 肘部走廊有界外扩+分隔带侧翼采样（窄窗跨过根除）+ 往返对
  总线分离 ≥0.16in。
- **泳道分隔带 keep-out**：沿带平行长跑候选拒绝；直连骑线平移后按真实
  轮廓重贴出入点；边标签禁跨带。
- **端点行钳制**：attach 错层过大时出入点行/列钳回 bbox 可达域。
- **泳道纵向均衡**：短列富余高度均摊到列内间隙+列底（free 精确扣除既有
  行距，内容不溢出带域）；band 底下延 0.15in（圆柱不贴画布底框）。
- **CJK 字体链确定性**：数据下划线 meta 键（_note 等模板元数据）不参与
  CJK 判定——meta 中文翻全局字体链改变拉丁测量→布局漂移根除。
- **CLI 几何边车**：`--dump-flow-routes PATH` 落盘路由/块几何快照（几何闸
  唯一真值源，进程内探针测量漂移假绿根除）。
- **折行断点**：边标签折行取最靠近中点的空格（"48 h SLA"→"48 h"/"SLA"）。
- **泳道转正**：实验性摘除（limits.md 转正说明+残项诚实边界）；泳道模板
  2 套（49→51）；data-formats subgraph 映射如实修正（分组框）。
- 测试：TestV80009 六闸（CLI 真几何审计八检 showcase+incident 双模板/
  diamond 公式锁/折行断点/转正标记/模板随包渲染）；**627 测试**。

<!-- 8.0.9 详情自 changelog.md 下沉（v8.1.0 发版，最近三版窗口滚动） -->

## 8.0.8 — 2026-11-19

**泳道已知限制文档化+回归基线**：limits.md 新增泳道专节（往返对分离/斜边端点
悬空 ≤40px/分组框空白带——均不影响 strict 判定，路由批次 2 排期后续版本）；
TestV80007 泳道回归快照（9 节点 3 泳道 showcase strict+apex 10/10+结构锁固化
基线）；621 测试。

<!-- 8.0.8 详情自 changelog.md 下沉（v8.1.0 发版，最近三版窗口滚动） -->

## 8.0.7 — 2026-11-19

**泳道修复批次 1**（visual-judge 三轮迭代，逐项像素证据）：

- **节点-标题带结构重设计**：旧公式偏移整体平移（band 底恒侵入节点 0.20in）——
  改为节点区顶=H、band 独立区间 [H+0.30, H+0.80]，间隙恒 0.30in；标题 WCAG
  反色（暗带白字实测 18.66:1）。
- **边标签**：swimlane 禁用「框行上/下+画布外远置」逃逸分支（芯片飞画布顶/底
  根除）——16-40 向螺旋扫描兜底+往返边沿走廊纵向错开（force_side）+strict
  闸内去重（同 bb 双记假撞根除）。
- **H 键轮廓贴合**：新增左右轮廓函数表（菱形顶点/IO 斜边/六边形收腰/梯形/
  斜顶）——H 键出入点 x 按实际轮廓（悬空 88-280px 同根因）。
- **其他**：骑分隔线平移（V 直连 x 落分隔线 ±0.15 → 偏 0.22）；分组框标题移
  框顶外上方（layered groups label 压节点根除）；lane 出入点吃 attach 错层；
  place 内 t=None 潜伏炸弹清除。
- 已知限制：泳道跨列回边路由（往返对分离/浮空端 ≤30px）仍在迭代——
  swimlane 维持 experimental 标注。
- **620 测试**。

<!-- 8.0.7 详情自 changelog.md 下沉（v8.1.0 发版，最近三版窗口滚动） -->

## 8.0.6 — 2026-11-19

**mermaid 导入+泳道引擎（experimental）**：

- **`--from-mermaid FILE.mmd -t flow`**（F5）：mermaid flowchart 源直接出图——形状语法 8 形态全映射（`{x}`→决策菱形、`[(x)]`→数据库圆柱、`[[x]]`→预定义子流程、`[/x/]`→IO、斜顶/倒梯形细分等）、边型五类（`-.->` dashed、`==>` thick、`<-->` 双头、`---` 无头）、管道+文本双标签形态、链式与 & 并联；subgraph 对→分组框（layered 既有已验证能力）；不支持构造（图标/图片/样式行）显式报错绝不静默丢边；-d 可省。
- **泳道布局引擎**（F3，实验性）：`layout=swimlane`+`"lanes"` 名称列表+节点 `"lane"` 归属（索引/名称），泳道背景条+标题带渲染，跨泳道边照常路由；机械闸全过（strict+apex 10/10）。视觉路由质量迭代中（judge 两轮 6 类缺陷在修）——标记 experimental，生产图建议先用 chain/layered/snake。
- 测试：TestV80006 五闸（泳道几何/归属校验/mermaid 映射/subgraph/端到端 strict×2）；**620 测试**。

<!-- 8.0.6 详情自 changelog.md 下沉（v8.0.9 发版，最近三版窗口滚动） -->

## 8.0.5 — 2026-11-18

**flow 形状语义系统**（cite-holmes 多轮研究定标：mermaid v11.3 官方形状面+Kimber 2018 学术方法图六原则；visual-judge 四轮迭代收敛）：

- **14 种语义形状**：决策菱形/数据库圆柱/IO/六边形/起止双圆/堆叠/斜切输入/人工操作/延迟/文档/预定义子流程/存储数据（+round/rect）；别名兼容；非矩形文本区内接系数+布局期自动放大；绘制内接 bbox（磁吸/闸零特判）。**边贴合锚点**：斜顶/顶点形状入出点按实际轮廓高度（悬空 80px/双向头埋框/顶边入框三类符号缺陷根除）；V lane 5 段避障走廊（穿层根除）。
- **边型扩展**：thick 粗线（2.5×可见）/bidirectional 双头/open 无头线（无留头回退）。
- **7 套学术模板**（模板库 42→49）：scRNA-seq 管线/临床决策树/细胞周期状态机/CRISPR 数据链/多中心伦理审批/双臂方法对照/PDCA 蛇形循环——全部真实学术场景语义+全元数据键。
- 测试：TestV80005 六闸（注册表别名/内接契约/边型头数/模板随包+strict 抽渲染/validate 白名单/stacked 契约）；**615 测试**。

<!-- 8.0.5 详情自 changelog.md 下沉（v8.0.9 发版，最近三版窗口滚动） -->

<!-- 8.0.4 详情自 changelog.md 下沉（v8.0.7 发版，最近三版窗口滚动） -->

## 8.0.4 — 2026-11-16

**flow 引擎顶刊精修包**（真实论文用例+独立视觉裁决四轮迭代驱动，全部机制级根修）：

- **角色化配色引擎**：主链按流程深度自动衍生同族明度阶梯（并行支路同深度
  同色），终点唯一强调色；回边断环判定（循环不再污染角色计算）；`--palette`
  注入任意色板自动获得同款分配；全显式 color 覆盖 `--palette` 时输出
  `[ignored]` 显式告知（静默无效根除）。
- **snake 环绕布局**（第三布局态）：`layout=snake`+`columns`(2-8)——列网格
  跨行对齐（换行边零偏移垂直直连）+奇数行反序；长链宽高比 ~2:1，版心缩放
  后字号保持可读。
- **路由三根修**：走廊限定两锚点间（末段从附着边外侧进线，穿框构造上不可能）；
  轴向回退（主轴向堵→换垂直轴向）；尾槽并入同侧头槽统一错层（回边尾端与
  前边头位零重合）。
- **框几何契约**：圆角框 pad 0（可视框=几何 bbox，磁吸所见即所得）；箭头
  终点负咬合（尖端止于描边外沿绝不入填充）；错层步距 0.18（同缘多箭头
  体间白隙）。
- **对齐与终裁**：行内垂直居中（异高框共轴）；layered barycenter 排序+行
  对中（主链边退化干净直降）；画布终裁按墨水包围盒+自适应边距（面积口径
  诚实占比）；数据级 `font_size`([6,40])+columns 校验前置 validate-first。
- 测试：TestV80004 八闸（角色阶梯/蛇形对齐/apex 机械断言/错层白隙/尾头
  零重合/[ignored]/font_size 边界/validate snake）；**609 测试**。

## 8.0.3 — 2026-11-16

**flow 引擎边标签系统定稿**（13 组真实场景+压力用例 strict 全过+visual-judge 多图 PASS）：

- **候选覆盖路线每段两侧**（长段优先）——不再只看最长段；自身线段白垫豁免
  （白底标签可贴自身线，graphviz 同款）；滑动搜索兜底；框行上/下+垂直引线
  标准化（fig2 PASS 形态）。
- **分层布局带标签行距预留 1.3in** + **chain 富余宽度均匀分配进列间距**
  （--width 横幅契约：内容铺满画布宽，右半不再空白）。
- **trim 尊重用户宽度**：画布=最大(用户宽, 内容宽)，内容居中不漂移。
- **箭头终点微咬合 0.02in**（尖端视觉停框缘线）+**拐点不入框验证**
  （弯在框里=judge 必抓）。
- **期刊 7pt 字号下限相对化**：min(8pt, 请求字号)——预设不再被误杀。
- 数字-单位粘行保护（48周/12.5mg 不拆行）。

## 8.0.2 — 2026-11-16

**发布文案净化重发（代码零差异）**：历史档两处内部调研来源表述与一处引擎注释
改中性价值语言（红线：公开文档只写价值不提来源过程）；来源类表述入打包禁词闸；
8.0.1 功能原样包含（flow 英寸坐标系重构+route 验证优先+边标签白底板+8 组压力用例）。

## 8.0.1 — 2026-11-16

**flow 引擎英寸绝对坐标系重构**（8 组真实场景压力用例驱动——CONSORT 两臂、期刊 7pt、
双回边、LR 分层、8 节点中文链、纯环、旧坐标混合、窄间隙长标签）：全部测量/布局/渲染
在恒定变换下（1 unit=1in，figure=内容尺寸）——测量↔范围互相污染的自引用死循环根除；
route 统一验证优先（直连→正交肘→lane 双侧×错层）；边标签白底板+框行候选标准化；
宽度实测驱动；字号下限相对化（期刊 7pt 解锁）；中断词保护。

## 8.0.0 — 2026-11-16

（v8.1.2 补写：该版本的详情节此前在多次下沉中缺失，本节据当版索引行与发布提交 03b80f3 补写，未添加其他内容。）

major·第 41 图型 `flow` 语义流程图+diagram 引擎重写（af_flow）：磁吸逐段箭头零穿框/回边 lane 绕行+虚线生效/边标签墨迹级避让（画后实测）/文本测量驱动自适应（数字-单位粘行）/画布自裁剪+`--gate strict` 三层 bbox 断言（重叠 exit 2 拒绝交付）——fig2 真实用例+中文 CONSORT 用例 visual-judge 双 PASS；42 模板；601 测试

（更正说明：索引行此前写「596 测试」，与发布提交和 v8.0.0 包内 README 徽章（tests-601）不符，按核实值记 601；索引行同一步更正。）

## 7.9.3 — 2026-11-15

**发布文案净化重发（代码零差异）**：历史存档两处内部环境称谓改中性表述；7.9.2 功能原样包含。

## 7.9.2 — 2026-11-15

（v8.1.2 补写：该版本的详情节此前在多次下沉中缺失，本节据当版索引行与发布提交 0e2bce1 补写，未添加其他内容。）

第六轮测试线批次3（门禁+覆盖欠账）：tester 建议五组验收门禁入套件（元素内文字 WCAG 对比度门/有序离散 ΔL*≥20 分离门/--explain 全量 schema 对拍/PDF 数字层抽样/dual_axis·composite·funnel 像素抽检）——schema 对拍首轮抓出 14 处 explain 缺口全补齐；596 测试

## 7.9.1 — 2026-11-15

**第六轮测试线批次2（可读性/配色家族）**：

- **热图格内数值自动反色**（AF32/AF6b）：颜色按格底色 WCAG 相对亮度选黑/白
  （cell_text_color() 单一真源）——原按数值阈值判黑白，暗底色阶 7/7 全部 <3:1
  （magma 1.00:1 隐形实锤）；diagram 块内文字（AF38，原固定白、浅块 1.2:1）共用。
- **大矩阵标注密度门控**（AF6）：auto 超 30 行/列自动隐藏格内数值+stderr 提示；
  --annot on|off 显式控制；字号自适应 9/7/6pt（原无条件逐格 9pt 死硬）。
- **--discrete 有序离散色阶**（AF43，热图）：ListedColormap 采样+BoundaryNorm
  阶梯映射+离散 colorbar——原连续 imshow 把 1/2/3 等级差压到 ΔL* 12~19。
- **--cell-edge 格线描边**（AF44，热图）：低对比色阶下保结构，edge 色随底色
  明暗自动取反（imshow 不支持 edgecolors→半整数边界 axvline/axhline 实现）。
- **定性色阶语义提示**（AF40）：Set1/2/3/Pastel/Accent/Dark2/Paired/tab10/20
  承载数值标度时 stderr 提示（colorbar 彩虹分段语义误导）。
- **热图 --theme 提示**（AF31）：显式 --theme 时 stderr 说明格色由 --cmap 决定。
- **--palette 外部配色注入**（G1 能力缺口）：hex 序列 2+；分类图按序替换主题
  系列色，热图按给定顺序构建连续色阶（浅端对齐低值）；非法 hex exit 3 精确报错；
  入通用旗标清单与 --list-flags 域表。
- **prisma 竖向箭头半截根修**（AF24）：箭头终点改用下一框实际高度 BH_BY[b]
  （原全局最大框高 BH——中文长标签使框不对称长高时箭头终点过冲钻进下一框底下
  被覆盖=「半截字形」实锤根因）。
- **slope 标签扩框入图**（AF37）：_spread 溢出的标签纳入 ylim（左端全同值时
  最下项标签掉出图框外实锤；扩框优于钳制——钳制会把多个标签挤到同点互叠）。
- **细元素可见性**（AF42）：slope 去强调线 alpha 0.32→0.45（白底可见性下限）。
- **raincloud KDE 边界裁剪**（AF27）：全正值数据密度云裁剪到数据范围
  （原尾部越过 0 伸入无意义负值区）。
- **PCA 载荷箭头色入主题**（AF33）：theme["colors"][-1]（原硬编码 #E8A33D
  琥珀+标签 #8a6414 不随 --theme）。591 测试（TestV70901 十项新锁）。

**第六轮测试线批次2（可读性/配色家族）**：

- **热图格内数值自动反色**：按格底色 WCAG 相对亮度选黑/白（原按数值阈值——暗底色阶 7/7 全部 <3:1、
  magma 1.00:1 隐形实锤）；cell_text_color() 单一真源，diagram 块内文字共用（原固定白，浅块 1.2:1）。
- **大矩阵标注密度门控**：auto 超 30 行/列自动隐藏+stderr 提示；--annot on|off 显式控制+字号自适应。
- **--discrete 有序离散色阶**+**--cell-edge 格线**（热图）：BoundaryNorm 阶梯映射+离散 colorbar
  （原连续插值把等级差压到 ΔL* 12~19）；低对比色阶下格线保结构。
- **--palette 外部配色注入**（G1 能力缺口）：hex 序列，分类图替换系列色/热图构建色阶（浅端对齐低值）。
- **双提示**：定性色阶承载数值标度语义提示+热图 --theme 格色由 --cmap 决定提示。
- **几何/主题小修**：prisma 竖箭头终点用实际框高（中文长标签半截根因）+slope 标签扩框入图+去强调线
  alpha 0.45+raincloud KDE 边界裁剪+PCA 载荷箭头色入主题。

## 7.9.0 — 2026-11-15

**第六轮测试线批次1（正确性与假警告根治）**：

- **CJK 探测回退链**：进程内加载探测脚本优先→子进程回退——agent 嵌套/嵌入式解释器
  （sys.executable 空串）旧路径静默吞错→rc=0 中文全豆腐块，根除。
- **通用字段假警告根治**：_KNOWN_DATA_FIELDS 补注册 prisma 全 schema 键+lang、km
  log_rank/risk_table、labbe events_t（顺带修 title/events_t 缺逗号连字隐性 bug）。
- **prisma 守恒校验独立化**：studies_included > reports_assessed 不可能流程无条件拦截
  （原守卫嵌套在 exclusion_reasons 分支内曾放行 200>169）。
- **校验类报错首行精确化**：以「图型: 」为前缀的 ValueError 首行直用精确原因并点名违例字段
  与实值（fc_cut=0 → "volcano: fc_cut=0 不满足 fc_cut>0"），去瞬态重试/AF_DEBUG 无关建议。
- **防错尺与精度**：nomogram 结局尺缺 points_at 显式警告（静默线性默认曾画错概率刻度）+
  DCA 峰值精度自适应（0.185/0.180 不再同显 +0.18）+色盲提示（非安全主题×≥3 系列）+
  哑铃连接线加深+ridgeline/km/volcano explain 形态补全+limits 登记 --vmax 压标度语义。

**第六轮测试线批次1（正确性与假警告根治）**：

- **CJK 探测回退链**：load_cjk_font 重构——进程内加载探测脚本优先，失败再回退子进程
  （sys.executable 非空 → python3）。agent 嵌套/嵌入式解释器场景（sys.executable 为空串）
  旧路径子进程失败被静默吞掉 → rc=0 中文全豆腐块（旗舰卖点在 agent 主路径失效）。
- **通用字段假警告根治**：_KNOWN_DATA_FIELDS 补注册 prisma 全 schema 键
  （records_identified/records_excluded/reports_excluded）与 lang、km log_rank/risk_table、
  labbe events_t——合法键不再被"不是有效字段"假警告误导（records_identified 缺了报 ERROR、
  有则假 WARNING 的自相矛盾消除）；顺带修复列表尾部缺逗号致 "title" 与 "events_t" 相邻
  字面量拼接成 "titleevents_t" 的隐性 bug（events_t 实际未注册）。
- **prisma 守恒校验独立化**：studies_included > reports_assessed（纳入数超过全文评估数的
  不可能流程）现在无条件拦截，不再依赖 exclusion_reasons 键存在（原守卫嵌套在该键分支内）。
- **校验类报错首行精确化**：以「图型: 」为前缀的 ValueError（含"校验失败"消息）首行直用
  精确原因并点名违例字段与实值（volcano fc_cut=0 → "volcano: fc_cut=0 不满足 fc_cut>0"），
  不再叠加瞬态重试/AF_DEBUG 等无关建议；volcano 约束违例逐字段点认（fc_cut/p_cut/top）。
- **nomogram 结局尺防错尺**：outcome_scales 缺 points_at 时 stderr 显式警告（静默按线性
  0~100 默认映射曾在总分上限≠100 的模型上画出错误概率刻度且不报错）。
- **DCA 峰值精度自适应**：峰值净收益显示在 2 位小数把不同真值折叠成同串时（0.185/0.180
  同显 +0.18，读者误判两模型等价）逐级升位到 3/4 位。
- **色盲安全提示**：非色盲安全主题×≥3 系列时 stderr 一行提示（建议 --theme okabe-ito）；
  默认主题 glm-brand 不变（品牌视觉），主题字典如实标注 colorblind_safe=False。
- **可读性小修**：哑铃图连接线 #BBBBBB→#999999（细元素亮度）；--explain ridgeline/km/
  volcano 形态补全（datasets 字典结构/患者级原始数据形态/轴标覆盖）；limits 登记 --vmax
  压标度语义。581 测试（TestV70900 九项新锁）。

## 7.8.2 — 2026-11-14

**第五轮复测修复（AF17-AF20）**：

- **AF18**：rob 摘要条数值标签从段内两行改为**条带上方单行**（每域最大段 ≥15%）——
  段内两行在薄条带里被相邻段裁切/重叠（复测实锤；ylim 反向轴上下语义同步校准）。
- **AF19**：`--explain rmst` τ 口径校准——缺省=**最小**最大随访之半（此前误写
  「最大随访之半」，一字之差 ΔRMST 26 天/结论可翻转）。
- **AF20**：自动 τ 渲染追加 stderr 提示「ΔRMST 结论对 τ 敏感时请以 --rmst-tau
  在多个随访阈值复核」（同一数据 τ=1000 与 τ=1607 的 P 值可跨越显著线）。
- **AF17 产品面**：limits 登记 PDF 文本层 CJK 提取环境相关（matplotlib 字体子集
  ToUnicode 差异）；回归测试改双层断言（PDF 只断数字形态+图例 CJK 内容改图对象
  内省——Text artist 恒持真 unicode，环境无关）。

<!-- 7.8.2 详情自 changelog.md 下沉（v8.0.9 发版，最近三版窗口滚动） -->

**第五轮复测修复（AF17-AF20）**：AF18 rob 摘要条数值标签移条带上方单行（段内两行
在薄条带被裁切/重叠实锤；ylim 反向轴语义校准）；AF19 --explain rmst τ 口径校准
（缺省=最小最大随访之半）；AF20 自动 τ 渲染追加 τ 敏感性复核提示；AF17 产品面
=limits 登记 PDF 文本层 CJK 提取环境相关（回归测试改双层断言：PDF 只断数字形态+
图例 CJK 内容走图对象内省——环境无关）。571 测试。

## 7.8.1 — 2026-11-14

**测试线四图型深测修复（AF9-AF16，外部独立实现逐位核对后目检发现）**：

- **AF11（P1）比值类 CI 格式化门**：L'Abbé 图例把 RR 上界 0.997 舍成 1.00——而
  RR 无效值恰为 1，读者会判「CI 含 1、无显著」与引擎结论相反。新增
  `fmt_ratio_ci` 自适应格式化（任一边界舍入后==无效值即升三位+「不含 1」显著
  标注），应用 L'Abbé 图例/forest Overall/forest 逐行三处；funnel/galbraith
  用有效数字格式不受影响。
- **AF9 隐式旗标不冒充**：品牌主题自动开斜纹后非 bar 图误报 `[ignored]
  --hatch`（用户从未传过）——隐式置位打标记、域检查跳过；`--hatch` 支持
  `on|off` 取值，`--hatch off` 显式关闭品牌默认斜纹（此前 argparse exit 2）。
- **AF12 rob 摘要条图内数值**：每域最大段标注 百分比+计数（≥15%；多段全标
  会在薄条带互挤——每域单标方案），计数明细保留 stderr。
- **AF13/AF15**：L'Abbé 气泡面积图内注（∝研究权重）；rmst 双臂面积 alpha
  0.15→0.22+第二臂斜纹（两臂面积一眼可归）。
- **AF16**：`--explain` 补齐 slope/volcano/rmst/labbe（此前输出泛指文档）。
- AF10（错误首行泛化）/AF14（L'Abbé 引线避让）P3 记录在案缓办；rob 摘要等权
  为设计决策非权重缺口。

**测试线四图型深测修复（AF9-AF16）**：AF11（P1）比值类 CI 格式化门——L'Abbé
图例 RR 上界 0.997 舍成 1.00 致临床判读反转（RR 无效值=1），`fmt_ratio_ci`
自适应升三位+「不含 1」标注，应用 labbe 图例/forest Overall/逐行三处；AF9 品牌
隐式 hatch 置位不冒充用户输入（非 bar 图不再误报 [ignored] --hatch）+`--hatch
on|off` 逃生门；AF12 rob 摘要条每域最大段图内标注（百分比+计数）；AF13 L'Abbé
气泡面积注；AF15 rmst 双臂面积 alpha 0.22+第二臂斜纹；AF16 --explain 补齐
slope/volcano/rmst/labbe。AF10/AF14 P3 记录缓办。rob 摘要等权为设计决策
（docstring 明示）。571 测试。

## 7.8.0 — 2026-11-13

**方法论批（文档批+引擎批同版）**：五点图约（出图前 5 问，写不出核心结论不出图）、
反冗余三层递进审计（Overview/Deviation/Relationship+5 陷阱+4 问）、主面板规格
（1.35:1+accent 唯一+3 秒结论）、叙事排序 5 规则、语义配色角色表（6 色+6 规则，
advisory 层）、审稿返修案例库 10 案（标注社区汇编未溯源）、审稿人模拟 5 镜头、
问题优先门（有数据没问题先反问）、交付命名约定。引擎批：composite `hero_panel`
字段（1.35:1 双列+跨全行，3-6 面板，>6 回退）+scatter >50K 分层栅格化
（数据层栅格、轴文字保矢量；与 cluster_heatmap 降采样互补——一个改数据一个改渲染层）。
全部文档经统一口径审校（字号/默认值以引擎实测行为为准，自相矛盾处以实测覆盖）。

**方法论批（文档批+引擎批同版）**：五点图约（五问预检仪式）+反冗余三层递进
（Overview/Deviation/Relationship 正交编码+5 冗余陷阱+排版前 4 问）+主面板规格
（1.2–1.5×辅面板面积/accent 高饱和全图唯一/3 秒结论；引擎 width_ratios [1.35,1.0]
双列+hero 跨全行，3-6 面板，>6 WARNING 回退均等）+叙事排序 5 规则（数据先于示意图）
+语义配色角色表（#2166AC 蓝=对照/#B2182B 红=疾病慎用/#1B7837 绿=获益/#F1A340 橙/
#762A83 紫/#999999 灰=不显著；6 规则含红绿必须冗余编码、限饱和面积、禁 jet 系）
+审稿返修案例库 10 案（相关矩阵 mask 三角填灰/单图>4 色降 3 色+线型/灰度打印检查/
小样本叠原始点/火山阈值线必画等；头部标注社区汇编未溯源）+审稿人模拟 5 镜头
（must-fix/suggestion 分级）+问题优先门（数据无问题先反问）+交付命名约定
（fig1_内容.pdf/fig2a_面板级/figS1_补充）。引擎批：composite hero_panel 字段+scatter
>50K 分层栅格化（与 cluster_heatmap --downsample 互补：一个改数据一个改渲染层）。
全部文档经统一口径审校；以下建议经评估不采纳（COPY-FIRST 资产复用/LLM 自检 QA 主体/数据
显著性闸门[阴性结果是合法科学结论]/R 双栈/300dpi 降档/journal-intel 未核实不采）。

## 7.7.2 — 2026-11-13

**测试线差量方案落地（AF1+AF2，2026-11-13 差量补测改进表）**：

- **AF1 `--data` inline 简写**：`-d "A=10,B=8,C=5"` 免临时文件出图（单系列，等价
  labels+series value；int/float/负数/中文名均可）。规则收紧=整体匹配「名称=数值
  (,名称=数值)*」才当 inline 解析——坏文件名的原报错路径保持不变，错误即教材不劣化。
  `--data` help 与 `--explain bar` 同步。
- **AF2 套件里程碑输出**：`tests/run_tests.py --verbose` 逐测试打 `[i/总数]+时间戳`，
  结束打 DONE 摘要（passed/failed/errors/skipped+总耗时）；支持类名/方法名定位子集。
  默认行为不变（CI 与既有脚本零风险）——横向共性①（PP1 同源）的 AF 侧落地。
- SKILL.md 瘦身按主看板 6 措施为准（待用户批准后实施，v7.8.0 候选主轴）。

**测试线差量方案落地（AF1+AF2）**：`--data` inline 简写 "A=10,B=8,C=5"（免临时文件；
规则收紧=整体匹配名称=数值才解析，坏文件名原报错不变；int/float/负数/中文名均可；
单系列系列名 value）；run_tests.py --verbose 里程碑输出（[i/总数]+时间戳+DONE 摘要，
支持测试名子集定位；默认行为不变 CI 零风险，横向共性①AF 侧落地）。554 测试。

## 7.7.1 — 2026-11-12

**收尾修复+契约升级（外部实测反馈驱动）**：v7.7.0 发布后外部实测抓到四处收尾遗漏，全部修复并升格为机械契约——

- **`--list-themes` 陈旧默认标记清正**：v7.6 默认切 glm-brand 时 glm 行仍写「素雅莫兰迪风
  （默认）」，误导选型回旧默认；现 glm-brand 携带唯一「（默认）」标记。
- **扫描器 3d 规则**：THEME_SWATCH_DESCRIPTIONS「（默认）」标记全库恰 1 处且必须等于
  resolve_theme(None) 真值（AST 对拍）——此类收尾遗漏从「靠人记」变「闸拦截」。
- **frontmatter date 入升版链**：af_release bump 同步刷 date；新增 date↔changelog 版本
  节日期一致性锁（v7.7.0 date 停 11-07 实锤防回潮）。
- **默认竞技场像素契约锁**：冠军色/三彩循环/灰基线逐色像素断言（视觉默认不再只有
  行为级 stderr 锁）。
- **基线加冕提示**：基线关键词柱（人类/baseline）为最高柱被自动加冕时 stderr 明示
  （出口：--arena "名称" / --arena off）；limits 同步说明。
- **trunk git 卫生**：恢复快照提交（v5.7.1→v7.7.0 单锚）+每版一 commit 入发车清单。

**收尾修复+契约升级（外部实测反馈驱动）**：--list-themes glm 行「（默认）」陈旧标记
清正（v7.6 默认切 glm-brand 漏改）+扫描器新增 3d 规则=THEME_SWATCH_DESCRIPTIONS
「（默认）」标记全库恰 1 处且=resolve_theme(None) 真值（AST 对拍）；frontmatter date
入 af_release 升版链+date↔changelog 一致性测试锁；默认竞技场像素契约锁（冠军
#0F8A6D/三彩循环/灰基线逐色断言）；基线关键词柱被自动加冕时 stderr 提示；trunk git
快照恢复+每版一 commit 卫生入发车清单。548 测试。

## 7.7.0 — 2026-11-12

**bar 单系列默认竞技场风格（默认输出=最佳输出第二期）**：v7.6.0 把品牌主题下沉为
引擎默认后，本版把基准对比场景的核心视觉同样机制化——

- **单系列竖向 bar 零参数即得竞技场风格**：per-bar 异质填充循环（橙白斜纹/蓝白
  点纹/紫白斜纹）+冠军柱实心深青绿+金色皇冠+数值加粗，冠军=最高柱自动加冕；
  stderr 提示冠军与来源（默认竞技场风格/--arena）。
- **`--arena off` 显式逃生门**：负面指标（最高=最差，如错误率/不良事件率/死亡率）
  不宜自动加冕，一参数回到普通柱状图；`--pub-ready` 投稿流自动规避竞技场默认
  （投稿图表走色盲安全主题）；`--alternate` 显式指定风格时优先生效；多系列/
  横向 bar/单值 bar 不受影响且无提示噪声。
- **`--suggest` 榜单配方路由**：bar 类推荐附带「基准榜单场景推荐 `--style sketch`
  手绘风」提示——大模型榜单速览图的标准配方固化为一句话（数据当期快照+来源
  上图 source_note 属数据纪律，见场景卡卡14）。
- SKILL 双语/cheatsheet/limits/antipatterns/CHART_NOTES/域表六处同步；SKILL 双语
  「近期版本行」陈旧修正（原停留 v6.7.0）；TestV70700 十项锁（默认启用/off 逃生门/
  多系列静默/单值跳过/alternate 优先/pub-ready 规避/suggest 提示/文档同步）。

**bar 单系列默认竞技场风格（默认输出=最佳输出第二期）**：单系列竖向 bar 零参数即得
per-bar 异质填充循环（橙白斜纹/蓝白点纹/紫白斜纹）+冠军柱实心深青绿+金色皇冠+数值
加粗，冠军=最高柱自动加冕，stderr 提示冠军与来源。`--arena off` 显式逃生门（负面
指标最高=最差不宜加冕）；`--pub-ready` 投稿流自动规避竞技场默认；`--alternate` 显式
风格优先；多系列/横向/单值 bar 不受影响且无提示噪声。`--suggest` bar 类推荐附带
「基准榜单场景推荐 --style sketch 手绘风」配方提示。SKILL 双语/cheatsheet/limits/
antipatterns/CHART_NOTES/域表六处同步；SKILL 双语近期版本行陈旧修正（原停留 v6.7.0）；
TestV70700 十项锁。

## 7.6.0 — 2026-11-08

**默认出图=品牌视觉（机制变更）**：此前零参数默认主题为 `glm`（素雅莫兰迪），
其他 agent/用户按最短路径调用（只传必需参数）得到的是朴素图——美观效果依赖
文档引导显式传参，靠不住。本版把品牌效果下沉为引擎默认：

- **零参数默认主题 `glm` → `glm-brand`**（信号黄×深钢蓝），**品牌斜纹随品牌
  主题自动开启**（斜纹=品牌组成部分非可选项）——最短路径调用即得黄蓝双斜线
  品牌图。
- 投稿色盲安全场景保留 `--theme okabe-ito` 逃生门；全部显式主题行为不变
  （别名解析/金标结构基线 40/40 实测零漂移）。
- 文档（SKILL 双语默认声明/cheatsheet/--list-themes 注记）与 `--suggest`
  输出同步；新增 TestV70600 两项锁（默认主题解析+零参数真渲染 smoke）。
- 测试 531→533。

## 7.5.0 — 2026-11-07

新功能 `--arena` 基准对比竞技场风格 + 一致性扫描器跨行命令修复：

- **`--arena [冠军]`（bar 单系列竖向）**：基准/模型/方法对比一键出「竞技场」视觉——
  每根柱异质填充循环（灰实心/橙白斜线/蓝白点纹），冠军柱实心深青绿+柱顶金色皇冠
  +数值加粗高亮。`--arena` 自动选最高柱，`--arena "名称"` 按类别标签指定冠军
  （如论文方法名）；域外图型/横向/多系列均 `[ignored]` 显式告知。
- **跨行命令一致性扫描**：check_consistency 此前按单行提取文档命令，反斜杠续行
  命令的旗标落在第二行时逃逸旗标域检查——本次修复后当场抓到场景卡
  「bar×--stats auto」矛盾（bar 是聚合数据不做自动检验，已改为 --sig-bracket
  comparisons 通道）与 SKILL subgroup 示例的 --cox-* 域表缺口（引擎实为一键
  拟合复用同参，域表扩 forest+subgroup 对齐）。
- **真实数据样例**：`examples/example_arena.json`（OSWorld 基准论文公开数字，
  arXiv:2404.07972 Table 5 可达性树口径+人类基线）+场景卡新增「基准对比竞技场」卡。
- 测试 526→531（+TestV70500 五项：arena 渲染与冠军通知/域外告知/场景卡锁/
  扫描器跨行机制锁/样例数据真值锁）。

## 7.4.1 — 2026-11-07

hotfix（引擎代码与 7.4.0 零差异）：

- **包内测试套件镜像适配**：新增的 `--stats` 域一致性锁中，读取 SKILL_ZH.md 的
  断言在无独立中文文件的分发形态（SkillHub 包/GitHub 公开镜像）下会直接报错——
  拆分为独立用例并挂镜像自动跳过（正本完整环境仍全量执行）。
  修复 7.4.0 包内运行测试套件会报 1 个 error 的问题。
- 测试 525→526（中文档锁拆分为独立用例）。

## 7.4.0 — 2026-11-07

文档口径统一大扫除（准确性审查发现的四处不一致全收）+ 引擎小修：

- **期刊宽度交互**：antipatterns.md 曾写「先 journal 后 width 可覆盖（顺序敏感）」，
  与引擎行为（`--journal` 锁宽、`--width` 被忽略并 `[auto]` 告知、`--height` 仍生效）
  表述相反——纠正为与 SKILL/limits/引擎三方一致（与给参顺序无关）。
- **`--stats` 适用域五处对齐权威域**：SKILL 双语与 limits 统一为
  `auto|multi|bootstrap` → box/violin/raincloud、`cox` → forest/subgroup；
  域外一律 `[ignored]` 显式告知后继续渲染（limits 曾误写「fatal 校验 exit 1」，
  实际行为是 `[ignored]`+exit 0）。
- **tests 自述计数**：套件头部说明与计数锁 docstring 更新为当前真值
  （15 smoke 图型、40 模板、realworld 18）。
- **examples/README 目录对拍**：逐图示例表补齐至 13 个 example_*.json、
  realworld 表补齐至 18 个（此前只列 5+4 个，与包内实际不符）；
  gallery README 首句语病修复。
- **引擎修复**：`--journal` × `--width` 同给时 `[auto]` 锁宽提示曾打印两次
  （重复代码块）——去重为一次。
- **机制防回潮**：新增 TestV70400 五项锁（期刊宽度真口径 / --stats 五处域同步 /
  examples README 逐文件覆盖 / `[auto]` 提示唯一性 / tests 自述计数真值）；
  测试徽章 520→525（README 徽章动态互锁自动对账）。

## 7.3.0 — 2026-11-06

包内输出样例 + 口径统一：

- **SVG 矢量预览随包**：`examples/gallery/` 新增三张 `*_preview.svg`
  （Mayo PBC KM/卵巢癌 RCT KM/Fleiss 1993 L'Abbé，150dpi 矢量，可直接查看）——
  包内自此既有可复现输入（JSON+命令）也有生成成品样例。
- **口径统一**：SKILL 双语「三条最常用边界」行补全 `--height` 有效
  （与 limits/quickstart/能力表三处口径一致）。
- **提示词卡自洽**：基线对比 bar 卡的用户话术改为「p 值已算好放进 comparisons」
  （bar 是聚合数据不能自动检验——话术与应产出不再矛盾）。
- **统计责任提示**：`--sig-auto` stderr 新增「检验假设（样本独立性/随机抽样）
  请自行确认；论文引用时请报告所用检验方法与各组 n」——自动检验不替用户承担
  统计设计责任。

## 7.2.1 — 2026-11-05

发布文案清净化重发（代码与 7.2.0 零差异）：

- 7.2.0 版本详情文案含不宜表述，未过平台安全审核——中性化改写重发；
  并新增机械锁：changelog 主文件禁同类表述（历史存档豁免不回改），
  纳入 check_consistency 扫描面。

## 7.2.0 — 2026-11-05

一致性扫描器 v2 + 安装/预览体验收口：

- **扫描面扩到引擎源码**：`check_consistency.py` 自此扫描 `scripts/*.py` 的运行时
  文案（CHART_NOTES 等 `--explain` 输出字典；注释/docstring 属历史描述豁免）——
  准确性审查发现的 `af_shared.py` bar 文案旧口径即此类（文档已更新而引擎
  --explain 输出仍沿用旧表述，一句话与实现脱节）。文案已更新为双通道真相
  （JSON errors 或 CSV 后缀列 v6.0+）。
- **MCP 安装本地优先**：mcp/README 安装顺序反转——`pip install -e <包目录>/mcp`
  （清华/阿里镜像）升为默认推荐，uvx git 直跑降为国际网络备选。
- **视觉样例库直链**：SKILL 双语能力表与 README 的 gallery 行直挂 GitHub 仓库
  预览链接（包内为可复现 JSON+命令，成品图在仓库一键可看）。

## 7.1.0 — 2026-11-04

命令一致性与文档可信度继续收口（自动一致性检查机制化）：

- **新工具 `scripts/check_consistency.py`**：全部命令载体（模板/真实场景 `_command` +
  文档代码块共 118 条）× 能力注册表（旗标域表 + `--verify` 仅 PDF 规则）逐条校验，
  另扫 CSV 误差旧口径残留——有发现 exit 1，发车闸直接可挂。本版首跑清出 15 处
  历史混用：9 处模板/真实场景命令带 `--verify` 却输出 PNG（该门禁仅对 PDF 生效）、
  提示词卡柱状图示例误用 `--stats auto`（聚合数据不可自动检验——正确通道=
  `comparisons` + `--sig-bracket`，或原始数据 `-t box --sig-auto`）、反模式页与
  SKILL 双语能力表的 CSV 表述过时。
- **域表真值化**：`--stats` 的旗标域补齐 raincloud（auto|multi 合法域，此前域表漏列）
  与 subgroup（cox 合法域）——`--list-flags` 输出自此与参数门禁完全一致。
- **ADR-0001 状态如实化**：Proposed→Partially adopted（af_resilience/af_shared/
  wrapper 通路已落地；af_draw 拆分继续推进）。

新工具 `scripts/check_consistency.py`：文档与能力注册表自动一致性检查
（118 条命令载体×旗标域表+--verify/PDF 规则+CSV 口径扫描；exit 1 发车闸）。
首跑清出 15 处历史混用（9 模板 --verify+PNG/prompt-cards --stats auto 误用/
域表 --stats 真值化+raincloud+subgroup/antipatterns+SKILL 双语 CSV/ADR
Proposed→Partially adopted）。511 项测试。金标=DRS retinopathy KM
（R survival 394 眼两臂，新数据集）。

## 7.0.0 — 2026-11-03

major：全自动组间显著性 + 文档可信度大扫除：

- **新功能 `--sig-auto`**（box/violin/raincloud）：不传 comparisons 也行——引擎自动
  两两检验（Shapiro 判常态：双常态组 Welch t，否则 Mann-Whitney U）并画分层
  bracket+星号。检验家族与 `--stats auto` 一致；聚合图（bar 系）不适用并显式告知
  （用 comparisons + --sig-bracket 传自己的 p 值）。
- **文档可信度大扫除**（准确性审查逐条收口）：`quickstart` CSV 误差旧限制残留与
  SKILL 决策树 JSON-only 提示纠正为 v6.0 后缀列真相；README 分发形态表述如实化
  （中文版=SkillHub 包 SKILL.md，无独立 SKILL_ZH.md 文件随包）；`openpyxl` 入
  正式依赖（--sheet Excel 直读自此声明完备）；MCP 子目录 wheel 包声明如实化
  （引擎随包根 scripts/ 提供，不再虚列 af_engine）。
- **版本历史补全**：6.9.0 节补写（该版 --sig-bracket 与文档收口，此前发版漏记）。

major：新功能 `--sig-auto` 全自动组间显著性（box/violin/raincloud 自动两两
检验 Shapiro→Welch t / Mann-Whitney U+分层 bracket；聚合图 ignored 指路）
+文档可信度大扫除五件（README 分发形态如实化/quickstart+SKILL 决策树 CSV
真相/openpyxl 依赖/pyproject 如实/版本历史补全）。504 项测试。

## 6.9.0 — 2026-11-02

新功能 `--sig-bracket` 组间显著性括号 + 文档准确性收口：

- **`--sig-bracket`**：数据携带 `comparisons=[{a,b,p}]` 任意比较对（p 值来自用户
  自己的检验，引擎只可视化）即自动画分层 bracket+星号（<0.05/<0.01/<0.001，
  NS 显式标注）；分层布局按区间重叠最低层分配（span 长的在底层，共享端点判撞）；
  bar/grouped_bar/box/violin 四图型可用。
- 文档准确性收口：MCP 工具清单补 `query_capability`、README 中文文档描述纠正、
  MCP 安装新增不依赖 GitHub 的本地路线、版本历史标注当前版本。

新功能 `--sig-bracket` 组间显著性括号（comparisons 任意比较对+分层防重叠
+bar/grouped_bar/box/violin；分层布局=区间重叠最低层分配，共享端点判撞）
+文档准确性四处收口（MCP 工具清单补 query_capability/README 中文文档描述
纠正/MCP 安装新增不依赖 GitHub 的本地路线/版本历史标注当前版本）。
494 项测试。金标=PlantGrowth scipy ttest_ind 真值（NS/*/ ** 三 bracket
全链机械对拍）。

## 6.8.0 — 2026-10-31

MCP 能力透明化 + CSV 误差能力文档真相化（准确性审查逐条收口）：

- **MCP 新工具 `query_capability`**：一命令查图型能力面——chart 留空=全图型
  清单+每旗标域适用图型速览；指定图型名=该图型专属/域外旗标（[ignored] 预告）。
  动态真值=引擎 --list-types / --list-flags，MCP 能力面自此与引擎注册表零漂移。
- **CHARTS 内置回退清单补齐 + 快照锁**：v5.7 时代快照缺 labbe/rmst/rob 三图型
  （引擎可达时被运行时刷新掩盖，静态读源码即见缺口）——补齐至 43 键，并新增
  AST 快照锁（内置清单必须与引擎注册表逐键一致，回退清单从此不可能漂移）。
- **CSV 误差能力文档真相化**：v6.0 已实现 CSV 误差列（`X_se`/`X_sd`/`X_sem`/
  `X_err` 后缀列自动配对），但 FAQ 两处、data-formats 三处仍写「CSV 不支持
  误差棒」，引擎 stderr 两处 hint 同样与自身行为矛盾（同屏打出旧文案+成功
  识别误差列）——全部改写为准确表述，测试锁防回潮。
- **守卫扩容**：计数守卫清单纳入 mcp/pyproject.toml（英文描述曾漏网），正则
  容忍英文修饰语结构（「N publication-grade academic chart types」类）；文档
  内「第 N 种图型」历史序号改为「第 N 号图型」（编号保留，不再与总量口径混淆）。
- **品牌斜纹补齐**：glm-brand 单系列柱状图不再豁免斜纹（斜纹是品牌组成部分
  非可选项）；其他主题显式 --hatch 单系列豁免时改为 [ignored] 显式告知
  （不再静默失效）。
- **show-values 精度自适应**：数值标签随系列数据小数位显示（cap 3 位）——
  固定 1 位小数曾把 5.032 显示成 5.0（视觉门机械断言抓获，交付链回归锁）。

## 6.7.0 — 2026-10-31

`--list-flags` 旗标域查询（实质新功能）+ 官方点名四项收口。

- **`--list-flags [TYPE]`**：一命令查某图型的专属旗标与域外旗标（[ignored] 预告），
  无参数=全图型速览；别名可达（survival→km）。旗标域注册表与 argparse 及图型
  注册表**测试互锁**（域内图型必须是真实注册图型、旗标必须存在于 argparse）——
  自此注册表不可能与引擎漂移。
- **收口**：SKILL 双语「37」残留×5（含 Section Nav 锚链接 `37-chart-types`——
  守卫正则自此覆盖连字符变体）；gallery 改为 JSON+README 随包（PNG 仅 GitHub/
  CH），File Index 指针不再死链，打包器新增死链断言；Python 下限统一 3.8
  （FAQ 3.9→3.8，与 frontmatter/README 对齐）；changelog 版本索引表格解挤压
  （一版本一行）；README 测试徽章与套件数**动态互锁**（徽章数==def test_ 计数）。

## 6.6.0 — 2026-10-30

一致性清剿第二轮（accuracy/usability 4.6 官方点名逐条收口）：

- **MCP**：server.py 头注释旧计数与 render_chart 文档、提交文档
  MCP_SUBMISSION.md 旧计数 → 全部 40（随引擎注册表）。
- **SKILL**：文件索引与代码布局两处旧计数 → 40；quickstart 旧计数 → 40。
- **limits.md**：四组旗标的「静默忽略」描述纠为实际的 `[ignored]` 显式告知行为
  （v3.6 起的真实行为，文档描述自此与代码一致）；并新增活文档禁「静默忽略」
  机械锁（历史存档豁免）。
- **守卫扩展**：计数扫描扩至 14 份活文档，正则覆盖裸 `types` 与「种学术图型/
  种投稿级学术图表」口径——上一轮漏网的全部口径自此入闸。

## 6.5.0 — 2026-10-30

文档一致性大扫除（准确性审查逐条收口）+ 视觉样例库。

- **计数口径统一**：cheatsheet、SKILL 文件索引、mcp/README 的旧计数与自相矛盾
  表述——全部统一为 40（随注册表）；引擎头注释
  v2.0.0→随版同步，并新增「头注释版本==SKILL 版本」测试锁（bump 从此不漏）。
- **守卫扩展**：mcp/README.md 与 cheatsheet.md 纳入计数扫描清单；正则覆盖
  「种投稿级学术图型」口径。
- **视觉样例库 `examples/gallery/`**：3 例真实公开数据成品图（Mayo PBC 队列 KM/
  卵巢癌 RCT KM/Fleiss 1993 L'Abbé），150dpi 缩略+可复现 JSON+命令——
  每例统计值经独立实现互拍与视觉验收。

## 6.4.1 — 2026-10-29

KM 统计框标签动态降级 + 交付验收逮漏修复：

- **中位生存标签诚实化**：任一组 CI 不可估（小样本/未到达）时标签自动从
  「中位生存（95%CI）」降级为「中位生存」——标签与内容一致；全组可估时保持
  原标签（pbc 等大样本回归验证不变）。
- log-rank p 与显著性标记之间加分隔空格（「0.303NS」→「0.303 NS」）。
- **CI 镜像测试自适应补漏**：v6.4.0 新增测试类漏挂 MIRROR skip（读 SKILL_ZH.md）
  致 GitHub CI 首次红灯——守卫类装饰器补齐。

## 6.4.0 — 2026-10-29

`--debug` 结构化失败诊断侧车（交互式排障落地）+ 文档密度守卫。

- **`--debug`**：渲染失败时写 `<output>.debug.json`——输入文件指纹（sha256 前缀/
  大小）、字段映射（fields_seen 与白名单外的 fields_unknown 名单）、异常分类与
  中文修复建议、重试代数。供 agent/脚本程序化排障；成功渲染不产出；不加旗标
  行为零变化（侧车自身失败不覆盖原退出码）。
- **文档密度守卫锁**：SKILL 双语 ≤33000 字节 + 近期版本行 ≤700 字符——
  版本历史堆砌曾把近期行推到 6.7KB（渐进披露退化），此后任何膨胀由测试拦截，
  历史一律下沉 changelog。
- 本版瘦身：SKILL 双语近期行 6742/3354 → 546/302 字符（各 -6KB）。

## 6.3.0 — 2026-10-27

新图型 #40：`labbe` L'Abbé 图（Meta 四件套收官：forest / funnel / galbraith / labbe）。

- 2×2 四格表（`events_t/n_t/events_c/n_c`）的处理组 vs 对照组事件率散点；
  对角线 = 无效应线（RR=1），DL 随机效应合并 RR 参考线，点面积 ∝ 研究权重，
  一眼判读：对角线上方=有害、下方=有益、离合并线远=异质性嫌疑。
- **骑线/夹缝点自动引线标注**：RR 贴合并线、两线夹缝的点贴位必撞参考线，
  自动改带细引线远置标注（归属清晰不悬空）；普通点朝远离合并线方向标注；
  紧凑避让（小步长贴点，不产生大位移漂移）。7 轮视觉验收对抗沉淀。
- `--suggest` 识别 2×2 四格表结构（与 funnel 的 effect/se 契约互斥不混淆）。
- 金标：Fleiss 1993 阿司匹林 7 RCT（realworld `cardio_fleiss93_aspirin_labbe`）——
  合并 RR=0.873（95%CI 0.764~0.997）与独立手写实现逐位互拍；
  MH 固定效应 OR=0.89 复现文献发表值 ≈0.90；I²=40%。
- 校验：四格表非法（事件>总数/n≤0）exit 3；<3 研究拒绝；零事件格剔除合并并告警。

## 6.2.0 — 2026-10-27

渲染稳定性双修（此前只有「建议重跑」的文字，无机制）：

- **瞬时失败自动重试**（`--retries`，默认 1）：渲染看门狗超时/内存耗尽（exit 5/6）
  自动以原参数重跑，每代看门狗预算放宽 ×1.5，stderr 透明记录重试代数；重试成功
  按最终退出码上报（成功=0），输出与一次成功逐字节一致（测试锁）。重叠/数据/环境
  等确定性错误不重试（重跑无意义）；`--retries 0` 关闭。进程级重试=状态零残留。
- **`--timeout 0` 语义收紧**：0 现在禁用自适应预算（30~1800s）但保留 7200s 硬保险，
  不再有完全无界的渲染；负数预算直接报错（exit 1）并指引。`AF_NO_WATCHDOG=1`
  仍可完全关闭（维护者逃生门，语义不变）。
- **看门狗小预算精度修复**：监控步长跟随预算（此前固定 1s 采样，<1s 预算永不触发）。
- 错误诊断建议与机制对齐：不再提示手动「重跑一次」，改为说明自动重试已内置。

## 6.1.1 — 2026-10-26

rob 判定扩展+出厂前逮漏：「Very high/critical」新增极高独立档（深红 V，
ROBINS-I 数据完整渲染）；「Unclear」归入顾虑档（ROB1 旧措辞，黄色警示档）；
摘要堆叠顺序 L→S→H→VH→NI；图例只列在场类别——修掉循环变量泄漏（在场判定
误用外层循环残留域键，实际只扫最后一个域）；图例下移避开旋转域标签（逐格
视觉审核逮住遮挡）；domains/judgements/title 入字段白名单。随包三个官方
工具真实数据示例（robvis 包：data_rob1 9×7、data_robins_e 10×7 含极高档、
data_quadas 12×4）；三图经逐格矩阵审核（72/80/60 格 diff=0）。

## 6.1.0 — 2026-10-26

偏倚风险交通灯图（第 39 图型，robvis 同款）：研究×域网格（判定中英同义词
均可）+各域摘要占比条；Overall 列入网格不入摘要；配色固定语义。另将
「谁拟合、谁可视化」三层能力矩阵写入双语 SKILL 正文（明确 subgroup
--stats cox 即引擎拟合、nomogram/rcs 仍为可视化路径），--suggest 新增
rob 结构与原始 time/event/group 长表识别。真实示例=robvis 包数据（9 项研究）。

## 6.0.0 — 2026-10-24

CSV 误差列约定（官方评测点名缺口收口）：列名 `X_se/X_sem/X_sd/X_err`
自动配对主列 X 画误差棒；`X_sd`+`X_n` 自动换算 SEM=sd/√n；孤儿列告警
并按普通数据保留；`--csv-no-errors` 逃生门；无后缀常规 CSV 零变化。

> 本文件为完整双语版本历史；主文档只保留最近三个版本。

## 5.9.2 — 2026-10-24

发布卫生：内部发布清单文档（docs/RELEASE_CHECKLIST.md，含内部工具名与
运维流程）误入 5.9.1 包——打包器泄漏红线正确拦截，但发车链管道 `| tail`
吞掉了非零退出码导致照发（教训已固化：打包步骤禁管道吞码）。本版移除该
文件，无代码变化。

## 5.9.1 — 2026-10-24

cif `cause_labels` 键一致性守卫：错码（数据中不存在的事件码）→ exit 3
可搜索中文报错；在场的竞争码缺标签 → 默认名+stderr 软提示。全谱审计
（10-24）确认引擎三类标签配对方式中唯一键间接映射点（cause_labels）
无守卫，同日补防。电池 TestV50901 三态锁（错码/缺标/正常）。

## 5.9.0 — 2026-10-23

rmst 限制平均生存时间（第 38 图型）：每臂 RMST(95%CI)=KM 阶梯积分到 τ
（Greenwood 型方差 Var=Σ(RMST(τ)−RMST(t_j))²·d_j/(Y_j(Y_j−d_j))，Y−d=0 项
跳过），两臂 ΔRMST 差值 CI（SE=√(V₁+V₂)，正态近似 p=erfc(|Z|/√2)）。
数据契约同 km（groups 原始对，恰好两臂）；--rmst-tau 或自动 τ；随访不足
平尾外推+覆盖率标注。守卫：τ 正数、两臂、组≥5 对（渲染层）、时间非负。
金标：手算 6 点恒等式（RMST 2.0/7-3，Var 2/9 与 8/27）+独立循环第二实现
+colon 真实队列 619 例全表。双实现对拍逮住两个出厂前 bug：①方差循环未按
τ 截断（混入 t>τ 垃圾项）②未排序输入事件表错位（unique first_idx 与
reduceat 顺序）。渲染：阶梯 S 曲线+阴影 AUC+τ 竖线+推断注释框。

## 5.8.0 — 2026-10-23

`subgroup --stats cox` 一键亚组拟合：逐层 Cox HR(95%CI,p)（Efron 核）+似然比
P 交互（含/不含 trt×层指示项的 2Δloglik，χ²，df=层−1）+Overall。旗标
--subgroup-vars/--treatment/--cut/--cox-cols。守卫：层内 n≥10、2~8 层、处理臂
恰两取值（数值/文本双分支）、处理臂不得兼任亚组、连续列须 --cut。文本层
保数据出现序（尊重临床因子惯例）、数值层排序。veteran 真实队列全表金标
（tests/fixtures/veteran.csv）：总体 HR=1.02(0.71~1.45) p=0.9218；四组 P 交互
0.042/0.087/0.239/0.024；层值层 n 逐项钉死。**出厂事故渊源**：v5.8 开发中抓出
第①期教学视频制备脚本标签-掩膜对调（var=(age<60) 时键 0=var==0=≥60），
本版金标即为此类错误的一票否决闸。附 ADR-0001 巨石拆解计划 + GitHub
Actions CI + 行预算守卫 3400→3600。

## 5.7.1 — 2026-10-21

galbraith 弧线-读数原子性 hotfix：弧线因碰撞被跳过读数时整条弧线保留=无读数
噪声——修为弧线与读数一同省略，并加「Arc 数==读数数」配对测试锁。
（本节为后补整理：5.7.1 发布时的 changelog 详情漏写，内容依据发版归档记忆恢复。）

## 5.7.0 — 2026-10-21

  - **New chart type #37: `cif` — competing-risk cumulative incidence
    (Aalen-Johansen)**: per-cause CIF step curves; dashed 1−KM naive reference
    shows how treating competing events as censored overestimates the target
    event (on a real Mayo Clinic mgus2 cohort of 1384 subjects the gap is
    +45.5 percentage points). Long-format `time`+`event` integer codes
    (0=censored, 1=target event, ≥2=competing), `cause_labels`, `percent`,
    `time_unit`, `compare_km` (auto = draw the reference only when competing
    events exist); stderr reports event counts, end-of-follow-up CIF per
    cause and the overestimation in percentage points. Single cohort —
    multi-arm data is routed to `-t km` (built-in AJ auto mode since v3.7,
    which now also points to the dedicated chart). Real-world example:
    `examples/realworld/hematology_mgus_cif.json`.
  - **Centralized anti-patterns page**: `references/antipatterns.md` — one
    page of what NOT to do (wrong chart for the data, data-prep traps,
    flag conflicts, statistical misreads, export mistakes), each entry with
    consequence + fix + cross-links into faq/pitfalls/limits; linked from
    SKILL.md/SKILL_ZH.md routing tables.
  - **Galbraith polish**: arc-label density relaxed (min spacing 10%→7.5% of
    the axis span, collision detection still guards glyphs) + a small
    no-effect reference label (`OR=1` on ratio scales, `差值=0` otherwise).
  - **Mechanism: `--list-types`** prints the authoritative chart registry
    (one per line); `mcp/server.py` now refreshes its chart list from the
    engine at startup (fallback list aligned with the v5.7 registry — the
    hardcoded list had drifted a dozen charts behind).
  - `--suggest` now recommends `cif` (score 96) when `time`+`event` contains
    competing-risk codes; scenario quick-reference in CLI help updated.

## 5.6.1 — 2026-10-20

  - **Fix: galbraith deep-branch crash** — with >12 studies and adjacent
    outlier labels, the label-declutter keep-outlier path hit a variable-name
    typo (NameError). Added a regression lock with duplicate outlier studies.
  - **Label avoidance upgrade**: the declutter now walks a vertical ladder
    (8 depths) plus mirrored horizontal candidates before giving up, driven
    by acceptance testing on a real 83-study meta-analysis dataset — dense
    outlier clusters now resolve with zero glyph overlap.

## 5.6.0 — 2026-10-20

  - **New chart type #36: `galbraith` — Galbraith radial plot (meta-analysis
    heterogeneity)**: precision (1/SE) on x vs standardized effect (effect/SE)
    on y; regression through origin = pooled fixed effect; ±1.96 parallel band
    covers homogeneous studies; out-of-band studies are highlighted with red
    circles and reported per-study on stderr (heterogeneity/outlier suspects).
    Same schema as `funnel` (`studies` name/effect/se, effects on the log
    scale); effect-size arcs (OR=0.125~16 readings) drawn by default for
    ratio labels (OR/HR/RR) and auto-disabled for difference scales
    (MD/SMD); stderr also reports DL random-effects pooling with I² and
    P_het. Right-edge study labels flip inward (canvas-fit guarantee).
  - **composite `share_y` auto-unification**: set `"share_y": true` and
    panels sharing the same ylabel are unified to one y scale (log scales
    sync too; unified range reported on stderr). The `--doctor` cross-panel
    shared-scale precheck now also reads panel-level ylabel (schema-accurate)
    and points to `share_y` as the fix.
  - **Prompt cards doc** (`references/prompt-cards.md`): 12 paste-ready
    agent prompts — "对智能体说 → expected command → acceptance checks" for
    the main scenarios (baseline/KM/ROC/prediction四件套/Meta trio/omics/
    composite/journal themes/CJK/pub-ready/batch/suggest).
  - **Changelog split**: this file becomes a version index + last-3 details;
    the full history moved verbatim to `references/changelog-full.md`
    (zero content loss).
  - **CLI help scenario quick-reference** (epilog) and wizard Meta row now
    routes forest/funnel/galbraith.
  - Test-suite hygiene mechanism: verbatim `_command` tests now redirect
    `-o` to temp dirs (no more render artifacts in the repo trunk).

## 5.5.0 — 2026-10-19

  - **New chart type #35: `subgroup` — subgroup analysis forest**: per-level
    estimate squares + 95%CI whiskers, P-interaction per variable on the
    subgroup header row, Overall diamond at the bottom, right-side est (95% CI)
    and P columns (significant values accented). JSON: `subgroups=[{name,
    p_interaction?, levels=[{name, est, ci_low, ci_high, n?, p?}]}]` (1-12
    variables × 2-8 levels) + optional `overall`; `est_label` picks the
    no-effect line (HR/OR/RR=1, MD/SMD=0); `log_x` defaults to ratio scale
    with plain log ticks. Visualizes your fitted subgroup model — the engine
    does not fit.
  - **FAQ discoverability**: top-of-SKILL pointer and section-nav entry for
    `references/faq.md`.
  - **Boundaries-first ordering**: Capabilities & Boundaries now sits right
    after the section nav (before Quick Start) in both SKILL docs.
  - **Domestic install channels documented first** in README: SkillHub /
    ModelScope mirror / setup_env mirror fallback; GitHub demoted to the
    international option.

## 5.4.0 — 2026-10-18

  - **New chart type #34: `rcs` — restricted cubic spline / nonlinear
    dose-response curve**: estimate line + 95%CI band (log-ratio axis by
    default), no-effect horizontal rule + `ref` vertical reference, exposure
    rug along the bottom. JSON: `points=[{value, est, ci_lo, ci_hi}]` (≥5 grid
    points from your fitted spline model — the engine visualizes, it does not
    fit); `log_y=false` switches to a linear scale with the reference level at
    y=0 (`hline_at` overrides).
  - **DCA benefit-region shading**: thresholds where a model's net benefit
    beats both reference strategies are shaded in the model's color
    (`benefit_shade=false` to disable); the shaded ranges are reported on
    stderr for figure-vs-text cross-checking.
  - **Tick-collision false positive fixed at the mechanism level** (found via
    the DCA shading work): the anti-overlap pass counted out-of-view ticks
    (e.g. x=0.0 when xlim starts at 0.016 — never rendered) as visible boxes;
    a false intersection with the corner y-label then triggered the
    degradation ladder and silently hid real tick labels. Collision detection
    now filters ticks to the view interval.
  - **Scenario cards** (`references/scenario-cards.md`): 12 complete
    workflows, one card each = scenario + full runnable command + per-flag
    explanation + variants — the single entry covering the whole parameter
    system (answers "why do I need several docs for one scenario").
  - **SKILL.md density slimming**: journal preset table sunk to
    `references/limits.md` §六, stats/legend mini-sections merged, rare flags
    delegated to the cheatsheet — 33 chart types stay, prose shrinks.
  - **--doctor cross-panel shared-scale precheck**: composite panels sharing a
    y-label (same variable semantics) with >5× range mismatch are flagged
    before rendering.
  - Log-axis plain ticks (LogLocator 1/1.5/2/3/5/7 + scalar formatter) for all
    log-scale renders — no more 10⁰-style offsets.

## 5.3.0 — 2026-10-17

  - **New chart type #33: `nomogram` — clinical nomogram**: the prediction-model
    lookup chart (points ruler → per-variable scales → Total Points → outcome
    scales). JSON: `variables=[{name, ticks[2-12], labels?, points_at?}]`
    (points_at defaults to linear 0-100) + `outcome_scales=[{label, ticks,
    points_at}]` (1-3, in total-points units) + optional `total_points_max`.
    Visualizes your **fitted** model — the engine does not fit; total-axis
    ticks adaptively choose the nicest split (350→five-way 0/70/140/210/280/350),
    and figure height scales with row count so dense nomograms never compress.
  - **Version-consistency lock** (doc-accuracy mechanism): packaged
    `evals/evals.json` `skill_version` now pinned to the SKILL version and
    asserted by a regression test — ends the stale-metadata drift class.
  - **Consolidated flag-conflict table** in `references/limits.md` §〇
    (journal×width, stats scope, composite nesting, verify×format — all in one
    place) and the cluster_heatmap two-tier wording (1500 warn / 3000 hard cap)
    made explicit in both summary rows.
  - **Per-chart pitfalls FAQ** in `references/faq.md` (Cox PH prerequisites,
    upset top_n truncation accounting, venn --area fit deviation, dca endpoint
    rule, calibration binning practice, nomogram provenance, swimmer arrows,
    raincloud zero-variance) and remaining English-only diagnostics
    (`VERIFY OK/FAIL`, `--verify` warnings) made bilingual.

## 5.2.0 — 2026-10-16

  - **New chart type #31: `calibration` — model calibration curve**: binned
    predicted probability vs observed rate with the ideal diagonal as reference
    (equal-aspect square axes, the publication convention). Two data schemas:
    `bins=[{predicted, observed, n?, ci_lo?, ci_hi?}]` objects or parallel
    `predicted`/`observed` arrays with optional `ci_lo`/`ci_hi`/`n`; optional
    `hl_p` annotates the Hosmer-Lemeshow p; `smooth=true` adds a thin
    interpolation line. Completes the clinical prediction-model evaluation set
    alongside ROC.
  - **New chart type #32: `dca` — decision curve analysis**: net benefit vs
    threshold probability per model against the two reference strategies —
    treat-all (theory line derived from `prevalence`, or an explicit
    `treat_all` array) and treat-none (y=0, `show_none` toggle). Accepts 1-6
    models; thresholds must be strictly ascending in the open (0,1) interval.
  - **`--pub-ready` now bundles the reproduce package**: the submission pack
    (--verify + colorblind-safe theme + multi-format export) also emits the
    `--repro` bundle. Mechanism hardening: audit/repro emission moved out of
    the single-format branch (they previously went silent with
    `--multi-format`), and moved after the verify gate so a verify-FAIL exit
    never leaves a reproduce bundle for a broken figure; multi-format exports
    are all copied into the bundle.
  - **Mechanism unification — reserved-band helper**: the bottom reserved-band
    pattern (swimmer fact box, dumbbell legend) is now a shared
    `reserve_bottom_band()` helper in the drawing layer, per the pitfalls
    class rule for floating elements.
  - **Bilingual helper outputs**: `--suggest` now appends the Chinese chart
    name to every recommendation line; wizard/guide outputs remain fully
    bilingual. All 32 templates now carry `_command`+`_note` meta fields
    (6 previously silent templates gained captions), locked by a regression
    test. `--alt` text available for both new chart types.
  - 2 new scenario templates (`templates/calibration.json`, `dca.json`) and 2
    real-world examples (`examples/realworld/realworld_sepsis_calibration.json`,
    `realworld_sepsis_dca.json`, mutually consistent n=500 cohort).

## 5.1.0 — 2026-10-15

  - **New chart type #30: `dumbbell` — two points per row, gap-first**: one
    horizontal connector + two dots per row (`from` open circle → `to` filled
    circle), sorted by gap size so the largest change sits on top
    (`sort=gap|input|to`). Strictly two time points/groups per row (baseline vs
    follow-up, male vs female, control vs treatment) — for >2 use slope/line,
    for paired testing use `paired`. Optional `show_values` (per-dot values)
    and `show_gap` (Δ label at the connector midpoint, Pew-style); legend via
    `from_label`/`to_label`; bottom band reserved so the legend never collides
    with the last row. `--suggest` routes `from`/`to` pairs; `--alt` text
    included.
  - **`--repro` reproduce bundle**: after a successful render,
    `<output>.repro/` assembles everything needed to reproduce the figure
    byte-for-byte — the exact command, a copy of the input data, a copy of the
    rendered figure, the number-checking `audit.json`, and a bilingual
    README. Deterministic engine guarantee: same input + same command = same
    bytes, so the bundle is a complete provenance record for reviewers and
    co-authors. Idempotent (rerun rebuilds the folder).
  - `templates/dumbbell.json` (30 templates); docs updated to 30 chart types
    across SKILL bilingual/README/quickstart/cheatsheet/templates-README.
  - Tests: +TestV50100 (E2E render, Δ-pairing correctness, validate fatals,
    alt/suggest, template _command, repro bundle determinism); suite green.

## 5.0.0 — 2026-10-14

  - **New chart type #29: `ridgeline` — stacked per-group densities (joyplot
    form)**: one KDE ridge per group stacked vertically with partial overlap
    (`overlap` 0–0.95, default 0.55), painter's-algorithm ordering (upper
    ridges in front), per-ridge baselines and theme-cycled colors; shows how a
    distribution shifts/morphs across ordered groups (time points, dose levels,
    scenarios) in one frame. Same schema as violin (`labels` + `datasets`);
    `sort=median` orders ridges by group median; single-value groups degrade to
    a marker line with an explicit stderr notice. `--suggest` lists ridgeline
    for raw per-group data; `--alt` accessibility text included.
  - **`--audit` figure-vs-data sidecar**: after a successful render,
    `<output>.audit.json` records descriptive statistics (n/mean/sd/median/
    min/max per series) recomputed independently from the input data — pure
    counts, zero inference — plus an input fingerprint, so any number on the
    figure can be checked against the data. Deterministic: same input, same
    audit file. Works for every chart type.
  - `templates/ridgeline.json` (29 templates); docs updated to 29 chart types
    across SKILL bilingual/README/quickstart/cheatsheet/templates-README.
  - Tests: +TestV50000 (E2E render, validate fatals, alt/suggest, audit sidecar
    determinism, template _command); suite green.

## 4.10.0 — 2026-10-13

  - **New chart type #28: `swimmer` — the clinical swimmer plot**: one
    horizontal bar per subject (treatment/follow-up duration), sorted by
    duration (classic form). `end` required (positive, unit-agnostic);
    optional `start` (bar offset, must be < end), `names` (per-subject
    labels), `group` (RECIST-aware coloring CR/PR/SD/PD sharing the
    waterfall semantic palette, case-normalized; other categories use theme
    colors in first-appearance order), `milestones` (per-subject marker
    times, e.g. first response; may exceed bar end — response persisting
    after treatment discontinuation), `ongoing` (arrowhead at bar end =
    still on treatment/in response at data cutoff), `ref_lines` (dashed
    landmark guides, e.g. month 12/24), `sort=duration|input`, `x_label`.
    Symbol legend (milestone dot / ongoing arrow) added automatically;
    stderr fact line reports n, ongoing count, milestone count and category
    counts; y labels never thinned (each bar = one subject, font adapts).
    `--alt` text, `--suggest` routing (per-subject `end` durations), demo
    data, template and real-world example included.
  - **--doctor submission-format hint**: when output is a
    submission format (PDF/TIFF/EPS) and `--verify` is off, doctor prints an
    actionable info line (use `--verify` or `--pub-ready`) — closing the
    "hidden rule" gap where reviewers expected verification on submission
    outputs.
  - `templates/swimmer.json` (28 templates) +
    `examples/realworld_csle_swimmer.json` (pediatric cSLE cohort,
    self-consistency-asserted); docs updated to 28 chart types across
    SKILL bilingual/README/quickstart/cheatsheet/templates-README.
  - Tests: +TestV41000 (E2E render group/no-group, validate fatals, alt
    text, suggest routing, template _command, real-world self-consistency);
    suite at 346 green (v4.1.0 regression class un-shadowed by rename).

## 4.9.0 — 2026-10-11

  - **New chart type #27: `raincloud` — the distribution trio** (Allen et al.
    2021 modern form): half-KDE cloud (density shape) + box (five-number
    summary: IQR box, bold median, 1.5×IQR whiskers) + deterministic jittered
    raw points ("rain") — every sample visible, nothing hidden. Same schema as
    violin (`labels` + `datasets`); `--stats auto/multi` apply; `jitter`
    (0–0.3, default 0.08) and `cloud_scale` (0–3, default 1.0) tunables;
    zero-variance groups degrade the cloud to a marker line with an explicit
    stderr notice (never silent). `--suggest` lists raincloud alongside
    violin/box for raw per-group data.
  - **setup_env.py `--fix`**: opt-in auto-install with mirror fallback
    (default PyPI → Tsinghua → Aliyun) — the #1 usability blocker (Python
    environment setup friction) now has a one-command path in China; default
    behavior unchanged (detect-only, no silent pip, supply-chain safe).
    quickstart step 1 now also points non-Python users to the cloud edition.
  - `templates/raincloud.json` (27 templates); docs updated to 27 chart types
    across SKILL bilingual/README/quickstart/cheatsheet/data-formats.
  - Tests: +TestV40900 (E2E render, validate fatals, registry count 27, demo
    render, suggest routing, zero-variance degradation); template lock 26→27;
    suite at 335 green.

## 4.8.0 — 2026-10-10

  - **New chart type #26: `waterfall` — oncology best-response waterfall**: one
    bar per patient (best % change from baseline, shrinkage negative), classic
    descending form (deterministic ties by input order; `sort="input"` keeps
    given order). RECIST-aware coloring: `group` (CR/PR/SD/PD, case-insensitive)
    uses canonical semantic colors; otherwise threshold bucketing (≤pr_cut blue
    response / ≥pd_cut orange progression / stable gray — volcano's semantic
    family). Dashed PR/PD threshold lines with right-edge labels (defaults
    -30/+20), count fact box in the always-empty lower-left region, zero
    baseline, `--show-values` per-bar labels, `y_label` override. Patient IDs
    rotate vertical above 14 bars (labels are data — exempt from tick thinning).
  - **suggest_chart_type dedup**: a whole recommendation block (funnel/venn/
    upset/bland_altman/roc) had been duplicated verbatim since v4.5 (masked by
    tail dedup) — second copy removed.
  - **Hardening from an independent read-only expert review (14 findings,
    all actionable ones fixed)**: waterfall fields (change/pr_cut/pd_cut)
    added to the known-field whitelist (kills false "invalid field" warnings);
    `--alt` now reports patient count and RECIST/fact-box categories; count
    fact box drawn on a white backing plate (readable over bars/threshold
    lines in any data shape); >60 patients thin x labels by stride with
    stderr disclosure (vertical 100-label smear fixed); NaN/±Infinity in
    `change` rejected as fatal (v4.5 numeric policy); sample data
    (DEMO/template/realworld) made RECIST-self-consistent — PR only at
    ≤-30% (reviewer caught -28.7%/-24.5%/-26.8% mislabeled PR); case
    variants of RECIST categories merge into canonical uppercase legend;
    stderr symbols ≤/≥ aligned with bucketing; SKILL_ZH stale "22 chart
    types" tree counts fixed; mcp af_engine synced (waterfall) and MCP docs
    de-hardcoded from "23".
  - Wizard gains a "per-patient best response" shape routing to waterfall.
  - `templates/waterfall.json` (26 templates), `examples/realworld/
    realworld_oncology_waterfall.json` (NSCLC II期 n=26 RECIST-consistent),
    docs updated to 26 chart types across SKILL bilingual/README/quickstart/
    cheatsheet/data-formats.
  - Tests: +TestV40800 (E2E group mode, bucket mode + show-values, validate
    fatals, registry count 26, demo render, sort=input path, stderr fact
    line, no-false-warning lock, --alt content lock, threshold-equality +
    NaN lock, 26-patient label-survival lock); realworld lock 3→4; suite at
    329 green.

## 4.7.0 — 2026-10-09

  - **New chart type #25: `upset` — UpSet set-intersection plot** (the standard
    successor to venn for 5+ sets): intersection-size bars (descending, labeled)
    + membership dot matrix + set-size bars; `sets{}` element lists (2~30 sets,
    ≥5 recommended), `top_n` (1~50, default 12), `min_size`, `sort`
    ("size"|"degree") with deterministic three-key tie-break; truncated
    intersections reported on stderr (never guessed). `--suggest` now routes
    ≥5-set data to upset (2~4 still venn); `--wizard` and `--explain upset`
    wired.
  - **Scenario guides** (reviewer-facing): new `references/color-guide.md`
    (data-semantics → color order → theme → grayscale self-check, colorblind
    rules, cross-figure semantic-color consistency) and
    `references/combo-guide.md` (composite vs pipeline decision, span/panel
    labels, multi-figure consistency disciplines, journal figure recipes).
  - **FAQ systematically indexed** (data / parameters / submission / environment
    categories with a top lookup table); new answers: color choice, multi-figure
    style consistency, venn-vs-upset selection. `pitfalls.md` adds two
    science-practice anti-pattern sections: rejection-prone color misuse and
    statistical-method misuse (SD-vs-SE, bar-hides-distribution, untested
    significance stars, paired-vs-independent, multi-comparison correction,
    censoring marks).
  - **Real-world research examples**: `examples/realworld/` (RCT 3-arm 48-week
    responses n=240; RNA-seq interferon-pathway DE; IgA nephropathy 3-arm KM,
    36.5-month follow-up) — realistic magnitudes and naming conventions, run-ready.
  - **limits.md quick-reference table** at top (hardest boundaries in 30
    seconds: cluster_heatmap/pca/venn/upset/km/paired/watchdog).
  - **Hardening from an independent read-only expert review (19 findings,
    all actionable ones fixed)**: composite panels reject the self-managed
    `upset` type up front (exit 1, Chinese guidance); intersection bars now
    share the dot-matrix column (classic UpSet alignment — bars sit exactly
    above their membership columns); set-name label band sized to the longest
    name (left margin + gap); short-set size labels fall back to dark
    out-of-bar text; set-name axis exempted from tick-label thinning;
    `title`/`top_n`/`min_size`/`sort`/`panel_labels` added to the known-field
    whitelist (no more false "invalid field" warnings); pipeline
    `format`/`multi_format` accept lists (YAML natural syntax); `--title` on
    self-managed types now prints an explicit [ignored] notice; `--alt` gains
    informative volcano/slope/upset descriptions; wizard routes upset to
    templates/upset.json; venn ≥5-set error points to `-t upset`; venn/comboguide
    recipes and realworld `_command`s verified runnable;
    `gen_slope`/`gen_volcano`/`gen_upset` re-exported from gen_figure.
  - Tests: +TestV40700 (upset E2E render, validate fatals, registry count 25,
    demo-data render, suggest routing, composite-panel rejection, new reference
    docs present); template count lock 24→25; suite at 318 green.

## 4.6.0 — 2026-10-08

  - P3 polish pack (from the same independent-testing rounds):
    - **ROC default semantic axis titles** ("False Positive Rate" / "True
      Positive Rate") — explicit --xlabel/--ylabel still win.
    - **venn title disambiguation**: the bare "n = 3" title (easily misread as
      a sample size) now reads "共 N 项（并集元素数）" in CJK context /
      "n = N (union of set elements)" otherwise.
    - **cluster_heatmap row-label font adapts to row count** (>60 rows shrink
      one step, >120 two steps; CJK font properties carry the size).
  - No chart-type or schema changes.

## 4.5.0 — 2026-10-07

  - **Fixes from two rounds of independent third-party testing (~180 cases,
    24/24 chart types, textbook datasets)**:
    - P0: missing `BboxBase` import crashed KM+ylabel / dual_axis / composite
      (now import-fixed; internal crashes exit 3, separated from --verify's 2).
    - P1: validator field-table synced to data-formats.md (estimates /
      studies_included / arrows / left* / pvalue / names no longer produce
      false "did you mean" warnings); `significance` keys now split on ":"
      before series lookup (false warnings eliminated).
    - P1: `tests/run_tests.py` now ships in the package (vendor promise kept).
    - R2-1: --suggest recognizes 5 statistical schemas (curves[]-roc /
      studies[]-funnel / sets{}-venn / log2fc+pvalue-volcano / methods{}-BA)
      — 10/10 standard forms hit.
    - R2-2: journal presets save WITHOUT tight-crop — physical width now
      matches declared mm exactly (was 2.5-2.6mm narrow).
    - R2-5: PDF byte-deterministic (CreationDate removed).
    - R2-6: KM single-subject group no longer prints a fake 95% CI.
    - P2/R2-9 unified numeric policy: bool → reject; inf → reject;
      numeric strings → auto-convert with warning; null → skipped (box family
      included, counted warning).
    - P2-6: GBK files report encoding (not "JSON syntax"); no phantom
      "--width None" message.
    - P3: CJK font detection prefers SC variant.

## 4.4.0 — 2026-10-06

  - **New chart type: `volcano` (type #24)** — omics differential expression
    standard form: x=log2FC, y=-log10(p-value); up/down/ns coloring (colorblind
    safe), threshold dashed lines, factual count box, auto top-N gene name
    labels with deterministic offsets. Schema: `log2fc`+`pvalue` arrays,
    optional `names`/`fc_cut`/`p_cut`/`top`.
  - Chart-type count 23 → 24 (docs counter-lock enforces update).
  - README: China mirror (ModelScope) link added to Install section.
  - SH description: "Trigger on" routing words appended (desc tail; routing
    optimization per search audit).

## 4.0.0 — 2026-10-02

  - **Engine modularization (4th cut, named in three consecutive reviews)**:
    the drawing layer moved out of gen_figure.py into `af_draw.py` (chart
    generators + stats-annotation helpers, ~2100 lines) and `af_shared.py`
    (leaf utilities: has_cjk/HATCH_PATTERNS/_ensure_ylabel_clear, 84 lines);
    gen_figure.py shrinks 5142 → ~3000 lines (args/validation/stats/pipeline).
    `import gen_figure` re-exports everything — zero API change.
  - **Structured title block (design-language item ⑥)**: new `--subtitle`
    (second line under the main title, smaller gray) and `--source`
    (bottom-right source note via fig.supxlabel — tight_layout-aware, never
    overlaps tick labels). The `--title "main / sub"` slash form stays valid.

## 3.10.0 — 2026-10-01

  - **`dual_axis` rebuilt to the canonical bars+lines form**: left-axis series
    now draw as grouped BARS and right-axis series as dashed LINES (paid-link
    feedback A1: the old all-lines form did not match the chart type). Override
    per side with data keys `left_type` / `right_type` ("bar"|"line").
  - **Legend rebuilt for dual_axis (A2+A4)**: the merged legend now covers
    series from BOTH axes and is drawn frameless inside a reserved top band on
    both scales — it can no longer occlude data peaks. `--legend-loc` /
    `--legend-outside` still honored.
  - **Single-series visual polish**: top-N emphasis (max bar in accent color,
    others muted), hatch exemption for single series, integer value labels
    (620 instead of 620.0), single-series legend suppression.
  - `left_ylabel` / `right_ylabel` data keys documented (per-axis titles).
  - **`left_floor` / `right_floor`** (optional): numeric lower bound per Y-axis —
    e.g. `"right_floor": 35` for a clean percentage-axis start (default 5% margin
    unchanged). Real-delivery feedback from the paid-link tester.

## 3.9.1 — 2026-09-30

  - **Docs accuracy pass** (post-release TRACE review): chart-type table now
    lists all 22 types (grouped_bar/paired/bland_altman/pca/funnel were
    missing); limits.md §2 flag-behavior column aligned with the actual
    `[ignored]` transparency mechanism (stats/egger/hatch/sheet/area rows were
    stale) and now covers `--order`/`--normalize`/`--doctor`/`--stats cox`;
    FAQ gains pub-ready/order/normalize/doctor entries; quickstart step 4 and
    pitfall #7 reference `--pub-ready`/`--doctor`; cheatsheet adds a
    scenario→flag-combination table; file-structure section lists all
    references/ docs. Zero code changes — documentation only.

## 3.9.0 — 2026-09-30

  - **`--order`**: custom category order for bar/box/violin/line — explicit
    comma list (must cover all labels) or `auto` (descending by first-series
    values; box/violin by group medians). Series/error arrays permuted and
    `significance` column indices remapped automatically.
  - **`--normalize`**: baseline scaling — `baseline` divides every series by
    the first series' mean (control = 1); `pct100` rescales each series to its
    own first point = 100. Error bars rescaled; distribution charts
    (box/violin) deliberately excluded.
  - **`--doctor`**: pre-render parameter/environment check report (flag
    compatibility, data schema, dependencies, output dir). Report-only with
    `-o`; omit `-o` for check-only mode (exit 1 = findings).

  - **Median bootstrap CI**: `--stats bootstrap` now also reports per-group
    **median** 95%CI alongside mean CI — the robust choice for skewed data
    (median CI printed with guidance note).
  - **`--pub-ready`**: one-flag submission bundle — expands to --verify +
    colorblind-safe theme + pdf,png multi-format (semantic sugar over four flags).

- **v3.7.0** (2026-09-26) — Competing-risks analysis (substantive statistical feature,
  second item of the statistics-methods roadmap; targets creativity 4.5/4.7):
  - **Aalen-Johansen estimator** (self-implemented): events encoded 0=censored,
    1=event, ≥2=competing risks → per-cause cumulative-incidence step curves.
    Triple validation: degenerates to 1-KM without competing risks (machine precision),
    completeness identity ΣCIF+S=1, and a hand-computed 6-patient literature example.
  - **Auto-switch**: KM with any event code ≥2 renders AJ cumulative-incidence curves
    with an `[auto]` notice; `cause_names` in data maps state codes to labels.
  - boundary: setup_env dependency versions pinned (matplotlib>=3.5, numpy>=1.21,
    pymupdf>=1.20, scipy>=1.7) and surfaced in the Safety & Data statement.

- **v3.6.0** (2026-09-26) — Flag-interaction transparency (targets the v3.5.0
  evaluation's usability 4.7 / accuracy 4.7 / completeness 4.8):
  - **`[ignored]` announcements**: incompatible flags are no longer silently ignored —
    six key combinations (--stats on non-box/violin, --compare/--egger/--area/--hatch/
    --sheet misuse) print an explicit stderr notice.
  - **CSV error-bar pre-hint**: bar/grouped_bar with .csv input prints the JSON
    errors-field guidance up front (previously only after a failed render attempt).
  - **Historical disclosure**: Lab Report PDF extraction (removed in v2.0.1) documented
    in pitfalls.md with the alternative path.

- **v3.5.0** (2026-09-26) — Bootstrap confidence-interval workstation (substantive
  statistical feature; targets creativity 4.7 / accuracy 4.7):
  - **`--stats bootstrap`** (box/violin): percentile bootstrap (Efron 1979), 5000
    resamples, fixed seed → deterministic output. Per-group mean 95%CI drawn as error
    diamonds + per-group-vs-first mean-difference CI brackets (CI-contains-zero
    explicitly stated instead of misleading stars).
  - **Dual gold-standard validation**: bootstrap CI vs analytic normal-theory CI
    convergence on large samples, and cross-check against scipy.stats.bootstrap.
  - Composite panel-level `stats_bootstrap` passthrough; stderr report per comparison.

- **v3.4.0** (2026-09-25) — Design-language pack, second slice: direct labeling
  (targets the v3.3.0 evaluation's creativity 4.7 / accuracy 4.7):
  - **`--direct-label`**: multi-series line charts label each series directly at the
    line end (auto vertical collision avoidance) instead of a legend box — Nature-style
    annotation. `glm-brand`/`nature-clean` themes enable it by default for line charts
    (`--no-direct-label` opt-out; explicit `--legend-loc` wins).
  - **Title hierarchy**: glm-brand/nature-clean themes render titles bold + left-aligned.
  - Pro API: options pass through whitelisted `style`/`theme` (regex-guarded).
  - **dual_axis combined legend preserved** (found by the 55-machine agent): the
    main flow re-created the legend with main-axis handles only, dropping right-axis
    series (e.g. CRP) from the legend. gen_dual_axis's combined legend is now kept.
    Regression: template 15 PDF text contains the right-axis series name.
  - **Composite KM panel `median_auto` passthrough** (found by the 55-machine agent):
    `median_auto: false` was silently ignored inside composite panels (panel-kwargs
    whitelist missed it) — auto median-survival labels re-appeared with wrong units.
    Fixed + regression lock.

- **v3.3.0** (2026-09-24) — Discovery-channel release (small & safe; no behavior changes):
  - **Frontmatter colon-bomb fix**: the platform's YAML reader treats ": " inside folded
    description/when_to_use values as a mapping and reports "no valid skill" (observed on
    another skill). Both EN frontmatter values rewritten with em-dash/parenthesis phrasing.
  - **README.md (official)**: bilingual first screen for the GitHub discovery channel —
    badges, quick start, "why" section, docs map, paper toolkit, docsor.cn site link.
  - GitHub sync is now step-10 of the release chain (sync_github.sh, one-way mirror,
    hygiene hard-scan; pitfalls.md excluded via .gh-sync-exclude).

- **v3.2.0** (2026-09-22) — Auto-behavior transparency + safety statement (targets the
  v3.1.0 evaluation's lowest items: accuracy 4.6, antiPatternFaq 4.7):
  - **`[auto]` transparency**: automatic behaviors are explicitly announced —
    `--journal` width-lock prints that `--width` was ignored; `--verify` on non-PDF
    output prints that no overlap check runs. (Follows the v3.1 auto-downsample pattern.)
  - **Boundaries front-loaded**: a top-3 boundary banner at the top of the main docs
    (--verify PDF-only, --journal width-lock, cluster auto-downsample).
  - **FAQ expanded**: a dedicated flag-conflict section (--journal×--width, --verify×format,
    --stats×chart-type, --compare scores, --egger funnel, --hatch vs --style, CSV errors).
  - **Safety & Data statement** (bilingual): fully-local rendering, zero network requests,
    no telemetry, explicit optional setup_env, --demo temp dir, per-process debug switches.
  - **`--style nature-clean`** (design-language pack, first slice): Okabe-Ito palette,
    top/right spines removed, grid off, frameless legend — the Nature-style visual
    language, answering the "default style looks provincial" critique with a
    one-flag switch. Pure addition: default behavior unchanged.

  - **Templates**: every scenario template gains a `_description` line.

- **v3.1.0** (2026-09-21) — One-command figure + auto-downsample + KM risk-table hotfix
  (merged release; supersedes v3.0.1 which was published hours earlier on the same day).
  Targets the v3.0.0 evaluation's lowest items: usability 4.6, errorHandling 4.8.
  Includes the v3.0.1 hotfix: KM auto risk-table silently dropped when a CJK font was
  loaded with non-CJK group names (regression since v2.9.0; fixed with regression lock
  + 22-template CJK sweep), plus the Related Resources section (MedWiki, docsor.cn):
  - **`--quick -d data`**: one-command figure — auto-picks the chart type from the data
    (reuses the --suggest analyzer) and renders immediately through the full pipeline
    (validation, watchdog, exit codes); prints alternative types.
  - **cluster_heatmap auto-downsample**: >3000 rows without `--downsample` now
    auto-samples to 2000 rows with a prominent notice instead of failing (behavior
    change; docs updated). Still deterministic; `--downsample N` overrides.
  - **venn --area high-residual guidance**: when the ellipse fit deviation is large
    (>15%), concrete remedies are printed (fewer sets / drop extreme regions / classic
    equal-circle mode).
  - **Docs**: --hatch wording unified across SKILL.md; limits.md gains a measured
    performance reference table; data-formats.md gains a JSON-vs-CSV capability matrix.
- **v3.0.1** (2026-09-20) — Hotfix: KM auto risk-table silently dropped when a CJK font
  was loaded with non-CJK group names (undefined symbol; regression since v2.9.0).
  Fixed with a regression lock + 22-template CJK sweep. Also adds a 'Related Resources'
  section (MedWiki reference site, same-author disclosure + disclaimer).
- **v3.0.0** (2026-09-19) — Main-doc layering, cheatsheet, script modularization
  (targets the v2.9.0 evaluation's lowest items: trigger 4.5, progressive 4.5, and the
  structure note on large scripts):
  - **Chart table gains a Category column** (Compare/Composition/Distribution/Trend/
    Matrix/Inference/Survival/Diagnosis/Sets/Flow) — scannable without reading every row.
  - **Key Flags table slimmed** to high-frequency entries; the full flag reference moved
    to the new `references/cheatsheet.md` (one-page commands + full flags + exit codes +
    top boundaries).
  - **Journal preset interactions surfaced inline** (--journal locks width, theme
    auto-linking) at the point of use, instead of requiring a trip to limits.md.
  - **Script modularization (first slice)**: wizard (`af_wizard.py`) and the exception
    diagnosis system (`af_diagnostics.py`: graded exit codes, Chinese three-part
    diagnosis, field near-miss hints) extracted from gen_figure.py; names remain
    importable from gen_figure (zero caller changes). gen_figure.py 4760→4522 lines.
  - Version history in the main docs compressed to one line + pointer (dedupe).

- **v2.9.0** (2026-09-19) — Boundary consolidation + standalone getting-started guide
  (targets the v2.8.0 evaluation's two lowest items: boundary 4.5, progressive 4.5):
  - **references/quickstart.md** (new): standalone getting-started guide — full chart
    decision tree, the three helpers (--wizard/--suggest/--explain), a 4-step first-run
    path, Python API entry points, and the top first-timer pitfalls. The main doc keeps
    a compact mapping plus a pointer.
  - **references/limits.md** §6/§7 (new): consolidated flag-interaction matrix
    (--journal × --width, PDF overlap check needs explicit --verify, default DPI,
    watchdog, journal×theme, --stats multi×auto) and runtime environment boundaries
    (headless Agg built in, CJK font detection, import-embedding Agg requirement,
    writable output dir, cluster row pre-advisory).
  - **Pre-emptive cluster advisory**: cluster_heatmap with >1500 rows (half the hard
    cap) now prints a --downsample suggestion at render time instead of only failing
    at the 3000-row limit.
  - **KeyError near-miss hints**: a misspelled JSON field in the error path now suggests
    the closest legal field names (difflib) in the Chinese diagnosis.
  - Python API surfaced from the Quick Start section; version bumps to 2.9.0.

  - **中位数 bootstrap CI**：`--stats bootstrap` 现同时报告每组**中位数** 95%CI——
    偏态数据的稳健引用口径（附引用建议注释）；
  - **`--pub-ready`**：一键投稿包——自动展开为 --verify + 色盲安全主题 + pdf,png
    多格式导出（四参数语义糖）。

- **v3.7.0**（2026-09-26）—— 竞争风险分析（实质统计功能第二项，统计方法线规划落地；
  对标 creativity 4.5/4.7）：
  - **Aalen-Johansen 估计器**（自研实现）：事件编码 0=删失 1=事件 ≥2=竞争风险 →
    每因累计发生率阶梯曲线。三重验证：无竞争风险退化恒等式 CIF=1-KM（机器精度）、
    完备性 ΣCIF+S=1、文献 6 人例手算对拍；
  - **自动切换**：KM 数据任一组 events 含 ≥2 编码即自动切 AJ 累计发生率曲线
    （[auto] 告知）；数据可带 cause_names 映射原因标签；
  - boundary：setup_env 依赖版本钉死（matplotlib>=3.5 等）并写入安全声明。

- **v3.6.0**（2026-09-26）—— 参数交互显式化（对标 v3.5.0 评测 usability 4.7 /
  accuracy 4.7 / completeness 4.8）：
  - **`[ignored]` 显式告知**：不兼容参数不再静默忽略——六组关键组合（--stats 用于
    非 box/violin、--compare/--egger/--area/--hatch/--sheet 误用）stderr 显式提示；
  - **CSV 误差棒前置提示**：bar/grouped_bar + .csv 输入即提示 JSON errors 字段路径
    （此前渲染失败后才提示）；
  - **历史功能披露**：Lab Report PDF 提取（v2.0.1 移除）入 pitfalls.md，附替代路径。

- **v3.5.0**（2026-09-26）—— Bootstrap 置信区间工作站（实质统计功能；对标 creativity 4.7 /
  accuracy 4.7）：
  - **`--stats bootstrap`**（box/violin）：percentile bootstrap（Efron 1979 经典方法），
    5000 次重采样，固定种子→确定性输出。每组均值 95%CI 误差棒 + 组间均值差 CI 括号
    （CI 含 0 明示，不给误导性星号）；
  - **双重金标准对拍**：大样本下 bootstrap CI 与正态解析 CI 收敛 + scipy.stats.bootstrap 交叉核对；
  - composite 面板级 stats_bootstrap 透传；stderr 逐对比报告。

- **v3.4.0**（2026-09-25）—— 设计语言第二刀：直接标注（对标 v3.3.0 评测 creativity 4.7 /
  accuracy 4.7）：
  - **`--direct-label`**：多系列线图在线末端直接标注系列名（自动上下避让碰撞），替代
    图例框——Nature 风标注语言；glm-brand/nature-clean 主题下 line 默认开启
    （`--no-direct-label` 关闭；显式 `--legend-loc` 优先）；
  - **标题层级**：glm-brand/nature-clean 主题标题加粗+左对齐；
  - Pro API options 白名单透传 style/theme（正则防护，引擎侧最终校验）。
  - **dual_axis 组合图例保留**（外部测试 agent 发现）：主流程无参重建图例仅含主轴
    handles，右轴系列（如 CRP）从图例消失；现保留 gen_dual_axis 内部组合图例。
    回归：模板 15 PDF 文本含右轴系列名。
  - **复合图 KM 面板 median_auto 面板级透传**（外部测试 agent 发现，本仓等效移植）：
    此前面板 kwargs 白名单缺失该键，composite 里 median_auto:false 被静默忽略——
    自动中位生存标签带错误单位复发。已修复+回归锁。

- **v3.3.0**（2026-09-24）—— 发现渠道版（小而稳；无行为变更）：
  - **frontmatter 冒号炸弹修复**：平台 YAML 解析器把 description/when_to_use 折叠值中的
    "冒号+空格"当作映射，导致判"无有效 skill"（其他 skill 已踩坑）。英文两处值改写为
    破折号/括号表述；
  - **README.md 官方化**：GitHub 发现渠道第一屏——双语徽章/快速开始/卖点/文档地图/
    论文全家桶/docsor.cn 官网入口；
  - GitHub 同步固化为发布链第⑩步（sync_github.sh 单向镜像+卫生硬扫描；
    pitfalls.md 经 .gh-sync-exclude 排除不上公开面）。

- **v3.2.0**（2026-09-22）—— 自动行为透明化与安全声明（对标 v3.1.0 评测最低项：
  accuracy 4.6、antiPatternFaq 4.7）：
  - **`[auto]` 透明化**：自动行为显式告知——`--journal` 锁宽度时明示 `--width` 被忽略；
    `--verify` 用于非 PDF 输出时明示本次不做重叠检查；
  - **边界前置**：主文档顶部新增三条最常用边界横幅（--verify 仅 PDF/--journal 锁宽/
    cluster 自动降采样）；
  - **FAQ 扩充**：新增参数冲突专节（--journal×--width、--verify×格式、--stats×图型、
    --compare scores、--egger、--hatch vs --style、CSV 误差棒）；
  - **「安全与数据」声明（双语）**：纯本地渲染零网络请求、无遥测、setup_env 为可选显式
    动作、--demo 临时目录、调试开关均为进程内显式设置；
  - **`--style nature-clean`**（设计语言包第一刀）：Okabe-Ito 配色+去顶右框线+无网格+
    无框图例——Nature 系版式语言一键开关，正面回应"默认风格保守"批评。
    纯增量：默认行为零变化。

  - **模板**：全部场景模板补 `_description` 说明行。
  - **历史功能披露**：Lab Report PDF 提取功能于 v2.0.1 移除（提取错误率不可接受），
    pitfalls.md 增补说明与替代路径（手工转录→标准管线）。

- **v3.1.0**（2026-09-21）—— 一键出图+自动降采样+KM 风险表热修（合并发布，含同日早间的
  v3.0.1 全部内容）。对标 v3.0.0 评测最低项：usability 4.6、errorHandling 4.8。
  含 v3.0.1 热修：KM 自动风险表在『已加载中文字体+组名英文』场景静默丢失（回归锁+22 模板
  CJK 扫描）；另含『相关资源（同一作者）』节（MedWiki，docsor.cn）。
  - **`--quick -d 数据`**：一键出图——按数据自动选择图型（复用 --suggest 分析器）并直接
    走完整渲染管线（校验/看门狗/退出码），stderr 打印备选图型；
  - **cluster_heatmap 自动降采样**：>3000 行未给 `--downsample` 时自动采样到 2000 行并
    显著告知（行为变更：此前为致命错退出；文档已同步更新），确定性不变，`--downsample N` 可覆盖；
  - **venn --area 高残差主动建议**：椭圆拟合偏差 >15% 时打印具体补救措施（减少集合数/
    去掉悬殊区域/改等圆模式）；
  - **文档**：--hatch 口径统一；limits.md 新增实测性能参考表；data-formats.md 新增
    JSON vs CSV 能力对照表。
- **v3.0.1**（2026-09-20）—— 热修：KM 自动风险表在『已加载中文字体+组名为英文』场景
  静默丢失（未定义符号，v2.9.0 起携带）；修复并加回归锁+22 模板 CJK 全量扫描。另新增
  『相关资源（同一作者）』节（MedWiki 医学参考站披露+免责声明）。
- **v3.0.0**（2026-09-19）—— 主文档信息分层、速查卡与脚本模块化（对标 v2.9.0 评测
  最低项：trigger 4.5、progressive 4.5 与 structure 的脚本体量点名）：
  - **图表类型表新增「类别」列**（比较/构成/分布/趋势/矩阵/统计推断/生存分析/诊断试验/
    集合/流程），一眼扫到目标图型；
  - **常用参数表瘦身**为高频 6 项，全量参数迁入新增的 `references/cheatsheet.md`
    （一页速查：22 种图型命令骨架+全量参数+退出码+边界 Top 5）；
  - **期刊预设交互行内前置**（--journal 锁宽度、theme 自动联动），不必翻 limits.md；
  - **脚本模块化第一刀**：选图向导（af_wizard.py）与异常诊断系统（af_diagnostics.py：
    分级退出码+中文三段式诊断+字段近似纠错）自 gen_figure.py 拆出，原名保持可从
    gen_figure 导入（调用方零改动）；gen_figure.py 4760→4522 行；
  - 主文档版本历史压缩为单行+指针（去重）。

- **v2.9.0**（2026-09-19）—— 边界收拢与独立快速入门（对标 v2.8.0 评测两个最低项：
  boundary 4.5、progressive 4.5）：
  - **references/quickstart.md（新增）**：独立快速入门指南——完整选图决策树、选图三件套
    （--wizard/--suggest/--explain）、上手四步、Python 内调用入口、常见第一坑 Top 6；
    主文档保留精简映射+指针。
  - **references/limits.md §六/§七（新增）**：参数交互矩阵收拢（--journal 锁宽度、
    PDF 重叠检测需显式 --verify、默认 DPI、看门狗、journal×theme、--stats multi×auto）
    与运行环境边界（内置 Agg 无显示环境开箱即跑、中文字体检测、import 嵌入需自行 Agg、
    输出目录可写、cluster 行数预判）。
  - **cluster_heatmap 预判式提示**：行数 >1500（半限）渲染时即输出 --downsample 建议，
    不再等 3000 行硬限报错。
  - **KeyError 字段纠错**：JSON 字段拼写错误时在中文诊断中给出最接近的合法字段名
    （difflib 近似匹配）。
  - 快速开始前置 Python API 入口；版本号升至 2.9.0。

- **v2.8.0** (2026-09-17) — Watchdog + zero-friction onboarding (targets the v2.7.0
  evaluation's lowest items: stability 4.3, doc length, exception coverage):
  - **Render watchdog**: adaptive per-type/size budget (30-1800s, `--timeout N` to
    override, `0` to disable); on breach prints a Chinese three-part diagnosis and
    hard-exits with code 5 — no more indefinite hangs.
  - **Graded exit codes**: 3=data/format error, 4=environment/dependency error,
    5=watchdog timeout, 6=memory guard rejected (0/1/2 semantics unchanged).
  - **Auto-degrade retry**: on MemoryError the figure is rebuilt at ×0.85 size and
    half output DPI, announced on stderr; second failure exits 6.
  - **`--downsample N`**: deterministic equidistant row sampling for cluster_heatmap;
    the >3000-row fatal error now suggests the exact command.
  - **venn 4-set ellipse** (v2.8 flagship): deterministic pinwheel layout validated
    so all 15 regions are non-empty; `--area` fits ellipse geometry to target areas
    (least-squares on a deterministic grid, eulerAPE-style) and honestly discloses
    the max residual; region counts stay exact; labels de-cluttered deterministically.
  - **`--wizard`**: 4 questions -> a ready-to-run command; non-TTY environments get
    a decision-tree guide instead of hanging.
  - **Exception coverage**: ImportError/ModuleNotFoundError/OSError/TimeoutExpired
    etc. now map to Chinese diagnoses (exit 4); FAQ error table 8 -> 12 rows.
  - **Docs**: SKILL_ZH 536 -> 316 lines (decision tree, exit-code table, single
    boundary source); deep-dive sections moved to references/pitfalls.md; a
    regression test now locks chart-count claims in all docs to the registry.
- **v2.7.0** (2026-09-16) — Stability + Cox regression workstation:
  - `--stats cox`: raw per-subject survival data -> automatic multi-variable Cox
    proportional hazards -> HR[95%CI] forest (self-implemented Efron ties +
    Newton-Raphson + Grambsch-Therneau PH test, zero new dependencies; cross-checked
    against lifelines to |Δβ| < 1e-6 on rossi/GBSG2).
  - `--size` aspect presets (16:9/4:5/9:16...); exception handler v3 (Chinese
    three-part diagnosis + original error + targeted tips, AF_DEBUG escape).
  - Deterministic output (same input -> byte-identical file), memory guard,
    200-chart soak; package hygiene (zero duplicate files; `scripts/journal/*.json`
    as the single journal-preset source); SKILL docs slimmed ~30%.
- **v2.6.0** (2026-09-15) — Pipeline edition (targets the v2.5.0 review's 4.7):
  - `--pipeline analysis.yaml|json`: whole-paper multi-figure pipeline with
    global `defaults` + per-figure `figures` list (previous `--batch` kept).
  - `--multi-format tiff,png,pdf`: one run renders every format from one
    source filename.
  - `references/python-api.md`: call from Python via subprocess or import
    (load_data / validate_data / gen_*), examples verified end-to-end.
  - Templates 16 → 22, now covering all 22 chart types, plus a full README
    index (fixes the "only 10 templates" discovery gap).
  - KM data-trap fix: CSV long tables (time/event/group columns) are rejected
    with a how-to-convert hint instead of silently rendering a meaningless
    single curve; validation messages are now Chinese-first (~10 English
    leftovers cleared) and the FAQ gained an error-message lookup table.
  - Mechanism fixes from the Pro audit ship here: KM risk-table group-name
    placement, venn set-label mirroring, PRISMA box heights with measured
    self-healing.
  - Forest null reference line now defaults by effect measure (OR/RR/HR → 1.0,
    MD/SMD → 0.0) instead of always 0 — natural-scale significance reads
    correctly without setting ref_line (found by real-data review).
- **v2.5.0** (2026-09-14) — Submission polish:
  - `--annotate "x,y:text"`: repeatable arrow annotations at data coordinates
    (category axes accept tick labels), auto declutter, arrows track texts.
  - NEJM + Science (AAAS) color themes; `--journal nejm|lancet|science|nature`
    now auto-links the matching color theme (explicit `--theme` wins).
  - venn `--area`: area-proportional Euler mode (2 sets analytic, 3 sets
    least-squares fit of centers+radii with honest fit report); new `"regions"`
    count input fixes the never-parseable numeric `"sets"` format from v2.3.
  - `--legend-loc` + `--legend-outside` (composite figures merge to one shared
    legend, duplicates removed).
  - Library exception Chinese mapping 9 → 18; payload description now states
    21 chart types / 9 themes (fixes stale "15 chart types" store summary).
- **v2.4.0** (2026-09-13) — Meta analysis workstation:
  - KM auto median survival + 95% CI (Greenwood log-log, lifelines-identical
    on 20 randomized datasets) annotated in-plot; `--no-median` opts out.
  - `forest --sensitivity`: leave-one-out DL re-pooling rendered under the main plot.
  - Library exception Chinese explanations (9 entries) + FAQ (references/faq.md).
  - CJK font enforcement mechanism: any CJK text found before render gets the
    CJK font automatically (kills tofu blocks at the mechanism level).
- **v2.3.0** (2026-09-12) — 6 new chart types (21 total): funnel (DL pooled line,
  `--egger`), bland_altman, pca (grouping ellipses + loadings), paired
  (paired-test brackets), venn (exact region counts), cluster_heatmap (Ward
  reorder); `--batch` manifest rendering with report JSON; `--caption` sidecar;
  vectorized KM (50k rows ≈ 3 s).
- **v2.2.0** (2026-09-11) — Journal & workflow expansion:
  - Journal presets 2 → 9: added `science`, `cell`, `nejm`, `jama`, `ieee`, and
    Chinese presets `cma` (中华医学会系列) + `cn-core` (中文核心通用) with auto CJK.
  - Excel input: `.xlsx/.xls` direct load with `--sheet` selection (openpyxl).
  - `--stats auto` (box/violin): pairwise-vs-first significance with automatic
    test selection (Shapiro → Welch t / Mann-Whitney U), brackets + stars drawn,
    per-comparison report on stderr.
  - `--alt`: accessibility (alt) text sidecar `<output>.alt.txt` generated from
    the data dict — groups, medians, AUC, overall effect, PRISMA counts, panels.
  - `templates/`: 10 scenario templates (data JSON + command + caption template)
    covering meta-analysis, RCT, survival, ROC, correlation, PRISMA,
    dose-response, composite, survey, Chinese-journal figures.
  - Mechanism fixes (staged 09-08): tick-label overlap ladder now rotates to 90°
    before any thinning and warns loudly when labels are hidden; PRISMA side
    boxes auto-fit long reason text (measured width + wrap + height); KM
    non-monotonic input auto-sorts with an honest warning. Tests 96 → 118.
- **v2.1.0** (2026-09-08) — Reviewer toolkit release: PRISMA 2020 flow + chart-type suggester.
  - New chart type `-t prisma`: PRISMA 2020 systematic-review flow diagram — three-phase spine
    (Identification / Screening / Included) with left-rail phase labels, exclusion boxes with
    per-reason counts, and standard EN/ZH wording via `"lang": "en"|"zh"`. `validate_data()`
    gates the arithmetic: screened = identified − duplicates, sought = screened − excluded,
    assessed = sought − not retrieved, exclusion reasons + included = assessed. Inconsistent
    counts are rejected with ERROR (exit 1) — catching the most common reviewer complaint
    before the figure ever ships.
  - New `--suggest`: structural analyzer recommends chart types from any data file (ranked
    scores + reasons + ready-to-run command). Recognizes prisma/diagram/composite/roc/km/
    forest/heatmap/dual_axis/violin/box/scatter/bar signatures.
  - `gen_legend.py` now covers prisma (journal-format flow description).
  - 13th example dataset (`examples/example_prisma.json`); regression tests 78 → 96 (prisma
    validation gates ×7, CLI EN/ZH renders ×2, suggest unit tests ×7 + CLI ×2); evals 8 → 10.
- **v2.0.1** (2026-08-13) — UX improvements (targeting SkillHub official review T5.0/R4.5/A4.4/C4.8/E4.6 gaps):
  - **Default theme changed to `glm`** (muted Morandi, colorblind-safe; old `default` renamed `classic`, kept for compatibility).
  - New: `--list-themes` (in-terminal color swatches), `--theme-swatch <theme> -o out.png`, `--style glm-hatch` (GLM signature style one-liner), `--demo` (interactive menu, 12 built-in sample datasets), `--explain <type>` (limitations/notes), theme aliases + case/prefix tolerance (`okabe`/`colorblind`/`glm-blog`/`default`→glm).
  - `--hatch` extended to stacked_bar and forest (overall diamond).
  - **Heatmap default colormap fix**: when `--cmap` is omitted the default is now RdBu_r (red-blue diverging) — previously the kwargs default silently fell through to matplotlib's viridis (yellow-green); explicit `--cmap` still overrides.
  - **Data-driven heatmap colormap (added)**: all-positive data now auto-switches to warm YlOrRd sequential (removes the "broken band" look from RdBu_r's white midpoint on low positive cells); diverging RdBu_r only for data with negatives; vmin/vmax follow data range. Regression tests ×2.
  - Error messages for known limits (e.g., CSV+error bars) now include HINT with the fix.
  - New `scripts/setup_env.py`: one-command env setup (deps/CJK font/font-cache cleanup/self-check).
  - New `examples/`: 5 sample data JSONs + 7 theme swatch previews + README.
  - Docs: new FAQ section (font cache/deps/CSV limits/theme cheatsheet).
- **v2.0.0** (2026-08-12) — Hardening release: data validation layer, journal presets, verification tooling, regression/evals suites.
  - `validate_data()`: structural validation across all 18 type/alias branches, called centrally from `main()`; fatal → `ERROR:` + exit 1 (no output), warning → `WARNING:` (accepted). Examples: empty series, length-mismatched series, box/violin labels ≠ group count, missing required keys, ROC `curves[].auc` outside [0,1].
  - `--journal nature|lancet` + `--column single|double`: official column widths (nature 89/183mm, lancet 85/183mm), font size (7/8pt), family (Helvetica/Arial), 600dpi.
  - `--verify`: in-line pixel-level overlap check on PDF output, exit 2 on real overlaps.
  - `scripts/audit_pdf.py`: font-size audit with `--min-size`/`--fail-below`/`--max-reports` — journal minimum text gate (nature 5pt, lancet 6pt).
  - `scripts/gen_legend.py`: journal-format supplementary legends from the same data JSON.
  - `legend_audit()`: empty-legend detection for Python-API misuse.
  - Bug fixes: box/violin `labels` validated as group names (series count, not value count); ROC AUC bounds checked per curve; `has_cjk()` extended to supplementary planes (Ext-B..F U+20000–U+2EBEF, Ext-G U+30000–U+3134F); composite legend double-period removed; `_scan_cjk()` now scans dict **keys** too (Chinese series names trigger font loading).
  - `tests/run_tests.py`: 50 unittest tests (14 chart-type CLI smoke tests + validate_data units + CSV edge cases + CJK + legend audit + PDF audit + legend gen).
  - `evals/evals.json`: 8 behavioral evals, each validated against real CLI behavior (exit codes, CJK auto-load, nature double=183mm, no-false-warning legend audit, CSV long-format, box group labels, KM legend formatting).
- **v1.6.6** (2026-08-12) — Scatter readability fixes: (1) `gen_scatter` now renders point labels from `data["labels"]` (one per x/y point, alternating above/below with growing offset so clustered points like years 1950/1953/1955 don't collide); (2) trend line now carries `label='Linear trend'` so the legend explains the dashed regression line instead of leaving it unlabeled. Rebuilt demo3 with full annotations (title, axis labels, point labels, legend) — verified 0 real overlaps.
- **v1.6.5** (2026-08-12) — Documentation: made overlap verification a mandatory step for PDF delivery. Added "Verification" section to SKILL.md/SKILL_ZH.md (3-stage pixel verifier usage + warning that PyMuPDF bbox intersections are line-height-model artifacts, 100% false positives on this generator's output), added `verify_overlap_pixel.py` to file-structure docs, and added `pymupdf`/`scipy` to the `requires` pip list (verifier dependencies). Demo figures regenerated with real KEGG pathway gene counts (demo2) and ChEMBL pchembl values (demo3) after the previous demo datasets were found to contain degenerate synthetic values (all-50 gene counts / all-4.0 max_phase) that compressed axes into misleading density.
- **v1.6.4** (2026-08-12) — Verifier fix: `confirm_min_dist` now uses unique assignment (a component whose centroid falls in both spans' candidate windows is assigned to the nearer origin) instead of shared assignment, eliminating false positives for rotated y-axis labels (e.g. scatter `(max phase)` label vs top tick `4.00` — claimed overlap was verifier cross-assignment, not real ink contact). Re-verified all 14 production figures + 4 demo figures: **0 real overlaps**. Added `_ensure_ylabel_clear()` safety net to `gen_figure.py` (auto-increases y-label labelpad when matplotlib's measured bbox actually collides with tick labels; inert when no conflict, as in all current figures).
- **v1.6.3** (2026-08-12) — Label overlap verification closed at pixel level. Root cause of all reported "overlaps": PyMuPDF span/char bboxes use the font line-height model (Noto CJK 2.856em, DejaVu 1.695em), which systematically overestimates rotated text (45°: 32.3pt claimed vs 16.8pt real ink for fs=9) and stacked labels (char row bbox spans full line height). Verified all 14 production figures with a 3-stage pixel verifier (connected components → component centroid ownership → min ink distance at 600dpi): **0 real ink overlaps**. matplotlib `get_window_extent` (20.9pt vs 16.8pt real) is slightly conservative, so the anti-overlap mechanism is correct as-is. Verifier at `scripts/verify_overlap_pixel.py`. Removed dead `math` import from `gen_figure.py`.
- **v1.6.2** (2026-08-11) — Fixed two quality issues found in production use. (1) CJK detection is now recursive: `_text_has_cjk()` scans the entire data dict including nested composite panels/diagram text, so Chinese titles inside composite panels correctly trigger Noto Sans CJK loading (previously they rendered as tofu boxes). (2) Automatic label anti-overlap: x-axis labels rotate 45° when >8 bars or >12-char labels (bar) / >10 points (line) / >6 columns or >14-char labels (heatmap); hbar y-labels shrink one point when >12 categories; composite panels pass `alternate` through to hbar subplots.
- **v1.6.1** (2026-08-07) — Brightened GLM theme yellow from `#D49356` to `#D79D55` (true mean pixel value of the GLM-5.2 blog chart, sampled from 143k yellow pixels; previous value was an unrepresentatively dark sample). All alternate-style bar charts now render with the brighter warm yellow.
- **v1.6.0** (2026-08-07) — Added `--alternate` flag: GLM-5.2 blog style blue/yellow alternating bars for single-series bar/hbar charts (`--theme glm --hatch --alternate` reproduces the blog's yellow+black-hatch look: `#D79D55` yellow / `#70A0D0` blue alternating per bar with black hatch lines). Colors come from the first two theme colors, so it also works with `cool`/`okabe-ito` themes.
- **v1.5.2** (2026-06-18) — Added `cool` theme: 8-color cool-toned palette (navy `#1B4965`, ocean `#2E6F9E`, sky `#4FA3C5`, dark teal `#3D8080`, medium teal `#62A0A8`, steel `#5B7BA0`, slate `#7B9AB5`, pale steel `#9DB5CC`), all hues in 190-260° range, colorblind-safe. Created in response to user rejecting warm/saturated palettes and requesting 素雅冷色调配色.
- **v1.5.1** (2026-06-18) — Bug fixes: `gen_km()` crashes when `median_survival` value is `null` (median not reached); `gen_scatter()` crashes when `groups` array length exceeds `x`/`y` length (composite panels). Both fixed with null/length guards. Added `cool` theme (navy/ocean/teal/slate cool-toned palette, colorblind-safe). See `references/pitfalls.md`.
- **v1.5.0** (2026-06-17) — Added 3 new chart types: horizontal bar charts (hbar, with ratio annotations like "4.96x"), multi-panel composite figures (Panel A+B+C with GridSpec, any chart type per panel), architecture/flow diagrams (colored blocks, arrows, groupings, annotations); added GLM theme (muted/dusty palette pixel-extracted from GLM-5.2 blog: `#70A0D0` blue + `#D79D55` yellow, mean pixel values); added bar hatching with BLACK lines on ALL bars (print-friendly, 9 patterns: `//`, `\\`, `||`, `--`, `++`, `xx`, etc.); added `--hatch`, `--show-ratio`, `--ratio-base`, `--horizontal` CLI flags; **white background mandatory** for all themes (publication standard); see `references/reverse-engineering-colors.md` for pixel extraction technique
- **v1.4.0** (2026-05-17) — Added 4 new chart types: Kaplan-Meier survival curves (log-rank test, risk tables, median survival, censor marks), ROC curves (AUC, 95% CI, optimal cutoff, multi-model comparison), stacked bar charts (compositional data, percentage labels), dual Y-axis line charts (clinical score + lab marker); expanded data validation for new types
- **v1.3.0** (2026-05-17) — Added Okabe-Ito colorblind-safe theme (Nature Methods standard); DPI upgraded 300→600 for line art; added PDF/TIFF/EPS output; enhanced forest plot (weight bubbles, I² heterogeneity, events/total, separator line); accessibility alt-text guidance; smart DPI by content type
- **v1.2.0** (2026-05-16) — Added version metadata, requires declaration, negative triggers, file structure docs
- **v1.1.0** — Added auto CJK detection, CSV long-format auto-conversion, empty data validation
- **v1.0.0** — Initial release: 7 chart types, 4 themes, CJK support, statistical annotations

> ↓ 以下为 v5.6.0 拆分前的旧格式双语历史（英文/中文，v5.6.1 及更早），原样存档，未与上方各节合并。

## English

## Version History

## 中文

### v5.6.1（2026-10-20）

- **修复 galbraith 深分支崩溃**：研究数>12 且多个离群标注相邻时，避让的
  「离群保留」分支引用了笔误变量名（NameError）；新增同点重复离群回归锁。
- **研究名避让算法升级**：纵向 8 档阶梯+横向镜像候选位全部试净后才落位；
  由真实 83 项研究元分析数据的验收 fail 驱动——密集离群区零字形叠印。

### v5.6.0（2026-10-20）

- **新图型 #36：`galbraith` Galbraith 径向图（Meta 异质性可视化，漏斗图姊妹图）**：
  横轴精度 1/SE、纵轴标准化效应 effect/SE；过原点回归线=固定效应合并（斜率 b），
  ±1.96 平行带覆盖同质研究；带外研究红圈高亮并在 stderr 逐个报名（异质性/离群嫌疑）。
  数据 schema 与 `funnel` 完全一致（studies name/effect/se，效应取 log 值）；
  比率标签（OR/HR/RR）默认画效应量弧线（OR=0.125~16 读数），差值尺度（MD/SMD）
  自动关；stderr 同报 DL 随机效应合并+I²+P_het。右缘研究名标注自动向画布内翻转（不裁切）。
- **composite `share_y` 共享尺度自动统一**：数据加 `"share_y": true`，同 ylabel
  （同变量语义）的面板 y 轴自动统一到全体范围（log 尺度同步），stderr 报统一区间；
  `--doctor` 跨面板共享尺度预检同步修复为面板级 ylabel 读取（与 composite schema 一致）
  并把 `share_y` 作为机制出口写进提示。
- **提示词卡片文档**（`references/prompt-cards.md`）：12 张对智能体说的可粘贴完整指令
  ——「对智能体说 → 应产出命令 → 验收点」，覆盖基线/KM/ROC/预测模型四件套/Meta 三件套/
  组学/组合图/期刊主题/中文/投稿包/批量重渲/选型建议十二场景。
- **changelog 拆分**：本文件改为版本索引+最近三版详情；完整历史原样移入
  `references/changelog-full.md`（内容零删减）。
- **CLI 帮助场景速查**（epilog）+向导 Meta 行路由 forest/funnel/galbraith 三件套。
- 测试卫生机制化：逐字执行 `_command` 的测试统一把 `-o` 重定向到临时目录
  （渲染产物不再落 trunk，哨兵泄漏教训进机制）。

### v5.5.0（2026-10-19）

- **新图型 #35：`subgroup` 亚组分析森林图**：逐层效应方块+95%CI、亚组标题
  行报 P 交互、底部 Overall 菱形、右侧 est(95%CI)/P 双列（显著值红色）。
  `subgroups=[{name, p_interaction?, levels=[...]}]`（1~12×2~8）+`overall`
  可选；`est_label` 定无效线；`log_x` 默认比率对数轴+平实刻度。只可视化
  已拟合亚组模型（引擎不拟合）。
- **FAQ 可发现性**：SKILL 顶部指针+章节导航条目。
- **边界前置**：能力与边界章节移至章节导航之后（双语）。
- **国内安装通路前置**：README 安装节 SkillHub/魔搭/setup_env 镜像优先。

### v5.4.0（2026-10-18）

- **新图型 #34：`rcs` 限制性立方样条/非线性剂量反应曲线**：估计线+95%CI 带
  （默认对数比值轴）、无效应水平参照线+`ref` 竖直参照线、底部暴露 rug。
  JSON：`points=[{value,est,ci_lo,ci_hi}]`（≥5 个网格点，来自你拟合的样条模型
  ——引擎只可视化不拟合）；`log_y=false` 切线性轴（参照水平默认 y=0，
  `hline_at` 可覆盖）。
- **DCA 获益区间着色**：模型净收益同时压过两条参照策略的阈值区段按模型色
  淡色填充（`benefit_shade=false` 关闭）；着色区段写入 stderr 供图文对账。
- **刻度碰撞假阳性机制级修复**（随 DCA 着色工作发现）：防重叠检查曾把视图
  区间外的刻度（如 xlim 从 0.016 起、渲染不显示的 x=0.0）当可见框，与轴角
  y 标签假相交后触发降级阶梯，静默藏掉真实刻度标签。碰撞检测现按视图区间
  过滤。
- **场景卡片**（`references/scenario-cards.md`）：12 个完整工作流，每卡=
  场景+完整可跑命令+参数逐项说明+常见变体——参数体系的单一入口。
- **SKILL.md 减密**：期刊预设表下沉 `references/limits.md` §六，统计/图例
  小节合并，低频参数移交 cheatsheet——33 种图型信息不减，密度下降。
- **--doctor 跨面板共享尺度预检**：组合图同 y 轴标签（同变量语义）面板数值
  范围差 >5 倍时渲染前提示。
- 全部对数轴平实刻度（LogLocator 1/1.5/2/3/5/7 + 标量格式化），不再出现
  10⁰ 式科学计数法。

### v5.3.0（2026-10-17）

- **新图型 #33：`nomogram` 列线图（临床预测模型第四件）**：Points 计分尺→
  逐变量刻度→Total Points→结局概率尺。JSON：`variables=[{name, ticks[2~12],
  labels?, points_at?}]`（points_at 缺省线性 0~100）+`outcome_scales=
  [{label, ticks, points_at}]`（1~3 个，总积分口径）+`total_points_max` 可选。
  **只可视化你已拟合的模型，引擎不拟合**（points 请来自 R rms::nomogram 等）；
  总轴刻度自适应选最好台阶（350→五等分 0/70/140/210/280/350）；图高随行数
  自适应（≥0.6 英寸/行），多变量列线图不再行距压缩。
- **版本一致性锁**（文档准确性机制化）：随包 `evals/evals.json` 的
  `skill_version` 钉住 SKILL 版本并由回归测试断言——终结陈旧元数据漂移类
  （此前 2.2.0 随包漂流三个大版本）。
- **参数冲突集中表**：`references/limits.md` §〇 新增一表收拢全部冲突组合
  （journal×width/stats 域/composite 嵌套/verify×格式）；cluster_heatmap
  两级口径（1500 警告线/3000 硬顶）在两处速查行写明。
- **图型专属易错点 FAQ**：faq.md 新增一节（Cox PH 前提/upset top_n 截断
  对账/venn --area 拟合偏差/dca 端点规则/calibration 分箱惯例/nomogram
  来源口径/swimmer 箭头/raincloud 零方差）；残留英文诊断输出
  （VERIFY OK/FAIL、--verify 警告）双语化。

### v5.2.0（2026-10-16）

- **新图型 #31：`calibration` 校准曲线（临床预测模型三件套补齐）**：分箱
  预测概率 vs 实际观测率+理想对角线参照，等比正方形坐标（发表惯例）。两种
  数据给法：`bins=[{predicted,observed,n?,ci_lo?,ci_hi?}]` 对象数组或
  `predicted`/`observed` 平行数组（`ci_lo`/`ci_hi`/`n` 可选）；`hl_p` 标注
  Hosmer-Lemeshow p；`smooth=true` 加细插值参考线。与 ROC 同一直接用户群
  （预测模型论文），补齐 ROC+校准+DCA 评价三件套。
- **新图型 #32：`dca` 决策曲线分析**：净收益 vs 阈值概率，各模型与两条参照
  策略同图——全部干预（由 `prevalence` 推理论线，或 `treat_all` 显式数组）
  与不干预（y=0 水平线，`show_none` 可关）；1~6 个模型；阈值须严格升序且在
  (0,1) 开区间（t=0/1 净收益无定义）。
- **`--pub-ready` 合流复跑包**：投稿包（--verify+色盲安全主题+多格式导出）
  现在同时产出 `--repro` 复跑交付包。机制硬化：audit/repro 写出移出单格式
  分支（此前遇 `--multi-format` 静默失效），并移到 verify 门禁之后——
  verify FAIL 退出不再给坏图留复跑包；多格式导出文件全部进包。
- **机制统一——预留带 helper**：swimmer 事实框/dumbbell 图例的底部预留带
  模式收敛为绘图层共享 `reserve_bottom_band()`（pitfalls「浮动元素预留带」
  类级铁律的共享实现）。
- **辅助输出双语化**：`--suggest` 每条推荐追加图型中文名；向导/决策树输出
  保持全中文；32 个模板 `_command`+`_note` 元字段全覆盖（此前 6 个模板
  缺图注说明），并由回归测试锁定。两个新图型均带 `--alt` 无障碍摘要。
- 模板 ×2（`templates/calibration.json`、`dca.json`）；真实场景示例 ×2
  （`examples/realworld/realworld_sepsis_calibration.json`、
  `realworld_sepsis_dca.json`，同一 n=500 队列叙事、n 逐箱自洽可对账）。

### v5.1.0（2026-10-15）

- **新图型 #30：`dumbbell` 哑铃图（差距优先）**：每行两点（`from` 空心圆 →
  `to` 实心圆）+连接线，默认按差距降序（最大改善居顶）；严格限两时点/两组
  （>2 用 slope/line，配对检验用 paired）；可选 `show_values` 点端数值与
  `show_gap` 中点 Δ 标注（Pew 式）；`from_label`/`to_label` 自定图例；底部
  预留带保证图例永不与末行碰撞；`--suggest` 自动路由、`--alt` 摘要齐备。
- **`--repro` 复跑交付包**：渲染成功后组装 `<输出>.repro/`——精确命令、输入
  数据副本、成图副本、数字对账 audit.json、双语 README，拿到包即可逐字节
  复现该图（确定性引擎：同输入+同命令=同字节）；幂等重建。
- 模板 dumbbell.json（30 模板）；双语文档 30 种图型同步。
- 测试：+TestV50100（E2E 渲染、Δ 配对正确性、校验致命项、alt/suggest、
  模板 _command、repro 包确定性）。


### v5.0.0（2026-10-14）

- **新图型 #29：`ridgeline` 山脊图（joyplot 形态）**：每组一条 KDE 密度山脊
  纵向堆叠、部分重叠（`overlap` 0~0.95，默认 0.55），画家算法上排在前的山脊
  完整覆盖下排；一屏展示分布随有序分组（时间点/剂量/场景）的移动与变形。
  schema 同 violin；`sort=median` 按组中位数排山脊；单值组退化为标记线并
  stderr 明示；`--suggest` 自动路由；`--alt` 无障碍摘要。
- **`--audit` 数字对账侧车**：渲染成功后写 `<输出>.audit.json`——从输入数据
  独立重算描述统计（n/均值/SD/中位数/极值，纯计数零推断）+ 输入指纹，
  图上的任何数都可与数据逐项对账；同输入同字节，全图型可用。
- 模板 ridgeline.json（29 模板）；双语文档 29 种图型同步。
- 测试：+TestV50000（E2E 渲染、校验致命项、alt/suggest、audit 侧车确定性、
  模板 _command 逐字执行）。


### v4.10.0（2026-10-13）

- **新图型 #28：`swimmer` 游泳图（临床试验逐例时长）**：每例一条横条
  （治疗/随访持续时长），按时长降序经典形态；`end` 必填（正数，单位自定）；
  可选 `start`（起条偏移，须小于 end）、`names`、`group`（RECIST 着色，
  与瀑布图同族语义色、大小写归一）、`milestones`（每例里程碑时点，如首次
  应答，可晚于条端=停药后应答持续形态）、`ongoing`（条端箭头=数据截止仍在
  治疗/缓解）、`ref_lines`（地标虚线）、`sort=duration|input`、`x_label`。
  符号图例自动添加；stderr 事实行含例数/持续中/里程碑/类别计数；y 标签
  不抽稀（每条=一名受试者，字号自适应）。--alt 无障碍摘要、--suggest 路由、
  demo、模板与真实场景示例齐备。
- **--doctor 投稿格式提示**：输出为投稿格式（PDF/TIFF/EPS）且未开 --verify
  时给出行动建议行（--verify 或 --pub-ready）。
- 模板 swimmer.json（28 模板）+ examples/realworld/realworld_csle_swimmer.json
  （儿童狼疮肾炎 cSLE 队列，程序化自洽断言）；双语文档 28 种图型同步。
- 测试：+TestV410000（E2E 分组/无分组渲染、校验致命项、alt 文本、suggest
  路由、模板与示例 _command 逐字执行、示例自洽断言、doctor 提示）。


### v4.6.0（2026-10-08）

- P3 视觉打磨包（同源独立测试发现项）：
  - **ROC 默认语义轴标题**（"False Positive Rate"/"True Positive Rate"；
    显式 --xlabel/--ylabel 仍优先）。
  - **venn 标题消歧**：裸数字 "n = 3"（易误读为样本量）改为 CJK 语境
    "共 N 项（并集元素数）"、非 CJK "n = N (union of set elements)"。
  - **cluster_heatmap 行标签字号随行数自适应**（>60 行缩 1 号、>120 行缩 2 号；
    CJK 字体属性携带字号）。
- 图型数与 schema 无变化。

### v4.5.0（2026-10-07）

- **两轮独立第三方严格测试（约 180 用例、24/24 图型、教科书数据集）的 12 项修复**：
  - P0：af_shared 缺 `BboxBase` 导入致 KM-ylabel/双轴/组合图开箱崩溃（已修；
    内部崩溃退出码改 3，与 --verify 的 2 语义分离）。
  - P1：校验器字段表与 data-formats.md 同源（estimates/studies_included/arrows/
    left*/pvalue/names 不再假警告）；`significance` 键先按 ":" 拆分再查系列
    （假警告消除）。
  - P1：包内自带 `tests/run_tests.py`（厂商回归承诺兑现）。
  - R2-1：--suggest 识别 5 种统计 schema（10/10 标准形态命中）。
  - R2-2：期刊预设保存不再 tight 裁边——实际图宽=宣称毫米（原系统性窄 2.5-2.6mm）。
  - R2-5：PDF 字节级确定（去除 CreationDate）。
  - R2-6：KM 单例组不再输出伪 95% CI。
  - P2/R2-9 数值策略统一：bool 拒绝、inf 拒绝、字符串数字自动转换+警告、
    null 跳过（box 家族兑现承诺，计数警告）。
  - P2-6：GBK 文件报编码问题（不再误报"JSON 语法错误"）；幻影
    "--width None" 消息消除。
  - P3：中文字体探测优先 SC 变体。

### v4.4.0（2026-10-06）

- **新图型：`volcano` 火山图（第 24 种）**——组学差异表达标准形态：x=log2FC、
  y=-log10(p)；上调暖橙/下调蓝/非显著灰（色盲安全），阈值虚线+计数事实框+
  显著性 Top-N 基因名自动标注（确定性偏移避让）。schema：`log2fc`+`pvalue`
  等长数组，可选 `names`/`fc_cut`/`p_cut`/`top`。
- 图型计数 23 → 24（文档计数锁强制同步）。
- README：Install 段新增 China mirror（ModelScope 魔搭）链接。
- SH description：尾部追加 "Trigger on" 路由词（搜索审计优化）。

### v4.0.0（2026-10-02）

- **引擎模块化第四刀**（连续三版评测点名）：绘制层自 gen_figure.py 拆出——
  `af_draw.py`（14 类图型生成器+统计标注助手，约 2100 行）+ `af_shared.py`
  （叶工具 has_cjk/HATCH_PATTERNS/_ensure_ylabel_clear，84 行）；
  gen_figure.py 5142 → ~3000 行（保留参数解析/校验/统计/流水线/文档）。
  `import gen_figure` 全量再导出——API 零变更。
- **结构化标题栏（设计语言⑥收官）**：新增 `--subtitle`（主标题下方第二行，
  小号灰色）与 `--source`（图底右对齐来源注，经 fig.supxlabel 参与
  tight_layout 自动让位，绝不与刻度标签重叠）。`--title "主/副"` 斜杠写法
  继续兼容。

### v3.10.0（2026-10-01）

- **`dual_axis` 重构为经典"左柱右线"形态**：左轴系列画分组柱、右轴系列画虚线
  （真金付费链路反馈 A1：旧的全折线形态与图型定义不符）。数据键
  `left_type` / `right_type`（"bar"|"line"）可按侧覆盖。
- **dual_axis 图例重构（A2+A4）**：合并图例覆盖左右轴全部系列，无边框绘制在
  双侧预留顶部带内——不再可能遮挡数据峰值。`--legend-loc` / `--legend-outside`
  仍可覆盖。
- **单系列视觉增强**：Top-N 强调（最大条主色、其余淡化）、单系列斜纹豁免、
  整数值标签（620 而非 620.0）、单系列图例抑制。
- `left_ylabel` / `right_ylabel` 数据键补文档（双轴各自标题）。
- **`left_floor` / `right_floor`**（可选）：双轴各自 Y 轴下限数值——如
  `"right_floor": 35` 让百分比右轴整数起算（投稿规范；默认 5% 边距行为不变）。
  真金交付链路测试者建议采纳。

### v3.9.1（2026-09-30）

- **文档准确性热修**（发布后 TRACE 评测反馈）：图表类型表补齐 22 种
  （grouped_bar/paired/bland_altman/pca/funnel 曾缺失）；limits.md §二参数行为列
  对齐 `[ignored]` 透明化机制（stats/egger/hatch/sheet/area 五行过时）并补入
  `--order`/`--normalize`/`--doctor`/`--stats cox`；FAQ 增 pub-ready/order/
  normalize/doctor 四问；quickstart 上手四步与第一坑接入 `--pub-ready`/`--doctor`；
  cheatsheet 新增「典型场景参数组合」节；文件结构节列全 references/ 全部文档。
  零代码变更，纯文档。

### v3.9.0（2026-09-30）

- **`--order`**：类别顺序重排（bar/box/violin/line）——显式逗号列表（须覆盖全部
  标签）或 `auto`（按第一系列值降序；box/violin 按各组中位数降序）。
  系列/误差数组同步重排，significance 列索引自动改写。
- **`--normalize`**：归一化——`baseline` 各系列÷第一系列均值（对照=1）；
  `pct100` 各系列÷自身首点×100。误差棒同步缩放；分布图（box/violin）明确不适用。
- **`--doctor`**：渲染前参数/环境体检（参数组合/数据/依赖/输出目录）。
  带 `-o` 只报告不拦截；省略 `-o` 纯体检模式（exit 1=有发现）。

## 版本历史

- **v4.9.0**（2026-10-11）—— 新图型 #27 raincloud 雨云图 + 环境门槛一键化：
  - **`raincloud`**：分布三合一（KDE 半小提琴云+箱线五数概括+确定性抖动原始点雨）
    ——摘要（箱）、形状（云）、每个样本（雨）同屏呈现且互不遮挡（Allen et al. 2021
    现代形态）。schema 同 violin；`--stats auto/multi` 通用；`jitter`/`cloud_scale`
    可调；方差为 0 的组云退化为标记线并 stderr 告知（零静默）。
  - **setup_env.py --fix**：显式自动安装+镜像回退（默认源→清华→阿里）——国内用户
    环境门槛一键路径；默认行为不变（仅检测不装，供应链安全）。quickstart 第一步
    补零 Python 用户云端版引导。
  - 模板 raincloud.json（27 模板）；全文档 27 种图型同步。
  - 测试：+TestV40900（E2E/fatal/注册表 27/demo/suggest/零方差退化）；模板锁 26→27；
    全量 335 绿。
- **v4.8.0**（2026-10-10）—— 新图型 #26 `waterfall` 肿瘤缓解瀑布图：
  - **`waterfall`**：每例（患者）自基线最佳变化%一柱，经典降序形态（并列按输入序，
    `sort=input` 保持给定序）；RECIST 感知着色——`group`（CR/PR/SD/PD 大小写不敏感）
    用规范语义色，未给 group 按阈值分桶（≤pr_cut 缓解蓝/≥pd_cut 进展橙/中间稳定灰，
    与 volcano 同语义族）；PR/PD 阈值虚线（默认 -30/+20）右端标注；计数事实框落
    恒空左下区；`--show-values` 柱端数值；患者标识 >14 例自动竖排（标签是数据，
    豁免抽稀）。
  - **suggest_chart_type 去重**：funnel/venn/upset/bland_altman/roc 推荐段自 v4.5
    起逐字重复两份（尾去重掩盖）——删第二份。
  - **独立只读专家审查加固（14 项发现，可动手项全修）**：waterfall 三字段
    （change/pr_cut/pd_cut）入字段白名单（消除假「无效字段」警告）；`--alt`
    报告例数与 RECIST/分桶计数；计数事实框加白底托板（任意数据形态下压柱/
    压阈值线都可读）；>60 例 x 标签按 stride 抽稀并 stderr 披露（修 100 例
    竖排糊死）；change 的 NaN/±Infinity 一律 fatal（v4.5 数值政策）；示例
    数据（DEMO/模板/realworld）RECIST 自洽——PR 只出现在 ≤-30%（审查逮住
    -28.7%/-24.5%/-26.8% 违标）；RECIST 类别大小写归一（PR/pr 不拆图例）；
    stderr 符号 ≤/≥ 与分桶口径对齐；SKILL_ZH 目录树残留「22 图型」修正；
    mcp af_engine 同步（waterfall）+MCP 文档去掉硬编码「23」。
  - 向导新增「每例最佳缓解百分比」形状。模板 waterfall.json（26 模板）+
    realworld NSCLC II 期 n=26（RECIST 自洽）示例；全文档 26 种图型计数同步。
  - 测试：+TestV40800 11 项（分组 E2E/分桶+show-values/fatal/注册表 26/demo
    直渲/sort=input/stderr 事实行/假警告锁/--alt 内容锁/阈值等值+NaN 锁/
    26 例标签存活锁）；realworld 锁 3→4；全量 329 绿。

- **v4.7.0**（2026-10-09）—— 新图型 #25 upset 集合交集图 + 场景化指导包：
  - **`upset`**：≥5 集合交集可视化（韦恩图 2~4 集合的标准后继）。交集大小柱（降序直标）+
    隶属点阵+集合大小横条；`sets{}` 元素列表（2~30 集合）、`top_n`(1~50)/`min_size`/
    `sort`(size|degree) 确定性三键 tie-break；未展示交集计入 stderr 事实行。--suggest
    ≥5 集合改推 upset、--wizard/--explain 已接线；模板 upset.json+计数锁 24→25。
  - **场景化指导**：新建 references/color-guide.md（配色选择策略：语义→色序→主题→灰度
    自检）与 combo-guide.md（多图组合应用：composite/pipeline 选型+一致性纪律）。
  - **FAQ 系统化**：顶部分类索引（数据/参数/投稿/环境）+三新增问；pitfalls 新增两节
    科研反模式（易退稿配色、统计方法误用）。
  - **真实科研场景示例** examples/realworld/ 三例（RCT 应答/组学火山图/三臂 KM）。
  - **独立只读专家审查加固（19 项发现，可动手项全修）**：composite 面板前置拒绝
    自管图型 upset（exit 1 中文指引）；交集柱与点阵同列对齐（经典 UpSet 版式，
    柱正好在其隶属点列上方）；集合名标签带按最长名字自适应（左边距+间隙）；
    短集合数值标签回落柱外深色；集合名轴豁免刻度抽稀；title/top_n/min_size/sort/
    panel_labels 入字段白名单（消除「无效字段」假警告）；pipeline 的
    format/multi_format 支持列表（YAML 自然写法）；--title 用于自管图型时显式
    [ignored] 提示；--alt 新增 volcano/slope/upset 有信息量描述；向导 upset 指向
    templates/upset.json；venn ≥5 集合报错指路 -t upset；组合配方与 realworld
    _command 逐字验证可执行；gen_slope/gen_volcano/gen_upset 经 gen_figure 再导出。
  - **limits.md 速查表**前置。测试 +TestV40700 共 318 绿。

- **v2.8.0**（2026-09-17）— 看门狗与上手零门槛（对标 v2.7.0 评测最低项：稳定性 4.3、文档偏长、异常覆盖）：
  - **渲染看门狗**：按图型与数据量自适应预算（30~1800s，`--timeout N` 覆盖、`0` 禁用）；超时输出中文三段式诊断并强制中断（退出码 5）——不再无限挂起。
  - **退出码分级**：3=数据/格式错、4=环境/依赖错、5=看门狗超时、6=内存护栏拒绝（0/1/2 语义不变）。
  - **自动降级重试**：MemoryError 时按 ×0.85 图幅+DPI 减半重建一次并在 stderr 明示；再失败退出码 6。
  - **`--downsample N`**：cluster_heatmap 确定性等距采样；超 3000 行的致命报错直接给出该命令。
  - **venn 4 集合椭圆**（本版旗舰）：确定性风车布局经验证 15 区域全非空；`--area` 按目标面积椭圆联合最优拟合（确定性网格最小二乘，eulerAPE 思路），残差如实中文披露；区域数字保持精确计数；标签确定性疏散防相撞。
  - **`--wizard`**：四问生成完整命令；非交互环境打印选图决策树，绝不挂起。
  - **异常词条扩容**：ImportError/ModuleNotFoundError/OSError/TimeoutExpired 等映射中文诊断（退出码 4）；FAQ 报错速查表 8→12 行。
  - **文档**：SKILL_ZH 536→316 行（新增选图决策树、退出码表、边界单一真源）；深水区内容外移 references/pitfalls.md；新增回归测试将全文档图型计数表述锁死到代码注册表。
- **v2.7.0**（2026-09-16）— 稳健基石+Cox 回归工作站：
  - `--stats cox`：原始逐例生存数据 → 自动多因素 Cox 比例风险回归 → HR[95%CI] 森林图（自研 Efron 结基线+Newton-Raphson+Grambsch-Therneau PH 检验，零新依赖；与 lifelines 对拍 |Δβ|<1e-6）。
  - `--size` 画幅预设（16:9/4:5/9:16）；异常兜底 v3（中文三段式诊断+原文+建议，AF_DEBUG 逃生门）。
  - 确定性输出、内存护栏、200 图压测；包结构治理（重复清零、journal/*.json 单一参数表）；主文档瘦身约 30%。
- **v2.6.0** (2026-09-15) — 流水线版（对标 v2.5.0 评测 4.7 定向改进）：
  - `--pipeline analysis.yaml|json`：多图流水线，defaults 全局默认 + figures 逐图条目，
    一篇论文全套图一条命令出齐（原 --batch 保留可用）。
  - `--multi-format tiff,png,pdf`：一次渲染输出多种格式，文件名同源。
  - 新增 `references/python-api.md`：subprocess 与 import 函数级两种编程调用，
    示例全部实测跑通；校验消息 100% 中文化收尾（~10 条英文残留清除），
    FAQ 新增报错速查表。
  - 模板 16→22，覆盖全部 22 种图型 + README 全索引（修"只见 10 个模板"）。
  - KM 数据陷阱机制修复：CSV 长表（time/event/group 列）拦截并给转换指引，
    不再静默渲染无意义单曲线；KM 风险表组名实测定位、韦恩图集合标签镜像、
    PRISMA 盒高实测自愈三项机制修复随本版发布。
  - 森林图无效参考线改按效应尺度自动取值（OR/RR/HR→1.0，MD/SMD→0.0），
    不再恒为 0——自然尺度 OR 的显著性判读不再画错位置（真实数据审核发现）。
- **v2.5.0** (2026-09-14) — 投稿精修：`--annotate "x,y:文字"` 数据坐标箭头注释（类别轴支持标签定位，
  自动防重叠+箭头跟随）；NEJM/Science 期刊配色主题 + `--journal` 自动联动配色；
  venn `--area` 面积比例 Euler 模式（2 集合解析解/3 集合最优拟合，拟合偏差如实报告）+
  `regions` 区域计数键（修复 v2.3 数字型 sets 从未可用的缺陷）；`--legend-loc`/`--legend-outside`
  （组合图合并共享图例）；库异常中文映射 9→18；发布描述更正为 21 图表/9 配色（修复"15 chart types"旧文案）。
- **v2.4.0** (2026-09-12) — Meta 分析工作站：KM 自动中位生存（95%CI，与 lifelines 全等对拍）图内标注；
  forest --sensitivity 留一法敏感性分析（自动画在同一图下方）；库异常中文名映射；常见问题 FAQ。
- **v2.3.0** (2026-09-11) — 统计深水区：KM 自动风险表+log-rank、--stats multi（Tukey/Dunn+Hochberg）、
  ROC --compare DeLong、新图型 funnel/bland_altman/pca/paired/venn/cluster_heatmap、--batch 批量、
  --caption 双语图注、CLI 全面中文化、极端输入友好报错。
- **v2.1.0** (2026-09-08) — 审稿人工具箱版本：PRISMA 2020 流程图 + 图表类型推荐器。
  - 新图表类型 `-t prisma`：PRISMA 2020 系统综述流程图——识别/筛选/纳入三阶段主轴 + 左侧
    旋转相位标签 + 右侧排除盒（含逐条排除原因计数），`"lang": "zh"|"en"` 输出中/英文标准
    措辞。`validate_data()` 对数字做自洽性闸门：初筛数=检索数−重复数、寻求获取数=初筛数−
    排除数、评估数=寻求数−未获取数、排除原因合计+纳入数=评估数——**数字对不上直接 ERROR
    拒绝出图**，把审稿人最常见的投诉拦在投稿之前。
  - 新 `--suggest`：分析任意数据文件的结构，推荐最合适的图表类型（评分排序 + 理由 +
    可直接运行的完整命令）。识别 prisma/diagram/composite/roc/km/forest/heatmap/
    dual_axis/violin/box/scatter/bar 特征签名。
  - `gen_legend.py` 支持 prisma（期刊格式流程描述图例）。
  - 第 13 个示例数据（examples/example_prisma.json）；回归测试 78 → 96（prisma 校验闸门
    ×7、CLI 中英渲染 ×2、suggest 单元+CLI ×9）；evals 8 → 10。
- **v2.0.1** (2026-08-13) — 用户体验优化（基于 SkillHub 官方评测 T5.0/R4.5/A4.4/C4.8/E4.6 的失分点）：
  - **默认配色改为 `glm`**（素雅莫兰迪、色盲安全；旧 default 改名 `classic` 兼容保留）。
  - 新增 `--list-themes`（终端彩色色块一览 7 套配色）、`--theme-swatch <主题> -o out.png`（色板预览图）、`--style glm-hatch`（GLM 黄蓝斜线招牌风格一键预设）、`--demo`（交互演示菜单，内置 12 类示例数据）、`--explain <类型>`（限制条件说明）、主题别名+大小写/前缀容错（`okabe`/`colorblind`/`glm-blog`/`default`→glm）。
  - `--hatch` 扩展支持 stacked_bar 与 forest（overall 菱形斜纹）。
  - **热力图默认色阶修复**：`--cmap` 未指定时默认 RdBu_r（红蓝发散，正红负蓝）——此前因 kwargs 默认值失效，热力图实际渲染为 matplotlib 默认 viridis（黄绿色）；显式 `--cmap` 仍可覆盖。
  - **热力图色阶数据驱动（v2.0.1 追加）**：全正数据自动改用 YlOrRd 暖色单渐变（消除 RdBu_r 白色中点导致的低值单元格"断层"感）；含负值才用 RdBu_r 红蓝发散；vmin/vmax 跟随数据范围。回归测试 ×2 锁定。
  - CSV+误差棒等已知限制的错误提示附带解决方案（HINT）。
  - 新增 `scripts/setup_env.py` 一键环境准备（依赖安装/中文字体检测/字体缓存清理/自检）。
  - 新增 `examples/` 目录：5 个示例数据 JSON + 7 套配色 swatch 预览 + README。
  - 文档新增 FAQ 章节（字体缓存/依赖/CSV 限制/配色速查）。
- **v2.0.0** (2026-08-12) — 加固版本：数据校验层、期刊预设、验证工具链、回归/评测套件。
  - `validate_data()`：覆盖全部 18 种类型/别名分支的结构校验，`main()` 集中调用；致命 → `ERROR:` + exit 1（不落盘），警告 → `WARNING:`（继续）。示例：空系列、长度不匹配系列、box/violin labels≠组数、缺少必需键、ROC `curves[].auc` 超出 [0,1]。
  - `--journal nature|lancet` + `--column single|double`：官方栏宽（nature 89/183mm，lancet 85/183mm）、字号（7/8pt）、字体族（Helvetica/Arial）、600dpi。
  - `--verify`：PDF 输出内联像素级重叠检查，真实重叠 exit 2。
  - `scripts/audit_pdf.py`：字号审计，`--min-size`/`--fail-below`/`--max-reports` — 期刊最小字号门禁（nature 5pt，lancet 6pt）。
  - `scripts/gen_legend.py`：从同一数据JSON生成期刊格式补充图例。
  - `legend_audit()`：Python API 误用导致的空图例检测。
  - Bug修复：box/violin `labels` 按组名校验（系列数而非值数）；ROC AUC 逐条曲线检查边界；`has_cjk()` 扩展到补充平面（Ext-B..F U+20000–U+2EBEF、Ext-G U+30000–U+3134F）；组合图图例重复句点移除；`_scan_cjk()` 现在也扫描字典**键**（中文系列名触发字体加载）。
  - `tests/run_tests.py`：50个unittest测试（14图型CLI冒烟 + validate_data单元 + CSV边界 + CJK + 图例审计 + PDF审计 + 图例生成）。
  - `evals/evals.json`：8个行为评测，每个都对照真实CLI行为验证（退出码、CJK自动加载、nature双栏=183mm、图例审计不误报、CSV长格式、box组标签、KM图例格式）。
- **v1.6.6** (2026-08-12) — 散点图可读性修复：(1) `gen_scatter` 现在渲染 `data["labels"]` 点标签（每个 x/y 点一个，上下交替偏移且偏移随索引增长，防止 1950/1953/1955 这类聚集点标签碰撞）；(2) 趋势线加 `label='Linear trend'`，图例会说明虚线是线性回归线（此前虚线无任何标注，读者无法理解）。demo3 以完整标注重建（标题、双轴标签、点标签、图例）——验证 0 处真实重叠。
- **v1.6.5** (2026-08-12) — 文档补强：交付 PDF 前必须运行像素级重叠验证器。SKILL.md/SKILL_ZH.md 新增"输出验证"章节（三级验证器用法 + 明确警告 PyMuPDF bbox 相交是行高模型产物，在本工具输出上 100% 为假阳性），文件结构文档补入 `verify_overlap_pixel.py`，`requires` pip 列表补入 `pymupdf`/`scipy`（验证器依赖）。demo 图改用真实数据重新生成（demo2 = KEGG 通路基因数、demo3 = ChEMBL pchembl 值）——此前 demo 数据集含退化合成值（基因数全 50 / max_phase 全 4.0），导致坐标轴被压缩成误导性密集刻度。
- **v1.6.4** (2026-08-12) — 验证器修复：`confirm_min_dist` 三级归属改为"唯一归属"（分量质心同时落入双方候选窗时归属距 origin 更近者），消除旋转 y 轴标签场景的假阳性（scatter 的 `(max phase)` 标签 × 顶部刻度 `4.00`——此前报告的"重叠"是验证器交叉归属所致，并非真实墨迹接触）。重验全部 14 张生产图 + 4 张 demo：**0 处真实重叠**。`gen_figure.py` 新增 `_ensure_ylabel_clear()` 安全网（matplotlib 实测 bbox 与刻度真实冲突时自动增大 y 轴 labelpad；无冲突时惰性不触发，当前全部图形均未触发）。
- **v1.6.3** (2026-08-12) — 标签重叠问题像素级验证闭环。所有"重叠"报告的根因：PyMuPDF 的 span/char bbox 采用字体行高模型（Noto CJK 2.856em、DejaVu 1.695em），对旋转文本系统性高估（45° 时 fs=9 报 32.3pt，真实墨迹仅 16.8pt），对竖排/堆叠标签的行 bbox 也覆盖整行行高。用三级像素验证器（连通分量 → 分量质心归属 → 600dpi 最小墨迹距离）验证全部 14 张生产图：**0 处真实墨迹重叠**。matplotlib `get_window_extent`（20.9pt vs 真实 16.8pt）略保守，防重叠机制本身正确无需改动。验证器归档于 `scripts/verify_overlap_pixel.py`；移除 `gen_figure.py` 中死导入 `math`。
- **v1.6.2** (2026-08-11) — 修复两个生产环境发现的质量问题。(1) CJK 检测改为递归：`_text_has_cjk()` 会扫描整个 data 字典（含嵌套的 composite 面板/diagram 文本），composite 面板内的中文标题现在能正确触发 Noto Sans CJK 字体加载（此前渲染成方框乱码）。(2) 标签自动防重叠：bar 图 x 轴标签 >8 个或标签 >12 字符、line 图 >10 个点、heatmap 列 >6 个或 >14 字符时自动旋转 45°；hbar 类别 >12 个时 y 轴标签字号缩小 1pt；composite 面板将 `alternate` 透传给 hbar 子图。
- **v1.6.1** (2026-08-07) — GLM 主题黄色提亮：`#D49356` → `#D79D55`（GLM-5.2 博客原图 14.3 万黄色像素的真实均值；此前取到了分布中偏暗的样本）。所有交替风格柱状图现使用更亮的暖黄色
- **v1.6.0** (2026-08-07) — 新增 `--alternate` 参数：GLM-5.2博客风格黄蓝交替柱状图。单系列 bar/hbar 图逐柱交替使用主题前两色（glm 主题下为黄 `#D79D55` / 蓝 `#70A0D0`），配合 `--hatch` 即复现博客的"黄蓝交替+黑色斜线"样式；也可与 `cool`/`okabe-ito` 等主题组合使用
- **v1.5.2** (2026-08-12) — 新增 `cool` 主题：8色冷色调配色（藏青 `#1B4965`、海蓝 `#2E6F9E`、天蓝 `#4FA3C5`、深青 `#3D8080`、中青 `#62A0A8`、钢蓝 `#5B7BA0`、石板 `#7B9AB5`、浅钢蓝 `#9DB5CC`），色相全在190-260°，色盲安全。因用户拒绝暖/饱和配色并需求素雅冷色调而创建。
- **v1.5.1** (2026-06-18) — Bug修复：`gen_km()` 在 `median_survival` 为 `null`（中位生存未达到）时崩溃；`gen_scatter()` 在 `groups` 数组长度超过 `x`/`y` 长度（composite面板）时崩溃。均已用 null/长度守卫修复。新增 `cool` 主题（藏青/海蓝/青灰/石板冷色调，色盲安全）。见 `references/pitfalls.md`。
- **v1.5.0** (2026-06-17) — 新增3种图表：水平柱状图（hbar，含比率标注"4.96x"）、多面板组合图（composite，GridSpec布局，每面板任意图表类型）、架构/流程图（diagram，色块+箭头+分组标注）；新增GLM配色方案（GLM-5.2像素提取柔和配色：`#70A0D0`蓝+`#D79D55`黄，取原图像素均值）；新增斜纹填充功能（`--hatch`，黑色线条，9种图案，打印友好）；新增 `--hatch`、`--show-ratio`、`--ratio-base`、`--horizontal` CLI参数；强制白底输出（出版标准）
- **v1.4.0** (2026-05-17) — 新增4种图表：Kaplan-Meier生存曲线（Log-rank检验、风险表、中位生存、删失标记）、ROC曲线（AUC、95%CI、最优截断点、多模型对比）、堆叠柱状图（构成比、百分比标签）、双Y轴折线图（临床评分+实验室指标同图展示）；扩展数据校验
- **v1.3.0** (2026-05-17) — 新增Okabe-Ito色盲安全配色（Nature Methods金标准）；DPI升级300→600线稿默认；新增PDF/TIFF/EPS输出；增强森林图（权重气泡、I²异质性、事件数列、分隔线）；无障碍Alt Text指南；智能DPI分场景
- **v1.2.0** (2026-05-16) — 新增版本元数据、依赖声明、负触发词、文件结构文档
- **v1.1.0** — 新增中文自动检测、CSV长格式自动转换、空数据校验
- **v1.0.0** — 初始版本：7种图表、4套配色、中文支持、统计标注

---
