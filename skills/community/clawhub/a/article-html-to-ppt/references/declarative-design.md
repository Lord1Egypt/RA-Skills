# 动态设计与原生重建工作流

这是本地开发版的 `engine design` 入口，依赖 `requirements.txt` 锁定的
python-pptx 1.0.2、Pillow 13.0.0、jsonschema 4.25.1、lxml 6.1.1。
Pillow 安全升级要求 Python 3.11 或更新版本；不要在旧解释器中静默回退到 11.3.0。
执行器不接受 Python、JavaScript、表达式、任意路径、远程 URL、SVG、
字体文件或 PPTX 模板。支持的能力由 `schema` 命令给出，未知属性拒绝执行。

## 职责与任务模式

宿主多模态模型逐次识读当前图像，核对文案、区域、视觉层级、素材与数据。
这不是独立 OCR 或自动分层引擎，不应宣称已自动恢复未知字体或图表数据。
原创任务默认由模型提交结构化设计，原生 PPTX 经实际渲染得到设计预览，再视觉修订。
宿主也可按需调用已授权的图片工具制作独立插图或完整外部设计目标。
本地 CLI 不持有图片服务凭证，不自动发起云端调用。

| 模式 | 目标 | 图片工具 |
| --- | --- | --- |
| `create` | 源材料 → 结构化设计 → 原生候选 → PNG 预览与修订 | 可选，不是交付前提 |
| `recreate` | 当前原始图；经授权的修正另存目标并记录差异 | 已有合格目标即可继续 |
| `template` | 保留原生模板 | 路由到 V4 Template，不从空白替代 |

`init --mode new_design/style_transfer` 是 create 的兼容别名；风格图登记为 style 参考。
既有保存任务中的旧 mode 保持原合同，不自动解除外部目标要求。`draft` 仅用于诊断草稿，
不能最终交付。CLI `route --template` / `route --design-target` 可查询意图路由。
`route --template --template-use style` 表示已允许参考模板重新设计，返回 create；
原生模板保留仍使用 template。详细流程见[模板风格设计](template-visual-design.md)。

用户意图已经明确时直接执行。只有显著影响结果的冲突才澄清。品牌规则仅在
本次请求要求时采用。多图分别声明用途、页映射、采用特征与优先级；不自动混合。
同一 PPTX 的画布一致，不同比例只能明确留白适配或拆分交付，禁止静默拉伸。

## 快速开始

所有命令在技能根目录执行；`TASK` 是当前用户已授权的任务目录。

```bash
python3 -m engine design capabilities
python3 -m engine design init --task-dir "$TASK" --task-id example \
  --mode create --width 960 --height 540 --pages 1 \
  --author author-model --audience 产品团队 --target-software LibreOffice
```

默认 create 不需要参考图片。用户提供完整设计图时改用 recreate，再登记图像：

```bash
python3 -m engine design ingest --task-dir "$TASK" --file reference.png \
  --asset-id ref-one --role reference --pages page-1 --source 用户提供的本次参考
python3 -m engine design schema
```

优先用 [紧凑作者输入与局部修订](declarative-authoring.md) 中的样式/来源/图标引用减少
重复模型输出。`context --page page-1 --section content` 按页读取，`--section scene`
用于修改几何；`schema --section node --type text` 仅查询一种节点，完整 Schema 只在必要时读取。
宿主根据当前输入写入内容、设计和场景。
create 必须具有当前设计 brief 与逐页备注。不要用程序假装完成
视觉识读。逐项保留出处及不确定信息；风格图中的业务文案不进入新内容。

装饰商务汇报、原创模板，或需要修复页面趋同/空散时，先读
[装饰商务设计](decorative-business-design.md)。初始化时可增加
`--review-profile decorative_business`：在 `design.pages[].composition` 记录本页主结论的
内容引用、信息关系、构图家族、阅读顺序和层次安排；完整构建要求逐页覆盖。
这不是固定模板，不改变原生对象后端，也不为旧任务追加必填字段。
`python3 -m engine design composition-check --task-dir "$TASK"` 输出构图矩阵与重复风险提示，
供代表页试制及合并后复审使用；没有提示不代表审美、原创性或实际排版合格。

`canvas` 与全部几何使用 pt。将原图像素坐标按 `canvas.width / image.width`
与 `canvas.height / image.height` 等比例转换。声明 `contain` 时，先算留白偏移，
再转坐标。字号、线宽也需换算。不要照搬文档案例中的 1672×941 或固定栏数。

### 五类记录

`task.json` 将四类可独立哈希的记录放在一个受约束的任务信封中；第五类是
构建后的 `manifest.json`、`review.json` 与 `acceptance.json`。

| 记录 | 重要字段 |
| --- | --- |
| `content` | 分页文字、真实图表系列、真实表格单元格、来源、核对状态、备注 |
| `design` | 当前模式、参考用途与优先级、可选外部目标、确认人、原图限制、接受差异 |
| `scene` | 页背景、节点、层级、位置、样式、内容绑定、编辑角色 |
| `assets` | 标识、原始与标准化字节摘要、尺寸、页范围、来源、裁片与真实工具回执 |
| 验收 | 输入版本、代码/依赖/字体、PPTX、实际预览、双重视觉结论、对象编辑行为 |

原生文字节点只引用 `content_id`，不另抄业务文案。换行属于锁定内容；
`spans` 使用字符区间指定混排字体，不将每个字拆成一个形状。
图表支持 column/bar/line/pie/doughnut，底层数据必须来自核对后的用户数据或
可读数值。表格存真实单元格，可指定列宽。形状支持矩形、圆角矩形、椭圆、
直线、箭头、菱形和三角形；路径支持 M/L/Q/C/Z。组内坐标相对父组，z 在组内排序。

不支持的渐变、蒙版、复杂透明效果、自动连接路由、智能文本重排和字体嵌入
应明确披露。复杂插画可以登记为独立图片；不能用整页图覆盖文字获得编辑指标。
图片仅接受已登记素材 ID。可以按明确的编辑要求接受数据图片替代，但同时需要
`required_edit: raster_accepted` 和该页 `raster_acceptances` 的理由与接受人，
并在交付中说明没有原生数据编辑能力。
原始数值完全未知时使用 `unknown_data` 内容记录，只登记描述与不确定项，
不要为满足 schema 填入虚构系列；它只能在明确接受后映射为独立图片。

### 素材与真实图片工具

```bash
python3 -m engine design crop --task-dir "$TASK" --from-asset ref-one \
  --asset-id illustration-one --role illustration --pages page-1 \
  --source 本次图中的独立插画 --source-crop 100 200 180 120
python3 -m engine design image-request --task-dir "$TASK"
```

裁片先真正解码并裁切再嵌入，不重复嵌入整张原图；原始字节另存。
尺寸、压缩字节、总像素、帧数和资源总量均受限，仅允许静态 PNG/JPEG。
不提供对任意图通用的去底阈值；需要处理时由宿主获得独立合格素材并重新登记。

`image-request.json` 仅是待调用请求，`generated: false`。宿主检查其可见内容，
实际调用可用的图片工具，然后登记返回的文件；`--tool-result` 接收真实回执：

```json
{"tool":"实际工具名","model":null,"invocation_id":null,
 "result_sha256":"工具返回图片的真实SHA256",
 "prompt_sha256":"实际发送提示词的真实SHA256"}
```

后端可验证字节对应，不能独立证明外部工具确实被调用；回执真实性由宿主负责。
没有图片工具时，create 继续程序设计和真实预览，已有目标的 recreate 继续还原。
仅在用户明确要求图片生成资产且没有合格替代时披露该资产缺口。
程序预览由 manifest 的 design_origins 记录，不能伪装成 generated 或 provided_design。

## 构建、修订与审核

```bash
python3 -m engine design validate --task-dir "$TASK" --complete
python3 -m engine design preflight --task-dir "$TASK" --isolation auto
python3 -m engine design build --task-dir "$TASK" --isolation auto
python3 -m engine design status --task-dir "$TASK" --build-id "$BUILD"
python3 -m engine design review-template --task-dir "$TASK" --build-id "$BUILD"
```

preflight 使用实际 LibreOffice 样本与 pdffonts/pdftotext 检查所选字体和当前文本字符，
按字体字节、样本和渲染器缓存。回退或缺字返回 font_review_required；缺少工具返回
preflight_unavailable。它是提前发现问题的样本检查，不能替代成稿逐页审核。
模型能力由宿主如实判断，capabilities 只检测本地工具，不声称检测到了当前模型的能力。

build/capabilities/preflight/review-template 默认返回短摘要与文件路径。显式 `--full`
取得完整结果；`inspect --task-dir "$TASK" --build-id "$BUILD" --page page-1` 读取某页证据。
state.json 是当前任务的接续摘要，task.json 与 manifest 才是审核绑定的事实来源。

每次构建创建私有随机目录；不覆盖旧候选。固定 worker 运行于独立进程，限定
输入资源和输出字节、构建墙钟时间。POSIX 系统另设 CPU、文件大小和描述符限制；
Windows 不声称具备这些 POSIX 限额，超时使用进程树终止。macOS 模式使用 Seatbelt
限制文件内容读取、写目录和 IP 网络；目录元数据与祖先目录遍历为运行时保留。
LibreOffice 本地 IPC 仅允许本次构建目录中的专用 Unix socket。
宿主禁止嵌套 sandbox 时需要宿主允许这一隔离启动。
默认 `auto` 在 Darwin 且存在 `sandbox-exec` 时选择 `macos`，其他环境选择 `host`。
显式选择 `macos` 而能力不可用时仍失败；启动失败也不会静默改用 `host`。
macOS 宿主明确不允许嵌套隔离时，可显式选择本地 `--isolation host`。

**PPT 质量验收与 OS 隔离策略分开。** Linux、Windows 和 macOS 的 `host` 模式
均可在全部质量门禁通过后生成最终 ZIP；manifest 和 acceptance 如实保留隔离
未验证的记录与提示，交付通过不表示运行环境通过安全认证。
有强制隔离要求时，构建增加 `--require-os-isolation`：缺少可用隔离即拒绝启动
worker。此策略写入审核绑定的 manifest，后续省略参数也不能解除；`review` 和
`deliver` 同样可加此参数进一步收紧验收。旧 manifest 缺少策略字段时保持原来的
严格规则。Linux/Windows 专用 OS 隔离适配器尚未实现，严格模式不能在 host 上通过。

### 跨平台运行条件

先运行 `capabilities` 检查 `execution` 和 `render`。三个系统都需要 Python 依赖、
LibreOffice、Poppler 的 `pdftoppm`、Fontconfig 的 `fc-match` 及任务实际使用的字体。
工具缺失时应安装对应依赖，不能填造预览或把字体状态改为通过。
引擎从 PATH 发现工具；LibreOffice 另支持 macOS 的标准应用目录与 Windows
Program Files 的标准安装位置。自定义安装的工具目录应加入启动 CLI 的 PATH，
worker 只继承已发现工具的目录，不透传全部环境变量或 API 密钥。

Windows 可使用原生 Python 入口 `python -m engine design`，以上多行 Bash 示例
在 PowerShell 中改为单行执行。可通过 MSYS2 的 UCRT64 Fontconfig/Poppler 包提供
`fc-match.exe` 和 `pdftoppm.exe`，将相应 `ucrt64/bin` 加入 PATH，并确认 `fc-match`
实际匹配任务字体。任务放在本地盘的普通目录；拒绝符号链接、junction/reparse
point、保留设备名和 UNC 网络目录。Windows 使用持有目录句柄的文件边界；
Linux/macOS 保留原有 descriptor-relative 文件边界。

这些适配不等于 PowerPoint/WPS 已通过兼容性验证；目标软件的实际编辑检查仍是
独立必过项。三系统回归由 CI 矩阵执行，未运行的平台测试不能声称实机通过。

`--no-preview` 只保留未渲染候选。实际预览使用私有 LibreOffice 配置目录，
从最终候选 PPTX 转 PDF，再由 Poppler 生成逐页 PNG。目标图不冒充预览。
`compare-<page>.png` 左为批准目标、右为实际预览。区域 RGB 误差仅用于找差异，
不代表审美分数或“99% 还原”。

审核须独立检查设计适当性与重建保真，并核查内容、对象编辑和字体。
复刻任务记录原图限制，不因审美偏好重排版。修改内容、参考用途、目标、素材、
场景、PPTX、预览、渲染器代码或字体，均会使原构建审核失效。同名文件也按字节检查。
新构建可通过 `review-template --inherit-from previous-review.json` 继承未变页的独立证据；
系统同时核对内容、备注、设计、素材、对象结构、实际预览及全局环境，不能仅凭像素相同
继承。保留原观察与来源审核哈希，修改过的页面仍从否决态开始。全局字体、brief、画布、
页序或渲染器变化使相关证据失效。全稿构建、哈希、来源/结构与目标软件编辑验证仍执行。
审核人 ID 必须与作者不同，但系统不提供审阅者身份认证；禁止伪造第二身份。

```bash
python3 -m engine design build --task-dir "$TASK" --parent-build "$BUILD"
python3 -m engine design review-template --task-dir "$TASK" --build-id "$BUILD" \
  --output review-draft.json
python3 -m engine design review --task-dir "$TASK" --build-id "$BUILD" \
  --review-file review-draft.json
python3 -m engine design deliver --task-dir "$TASK" --build-id "$BUILD" \
  --review-file review-draft.json
```

`review-template` 生成待填写的否决态审核表，不预填通过。审核表必须绑定构建
manifest 的真实 SHA256，覆盖全部页面与关键内容对象，记录具体观察和目标软件
中的打开、改字、改数据、替换素材等实际动作。子版本修订预算耗尽时保留问题，
不能自动批准。新目标变更必须重新确认并重新审阅。

`observed_node_ids` 的覆盖对象是该页所有带 `content_id` 的节点，包括页码、来源、
脚注、图表与表格，不能只填写几项代表对象。用 `objects.json` 的 bindings 与 scene
逐一核对，检查后再记入；不要预填全部ID冒充已审阅。并行审阅者交付各自真实页面与
对象范围，合并者检查覆盖完整，不替别人补造观察。

启用 `decorative_business` 的候选还须填写 `deck_composition`：检查当前合并稿的整册
构图、视觉层次和阅读路径，记录实际观察并覆盖所有页面。它从 `revise` 开始，不能
因为逐页审核通过或继承了未变页证据就自动通过。先看总览定位重复，再打开相关单页
检查文字归属、形状内部的安全区、连接/遮挡、色彩主次和小字；不使用对象数、空白率或
图形品种数替代视觉判断。缺少整册审核会阻止该 profile 的最终交付。

整册观察分别覆盖构图多样性、全册规整度、叙事完整性：比较正文骨架，同时核对
标题/导航和线条的稳定性、章节起点及总结/决策/结束的实际顺序。总览中的疑似文字
碰撞应在同一构建的实际大图或局部确认；误报撤回时保留原因，不能凭缩略图误读改版。
具体方法见[装饰商务指南](decorative-business-design.md)。这些补充使用既有字段，
不要求旧任务增加新的JSON合同或每份短简报补齐目录、章节和感谢页。

create 无外部目标时 reconstruction 必须为 not_applicable，其他维度仍须独立批准；
有外部目标的页面必须为 pass。不能把自身预览当目标来证明保真或审美。
继承页仅复用已有有效审阅，不冒充新审阅；最终 ZIP 含继承的审阅记录和来源 manifest。

最终 ZIP 包含原始输入、逐页目标映射、可编辑 PPTX、PDF、实际预览、对照图、
对象清单、验收与编辑限制。`deliver` 每次重新核验当前字节，不信任之前的成功
状态；相同构建不重复覆盖交付包。

## 能力与发布边界

本流程是模型辅助工作流，尚不是无人值守图片识读产品。复杂参考的解析质量、
字体识别、遮挡、原图内数据冲突仍需要宿主和独立视觉审阅。
仅对子进程化或 JSON 校验通过，不宣称完成系统隔离。
素材登记角色属于语义声明；伪装文字的插画仍需审阅者检查。
外部 PPTX/SVG/字体不进入此新入口，模板模式按原独立路由处理，不能继承新入口
的安全结论。正式平台审核与 PowerPoint/WPS 实机兼容性需各自验证。

macOS 隔离部署时可运行固定探针，检查真实的拒绝结果，而不是根据平台名称猜测；
这不是 host 模式交付的前置步骤，也不提供 Linux/Windows 隔离证明：

```bash
python3 -m engine.design_scene.isolation_probe --output-dir "$TASK/isolation-check"
```

探针只访问自行创建的哨兵文件，不读取用户私有材料。内存由输入字节/像素/节点
上限约束；尚无 OS 级常驻内存限额。PNG/JPEG 登记解码发生在宿主进程，因此
不把渲染 worker 的隔离证据扩大为所有依赖解码路径均通过部署安全评审。

实现依据已核对的公开接口：
[python-pptx 原生对象](https://python-pptx.readthedocs.io/en/latest/api/shapes.html)、
[LibreOffice 命令行转换](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html)。
