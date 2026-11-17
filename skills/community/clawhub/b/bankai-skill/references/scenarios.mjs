// AUTO-GENERATED from src/ToolPage.jsx — 请勿手改，改源码后重跑 extract_scenarios.mjs
// 生成时间: 2026-07-08T13:46:56.486Z

export const FORMAT_INSTRUCTION = `

【公文格式规范——严格对齐GB/T 9704-2012《党政机关公文格式》及商业银行行文规范】
本产品严格对齐国标，覆盖银行95%以上高频公文场景。

一、页面与排版规范（强制遵循）
- 纸张规格：A4（210mm×297mm）
- 页边距：上3.7cm、下3.5cm、左2.8cm、右2.6cm
- 每页22行，每行28字，撑满版心
- 行距：固定值28磅（三号仿宋对应标准行距）
- 页码：底部居中，四号半角宋体

二、字体字号层级（强制遵循）
| 要素 | 字体字号 |
|------|---------|
| 公文标题 | 二号小标宋体，居中，回行词意完整 |
| 主送机关 | 三号仿宋_GB2312，顶格 |
| 正文内容 | 三号仿宋_GB2312，首行缩进2字符 |
| 一级标题 | 三号黑体，独占一行，末尾不加标点 |
| 二级标题 | 三号楷体_GB2312加粗，独占一行 |
| 三级及以下 | 三号仿宋_GB2312加粗，可接正文 |
| 附件说明 | 三号仿宋_GB2312，正文下空一行左空二字 |
| 发文机关署名/成文日期 | 三号仿宋_GB2312，右空四字 |
| 附注 | 三号仿宋_GB2312，加圆括号居左空二字 |

三、核心格式规则
1. 发文字号：机关代字 + 〔年份〕 + 顺序号，年份用六角括号，序号不编虚位、不加"第"字，例：×银办发〔2026〕12号
2. 成文日期：用阿拉伯数字全称，例：2026年6月25日，禁用汉字数字简写
3. 主送机关：下行文可统称"各支行、各部室"，上行文必须标注具体机关
4. 附件标注：附件名称后不加标点，多个附件用阿拉伯数字排序
5. 盖章要求：正式公文标注"（公章）"占位，骑年盖月

四、禁止事项（绝对不允许）
1. 禁止使用任何Markdown格式（#、**、*、\`、-等符号）
2. 禁止使用英文半角标点，必须使用中文全角标点（，。；：""（）！？、《》）
3. 禁止在报告中夹带请示事项；请示必须一文一事
4. 禁止多头主送上行文（上行文只主送一个上级机关）
5. 禁止部门对外正式行文（除办公室外）

五、公文结构（按以下顺序完整输出）

【版头部分】
- 发文机关标志：如"XX银行XX分行文件"（居中，庄重醒目）
- 发文字号：机关代字 + 〔年份〕 + 序号，如"XX银分〔2026〕25号"
- 签发人：仅上行文（请示、报告）需要，格式"签发人：XXX"（右对齐）

【主体部分】
- 标题：发文机关全称 + 事由 + 文种，标题一般不用标点
- 主送机关：顶格书写，后加全角冒号
- 正文：见下方"正文层级规范"
- 附件说明：正文下空一行，左空2字，附件名称后不加标点
- 发文机关署名：全称或规范化简称
- 成文日期：阿拉伯数字全称，如"2026年6月25日"，右空四字
- 印章：标注"（公章）"占位

【版记部分】
- 抄送机关：左空1字标注"抄送："
- 印发机关和日期：印发机关左空1字，日期右空1字

六、正文层级规范（必须严格遵守）
一级标题：一、二、三、 （序号后加顿号，独占一行，末尾无句号）
二级标题：（一）（二）（三）（括号后无标点，独占一行）
三级标题：1. 2. 3. （序号后加小圆点，可接正文）
四级标题：（1）（2）（3）（括号后无标点，可接正文）

七、数字与单位规范
- 金额：统一用"万元"，保留两位小数（如46,505.00万元）
- 百分比：保留1-2位小数（如"109.33%"）
- 日期：成文日期用全称阿拉伯数字
- 机构名称：首次用全称，后可用简称加注

八、语言风格要求
1. 使用银行公文正式书面语体，杜绝口语化、网络化表达
2. 善用银行专业术语（授信、拨备、迁徙率、资本充足率、净息差等）
3. 多用公文惯用语："依据""经研究决定""为贯彻落实""现就...通知如下"
4. 禁止主观口语："我们""我觉得"→ 改用"本行""经研究""建议"
5. 数据表述规范："同比增长X%""较上年末下降X个百分点"

九、字数要求（硬性约束）
1. 输出字数必须在用户要求值的±30%范围内，超出即不合格
2. 达到字数方法：充分展开论述，补充具体细节、数据、案例分析
3. 不要为了凑字数而重复啰嗦，以精炼准确为优先`;

export const SCENARIOS = [
  // ---- 监管回复 ----
  {
    id: 'situation-report',
    name: '情况说明',
    icon: '📋',
    category: 'regulatory',
    desc: '监管回复、情况说明、风险提示等',
    systemPrompt: '你是一名商业银行公文写作专家，精通银行监管要求和公文规范。你写的情况说明必须：1）符合银行公文格式标准；2）术语精准、用词严谨，使用银行专业术语；3）逻辑清晰、数据准确；4）语气客观、不使用模糊表述；5）语言正式规范，杜绝口语化表达，使用"本行""经核实""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '事由', placeholder: '如：关于XX支行2025年一季度不良贷款率上升的情况说明', required: true, type: 'text' },
      { key: 'facts', label: '关键数据和事实', placeholder: '如：不良率从2.1%上升至2.8%，主要受XX行业影响...', required: true, type: 'textarea' },
      { key: 'recipient', label: '报送对象', placeholder: '如：分行风险管理部/监管科室', required: false, type: 'text' },
      { key: 'measures', label: '已采取/拟采取的措施', placeholder: '如：已加强贷后检查频次，拟调整XX行业授信政策', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认800-1500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数800-1500字，请充分展开论述'
      return `请根据以下信息撰写一份正式的情况说明：

【事由】${data.title}
${data.recipient ? `【报送对象】${data.recipient}\n` : ''}【关键事实】${data.facts}
${data.measures ? `【应对措施】${data.measures}\n` : ''}
要求：
1. 标准公文格式（标题、主送、正文、落款）
2. 先概述事实，再分析原因，最后提出措施
3. 措辞严谨，不使用模糊表述
4. ${wc}`
    }
  },
  {
    id: 'investigation-report',
    name: '调查报告',
    icon: '🔍',
    category: 'regulatory',
    desc: '专项调查、事件调查、风险排查报告等',
    systemPrompt: '你是一名商业银行风险排查与调查专家，精通银行合规要求和调查报告规范。你写的调查报告必须：1）调查背景、过程、发现、结论、建议结构完整；2）事实描述客观中立，用数据说话；3）结论有依据，建议有操作性；4）措辞严谨规范，使用银行专业术语；5）语言正式规范，杜绝口语化，使用"经调查""依据""本行"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '调查事由', placeholder: '如：关于XX客户关联交易违规的调查报告', required: true, type: 'text' },
      { key: 'background', label: '调查背景', placeholder: '如：接监管通知，要求对XX业务进行专项排查', required: true, type: 'textarea' },
      { key: 'findings', label: '调查发现/问题', placeholder: '如：发现XX笔贷款存在担保链问题，涉及金额XX万', required: true, type: 'textarea' },
      { key: 'conclusion', label: '初步结论', placeholder: '如：存在授信审批不合规、贷后管理不到位等问题', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、3000（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份调查报告：

【调查事由】${data.title}
【调查背景】${data.background}
【调查发现】${data.findings}
${data.conclusion ? `【初步结论】${data.conclusion}\n` : ''}
要求：
1. 包含：调查背景、调查范围与过程、调查发现、问题分析、处理建议
2. 事实描述客观中立，用数据说话
3. 结论有依据，建议有操作性
4. ${wc}`
    }
  },

  {
    id: 'regulatory-report',
    name: '监管指标专项说明报告',
    icon: '🏛️',
    category: 'regulatory',
    desc: '监管指标专项说明、差异分析、整改报告等',
    systemPrompt: '你是一名商业银行监管报送专家，精通1104报表体系和监管指标计算。你写的监管指标专项说明报告必须：1）准确引用监管依据和文件号；2）指标数据精确无误；3）差异分析客观深入；4）整改措施具体可操作；5）语言正式规范，使用银行专业术语和监管用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '报告名称', placeholder: '如：关于2025年一季度不良贷款率超监管容忍度的专项说明', required: true, type: 'text' },
      { key: 'regulatoryBasis', label: '监管依据/文件号', placeholder: '如：《商业银行风险监管核心指标》银监发〔2025〕XX号', required: true, type: 'text' },
      { key: 'indicators', label: '涉及监管指标及数据', placeholder: '如：不良贷款率3.2%，拨备覆盖率145%，资本充足率11.5%', required: true, type: 'textarea' },
      { key: 'deviationAnalysis', label: '差异原因分析', placeholder: '如：受XX行业下行影响，不良贷款增加XX万元', required: true, type: 'textarea' },
      { key: 'improvement', label: '整改措施/改进计划', placeholder: '如：1.加大不良清收力度 2.严控新增不良 3.调整授信结构', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份监管指标专项说明报告：

【报告名称】${data.title}
【监管依据】${data.regulatoryBasis}
【涉及指标】${data.indicators}
【差异分析】${data.deviationAnalysis}
${data.improvement ? `【整改措施】${data.improvement}\n` : ''}要求：
1. 包含：监管依据、指标数据、差异分析、整改措施
2. 指标数据精确无误
3. 差异分析客观深入
4. 整改措施具体可操作
5. ${wc}`
    }
  },
  {
    id: 'inspection-reply',
    name: '监管检查整改回复',
    icon: '🏛️',
    category: 'regulatory',
    desc: '监管现场检查后的整改措施回复报告',
    systemPrompt: '你是一名商业银行监管对接专家，精通监管检查整改回复报告的撰写。你写的整改报告必须：1）对检查发现的问题逐一回应；2）整改措施具体可操作；3）整改时限明确；4）附整改佐证材料清单；5）语气诚恳严谨。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '报告标题', placeholder: '如：关于监管现场检查发现问题的整改回复报告', required: true, type: 'text' },
      { key: 'inspectionUnit', label: '检查单位', placeholder: '如：XX银保监局', required: true, type: 'text' },
      { key: 'inspectionDate', label: '检查日期', placeholder: '如：2026年3月', required: true, type: 'text' },
      { key: 'findings', label: '检查发现的问题', placeholder: '逐条列出检查发现的问题', required: true, type: 'textarea' },
      { key: 'correctiveActions', label: '整改措施及完成情况', placeholder: '逐条对应问题的整改措施、完成时限', required: true, type: 'textarea' },
      { key: 'results', label: '整改成效', placeholder: '如：已完善相关制度X项，问责X人次', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、3000（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份监管检查整改回复报告：

【报告标题】${data.title}
【检查单位】${data.inspectionUnit}
【检查日期】${data.inspectionDate}
【发现的问题】${data.findings}
【整改措施及完成情况】${data.correctiveActions}
${data.results ? `【整改成效】${data.results}\n` : ''}要求：
1. 对检查发现的问题逐一回应
2. 整改措施具体可操作
3. 整改时限明确
4. 语气诚恳严谨
5. ${wc}`
    }
  },
  {
    id: 'admin-defense',
    name: '陈述申辩函',
    icon: '⚖️',
    category: 'regulatory',
    desc: '收到监管行政处罚事先告知书后的陈述申辩',
    systemPrompt: '你是一名商业银行法律合规专家，精通行政处罚陈述申辩函的撰写。你写的申辩函必须：1）事实陈述客观准确；2）法律依据引用充分；3）申辩理由有说服力；4）语气不卑不亢；5）附相关证据材料。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '标题', placeholder: '如：关于XX行政处罚事先告知书的陈述申辩函', required: true, type: 'text' },
      { key: 'penaltyNoticeRef', label: '处罚告知书文号', placeholder: '如：银罚告字〔2026〕第XX号', required: true, type: 'text' },
      { key: 'allegedViolation', label: '拟处罚事项', placeholder: '描述监管拟处罚的违规事项', required: true, type: 'textarea' },
      { key: 'defenseFacts', label: '陈述事实', placeholder: '客观陈述相关事实情况', required: true, type: 'textarea' },
      { key: 'defenseReason', label: '申辩理由', placeholder: '阐述申辩的依据和理由', required: true, type: 'textarea' },
      { key: 'evidence', label: '相关证据', placeholder: '如：1.XX合同复印件 2.XX审批单', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1000-2000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1000-2000字，请充分展开论述'
      return `请根据以下信息撰写一份陈述申辩函：

【标题】${data.title}
【处罚告知书文号】${data.penaltyNoticeRef}
【拟处罚事项】${data.allegedViolation}
【陈述事实】${data.defenseFacts}
【申辩理由】${data.defenseReason}
${data.evidence ? `【相关证据】${data.evidence}\n` : ''}要求：
1. 事实陈述客观准确
2. 法律依据引用充分
3. 申辩理由有说服力
4. 语气不卑不亢
5. ${wc}`
    }
  },
  {
    id: 'major-incident',
    name: '重大事项即时上报',
    icon: '🚨',
    category: 'regulatory',
    desc: '重大风险事件、安全事故、突发事件的即时上报',
    systemPrompt: '你是一名商业银行风险管理专家，精通重大事项即时报告的撰写。你写的即时报告必须：1）事件描述准确客观；2）影响评估全面；3）已采取的措施和后续计划明确；4）报告时效性强；5）语言简洁有力。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '报告标题', placeholder: '如：关于XX支行发生客户信息泄露事件的即时报告', required: true, type: 'text' },
      { key: 'incidentTime', label: '事发时间', placeholder: '如：2026年6月25日上午10时', required: true, type: 'text' },
      { key: 'incidentLocation', label: '事发地点/单位', placeholder: '如：XX支行营业大厅', required: true, type: 'text' },
      { key: 'incidentDesc', label: '事件经过', placeholder: '详细描述事件发生经过', required: true, type: 'textarea' },
      { key: 'impact', label: '影响评估', placeholder: '如：涉及客户XX户，金额XX万元，声誉风险等', required: true, type: 'textarea' },
      { key: 'measures', label: '已采取的措施', placeholder: '如：1.立即启动应急预案 2.成立应急处置小组', required: true, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1000、2000（留空则默认800-1500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数800-1500字，请充分展开论述'
      return `请根据以下信息撰写一份重大事项即时上报报告：

【报告标题】${data.title}
【事发时间】${data.incidentTime}
【事发地点】${data.incidentLocation}
【事件经过】${data.incidentDesc}
【影响评估】${data.impact}
【已采取措施】${data.measures}
要求：
1. 事件描述准确客观
2. 影响评估全面
3. 已采取的措施明确
4. 报告时效性强
5. ${wc}`
    }
  },
  {
    id: 'bank-confirmation',
    name: '银行询证函回复',
    icon: '📋',
    category: 'regulatory',
    desc: '审计机构发来的银行询证函回复',
    systemPrompt: '你是一名商业银行运营管理专家，精通银行询证函回复的撰写。你写的询证函回复必须：1）数字准确无误；2）信息一一对应；3）格式规范标准；4）加盖印章说明到位；5）语言正式规范。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '标题', placeholder: '如：银行询证函回函', required: true, type: 'text' },
      { key: 'auditFirm', label: '会计师事务所名称', placeholder: '如：XX会计师事务所（特殊普通合伙）', required: true, type: 'text' },
      { key: 'clientName', label: '被审计单位', placeholder: '如：XX股份有限公司', required: true, type: 'text' },
      { key: 'accountInfo', label: '账户信息', placeholder: '逐项列出账号、账户名称、币种、账户类型', required: true, type: 'textarea' },
      { key: 'balance', label: '账户余额', placeholder: '逐项列出各账户截至函证日的余额', required: true, type: 'textarea' },
      { key: 'loans', label: '贷款信息', placeholder: '如：贷款合同号、金额、起止日期、利率、余额', required: false, type: 'textarea' },
      { key: 'guaranteeItems', label: '担保信息', placeholder: '如：保函编号、金额、有效期', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：500、1000（留空则默认400-800字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数400-800字，请充分展开论述'
      return `请根据以下信息撰写一份银行询证函回复：

【标题】${data.title}
【会计师事务所】${data.auditFirm}
【被审计单位】${data.clientName}
【账户信息】${data.accountInfo}
【账户余额】${data.balance}
${data.loans ? `【贷款信息】${data.loans}\n` : ''}${data.guaranteeItems ? `【担保信息】${data.guaranteeItems}\n` : ''}要求：
1. 数字准确无误
2. 信息一一对应
3. 格式规范标准
4. ${wc}`
    }
  },

  // ---- 分析研判 ----
  {
    id: 'post-lending-check',
    name: '贷款贷后检查报告',
    icon: '🔍',
    category: 'analysis',
    desc: '贷后定期检查、专项检查、风险排查报告等',
    systemPrompt: '你是一名商业银行信贷管理专家，精通贷款贷后检查的规范要求和报告撰写。你写的贷后检查报告必须：1）结构完整，涵盖客户概况、贷款基本情况、检查内容、检查发现、风险评价、处置建议；2）检查内容全面覆盖经营状况、财务状况、担保状况、还本付息情况、贷款用途合规性；3）风险评价客观准确，使用标准风险等级描述；4）处置建议具体可执行，区分一般关注、重点关注、重大风险等级；5）语言正式规范，杜绝口语化，使用银行专业术语（如：贷后检查、五级分类、担保覆盖率、第一还款来源、第二还款来源等），使用"本行""经检查""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'customerName', label: '客户名称', placeholder: '如：XX房地产开发有限公司', required: true, type: 'text' },
      { key: 'loanType', label: '贷款品种', placeholder: '如：流动资金贷款/固定资产贷款/个人经营性贷款', required: true, type: 'text' },
      { key: 'loanAmount', label: '贷款金额及余额', placeholder: '如：授信5000万元，已用信3000万元，余额3000万元', required: true, type: 'text' },
      { key: 'loanDate', label: '贷款发放日期/期限', placeholder: '如：2024年6月发放，期限2年，到期日2026年6月', required: true, type: 'text' },
      { key: 'checkPeriod', label: '检查期间', placeholder: '如：2025年一季度常规贷后检查', required: true, type: 'text' },
      { key: 'businessStatus', label: '经营/项目建设情况', placeholder: '如：企业经营正常，年营收约1.2亿，XX项目已完工80%', required: true, type: 'textarea' },
      { key: 'financialStatus', label: '财务状况', placeholder: '如：资产负债率65%，流动比率1.2，经营性现金流稳定', required: false, type: 'textarea' },
      { key: 'guaranteeStatus', label: '担保状况', placeholder: '如：以XX房产抵押，评估值8000万，抵押率62.5%，保证人XX公司', required: false, type: 'textarea' },
      { key: 'repaymentStatus', label: '还本付息情况', placeholder: '如：按期付息无逾期，已归还本金500万元', required: true, type: 'text' },
      { key: 'riskSignals', label: '风险信号/检查发现', placeholder: '如：发现XX行业下行导致订单减少，担保人涉诉', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、3000（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份贷款贷后检查报告：

【客户名称】${data.customerName}
【贷款品种】${data.loanType}
【贷款金额及余额】${data.loanAmount}
【贷款发放日期/期限】${data.loanDate}
【检查期间】${data.checkPeriod}
【经营/项目建设情况】${data.businessStatus}
${data.financialStatus ? `【财务状况】${data.financialStatus}\n` : ''}${data.guaranteeStatus ? `【担保状况】${data.guaranteeStatus}\n` : ''}【还本付息情况】${data.repaymentStatus}
${data.riskSignals ? `【风险信号/检查发现】${data.riskSignals}\n` : ''}
要求：
1. 包含：检查依据、客户及贷款基本情况、检查内容（经营状况、财务状况、担保状况、还本付息、贷款用途）、检查发现、风险评价、处置建议
2. 检查内容全面，覆盖第一还款来源和第二还款来源分析
3. 风险评价客观准确，按五级分类标准评估
4. 处置建议具体可执行，按风险等级分类提出
5. ${wc}`
    }
  },
  {
    id: 'risk-report',
    name: '风险分析报告',
    icon: '📊',
    category: 'analysis',
    desc: '信贷风险分析、行业风险研判等',
    systemPrompt: '你是一名商业银行风险分析专家，精通银行风险管理体系和监管要求。你写的风险分析报告必须：1）框架完整，涵盖概述、数据分析、风险识别、评估、建议；2）风险等级判断使用标准术语（低/中/高/较高）；3）数据引用准确，趋势判断有依据；4）建议措施具体可执行；5）语言正式规范，使用银行专业术语，杜绝口语化，使用"本行""经分析""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'reportType', label: '报告类型', placeholder: '如：信贷风险分析报告/行业风险分析报告', required: true, type: 'text' },
      { key: 'target', label: '分析对象', placeholder: '如：XX行业/XX支行信贷资产', required: true, type: 'text' },
      { key: 'period', label: '分析期间', placeholder: '如：2025年一季度', required: true, type: 'text' },
      { key: 'indicators', label: '关键数据指标', placeholder: '如：不良率2.8%，拨备覆盖率150%，关注类贷款占比...', required: true, type: 'textarea' },
      { key: 'risks', label: '已知风险点', placeholder: '如：XX行业集中度偏高，担保链风险暴露', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、3000（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份风险分析报告：

【报告类型】${data.reportType}
【分析对象】${data.target}
【分析期间】${data.period}
【关键数据指标】${data.indicators}
${data.risks ? `【已知风险点】${data.risks}\n` : ''}
要求：
1. 包含：概述、数据分析、风险识别、风险评估、建议措施
2. 风险等级判断使用标准术语
3. 建议措施具体可执行
4. ${wc}`
    }
  },

  {
    id: 'pre-lending-report',
    name: '贷前调查报告',
    icon: '🔍',
    category: 'analysis',
    desc: '对公/零售贷款的客户资质尽职调查报告',
    systemPrompt: '你是一名商业银行信贷调查专家，精通贷前尽职调查规范和报告撰写。你写的贷前调查报告必须：1）结构完整，涵盖客户基本情况、经营分析、财务分析、担保分析、风险点识别、授信建议；2）客户信息真实可靠，分析客观；3）风险识别全面准确；4）授信建议理由充分；5）语言正式规范，使用银行专业术语，杜绝口语化，使用"本行""经调查""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'customerName', label: '客户名称', placeholder: '如：XX科技有限公司', required: true, type: 'text' },
      { key: 'borrowerInfo', label: '客户基本信息', placeholder: '如：成立时间、注册资本、主营业务、行业地位等', required: true, type: 'textarea' },
      { key: 'businessAnalysis', label: '经营情况分析', placeholder: '如：近三年营收、毛利率、市场份额、上下游客户等', required: true, type: 'textarea' },
      { key: 'financialAnalysis', label: '财务情况分析', placeholder: '如：资产负债率、流动比率、速动比率、现金流等', required: true, type: 'textarea' },
      { key: 'guaranteeAnalysis', label: '担保措施分析', placeholder: '如：抵质押物类型、评估值、变现能力、保证人资信等', required: false, type: 'textarea' },
      { key: 'riskPoints', label: '主要风险点', placeholder: '如：行业周期性风险、关联交易风险、担保不足等', required: false, type: 'textarea' },
      { key: 'creditSuggestion', label: '授信建议', placeholder: '如：建议授信XX万元，期限X年，担保方式XX', required: true, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、3000（留空则默认2000-3000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数2000-3000字，请充分展开论述'
      return `请根据以下信息撰写一份贷前调查报告：

【客户名称】${data.customerName}
【客户基本信息】${data.borrowerInfo}
【经营情况分析】${data.businessAnalysis}
【财务情况分析】${data.financialAnalysis}
${data.guaranteeAnalysis ? `【担保措施分析】${data.guaranteeAnalysis}\n` : ''}${data.riskPoints ? `【主要风险点】${data.riskPoints}\n` : ''}【授信建议】${data.creditSuggestion}
要求：
1. 包含：客户概况、经营分析、财务分析、担保分析、风险识别、授信建议
2. 分析客观全面，数据翔实
3. 风险识别准确，授信建议理由充分
4. ${wc}`
    }
  },
  {
    id: 'credit-approval',
    name: '授信审批意见书',
    icon: '✅',
    category: 'analysis',
    desc: '贷审会/审批岗的最终审批结论',
    systemPrompt: '你是一名商业银行授信审批专家，精通信贷审批流程和审批意见撰写。你写的授信审批意见书必须：1）结构完整，涵盖申请人信息、授信方案概述、风险分析、审批意见、审批条件；2）审批意见明确清晰，使用"同意/有条件同意/不同意"等标准用语；3）审批条件具体可落实；4）风险控制措施到位；5）语言正式规范，使用银行专业术语，杜绝口语化，使用"本行""经审查""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '审批事项', placeholder: '如：关于XX公司XX万元流动资金贷款的审批意见', required: true, type: 'text' },
      { key: 'applicantInfo', label: '申请人/企业概况', placeholder: '如：XX公司，主营XX，注册资本XX万元', required: true, type: 'textarea' },
      { key: 'creditOverview', label: '授信方案概述', placeholder: '如：申请流动资金贷款XX万元，期限X年，由XX提供担保', required: true, type: 'textarea' },
      { key: 'riskAnalysis', label: '风险审查分析', placeholder: '如：第一还款来源充足性、第二还款来源有效性、行业风险等', required: true, type: 'textarea' },
      { key: 'approvalOpinion', label: '审批意见', placeholder: '如：同意授信XX万元，期限X年，利率XX%', required: true, type: 'textarea' },
      { key: 'conditions', label: '审批条件/限制性条款', placeholder: '如：1.落实抵押登记 2.资金专户管理 3.按季监控销售回款', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1000、2000（留空则默认1000-2000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1000-2000字，请充分展开论述'
      return `请根据以下信息撰写一份授信审批意见书：

【审批事项】${data.title}
【申请人概况】${data.applicantInfo}
【授信方案概述】${data.creditOverview}
【风险审查分析】${data.riskAnalysis}
【审批意见】${data.approvalOpinion}
${data.conditions ? `【审批条件】${data.conditions}\n` : ''}
要求：
1. 包含：申请人概况、授信方案、风险分析、审批意见、审批条件
2. 审批意见明确清晰，使用标准用语
3. 审批条件具体可落实
4. 风险控制措施到位
5. ${wc}`
    }
  },
  {
    id: 'risk-warning',
    name: '风险预警通知书',
    icon: '⚠️',
    category: 'analysis',
    desc: '客户风险触发后的提示与处置要求',
    systemPrompt: '你是一名商业银行风险监控专家，精通风险预警和风险提示工作。你写的风险预警通知书必须：1）风险信号描述准确清晰；2）风险等级判断客观合理；3）处置要求具体可操作；4）时限要求明确；5）语言正式规范，使用银行专业术语，杜绝口语化，使用"本行""经监测""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'customerName', label: '客户名称', placeholder: '如：XX房地产开发有限公司', required: true, type: 'text' },
      { key: 'riskSignals', label: '风险信号/预警触发条件', placeholder: '如：贷款逾期30天、经营性现金流为负、涉及重大诉讼', required: true, type: 'textarea' },
      { key: 'riskLevel', label: '风险等级', placeholder: '如：关注/预警/重点关注/重大风险', required: true, type: 'text' },
      { key: 'requiredActions', label: '处置要求/需采取的措施', placeholder: '如：1.立即开展现场检查 2.核实企业经营状况 3.制定风险化解方案', required: true, type: 'textarea' },
      { key: 'deadline', label: '完成时限', placeholder: '如：收到本通知后5个工作日内反馈', required: true, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：500、1000（留空则默认500-1000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数500-1000字，请充分展开论述'
      return `请根据以下信息撰写一份风险预警通知书：

【客户名称】${data.customerName}
【风险信号】${data.riskSignals}
【风险等级】${data.riskLevel}
【处置要求】${data.requiredActions}
【完成时限】${data.deadline}
要求：
1. 风险信号描述准确清晰
2. 风险等级判断客观合理
3. 处置要求具体可操作
4. 时限要求明确
5. ${wc}`
    }
  },
  {
    id: 'npl-disposal',
    name: '不良资产处置报告',
    icon: '📉',
    category: 'analysis',
    desc: '不良贷款核销、重组、清收处置方案',
    systemPrompt: '你是一名商业银行不良资产处置专家，精通不良资产清收、重组、核销、转让等处置方式。你写的不良资产处置报告必须：1）不良资产基本情况清晰明了；2）处置方案多种对比，优中选优；3）损失预估准确合理；4）实施步骤具体可操作；5）语言正式规范，使用银行专业术语，杜绝口语化，使用"本行""经分析""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'customerName', label: '客户名称', placeholder: '如：XX贸易有限公司', required: true, type: 'text' },
      { key: 'nplOverview', label: '不良贷款基本情况', placeholder: '如：贷款余额XX万元，五级分类为次级/可疑/损失，逾期天数XX天', required: true, type: 'textarea' },
      { key: 'disposalPlans', label: '处置方案/对比分析', placeholder: '如：方案一：债务重组（展期+降息）；方案二：诉讼清收；方案三：核销', required: true, type: 'textarea' },
      { key: 'estimatedLoss', label: '损失预估', placeholder: '如：预计损失率XX%-XX%，预计回收金额XX万元', required: true, type: 'textarea' },
      { key: 'implementation', label: '实施步骤/时间安排', placeholder: '如：1.XX日前完成法律尽调 2.XX日报审 3.XX日前完成处置', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份不良资产处置报告：

【客户名称】${data.customerName}
【不良贷款基本情况】${data.nplOverview}
【处置方案分析】${data.disposalPlans}
【损失预估】${data.estimatedLoss}
${data.implementation ? `【实施步骤】${data.implementation}\n` : ''}
要求：
1. 包含：基本情况、处置方案对比分析、损失预估、实施步骤
2. 处置方案多种对比，优中选优
3. 损失预估准确合理
4. 实施步骤具体可操作
5. ${wc}`
    }
  },
  {
    id: 'compliance-review',
    name: '合规审查意见书',
    icon: '🔒',
    category: 'analysis',
    desc: '业务、产品、合同的合规性审核',
    systemPrompt: '你是一名商业银行合规管理专家，精通银行合规审查要求和监管规定。你写的合规审查意见书必须：1）审查依据引用准确完整；2）风险点识别全面深入；3）审查结论明确，使用"合规/基本合规/不合规"等标准用语；4）修改建议具体可落实；5）语言正式规范，使用银行专业术语和监管用语，杜绝口语化，使用"本行""经审查""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'reviewItem', label: '审查事项', placeholder: '如：XX理财产品销售管理办法合规审查', required: true, type: 'text' },
      { key: 'regulatoryBasis', label: '审查依据/法规', placeholder: '如：《商业银行理财业务监督管理办法》银保监会令XX号', required: true, type: 'text' },
      { key: 'riskPoints', label: '合规风险点/问题', placeholder: '如：1.销售适当性管理不到位 2.信息披露不充分 3.风险揭示不完整', required: true, type: 'textarea' },
      { key: 'reviewConclusion', label: '审查结论', placeholder: '如：基本合规/合规/不合规', required: true, type: 'text' },
      { key: 'modificationSuggestions', label: '修改建议', placeholder: '如：1.补充客户风险评估流程 2.完善信息披露条款', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1000、2000（留空则默认1000-2000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1000-2000字，请充分展开论述'
      return `请根据以下信息撰写一份合规审查意见书：

【审查事项】${data.reviewItem}
【审查依据】${data.regulatoryBasis}
【合规风险点】${data.riskPoints}
【审查结论】${data.reviewConclusion}
${data.modificationSuggestions ? `【修改建议】${data.modificationSuggestions}\n` : ''}
要求：
1. 包含：审查事项、审查依据、风险点分析、审查结论、修改建议
2. 审查依据引用准确完整
3. 风险点识别全面深入
4. 审查结论明确，修改建议具体可落实
5. ${wc}`
    }
  },
  {
    id: 'financial-analysis',
    name: '财务分析报告',
    icon: '📊',
    category: 'analysis',
    desc: '月度/季度/年度经营效益分析',
    systemPrompt: '你是一名商业银行财务分析专家，精通银行财务报表分析和经营效益评估。你写的财务分析报告必须：1）结构完整，涵盖收入分析、支出分析、利润分析、资产负债分析、指标评价；2）数据准确，趋势分析有依据；3）问题诊断到位，改进建议可行；4）语言正式规范，使用银行专业术语，杜绝口语化，使用"本行""经分析""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'reportType', label: '报告类型', placeholder: '如：月度财务分析报告/季度财务分析报告/年度财务分析报告', required: true, type: 'text' },
      { key: 'department', label: '分析对象/部门', placeholder: '如：XX分行/XX支行/全行', required: true, type: 'text' },
      { key: 'indicators', label: '主要经营指标', placeholder: '如：营业收入XX万元，净利润XX万元，ROE为XX%', required: true, type: 'textarea' },
      { key: 'structureAnalysis', label: '结构分析', placeholder: '如：利息净收入占比XX%，中间业务收入占比XX%，费用结构...', required: true, type: 'textarea' },
      { key: 'changeAnalysis', label: '变动分析/趋势分析', placeholder: '如：营收同比增长XX%，环比增长XX%，主要驱动因素...', required: false, type: 'textarea' },
      { key: 'suggestions', label: '改进建议', placeholder: '如：1.优化资产负债结构 2.压降高成本存款 3.拓展中间业务', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、3000（留空则默认2000-3000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数2000-3000字，请充分展开论述'
      return `请根据以下信息撰写一份财务分析报告：

【报告类型】${data.reportType}
【分析对象】${data.department}
【主要经营指标】${data.indicators}
【结构分析】${data.structureAnalysis}
${data.changeAnalysis ? `【变动趋势分析】${data.changeAnalysis}\n` : ''}${data.suggestions ? `【改进建议】${data.suggestions}\n` : ''}
要求：
1. 包含：收入分析、支出分析、利润分析、资产负债分析、指标评价
2. 数据准确，趋势分析有依据
3. 问题诊断到位，改进建议可行
4. ${wc}`
    }
  },
  {
    id: 'loan-classification',
    name: '贷款五级分类认定',
    icon: '🔍',
    category: 'analysis',
    desc: '贷款风险五级分类的认定依据及结论',
    systemPrompt: '你是一名商业银行信贷管理专家，精通贷款五级分类认定报告的撰写。你写的分类认定报告必须：1）认定依据引用准确；2）财务和非财务因素分析全面；3）风险分类判断合理；4）建议明确。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'customerName', label: '客户名称', placeholder: '如：XX制造有限公司', required: true, type: 'text' },
      { key: 'loanAmount', label: '贷款金额', placeholder: '如：人民币2000万元', required: true, type: 'text' },
      { key: 'currentClassification', label: '现有分类', placeholder: '如：关注类/次级类', required: true, type: 'text' },
      { key: 'classificationBasis', label: '认定依据', placeholder: '引用五级分类相关监管规定和行内制度依据', required: true, type: 'textarea' },
      { key: 'financialAnalysis', label: '财务分析', placeholder: '如：资产负债率、流动比率、经营性现金流等财务指标分析', required: true, type: 'textarea' },
      { key: 'riskFactors', label: '风险因素分析', placeholder: '如：行业风险、经营风险、担保风险、法律风险等', required: true, type: 'textarea' },
      { key: 'recommendedClassification', label: '建议分类', placeholder: '如：次级类/可疑类/损失类', required: true, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1200-2000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1200-2000字，请充分展开论述'
      return `请根据以下信息撰写一份贷款五级分类认定报告：

【客户名称】${data.customerName}
【贷款金额】${data.loanAmount}
【现有分类】${data.currentClassification}
【认定依据】${data.classificationBasis}
【财务分析】${data.financialAnalysis}
【风险因素】${data.riskFactors}
【建议分类】${data.recommendedClassification}
要求：
1. 认定依据引用准确
2. 财务和非财务因素分析全面
3. 风险分类判断合理
4. ${wc}`
    }
  },
  {
    id: 'overdue-notice',
    name: '逾期催收通知书',
    icon: '⚠️',
    category: 'analysis',
    desc: '贷款逾期后向客户发送的催收通知',
    systemPrompt: '你是一名商业银行信贷管理专家，精通逾期贷款催收通知书的撰写。你写的催收通知必须：1）逾期信息准确；2）催收要求明确；3）违约后果告知到位；4）语言正式有严肃性。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'customerName', label: '客户名称', placeholder: '如：XX贸易有限公司', required: true, type: 'text' },
      { key: 'contractNo', label: '合同编号', placeholder: '如：2025年XX字第001号', required: true, type: 'text' },
      { key: 'loanAmount', label: '贷款金额', placeholder: '如：人民币500万元', required: true, type: 'text' },
      { key: 'overdueAmount', label: '逾期金额', placeholder: '如：人民币500万元及利息', required: true, type: 'text' },
      { key: 'overdueDays', label: '逾期天数', placeholder: '如：60天', required: true, type: 'text' },
      { key: 'repaymentDeadline', label: '还款期限', placeholder: '如：请于收到本通知后7日内偿还', required: true, type: 'text' },
      { key: 'legalConsequences', label: '逾期后果告知', placeholder: '如：征信记录影响、加收罚息、法律诉讼等', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：500、1000（留空则默认400-800字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数400-800字，请充分展开论述'
      return `请根据以下信息撰写一份贷款逾期催收通知书：

【客户名称】${data.customerName}
【合同编号】${data.contractNo}
【贷款金额】${data.loanAmount}
【逾期金额】${data.overdueAmount}
【逾期天数】${data.overdueDays}
【还款期限】${data.repaymentDeadline}
${data.legalConsequences ? `【逾期后果】${data.legalConsequences}\n` : ''}要求：
1. 逾期信息准确
2. 催收要求明确
3. 违约后果告知到位
4. 语言正式有严肃性
5. ${wc}`
    }
  },
  {
    id: 'product-prospectus',
    name: '产品说明书',
    icon: '📄',
    category: 'analysis',
    desc: '理财、贷款、结算产品的官方说明',
    systemPrompt: '你是一名商业银行产品管理专家，精通金融产品说明书的撰写。你写的产品说明书必须：1）产品信息完整准确；2）风险揭示充分；3）费率条款清晰；4）语言通俗易懂兼顾专业性。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'productName', label: '产品名称', placeholder: '如：XX银行"稳盈"系列理财产品', required: true, type: 'text' },
      { key: 'productType', label: '产品类型', placeholder: '如：理财产品/贷款产品/结算产品', required: true, type: 'text' },
      { key: 'targetCustomers', label: '适用客群', placeholder: '如：个人客户/小微企业主/机构客户', required: true, type: 'textarea' },
      { key: 'rateAndFees', label: '费率与收益', placeholder: '如：预期年化收益率X%，管理费率X%', required: true, type: 'textarea' },
      { key: 'riskDisclosure', label: '风险揭示', placeholder: '充分揭示产品相关风险', required: true, type: 'textarea' },
      { key: 'applicationProcess', label: '办理流程', placeholder: '如：1.客户申请 2.资料审核 3.签约 4.放款', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1000-2000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1000-2000字，请充分展开论述'
      return `请根据以下信息撰写一份产品说明书：

【产品名称】${data.productName}
【产品类型】${data.productType}
【适用客群】${data.targetCustomers}
【费率与收益】${data.rateAndFees}
【风险揭示】${data.riskDisclosure}
${data.applicationProcess ? `【办理流程】${data.applicationProcess}\n` : ''}要求：
1. 产品信息完整准确
2. 风险揭示充分
3. 费率条款清晰
4. 语言通俗易懂兼顾专业性
5. ${wc}`
    }
  },

  // ---- 规章制度 ----
  {
    id: 'regulation',
    name: '管理办法',
    icon: '📜',
    category: 'regulation',
    desc: '业务管理办法、实施细则、操作规程等',
    systemPrompt: '你是一名商业银行制度文件起草专家，精通银行内部规章制度体系。你写的管理办法必须：1）结构完整：总则（目的、依据、适用范围）、组织职责、管理内容、操作流程、监督检查、附则；2）条款表述清晰、无歧义；3）职责分工明确，流程闭环；4）与监管要求一致；5）使用"应当""不得""严禁"等规范用语；6）语言正式规范，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '制度名称', placeholder: '如：XX银行业务运营风险管理系统管理办法', required: true, type: 'text' },
      { key: 'purpose', label: '制定目的', placeholder: '如：规范XX业务操作流程，防范操作风险', required: true, type: 'textarea' },
      { key: 'scope', label: '适用范围', placeholder: '如：全行各分支行、各部门XX业务', required: true, type: 'text' },
      { key: 'keyPoints', label: '核心管理内容/要点', placeholder: '如：职责分工、审批流程、风险控制措施、报告机制、罚则', required: true, type: 'textarea' },
      { key: 'isTrial', label: '是否试行', placeholder: '如：是/否（留空默认否）', required: false, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：3000、5000（留空则默认3000-5000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数3000-5000字，请充分展开论述'
      const trial = data.isTrial === '是' ? '标题标注"（试行）"' : ''
      return `请根据以下信息起草一份管理办法：

【制度名称】${data.title}
【制定目的】${data.purpose}
【适用范围】${data.scope}
【核心管理内容】${data.keyPoints}
${trial}
要求：
1. 包含：总则（目的、依据、适用范围）、组织职责、管理规则、操作流程、监督检查、罚则、附则
2. 条款表述清晰无歧义，使用"应当""不得""严禁"等规范用语
3. 职责分工明确，流程闭环
4. ${wc}`
    }
  },
  {
    id: 'implementation-plan',
    name: '实施方案',
    icon: '📑',
    category: 'regulation',
    desc: '工作方案、实施方案、推进计划等',
    systemPrompt: '你是一名商业银行项目管理专家，精通银行工作方案的策划与撰写。你写的实施方案必须：1）目标明确、可衡量；2）步骤清晰、时间节点具体；3）责任到人/部门；4）配套措施和保障机制到位；5）风险预判和应急预案；6）语言正式规范，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '方案名称', placeholder: '如：XX支行2025年不良贷款处置实施方案', required: true, type: 'text' },
      { key: 'goal', label: '工作目标', placeholder: '如：年内处置不良贷款XX万元，不良率下降至X%', required: true, type: 'textarea' },
      { key: 'period', label: '实施时间', placeholder: '如：2025年3月-12月', required: true, type: 'text' },
      { key: 'scope', label: '实施范围', placeholder: '如：全行各支行信贷条线', required: true, type: 'text' },
      { key: 'keyActions', label: '主要举措', placeholder: '如：1.分类施策 2.批量转让 3.诉讼清收 4.核销', required: true, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、3000（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份实施方案：

【方案名称】${data.title}
【工作目标】${data.goal}
【实施时间】${data.period}
【实施范围】${data.scope}
【主要举措】${data.keyActions}
要求：
1. 包含：目标、组织领导、实施步骤（含时间节点）、责任分工、保障措施、考核机制
2. 目标明确可衡量，步骤清晰有时限
3. 责任到部门/岗位
4. ${wc}`
    }
  },
  {
    id: 'emergency-plan',
    name: '突发事件应急预案',
    icon: '🆘',
    category: 'regulation',
    desc: '系统故障、安全事故、自然灾害等应急预案',
    systemPrompt: '你是一名商业银行运营管理专家，精通应急预案的撰写。你写的应急预案必须：1）事件分级清晰；2）应急组织架构完整；3）处置流程闭环；4）恢复措施具体；5）职责分工明确。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '预案名称', placeholder: '如：XX银行信息系统突发事件应急预案', required: true, type: 'text' },
      { key: 'riskTypes', label: '适用范围及风险类型', placeholder: '如：系统故障、网络攻击、数据丢失等', required: true, type: 'textarea' },
      { key: 'orgStructure', label: '应急组织架构', placeholder: '如：领导小组、工作小组、技术保障组等', required: true, type: 'textarea' },
      { key: 'responseProcedures', label: '应急处置流程', placeholder: '详细描述预警、报告、响应、处置各环节流程', required: true, type: 'textarea' },
      { key: 'postRecovery', label: '后期恢复措施', placeholder: '如：数据恢复、业务验证、总结评估等', required: true, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：3000、5000（留空则默认3000-5000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数3000-5000字，请充分展开论述'
      return `请根据以下信息起草一份突发事件应急预案：

【预案名称】${data.title}
【适用范围】${data.riskTypes}
【应急组织架构】${data.orgStructure}
【应急处置流程】${data.responseProcedures}
【后期恢复】${data.postRecovery}
要求：
1. 包含：编制目的和依据、适用范围、事件分级、应急组织、预警与报告、应急处置流程、后期处置
2. 事件分级清晰
3. 应急组织架构完整
4. 处置流程闭环
5. 职责分工明确
6. ${wc}`
    }
  },
  {
    id: 'job-description',
    name: '岗位说明书',
    icon: '📋',
    category: 'regulation',
    desc: '各岗位职责说明书、任职资格要求',
    systemPrompt: '你是一名商业银行人力资源管理专家，精通岗位说明书的撰写。你写的岗位说明书必须：1）职责描述清晰无歧义；2）任职资格合理；3）核心指标可量化；4）符合银行岗位管理体系。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'positionName', label: '岗位名称', placeholder: '如：信贷审查岗/风险管理岗/客户经理岗', required: true, type: 'text' },
      { key: 'department', label: '所属部门', placeholder: '如：风险管理部', required: true, type: 'text' },
      { key: 'superior', label: '直接上级', placeholder: '如：风险管理部总经理', required: false, type: 'text' },
      { key: 'subordinates', label: '下属人数', placeholder: '如：0人/3人', required: false, type: 'text' },
      { key: 'duties', label: '岗位职责', placeholder: '逐条列明岗位主要职责，如：1.负责XX 2.负责XX', required: true, type: 'textarea' },
      { key: 'qualifications', label: '任职资格', placeholder: '如：学历要求、专业要求、工作经验、资格证书等', required: true, type: 'textarea' },
      { key: 'performanceIndicators', label: '核心考核指标', placeholder: '如：KPI指标及权重', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1000、2000（留空则默认800-1500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数800-1500字，请充分展开论述'
      return `请根据以下信息撰写一份岗位说明书：

【岗位名称】${data.positionName}
【所属部门】${data.department}
${data.superior ? `【直接上级】${data.superior}\n` : ''}${data.subordinates ? `【下属人数】${data.subordinates}\n` : ''}【岗位职责】${data.duties}
【任职资格】${data.qualifications}
${data.performanceIndicators ? `【核心考核指标】${data.performanceIndicators}\n` : ''}要求：
1. 职责描述清晰无歧义
2. 任职资格合理
3. 核心指标可量化
4. ${wc}`
    }
  },
  {
    id: 'cooperation-agreement',
    name: '合作框架协议',
    icon: '🤝',
    category: 'regulation',
    desc: '银企合作框架协议、同业合作协议等',
    systemPrompt: '你是一名商业银行法律合规专家，精通合作协议的撰写。你写的合作协议必须：1）权责划分清晰；2）风险防控措施到位；3）条款完整无歧义；4）格式符合合同规范。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '协议名称', placeholder: '如：XX银行与XX公司战略合作框架协议', required: true, type: 'text' },
      { key: 'partyA', label: '甲方', placeholder: '如：XX银行XX分行', required: true, type: 'text' },
      { key: 'partyB', label: '乙方', placeholder: '如：XX科技有限公司', required: true, type: 'text' },
      { key: 'cooperationScope', label: '合作内容与范围', placeholder: '详细描述双方合作的具体领域和内容', required: true, type: 'textarea' },
      { key: 'rightsObligations', label: '双方权利义务', placeholder: '逐条列明甲乙双方的权利和义务', required: true, type: 'textarea' },
      { key: 'confidentiality', label: '保密条款', placeholder: '如：保密信息范围、保密期限、违约责任', required: false, type: 'textarea' },
      { key: 'disputeResolution', label: '争议解决方式', placeholder: '如：协商解决/仲裁/诉讼', required: false, type: 'textarea' },
      { key: 'effectivePeriod', label: '协议有效期', placeholder: '如：自签署之日起两年', required: true, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、4000（留空则默认2000-3500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数2000-3500字，请充分展开论述'
      return `请根据以下信息撰写一份合作框架协议：

【协议名称】${data.title}
【甲方】${data.partyA}
【乙方】${data.partyB}
【合作内容】${data.cooperationScope}
【权利义务】${data.rightsObligations}
${data.confidentiality ? `【保密条款】${data.confidentiality}\n` : ''}${data.disputeResolution ? `【争议解决】${data.disputeResolution}\n` : ''}【协议有效期】${data.effectivePeriod}
要求：
1. 包含：合作双方、合作宗旨与原则、合作内容、权利义务、保密条款、争议解决、有效期
2. 权责划分清晰
3. 风险防控措施到位
4. 条款完整无歧义
5. ${wc}`
    }
  },

  // ---- 行政公文 ----
  {
    id: 'notice',
    name: '通知',
    icon: '📢',
    category: 'admin',
    desc: '工作通知、会议通知、制度印发通知等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"通知"类公文的撰写规范。你写的通知必须：1）标题格式规范（关于XX的通知）；2）正文先写通知事由，再写具体要求；3）要求清晰明确、可执行；4）必要时列明时间节点和责任人；5）语言正式规范，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '通知事由', placeholder: '如：关于开展2025年度信贷资产风险分类工作的通知', required: true, type: 'text' },
      { key: 'content', label: '通知内容/要求', placeholder: '如：各支行需在6月30日前完成分类工作，重点排查...', required: true, type: 'textarea' },
      { key: 'deadline', label: '截止时间/时间节点', placeholder: '如：2025年6月30日', required: false, type: 'text' },
      { key: 'scope', label: '通知范围', placeholder: '如：各分支行、总行信贷管理部', required: false, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认500-1200字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数500-1200字，请充分展开论述'
      return `请根据以下信息撰写一份通知：

【通知事由】${data.title}
【通知内容】${data.content}
${data.deadline ? `【截止时间】${data.deadline}\n` : ''}${data.scope ? `【通知范围】${data.scope}\n` : ''}
要求：
1. 标题格式：关于XX的通知
2. 正文先写事由，再写具体要求
3. 要求清晰明确、可执行
4. ${wc}`
    }
  },
  {
    id: 'letter',
    name: '函件',
    icon: '✉️',
    category: 'admin',
    desc: '商洽函、询问函、答复函、催办函等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"函"类公文的撰写规范。你写的函件必须：1）标题格式规范（关于XX的函）；2）语气不卑不亢，符合平行文行文规范；3）事由清楚，诉求明确；4）用语得体规范，使用银行专业术语和公文用语；5）语言正式规范，杜绝口语化，使用"贵行""本行""依据"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '函件事由', placeholder: '如：关于协助查询XX客户账户信息的函', required: true, type: 'text' },
      { key: 'recipient', label: '收函单位', placeholder: '如：XX银行XX分行', required: true, type: 'text' },
      { key: 'content', label: '函件内容/诉求', placeholder: '如：因XX案件需要，请协助提供XX客户近半年交易流水', required: true, type: 'textarea' },
      { key: 'letterType', label: '函件类型', placeholder: '如：商洽函/询问函/答复函/催办函（留空默认商洽函）', required: false, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：500、800（留空则默认300-800字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数300-800字，请充分展开论述'
      return `请根据以下信息撰写一份函件：

【函件事由】${data.title}
【收函单位】${data.recipient}
【函件内容】${data.content}
${data.letterType ? `【函件类型】${data.letterType}\n` : ''}
要求：
1. 标题格式：关于XX的函
2. 语气不卑不亢，符合平行文规范
3. 事由清楚，诉求明确
4. 用语得体规范
5. ${wc}`
    }
  },
  {
    id: 'request',
    name: '请示',
    icon: '🙋',
    category: 'admin',
    desc: '请示批准、请示指示、请示审批等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"请示"类公文的撰写规范。你写的请示必须：1）一文一事，不夹带其他事项；2）请示理由充分、依据明确；3）请示事项具体清楚；4）语气恰当，用"妥否，请批示"等规范结尾；5）语言正式规范，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '请示事由', placeholder: '如：关于增设XX社区支行的请示', required: true, type: 'text' },
      { key: 'reason', label: '请示理由/背景', placeholder: '如：该社区常住人口5万，周边无银行网点，金融服务需求旺盛', required: true, type: 'textarea' },
      { key: 'requestContent', label: '请示事项', placeholder: '如：拟在XX路XX号设立社区支行，面积约200平方米，配备人员5名', required: true, type: 'textarea' },
      { key: 'recipient', label: '主送单位', placeholder: '如：分行/总行', required: false, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认500-1200字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数500-1200字，请充分展开论述'
      return `请根据以下信息撰写一份请示：

【请示事由】${data.title}
【请示理由】${data.reason}
【请示事项】${data.requestContent}
${data.recipient ? `【主送单位】${data.recipient}\n` : ''}
要求：
1. 一文一事，不夹带其他事项
2. 理由充分，依据明确
3. 请示事项具体清楚
4. 语气恰当，用"妥否，请批示"等规范结尾
5. ${wc}`
    }
  },
  {
    id: 'bulletin',
    name: '通报',
    icon: '🔔',
    category: 'admin',
    desc: '表彰通报、批评通报、情况通报等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"通报"类公文的撰写规范。你写的通报必须：1）标题格式规范（关于XX的通报）；2）事实描述客观准确；3）定性分析有理有据；4）处理决定/要求明确具体；5）表彰用正面引导语气，批评用严肃规范语气；6）语言正式规范，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '通报事由', placeholder: '如：关于XX支行违规办理业务的通报', required: true, type: 'text' },
      { key: 'bulletinType', label: '通报类型', placeholder: '如：表彰通报/批评通报/情况通报', required: true, type: 'text' },
      { key: 'facts', label: '通报事实', placeholder: '如：XX支行客户经理在办理XX业务时存在XX违规行为', required: true, type: 'textarea' },
      { key: 'decision', label: '处理决定/要求', placeholder: '如：给予XX行政处分，扣发绩效XX元，全行通报', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认500-1200字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数500-1200字，请充分展开论述'
      return `请根据以下信息撰写一份通报：

【通报事由】${data.title}
【通报类型】${data.bulletinType}
【通报事实】${data.facts}
${data.decision ? `【处理决定/要求】${data.decision}\n` : ''}
要求：
1. 标题格式：关于XX的通报
2. 事实描述客观准确
3. 定性分析有理有据
4. 处理决定/要求明确具体
5. ${wc}`
    }
  },
  {
    id: 'minutes',
    name: '会议纪要',
    icon: '📋',
    category: 'admin',
    desc: '专题会议纪要、协调会议纪要等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"会议纪要"的撰写规范。你写的会议纪要必须：1）格式规范：会议名称、时间、地点、主持人、参会人员、议题、议定事项；2）忠实反映会议内容，不得添枝加叶；3）议定事项明确具体、责任到人、有时限；4）用语简练规范，使用银行专业术语；5）语言正式规范，杜绝口语化，使用"本行""经研究""议定"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'meetingName', label: '会议名称', placeholder: '如：XX支行2025年风险防控专题会议', required: true, type: 'text' },
      { key: 'meetingInfo', label: '会议基本信息', placeholder: '时间、地点、主持人、参会人员（如：2025年3月15日，支行会议室，张XX主持，各部门负责人参加）', required: true, type: 'text' },
      { key: 'topics', label: '会议议题', placeholder: '如：1.通报一季度风险情况 2.研究不良处置方案 3.部署二季度风控工作', required: true, type: 'textarea' },
      { key: 'decisions', label: '议定要点（已知）', placeholder: '如：1.成立不良处置专项小组 2.6月底前完成XX户不良清收', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1000、2000（留空则默认800-1500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数800-1500字，请充分展开论述'
      return `请根据以下信息撰写一份会议纪要：

【会议名称】${data.meetingName}
【会议信息】${data.meetingInfo}
【会议议题】${data.topics}
${data.decisions ? `【议定要点】${data.decisions}\n` : ''}
要求：
1. 包含：会议名称、时间地点、参会人员、议题、议定事项
2. 忠实反映会议内容
3. 议定事项明确具体、责任到人、有时限
4. 用语简练规范
5. ${wc}`
    }
  },

  {
    id: 'reply',
    name: '批复',
    icon: '📝',
    category: 'admin',
    desc: '对应下级请示，给明确审批意见',
    systemPrompt: '你是一名商业银行公文写作专家，精通"批复"类公文的撰写规范。你写的批复必须：1）标题格式规范（关于XX的批复）；2）引用来文标题和文号；3）批复意见明确清晰，使用"同意/不同意/原则同意"等标准用语；4）如有要求需分条列明；5）语言正式规范，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '批复事项', placeholder: '如：关于XX支行增设XX社区支行的批复', required: true, type: 'text' },
      { key: 'incomingRef', label: '来文标题/文号', placeholder: '如：《关于增设XX社区支行的请示》（XX银报〔2025〕XX号）', required: true, type: 'text' },
      { key: 'applicant', label: '请示单位', placeholder: '如：XX支行', required: true, type: 'text' },
      { key: 'approvalOpinion', label: '批复意见', placeholder: '如：同意在XX路XX号设立社区支行，面积不超过200平方米', required: true, type: 'textarea' },
      { key: 'requirements', label: '相关要求', placeholder: '如：1.按规定办理相关手续 2.配备合规人员 3.完成时间节点', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：500、1000（留空则默认400-800字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数400-800字，请充分展开论述'
      return `请根据以下信息撰写一份批复：

【批复事项】${data.title}
【来文标题/文号】${data.incomingRef}
【请示单位】${data.applicant}
【批复意见】${data.approvalOpinion}
${data.requirements ? `【相关要求】${data.requirements}\n` : ''}
要求：
1. 标题格式：关于XX的批复
2. 引用来文标题和文号
3. 批复意见明确清晰
4. 如有要求需分条列明
5. ${wc}`
    }
  },
  {
    id: 'opinion',
    name: '意见',
    icon: '💡',
    category: 'admin',
    desc: '对重要工作提出见解和处理办法',
    systemPrompt: '你是一名商业银行公文写作专家，精通"意见"类公文的撰写规范。你写的意见必须：1）标题格式规范（关于XX的意见）；2）意见提出依据充分；3）观点明确、说理透彻；4）措施建议有针对性、可操作性；5）语言正式规范，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '意见事由', placeholder: '如：关于加强XX业务风险防控的指导意见', required: true, type: 'text' },
      { key: 'background', label: '背景/依据', placeholder: '如：当前XX业务风险暴露增多，亟需完善风控措施...', required: true, type: 'textarea' },
      { key: 'mainTasks', label: '主要意见/任务', placeholder: '如：1.完善客户准入标准 2.加强贷后管理 3.建立预警机制', required: true, type: 'textarea' },
      { key: 'guaranteeMeasures', label: '保障措施', placeholder: '如：1.强化考核引导 2.加强人员培训 3.完善系统支撑', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1000-2000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1000-2000字，请充分展开论述'
      return `请根据以下信息撰写一份意见：

【意见事由】${data.title}
【背景依据】${data.background}
【主要意见】${data.mainTasks}
${data.guaranteeMeasures ? `【保障措施】${data.guaranteeMeasures}\n` : ''}
要求：
1. 标题格式：关于XX的意见
2. 意见提出依据充分
3. 观点明确、说理透彻
4. 措施建议有针对性、可操作性
5. ${wc}`
    }
  },
  {
    id: 'decision',
    name: '决定',
    icon: '📜',
    category: 'admin',
    desc: '重大决策部署、奖惩、机构变更等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"决定"类公文的撰写规范。你写的决定必须：1）标题格式规范（关于XX的决定）；2）决定依据充分、事实清楚；3）决定事项表述严谨、无歧义；4）执行要求明确具体；5）语言正式规范，语气庄重严肃，使用银行专业术语和公文用语，杜绝口语化，使用"本行""依据""经研究决定"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '决定事由', placeholder: '如：关于表彰2025年度先进集体的决定', required: true, type: 'text' },
      { key: 'reason', label: '决定依据/背景', placeholder: '如：为表彰先进、树立典型，经考核评选...', required: true, type: 'textarea' },
      { key: 'decisionContent', label: '决定事项', placeholder: '如：授予XX支行等10个单位"先进集体"称号', required: true, type: 'textarea' },
      { key: 'executionReq', label: '执行要求', placeholder: '如：希望受表彰单位珍惜荣誉，再创佳绩', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：500、1000（留空则默认400-800字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数400-800字，请充分展开论述'
      return `请根据以下信息撰写一份决定：

【决定事由】${data.title}
【决定依据】${data.reason}
【决定事项】${data.decisionContent}
${data.executionReq ? `【执行要求】${data.executionReq}\n` : ''}
要求：
1. 标题格式：关于XX的决定
2. 决定依据充分、事实清楚
3. 决定事项表述严谨、无歧义
4. 执行要求明确具体
5. ${wc}`
    }
  },
  {
    id: 'announcement',
    name: '公告',
    icon: '📢',
    category: 'admin',
    desc: '面向社会公众发布重要事项',
    systemPrompt: '你是一名商业银行公文写作专家，精通"公告"类公文的撰写规范。你写的公告必须：1）标题格式规范（关于XX的公告）；2）公告事由清楚、内容准确完整；3）告知对象明确、信息充分；4）生效时间/有效期明确；5）语言正式规范，语气庄重，使用银行专业术语和公文用语，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '公告事由', placeholder: '如：关于XX银行XX分行迁址的公告', required: true, type: 'text' },
      { key: 'reason', label: '公告背景/依据', placeholder: '如：经监管部门批准，本行XX支行将搬迁至新址办公', required: true, type: 'textarea' },
      { key: 'announcementContent', label: '公告内容', placeholder: '如：新址位于XX路XX号，自X月X日起对外营业', required: true, type: 'textarea' },
      { key: 'effectiveDate', label: '生效日期/时间', placeholder: '如：自2025年6月1日起生效', required: true, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：300、600（留空则默认300-600字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数300-600字，请充分展开论述'
      return `请根据以下信息撰写一份公告：

【公告事由】${data.title}
【公告背景】${data.reason}
【公告内容】${data.announcementContent}
【生效日期】${data.effectiveDate}
要求：
1. 标题格式：关于XX的公告
2. 公告事由清楚、内容准确完整
3. 告知对象明确、信息充分
4. 生效时间明确
5. ${wc}`
    }
  },
  {
    id: 'proclamation',
    name: '通告',
    icon: '🔔',
    category: 'admin',
    desc: '一定范围内告知业务规则、临时安排等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"通告"类公文的撰写规范。你写的通告必须：1）标题格式规范（关于XX的通告）；2）通告背景明确；3）业务规则/安排清楚详细；4）违规后果/罚则明确；5）生效期限具体；6）语言正式规范，使用银行专业术语和公文用语，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '通告事由', placeholder: '如：关于调整个人外汇业务办理流程的通告', required: true, type: 'text' },
      { key: 'reason', label: '通告背景/依据', placeholder: '如：为优化业务流程，提升客户体验，根据监管要求...', required: true, type: 'textarea' },
      { key: 'specificRules', label: '具体规则/安排', placeholder: '如：1.个人结汇单笔限额调整 2.新增线上预约功能 3.材料清单更新', required: true, type: 'textarea' },
      { key: 'penalties', label: '违规后果/注意事项', placeholder: '如：对不符合新规要求的业务将不予受理', required: false, type: 'textarea' },
      { key: 'effectiveDate', label: '生效日期', placeholder: '如：自2025年7月1日起施行', required: true, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：500、1000（留空则默认400-800字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数400-800字，请充分展开论述'
      return `请根据以下信息撰写一份通告：

【通告事由】${data.title}
【通告背景】${data.reason}
【具体规则】${data.specificRules}
${data.penalties ? `【违规后果】${data.penalties}\n` : ''}【生效日期】${data.effectiveDate}
要求：
1. 标题格式：关于XX的通告
2. 通告背景明确
3. 业务规则清楚详细
4. 生效期限具体
5. ${wc}`
    }
  },
  {
    id: 'work-plan',
    name: '工作计划',
    icon: '📅',
    category: 'admin',
    desc: '年度/季度/月度工作计划，重点工作安排',
    systemPrompt: '你是一名商业银行行政管理专家，精通工作计划和工作要点的撰写。你写的工作计划必须：1）目标明确、可量化；2）任务分解具体到责任人和时间节点；3）措施有操作性；4）符合银行内部管理规范；5）语言正式规范，使用银行专业术语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '计划名称', placeholder: '如：XX分行2026年信贷风险管理工作计划', required: true, type: 'text' },
      { key: 'department', label: '制定部门', placeholder: '如：风险管理部', required: true, type: 'text' },
      { key: 'period', label: '计划期间', placeholder: '如：2026年度/2026年一季度', required: true, type: 'text' },
      { key: 'goals', label: '主要工作目标', placeholder: '列出3-5项核心目标，尽量包含量化指标', required: true, type: 'textarea' },
      { key: 'keyTasks', label: '重点任务及时间节点', placeholder: '如：1.一季度完成XX排查 2.二季度修订XX制度 3.三季度开展XX培训', required: true, type: 'textarea' },
      { key: 'measures', label: '保障措施', placeholder: '如：组织保障、考核机制、资源配备等', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份工作计划：

【计划名称】${data.title}
【制定部门】${data.department}
【计划期间】${data.period}
【工作目标】${data.goals}
【重点任务】${data.keyTasks}
${data.measures ? `【保障措施】${data.measures}\n` : ''}要求：
1. 结构包含：指导思想、工作目标、重点任务与时间节点、保障措施
2. 目标明确可量化
3. 任务分解到责任人和时间节点
4. 措施具有可操作性
5. ${wc}`
    }
  },
  {
    id: 'inter-dept-note',
    name: '跨部门工作联系单',
    icon: '🔗',
    category: 'admin',
    desc: '跨部门业务协作、事项转办、工作联系等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"工作联系单"的撰写规范。你写的工作联系单必须：1）事项清楚、诉求明确；2）语气得体，符合平行文规范；3）必要时限明确；4）语言正式规范，使用银行专业术语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '标题', placeholder: '如：关于XX业务系统数据接口调整的工作联系单', required: true, type: 'text' },
      { key: 'fromDept', label: '发文部门', placeholder: '如：信息技术部', required: true, type: 'text' },
      { key: 'toDept', label: '收文部门', placeholder: '如：运营管理部', required: true, type: 'text' },
      { key: 'content', label: '联系事项及要求', placeholder: '请详细描述需要协作的事项、要求及时限', required: true, type: 'textarea' },
      { key: 'deadline', label: '时限要求', placeholder: '如：请于5个工作日内回复', required: false, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：500、1000（留空则默认400-800字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数400-800字，请充分展开论述'
      return `请根据以下信息撰写一份跨部门工作联系单：

【标题】${data.title}
【发文部门】${data.fromDept}
【收文部门】${data.toDept}
【联系事项】${data.content}
${data.deadline ? `【时限】${data.deadline}\n` : ''}要求：
1. 事项清楚、诉求明确
2. 语气得体，符合平行文规范
3. 必要时限明确
4. ${wc}`
    }
  },
  {
    id: 'supervision-notice',
    name: '督办通知',
    icon: '⏰',
    category: 'admin',
    desc: '重要工作督办、限期办结通知、催办函等',
    systemPrompt: '你是一名商业银行行政管理专家，精通督办通知的撰写。你写的督办通知必须：1）督办事项具体明确；2）时限要求清晰；3）反馈要求可执行；4）语气严肃得体；5）语言正式规范，使用银行专业术语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '标题', placeholder: '如：关于加快推进XX项目建设的督办通知', required: true, type: 'text' },
      { key: 'supervisedUnit', label: '被督办单位', placeholder: '如：XX支行/XX部门', required: true, type: 'text' },
      { key: 'deadline', label: '完成时限', placeholder: '如：2026年6月30日前', required: true, type: 'text' },
      { key: 'content', label: '督办事项及要求', placeholder: '详细描述督办事项内容及具体要求', required: true, type: 'textarea' },
      { key: 'reportReq', label: '反馈要求', placeholder: '如：请于完成后3个工作日内提交书面报告', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：600、1200（留空则默认500-1000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数500-1000字，请充分展开论述'
      return `请根据以下信息撰写一份督办通知：

【标题】${data.title}
【被督办单位】${data.supervisedUnit}
【完成时限】${data.deadline}
【督办事项】${data.content}
${data.reportReq ? `【反馈要求】${data.reportReq}\n` : ''}要求：
1. 督办事项具体明确
2. 时限要求清晰
3. 反馈要求可执行
4. 语气严肃得体
5. ${wc}`
    }
  },
  {
    id: 'compliance-pledge',
    name: '合规承诺书',
    icon: '🤝',
    category: 'admin',
    desc: '合规经营承诺书、廉洁从业承诺、年度绩效责任书等',
    systemPrompt: '你是一名商业银行合规管理专家，精通各类承诺书和责任书的撰写。你写的承诺书必须：1）承诺事项清晰具体；2）违约责任明确；3）语气庄重严肃；4）语言正式规范，使用银行专业术语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '标题', placeholder: '如：XX银行员工合规经营承诺书', required: true, type: 'text' },
      { key: 'name', label: '承诺人姓名', placeholder: '如：张三', required: true, type: 'text' },
      { key: 'position', label: '职务', placeholder: '如：XX支行行长/客户经理', required: true, type: 'text' },
      { key: 'pledgeContent', label: '承诺事项', placeholder: '逐条列明承诺事项，如：1.严格遵守法律法规 2.遵守行内规章制度...', required: true, type: 'textarea' },
      { key: 'penalty', label: '违约处理', placeholder: '如：如有违反，自愿接受行内规章制度的相关处罚', required: false, type: 'textarea' },
      { key: 'effectiveDate', label: '生效日期', placeholder: '如：自签署之日起生效', required: false, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认600-1200字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数600-1200字，请充分展开论述'
      return `请根据以下信息撰写一份承诺书：

【标题】${data.title}
【承诺人】${data.name}
【职务】${data.position}
【承诺事项】${data.pledgeContent}
${data.penalty ? `【违约处理】${data.penalty}\n` : ''}${data.effectiveDate ? `【生效日期】${data.effectiveDate}\n` : ''}要求：
1. 承诺事项清晰具体
2. 违约责任明确
3. 语气庄重严肃
4. ${wc}`
    }
  },
  {
    id: 'employment-cert',
    name: '在职/收入证明',
    icon: '🪪',
    category: 'admin',
    desc: '员工在职证明、收入证明、对外业务介绍信等制式证明',
    systemPrompt: '你是一名商业银行综合管理专家，精通各类制式证明函的撰写。你写的证明文件必须：1）信息准确无误；2）格式规范标准；3）用途标注明确；4）语言正式规范。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'docType', label: '证明类型', placeholder: '在职证明/收入证明/介绍信', required: true, type: 'text' },
      { key: 'employeeName', label: '员工姓名', placeholder: '如：李四', required: true, type: 'text' },
      { key: 'idNumber', label: '身份证号', placeholder: '如：110101199001011234', required: true, type: 'text' },
      { key: 'employer', label: '所在单位', placeholder: '如：XX银行XX分行', required: true, type: 'text' },
      { key: 'position', label: '职务', placeholder: '如：客户经理', required: false, type: 'text' },
      { key: 'annualIncome', label: '年收入', placeholder: '如：人民币贰拾万元整', required: false, type: 'text' },
      { key: 'purpose', label: '证明用途', placeholder: '如：用于办理信用卡/购房贷款', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：300、500（留空则默认200-500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数200-500字，请充分展开论述'
      return `请根据以下信息撰写一份${data.docType}：

【姓名】${data.employeeName}
【身份证号】${data.idNumber}
【所在单位】${data.employer}
${data.position ? `【职务】${data.position}\n` : ''}${data.docType === '收入证明' && data.annualIncome ? `【年收入】${data.annualIncome}\n` : ''}${data.purpose ? `【用途】${data.purpose}\n` : ''}要求：
1. 格式规范标准
2. 信息准确无误
3. 用途标注明确
4. ${wc}`
    }
  },
  {
    id: 'cash-transfer',
    name: '现金调拨申请',
    icon: '💰',
    category: 'admin',
    desc: '网点现金调拨、重要空白凭证领用/上缴申请',
    systemPrompt: '你是一名商业银行运营管理专家，精通现金和重要空白凭证调拨申请的撰写。你写的调拨申请必须：1）申请事项明确；2）数据准确；3）理由充分合理；4）语言正式规范。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'applicant', label: '申请单位', placeholder: '如：XX支行/XX网点', required: true, type: 'text' },
      { key: 'itemName', label: '调拨物品', placeholder: '如：人民币现金/重要空白凭证（支票/存单）', required: true, type: 'text' },
      { key: 'applyAmount', label: '申请数量/金额', placeholder: '如：现金500万元/凭证200份', required: true, type: 'text' },
      { key: 'reason', label: '申请事由', placeholder: '如：临近节假日，柜面现金需求量大', required: true, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：300、600（留空则默认300-600字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数300-600字，请充分展开论述'
      return `请根据以下信息撰写一份调拨申请：

【申请单位】${data.applicant}
【调拨物品】${data.itemName}
【申请数量】${data.applyAmount}
【申请事由】${data.reason}
要求：
1. 申请事项明确、理由充分
2. 数据准确
3. ${wc}`
    }
  },
  {
    id: 'personnel-notice',
    name: '人事通知',
    icon: '👤',
    category: 'admin',
    desc: '岗位调整通知、转正通知、离职告知等',
    systemPrompt: '你是一名商业银行人力资源专家，精通人事通知的撰写。你写的人事通知必须：1）事项准确无误；2）生效时间明确；3）相关方告知到位；4）语言正式规范，使用银行专业术语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'noticeType', label: '通知类型', placeholder: '任免通知/转正通知/离职通知', required: true, type: 'text' },
      { key: 'employeeName', label: '员工姓名', placeholder: '如：王五', required: true, type: 'text' },
      { key: 'originalPosition', label: '原职务', placeholder: '如：XX支行副行长', required: false, type: 'text' },
      { key: 'newPosition', label: '新职务', placeholder: '如：XX支行行长', required: false, type: 'text' },
      { key: 'effectiveDate', label: '生效日期', placeholder: '如：2026年7月1日', required: true, type: 'text' },
      { key: 'content', label: '通知内容', placeholder: '其他人事变动相关信息、工作交接要求等', required: true, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：400、800（留空则默认300-600字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数300-600字，请充分展开论述'
      return `请根据以下信息撰写一份${data.noticeType}：

【员工姓名】${data.employeeName}
${data.originalPosition ? `【原职务】${data.originalPosition}\n` : ''}${data.newPosition ? `【新职务】${data.newPosition}\n` : ''}【生效日期】${data.effectiveDate}
【通知内容】${data.content}
要求：
1. 事项准确无误
2. 生效时间明确
3. 相关方告知到位
4. ${wc}`
    }
  },
  {
    id: 'complaint-reply',
    name: '客户投诉回复函',
    icon: '📨',
    category: 'admin',
    desc: '客户投诉、咨询的正式书面回复',
    systemPrompt: '你是一名商业银行客户服务专家，精通客户投诉回复函的撰写。你写的投诉回复必须：1）态度诚恳、不推诿；2）调查核实客观公正；3）处理结果明确具体；4）语言正式规范。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '标题', placeholder: '如：关于XX客户投诉事项的回复函', required: true, type: 'text' },
      { key: 'customerName', label: '客户姓名', placeholder: '如：赵六', required: false, type: 'text' },
      { key: 'complaintContent', label: '投诉事由', placeholder: '客户投诉的具体内容', required: true, type: 'textarea' },
      { key: 'investigation', label: '调查核实情况', placeholder: '客观描述调查过程和核实结果', required: true, type: 'textarea' },
      { key: 'handlingResult', label: '处理结果', placeholder: '具体的处理措施和结果', required: true, type: 'textarea' },
      { key: 'apology', label: '致歉与后续服务', placeholder: '如有过错的致歉说明及后续改进承诺', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认600-1200字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数600-1200字，请充分展开论述'
      return `请根据以下信息撰写一份客户投诉回复函：

【标题】${data.title}
${data.customerName ? `【客户姓名】${data.customerName}\n` : ''}【投诉事由】${data.complaintContent}
【调查核实情况】${data.investigation}
【处理结果】${data.handlingResult}
${data.apology ? `【致歉与后续服务】${data.apology}\n` : ''}要求：
1. 态度诚恳、不推诿
2. 调查核实客观公正
3. 处理结果明确具体
4. ${wc}`
    }
  },
  {
    id: 'account-freeze',
    name: '账户冻结告知函',
    icon: '🔒',
    category: 'admin',
    desc: '司法冻结/解冻告知、账户管控通知等',
    systemPrompt: '你是一名商业银行运营管理专家，精通账户冻结/解冻告知函的撰写。你写的告知函必须：1）法律依据准确；2）执行内容明确；3）告知事项完整；4）语言正式规范。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '标题', placeholder: '如：关于账户冻结的告知函', required: true, type: 'text' },
      { key: 'customerName', label: '客户名称', placeholder: '如：XX贸易有限公司', required: true, type: 'text' },
      { key: 'accountNumber', label: '账号', placeholder: '如：6200XXXXXXXXXXX', required: true, type: 'text' },
      { key: 'reason', label: '冻结/管控原因', placeholder: '如：根据XX法院协助执行通知书', required: true, type: 'text' },
      { key: 'freezeAmount', label: '冻结金额', placeholder: '如：人民币伍佰万元整', required: false, type: 'text' },
      { key: 'legalBasis', label: '法律依据', placeholder: '如：《中华人民共和国民事诉讼法》第二百四十二条', required: true, type: 'text' },
      { key: 'effectiveDate', label: '生效日期', placeholder: '如：自2026年6月25日起', required: true, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：400、800（留空则默认300-600字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数300-600字，请充分展开论述'
      return `请根据以下信息撰写一份账户冻结/解冻告知函：

【标题】${data.title}
【客户信息】${data.customerName}
【账户信息】${data.accountNumber}
【冻结原因】${data.reason}
${data.freezeAmount ? `【冻结金额】${data.freezeAmount}\n` : ''}【法律依据】${data.legalBasis}
【生效日期】${data.effectiveDate}
要求：
1. 法律依据准确
2. 执行内容明确
3. 告知事项完整
4. ${wc}`
    }
  },
  {
    id: 'loan-maturity',
    name: '贷款到期提醒函',
    icon: '⏳',
    category: 'admin',
    desc: '贷款到期前提醒、逾期催收通知书等',
    systemPrompt: '你是一名商业银行信贷管理专家，精通贷款到期提醒函的撰写。你写的提醒函必须：1）贷款信息准确；2）到期时间明确；3）还款方式清晰；4）语言正式规范，使用银行专业术语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'customerName', label: '客户名称', placeholder: '如：XX贸易有限公司', required: true, type: 'text' },
      { key: 'contractNo', label: '合同编号', placeholder: '如：2025年XX字第001号', required: true, type: 'text' },
      { key: 'loanAmount', label: '贷款金额', placeholder: '如：人民币壹仟万元整', required: true, type: 'text' },
      { key: 'dueDate', label: '到期日期', placeholder: '如：2026年7月15日', required: true, type: 'text' },
      { key: 'outstandingAmount', label: '应还金额', placeholder: '如：人民币壹仟万元整及利息', required: false, type: 'text' },
      { key: 'repaymentMethod', label: '还款方式及账户', placeholder: '如：请将款项汇入XX银行XX账户', required: false, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：400、800（留空则默认300-600字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数300-600字，请充分展开论述'
      return `请根据以下信息撰写一份贷款到期提醒函：

【客户名称】${data.customerName}
【合同编号】${data.contractNo}
【贷款金额】${data.loanAmount}
【到期日期】${data.dueDate}
${data.outstandingAmount ? `【应还金额】${data.outstandingAmount}\n` : ''}${data.repaymentMethod ? `【还款方式】${data.repaymentMethod}\n` : ''}要求：
1. 贷款信息准确
2. 到期时间明确
3. 还款方式清晰
4. ${wc}`
    }
  },

  // ---- 汇报总结 ----
  {
    id: 'work-summary',
    name: '工作总结',
    icon: '📝',
    category: 'report',
    desc: '工作总结、季度总结、年度总结等',
    systemPrompt: '你是一名商业银行公文写作专家，精通银行各类总结汇报的规范和要求。你写的工作总结必须：1）成果部分用数据说话，避免空泛描述；2）不足部分客观诚恳，不回避问题；3）计划部分具体可衡量；4）符合银行内部汇报规范；5）语言正式但不刻板，使用银行专业术语；6）杜绝口语化，使用"本行""经梳理""依据"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'docType', label: '文种', placeholder: '如：工作总结/季度总结/年度总结', required: true, type: 'text' },
      { key: 'department', label: '汇报人/部门', placeholder: '如：风险管理部/XX支行', required: true, type: 'text' },
      { key: 'period', label: '汇报期间', placeholder: '如：2025年一季度', required: true, type: 'text' },
      { key: 'achievements', label: '主要工作成果', placeholder: '列出3-5项核心成果，尽量包含量化数据', required: true, type: 'textarea' },
      { key: 'issues', label: '存在的不足', placeholder: '如：不良率控制压力大，新发放贷款质量需关注', required: false, type: 'textarea' },
      { key: 'plans', label: '下一步计划', placeholder: '如：加强贷后管理、推进不良处置', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1000、2000（留空则默认1000-2000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1000-2000字，请充分展开论述'
      return `请根据以下信息撰写一份${data.docType}：

【文种】${data.docType}
【汇报人/部门】${data.department}
【汇报期间】${data.period}
【主要工作成果】${data.achievements}
${data.issues ? `【存在的不足】${data.issues}\n` : ''}${data.plans ? `【下一步计划】${data.plans}\n` : ''}
要求：
1. 成果部分用数据说话，避免空泛描述
2. 不足部分客观诚恳
3. 计划部分具体可衡量
4. 符合银行内部汇报规范
5. ${wc}`
    }
  },
  {
    id: 'work-report',
    name: '工作报告',
    icon: '📊',
    category: 'report',
    desc: '专项工作报告、述职类报告等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"工作报告"类公文的撰写规范。你写的工作报告必须：1）向上级汇报工作进展或完成情况；2）内容全面、重点突出；3）数据翔实、分析到位；4）存在问题和建议有针对性；5）符合上行文规范；6）语言正式规范，使用银行专业术语，杜绝口语化，使用"本行""依据""经梳理"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '报告事由', placeholder: '如：关于2025年上半年普惠金融工作推进情况的报告', required: true, type: 'text' },
      { key: 'department', label: '报告部门', placeholder: '如：普惠金融部/XX支行', required: true, type: 'text' },
      { key: 'progress', label: '工作进展/完成情况', placeholder: '如：新增普惠贷款XX万元，完成年度目标的XX%', required: true, type: 'textarea' },
      { key: 'problems', label: '存在问题', placeholder: '如：客户触达不足，产品竞争力待提升', required: false, type: 'textarea' },
      { key: 'suggestions', label: '工作建议', placeholder: '如：加大考核激励、优化审批流程', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1000-2000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1000-2000字，请充分展开论述'
      return `请根据以下信息撰写一份工作报告：

【报告事由】${data.title}
【报告部门】${data.department}
【工作进展】${data.progress}
${data.problems ? `【存在问题】${data.problems}\n` : ''}${data.suggestions ? `【工作建议】${data.suggestions}\n` : ''}
要求：
1. 向上级汇报工作进展或完成情况
2. 内容全面、重点突出
3. 数据翔实、分析到位
4. 存在问题和建议有针对性
5. ${wc}`
    }
  },
  {
    id: 'performance-report',
    name: '述职报告',
    icon: '🎯',
    category: 'report',
    desc: '个人述职、竞聘述职、年度述职等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"述职报告"的撰写规范。你写的述职报告必须：1）德能勤绩廉全面覆盖；2）业绩用数据和事实说话；3）自我评价客观中肯；4）不足剖析深入诚恳；5）改进方向明确具体；6）语言正式但有人情味，使用银行专业术语，杜绝口语化，使用"本行""依据""经梳理"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'name', label: '述职人姓名/职务', placeholder: '如：张XX/XX支行副行长', required: true, type: 'text' },
      { key: 'period', label: '述职期间', placeholder: '如：2025年度', required: true, type: 'text' },
      { key: 'duties', label: '岗位职责', placeholder: '如：分管信贷业务和风险管理', required: true, type: 'text' },
      { key: 'achievements', label: '主要业绩', placeholder: '列出3-5项核心业绩，用量化数据', required: true, type: 'textarea' },
      { key: 'weaknesses', label: '自我剖析不足', placeholder: '如：创新意识不够强，对新业务学习需加强', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份述职报告：

【述职人】${data.name}
【述职期间】${data.period}
【岗位职责】${data.duties}
【主要业绩】${data.achievements}
${data.weaknesses ? `【不足剖析】${data.weaknesses}\n` : ''}
要求：
1. 德能勤绩廉全面覆盖
2. 业绩用数据和事实说话
3. 自我评价客观中肯
4. 不足剖析深入诚恳，改进方向明确具体
5. ${wc}`
    }
  },
  {
    id: 'competitive-speech',
    name: '竞聘报告',
    icon: '🏆',
    category: 'report',
    desc: '竞聘上岗演讲稿、竞聘方案等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"竞聘报告/演讲稿"的撰写。你写的竞聘报告必须：1）竞聘理由充分，展示个人优势；2）对岗位理解深刻到位；3）工作思路清晰、有创新点；4）目标具体可衡量；5）语气自信但不张扬，诚恳有感染力；6）语言正式规范，使用银行专业术语，杜绝口语化，使用"本行""依据""经梳理"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'target', label: '竞聘岗位', placeholder: '如：XX支行行长/信贷管理部总经理', required: true, type: 'text' },
      { key: 'name', label: '竞聘人姓名/现职务', placeholder: '如：李XX/现任XX支行副行长', required: true, type: 'text' },
      { key: 'advantages', label: '个人优势/竞聘理由', placeholder: '如：10年信贷经验，熟悉该区域市场，曾主导XX项目', required: true, type: 'textarea' },
      { key: 'vision', label: '工作思路/目标', placeholder: '如：1.强化风控 2.拓展普惠金融 3.提升人均产能', required: true, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份竞聘报告：

【竞聘岗位】${data.target}
【竞聘人】${data.name}
【个人优势】${data.advantages}
【工作思路】${data.vision}
要求：
1. 竞聘理由充分，展示个人优势
2. 对岗位理解深刻到位
3. 工作思路清晰有创新点，目标具体可衡量
4. 语气自信不张扬，诚恳有感染力
5. ${wc}`
    }
  },

  {
    id: 'work-bulletin',
    name: '工作简报',
    icon: '📋',
    category: 'report',
    desc: '业务进展、一线动态的简版报送',
    systemPrompt: '你是一名商业银行公文写作专家，精通"工作简报"的撰写规范。你写的工作简报必须：1）简报格式规范（标题+正文+报送范围）；2）内容精炼、重点突出；3）用数据说话，简明扼要；4）语言简练规范，使用银行专业术语，杜绝口语化，使用"本行""依据""经梳理"等公文用语。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '简报标题', placeholder: '如：XX支行一季度普惠金融工作简报', required: true, type: 'text' },
      { key: 'department', label: '报送部门', placeholder: '如：XX支行/普惠金融部', required: true, type: 'text' },
      { key: 'period', label: '期间', placeholder: '如：2025年一季度', required: true, type: 'text' },
      { key: 'coreData', label: '核心数据/成效', placeholder: '如：新增普惠贷款XX万元，服务客户XX户，完成进度XX%', required: true, type: 'textarea' },
      { key: 'mainPractices', label: '主要做法/亮点', placeholder: '如：1.线上+线下联动营销 2.优化审批流程 3.产品创新', required: false, type: 'textarea' },
      { key: 'nextSteps', label: '下一步计划', placeholder: '如：加大XX行业拓展力度，推进XX产品上线', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认500-1000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数500-1000字，请充分展开论述'
      return `请根据以下信息撰写一份工作简报：

【简报标题】${data.title}
【报送部门】${data.department}
【期间】${data.period}
【核心数据】${data.coreData}
${data.mainPractices ? `【主要做法】${data.mainPractices}\n` : ''}${data.nextSteps ? `【下一步计划】${data.nextSteps}\n` : ''}
要求：
1. 简报格式规范
2. 内容精炼、重点突出
3. 用数据说话，简明扼要
4. ${wc}`
    }
  },
  {
    id: 'proposal',
    name: '倡议书',
    icon: '✊',
    category: 'report',
    desc: '旺季营销倡议、合规从业倡议等',
    systemPrompt: '你是一名商业银行公文写作专家，精通"倡议书"的撰写规范。你写的倡议书必须：1）标题格式规范（关于XX的倡议书）；2）背景说明充分，有感染力；3）倡议内容具体、有号召力；4）语言热情诚恳、有感染力，使用银行专业术语和公文用语，杜绝口语化。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '倡议事项', placeholder: '如：关于开展"开门红"旺季营销活动的倡议书', required: true, type: 'text' },
      { key: 'background', label: '背景/动因', placeholder: '如：2025年旺季营销已全面启动，为激发全员斗志...', required: true, type: 'textarea' },
      { key: 'proposalContent', label: '倡议内容/行动号召', placeholder: '如：1.全员行动起来 2.优化客户服务 3.争创营销佳绩', required: true, type: 'textarea' },
      { key: 'appeal', label: '号召/寄语', placeholder: '如：让我们以饱满的热情投入旺季营销，共创佳绩！', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认600-1200字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数600-1200字，请充分展开论述'
      return `请根据以下信息撰写一份倡议书：

【倡议事项】${data.title}
【背景动因】${data.background}
【倡议内容】${data.proposalContent}
${data.appeal ? `【号召寄语】${data.appeal}\n` : ''}
要求：
1. 标题格式：关于XX的倡议书
2. 背景说明充分，有感染力
3. 倡议内容具体、有号召力
4. 语言热情诚恳
5. ${wc}`
    }
  },
  {
    id: 'memorandum',
    name: '备忘录',
    icon: '📌',
    category: 'report',
    desc: '部门间会谈、同业洽谈的共识记录',
    systemPrompt: '你是一名商业银行公文写作专家，精通"备忘录"的撰写规范。你写的备忘录必须：1）记录会谈基本情况（时间、地点、参会方、参会人员）；2）讨论议题和各方观点忠实记录；3）达成的共识和协议事项清楚明确；4）后续跟进事项责任到人、时限明确；5）语言客观中立，使用银行专业术语和公文用语，杜绝口语化。你必须写出充分、详实的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '备忘录标题', placeholder: '如：与XX银行关于同业合作事项的会谈备忘录', required: true, type: 'text' },
      { key: 'participants', label: '参会各方/人员', placeholder: '如：XX银行XX部门张XX等X人，本行XX部门李XX等X人', required: true, type: 'text' },
      { key: 'meetingDate', label: '会谈时间', placeholder: '如：2025年5月20日', required: true, type: 'text' },
      { key: 'topics', label: '讨论议题/内容', placeholder: '如：1.银团贷款合作 2.同业授信额度 3.资金业务合作', required: true, type: 'textarea' },
      { key: 'consensus', label: '达成共识', placeholder: '如：1.同意开展XX亿元银团贷款合作 2.互予XX亿元授信额度', required: true, type: 'textarea' },
      { key: 'followUps', label: '后续事项', placeholder: '如：1.XX日前完成合作协议草案 2.XX日前提交授信材料', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认600-1200字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数600-1200字，请充分展开论述'
      return `请根据以下信息撰写一份备忘录：

【备忘录标题】${data.title}
【参会各方】${data.participants}
【会谈时间】${data.meetingDate}
【讨论议题】${data.topics}
【达成共识】${data.consensus}
${data.followUps ? `【后续事项】${data.followUps}\n` : ''}
要求：
1. 记录会谈基本情况
2. 讨论议题和各方观点忠实记录
3. 共识和协议事项清楚明确
4. 后续跟进事项责任到人、时限明确
5. ${wc}`
    }
  },
  {
    id: 'marketing-plan',
    name: '营销活动方案',
    icon: '🎯',
    category: 'report',
    desc: '旺季营销、节日活动、产品推广全案',
    systemPrompt: '你是一名商业银行营销策划专家，精通银行营销活动的方案策划与撰写。你写的营销活动方案必须：1）目标明确可衡量；2）目标客群定位精准；3）活动规则清晰有吸引力；4）推广渠道策略明确；5）预算和资源配置合理；6）考核评估机制完善；7）语言正式规范，使用银行专业术语，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '方案名称', placeholder: '如：XX银行2025年"开门红"旺季营销活动方案', required: true, type: 'text' },
      { key: 'goal', label: '活动目标', placeholder: '如：新增存款XX亿元，新增贷款XX亿元，新增客户XX户', required: true, type: 'textarea' },
      { key: 'targetCustomers', label: '目标客群', placeholder: '如：1.存量优质客户 2.代发工资客户 3.周边社区居民', required: true, type: 'textarea' },
      { key: 'activityRules', label: '活动内容/规则', placeholder: '如：1.存款送礼 2.推荐有礼 3.利率优惠 4.积分兑换', required: true, type: 'textarea' },
      { key: 'channels', label: '推广渠道', placeholder: '如：1.厅堂营销 2.电话外呼 3.社区宣传 4.线上推送', required: false, type: 'textarea' },
      { key: 'budget', label: '预算/资源配置', placeholder: '如：总预算XX万元，其中礼品XX万元，宣传XX万元', required: false, type: 'textarea' },
      { key: 'assessment', label: '考核/评估方式', placeholder: '如：按周通报进度，月末考核，优胜单位和个人给予奖励', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、3000（留空则默认2000-3000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数2000-3000字，请充分展开论述'
      return `请根据以下信息撰写一份营销活动方案：

【方案名称】${data.title}
【活动目标】${data.goal}
【目标客群】${data.targetCustomers}
【活动内容】${data.activityRules}
${data.channels ? `【推广渠道】${data.channels}\n` : ''}${data.budget ? `【预算配置】${data.budget}\n` : ''}${data.assessment ? `【考核评估】${data.assessment}\n` : ''}
要求：
1. 包含：目标、客群、活动规则、推广渠道、预算、考核
2. 目标明确可衡量
3. 目标客群定位精准
4. 活动规则清晰有吸引力
5. 考核评估机制完善
6. ${wc}`
    }
  },
  {
    id: 'accounting-error',
    name: '柜面账务差错说明',
    icon: '📊',
    category: 'report',
    desc: '柜面业务差错、账务差错的情况说明及整改',
    systemPrompt: '你是一名商业银行运营管理专家，精通柜面账务差错处理说明的撰写。你写的差错说明必须：1）差错事实描述准确；2）原因分析深入；3）账务调整方案合规；4）整改措施到位；5）语言客观不推诿。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '标题', placeholder: '如：关于XX支行柜面业务差错的说明', required: true, type: 'text' },
      { key: 'errorTime', label: '差错发生时间', placeholder: '如：2026年6月20日', required: true, type: 'text' },
      { key: 'errorDesc', label: '差错事实描述', placeholder: '详细描述差错的经过和具体情况', required: true, type: 'textarea' },
      { key: 'errorAmount', label: '差错金额', placeholder: '如：人民币XX万元', required: true, type: 'text' },
      { key: 'rootCause', label: '原因分析', placeholder: '深入分析差错发生的根本原因', required: true, type: 'textarea' },
      { key: 'adjustmentPlan', label: '账务调整方案', placeholder: '描述具体的账务调整措施', required: true, type: 'textarea' },
      { key: 'responsibility', label: '责任认定', placeholder: '如：经办人员XX负主要责任，复核人员XX负次要责任', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认600-1200字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数600-1200字，请充分展开论述'
      return `请根据以下信息撰写一份柜面账务差错处理说明：

【标题】${data.title}
【差错发生时间】${data.errorTime}
【差错事实】${data.errorDesc}
【差错金额】${data.errorAmount}
【原因分析】${data.rootCause}
【账务调整方案】${data.adjustmentPlan}
${data.responsibility ? `【责任认定】${data.responsibility}\n` : ''}要求：
1. 差错事实描述准确
2. 原因分析深入
3. 账务调整方案合规
4. 语言客观不推诿
5. ${wc}`
    }
  },
  {
    id: 'budget-plan',
    name: '预算编制/执行分析',
    icon: '📑',
    category: 'report',
    desc: '年度预算编制方案、预算执行情况分析报告',
    systemPrompt: '你是一名商业银行财务管理专家，精通预算编制和执行分析报告的撰写。你写的预算方案必须：1）编制依据充分；2）预算指标合理；3）分解方案具体；4）执行分析深入。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'docType', label: '文种', placeholder: '预算编制方案/预算执行分析报告', required: true, type: 'text' },
      { key: 'department', label: '部门/单位', placeholder: '如：XX分行/XX支行', required: true, type: 'text' },
      { key: 'period', label: '期间', placeholder: '如：2026年度', required: true, type: 'text' },
      { key: 'budgetTarget', label: '预算总体目标/执行概况', placeholder: '如：总收入目标XX万元，总支出控制在XX万元以内', required: true, type: 'textarea' },
      { key: 'breakdown', label: '分条线分解情况', placeholder: '如：公司条线XX万元、零售条线XX万元、同业条线XX万元', required: false, type: 'textarea' },
      { key: 'executionAnalysis', label: '执行差异分析', placeholder: '如：收入完成率XX%，差异原因分析', required: false, type: 'textarea' },
      { key: 'controlMeasures', label: '管控措施', placeholder: '如：1.按月监控 2.预警机制 3.调整审批', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、3000（留空则默认1500-2500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1500-2500字，请充分展开论述'
      return `请根据以下信息撰写一份${data.docType}：

【部门】${data.department}
【期间】${data.period}
【预算目标/执行概况】${data.budgetTarget}
${data.breakdown ? `【分条线分解】${data.breakdown}\n` : ''}${data.executionAnalysis ? `【执行差异分析】${data.executionAnalysis}\n` : ''}${data.controlMeasures ? `【管控措施】${data.controlMeasures}\n` : ''}要求：
1. 编制依据充分
2. 预算指标合理
3. 分解方案具体
4. 执行分析深入
5. ${wc}`
    }
  },
  {
    id: 'final-accounts',
    name: '年末财务决算报告',
    icon: '📊',
    category: 'report',
    desc: '年度财务决算说明、监管报送决算报告',
    systemPrompt: '你是一名商业银行财务管理专家，精通财务决算报告的撰写。你写的决算报告必须：1）数据准确完整；2）分析深入到位；3）特殊事项说明清晰；4）符合监管报送要求。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '报告标题', placeholder: '如：XX银行XX分行2026年度财务决算报告', required: true, type: 'text' },
      { key: 'department', label: '编制单位', placeholder: '如：XX分行财务会计部', required: true, type: 'text' },
      { key: 'fiscalYear', label: '决算年度', placeholder: '如：2026年度', required: true, type: 'text' },
      { key: 'coreData', label: '核心财务数据', placeholder: '如：总资产XX亿元，净利润XX亿元，营业收入XX亿元', required: true, type: 'textarea' },
      { key: 'specialItems', label: '特殊事项说明', placeholder: '如：重大资产处置、减值准备计提、税务调整等', required: false, type: 'textarea' },
      { key: 'resultApplication', label: '决算结果应用', placeholder: '如：利润分配方案、绩效考核依据', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：2000、4000（留空则默认2000-3500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数2000-3500字，请充分展开论述'
      return `请根据以下信息撰写一份财务决算报告：

【报告标题】${data.title}
【编制单位】${data.department}
【决算年度】${data.fiscalYear}
【核心财务数据】${data.coreData}
${data.specialItems ? `【特殊事项说明】${data.specialItems}\n` : ''}${data.resultApplication ? `【决算结果应用】${data.resultApplication}\n` : ''}要求：
1. 数据准确完整
2. 分析深入到位
3. 特殊事项说明清晰
4. ${wc}`
    }
  },
  {
    id: 'fund-position',
    name: '资金头寸报告',
    icon: '💹',
    category: 'report',
    desc: '每日/每周资金流动性测算报告',
    systemPrompt: '你是一名商业银行资金管理专家，精通资金头寸报告的撰写。你写的资金报告必须：1）数据时效性强；2）收支预测合理；3）缺口判断准确；4）建议可操作。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'reportType', label: '报告类型', placeholder: '日报/周报/月报', required: true, type: 'text' },
      { key: 'department', label: '编制单位', placeholder: '如：资金运营部', required: true, type: 'text' },
      { key: 'period', label: '报告期间', placeholder: '如：2026年6月25日', required: true, type: 'text' },
      { key: 'currentPosition', label: '当前头寸情况', placeholder: '如：备付金余额XX亿元，超额准备金率XX%', required: true, type: 'text' },
      { key: 'forecast', label: '未来收支预测', placeholder: '如：预计未来3日大额支出XX笔共XX亿元，大额收入XX笔共XX亿元', required: true, type: 'textarea' },
      { key: 'gapAnalysis', label: '缺口/盈余分析', placeholder: '如：预计明日头寸缺口约XX亿元', required: false, type: 'textarea' },
      { key: 'recommendations', label: '资金运作建议', placeholder: '如：建议开展XX亿元逆回购操作', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：600、1200（留空则默认500-1000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数500-1000字，请充分展开论述'
      return `请根据以下信息撰写一份资金头寸报告：

【报告类型】${data.reportType}
【编制单位】${data.department}
【报告期间】${data.period}
【当前头寸】${data.currentPosition}
【收支预测】${data.forecast}
${data.gapAnalysis ? `【缺口分析】${data.gapAnalysis}\n` : ''}${data.recommendations ? `【资金建议】${data.recommendations}\n` : ''}要求：
1. 数据时效性强
2. 收支预测合理
3. 缺口判断准确
4. 建议可操作
5. ${wc}`
    }
  },
  {
    id: 'tax-report',
    name: '税务测算及申报说明',
    icon: '🧾',
    category: 'report',
    desc: '各税种计提测算、纳税申报说明',
    systemPrompt: '你是一名商业银行税务管理专家，精通税务测算和申报说明的撰写。你写的税务说明必须：1）计税依据准确；2）测算过程清晰；3）法规引用正确；4）申报安排合理。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '标题', placeholder: '如：2026年二季度增值税测算及申报说明', required: true, type: 'text' },
      { key: 'taxType', label: '税种', placeholder: '如：增值税/企业所得税/印花税/房产税', required: true, type: 'text' },
      { key: 'calculationBasis', label: '计税依据', placeholder: '如：应税收入XX万元，适用税率X%', required: true, type: 'textarea' },
      { key: 'calculationProcess', label: '测算过程', placeholder: '详细描述税额计算过程', required: true, type: 'textarea' },
      { key: 'taxPayable', label: '应缴税额', placeholder: '如：人民币XX万元', required: true, type: 'text' },
      { key: 'declarationSchedule', label: '申报安排', placeholder: '如：于7月15日前完成申报缴纳', required: false, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500（留空则默认600-1200字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数600-1200字，请充分展开论述'
      return `请根据以下信息撰写一份税务测算及申报说明：

【标题】${data.title}
【税种】${data.taxType}
【计税依据】${data.calculationBasis}
【测算过程】${data.calculationProcess}
【应缴税额】${data.taxPayable}
${data.declarationSchedule ? `【申报安排】${data.declarationSchedule}\n` : ''}要求：
1. 计税依据准确
2. 测算过程清晰
3. 法规引用正确
4. 申报安排合理
5. ${wc}`
    }
  },
  {
    id: 'performance-bulletin',
    name: '绩效考核通报',
    icon: '🏆',
    category: 'report',
    desc: '各机构/部门绩效考核结果与排名通报',
    systemPrompt: '你是一名商业银行绩效管理专家，精通绩效考核通报的撰写。你写的考核通报必须：1）考核规则说明清晰；2）数据准确无争议；3）结果排名客观；4）改进建议有针对。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'title', label: '通报标题', placeholder: '如：2026年一季度绩效考核结果通报', required: true, type: 'text' },
      { key: 'period', label: '考核期间', placeholder: '如：2026年一季度', required: true, type: 'text' },
      { key: 'assessmentRules', label: '考核规则说明', placeholder: '如：考核指标体系、计分方式、权重分配等', required: true, type: 'textarea' },
      { key: 'overallResults', label: '整体完成情况', placeholder: '如：综合得分率XX%，较上期提升XX个百分点', required: true, type: 'textarea' },
      { key: 'rankings', label: '排名与得分', placeholder: '如：第一名XX支行XX分，末位XX支行XX分', required: true, type: 'textarea' },
      { key: 'improvement', label: '改进要求', placeholder: '如：末三位单位需提交整改方案', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1000、2000（留空则默认800-1500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数800-1500字，请充分展开论述'
      return `请根据以下信息撰写一份绩效考核通报：

【通报标题】${data.title}
【考核期间】${data.period}
【考核规则】${data.assessmentRules}
【整体完成情况】${data.overallResults}
【排名与得分】${data.rankings}
${data.improvement ? `【改进要求】${data.improvement}\n` : ''}要求：
1. 考核规则说明清晰
2. 数据准确无争议
3. 结果排名客观
4. 改进建议有针对
5. ${wc}`
    }
  },
  {
    id: 'training-plan',
    name: '培训计划/总结',
    icon: '📚',
    category: 'report',
    desc: '年度培训计划安排、专项培训总结',
    systemPrompt: '你是一名商业银行人力资源专家，精通培训计划和培训总结的撰写。你写的培训计划必须：1）目标明确有针对性；2）课程安排合理；3）参训人员准确；4）预算合理。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'docType', label: '文种', placeholder: '培训计划/培训总结', required: true, type: 'text' },
      { key: 'department', label: '部门', placeholder: '如：人力资源部', required: true, type: 'text' },
      { key: 'period', label: '期间', placeholder: '如：2026年度', required: true, type: 'text' },
      { key: 'trainingGoals', label: '培训目标/完成情况', placeholder: '如：计划举办XX期培训，覆盖XX人次，重点提升XX能力', required: true, type: 'textarea' },
      { key: 'courseArrangement', label: '课程安排/实施情况', placeholder: '详细列出课程名称、时间、形式、师资等', required: true, type: 'textarea' },
      { key: 'participants', label: '参训人员范围', placeholder: '如：全行信贷条线客户经理', required: false, type: 'text' },
      { key: 'budget', label: '培训预算/费用', placeholder: '如：XX万元', required: false, type: 'text' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：1500、2500（留空则默认1000-2000字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数1000-2000字，请充分展开论述'
      return `请根据以下信息撰写一份${data.docType}：

【部门】${data.department}
【期间】${data.period}
【培训目标/完成情况】${data.trainingGoals}
【课程安排/实施情况】${data.courseArrangement}
${data.participants ? `【参训人员】${data.participants}\n` : ''}${data.budget ? `【培训预算】${data.budget}\n` : ''}要求：
1. 目标明确有针对性
2. 课程安排合理
3. 参训人员准确
4. ${wc}`
    }
  },

  // ---- 自定义公文 ----
  {
    id: 'custom',
    name: '自定义公文',
    icon: '✏️',
    category: 'custom',
    desc: '任意公文类型，自定义要求，搜索不到时点此创建',
    systemPrompt: '你是一名商业银行公文写作专家，精通银行各类公文的撰写规范，包括但不限于：管理办法、实施细则、决定、批复、意见、决议、命令、批示、公告、通告、公示、承诺书、声明、协议、合同、制度、规程、规范、标准等。你写的公文必须：1）格式规范，符合银行公文行文标准；2）术语精准、用词严谨，使用银行专业术语；3）逻辑清晰、层次分明；4）语气得体，符合行文方向（上行文/下行文/平行文）；5）根据用户指定的公文类型自动适配格式和行文风格；6）语言正式规范，杜绝口语化，使用"本行""依据""经研究"等公文用语。你必须写出充分、详实、有深度的内容，不可敷衍了事。' + FORMAT_INSTRUCTION,
    fields: [
      { key: 'docType', label: '公文类型', placeholder: '如：管理办法/批复/决定/意见/公告/承诺书/公示/声明/实施细则...', required: true, type: 'text' },
      { key: 'title', label: '标题/事由', placeholder: '如：关于XX的批复 / XX管理办法', required: true, type: 'text' },
      { key: 'sender', label: '发文单位', placeholder: '如：XX银行XX分行/风险管理部', required: false, type: 'text' },
      { key: 'recipient', label: '主送/收文单位', placeholder: '如：各分支行/XX科室/监管分局', required: false, type: 'text' },
      { key: 'content', label: '核心内容/事由', placeholder: '详细描述公文要写的内容、背景、要点', required: true, type: 'textarea' },
      { key: 'customReqs', label: '其他要求', placeholder: '如：需包含附件清单、需引用XX监管文件、特定章节结构、试行期限等', required: false, type: 'textarea' },
      { key: 'wordCount', label: '字数要求', placeholder: '如：800、1500、3000（留空则默认800-1500字）', required: false, type: 'text' },
    ],
    buildUserPrompt: (data) => {
      const wc = data.wordCount ? `【硬性字数要求】输出约${data.wordCount}字，控制在${Math.round(data.wordCount * 0.8)}-${Math.round(data.wordCount * 1.3)}字之间，超出范围视为不合格。` : '字数800-1500字，请充分展开论述'
      return `请根据以下信息撰写一份${data.docType}：

【公文类型】${data.docType}
【标题】${data.title}
${data.sender ? `【发文单位】${data.sender}\n` : ''}${data.recipient ? `【主送单位】${data.recipient}\n` : ''}【核心内容】${data.content}
${data.customReqs ? `【其他要求】${data.customReqs}\n` : ''}
要求：
1. 严格按照"${data.docType}"的公文格式和行文规范撰写
2. 术语精准、用词严谨
3. 逻辑清晰、层次分明
4. 语气得体，符合行文方向
5. ${wc}`
    }
  },
];
