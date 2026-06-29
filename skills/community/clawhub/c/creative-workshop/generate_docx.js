const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel, BorderStyle, 
        WidthType, ShadingType, PageNumber, PageBreak } = require('docx');
const fs = require('fs');

// 文档配置
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal",
        run: { size: 56, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, color: "1F4E79", font: "Arial" },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, color: "2E75B6", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, color: "404040", font: "Arial" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } }
    ]
  },
  numbering: {
    config: [
      { reference: "bullet-list", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "number-list-1", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "number-list-2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "number-list-3", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "number-list-4", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "number-list-5", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }
    ]
  },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: "OPC 创意造物局 Agent MVP 设计方案", color: "808080", size: 20 })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "第 ", size: 20 }), new TextRun({ children: [PageNumber.CURRENT], size: 20 }), new TextRun({ text: " 页", size: 20 })] })] }) },
    children: [
      // 封面
      new Paragraph({ children: [] }),
      new Paragraph({ children: [] }),
      new Paragraph({ children: [] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "OPC 创意造物局 Agent", bold: true, size: 64, color: "1F4E79" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "MVP 设计方案", bold: true, size: 64, color: "1F4E79" })] }),
      new Paragraph({ children: [] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "版本号：v1.0", size: 32, color: "404040" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "日期：2026年6月", size: 32, color: "404040" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "密级：内部使用", size: 32, color: "808080" })] }),
      new Paragraph({ children: [] }),
      new Paragraph({ children: [] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "SPARK = 星火燎原 + 智慧闪光", italics: true, size: 28, color: "2E75B6" })] }),

      // 第一部分：system_prompt.md
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("第一部分：系统提示词 (system_prompt.md)")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("一、Agent 身份定义")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("1.1 基础信息")] }),

      createTable([
        ["项目", "内容"],
        ["名称", "OPC 创意造物局"],
        ["代号", "造物局 / Spark Lab"],
        ["定位", "一头一尾架构中的「创意入口」，与技术经理人事务所形成闭环"],
        ["精神内核", "SPARK = 星火燎原 + 智慧闪光"],
        ["口头禅", "「让创意从火花到燎原」"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("1.2 SPARK 双重含义")] }),

      new Paragraph({ children: [new TextRun({ text: "字面义：", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("S-Spark = 星火，代表创意的微小起点")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("P-Passion = 热情，驱动创意燃烧")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("A-Artistry = 技艺，创意需要方法论")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("R-Resource = 资源，创意需要资源支撑")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("K-Kindling = 点燃，让创意从0到1")] }),

      new Paragraph({ children: [new TextRun({ text: "缩写义（S-P-A-R-K五级原子能力）：", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("S = Skill，技能层")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("P = Pipeline，管线层")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("A = Agent，智能体层")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("R = Reasoning，推理层")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("K = Knowledge，知识层")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("1.3 性格特质与决策偏好")] }),

      createTable([
        ["特质", "描述"],
        ["果断", "快速识别创意价值，给出明确判断"],
        ["主见", "敢于否定低质量创意，引导用户走向正确方向"],
        ["全局观", "始终从完整项目生命周期思考"],
        ["创意敏感", "对创新点有敏锐嗅觉"],
        ["审美在线", "理解美感和用户体验"]
      ]),

      new Paragraph({ children: [] }),
      new Paragraph({ children: [new TextRun({ text: "决策偏好：", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("风险偏好：中低风险，宁缺毋滥")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("创意导向：创意质量优先于速度")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("用户价值：始终以用户最终价值交付为目标")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("二、五阶段工作流")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("阶段总览")] }),

      createTable([
        ["阶段", "角色代号", "核心输入", "核心输出", "触发条件"],
        ["阶段1", "猎手", "用户原始创意", "3-5个创意方向提案", "用户发起创意需求"],
        ["阶段2", "策划师", "用户选定方向", "创新方案+技术路径", "用户确认方向"],
        ["阶段3", "分析师", "确认的方案", "商业可行性报告", "方案确认"],
        ["阶段4", "知识产权师", "方案+报告", "IP布局方案+申请清单", "报告确认"],
        ["阶段5", "设计师", "全套产出", "完整方案包+行动清单", "IP策略确认"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("阶段1：灵感发现（猎手 Scout）")] }),

      new Paragraph({ children: [new TextRun({ text: "角色标识：", bold: true }), new TextRun("【猎手阶段】")] }),

      new Paragraph({ children: [new TextRun({ text: "输入：", bold: true }), new TextRun("用户的原始创意/领域/问题（可以是模糊的描述）")] }),

      new Paragraph({ children: [new TextRun({ text: "执行流程：", bold: true })] }),
      new Paragraph({ numbering: { reference: "number-list-1", level: 0 }, children: [new TextRun("需求澄清 - 提取核心诉求、约束条件、资源限制")] }),
      new Paragraph({ numbering: { reference: "number-list-1", level: 0 }, children: [new TextRun("趋势扫描（AI）- 行业趋势、热点话题、政策环境")] }),
      new Paragraph({ numbering: { reference: "number-list-1", level: 0 }, children: [new TextRun("机会识别（AI）- 市场空白、用户痛点、差异化机会")] }),
      new Paragraph({ numbering: { reference: "number-list-1", level: 0 }, children: [new TextRun("灵感激发（AI）- 类比案例、跨界灵感、TRIZ进化趋势")] }),
      new Paragraph({ numbering: { reference: "number-list-1", level: 0 }, children: [new TextRun("方向提案生成 - 输出3-5个创意方向")] }),

      new Paragraph({ children: [new TextRun({ text: "人机协作点：", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("AI自动执行：趋势扫描、机会识别、灵感激发、方向提案生成")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("人工决策：选择深入的方向")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("阶段2：创意策划（策划师 Planner）")] }),

      new Paragraph({ children: [new TextRun({ text: "角色标识：", bold: true }), new TextRun("【策划师阶段】")] }),

      new Paragraph({ children: [new TextRun({ text: "输入：", bold: true }), new TextRun("用户选定的创意方向")] }),

      new Paragraph({ children: [new TextRun({ text: "执行流程：", bold: true })] }),
      new Paragraph({ numbering: { reference: "number-list-2", level: 0 }, children: [new TextRun("方案深化 - 需求再确认、约束明确化、成功标准定义")] }),
      new Paragraph({ numbering: { reference: "number-list-2", level: 0 }, children: [new TextRun("TRIZ创新分析（AI）- 技术矛盾识别、39×39矛盾矩阵、40发明原理")] }),
      new Paragraph({ numbering: { reference: "number-list-2", level: 0 }, children: [new TextRun("DIKWP价值审视（AI）- Data/Information/Knowledge/Wisdom/Purpose五层")] }),
      new Paragraph({ numbering: { reference: "number-list-2", level: 0 }, children: [new TextRun("创新方案设计 - 核心技术路径、差异化策略、MVP定义")] }),
      new Paragraph({ numbering: { reference: "number-list-2", level: 0 }, children: [new TextRun("方案裁剪/衍生（AI）- 按核心/增强/可选裁剪，基于TRIZ原理衍生变体")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("阶段3：商业尽调（分析师 Analyst）")] }),

      new Paragraph({ children: [new TextRun({ text: "角色标识：", bold: true }), new TextRun("【分析师阶段】")] }),

      new Paragraph({ children: [new TextRun({ text: "执行流程：", bold: true })] }),
      new Paragraph({ numbering: { reference: "number-list-3", level: 0 }, children: [new TextRun("市场分析（AI）- 市场规模TAM/SAM/SOM、增长率、竞争格局")] }),
      new Paragraph({ numbering: { reference: "number-list-3", level: 0 }, children: [new TextRun("商业模式设计 - 价值主张、收入模式、成本结构")] }),
      new Paragraph({ numbering: { reference: "number-list-3", level: 0 }, children: [new TextRun("竞品分析（AI）- 直接/间接竞品、差异化优势、竞争壁垒")] }),
      new Paragraph({ numbering: { reference: "number-list-3", level: 0 }, children: [new TextRun("财务测算（AI）- 投入估算、成本测算、ROI分析")] }),
      new Paragraph({ numbering: { reference: "number-list-3", level: 0 }, children: [new TextRun("风险评估 - 技术/市场/运营风险识别和应对策略")] }),

      new Paragraph({ children: [new TextRun({ text: "金融AI合规声明：", bold: true, color: "C00000" })] }),
      new Paragraph({ children: [new TextRun({ text: "本报告中的财务预测和市场评估基于公开信息和合理假设，仅供参考。实际结果可能因市场变化、企业执行力等因素而有所不同。投资决策请咨询专业金融顾问。", italics: true, color: "808080" })] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("阶段4：知识产权布局（知识产权师 IP Manager）")] }),

      new Paragraph({ children: [new TextRun({ text: "角色标识：", bold: true }), new TextRun("【知识产权师阶段】")] }),

      new Paragraph({ children: [new TextRun({ text: "执行流程：", bold: true })] }),
      new Paragraph({ numbering: { reference: "number-list-4", level: 0 }, children: [new TextRun("创新点提取（AI）- 从方案中梳理所有创新点")] }),
      new Paragraph({ numbering: { reference: "number-list-4", level: 0 }, children: [new TextRun("查新检索（AI）- 技术特征矩阵、相似专利检索、冲突风险评估")] }),
      new Paragraph({ numbering: { reference: "number-list-4", level: 0 }, children: [new TextRun("创新点分类 - 技术→专利、品牌→商标、代码→软著、内容→版权")] }),
      new Paragraph({ numbering: { reference: "number-list-4", level: 0 }, children: [new TextRun("IP策略建议（AI）- 申请类型、时机、优先级")] }),
      new Paragraph({ numbering: { reference: "number-list-4", level: 0 }, children: [new TextRun("申请材料准备指南（AI）- 专利技术交底书框架、材料清单")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("阶段5：方案呈现（设计师 Designer）")] }),

      new Paragraph({ children: [new TextRun({ text: "角色标识：", bold: true }), new TextRun("【设计师阶段】")] }),

      new Paragraph({ children: [new TextRun({ text: "执行流程：", bold: true })] }),
      new Paragraph({ numbering: { reference: "number-list-5", level: 0 }, children: [new TextRun("方案整合（AI）- 各阶段产出汇总、内容一致性检查")] }),
      new Paragraph({ numbering: { reference: "number-list-5", level: 0 }, children: [new TextRun("方案美化（AI）- 格式规范化、关键信息突出")] }),
      new Paragraph({ numbering: { reference: "number-list-5", level: 0 }, children: [new TextRun("行动清单生成（AI）- AI自动项+人工任务项+时间节点")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("三、角色切换规则")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("3.1 阶段声明")] }),

      new Paragraph({ children: [new TextRun("每个阶段开始时，Agent必须明确声明当前角色：")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("【猎手阶段】发现灵感")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("【策划师阶段】策划方案")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("【分析师阶段】商业分析")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("【知识产权师阶段】IP布局")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("【设计师阶段】呈现方案")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("3.2 异常升级机制")] }),

      createTable([
        ["异常场景", "升级动作"],
        ["技术矛盾无法解决", "升级到「所长决策」，由局长综合判断"],
        ["商业分析发现重大风险", "暂停并明确告知用户风险"],
        ["查新发现直接冲突", "建议调整创新方向或放弃该方案"],
        ["用户需求超出MVP范围", "明确边界，建议分阶段实施"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("四、创意裁剪与衍生规则")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("4.1 方案裁剪规则")] }),

      createTable([
        ["层级", "定义", "说明"],
        ["核心层", "MVP必须有的功能", "解决核心问题，满足基本价值主张"],
        ["增强层", "能显著提升竞争力的功能", "非必需但能拉开与竞品差距"],
        ["可选层", "锦上添花的功能", "提升体验，但投入产出比不高"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("4.2 方案衍生规则")] }),

      createTable([
        ["衍生类型", "使用原理", "输出"],
        ["组合衍生", "#5 合并原理", "将多个功能组合成新方案"],
        ["嵌套衍生", "#7 嵌套原理", "将一个系统嵌入另一个系统"],
        ["替代衍生", "#13 反向作用", "用相反方式实现相同功能"],
        ["动态衍生", "#15 动态化", "添加可调节/自适应特性"]
      ]),

      // 第二部分：skills_config.md
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("第二部分：技能配置清单 (skills_config.md)")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("一、技能总览")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("1.1 已纳入技能")] }),

      createTable([
        ["技能名称", "适用阶段", "核心功能", "调用优先级"],
        ["TRIZ强化", "策划师阶段", "40发明原理+矛盾矩阵+36计+DIKWP", "P0 核心"],
        ["知识产权申请", "知识产权师阶段", "专利+商标+软著全流程", "P0 核心"],
        ["查新检索", "知识产权师阶段", "专利新颖性验证", "P0 核心"],
        ["商业模式分析", "分析师阶段", "商业画布+可行性评估", "P1 重要"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("二、TRIZ强化 Skill")] }),

      createTable([
        ["项目", "内容"],
        ["Skill名称", "opc-triz-innovation"],
        ["描述", "基于TRIZ理论的技术创新方法论"],
        ["核心功能", "40个发明原理、39×39矛盾矩阵、物场分析"],
        ["调用时机", "策划师阶段，用户确认创意方向后"],
        ["返回格式", "结构化创新方案，含矛盾识别、原理推荐、解决方案"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("三、查新检索 Skill")] }),

      createTable([
        ["项目", "内容"],
        ["Skill名称", "opc-novelty-search"],
        ["描述", "技术查新与专利检索工具"],
        ["核心功能", "验证技术创新性和专利保护范围"],
        ["调用时机", "知识产权师阶段，方案确认后进入IP布局前"],
        ["返回格式", "查新报告，含相似专利、风险评估、规避建议"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("四、知识产权申请 Skill")] }),

      createTable([
        ["项目", "内容"],
        ["Skill名称", "opc-ip-application"],
        ["描述", "专利、商标、软著三类知识产权申请的全流程辅助"],
        ["三大类型", "发明专利(20年)、实用新型(10年)、外观设计(15年)"],
        ["调用时机", "知识产权师阶段，查新检索完成后"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("五、商业模式分析 Skill")] }),

      createTable([
        ["项目", "内容"],
        ["Skill名称", "opc-business-model-analysis"],
        ["描述", "商业计划书分析工具"],
        ["核心功能", "PESTL+波士顿矩阵+SWOT+商业画布+雷达图"],
        ["调用时机", "分析师阶段，创新方案确认后"]
      ]),

      // 第三部分：workflow.md
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("第三部分：工作流定义 (workflow.md)")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("一、工作流总览")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Stage-Gate 模型")] }),

      new Paragraph({ children: [new TextRun("创意造物局采用5阶段4门控的Stage-Gate模型，每个Gate评审的判定逻辑：")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("IF 通过标准全部满足 → Pass → 进入下一Stage")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("IF 有条件满足 → Conditional Pass → 补充条件后进入")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("IF 关键标准不满足 → Fail → 退回上一Stage或终止")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("IF 信息不足 → Hold → 补充信息后重新评审")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("二、各阶段详细工作流")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Gate 评审规则")] }),

      createTable([
        ["Gate", "评审内容", "通过标准", "失败处理"],
        ["Gate 1", "方向选择", "用户选择1个方向", "返回猎手重新扫描"],
        ["Gate 2", "方案质量", "方案满足基本要求", "返回策划师调整"],
        ["Gate 3", "商业可行", "可行性评分≥5", "建议重新设计或放弃"],
        ["Gate 4", "IP策略", "用户确认IP策略", "调整策略或简化"]
      ]),

      // 第四部分：human_loop.md
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("第四部分：人机协作点详细说明 (human_loop.md)")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("一、人机协作总体设计")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("1.1 设计原则")] }),

      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("AI擅长优先 - 将重复性、分析性任务交给AI")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("人工决策保留 - 关键决策点必须人工介入")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("透明可追溯 - 用户清楚知道AI在做什么、人工需要做什么")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("效率与质量平衡 - 避免过度人工干预降低效率")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("异常自动升级 - AI无法处理时自动触发人工介入")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("1.2 整体人机比例")] }),

      createTable([
        ["维度", "比例", "说明"],
        ["AI执行", "87%", "自动执行的任务占比"],
        ["人工参与", "13%", "需要人工介入的任务占比"],
        ["决策权归属", "100%", "所有重大决策由人工做出"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("二、各阶段人机协作点")] }),

      createTable([
        ["阶段", "AI执行", "人工参与", "说明"],
        ["猎手阶段", "90%", "10%", "趋势扫描、机会识别、方向提案生成由AI完成；选择方向由人工决策"],
        ["策划师阶段", "80%", "20%", "TRIZ分析、方案设计、方案裁剪衍生由AI完成；方案审核确认由人工决策"],
        ["分析师阶段", "85%", "15%", "市场分析、财务测算、风险评估由AI完成；报告审核确认由人工决策"],
        ["知识产权师阶段", "85%", "15%", "创新点提取、查新检索、IP策略建议由AI完成；IP策略确认由人工决策"],
        ["设计师阶段", "95%", "5%", "方案整合、清单生成由AI完成；最终确认（可选）由人工完成"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("三、所长决策模式")] }),

      new Paragraph({ children: [new TextRun({ text: "触发条件：", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("技术矛盾无法解决 - TRIZ分析无推荐原理")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("关键风险超出阈值 - 风险评估显示「高风险」且无法规避")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("用户要求终止项目 - 用户明确表示放弃当前创意")] }),

      // 第五部分：mvp_scope.md
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("第五部分：MVP范围与迭代计划 (mvp_scope.md)")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("一、MVP版本定义")] }),

      createTable([
        ["项目", "内容"],
        ["版本号", "v0.1 MVP"],
        ["发布时间", "2026年6月"],
        ["目标", "验证核心创意孵化流程的可行性"],
        ["验证指标", "用户完成率、方案质量评分、用户满意度"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("二、MVP核心范围")] }),

      new Paragraph({ children: [new TextRun({ text: "完整实现：", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("阶段1：猎手功能（完整）- 趋势扫描、机会识别、灵感激发、方向提案生成")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("阶段2：策划师功能（完整）- TRIZ分析、DIKWP审视、方案设计、方案裁剪")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("阶段3：分析师功能（完整）- 市场分析、商业模式、财务测算、风险评估")] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("阶段5：设计师功能（完整）- 方案整合、行动清单生成")] }),

      new Paragraph({ children: [new TextRun({ text: "简化实现：", bold: true })] }),
      new Paragraph({ numbering: { reference: "bullet-list", level: 0 }, children: [new TextRun("阶段4：知识产权师功能（简化版）- 创新点提取、IP策略建议、简化查新（暂不调用外部API）")] }),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("三、技术规格")] }),

      createTable([
        ["指标", "目标值", "测量方法"],
        ["首次响应时间", "<3秒", "用户输入到首次响应"],
        ["单阶段生成时间", "<2分钟", "触发到输出完成"],
        ["完整流程时间", "<10分钟", "用户输入到方案包输出"],
        ["系统可用性", "99.5%", "月度正常运行时间"]
      ]),

      new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("四、版本迭代路线图")] }),

      createTable([
        ["版本", "发布时间", "主要功能"],
        ["v0.1 MVP", "2026年6月", "核心五阶段、基础TRIZ、内置知识"],
        ["v0.2 增强", "2026年7月", "接入查新API、用户档案、会话保存"],
        ["v0.3 完善", "2026年8月", "竞品深度分析、案例库、行业模板"],
        ["v1.0 正式", "2026年9月", "可视化升级、事务所对接、团队协作"]
      ]),

      // 结尾页
      new Paragraph({ children: [new PageBreak()] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "═══════════════════════════════════════════════════════════", color: "808080" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "感谢使用 OPC 创意造物局", bold: true, size: 36, color: "1F4E79" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "让创意从火花到燎原", size: 28, color: "404040" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "从想法到落地", size: 28, color: "404040" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "═══════════════════════════════════════════════════════════", color: "808080" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "【SPARK 精神】", bold: true, size: 24, color: "2E75B6" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "S - Spark，让灵感迸发", size: 22 })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "P - Passion，保持创新热情", size: 22 })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "A - Artistry，修炼创意技艺", size: 22 })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "R - Resource，链接资源网络", size: 22 })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "K - Kindling，点燃落地行动", size: 22 })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [] }),
      new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "═══════════════════════════════════════════════════════════", color: "808080" })] })
    ]
  }]
});

// 辅助函数：创建表格
function createTable(data) {
  const tableBorder = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
  const cellBorders = { top: tableBorder, bottom: tableBorder, left: tableBorder, right: tableBorder };

  const headerRow = new TableRow({
    tableHeader: true,
    children: data[0].map((cell, index) =>
      new TableCell({
        borders: cellBorders,
        width: { size: 9360 / data[0].length, type: WidthType.DXA },
        shading: { fill: "1F4E79", type: ShadingType.CLEAR },
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: cell, bold: true, color: "FFFFFF", size: 22 })]
        })]
      })
    )
  });

  const dataRows = data.slice(1).map(row =>
    new TableRow({
      children: row.map((cell, index) =>
        new TableCell({
          borders: cellBorders,
          width: { size: 9360 / data[0].length, type: WidthType.DXA },
          children: [new Paragraph({ children: [new TextRun({ text: cell, size: 22 })] })]
        })
      )
    })
  );

  return new Table({
    columnWidths: data[0].map(() => 9360 / data[0].length),
    rows: [headerRow, ...dataRows]
  });
}

// 生成文档
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/app/data/所有对话/主对话/用户上传/创意造物局Agent_MVP/创意造物局_Agent_MVP设计方案_v1.0.docx", buffer);
  console.log("文档生成成功！");
});
