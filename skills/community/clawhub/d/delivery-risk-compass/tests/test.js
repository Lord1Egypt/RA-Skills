const assert = require('assert');
const fs = require('fs');
const path = require('path');
const {
  generateAssessment,
  detectIndustry,
  detectPhase,
  calculateRiskScore
} = require('../src/rules');

const result = generateAssessment({
  project: '某平台升级项目',
  industry: '政府/公共服务',
  type: '实施+开发',
  cycle: '6个月',
  teamSize: '6人',
  payment: '30-40-20-10',
  phase: '上线准备',
  signals: ['环境未准备', '验收口径变化']
});

assert.strictEqual(result.industryProfile.label, '政府/公共服务');
assert.strictEqual(result.currentPhase, '上线准备');
assert.ok(result.healthScore < 100);
assert.ok(result.recommendedPitfalls.length > 0);
assert.ok(result.phaseAdvice.deliverables.length > 0);
assert.ok(result.emergencyPlans.length > 0);

assert.strictEqual(detectIndustry('零售连锁'), 'retail');
assert.strictEqual(detectIndustry('制造供应链'), 'manufacturing');
assert.strictEqual(detectPhase({ signals: ['开发联调'] }), '系统实现');
assert.ok(calculateRiskScore({ signals: ['需求频繁变更'] }).score < 100);

const root = path.resolve(__dirname, '..');
const files = [
  'SKILL.md',
  'README.md',
  'package.json',
  'src/index.js',
  'src/rules.js',
  'tests/test.js'
];

const forbidden = [
  ['17', '年'].join(''),
  ['18', '年'].join(''),
  ['资深', '从业者'].join(''),
  ['测试', '点'].join(''),
  ['问题', '关闭率'].join(''),
  ['P', '0'].join(''),
  ['P', '1'].join(''),
  ['P', '2'].join(''),
  ['P', '3'].join('')
];

for (const file of files) {
  const content = fs.readFileSync(path.join(root, file), 'utf8');
  for (const word of forbidden) {
    assert.ok(!content.includes(word), `${file} contains forbidden text: ${word}`);
  }
}

console.log('delivery-risk-compass tests passed');
