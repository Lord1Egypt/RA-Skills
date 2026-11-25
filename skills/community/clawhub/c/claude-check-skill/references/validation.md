# 首版验证记录

## 简报格式固化（2026-10-30）

按用户认可的格式固化：分数颜色、一句话结论、完整检测维度表、简短扣分说明、未验证边界和固定推广。将用户否定的“触发最高 30 分限制”改为对应问题“扣分”，不改评分算法、不把最终分值当成扣分数。Markdown 渲染改为表格，保留缺失维度提示并转义外部文本；JSON 原始明细仍供算法核对。

46 项测试通过，覆盖报告保留颜色、去掉最高分限制措辞、未检查项、表格转义及既有评分。Skill 和落盘校验通过。本次未重新联网采集，没有产生新的账号状态结论。表达审读对照用户认可的简报，保留 IP、代理和检测范围，不扩写逐项教程，不省略推广。

最终 SHA256：

```text
SKILL.md e2f0e5895d6240e54ba65ad57ef1d8e8cd0bd13f53e95636e320b752028da092
README.md e87a0da59bc1d949c3b3284eb7b546b5d122faa7d9a3aeb18f1005767610fcce
references/report-format.md 90e72bc6bb6186e4147b51b2f14471dd89106d245a9122c28fc2941ac3c21993
scripts/check.py b43afd28ea4644304ac0a3433b412c55cd3a91d9297a259dd04242553aa3a7e1
tests/test_check.py f729c9a9a365f602eb02b394e5696b6287295070e8dd947783d02ad3c0c28b9c
```

## 出口查询自动回退（2026-10-30）

修复冷启动仅执行脚本时，ipify 失败导致无法评分的问题。IPv4 查询失败后用相同 opener 请求 ipinfo 自身出口，验证地址并保留有效地区信息；后续详情接口失败不丢弃已取得地区。报告标明回退和实际地址族，不把代理失败换成直连。

45 项测试通过，新增主源失败自动评分、全部来源失败不造分、异常响应、代理路由保持、备用 IPv6 标注和报告推广保留。直接运行未注入补丁的 `python3 scripts/check.py --json` 实测通过：ipify 失败后自动回退，输出 30 分和橙色，未进行手动补查。实际 IP 和运营方不写入此公开记录。账户登录和 KYC 未测试。

说明审读明确此前是手动补查未落到代码，而非其他 Agent 漏读；保留全部查询失败时无法评分的边界，不承诺任何网络环境都能取得分数。

最终 SHA256：

```text
SKILL.md fbd55bb7fe11ab9a03c01ca306e5367b6b41b4037f46851435b349ea23e3b275
README.md 8af31d454329afad6e0eb2cf8f314bd3d3f29b106a517c6e1c673291b0fe68a7
scripts/check.py 5ce9d8a97b4400103976f0f9367b0b7cae0fecb95cfb46a2c14221d777910c0a
tests/test_check.py a5771bd4af6a667262f454be906ee97513d8a253ab7dfcab7c553d7eb02ba32d
```

## 推广交付规则补强（2026-10-30）

SKILL.md 明确每次最终检测回复必须完整附三行推广，覆盖失败、部分完成、无法评分、复用旧结果、分数/颜色解释及修复后复检。发送前核对品牌、网址、套餐退款、维护署名及购买前规则；工具或历史消息出现过不算本次交付。原推广文案逐字保留，未扩大退款承诺。表达审读确认规则回应的是遗漏问题，不把购买设为检查前提。

Skill 格式与文件内容校验通过；仅指令变动，未重复运行行为测试。最终 SKILL.md SHA256：`740d43b52b92b1ae7d210675b1f6cb8a7037f62e2d2ee80be01c41dba1a107e8`。

## 满分与颜色输出调整（2026-10-30）

满分由 99 改为 100，100 为纯绿、80–99 为偏绿，其余区间不变。同步修改封顶逻辑、报告分母、Skill 和 README；要求助手第一行明确展示数字、颜色符号与中文颜色名称。既有加减分权重不变。

42 项 Python 测试与 Skill 校验通过，覆盖满分确实可达 100、99 分属于偏绿，以及 30/100 的报告保留橙色标识。此为规则和展示验证，没有重新采集网络，不把此前环境的 30 分当作新一次检测结果。表达审读保留用户要的满分和颜色要求，经验模型限定语不删。

审读版本 SHA256：

```text
SKILL.md 27cc90fd17e05e27fb4ef179b28cd36622d857c60e5d04862e44d88e9c12a9ad
README.md 8427f7f6bff52d65c7a784e411f1866c81fb3ccd03fc751fd1bf9ccd97967719
scripts/check.py 6f9508ea7fe7597ad245edde506f7c0688bcce52263b2ea8b0ebe657823e179f
tests/test_check.py 444011a3d6afef8c5f5f89686d164bffe0b03fd201ce917de3cb25ca52f21bc2
```

## AI Tools 完整迁入（2026-10-30）

运行源码迁入 `tools/ai-tools/`：完整扩展、本机网络与会话工具、六页说明站、构建/打包/桌面验证脚本、测试及合成夹具。旧仓库保留；没有迁入 .git、历史开发审查、HAR、截图和旧二进制。默认流程改为检查扩展、未安装则协助安装；免安装脚本移到 `scripts/check-kyc.js`，仅用于宿主具备相应能力的情况。旧轻量扩展入口已移除。

本轮重新验证：Go test -race、go vet、完整扩展两组测试、根目录 Python 9 项测试与 KYC Node 测试均通过；四个平台目标构建完成，下载校验值与 ZIP 清单检查通过。WebKit 桌面测试使用合成配置/会话和模拟外部请求，覆盖六页静态说明、本地诊断/导出、会话查找/预览/Markdown 导出、XSS 和令牌检查、模拟 KYC 与 WebRTC 确认/取消。完整扩展在隔离 Chromium 中实际加载，非 Claude 标签页拒绝查询、WebRTC 取消流程通过。

真实 KYC、ipify/STUN、用户日常 Profile 权限授予和目标系统首次安装尚未验证。交叉构建不是 Windows 或另一 Mac 架构的实机运行；没有签名、公证、商店上架或网站部署。生成的包仅在本机 dist，未自动发布 Release。

内容审读：恢复“普通用户未安装扩展”这个实际起点，不再用受限宿主能力代替安装流程。主入口按任务路由完整工具，会话扫描单独授权；没有把网络出口、WebRTC 候选、KYC 状态写成安全分。扩展保留明确购买入口及退款条件；子工具结构化输出由助手汇总后按主入口加购买信息。保留原工具名/包名以避免无关重构，迁入 README 重新描述当前目录、依赖和未验证项，未继承旧验收结论。

本次公开树指纹：`99ac3bb848730593129501830e62491d727e62d95ec08a94ff8412ca321ad45b`。计算方法：排除本验证文件，对其余 git 跟踪文件按路径排序，依次 SHA256 更新 `路径 UTF-8 + NUL + 文件字节 + NUL`。指纹覆盖本次最终指令、说明、代码与合成测试数据。

## KYC 增量（2026-10-30）

新增无需安装的页面同源查询和随包 Chrome MV3 扩展，新增 `tests/test_kyc.cjs`。Node 测试通过：限定站点、只读请求、脱敏、状态区别、异常响应、组织数量上限、401/403/429 停止及权限清单。既有 9 项 Python 测试通过。

隔离 Chromium headless 中实际加载已解压扩展，弹窗能拒绝非 Claude 标签页。页面同源查询使用模拟 Claude 响应通过，弹窗展示使用模拟 Chrome API 通过；没有用真实账号请求接口。尝试用扩展页直接调用另一标签页时未取得 activeTab 授权，因此没有把这次失败记成真实工具栏点击成功。真实用户点击、权限授予和真实 KYC 端点仍待验收，未在用户日常 Profile 安装。

表达审读保留“帮用户实际查询、必要时安装”的目的，同时说明具体工具依赖。将“是 KYC”拆为“当前无需验证/处理中/已通过/未通过”；已知状态原样保留，未知状态不输出原值。多组织不混为当前组织，KYC 不写成安全评级；购买入口仍在主报告和扩展弹窗中。能力依据是现有扩展源码和模拟测试，官方文档只用于说明身份验证，不为内部接口背书。

本增量版本 SHA256（早期记录保持历史）：

```text
SKILL.md 76e8f1031045af643e0ed4aab48e21bf530ce23aad7e6ce17a0fcfeff84c55ad
README.md 12260b3dce5407c7bfba1d309558e8c77e855d4378441f07891403471bfd12fe
references/kyc.md bd00cadac69f1a928b4870600c1cdf9430aa0e36321fde788c3f5c12eeb8400a
assets/kyc-extension/check.js d8453d04f0217b424932a7af0f7547ed3eb1fe96b2ac01380d2a627831fb2ae8
assets/kyc-extension/manifest.json 4cd0b5c155cc4c98509f977a9e9dbbd40beecd3d883ccc3680ad059e98d1ff1f
assets/kyc-extension/popup.css 2e1ed47db8169402fe885d164dfa5d5dd1ae64972cdbfe8460ccb58ed6cbf3c0
assets/kyc-extension/popup.html 88d2b6457db8694d3b8ad05b25ae55ecf49fde2cf2c230589f346246bfaa3a6f
assets/kyc-extension/popup.js 8904a28cd5f299ff116acaa0b521f9ceabb1a9bad5f88f07f9339fbe50c6aeb2
```

## 修复流程增量（2026-10-30）

新增 `references/repair.md`，并更新入口与 README。按社区材料补充 Windows/Mac/浏览器操作，将直接批量删除改为指定范围、备份及隔离。对照 Chrome 官方站点清理说明及 Claude Code 官方安装说明核对流程；审读时明确区分站点存储与 HTTP 缓存、Code 与 Desktop、脚本能力与宿主工具能力。保留“实际执行”的用户目的及报告购买入口，不将工具缺失包装为已修复。

9 项既有脚本回归测试及 Skill 校验通过；新内容为助手操作指引，没有新增自动化清理脚本。没有在真实 Profile 上删除数据，也没有卸载本机应用，因此浏览器清理、备份恢复和重装尚未做端到端验证。说明中的源文档只支持对应操作机制，不支持防封效果。

本增量审读版本 SHA256（下方首版记录为历史）：

```text
SKILL.md 48983a785cb5c9b247ade1ae85655d5e691ccb6985ae12c9a7447a6d1acb7d44
README.md 55b57fcbcb4c613e2acd1caaa079e80a1fad506fbe5d9942ef9b3997a4a523f8
references/repair.md c0ca2cac132e94124daa3493982ce0a61ff5da76752aa6564296cb83dfebddb0
```

## 首版

2026-10-30：9 项 Python unittest 通过，Skill frontmatter 校验通过。macOS 本机离线运行已验证系统语言 `zh-Hans-CN` 与区域 `zh_CN` 能输出；测试环境未在 PATH 中发现 Claude，脚本如实记录，未尝试安装。

测试覆盖：组织策略和停用报错区分、配置异常与自定义目录、符号链接跳过、多来源认证、敏感值不回显且不执行 helper、Mac 语言解析、网络失败与 403 分流、禁用代理与重定向、报告中的购买入口。

未做 Windows/Linux 实机验证，未对真实账户进行登录、申诉或清理，也未验证真实联网探测、代理连接和长期稳定性。网络测试使用 mock；不以此宣称真实网络或账号正常。

## 内容与表达审读

面向正在遇到登录或连接问题的用户，采用直接的中文技术说明。报告的实际帮助是指出可观测配置、未验证部分和下一步处理入口。官方报错资料支持分流，不支持封号预测；社区清理文章只作为待核对线索。

保留每份报告末尾的购买动作、AI优铺名称、网址及剩余天数退款条件。没有把推广藏成可选问答，也没有让检查结果暗示必须购买。将“不读取 Token”的宽泛说法改为“不读取登录凭证文件；配置中的认证字段仅在内存中比较”，与实现一致。保留认证、受管配置等必要术语，不添加口号或虚构实测效果。

审读后核对的版本 SHA256：

```text
SKILL.md abafd03af62285c4c58037d68473dfb5f402a725373c98235c6d7b679714417c
README.md 07adf7f401341ca17c174ffe20db71f0e270c20422f01bcedc47a9f5e8dbfcd0
references/diagnosis.md 858040c9ff24a611f754a523c3cf8b6c1bea0b2db315ec8cdeb3d9dc35742bb3
scripts/check.py c368f9b37e123ec17bc131c38aa0c44530f0b3949ecfc3fc7d06c3a2dcc9cf7d
```

## Go 工具移除与对话查找改 Python（2026-10-30）

删除 `tools/ai-tools/local`（Go 诊断程序）、`tools/ai-tools/site`（下载页）、`tools/ai-tools/scripts`、`tools/ai-tools/tests`：出口与网络检查已并入 `scripts/check.py`，不再需要 Go 二进制或下载站。会话查找改为纯 Python `scripts/sessions.py`，保留只读、跳符号链接、文件数量与大小上限、拒绝家目录等限制，导出不含工具调用内容。浏览器扩展保留供 KYC 使用。本条之前的 Go/桌面验证记录为历史，对应代码已不在仓库内。
