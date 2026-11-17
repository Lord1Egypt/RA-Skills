---
name: content-orchestrator
version: "1.0.0"
description: "内容生成+发布统一编排器,15条管道文件(12 PL-*+3 E2E-*):VIDEO/VIDEO-BATCH/IMAGE/AUDIO/LIPSYNC/COMIC/COMIC-BATCH/ARTICLE-BATCH/NOVEL-BATCH/PRODUCT/HOTSPOT/NEWPROD+E2E-VIDEO/E2E-IMAGE/E2E-DAILY+3内置虚拟路由(PL-NOVEL连载/PL-DRAMA短剧/PL-UPLOAD上传)。平台注册表自动路由+代理自动注入+多租户感知(tenant_id→风格/人设/素材/平台隔离)+素材→闲鱼商品(PL-PRODUCT)+热点→商品(PL-HOTSPOT)+小说连载(PL-NOVEL/PL-NOVEL-BATCH)+短剧生成(PL-DRAMA内置)。触发:生成内容/发布内容/一条龙/日常运营/素材转商品/热点选品/热点上架/小说连载/短剧生成/上传内容生成 不触发:纯闲鱼运营/纯客服回复/数据分析查询"
tools: [read, exec]
# BUG-228修复: 添加content-qa-guard依赖(内容合规审核守卫,来源:02手册§五5.3合规检测步骤)
# P0-5修复: 添加geo-content-optimizer依赖(GEO评分≥60门控,来源:02手册§12.7 GEO优化规则)
# P2-10修复: novel-bridge是exec脚本(mcps/shared/novel_bridge.py,P0-030迁移)非Skill,从dependencies移除,exec依赖见metadata.openclaw.exec_scripts
# FIX-V3-009/BUG-V4-013: 移除硬编码dependencies(原18个,含lazy Skill),改为运行时动态发现
# 管道Skill(video-generator/content-publisher/cosyvoice等)在运行时由编排器自动发现和加载
dependencies: []
metadata:
  layer: product
  priority: P0
  category: content-creation
  dynamic_dependencies: true  # FIX-V3-009: 运行时动态发现管道Skill,而非硬编码依赖
  openclaw:
    emoji: "🎭"
    color: "#7b3fe4"
    vibe: "professional"
    os: ["win32", "linux", "darwin"]
    exec_scripts: ["novel_bridge.py"]
    requires:
      bins: ["python", "ffmpeg"]
      config: ["mcp.servers.sau-mcp", "mcp.servers.device-operations-mcp", "mcp.servers.proxy-pool-mcp", "mcp.servers.pps-mcp", "mcp.servers.agency-portal-mcp", "mcp.servers.narrato-mcp", "mcp.servers.liveportrait-mcp", "mcp.servers.fishclaw-mcp", "mcp.servers.tts-adapter-mcp"]
      env: ["SILICONFLOW_API_KEY"]
---

# Content Orchestrator 内容编排器

**版本**: v1.1.0 | **优先级**: P0（内容生产统一入口） | **所属部门**: 内容部

## 使用场景

- 一键视频发布: "帮我生成一条AI热点短视频并发布到抖音和视频号"
- 图文矩阵分发: "生成一组产品图文，发到小红书+头条+知乎"
- 日常运营: "执行今日日常运营任务"（热点→选题→生成→排期发布）
- 口型同步视频 / 漫画视频
- 素材转商品: "把这组图文素材转成闲鱼商品发布"（PL-PRODUCT管道）
- 热点选品上架: "发现热点后自动生成商品并上架闲鱼"（PL-HOTSPOT管道，热点→选品→商品→发布）
- 小说连载: "生成今日2章小说并发布到图文平台"（PL-NOVEL管道，InkOS→章节生成→发布）
- 短剧生成: "取今日小说章节生成1集短剧并发布到视频平台"（PL-DRAMA管道，章节→剧本→分镜→视频→发布）

## 成功指标

| 指标 | 目标值 | 来源 |
|:-----|:-------|:-----|
| 管道路由准确率 | ≥95% | 智能路由5步决策 |
| 内容生成成功率 | ≥90% | 10条内容管道执行 |
| 营销门控通过率 | ≥85% | 营销注入门控流程 |
| 多平台发布成功率 | ≥80% | 3条端到端管道 |
| 内容差异化检查通过率 | ≥90% | 内容差异化检查流程 |

## 通信风格

content-orchestrator以专业数据驱动的风格编排内容生产，语言风格参考IDENTITY.md。
- 语气: 专业沉稳，管道执行结果以结构化数据呈现
- 输出: 简洁明了，管道选择+引擎路由+发布结果以JSON输出
- 交互: 主动建议内容生产方向（如热点选题、素材复用、小说连载排期）

## 十条内容管道

| 管道 | 流程 | 输出 |
|:-----|:-----|:-----|
| PL-VIDEO | narrato-mcp脚本→cosyvoice配音→kling画面→合成+字幕→🔴营销注入门控→AI声明注入 | 成品视频 |
| PL-IMAGE | (可选)竞品数据采集→content-template文案→🔴营销注入门控→flux配图→排版合成→AI声明注入 | 成品图文卡片 |
| PL-AUDIO | cosyvoice/fish-speech/gpt-sovits→语音合成→🔴营销注入门控→AI声明注入 | 音频文件 |
| PL-LIPSYNC | cosyvoice语音→flyworks/liveportrait口型同步→🔴营销注入门控→AI声明注入 | 数字人视频 |
| PL-COMIC | character-consistency角色画面→narrato-mcp分镜→kling I2V转视频→🔴营销注入门控→AI声明注入 | 漫画视频 |
| PL-NOVEL | novel_bridge初始化→InkOS章节生成→标题生成→🔴营销注入门控→SEO→AI声明→多平台发布 | 小说章节(图文) |
| PL-DRAMA | novel_bridge章节获取→剧本转换→系列管理→narrato分镜→cosyvoice配音→kling画面→合成+字幕→一致性验证→🔴营销注入→AI声明→多平台发布 | 短剧视频 |
| PL-PRODUCT | 图文素材→图片规格转换→文案风格转换→5要素注入→fishclaw-mcp发布 | 闲鱼商品规格 |
| PL-HOTSPOT | 热点数据→选品方向转换→unified-product-ops选品→商品参数转换→fishclaw-mcp发布 | 闲鱼商品(热点驱动) |
| PL-UPLOAD | 用户上传文件→格式检测→文本/图片提取→路由到PL-COMIC/PL-NOVEL/PL-IMAGE→🔴营销注入门控→AI声明注入 | 用户上传内容处理 |
| PL-ARTICLE-BATCH | 批量选题→批量文案生成→🔴营销注入门控→批量配图→批量排版→多平台发布→状态回写(11步) | 批量文章 |
| PL-VIDEO-BATCH | 批量脚本生成→批量配音→批量画面生成→批量合成+字幕→一致性验证→🔴营销注入门控→AI声明→多平台发布(13步) | 批量视频 |
| PL-NOVEL-BATCH | InkOS批量初始化→批量章节生成→批量标题生成→🔴营销注入门控→批量SEO→AI声明→多平台发布(10步) | 批量小说章节 |
| PL-COMIC-BATCH | 批量角色画面→批量分镜→批量I2V转视频→🔴营销注入门控→AI声明→多平台发布(12步) | 批量漫剧 |

### PL-NOVEL 小说连载管道

PL-NOVEL通过InkOS(v2.3.2)的7 Truth Files系统生成连载小说章节，并发布到图文自媒体平台。支持多租户隔离和每日自动生成。

**输入**: `{topic: str, tenant_id: str, genre: str, style_config: dict}`

**步骤**:

1. **小说初始化** — novel_bridge.init_novel
   - 调用InkOS `book create`创建书籍项目（含7 Truth Files初始化）
   - 写入风格配置（genre/chapter_words/writing_style/inkos_style_ref）
   - PG novel_books表插入书籍元数据（book_id为InkOS slug字符串）
   - 工作目录: `data/books/{tenant_id}/{book_id}/`

2. **章节生成** — novel_bridge.generate_chapters
   - 调用InkOS `write next --count 2 --words 3000`生成2章
   - InkOS自动维护World State/Character Matrix/Pending Hooks等Truth Files
   - PG novel_chapters表插入章节（含content_full完整正文，content_preview前500字）
   - 4级错误降级: 重试(5s/15s/45s)→标记失败+入sync_queue→连续3章告警→人工介入

3. **标题生成** — title-generator.generate
   - 基于章节内容生成吸引人的标题

4. **营销注入** — market-copywriter.adapt_platform（🔴门控检查）
5. **SEO优化** — seo-optimizer.optimize
6. **AI声明注入** — risk-detector.inject_ai_declaration
7. **多平台发布** — content-publisher.publish（知乎/头条/微信公众号）

**输出**: `{success:bool, data:{book_id, chapters_generated, chapters:[{chapter_number, title, word_count}]}}`

### PL-DRAMA 短剧生成管道

PL-DRAMA取PL-NOVEL生成的最新章节，转换为短剧剧本并生成视频，发布到视频平台。

**输入**: `{tenant_id: str, book_id: str(可选)}`

**步骤**:

1. **章节获取** — novel_bridge.get_latest_chapter
   - 从PG novel_chapters查询最新章节（返回content_full完整文本，≥3000字）
   - narrato-mcp generate_short_drama_script需要3000+字输入

2. **剧本转换** — novel-to-script.convert
   - 将小说章节文本转换为短剧剧本格式（场景/对话/动作描述）

3. **系列管理** — series-manager.generate
   - 维护角色一致性（voice_id/face_ref跨集一致）
   - 生成系列元数据（集数/前情提要/下集预告）

4. **分镜生成** — narrato-mcp.generate_short_drama_script
   - 基于剧本生成分镜脚本（注意: action名称为generate_short_drama_script，非generate_script）

5. **配音生成** — tts-adapter-mcp.synthesize(BUG-V6-015副作用同步: 替换已删除的gpt-sovits-mcp)
6. **画面生成** — kling-mcp.text_to_video
7. **视频合成** — video-generator.compose_video
8. **字幕生成** — video-generator.generate_subtitle
9. **一致性验证** — series-manager.validate（角色/场景/剧情连贯性检查）
10. **营销注入** — market-copywriter.adapt_platform（🔴门控检查）
11. **AI声明注入** — risk-detector.inject_ai_declaration
12. **多平台发布** — content-publisher.publish（抖音/快手/B站）

**输出**: `{success:bool, data:{video_url, subtitle_url, episode_number, platforms_published}}`

### PL-PRODUCT 素材→商品转换管道（可选）

PL-PRODUCT将已生成的图文素材自动复用为闲鱼商品，实现内容素材→电商商品的跨域转换。该管道为可选管道，不影响现有PL-IMAGE/PL-VIDEO/PL-SHORT管道。

**输入**: 已生成的图文素材（图片URL列表+文案文本）

**步骤**:

1. **图片规格转换** — 内容平台尺寸→闲鱼商品图尺寸
   - 调用ai-capabilities-mcp图片处理工具
   - 闲鱼商品图要求: 主图800×800px以上，正方形比例1:1，最多9张（来源:01手册§四4.1）
   - 内容平台原图若为竖版(如小红书3:4)→裁剪为1:1正方形+居中构图
   - 输出: 闲鱼规格图片URL列表

2. **文案风格转换** — 内容平台风格→闲鱼商品描述风格
   - 调用ai-capabilities-mcp文本生成工具
   - 内容文案特点: 种草/分享/叙事风格 → 闲鱼商品描述特点: 卖点直击/价格透明/售后明确
   - 转换规则: 去除emoji装饰→提炼核心卖点→补充商品属性→添加交易引导语（来源:01手册§四4.3）

3. **5要素注入** — 补充闲鱼商品必需字段（来源:01手册§四4.1+4.3）
   - 商品名称: 从文案提取+优化为闲鱼标题格式(≤30字，关键词前置)
   - 价格: 从UTD.price读取，无则使用默认定价策略（来源:01手册§七7.1）
   - 规格: 从UTD.specs读取，无则生成默认规格描述
   - 发货方式: 虚拟商品默认"自动发货"，实体商品默认"快递"（来源:01手册§五5.1）
   - 售后说明: 按商品类型注入标准售后模板（来源:01手册§四4.3）

4. **调用fishclaw-mcp.publish_item发布** — 将转换后的商品规格传递给fishclaw-mcp MCP
   - 输入: {title, account_id}（title从步骤3商品参数生成获取，account_id默认default）
   - DEF-01修复(TECH-DEBT-032): 原xianyu-manager是SKILL(梯度SKU生成)非MCP,实际发布走fishclaw-mcp.publish_item
   - 发布间隔≥5秒（来源:01手册§十10.1风控安全线）

**输出**: `{success:bool, data:{product_id, xianyu_url, converted_images:N, pipeline:"PL-PRODUCT"}}`

### PL-HOTSPOT 热点→商品自动上架管道（可选）

PL-HOTSPOT将trend-discovery发现的热点数据自动转化为闲鱼商品并上架，实现热点趋势→选品→商品发布的全链路自动化。该管道为可选管道，不影响现有6条内容管道和3条E2E管道。

**输入**: trend-discovery输出的热点数据 `{topic: str, heat: int, platforms: list[str], trend: str}`

**步骤**:

1. **热点→选品方向转换** — 提取热点关键词作为选品方向
   - 从热点数据提取`topic`作为`direction`（选品方向关键词）
   - 按`heat`值排序: heat>80的热点优先处理，heat≤30的热点跳过（低热度不值得选品）
   - 从`trend`字段提取趋势方向(上升/稳定/下降)，仅处理上升趋势热点
   - 输出: `{direction: str, heat: int, trend: str, source_topic: str}`

1.5. **竞品数据采集**(可选,Token优化) — 采集同类商品在社交平台的用户评价和卖点话术
   - 调用media-crawler-mcp.search_posts(platform="xiaohongshu", keyword=direction, limit=10)
   - 调用media-crawler-mcp.format_for_prompt(data=结果, max_posts=3) → 压缩为≤200 token精简文本
   - 将精简文本注入步骤3的AI生成prompt中作为"竞品参考"段落
   - Token控制: 竞品参考≤200 token,不超过总prompt的15%
   - 失败不阻断: 采集失败→跳过,记录warning日志
   - 完成后调用media-crawler-mcp.stop_service()关闭容器节省资源

2. **调用unified-product-ops选品分析** — 基于选品方向进行选品
   - 调用unified-product-ops Skill，传入`direction`关键词
   - unified-product-ops返回选品报告: `{niche, competition, demand, pricing_range, suggested_products}`
   - 若unified-product-ops返回无合适选品→终止管道，返回`{success:false, error:"no_suitable_product", code:"HR-002"}`
   - 输出: 选品报告数据

3. **选品报告→商品参数转换** — AI辅助生成闲鱼商品参数
   - 调用ai-capabilities-mcp文本生成工具，基于选品报告+热点数据生成商品参数:
     - 商品名称: 热点关键词+商品类型，≤30字，关键词前置（来源:01手册§四4.1）
     - 商品描述: 融合热点趋势描述+选品分析结论+商品卖点，卖点直击+价格透明+售后明确（来源:01手册§四4.3）
     - 定价建议: 从选品报告的`pricing_range`提取，结合01手册§七7.1动态定价策略
     - 商品规格: 从选品报告的`suggested_products`提取规格描述
   - 输出: `{title, price, description, specs, delivery_type, after_sale}`

4. **调用fishclaw-mcp.publish_item发布商品** — 将商品参数传递给fishclaw-mcp MCP
   - 输入: {title, account_id}（title从步骤3商品参数生成获取）
   - DEF-01修复(TECH-DEBT-032): 实际闲鱼商品发布走fishclaw-mcp.publish_item(已注册MCP)
   - 发布间隔≥5秒（来源:01手册§十10.1风控安全线）
   - 5要素注入在前面_MARKETING_SEO_GEO_REVIEW_STEPS中已执行，本步骤仅负责发布

5. **结果回写** — 将发布结果与热点数据关联
   - 记录热点→商品的映射关系: `{hotspot_topic, product_id, xianyu_url, pipeline:"PL-HOTSPOT"}`
   - 用于后续追踪热点商品的销售表现

**输出**: `{success:bool, data:{product_id, xianyu_url, hotspot_topic, heat, pipeline:"PL-HOTSPOT"}}`

### PL-UPLOAD 用户上传内容处理管道

PL-UPLOAD接收用户上传的文件（文本/图片/PDF），自动检测格式并提取内容，路由到对应的内容生成管道。支持多租户隔离。

**输入**: `{pipeline_type:"PL-UPLOAD", tenant_id, upload_files:[{path, type, filename}]}`

**流程**:
1. 文件格式检测: 文本(.txt/.md/.docx)→文本提取, 图片(.jpg/.png/.webp)→图片分析, PDF(.pdf)→OCR(paddleocr-mcp)
2. 内容解析: 文本→分章节/分场景, 图片→描述生成, PDF→全文提取
3. 智能路由:
   - 小说文本→PL-NOVEL（继续连载或从头生成）
   - 故事文本→PL-COMIC（生成漫剧）
   - 图片素材→PL-IMAGE（生成图文卡片）
   - 混合内容→PL-DRAMA（生成短剧）
4. 调用目标管道执行生成+发布

**输出**: `{success:bool, data:{pipeline:"PL-UPLOAD", routed_to:"PL-COMIC", upload_count:N, generated_items:[...]}}`

### PL-NEWPROD 9商品内容生产专属管道（v1.1新增 2026-06-03）

PL-NEWPROD是面向NEW-PROD-01~09 AI服务商品矩阵的专属内容生产管道，将商品信息拉取→热点监控→选题决策→文案生成→配图/视频生成→个人IP特质注入→写作风格特质注入→去AI味→营销注入→SEO优化→GEO优化→内容审核→AI声明注入→多平台发布→排期调度→效果分析整合为16步端到端自动化流程。

**输入**:
- 默认: 全量9商品(`product_id="all"`)
- 自定义: 指定商品ID列表(`product_id="NEW-PROD-01,NEW-PROD-02"`)
- 可选: tenant_id(代运营场景)

**步骤**:

| 步骤 | 名称 | Tool | Action | 说明 |
|:-----|:-----|:-----|:-------|:-----|
| 1 | 商品信息拉取 | xianyu-manager | get_new_prod_suggestions | 拉取9商品配置(价格/MCP/合规) |
| 2 | 热点监控 | dailyhot-mcp | get_hot_topics | 关注"AI服务"分类热点 |
| 2.5 | 竞品数据采集(可选) | media-crawler-mcp | search_posts+format_for_prompt | 搜索小红书/抖音竞品内容+用户评论,压缩后注入步骤4文案生成prompt(Token优化:≤300token) |
| 3 | 选题决策 | content-research-mcp | generate_topic_suggestions | focus=new_product_promotion |
| 4 | 文案生成(商品介绍) | content-template | create | template_type=product_intro |
| 5 | AI内容声明注入 | risk-detector | inject_ai_declaration | R12合规强制标注 |
| 6 | 配图/视频生成(按商品路由) | content-orchestrator-router | route_by_product | 按商品类型路由到对应MCP |
| 7 | 内容审核(R12-R15) | sensitive-word-mcp | check_text | 4条合规规则校验 |
| 8 | 多平台发布(抖音+小红书+视频号) | content-publisher | publish | 默认3平台批量发布 |
| 9 | 排期调度 | content-publisher | schedule_smart | preferred_time=auto |
| 10 | 效果分析(72h后) | content-analytics | track_performance | 跟踪72h窗口数据 |

**商品→引擎路由映射** (来源:xianyu-manager v1.1 NEW-PROD-01~09):
| 商品 | 路由引擎 | 适用场景 |
|:-----|:---------|:---------|
| NEW-PROD-01 | kling-mcp | 照片→视频(3/8/20秒) |
| NEW-PROD-02 | DeOldify+flux+kling | 老照片修复+动态化 |
| NEW-PROD-03 | cosyvoice+flyworks | AI数字人口播(声音克隆+口型同步) |
| NEW-PROD-04 | flux+kling+airi | 宠物写真+拟人化 |
| NEW-PROD-05 | flux+kolors+airi | 头像/表情包/海报 |
| NEW-PROD-06 | flux+kolors+pps | 产品主图/电商海报 |
| NEW-PROD-07 | SILICONFLOW-LLM | 短视频脚本/口播文案 |
| NEW-PROD-08 | kling+flux+liveportrait | 写真/形象IP/职业照 |
| NEW-PROD-09 | character-consistency+narrato | 绘本/儿童故事视频 |

**与content-publisher v4.4 newprod_publisher.py协作**:
PL-NEWPROD管道的"多平台发布"步骤可调用content-publisher v4.4新增的`newprod_publisher.batch_publish`作为批量发布加速入口，实现9商品×3平台×3梯度=81次发布的批量编排能力。

**输出**: `{success:bool, data:{pipeline_type:"PL-NEWPROD", total_steps:16, steps:[...]}}`

## 三条端到端管道

| 管道 | 流程 | 关键约束 |
|:-----|:-----|:---------|
| E2E-VIDEO | PL-VIDEO→格式适配→代理注入→AI声明注入→逐平台发布 | 平台间间隔5-10分钟(来源:02手册§九9.2) |
| E2E-IMAGE | PL-IMAGE→AI声明注入→逐平台发布 | 平台间间隔5-10分钟 |
| E2E-DAILY | trend-discovery→AI选题→自动选管道→AI声明注入→排期发布 | ✅排期调度已集成(content-publisher.schedule_smart) |

## 营销注入门控(强制)

所有5条内容管道(PL-VIDEO/PL-IMAGE/PL-AUDIO/PL-LIPSYNC/PL-COMIC)在发布前必须通过营销注入门控。PL-PRODUCT和PL-HOTSPOT管道例外: 闲鱼商品描述属交易属性，非内容属性，不强制营销注入。

### 门控流程

1. 调用market-copywriter Skill，输入内容摘要+目标平台+受众
2. 获取核心卖点(selling_points)+情绪钩子(emotional_hook)+CTA话术
3. 将营销元素注入到内容文案中(开头钩子+中间卖点+结尾CTA)
4. 门控判定:
   - market-copywriter返回success=true → ✅通过门控，继续发布流程
   - market-copywriter返回success=false → 重试1次(降级为基础营销模板)
   - 重试仍失败 → ❌拦截发布，返回`{success:false, error:"MARKETING_GATE_FAILED", code:"MG-001"}`

### 降级策略(重试时)

重试时使用品类差异化基础营销模板替代market-copywriter:

| 品类 | 开头钩子 | 核心卖点模板 | 结尾CTA |
|:-----|:---------|:------------|:--------|
| AI工具/软件 | "还在手动{痛点}？{产品名}用AI帮你3秒搞定！" | "{特性1}: AI自动{功能}，效率提升N倍 / {特性2}: 一键{功能}，省时省力 / {特性3}: 智能优化，效果更好" | "私信我'{关键词}'免费体验AI{功能}" |
| 设计/创意 | "设计灵感枯竭？{产品名}帮你秒出大片！" | "{特性1}: 多种风格一键生成 / {特性2}: 专业级效果无需PS / {特性3}: 批量出图效率翻倍" | "私信我'{关键词}'获取设计模板" |
| 文案/写作 | "写不出好文案？{产品名}帮你10秒出稿！" | "{特性1}: AI理解你的需求精准生成 / {特性2}: 多平台风格自动适配 / {特性3}: 一键优化去AI味" | "私信我'{关键词}'获取写作神器" |
| 电商/运营 | "店铺运营太累？{产品名}帮你全自动搞定！" | "{特性1}: 自动上架+定价+客服 / {特性2}: 智能选品数据驱动 / {特性3}: 7×24小时无人值守" | "私信我'{关键词}'了解代运营方案" |
| 通用(默认) | "还在为{痛点}发愁？{产品名}帮你解决！" | 从内容中提取3个关键特性，按FAB法则组织 | "私信我'{关键词}'了解更多" |

品类判定规则: 根据内容标题/描述中的关键词匹配品类，无匹配时使用通用模板。

### 与AI声明注入的关系

营销注入门控在AI声明注入之前执行。流程: 营销注入门控→AI声明注入→发布。两者均为强制步骤，任一不通过则拦截发布。

## 内容吸引力评分门控(强制)

所有5条内容管道(PL-VIDEO/PL-IMAGE/PL-AUDIO/PL-LIPSYNC/PL-COMIC)在发布前必须通过内容吸引力评分门控。PL-PRODUCT和PL-HOTSPOT管道例外: 闲鱼商品描述属交易属性，非内容属性，不强制评分。

### 评分维度

| 维度 | 权重 | 评分标准 |
|:-----|:-----|:---------|
| 标题吸引力 | 30% | 是否包含数字/疑问/对比/悬念等钩子元素 |
| 开头3秒钩子 | 25% | 前3秒/前50字是否能抓住注意力 |
| 内容深度 | 20% | 是否有独特见解/数据支撑/实操步骤 |
| CTA清晰度 | 15% | 行动号召是否明确可执行 |
| SEO适配度 | 10% | 关键词布局是否合理，标题是否含核心关键词 |

### 评分方式

调用LLM对生成内容进行0-100分评分:
1. 将内容标题+正文摘要+目标平台传入LLM
2. LLM按5个维度分别打分(0-100)
3. 加权计算总分: 总分=标题×0.30+钩子×0.25+深度×0.20+CTA×0.15+SEO×0.10
4. LLM评分使用SILICONFLOW_API_KEY，base_url=os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")，model=os.getenv("SILICONFLOW_MODEL", "Qwen/Qwen3-8B")

### 门控规则

| 总分 | 动作 | 说明 |
|:-----|:-----|:-----|
| <60分 | ❌拦截发布 | 内容质量不达标，必须重新生成 |
| 60-75分 | ⚠️警告但允许发布 | 内容质量一般，建议优化后发布 |
| >75分 | ✅通过 | 内容质量达标 |

### LLM评分Prompt模板

```
你是一位内容营销评分专家。请对以下内容进行吸引力评分(0-100分)。

目标平台: {platform}
内容标题: {title}
内容摘要: {summary}

评分维度:
1. 标题吸引力(权重30%): 是否包含数字/疑问/对比/悬念等钩子元素
2. 开头3秒钩子(权重25%): 前50字是否能抓住注意力
3. 内容深度(权重20%): 是否有独特见解/数据支撑/实操步骤
4. CTA清晰度(权重15%): 行动号召是否明确可执行
5. SEO适配度(权重10%): 关键词布局是否合理

评分锚点(防止评分虚高):
- 30分: "XX产品很好用，推荐大家购买" (无钩子/无深度/无CTA/纯广告)
- 50分: "还在为XX发愁？试试XX产品，效果不错哦~" (有痛点钩子但无深度/CTA模糊)
- 70分: "3个方法帮你解决XX问题，第2个最有效！1.XX 2.XX 3.XX 私信我获取完整方案" (有数字钩子+有步骤+有CTA)
- 90分: "我花了3个月测试了5种XX方案，发现只有第3种真正有效(附数据对比)。1.方案A:效果X但成本Y 2.方案B:效果Z但耗时W 3.方案C:效果最佳+成本最低+实操步骤→私信'XX'获取完整教程" (数据支撑+对比+深度+明确CTA)

请参照锚点严格评分，不要因为内容"还行"就给70+。大部分AI生成内容应在50-70分区间。

严格输出JSON:
{"title_score": N, "hook_score": N, "depth_score": N, "cta_score": N, "seo_score": N, "total_score": N, "suggestion": "优化建议"}
```

### 评分失败降级

- LLM调用失败 → 跳过评分门控，记录警告日志，允许发布(评分门控为质量提升手段，非安全红线)
- SILICONFLOW_API_KEY未设置 → 跳过评分门控，记录警告日志

## AI展示声明注入

所有10条管道(7条内容管道+3条E2E管道)在发布前必须执行AI展示声明注入步骤。PL-PRODUCT和PL-HOTSPOT管道例外: 闲鱼商品描述不注入AI声明(商品描述属交易属性，非内容属性)。

### 注入流程

1. 读取目标平台的`ai_declaration`配置(来源: content-publisher/scripts/platform_specs.json)
2. 判断`enabled`字段: `false`→跳过该平台(如TikTok)
3. 按`format`字段选择声明格式，将`template`内容注入到内容末尾(标题/描述)
4. 注入后继续执行发布步骤

### 平台声明格式差异

| 格式 | 说明 | 适用平台 |
|:-----|:-----|:---------|
| tag | 标签形式，附加在标题/描述末尾 | 抖音、快手 |
| short_tag | 简短标注，节省正文空间 | 小红书、抖音图文 |
| paragraph | 段落声明，完整展示AI能力 | 视频号、B站、百家号 |
| none | 不注入(平台豁免) | TikTok(enabled=false) |

### 跳过规则

- TikTok: `ai_declaration.enabled=false`，跳过注入(来源:platform_specs.json tiktok配置，海外平台豁免AI声明避免合规风险)
- 未在platform_specs.json注册的平台: 跳过注入，记录警告日志
- `required=false`的平台(如B站、百家号): 仍注入声明(展示AI能力)，但不强制

### 注入位置

- 视频: 注入到描述(description)末尾
- 图文: 注入到正文(body)末尾
- 音频: 注入到标题(title)末尾

## 智能路由5步决策

1. **解析意图** → 提取内容类型(视频/图文/音频/口型/漫画/商品/热点选品)
2. **选择管道** → 匹配7条内容管道(含PL-PRODUCT素材转商品、PL-HOTSPOT热点选品)
3. **选择引擎** → 按可用性+成本+质量排序(kling→pixelle→mpt逐级降级)
4. **代理注入** → proxy-pool-mcp获取可用代理，不可用→降级直连
5. **平台路由** → 查平台注册表，映射到对应MCP Server发布

## 内容差异化检查(强制)

同一主题内容在矩阵账号多平台分发时，必须通过差异化检查，防止内容同质化导致平台降权。

### 差异化维度

| 维度 | 可选值 | 说明 |
|:-----|:-------|:-----|
| 切入角度 | 教程/评测/故事/数据 | 内容的核心视角 |
| 情绪基调 | 专业/轻松/煽情 | 内容的情感倾向 |
| 内容深度 | 入门/进阶/硬核 | 目标受众的知识水平 |
| 表现形式 | 图文/视频/音频 | 内容的载体形式 |

### 差异化规则

- **24小时同主题多平台规则**: 同一主题在24小时内发布到不同平台时，至少2个维度必须不同
- **矩阵账号规则**: 同一矩阵内多个账号发布同主题内容时，至少2个维度必须不同
- **自动调整**: 当差异化检查不通过时，自动调整切入角度或情绪基调，无需人工干预

### 相似度检查

矩阵账号发布前执行内容相似度检查:
1. 提取待发布内容的4个差异化维度值
2. 与24小时内同主题已发布内容的维度值逐一比对
3. 计算相似度: 相同维度数/总维度数×100%
4. 相似度>70% → ❌拒绝发布，要求重新生成(调整至少1个维度)
5. 相似度≤70% → ✅通过差异化检查

### 检查流程

1. 路由决策完成后，发布前执行差异化检查
2. 查询24小时内同主题已发布内容的差异化维度
3. 计算与待发布内容的相似度
4. 相似度>70% → 返回`DIFFERENTIATION_FAILED`，附带建议调整的维度
5. 相似度≤70% → 继续发布流程

## 平台注册表(17平台)

| 平台 | MCP Server | 内容类型 | 备注 |
|:-----|:-----------|:---------|:-----|
| 抖音/快手/小红书/B站 | sau-mcp | 视频 | upload_video |
| 视频号/TikTok | device-operations | 视频 | device_publish_to_* |
| 小红书/抖音图文/百家号 | device-operations | 图文 | device_publish_to_* |
| 头条 | content-publisher(toutiao adapter) | 图文 | F2合并:由content-publisher统一调用 |
| 知乎/微博 | multi-publisher-mcp | 图文 | Wechatsync v2已支持(zhihu.py/weibo.py) |
| YouTube/FB/IG | aitoearn-mcp | 视频/图文 | ⚠️aitoearn-mcp已禁用 |
| 闲鱼 | xianyu-manager | 图文→商品 | PL-PRODUCT/PL-HOTSPOT管道专用，图片1:1裁剪+文案风格转换+5要素注入 |

> 完整16平台注册表、UTD/UPR输入格式、输出格式详见 scripts/content_orchestrator_reference.json

## 多租户感知(v1.2 DEF-U49 P2)

当UTD含tenant_id时，自动注入租户上下文:
1. agency-client-manager.query → 获取方向/平台/风格/人设/预算
2. tenant-style-config.get → 获取视觉风格(prompt_prefix/frame/color/font)
3. pps-mcp.get_persona_profile → 获取人设档案(配音/外观/照片/文字风格)
4. pps-mcp.get_distill_fingerprint → 获取蒸馏21维指纹(DEF-U49 P2新增)
   - persona_profile(4维人物IP) + style_fingerprint(6维写作风格)
   - video_style_fingerprint(6维视频风格) + longform_structure(5维长文结构)
   - brand_analysis(品牌分析缓存)
5. 注入UTD → platform/agent_id/style可设为"auto"自动填充 + 5蒸馏字段注入step_params

蒸馏数据消费分工(DEF-U49 P2):
- content-orchestrator: 预查询蒸馏数据并注入step_params(本Skill)
- content-template: 消费style_fingerprint/longform_structure(模板渲染,P2示范)
- market-copywriter/seo-optimizer: 待P3接入(按需消费persona_profile/brand_analysis)
- 注: 下游Skill用setdefault注入,不读则用默认值,不报错(非致命降级)

租户约束: 内容方向→directions范围 / 目标平台→仅租户配置平台 / 视觉风格→注入prompt / 人设绑定→统一配音外观 / 预算限制→成本过滤 / 钩子结尾图→引流图注入 / 素材优先→租户素材库 / 蒸馏指纹→21维注入下游

> 完整租户注入流程、7项约束详情、UTD扩展字段详见 scripts/content_orchestrator_reference.json

## 异常处理

| 异常码 | 场景 | 处理 | 降级 |
|:-------|:-----|:-----|:-----|
| PIPELINE_NOT_FOUND | 管道不存在 | 返回可用管道列表 | 必须指定有效管道 |
| ENGINE_UNAVAILABLE | 引擎不可用 | 自动降级备选引擎 | kling→pixelle→mpt |
| PUBLISH_FAILED | 发布失败 | 跳过该平台继续 | 部分成功+失败列表 |
| PROXY_FAILED | 代理获取失败 | 降级直连+告警 | 直连发布 |
| GENERATION_TIMEOUT | 生成超时(>5分钟) | 重试1次 | 返回中间产物 |
| PLATFORM_UNSUPPORTED | 平台不在注册表 | 忽略该平台 | 仅发布已注册平台 |
| TENANT_CONFIG_MISSING | 租户配置缺失 | 返回错误 | 降级默认模式 |
| SCRIPT_GENERATION_FAILED | 脚本生成失败 | 默认脚本模板 | 固定3段式脚本 |
| AI_DECLARATION_FAILED | AI声明注入失败 | 跳过注入+警告日志 | 继续发布(声明非阻塞) |
| IMAGE_CONVERT_FAILED | PL-PRODUCT图片规格转换失败 | 使用原图发布+警告 | 闲鱼可能显示变形 |
| COPYWRITE_CONVERT_FAILED | PL-PRODUCT文案风格转换失败 | 使用原文案发布 | 商品描述可能不符闲鱼风格 |
| PRODUCT_ELEMENT_MISSING | PL-PRODUCT 5要素缺失 | 缺价格→拒绝发布，缺其他→使用默认值 | 价格为必填(来源:01手册§四4.1) |
| XIANYU_PUBLISH_FAILED | 闲鱼商品发布失败 | 返回转换结果+发布失败详情 | 素材已转换可手动发布 |
| HOTSPOT_LOW_HEAT | PL-HOTSPOT热点热度不足(heat≤30) | 跳过该热点，处理下一个 | 仅处理heat>30的热点 |
| HOTSPOT_NO_PRODUCT | PL-HOTSPOT选品无合适商品(unified-product-ops返回空) | 终止该热点管道，记录原因 | 热点不适合选品，不强制上架 |
| HOTSPOT_CONVERT_FAILED | PL-HOTSPOT商品参数转换失败(AI生成失败) | 使用默认模板生成商品参数 | 商品描述可能不够精准 |
| MARKETING_GATE_FAILED | 营销注入门控失败(market-copywriter调用失败+降级也失败) | ❌拦截发布，不允许跳过 | 必须修复market-copywriter或降级模板后重试 |
| DIFFERENTIATION_FAILED | 内容差异化检查未通过(与24h内同主题内容相似度>70%) | ❌拦截发布，要求重新生成 | 调整至少1个差异化维度(切入角度/情绪基调/内容深度/表现形式) |
| ATTRACTIVENESS_SCORE_LOW | 内容吸引力评分<60分(标题/钩子/深度/CTA/SEO加权总分不达标) | ❌拦截发布，必须重新生成 | 按LLM返回的suggestion优化后重新评分 |

## 输入格式

支持自然语言指令或JSON结构化输入:

- **自然语言**: "帮我做一条AI热点短视频发到抖音和视频号"
- **JSON结构化**: `{"pipeline":"PL-VIDEO","tenant_id":"t_001","platforms":["douyin","shipinhao"],"topic":"AI头像生成"}`
- **热点驱动**: trend-discovery输出 `{topic, heat, platforms, trend}` 自动触发PL-HOTSPOT
- **素材驱动**: 用户上传素材列表 `{"materials":[...],"target":"xianyu_product"}` 触发PL-PRODUCT

## 输出格式

统一返回JSON结构(符合exec脚本规范):

```json
{
  "success": true,
  "data": {
    "task_id": "co-20260519-001",
    "pipeline": "PL-VIDEO",
    "published": {"douyin": {"status":"success","url":"..."}},
    "marketing_gate": "passed",
    "attractiveness_score": 85
  },
  "error": null,
  "code": null
}
```

异常时: `{"success":false,"data":{},"error":"MARKETING_GATE_FAILED","code":"GATE_BLOCKED"}`

## 业务交付物

运营报告模板见 `docs/templates/content_report.md`，exec脚本生成报告时填充实际数据。

## 业务工作流(高层)

内容生产全链路遵循以下业务闭环:
1. 选题: trend-discovery热点发现+content-research选题决策,确定内容方向
2. 素材: 竞品数据采集+用户上传素材处理,准备创作原料
3. 生成: 按管道类型(视频/图文/音频/漫画/小说/短剧)调用对应引擎生成内容
4. 质检: 质量门控+营销注入门控+吸引力评分+AI声明注入+差异化检查
5. 发布: content-publisher多平台分发,支持排期/定时/批量
6. 复盘: content-analytics效果分析(72h窗口),指导下一轮选题

> 以下"工作流"为管道执行层详细步骤,业务工作流为其提供高层上下文。

## 热点驱动发布工作流(B3-04/R-92闭环连接)

本章节集中声明热点→发布完整闭环链路,满足R-92闭环连接规范。链路通过两条管道实现:**E2E-DAILY**(热点→内容→多平台发布)和**PL-HOTSPOT**(热点→选品→商品→闲鱼发布),均以trend-discovery为统一热点输入源(B2-05已完成dailyhot-mcp统一)。

### 闭环链路图

```
trend-discovery(获取热点)
    │
    ├─[内容分发路径]──> E2E-DAILY管道 ─────────────> content-publisher(多平台发布)
    │                     ↓
    │               AI选题→自动选管道→AI声明注入→排期发布
    │
    └─[商品上架路径]──> PL-HOTSPOT管道 ────────────> fishclaw-mcp+content-publisher(闲鱼+多平台)
                          ↓
                    选品方向→unified-product-ops选品→商品参数转换→发布
```

### 链路依赖声明

| 链路节点 | Skill | 声明位置 | 依赖类型 |
|:---------|:------|:---------|:---------|
| 热点输入 | trend-discovery | content-publisher/SKILL.md dependencies | 静态依赖(已声明) |
| 热点输入 | trend-discovery | content-orchestrator业务工作流第1步 | 动态依赖(FIX-V3-009) |
| 热点输入 | dailyhot-mcp | trend-discovery/SKILL.md dependencies | 静态依赖(B2-05统一) |
| 内容生成 | content-orchestrator | content-publisher协作关系表 | 动态依赖 |
| 多平台发布 | content-publisher | content-orchestrator管道步骤(PL-HOTSPOT步骤15/E2E-DAILY排期发布) | 动态依赖 |
| 闲鱼发布 | fishclaw-mcp | content-orchestrator PL-HOTSPOT步骤14 | MCP依赖 |

### 工作流步骤(完整闭环)

1. **热点获取** — trend-discovery通过dailyhot-mcp统一采集4平台热榜(抖音/微博/知乎/B站,R-75碎片化统一化),输出`{topic, heat, platforms, trend}`
   - 触发方式: Cron每2小时自动触发 / 手动调用 / E2E-DAILY管道内置
   - 数据源: trend-discovery/SKILL.md v1.4已声明dailyhot-mcp为唯一数据源(B2-05完成)
2. **热点路由判定** — content-orchestrator接收trend-discovery输出,按热点类型路由:
   - 内容型热点(教程/科普/娱乐) → E2E-DAILY管道(热点→内容→多平台发布)
   - 商品型热点(可电商化) → PL-HOTSPOT管道(热点→选品→闲鱼商品发布)
3. **内容生成**(E2E-DAILY路径) — AI选题→自动选择PL-VIDEO/PL-IMAGE/PL-NOVEL等管道→内容生成
4. **选品上架**(PL-HOTSPOT路径) — 热点→选品方向→unified-product-ops选品→商品参数转换→5要素注入
5. **质检门控** — 营销注入门控+吸引力评分+AI声明注入+差异化检查+敏感词检测
6. **多平台发布** — content-publisher.publish统一分发到12平台(抖音/快手/小红书/B站/视频号/百家号/微信公众号/头条号/知乎/微博/抖音图文/TikTok),支持排期/定时/批量
7. **闲鱼商品发布**(PL-HOTSPOT路径) — fishclaw-mcp.publish_item发布到闲鱼,发布间隔≥5秒(来源:01手册§十10.1)
8. **结果回写** — 发布结果回写product_catalog(PL-HOTSPOT)或content_catalog(E2E-DAILY),记录热点→内容/商品映射关系
9. **复盘优化** — content-analytics效果分析(72h窗口),指导下一轮热点选题,形成闭环

### 异常处理

| 异常 | 处理 | 来源 |
|:-----|:-----|:-----|
| trend-discovery返回空热点 | 跳过本轮热点驱动发布,记录info日志 | trend-discovery/SKILL.md异常表 |
| unified-product-ops无合适选品 | 终止PL-HOTSPOT管道,返回`{success:false, error:"no_suitable_product", code:"HR-002"}` | content-orchestrator/SKILL.md异常表 |
| content-publisher发布失败 | 单平台失败不阻断其余,加入重试队列(指数退避1/5/15分钟) | content-publisher/SKILL.md步骤5.5 |
| 热点热度不足(heat≤30) | 跳过该热点,处理下一个 | HOTSPOT_LOW_HEAT异常码 |

### 验证状态

- ✅ trend-discovery SKILL.md v1.4(2026-07-17) B2-05已完成dailyhot统一
- ✅ content-publisher dependencies已声明trend-discovery(第15行)
- ✅ content-publisher协作关系表已声明trend-discovery(第377行,"热点结合排期")
- ✅ content-orchestrator业务工作流已声明trend-discovery为选题输入(第561行)
- ✅ E2E-DAILY管道定义完整(trend-discovery→AI选题→自动选管道→AI声明注入→排期发布)
- ✅ PL-HOTSPOT管道定义完整(17步,热点获取→...→多平台内容分发→发布反馈)
- ✅ PL-HOTSPOT.json管道文件存在(pipelines/PL-HOTSPOT.json,17步完整定义)
- **结论**: 热点→发布链路已连接,验证通过

## 内容闭环工作流(B3-08/R-99闭环连接)

本章节集中声明内容发布→采集→分析→优化的4步闭环链路,满足R-99闭环连接规范。闭环以content-orchestrator为编排中心,串联content-publisher(发布)→media-crawler(采集)→content-analytics(分析)→content-calibrator+seo-optimizer(优化)四个环节,形成持续迭代的内容优化循环。本闭环与content-analytics Skill的6步闭环(发布→推荐→反馈→分析→优化→学习)互补:content-analytics(v25.0合并content-closed-loop)是闭环执行引擎,本工作流是编排层声明。

### 闭环链路图

```
content-publisher(发布) ───> 多平台内容上线(12平台)
    │
    └─[发布结果回写]──> content_catalog(发布日志+post_ids)
                              │
                              ▼
                    media-crawler(采集) ───> 互动数据(播放/点赞/评论/分享)
                              │                 ┌─opencli-mcp(小红书/B站/知乎/微博 4平台真实数据)
                              │                 └─估算数据(抖音/快手/视频号等无API平台,标注REAL_DATA_UNAVAILABLE)
                              ▼
                    content-analytics(分析) ───> S/A/B/C评级+优化建议
                              │                 (播放量25%+完播率25%+互动率20%+转化率20%+分享率10%)
                              ▼
                    content-calibrator+seo-optimizer(优化) ───> 内容质量校准+SEO优化
                              │                 (7维评分:ER情感/HP钩子/SR议题/QL金句/NA叙事/AB受众/PV实用)
                              ▼
                    下一轮内容生成(注入优化建议+校准rubric)
```

### 链路依赖声明

| 链路节点 | Skill | 声明位置 | 依赖类型 |
|:---------|:------|:---------|:---------|
| 发布 | content-publisher | content-orchestrator管道步骤(PL-NOVEL步骤7/E2E-DAILY排期发布) | 动态依赖(FIX-V3-009) |
| 发布 | content-publisher | content-analytics/SKILL.md dependencies(反向) | 静态依赖(已声明) |
| 采集 | media-crawler | content-orchestrator PL-HOTSPOT步骤1.5/PL-NEWPROD步骤2.5 | 动态依赖 |
| 采集 | media-crawler-mcp | content-publisher/SKILL.md协作关系表(步骤2.5竞品参考) | MCP依赖 |
| 分析 | content-analytics | content-orchestrator业务工作流第6步+PL-NEWPROD步骤10 | 动态依赖 |
| 分析 | content-analytics | content-analytics dependencies=[content-publisher] | 静态依赖(已声明) |
| 优化 | content-calibrator | content-orchestrator PL-HOTSPOT.json步骤6(内容质量评分) | 动态依赖 |
| 优化 | seo-optimizer | content-orchestrator PL-NOVEL步骤5/通用流程步骤6 | 动态依赖 |
| 闭环引擎 | content-analytics | content-orchestrator业务工作流(6步闭环互补,v25.0合并content-closed-loop) | 动态依赖 |

### 4步闭环工作流(完整链路)

1. **发布(content-publisher)** — 内容生成完成后,通过content-publisher多平台分发
   - 输入: 已生成内容(视频/图文/音频)+目标平台列表+tenant_id
   - 执行: content-publisher.publish_now → 12平台分发(抖音/快手/小红书/B站/视频号/百家号/微信公众号/头条号/知乎/微博/抖音图文/TikTok)
   - 质检门控: 营销注入门控+吸引力评分+AI声明注入+差异化检查+SimHash去重
   - 输出: `{content_id, post_ids:{platform:url}, status:"published"}`
   - 结果回写: content_catalog表+memory/YYYY-MM-DD.md发布日志

2. **采集(media-crawler)** — 发布后72小时窗口采集互动数据
   - 真实数据采集: media-crawler-mcp采集小红书/B站/知乎/微博4平台(opencli-mcp兼容)
   - 无API平台降级: 抖音/快手/视频号等使用估算数据,标注`REAL_DATA_UNAVAILABLE`(来源:DEF-10)
   - 竞品数据采集(可选): media-crawler.search_posts采集同类竞品内容,format_for_prompt压缩为≤200 token
   - 输出: `{views, likes, comments, shares, click_rate, data_source:"real|estimated"}`
   - 失败处理: 采集失败→标记feedback为pending状态,等待真实API数据回填

3. **分析(content-analytics)** — 计算内容效果指标+评级+优化建议
   - 数据源优先级: data-copilot-mcp > postgres-mcp > analytics_cache > memory发布记录
   - 计算指标: 播放量/完播率=complete_views/views / 互动率=(likes+comments+shares)/views / 转化率=follows/views / 分享率=shares/views
   - 评级生成: S(>90)/A(70-90)/B(50-70)/C(≤50),权重:播放25%+完播25%+互动20%+转化20%+分享10%
   - 优化建议: C→详细 / B→基础 / A/S→成功要素总结
   - 常青内容识别: 30天持续流量>发布首日30%→标记常青(DEF-51)
   - 发布时机优化: 分析90天历史数据推荐最佳发布时段(DEF-51)
   - 输出: `{rating, score, metrics, score_breakdown, suggestions, evergreen}`

4. **优化(content-calibrator+seo-optimizer)** — 内容质量校准+SEO优化,指导下一轮生成
   - **content-calibrator(质量校准)**: 7维LLM评分(ER情感/HP钩子/SR议题/QL金句/NA叙事/AB受众/PV实用)+盲预测+T+3d复盘+rubric进化
     - 综合分校式: `composite = (ER×1.5 + HP×1.5 + SR×1.5 + QL + NA + AB + PV) / 8.5 × 2.0`
     - 盲预测: 仅喂稿件+rubric,不读对话历史,预测互动表现
     - T+3d复盘: 预测vs实际数据对比,计算偏差,更新rubric
   - **seo-optimizer(SEO优化)**: 关键词布局优化+标题SEO适配+标签优化
     - 来源:content-orchestrator PL-NOVEL步骤5/通用流程步骤6
   - 优化建议回写: 写入`memory/analytics/{content_id}.json`+`data/content-calibrator/rubric_{platform}.json`
   - 下一轮注入: content-orchestrator下一轮内容生成时,从memory/analytics读取历史优化建议,注入到管道step_params

### 异常处理

| 异常 | 处理 | 来源 |
|:-----|:-----|:-----|
| content-publisher发布失败 | 单平台失败不阻断其余,加入重试队列(指数退避1/5/15分钟) | content-publisher/SKILL.md步骤5.5 |
| media-crawler采集失败 | 跳过该平台采集,使用估算数据,标注REAL_DATA_UNAVAILABLE | DEF-10降级方案 |
| content-analytics数据不足 | 返回空分析,标注INSUFFICIENT_DATA,不生成评级 | content-analytics/SKILL.md异常表 |
| content-calibrator LLM评分失败 | 使用历史rubric作为兜底,记录warning | content-calibrator OPTIMIZE_FAILED |
| seo-optimizer不可用 | 跳过SEO优化,继续发布流程,记录warning | content-orchestrator异常表 |
| 闭环步骤执行超时(>60秒) | 跳过超时步骤,继续后续步骤,最终报告标注跳过项 | content-analytics LOOP_TIMEOUT |

### 与content-analytics Skill的关系(原content-closed-loop已合并)

content-analytics(v25.0合并content-closed-loop,R75.5 Skill去重)是6步闭环执行引擎(发布→推荐→反馈→分析→优化→学习),本工作流是content-orchestrator编排层的4步闭环声明。两者互补:
- content-orchestrator(本工作流): 编排层,声明闭环链路,负责发布→采集→分析→优化的Skill调度
- content-analytics: 执行层,执行6步闭环的完整循环,含推荐+反馈+学习步骤(v25.0合并自content-closed-loop)
- 协作方式: content-orchestrator在业务工作流第6步"复盘"中可调用content-analytics执行完整6步闭环,本4步闭环是其核心子集

### 验证状态

- ✅ content-publisher Skill存在(skills/content-publisher/SKILL.md v4.5.3)
- ✅ media-crawler Skill存在(skills/_lazy/media-crawler/SKILL.md,依赖media-crawler-mcp)
- ✅ content-analytics Skill存在(skills/content-analytics/SKILL.md v1.5,dependencies声明content-publisher)
- ✅ content-calibrator Skill存在(skills/content-calibrator/SKILL.md v1.0,7维评分+盲预测+T+3d复盘)
- ✅ seo-optimizer Skill存在(skills/seo-optimizer/SKILL.md)
- ✅ content-analytics Skill存在(skills/content-analytics/SKILL.md v2.0,v25.0合并content-closed-loop,6步闭环引擎)
- ✅ content-orchestrator业务工作流第6步已声明content-analytics(第566行)
- ✅ content-orchestrator PL-NEWPROD步骤10已声明content-analytics(第265行)
- ✅ content-orchestrator PL-HOTSPOT步骤1.5/PL-NEWPROD步骤2.5已声明media-crawler-mcp
- ✅ content-orchestrator PL-NOVEL步骤5/通用流程步骤6已声明seo-optimizer
- ✅ content-analytics dependencies已声明content-publisher(反向依赖,分析层依赖发布层)
- ✅ content-calibrator dependencies已声明published-track(发布记录统一入口)
- **结论**: 内容发布→采集→分析→优化闭环已连接,验证通过

## 工作流

### 智能路由流程
1. **接收请求**: 解析用户意图,识别管道类型(VIDEO/IMAGE/NOVEL/DRAMA/PRODUCT/HOTSPOT等13种)
2. **平台注册表路由**: 根据目标平台自动选择发布MCP(sau-mcp视频/device-operations-mcp图文/wechat-official-account-mcp公众号)
3. **代理自动注入**: 根据tenant_id自动注入租户配置(风格/人设/素材/平台隔离)
4. **管道执行**: 按管道定义顺序执行各阶段(生成→营销门控→AI声明→发布)
5. **结果回写**: 发布结果回写product_catalog(PL-PRODUCT/PL-HOTSPOT)或content_catalog(内容管道)

> **FIX-V3-009动态依赖发现**: 管道Skill(video-generator/content-publisher/cosyvoice/flux/kling/pps等)在运行时由编排器自动发现和加载,而非通过frontmatter dependencies硬编码声明。编排器根据管道类型和阶段需求,动态匹配并调用对应的Skill。metadata.dynamic_dependencies=true启用此模式。

### 通用流程(所有管道)
1. 管道类型识别 → 2. 租户配置注入 → 3. 素材/热点获取 → 4. 内容生成 → 5. 🔴营销注入门控 → 6. SEO优化 → 7. AI声明注入 → 8. 多平台发布 → 9. 结果回写

## 经验回写(自生长闭环)

内容生成与发布完成后,自动回写经验到自生长系统,供后续生成参考(自生长引擎路径: `skills/_lazy/self-growth/scripts/self_growth_engine.py`,支持action: extract/learn/query/stats):

1. 生成前查询历史经验: `python skills/_lazy/self-growth/scripts/self_growth_engine.py --action query --keyword "内容编排" --limit 5 --agent-id default` — 注入历史经验到管道参数,优化管道路由决策
2. 生成成功后记录经验: `python skills/_lazy/self-growth/scripts/self_growth_engine.py --action extract --from content-orchestrator --success true --result-data '{"pipeline":"...","published":{...}}' --agent-id default` — 记录成功生成模式
3. 生成失败时记录错误教训: `python skills/_lazy/self-growth/scripts/self_growth_engine.py --action learn --scenario "内容编排失败" --lesson "[错误码和原因]" --category error --importance 8 --agent-id default` — 错误经验自动记录,避免重复犯错
4. 定期统计经验: `python skills/_lazy/self-growth/scripts/self_growth_engine.py --action stats --agent-id default` — 统计经验积累情况

### 已有管道自生长接入文档化

content-orchestrator已通过以下管道在脚本层面接入自生长闭环(调用self_growth_activator.record_feedback):

- **PL-HOTSPOT管道**: `content_orchestrator.py` L1077 — 热点→商品发布后调用 `self_growth_activator.record_feedback` 记录热点选题经验
- **PL-PRODUCT管道**: `content_orchestrator.py` L1093 — 素材→商品发布后调用 `self_growth_activator.record_feedback` 记录产品生成经验
- **fallback路径**: `content_orchestrator.py` L379 — self_growth_activator.py存在于scripts/目录,作为exec脚本的fallback路径

> 注: PL-HOTSPOT和PL-PRODUCT管道定义内置于content_orchestrator.py中(非外部JSON文件),在"多平台内容分发"步骤后自动执行"发布反馈(U13)"步骤调用self_growth_activator。

## 质量门控

每条管道的关键阶段输出通过`scripts/quality_gate.py`执行质量门控检查，综合得分≥阈值（默认0.7）才允许进入下一阶段。质量门控在内容生成完成后、营销注入门控之前执行，是管道阶段间的硬性质量卡点。

### 门控执行方式

```bash
python skills/content-orchestrator/scripts/quality_gate.py \
  --pipeline-name PL-VIDEO \
  --stage content \
  --content-file data/content/draft.txt \
  --threshold 0.7
```

- `--pipeline-name`: 管道名称（如PL-VIDEO/PL-IMAGE/PL-NOVEL等）
- `--stage`: 检查阶段（draft/script/content/final，不同阶段最低字数要求不同）
- `--content-file`: 待检查内容文件路径
- `--threshold`: 通过阈值（默认0.7，综合得分≥阈值且敏感词检查通过才放行）

### 四个检查维度

| 维度 | 检查内容 | 权重 | 不达标处理 |
|:-----|:---------|:-----|:-----------|
| 内容长度 | 按阶段检查最低字数（draft≥200/script≥300/content≥500/final≥800） | 25% | 建议补充内容至达标字数 |
| 关键词覆盖 | 检查标题/段落/标签三要素覆盖率是否≥阈值 | 25% | 建议补充缺失的关键词要素 |
| 格式合规 | 检查标题结构/段落分隔/长文本分段是否合规 | 25% | 建议优化格式结构 |
| 敏感词检测 | 调用sensitive-word-mcp检测敏感词（MCP不可用时降级本地词库检查） | 25% | 命中敏感词直接拦截，不允许进入下一阶段 |

### 门控规则

- 综合得分 = (长度得分 + 关键词得分 + 格式得分 + 敏感词得分) / 4
- 综合得分≥阈值 **且** 敏感词检查通过 → ✅放行，进入下一阶段
- 综合得分<阈值 **或** 敏感词命中 → ❌拦截，返回修改建议，要求优化后重新检查
- 敏感词检测为一票否决项：即使综合得分达标，敏感词命中也直接拦截

### 输出格式

```json
{
  "success": true,
  "data": {
    "passed": true,
    "score": 0.85,
    "pipeline": "PL-VIDEO",
    "stage": "content",
    "threshold": 0.7,
    "checks": {
      "length": {"passed": true, "score": 1.0, "detail": "字数620/500达标"},
      "keywords": {"passed": true, "score": 1.0, "detail": "覆盖率100%"},
      "format": {"passed": true, "score": 0.67, "detail": "问题:缺少标题"},
      "sensitive": {"passed": true, "score": 1.0, "detail": "无敏感词"}
    },
    "suggestions": ["优化格式:添加标题和段落分隔"]
  },
  "error": null,
  "code": null
}
```

## 示例

### 一键视频发布

1. 输入: "帮我做一条AI热点短视频发到抖音和视频号"
2. 解析→PL-VIDEO→narrato-mcp脚本→cosyvoice配音→kling画面→合成→AI声明注入→发布
3. 输出: `{success:true, data:{task_id:"co-20260519-001", pipeline:"PL-VIDEO", published:{douyin:{status:"success"}}}}`

### 热点选品上架

1. 输入: trend-discovery输出热点数据 `{topic:"AI头像生成", heat:92, platforms:["小红书","抖音"], trend:"上升"}`
2. 解析→PL-HOTSPOT→热点→选品方向→unified-product-ops选品→商品参数转换→xianyu-manager发布
3. 输出: `{success:true, data:{product_id:"xy-20260528-001", xianyu_url:"https://...", hotspot_topic:"AI头像生成", heat:92, pipeline:"PL-HOTSPOT"}}`

> UTD调用/E2E日常运营示例详见 scripts/content_orchestrator_reference.json
