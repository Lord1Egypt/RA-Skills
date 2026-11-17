# 来源与许可

本技能是原创综合。思路取自下列技能，经概括并用我们自己的话重写；未复制大段原文。`minimalist.md` 中的具体颜色值是常见、通用的起始值，仅作示例。复用上游文本前，请到各上游仓库确认权威、最新的许可。

| 本地技能（名称） | 上游 | 许可（本地所见） | 用于 |
|---|---|---|---|
| frontend-design | https://github.com/anthropics/skills (skills/frontend-design) | Apache-2.0（附带 LICENSE.txt） | 方向先行的思考、坚持风格、反同质化审美 |
| canvas-design | https://github.com/anthropics/skills (skills/canvas-design) | Apache-2.0（附带 LICENSE.txt） | 海报/艺术的“哲学 → 画布”流程 |
| theme-factory | https://github.com/anthropics/skills (skills/theme-factory) | Apache-2.0（附带 LICENSE.txt） | 主题 = 配色 + 字体，幻灯片/文档主题化 |
| ui-ux-pro-max | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | 上游仓库为 MIT（本地副本无 LICENSE 文件；需核实） | UX 规则、无障碍、配色/字体推理 |
| design-taste-frontend (taste-skill) | https://github.com/Leonxlnx/taste-skill | MIT（GitHub API，2026-10-13 核实） | 反 slop 清单、预检 |
| redesign-existing-projects (taste-redesign) | https://github.com/Leonxlnx/taste-skill | 本地副本未注明——需到上游核实 | 先审查后重设计的流程 |
| minimalist-ui (taste-minimalist) | https://github.com/Leonxlnx/taste-skill | 本地副本未注明——需到上游核实 | 暖色单色编辑风格（转述） |
| impeccable | https://github.com/pbakaus/impeccable | 上游为 Apache-2.0（本地副本无 LICENSE；需核实） | audit/critique/polish/bolder/quieter/distill 词汇，动效与字体指导 |
| design-system (ui-ux-design-system) | ClaudeKit skills（作者：claudekit），如 https://github.com/mrgoonie/claudekit-skills | MIT（frontmatter） | 三层 token、组件规格 |
| oil-ui | https://github.com/oil-oil/oil-ui | MIT（附带 LICENSE） | 探索/比较方向、基于截图的评审 |

未沿用：附带的数据集（CSV/JSON 目录）、字体、第三方 JS、搜索/更新脚本，以及部分上游技能的自动更新钩子。本技能自带的脚本（`review_site.py`、`review_image.py`）为原创代码，不进行任何下载。

## 图片审美来源（2026-10-13 核实）

用于 `image-aesthetics.md`、`image-workflows.md` 和 `review_image.py`。全部用我们自己的话概括；未复制代码或长文本。除注明外，许可信息来自 GitHub API。

| 来源 | URL | 许可 | 借鉴内容（转述） |
|---|---|---|---|
| Taste Skill (Leonxlnx) | https://github.com/Leonxlnx/taste-skill | MIT | 反 slop 立场；该仓库还有 `imagegen-frontend-*`、`image-to-code-skill`（未复制） |
| Apito —《9 个照片处理 Skill》盘点 | https://apito.ai/zh/blog/tools/photo-enhancement-skills-agents-apito/ | 文章（保留所有权利） | 思路：先判断主体/空间/色彩/情绪，再选择纸刊、拼贴、产品或编辑处理 |
| UIED / 优设 报道 | https://www.uied.cn/posts/922020 , https://www.uisdc.com/travel-poster-skill | 文章 | 配方概览；“一个构图、一种材质、一个颜色来源、≤1 个装饰”规则（营造） |
| gc-minimal-zine-poster | https://github.com/LiamGvchi/gc-minimal-zine-poster | MIT | 3:5 做旧纸、70–90% 留空、主体 8–25%、一个饱和强调色 |
| gathered-scenes-zine-skill（拾景纸刊） | https://github.com/kzzzp/gathered-scenes-zine-skill | MIT | 保留照片 vs 提炼的区分；区分照片颜色与新增印刷色；系列色卡 |
| photo-abstract-editorial | https://github.com/ZzzLc0405/photo-abstract-editorial | NOASSERTION（未检测到 SPDX 许可——视为保留所有权利） | 仅借鉴“上方照片 + 象牙色抽象面板”的想法 |
| 营造 Yingzao (guizang) | https://github.com/op7418/guizang-yingzao-skill | 未检测到 | 从照片取色；“每样只要一个”的克制规则 |
| nature-skills / nature-figure | https://github.com/yuan1z0825/nature-skills | Apache-2.0 | 结论先行的配图约定、主分图、小写粗体分图标号、每种方法一个色相族、配图质检 |
| Nature 科研配图指南 | https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/ | Springer Nature 网页 | 5–7 pt 文字、标准字体、嵌入字体、避免红/绿和彩虹色、避免装饰图标 |
| happy-figure / happy-figure-skill (Datawhale) | https://github.com/BAIKEMARK/happy-figure-skill（教程：https://github.com/datawhalechina/happy-figure） | NOASSERTION（请查看仓库） | 按领域 × 图类型 × 模型组织的科研配图提示词；少文字生成 |
| colorgram.py | https://github.com/obskyr/colorgram.py | MIT | 配色提取思路（我们使用自己的 numpy k-means） |
| Real-ESRGAN | https://github.com/xinntao/Real-ESRGAN | BSD-3-Clause | 可选的放大步骤（未打包） |
| SPO —— 逐步偏好优化（MSRA 合著者，如 Yuhui Yuan） | https://arxiv.org/abs/2406.04314 ，代码 https://github.com/RockeyCoss/SPO (MIT) | 论文；代码 MIT | 审美通过在每个去噪步累积细节偏好而提升，与布局分开评判 |
| SGPO —— 分阶段逐步优化（北京大学，非 MSRA） | https://arxiv.org/abs/2608.06768 | arXiv | 去噪早/中/晚阶段；过度优化审美奖励 → 奖励投机（重复、过度放大的细节）——用于“AI slop”清单 |
| AVA 数据集（Murray 等，CVPR 2012） | https://ieeexplore.ieee.org/document/6247954 | 研究数据集（图像权利归摄影师） | 审美分数分布、风格/语义标签 |
| NIMA（Talebi & Milanfar, 2017） | https://arxiv.org/abs/1709.05424 ；实现 https://github.com/idealo/image-quality-assessment (Apache-2.0) | 论文 / Apache-2.0 | 预测分数分布而非单一数字 |
| LAION improved aesthetic predictor | https://github.com/christophschuhmann/improved-aesthetic-predictor | Apache-2.0 | CLIP 嵌入 + MLP 的 1–10 审美分（扩散 RL 论文中用作奖励 “AES”） |
| Q-Align / OneAlign | https://github.com/Q-Future/Q-Align | S-Lab License 1.0（非商用） | 用文字定义的评级档位（bad…excellent）进行 IQA/IAA 打分 |
| AesBench | https://github.com/yipoh/AesBench | Apache-2.0 | MLLM 的审美感知 / 共情 / 评估 / 解释 |
| UNIAA | https://arxiv.org/abs/2404.09619 ；https://github.com/KwaiVGI/Uniaa | 仓库元数据未注明许可——需核实 | 属性集：内容/主题、构图、色彩、光线、对焦、情感（对应我们的 D1–D7） |
| Hasler & Süsstrunk 色彩丰富度（2003） | https://doi.org/10.1117/12.477378 | 论文 | `review_image.py` 中的 colorfulness 公式 |
| Immerkær 快速噪声估计（1996） | https://doi.org/10.1006/cviu.1996.0060 | 论文 | `review_image.py` 中的噪声 sigma |
| Okabe & Ito 色盲友好配色 | https://jfly.uni-koeln.de/color/ | 网页 | 配图用分类配色 |

未核实 / 已标注：未找到与“MSRA 分阶段审美偏好”这一描述完全对应的单篇论文；最接近的真实工作是 SPO（MSRA 合著）和 SGPO（北大，分阶段）。happy-figure 中的 “Figma 矢量化” 只作为教程章节主题出现（矢量化重构，标注为进行中），并非工具。X 搜索（2 次）未发现上述之外的图片审美技能。

## 游戏美术来源（game-aesthetics.md、game-workflows.md、review_image.py 游戏类型）

2026-10-13 调研。用我们自己的话概括；未复制文本、图像或代码。许可依据来源声明或 GitHub API。

| 来源 | URL | 许可 | 借鉴内容（转述） |
|---|---|---|---|
| Steamworks —— 商店图形资产 | https://partner.steamgames.com/doc/store/assets/standard | Valve 文档（保留所有权利） | 小胶囊图 462×174 自动缩放到 184×69 和 120×45；logo 必须保持可读，可几乎填满胶囊图；小胶囊图可用不同美术 |
| Steamworks —— 图形资产规则 | https://partner.steamgames.com/doc/store/assets/rules | Valve 文档 | 基础胶囊图 = 只能有美术 + 游戏名 + 官方副标题；不得有评分、奖项、折扣或 CTA 文字；PG-13 |
| Steam 胶囊图检查清单（Steam Analyzer） | https://www.steamanalyser.com/steam-capsule-checklist | 文章 | 在 Steam 深蓝 `#1b2838` 上做 120×45 灰度测试；先按最小尺寸设计标题 |
| Immutable —— Steam 小胶囊图 | https://www.immutable.com/insights/steam-small-capsule | 文章 | 一个主体；多个角色缩小后会粘连 |
| Apple —— 产品页制作 / 资产最佳实践 / 截图规格 | https://developer.apple.com/app-store/product-page/ , https://developer.apple.com/app-store/asset-best-practices/ , https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications/ | Apple 文档 | 前 1–3 张截图出现在搜索结果中；展示 App/游戏使用中的画面；最多 10 张；不得有透明通道 |
| App Store 审核指南 2.3.3（经 Gummicube 引用） | https://www.gummicube.com/blog/aso-academy/app-store-screenshot-dimensions-and-guidelines/ | 引用 Apple 的文章 | 截图展示使用中的 App，而不只是标题图/启动画面 |
| Game UI Database | https://www.gameuidatabase.com/ | 网站（截图版权归各发行商） | 可按 HUD 元素/品类筛选的参考库——仅作为“查惯例”的指引 |
| Gamasutra/Game Developer —— 游戏 UI 设计（叙事内 / 非叙事 / 空间 / 元，源自 Fagerholt & Lorentzon） | https://www.gamedeveloper.com/design/user-interface-design-in-video-games | 文章 | UI 分类法；竞技游戏偏好非叙事 HUD |
| Unity 博客 —— 沉浸式 UI | https://unity.com/blog/games/how-to-immerse-your-players-through-effective-ui-and-game-design | 文章 | 品类惯例（如 FPS 血量在底部），研究同品类作品 |
| Riot —— League 的清晰度；League 特效风格指南 | https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/ , https://nexus.leagueoflegends.com/en-us/2017/10/dev-leagues-vfx-style-guide/ | Riot 页面 / 公开 PDF | 特效强度 ∝ 玩法影响、形状与判定框一致、皮肤清晰度对等、预兆→消散 |
| GDC 2012《暗黑破坏神 III》的美术（Lichtner），报道 | https://gameranx.com/features/id/5666/article/gdc-2012-the-art-of-diablo-iii/ | 文章 | 可读性是第一原则；职业/怪物剪影；场景作为画布 |
| GDC 2015《看火人》的美术（Jane Ng） | https://www.thumbsticks.com/gdc-2015-the-art-of-firewatch/ , https://www.youtube.com/watch?v=ZYnS3kKTcGg | 文章 / 演讲视频 | 按剧情节点的色彩脚本；分层颜色表现纵深；带强剪影的平面形状；细节密度暗示重要性 |
| GDC 2017《守望先锋》的美术（Petras, Tsang） | https://www.gdcvault.com/play/1024268/The-Art-of-Overwatch-Evolving | GDC Vault（演讲不可免费观看） | 英雄剪影（含动画）远距离可读；仅使用概要层面的说法 |
| 80.lv —— 形状语言与可读性 | https://80.lv/articles/character-design-shape-language-and-readability | 文章 | “处处细节 = 没有细节”；休息区；先铺大形 |
| Olgskaia-Mustonen 论文（Theseus） | https://www.theseus.fi/bitstream/handle/10024/904059/Olgskaia-Mustonen_Kristina.pdf | 学位论文（学术，保留所有权利） | 3D 角色可读性中的剪影 + 明度图案 |
| game-art SKILL.md (sickn33/agentic-awesome-skills) | https://github.com/sickn33/agentic-awesome-skills/blob/main/skills/game-development/game-art/SKILL.md | MIT | 现有 agent 技能：风格决策树、“美术服务玩法”、在游戏距离下测试——我们补充了评分、品类档案和指标 |
| 发现的其他 agent 技能（仅用于确认空白） | https://github.com/ianlintner/ai-pixel-art-image-generation (MIT), https://github.com/isabellagreco1997/sprite-forge (MIT), https://github.com/majidmanzarpour/blender-game-skills (MIT) | MIT | 已有像素画生成 / 精灵工具；未发现游戏美术*评审*量表类技能 |
| Otsu 阈值法（1979） | https://doi.org/10.1109/TSMC.1979.4310076 | 论文 | `review_image.py` 中的图底蒙版与可分离度 |
| 测试图像（仅本地使用，不再分发） | Steam 公共 CDN，如 https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1145360/… | © 各发行商 | Hades、Hollow Knight、Dota 2、Baldur's Gate 3 的截图/胶囊图，仅用于本地脚本测试 |

品类配色（如石青/朱砂颜料、墨分五色）、各品类的 HUD 惯例和数字目标是我们对常见实践的综合——**并非**来自单一可引用的标准；数字请当作启发式。

未核实 / 受阻：
- **X**：3 次搜索（英文可读性技巧、Steam 胶囊图、中文“游戏美术 可读性”）分别返回 1、1、0 条帖子——一位独立开发者在征求胶囊图可读性反馈；没有可作为指导引用的内容。
- **Facebook**：小组（如 “Creative Crossroads – Game Art Showcase”、“Game Artists Connect”）只能通过第三方提及发现；内容需登录，未读取也未引用。
- GDC Vault 演讲（守望先锋）需付费；相关说法仅来自公开报道。Riot 特效 PDF 未直接打开（概要来自搜索结果）。
- Game UI Database 内容（截图）版权归发行商；仅作为指引使用。
