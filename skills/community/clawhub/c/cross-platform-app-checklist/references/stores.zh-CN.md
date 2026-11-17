# 商店提交与发布检查

[English](stores.md)。公开来源核验日期：**2026-10-22**。
本指南细化既有 **P4、P8、P9、W4、X6**，不增加或重编号清单 ID。
新上架、更新、应用转移或分发渠道变更时使用；只读取实际选择的渠道，
无需为了完成清单加入所有商店。

## 适用范围与证据

先记录 `商店／包模型 × OS／架构 × 国家地区 × 应用类型`，以及开发者
账号、应用／包 ID、版本、产物哈希、测试轨道、目标受众和账号、UGC、
广告、支付、受监管服务等功能。Mac App Store 与站外 Developer ID
下载、Microsoft Store 的 MSIX 与托管 MSI/EXE 都是不同渠道。厂商的
Android、HarmonyOS、快应用也不是同一个提交目标。

渠道章节中的 **R** 表示该路径的明确强制要求；**C** 表示触发所述条件后
必须满足；**A** 表示建议或可选计划。它们与 **verified／to do／needs
device／not applicable** 是两组不同信息，不能把建议写成必然拒审理由。
每项适用规则记录官方直链、核验日期、触发条件、证据与负责人。
后台专属规则无法读取时，交由账号负责人核验并标记 `to do`，不能当作没有要求。

本指南不额外授权发布、修改开发者账号、接受协议、购买证书或联系审核人员。
在用户已授权范围内准备具体可审核的材料，未授权的外部操作保留到最后处理。

## 通用发布证据

下表是本技能采用的检查方法；是否属于商店硬性规定由后面的渠道章节决定，
不得把一家商店的规则套用到其他商店。

| 检查内容 | 证据／适用条件 | 既有 ID |
|---|---|---|
| 主体与权利 | 账号所有者、适用的个人／组织验证、应用归属、商标／内容／再分发授权、当前协议、提交者权限。按地区或变现条件核对交易者、商户、税务信息。后台截图脱敏，不在报告中存放凭据。 | P9、W4 |
| 包与更新身份 | 对比产物和后台的 ID、签名、版本／构建号、架构、最低 OS 及上一版。实测更新；涉及转移、改 ID 或商店版与站外版共存时分别验证。重装不等于升级。 | B7、W4、X6 |
| 隐私与权限 | 盘点应用和 SDK 的收集、共享、保留行为，对照隐私政策、后台披露与最终 manifest／entitlements／沙盒权限。测试首次授权、拒绝、撤销、删除。“不收集”也需要依据，不能省略必填表单。 | P1–P6、P9 |
| 受众与条件功能 | 重新核对年龄、内容、儿童、广告、UGC 运营、账号创建／注销、第三方登录、游戏、生成式 AI 和受监管服务；保留类别／地区依据及功能测试。没有账号创建可能使账号注销条款不适用，不会使全部隐私检查不适用。 | P4、P9 |
| 支付与地区条件 | 区分数字／实物商品、应用／游戏、商店地区和已加入的替代支付计划，验证允许的购买、恢复、续订、退款、取消流程。没有支付可说明 P8 不适用；不能共用一个全球外链购买策略。 | P8 |
| 商店素材与无障碍声明 | 按当前渠道核对必填字段、素材规格、应用与商店页语言、截图／图标授权、支持／隐私链接、真实功能和设备要求。逐语言预览商店页；无障碍声明需要功能测试证据。 | D2、D5、I5、P9 |
| 审核可达性 | 受限功能提供专用可用测试账号或允许的演示模式、权益、样例数据、硬件说明及可达后端。从全新安装验证地区、网络、验证码／MFA 依赖。凭据只填安全审核字段，不放公共介绍或仓库。 | P9、X6、X8 |
| 安装后的正式产物 | 归档准确产物和验证报告，以普通用户实测安装、启动、敏感功能、升级、卸载；使用商店沙盒／签名身份并覆盖支持的 OS、架构、硬件边界。自动测试数量、后台人工检查、真机检查分别记录。 | W4、X4、X6、X9 |
| 发布与恢复 | 区分审核批准和已发布，记录轨道／分支、国家、价格、操作人、停止条件，演练可用的灰度／暂停控制及前向修复。停止灰度或下架不会移除已装版本，也不会撤销数据迁移；降级仍须满足 B7。 | B7、W4、X6 |

隐私、注销、UGC、儿童、支付的行为测试见 [permissions.md](permissions.md)，
签名和安装包见 [desktop.md](desktop.md)，真机与发布证据见
[testing.md](testing.md)。

## Apple App Store：iOS、iPadOS、macOS

- **R：应用记录与审核。** 团队、bundle ID 与应用记录一致；核对
  [应用记录要求](https://developer.apple.com/help/app-store-connect/create-an-app-record/add-a-new-app/)
  和当前 [提交 SDK 要求](https://developer.apple.com/news/upcoming-requirements/)。
  按 [提交前检查](https://developer.apple.com/app-store/review/guidelines/#before-you-submit)
  准备完整资料、可用测试入口和在线服务。
- **C：Mac App Store。** 2.4.5 要求适当沙盒、Xcode 支持的独立应用包和
  Store 更新，不使用第三方安装器／更新器替代。检查最终签名的沙盒能力并
  实测文件和设备访问。[Mac 专项要求](https://developer.apple.com/app-store/review/guidelines/#hardware-compatibility)
  与 [站外 Developer ID／公证路径](desktop.md#w4-packaging-and-distribution--p0-for-release)
  不同，公证不代表 App Review 批准，也不能替代 iOS／iPadOS 的商店提交。
- **C：功能与地区。** 对实际功能应用 P4／P8／P9，填写
  [加密出口信息](https://developer.apple.com/help/app-store-connect/manage-app-information/overview-of-export-compliance/)
  及适用类别／地区材料。除原生目标外，还要记录 iPad 应用在 Mac／Vision Pro
  的兼容分发设置（W4）。
- **A／C：无障碍声明。** 当前 [无障碍标签指引](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/overview-of-accessibility-nutrition-labels/)
  描述自愿填写并向必填过渡；发布时以当前后台要求为准，已作声明必须有证据。
- **A：控制发布。** TestFlight 与 [分阶段更新](https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases/)
  可用于验证；自动更新灰度不会阻止用户手动下载。记录所选发布方式和前向修复流程。

**证据：** 已处理构建／archive ID、最终 entitlements 与隐私报告、后台
功能问卷、审核入口演练、安装结果及发布选项。只有本地 archive 不等于
提交获批，新应用和每次更新都要重新检查。

## Google Play

- **R：主体与包。** 完成适用的 [开发者身份验证](https://support.google.com/googleplay/android-developer/answer/10841920?hl=en)，
  核对永久包名、递增 versionCode 和 [应用设置](https://support.google.com/googleplay/android-developer/answer/9859152?hl=en)。
  遵循所选 [产物格式与发布轨道](https://support.google.com/googleplay/android-developer/answer/9859348?hl=en)
  及 [Play App Signing](https://developer.android.com/studio/publish/app-signing)，
  分别记录上传证书和实际分发证书指纹。
- **R／C：应用内容声明。** 核对 [App content](https://support.google.com/googleplay/android-developer/answer/9859455?hl=en)
  中访问方式、广告、受众、评级、隐私／Data safety、敏感权限和类别声明。
  P4／P8／P9 提供实际行为检查，包含条件适用的账号注销。发布时核对当前
  [目标 API 政策](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en)
  与 [原生 page-size 要求](https://developer.android.com/guide/practices/page-sizes)，
  不复制旧截止日期。
- **C：正式发布权限。** 新建个人账号适用
  [封闭测试与 production access 流程](https://support.google.com/googleplay/android-developer/answer/14151465?hl=en)。
  按当前账号条件核对测试者数量／持续时间和批准结果；内部测试不等于完成此门槛。
- **A：发布控制。** 选择正确测试／正式轨道、地区和设备；
  [发布状态](https://support.google.com/googleplay/android-developer/answer/9859751?hl=en)
  与上传成功不同，验证预期账号能实际获取版本。

**证据：** 后台配置和声明、bundle 与实际交付 APK 检查、设备上的签名升级、
审核账号演练、适用的测试轨道／正式发布资格。模拟器或旁加载 debug APK
不能证明 Play 设备可用范围。

## Microsoft Store：选择 MSIX 或托管 MSI/EXE

[提交指南](https://learn.microsoft.com/en-us/windows/apps/publish/get-started)
区分两条路径。先在 Partner Center 保留产品身份，核对账号、包身份、年龄、
能力及认证说明。Store 会重新签署 MSIX/AppX，**不要求购买自有可信 CA
证书用于 Store 提交**；站外 MSIX 分发是另一回事。

**C：非游戏、仅 PC 的 HTTPS MSI/EXE 路径。** 当前
[Store Policies 10.2.9](https://learn.microsoft.com/en-us/windows/apps/publish/store-policies#102-security)
要求带版本且提交后内容不变的 HTTPS 地址、独立离线安装器、静默安装
（允许 UAC），以及安装器和**全部内含 PE 文件**使用可信 CA 证书签名。
逐个检查二进制，从准确 URL 实测安装／升级／卸载；不要套用到 MSIX。
本次依据为 **7.20**，发布于 2026-09-15，**2026-10-22 生效**。
[MSI/EXE 认证帮助页](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/app-certification-process)
仍写“建议签名”，此处以当前正式政策为强制依据，提交前重新核对冲突。

**C：实际行为。** 按条件核对 10.3 测试账号／在线服务、10.5 个人信息、
10.8 支付与 11 内容／年龄／UGC。游戏与非游戏 PC 应用支付规则不同（P8），
不能把 Apple 登录条款或 Play 注销 URL 表单当成 Microsoft 要求。

**证据：** 包／安装器身份与签名清单、固定 URL 哈希、普通用户生命周期测试、
适用的 WACK／认证报告、商店资料和可用审核账号。WACK 是预检，不是商店认证。

## Flathub

- **R：收录与打包。** 按当前 [requirements](https://docs.flathub.org/docs/for-app-authors/requirements)
  检查 app ID 权限、再分发许可、声明的离线构建源、通过验证的 AppStream
  元数据、desktop entry／图标、最小静态权限与适用 portals。核对目标架构
  和受支持 runtime，在没有本地权限覆盖的环境测试。
- **C：实际提交的人工作业边界。** 当前
  [生成式 AI 政策](https://docs.flathub.org/docs/for-app-authors/requirements#generative-ai-policy)
  要求披露已知的 AI 生成应用／打包材料；Flathub manifest 不允许 AI 生成或
  辅助。agent 不能创建／自动化提交 PR，也不能生成其 commit message、
  描述、评审交互；提交者不能请求 AI agent 评审。实际 Flathub 提交应由人
  处理这些步骤；披露也不保证收录。此限制只针对该渠道，不扩大到无关项目工作。
- **A：身份与展示。** [开发者验证](https://docs.flathub.org/docs/for-app-authors/verification)
  与 [商店页质量检查](https://docs.flathub.org/docs/for-app-authors/metainfo-guidelines/quality-guidelines)
  影响信任／推广；quality guidelines 明确不是全部都属于初次提交硬性要求，
  应与收录要求分开。

**证据：** 人工确认的来源与权利、源码／runtime／commit 标识、
[提交构建和 lint 结果](https://docs.flathub.org/docs/for-app-authors/submission)、
实际安装的沙盒／portal 测试，以及确实提交后的审核结论。本地 `.flatpak`
或应用仓库 PR 合并都不等于 Flathub 收录。

## Snap Store

- **R：发布身份。** 注册发布者与 snap 名称，核对包资料和声明架构，检查
  [上传与自动审核流程](https://ubuntu.com/docs/snapcraft/9/how-to/publishing/publish-a-snap/)。
- **C：限制模式与权限。** [权限申请](https://snapcraft.io/docs/permission-requests)
  对 classic 及指定高权限／自动连接需要批准；`devmode` 不能发布到 stable。
  测试实际 [confinement](https://snapcraft.io/docs/explanation/security/snap-confinement/)
  和接口连接，本地 `--devmode`、`--dangerous` 或手工连接不能证明 Store 安装行为。
- **A：发布控制。** 选择 [track／risk channel 与渐进发布](https://ubuntu.com/docs/snapcraft/9/how-to/publishing/manage-revisions-and-releases/)，
  分开记录 revision 与显示版本；变更正式渠道前验证 Store 安装、从旧 revision
  refresh 和数据兼容。上传并不额外授权推广到 stable。

**证据：** 发布者／名称、revision／channel、自动审核结果、必要人工授权
链接、安装后的 `snap connections` 和 refresh 测试。商店内容／服务条款
中的 [内容、许可与第三方隐私权要求](https://ubuntu.com/legal/terms-and-policies/snap-store-terms)
仍适用，但不能凭空要求本渠道提供 Play Data safety 或 IARC 表单。

## 中国大陆 Android：代表渠道

逐个选择实际渠道与地区。以下不是所有 Android 商店的统一政策，也不是
穷尽的法律适用判断；APK、HarmonyOS 和快应用分开记录。其他实际发布的
商店仍需读取其官方规则并保存后台证据。

| 渠道／来源 | 该渠道提交前检查 | 2026-10-22 来源读取范围 |
|---|---|---|
| 华为 AppGallery [审核政策索引](https://developer.huawei.com/consumer/cn/doc/doccenter-submission/50000) | 获取所选平台／地区的应用审核、资质／备案、年龄及隐私标签指引，记录主体与准确包类型。 | 读取官方索引摘要，详细页面未完整可读；负责人需在后台核验，不能由索引推断已满足细则。 |
| 小米 [当前上架要求](https://dev.mi.com/xiaomihyperos/documentation/detail?pId=1322) | 核对主体／应用信息、资质／备案，实测首次隐私同意／拒绝、同意前 SDK 行为、内外政策一致、适用的账号注销和付费功能测试账号。 | 已读完整公开要求，页面日期 2025-09-02。优先于旧 MIUI 截图／流程说明，发布时再查后台变更。 |
| OPPO [发布入口](https://open.oppomobile.com/new/developmentDoc/info?id=10035) 与 [审核规范迁移入口](https://open.oppomobile.com/new/developmentDoc/info?id=10071) | 跟进迁移后的当前应用／资质规则、隐私审核、测试入口，在后台核对地区及支付／内容条件。 | 读取官方索引摘要；公开 HTML 依赖 JavaScript 且指南迁移，详细规则仍待负责人后台核验。 |

**C：地区／服务。** [工信部 APP 备案通知](https://www.miit.gov.cn/jgsj/xgj/wjfb/art/2023/art_dd783a581c9644a4aee10afa582811db.html)
针对在中国境内从事 APP 互联网信息服务的主办者。记录是否属于此范围，
需要时保留备案／许可和展示编号；新闻、游戏、医疗、金融等行业资质取决于
实际服务与渠道。软著证明、互联网服务备案、行业许可、隐私同意是不同检查，
不能由中文界面或一家商店的批准推导通用备案／支付／注销义务。

**证据：** 当前官方细则／后台记录、主体与包对应关系、适用资质、隐私与 SDK
测试报告、设备安装／签名升级和审核账号。规则或适用范围未确认时标记 `to do`
并指定负责人；Play 构建通过，不能让未测的国内渠道变成 `not applicable`。

## 其他实际选择的分发渠道

以下是条件化入口，不是额外必须上的商店：

- **WinGet 社区仓库：** 按 [manifest／安装器验证](https://learn.microsoft.com/en-us/windows/package-manager/package/winget-validation)
  与包政策检查发布者 URL、哈希、架构、静默参数，实测安装／升级／卸载。
  manifest 收录不代表 Microsoft Store 认证。
- **Homebrew Cask：** 检查 [收录条件](https://docs.brew.sh/Acceptable-Casks)
  和 [cask 配方](https://docs.brew.sh/Cask-Cookbook)，核对上游版本、URL、
  校验和／允许的例外、支持平台；不能绕过 macOS 安全要求（W4）。
- **F-Droid 主仓库：** 若选择该渠道，核对 [源码与依赖收录要求](https://f-droid.org/docs/Inclusion_Policy/)，
  计划 flavor、签名和更新路径。带专有 SDK 的 Play 产物不能假定适用，
  也不能悄悄删除产品功能。
- **站外下载／发行版仓库：** 按所选仓库／安装器的政策及 W4／X6 保存
  签名、更新信任和恢复证据。一个 `.deb`、`.rpm`、AppImage、DMG 或 MSI
  不等于桌面软件中心已经审核通过。

## 报告记录

应用、产物公共信息记录一次；不同商店、包模型、地区、功能触发条件的结果
不同时拆行。下表仅为示例，**不是实际提交结果**：

| ID／渠道 | 规则等级／触发条件 | 状态 | 证据／下一步 |
|---|---|---|---|
| W4／Microsoft 托管 MSI | C；非游戏 PC URL 路径 | to do | 2026-10-22 核对 10.2.9；待签名安装器及所有 PE，保存固定 URL 哈希和普通用户安装记录。负责人：发布工程师。 |
| P9／Apple／账号删除 | C；没有账号创建 | not applicable | 明确本版没有访客、自动、外链或应用内账号创建；增加账号时复查。隐私检查仍适用。 |
| X6／Snap／摄像头 | C；发布摄像头功能 | needs device | 记录 revision、channel，负责人在支持硬件测试 Store 安装、接口权限、采集／拒绝／refresh。 |

后台和审核人员证据与本地测试分开记录。编写本指南时没有操作真实商店账号、
提审或验证商店批准。正式发布时重读官方来源和所选后台，不把旧 SDK 截止日、
测试人数、截图尺寸、费用或审核时长写死到项目代码。
