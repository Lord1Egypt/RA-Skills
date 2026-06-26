#!/usr/bin/env node
/**
 * chudaxia-ai-coach / scripts/setup-workflow.cjs
 * 
 * 实训营前置准备工作流检查脚本
 * 来源：基于IMA知识库中AI实战训练营（2天）文档
 */

const args = process.argv.slice(2);
const clientIdx = args.indexOf('--client');
const modeIdx = args.indexOf('--mode');

const config = {
  client: clientIdx !== -1 ? args[clientIdx + 1] : '未指定客户',
  mode: modeIdx !== -1 ? args[modeIdx + 1] : 'full',
};

console.log(`\n╔═══════════════════════════════════════╗`);
console.log(`║  楚大侠 · 实训营前置准备工作流      ║`);
console.log(`║  客户: ${config.client.padEnd(20)}║`);
console.log(`╚═══════════════════════════════════════╝\n`);

const checklist = [
  {
    id: 'C01', category: '客户调研',
    items: [
      '收集客户组织架构图',
      '确认参训规模（建议50人以内）',
      '了解客户行业背景与数字化成熟度',
      '确认参训人员层级（管理层/业务负责人/数字化负责人/核心骨干）',
      '收集参训人员岗位职责说明书',
    ],
  },
  {
    id: 'C02', category: '培训方案',
    items: [
      '确认培训时长（建议2天）',
      '准备行业相关案例素材',
      '打印选题卡实训物料',
      '设计分组策略（分组实训，建议5-6人/组）',
      '确认是否需定制课程内容',
    ],
  },
  {
    id: 'C03', category: '工具准备',
    items: [
      '确认飞书/企微/钉钉企业版账号（含AI权益）',
      '确认腾讯IMA知识库工具可用',
      '确认WiFi/投影/音响设备正常',
      '确认学员自带电脑',
      '准备数字员工平台演示环境',
    ],
  },
  {
    id: 'C04', category: '教学物料',
    items: [
      '准备业务场景选题卡（每人2-3张）',
      '准备授课PPT（AI趋势/行业实践/挑战对策/工具应用/智能体架构/项目组织）',
      '准备案例资料包',
      '准备结营路演评分表',
    ],
  },
];

for (const group of checklist) {
  console.log(`\n📋 ${group.category} [${group.id}]`);
  console.log('─'.repeat(40));
  for (const item of group.items) {
    console.log(`  □ ${item}`);
  }
}

console.log(`\n${'═'.repeat(50)}`);
console.log(`📊 汇总`);
console.log(`  客户: ${config.client}`);
console.log(`  建议准备时间: ${config.mode === 'quick' ? '半天' : '1-2天'}`);

console.log(`\n📚 可引用案例（来自知识库）：`);
console.log(`  南方电网、广汽集团、广东省建设银行、广东省环保协会`);
console.log(`  深圳机场、东风集团、福建海关、拓尔思智能学院`);
console.log(`  中关村人工智能学院、鲁邦通、里弗斯医疗`);

console.log(`\n✅ 准备完成。\n`);
