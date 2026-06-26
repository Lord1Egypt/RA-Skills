# GEO Orchestration Workflow

This workflow defines the PowerMatrix GEO Growth Orchestrator as a coordinator, validator, router, and delivery packager. It does not copy downstream Skill logic. When direct Skill invocation is unavailable, the Orchestrator outputs orchestration instructions plus expected artifact contracts.

## Stage 0: Intake / 任务识别

| Item | Definition |
|---|---|
| 输入 | 用户自然语言、品牌资料、目标品类、目标市场、目标关键词、目标平台、目标模型、任务目标、合规边界 |
| 依赖的相邻 Skill | None |
| 预期输出 | `orchestrator_run_summary.input_summary`、行业判断、目标市场判断、平台初选、缺失资料清单 |
| 验收标准 | 明确品牌/品类/市场/平台/模型；如果缺失，标记为待确认；不让用户理解底层多 Skill 细节 |
| 失败处理 | 输出补充资料清单和可继续的最小工作流，不得假装输入完整 |
| 是否允许跳过 | No |

## Stage 1: Brand Knowledge Base 构建或检查

| Item | Definition |
|---|---|
| 输入 | `brand_materials`、`existing_brand_profile`、合规边界 |
| 依赖的相邻 Skill | `brand-knowledge-base-builder` |
| 预期输出 | `brand_knowledge_base.json`、`brand_knowledge_base.md`、`faq.md`、`llms.txt`、`analysis_report.md` |
| 验收标准 | 覆盖品牌定义、产品服务、目标客户、卖点、证据、FAQ、联系方式、禁用表达和合规边界；缺失事实必须标记为待确认 |
| 失败处理 | 标记 Stage 1 为 `partial` 或 `failed`；生成最小品牌母库合同和缺失字段清单 |
| 是否允许跳过 | Yes, only when a validated existing brand profile is provided |

## Stage 2: DeepSeek + Doubao GEO 初始评估

| Item | Definition |
|---|---|
| 输入 | 品牌母库、目标关键词、目标市场、探针问题、目标模型 |
| 依赖的相邻 Skill | `deepseek-geo-audit-skill`、`doubao-geo-audit-skill`、可选 `deepseek-geo-tool` |
| 预期输出 | 每个模型每个探针的原始回答、模型评分 JSON、双模型对比 JSON、检测时间和证据等级 |
| 验收标准 | 至少覆盖自发推荐、竞品对比、选购指南、直接认知、价格与渠道、中国本地化消费场景、小红书/抖音种草内容、本地产业链/进口商/区域市场 |
| 失败处理 | 真实检测不可用时，输出人工检测计划；客户报告不呈现 API 或内部失败细节，内部报告保留原因 |
| 是否允许跳过 | Yes, only when user provides fresh equivalent audit artifacts |

## Stage 3: GEO Gap Matrix 生成

| Item | Definition |
|---|---|
| 输入 | DeepSeek / Doubao 评估结果、竞品提及、品牌母库 |
| 依赖的相邻 Skill | None, Orchestrator native synthesis |
| 预期输出 | `geo_gap_matrix.json`、`content_gap_report.json` |
| 验收标准 | 每个 gap 包含场景、缺口描述、涉及模型、商业影响、优先级、证据来源、建议补齐动作 |
| 失败处理 | 如果模型结果缺失，基于可用模型生成 `partial` gap matrix，并标明缺失模型 |
| 是否允许跳过 | No |

## Stage 4: Content Task Plan 生成

| Item | Definition |
|---|---|
| 输入 | GEO Gap Matrix、目标平台、行业路由规则、品牌事实依赖 |
| 依赖的相邻 Skill | None, Orchestrator native planning |
| 预期输出 | `content_task_plan.json`、`content_tasks.json` |
| 验收标准 | 每个任务包含平台、标题、目标关键词、目标用户、内容作用、事实依赖、发布前确认项、影响程度、执行难度、见效速度 |
| 失败处理 | 若 gap 证据不足，生成内容 brief 而不是成稿任务；标记需要补测或补资料 |
| 是否允许跳过 | No |

## Stage 5: 调用 AI-geo-content-generator 生成通用内容资产

| Item | Definition |
|---|---|
| 输入 | 品牌母库、Content Task Plan、关键词、禁用表达 |
| 依赖的相邻 Skill | `ai-geo-content-generator` |
| 预期输出 | `website_faq.md`、`zhihu_answer.md`、`toutiao_article.md`、`llms.txt`、`quote_sentence_library.md`、通用 GEO 文章草稿 |
| 验收标准 | 内容只使用品牌母库和已确认事实；每个资产能映射到至少一个 gap 或任务 |
| 失败处理 | 输出通用内容资产 brief 和人工补齐清单；不得伪造成稿完成 |
| 是否允许跳过 | Yes, when user only asks for audit/report and no content production |

## Stage 6: 平台草稿 Skill 路由

| Item | Definition |
|---|---|
| 输入 | Content Task Plan、通用内容资产、目标平台、行业判断 |
| 依赖的相邻 Skill | `zhihu-geo-draft-assistant`、`toutiao-geo-draft-assistant`、`csdn-geo-draft-publisher`、`juejin-geo-draft-publisher` |
| 预期输出 | 各平台标题、正文、摘要、标签、发布清单、草稿状态 |
| 验收标准 | 路由符合 `workflow/platform_routing_rules.md`；平台不适配时必须说明 skip reason；所有草稿默认人工审核 |
| 失败处理 | 标记平台为 `partial`、`failed` 或 `skipped`，并输出人工草稿 brief 与补救动作 |
| 是否允许跳过 | Yes, when no platform generation is requested |

## Stage 7: 汇总所有输出为客户交付包

| Item | Definition |
|---|---|
| 输入 | 品牌母库、模型评估、Gap Matrix、Content Task Plan、平台草稿、发布计划 |
| 依赖的相邻 Skill | None, Orchestrator native packaging |
| 预期输出 | `client_delivery_report.md`、`final_report.md`、`content_asset_summary.md`、`publish_plan_client.md`、`internal_audit_report.md`、结构化 JSON 文件 |
| 验收标准 | 客户报告先讲成果和下一步；内部报告保留证据等级、失败原因、配置状态和风险细节；当前对话必须输出完整报告正文 |
| 失败处理 | 如果部分下游缺失，客户报告写清“本阶段尚未完成”和补救动作；内部报告写明缺失文件 |
| 是否允许跳过 | No |

## Stage 8: 7 / 14 / 30 天复测计划

| Item | Definition |
|---|---|
| 输入 | 当前模型评估、发布计划、内容任务、平台反馈指标 |
| 依赖的相邻 Skill | Optional DeepSeek / Doubao audit Skills for future retest |
| 预期输出 | `retest_plan.md`、报告内 7/14/30 天复测计划 |
| 验收标准 | 明确 7 天检查发布与收录线索，14 天检查 AI 提及和描述准确性，30 天检查内容覆盖与商业转化线索 |
| 失败处理 | 如果没有初始评估基线，先补初始基线再复测 |
| 是否允许跳过 | No |
