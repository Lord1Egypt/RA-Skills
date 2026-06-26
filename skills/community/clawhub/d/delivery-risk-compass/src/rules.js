/**
 * delivery-risk-compass
 *
 * 行业 + 经验方法论项目交付规则引擎。
 * 保留行业交付特征，去除个人、公司、客户、厂商、项目和具体数据痕迹。
 */

const PHASE_RULES = {
  '项目准备': {
    overall: '准备期决定项目后续是否可控。关键是组织、范围、计划、环境、沟通机制一次性拉齐。',
    key_points: [
      '启动会必须明确项目目标、范围边界、双方角色和升级路径',
      '项目计划按里程碑拆解，并标注客户依赖项',
      '提前确认部署、网络、账号、权限、数据和第三方系统条件',
      '建立统一文档、会议纪要、问题跟踪和变更管理机制'
    ],
    deliverables: ['项目章程', '组织与职责表', '总体计划', '环境准备清单', '沟通机制'],
    checkpoints: [
      '是否有双方认可的项目目标和范围？',
      '客户侧是否指定了业务、技术、管理三类负责人？',
      '环境和权限是否已列出责任人和完成时间？',
      '风险升级路径是否明确到具体角色？'
    ]
  },
  '需求调研与蓝图': {
    overall: '需求阶段最容易埋雷。要把现状、目标流程、数据边界和变更机制固化成可签收蓝图。',
    key_points: [
      '先画现状流程，再设计目标流程，避免直接写功能清单',
      '政府项目要补齐制度、审批、留痕、验收和安全要求',
      '零售项目要覆盖总部、门店、仓配、客服、运营等真实角色',
      '需求变更必须有影响评估、排期调整和确认记录'
    ],
    deliverables: ['现状流程', '目标蓝图', '需求边界说明', '数据与接口清单', '变更流程'],
    checkpoints: [
      '关键业务方是否参与确认？',
      '异常流程和边界场景是否覆盖？',
      '数据口径是否有归口负责人？',
      '变更流程是否在开发前确认？'
    ]
  },
  '系统实现': {
    overall: '实现阶段要防止“进度看似正常，理解已经偏航”。要让客户持续看到中间成果。',
    key_points: [
      '开发任务按业务闭环拆，不只按技术模块拆',
      '集成、数据、权限和报表类工作提前联调，不等到最后',
      '定期演示中间成果，让业务方及早纠偏',
      '测试标准要覆盖主流程、异常流程、权限边界和数据一致性'
    ],
    deliverables: ['任务分解表', '迭代计划', '接口与数据说明', '测试计划', '阶段演示记录'],
    checkpoints: [
      '客户是否看过阶段成果并反馈？',
      '核心接口是否已进入联调？',
      '测试标准是否包含业务验收口径？',
      '需求变更是否同步影响到计划和成本？'
    ]
  },
  '上线准备': {
    overall: '上线准备的风险集中在数据、培训、切换、回滚和支持资源。任何一个缺口都可能放大成上线事故。',
    key_points: [
      '数据迁移要先预演，再正式切换，并保留校验规则',
      '培训要覆盖关键用户和一线使用者，不能只培训管理员',
      '上线方案要明确灰度、全量、冻结窗口、值守安排和回滚条件',
      '验收材料提前准备，避免上线后才补文档'
    ],
    deliverables: ['上线方案', '数据迁移计划', '培训材料', '回滚方案', '验收材料包'],
    checkpoints: [
      '数据迁移是否做过预演和校验？',
      '关键用户是否完成实操训练？',
      '回滚条件和责任人是否明确？',
      '上线时间是否避开业务高峰？'
    ]
  },
  '上线与运维': {
    overall: '上线不是结束，稳定运行和终验闭环才是交付完成。要快速响应、沉淀知识、推动验收。',
    key_points: [
      '上线初期设置集中值守和问题分级处理机制',
      '每个问题要记录现象、影响、原因、处理动作和关闭结论',
      '运维交接要覆盖账号、配置、接口、数据、常见问题和升级路径',
      '终验标准必须回到合同、蓝图和验收材料，不临时扩口径'
    ],
    deliverables: ['值守计划', '问题台账', '运维手册', '知识库', '验收报告'],
    checkpoints: [
      '上线问题是否有统一入口和分级机制？',
      '高频问题是否沉淀到知识库？',
      '运维边界是否移交清楚？',
      '终验材料是否与合同和蓝图一致？'
    ]
  }
};

const INDUSTRY_RISK_PROFILES = {
  government: {
    label: '政府/公共服务',
    priorities: ['合规与审计', '跨部门协同', '数据安全', '验收材料', '运维边界'],
    watchouts: [
      '审批链长导致决策慢，计划要预留确认周期',
      '验收材料比功能演示更重要，要从项目初期同步积累',
      '安全、权限、日志和数据边界必须前置确认'
    ],
    recommendedPitfallIds: ['R01', 'R03', 'R08', 'R10']
  },
  retail: {
    label: '零售/消费品',
    priorities: ['业务连续性', '门店推广', '会员与订单数据', '活动高峰', '培训落地'],
    watchouts: [
      '门店、仓配、客服、运营口径不一致会造成返工',
      '上线窗口要避开活动高峰和财务结算关键期',
      '培训不到位会让系统上线后被一线绕开'
    ],
    recommendedPitfallIds: ['R02', 'R04', 'R05', 'R09']
  },
  manufacturing: {
    label: '制造/供应链',
    priorities: ['主数据', '系统集成', '计划协同', '质量追溯', '分阶段切换'],
    watchouts: [
      '主数据不治理，后续接口和报表都会失真',
      '生产和仓储系统不能等全部开发完才联调',
      '一次性切换风险高，通常需要并行或灰度策略'
    ],
    recommendedPitfallIds: ['R03', 'R04', 'R06', 'R07']
  },
  finance: {
    label: '金融/强监管',
    priorities: ['合规审查', '权限隔离', '审计追踪', '稳定性', '回滚与容灾'],
    watchouts: [
      '安全和合规评审会影响排期，不能后置',
      '敏感数据和权限模型需要专门确认',
      '上线前必须强化压测、回滚和应急演练'
    ],
    recommendedPitfallIds: ['R01', 'R03', 'R06', 'R08']
  },
  generic: {
    label: '通用企业项目',
    priorities: ['范围管理', '干系人协同', '数据与接口', '测试验收', '运维移交'],
    watchouts: [
      '范围不清会让项目持续膨胀',
      '只和单一部门对接会导致验收时意见反转',
      '验收标准要在需求阶段定义，而不是上线后再讨论'
    ],
    recommendedPitfallIds: ['R01', 'R02', 'R04', 'R06']
  }
};

const COMMON_PITFALLS = [
  {
    id: 'R01',
    severity: 'fatal',
    name: '需求边界未签收就开工',
    description: '需求只停留在口头确认，后续很容易出现范围扩大、返工和验收争议。',
    mitigation: '形成需求边界说明，并把未纳入范围、待确认事项和变更流程写清楚。',
    from: '行业普遍教训'
  },
  {
    id: 'R02',
    severity: 'serious',
    name: '关键业务方缺席',
    description: '只和技术或采购对接，业务方上线时才发现流程不匹配。',
    mitigation: '需求、演示、UAT和验收都要安排业务负责人参与。',
    from: '实战经验总结'
  },
  {
    id: 'R03',
    severity: 'fatal',
    name: '环境、权限和安全条件后置',
    description: '部署环境、账号权限、安全策略或网络连通晚确认，会直接压缩开发和测试时间。',
    mitigation: '项目准备期建立环境清单，逐项绑定客户侧责任人和完成时间。',
    from: '行业普遍教训'
  },
  {
    id: 'R04',
    severity: 'serious',
    name: '数据迁移和接口联调启动过晚',
    description: '数据和接口问题通常不是单点问题，越晚发现越难纠偏。',
    mitigation: '在系统实现中期前启动样本数据校验和核心接口联调。',
    from: '实战经验总结'
  },
  {
    id: 'R05',
    severity: 'serious',
    name: '培训只覆盖管理员',
    description: '一线使用者没有充分训练，上线后会出现抵触、误用或绕开系统。',
    mitigation: '按角色设计培训和演练，让关键用户完成真实场景操作。',
    from: '行业普遍教训'
  },
  {
    id: 'R06',
    severity: 'serious',
    name: '测试只测主流程',
    description: '只验证顺畅路径，忽略异常流程、权限边界和数据一致性，上线后风险集中爆发。',
    mitigation: '测试用例覆盖主流程、异常流程、权限、数据、性能和回滚。',
    from: '实战经验总结'
  },
  {
    id: 'R07',
    severity: 'normal',
    name: '客户依赖项无人追踪',
    description: '客户侧数据、接口、人员、审批等依赖没有责任人，会变成隐性延期。',
    mitigation: '项目周报单独列客户依赖项，明确责任人、完成时间和升级动作。',
    from: '行业普遍教训'
  },
  {
    id: 'R08',
    severity: 'serious',
    name: '验收材料上线后才补',
    description: '功能做完但材料不完整，会拖慢初验、终验和回款。',
    mitigation: '从项目准备期建立验收材料目录，按里程碑沉淀证据。',
    from: '实战经验总结'
  },
  {
    id: 'R09',
    severity: 'normal',
    name: '上线窗口选择不当',
    description: '在业务高峰、结算窗口或组织调整期上线，会放大任何小问题。',
    mitigation: '上线计划必须结合业务日历，并准备灰度或回滚策略。',
    from: '行业普遍教训'
  },
  {
    id: 'R10',
    severity: 'fatal',
    name: '售前承诺未交接',
    description: '交付团队不知道售前承诺了哪些范围、服务或效果，后续极易产生争议。',
    mitigation: '项目启动前完成售前交付交接，形成承诺清单和风险清单。',
    from: '实战经验总结'
  }
];

const COMMUNICATION_STRATEGY = {
  default_frequency: '每周一次正式同步，关键风险即时升级',
  escalation_rules: [
    { condition: '范围变化影响里程碑', action: '发起变更评估，并同步工期、成本和验收影响' },
    { condition: '客户依赖项连续延期', action: '升级到双方项目负责人，重新确认优先级' },
    { condition: '上线风险无法在计划内关闭', action: '组织上线评审，明确延期、灰度或回滚策略' },
    { condition: '验收口径发生变化', action: '回到合同、蓝图和会议纪要重新对齐' }
  ],
  stakeholder_strategy: {
    '管理层': {
      frequency: '按里程碑汇报，重大风险即时同步',
      format: '一页进度图 + 三项风险 + 需要拍板事项',
      tip: '管理层只需要判断方向、资源和风险，不要沉入任务细节。'
    },
    '业务负责人': {
      frequency: '需求、演示、UAT、上线前后重点沟通',
      format: '业务流程演示 + 问题清单 + 决策项',
      tip: '业务负责人必须持续参与，否则验收阶段容易反转。'
    },
    '技术负责人': {
      frequency: '每周例会，集成和环境问题即时沟通',
      format: '接口、环境、数据、缺陷、发布计划',
      tip: '技术负责人是风险前置的关键同盟。'
    },
    '一线用户': {
      frequency: '培训、演练、上线初期高频沟通',
      format: '场景化操作、问题收集、常见问答',
      tip: '一线用户的使用体验会直接影响推广成败。'
    }
  }
};

const EMERGENCY_RULES = [
  {
    situation: '项目明显延期',
    actions: [
      '冻结新增需求，先盘点剩余范围和关键阻塞',
      '把任务拆成必须交付、可延期、可替代三类',
      '重新确认客户依赖项和双方资源投入',
      '用新里程碑替代模糊承诺，并建立每日或隔日跟踪机制'
    ],
    from: '实战经验总结'
  },
  {
    situation: '客户对接人变动',
    actions: [
      '整理一份项目简报，包含目标、范围、进度、风险和待决事项',
      '组织交接会，让新旧对接人共同确认关键结论',
      '所有历史决策回到纪要和确认材料，不靠口头记忆',
      '观察新对接人的权限，如果无法拍板要及时升级'
    ],
    from: '行业普遍教训'
  },
  {
    situation: '上线前风险未关闭',
    actions: [
      '组织上线评审，逐项判断风险是否可接受',
      '准备灰度、延期或回滚三套方案',
      '明确上线值守和问题升级人',
      '把未关闭风险写入上线纪要，由双方负责人确认'
    ],
    from: '实战经验总结'
  },
  {
    situation: '验收卡住',
    actions: [
      '把争议拆成合同范围、蓝图范围、变更范围和新增诉求',
      '先关闭无争议项，保留争议项单独处理',
      '补齐证据材料，包括纪要、演示记录、测试记录和问题关闭记录',
      '必要时升级管理层，用范围和证据讨论，而不是情绪对抗'
    ],
    from: '行业普遍教训'
  }
];

const SIGNAL_RISK_RULES = [
  { match: ['需求频繁变更', '需求变更', '范围扩大'], score: 16, warning: '需求边界不稳：立即启用变更评估和范围冻结机制。' },
  { match: ['决策人不露面', '拍板人不见', '管理层缺席'], score: 14, warning: '关键决策人缺席：项目风险可能无法被及时拍板处理。' },
  { match: ['对接人变动', '换对接人'], score: 10, warning: '对接人变动：需要做正式交接，防止信息断层。' },
  { match: ['环境未准备', '权限未开通', '网络不通'], score: 14, warning: '环境依赖未关闭：会直接挤压开发、测试和上线时间。' },
  { match: ['数据质量差', '接口不稳定', '联调延期'], score: 14, warning: '数据或接口风险：应提前建立样本校验和联调日报。' },
  { match: ['售前承诺', '额外承诺'], score: 16, warning: '售前承诺风险：必须形成承诺清单并重新确认范围。' },
  { match: ['验收口径变化', '验收卡住'], score: 12, warning: '验收口径变化：回到合同、蓝图和变更记录对齐。' },
  { match: ['培训不足', '用户抵触'], score: 8, warning: '推广风险：需要补角色化培训和一线问题闭环。' }
];

const EXPERIENCE_TIPS = [
  '行业普遍教训：需求没签收就开工，后续争议几乎一定会落到交付团队身上。',
  '实战经验总结：政府类项目要从第一天沉淀验收证据，零售类项目要从第一天考虑一线推广。',
  '行业普遍教训：数据、接口、权限这三类问题不能等开发结束后再处理。',
  '实战经验总结：上线前的关键问题不是“能不能发版”，而是“出问题时谁能决策”。',
  '行业普遍教训：验收卡住时，不要争论感受，要回到合同、蓝图、纪要和证据。'
];

function detectIndustry(industry = '') {
  const text = String(industry).toLowerCase();
  if (/政府|政务|公共|应急|监管/.test(text)) return 'government';
  if (/零售|快消|消费|连锁|门店|电商|餐饮/.test(text)) return 'retail';
  if (/制造|供应链|工厂|生产|仓储|物流/.test(text)) return 'manufacturing';
  if (/金融|银行|保险|证券|支付|风控/.test(text)) return 'finance';
  return 'generic';
}

function detectPhase(input = {}) {
  const text = `${input.phase || ''} ${(input.signals || []).join(' ')}`;
  if (/上线准备|培训|迁移|切换|回滚/.test(text)) return '上线准备';
  if (/上线|运维|验收|终验|移交/.test(text)) return '上线与运维';
  if (/准备|启动|合同|立项/.test(text)) return '项目准备';
  if (/需求|调研|蓝图|流程/.test(text)) return '需求调研与蓝图';
  if (/开发|实现|联调|测试/.test(text)) return '系统实现';
  return '需求调研与蓝图';
}

function parseCycleMonths(cycle = '') {
  const match = String(cycle).match(/\d+/);
  return match ? Number(match[0]) : null;
}

function parsePayment(payment = '') {
  const parts = String(payment).split('-').map(item => Number(item)).filter(num => Number.isFinite(num));
  return parts.length ? parts : null;
}

function calculateRiskScore(input = {}) {
  let score = 100;
  const warnings = [];
  const signals = Array.isArray(input.signals) ? input.signals : [];
  const joined = signals.join(' ');

  for (const rule of SIGNAL_RISK_RULES) {
    if (rule.match.some(keyword => joined.includes(keyword))) {
      score -= rule.score;
      warnings.push(rule.warning);
    }
  }

  const months = parseCycleMonths(input.cycle);
  if (months && months >= 9) {
    score -= 8;
    warnings.push('周期较长：需要拆分阶段验收，避免风险在后期集中暴露。');
  }

  const payment = parsePayment(input.payment);
  if (payment) {
    if (payment[0] < 30) {
      score -= 8;
      warnings.push('首付款比例偏低：需要关注现金流和资源投入节奏。');
    }
    if (payment[payment.length - 1] > 20) {
      score -= 6;
      warnings.push('尾款比例偏高：需要提前设计验收证据和回款推动机制。');
    }
  }

  const teamSize = Number.parseInt(input.teamSize, 10);
  if (Number.isFinite(teamSize) && teamSize > 0 && teamSize < 3) {
    score -= 8;
    warnings.push('团队规模偏小：关键角色容易形成单点风险。');
  }

  score = Math.max(0, score);
  return {
    score,
    level: score >= 85 ? '健康' : score >= 70 ? '可控' : score >= 55 ? '需关注' : '高风险',
    warnings
  };
}

function severityLabel(severity) {
  return {
    fatal: '致命',
    serious: '严重',
    normal: '一般'
  }[severity] || '一般';
}

function generateAssessment(input = {}) {
  const project = input.project || '未命名项目';
  const industry = input.industry || '通用行业';
  const type = input.type || '实施+开发';
  const cycle = input.cycle || '未明确';
  const teamSize = input.teamSize || '未明确';
  const payment = input.payment || '未明确';
  const clientLocation = input.clientLocation || '未明确';
  const signals = Array.isArray(input.signals) ? input.signals.filter(Boolean) : [];
  const industryKey = detectIndustry(industry);
  const industryProfile = INDUSTRY_RISK_PROFILES[industryKey];
  const currentPhase = detectPhase({ ...input, signals });
  const risk = calculateRiskScore({ ...input, signals });

  const recommendedPitfalls = COMMON_PITFALLS
    .filter(item => industryProfile.recommendedPitfallIds.includes(item.id))
    .map(item => ({ ...item, severityLabel: severityLabel(item.severity) }));

  const fatal = COMMON_PITFALLS.filter(item => item.severity === 'fatal').length;
  const serious = COMMON_PITFALLS.filter(item => item.severity === 'serious').length;
  const normal = COMMON_PITFALLS.filter(item => item.severity === 'normal').length;

  return {
    project,
    industry,
    type,
    cycle,
    teamSize,
    payment,
    clientLocation,
    healthScore: risk.score,
    healthLevel: risk.level,
    warnings: risk.warnings,
    currentPhase,
    phaseAdvice: PHASE_RULES[currentPhase],
    industryProfile,
    recommendedPitfalls,
    pitfallStats: {
      fatal,
      serious,
      normal,
      total: COMMON_PITFALLS.length
    },
    communicationStrategy: COMMUNICATION_STRATEGY,
    emergencyPlans: EMERGENCY_RULES,
    nextMoves: [
      '补齐范围、依赖、风险、验收四张清单',
      '按当前阶段组织一次客户确认会',
      '把高风险项转成责任人、截止时间和升级动作'
    ],
    tip: EXPERIENCE_TIPS[Math.floor(Math.random() * EXPERIENCE_TIPS.length)]
  };
}

module.exports = {
  generateAssessment,
  PHASE_RULES,
  INDUSTRY_RISK_PROFILES,
  COMMON_PITFALLS,
  COMMUNICATION_STRATEGY,
  EMERGENCY_RULES,
  calculateRiskScore,
  detectIndustry,
  detectPhase
};
