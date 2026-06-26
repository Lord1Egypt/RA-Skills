const assert = require('assert');
const ChangeBrief = require('../src/index.js');

function run() {
  const engine = new ChangeBrief();
  let passed = 0;
  let failed = 0;

  function test(name, fn) {
    try {
      fn();
      console.log(`PASS ${name}`);
      passed += 1;
    } catch (error) {
      console.log(`FAIL ${name}: ${error.message}`);
      failed += 1;
    }
  }

  const beforeText = `
上周假设 onboarding 最大问题是注册步骤太多，暂时不需要法务审批。
计划 4 月底上线企业版 beta。
客户反馈主要来自中小团队，平均部署周期 14 天。
目前默认只支持英文模板。
`;

  const afterText = `
这周新增 6 条客户访谈，反复指出 onboarding 的核心问题是价值表达不清。
企业版 beta 改为 5 月中旬上线，需要先完成法务审批。
新签的两家大客户要求中文模板，本季度必须补上。
部署周期已降到 7 天，但安全审查成为新的 blocker。
`;

  test('analyze finds important additions', () => {
    const result = engine.analyze({ 'before-text': beforeText, 'after-text': afterText });
    assert(result.importantAdditions.some((item) => item.line.includes('新签的两家大客户要求中文模板')));
  });

  test('analyze finds changed claims across snapshots', () => {
    const result = engine.analyze({ 'before-text': beforeText, 'after-text': afterText });
    assert(result.changedClaims.some((item) => item.before.includes('计划 4 月底上线企业版 beta') && item.after.includes('企业版 beta 改为 5 月中旬上线')));
  });

  test('invalidations catches stale legal assumption', () => {
    const result = engine.invalidations({ 'before-text': beforeText, 'after-text': afterText });
    assert(result.items.some((item) => item.stale.includes('暂时不需要法务审批') && item.replacement.includes('需要先完成法务审批')));
  });

  test('conflicts surfaces a decision-worthy change', () => {
    const result = engine.conflicts({ 'before-text': beforeText, 'after-text': afterText });
    assert(result.items.length >= 1);
    assert(result.items.some((item) => /审批|时间线|优先级/.test(item.decision)));
  });

  test('priorities returns three or fewer ranked actions', () => {
    const result = engine.priorities({ 'before-text': beforeText, 'after-text': afterText });
    assert(result.items.length >= 1);
    assert(result.items.length <= 3);
  });

  test('rendered brief includes the core management sections', () => {
    const result = engine.brief({ 'before-text': beforeText, 'after-text': afterText });
    const rendered = engine.render(result);
    assert(rendered.includes('这周新增了哪些重要信息'));
    assert(rendered.includes('哪些旧结论可能失效'));
    assert(rendered.includes('最值得立刻行动的 3 个变化'));
  });

  console.log(`\n${passed} passed, ${failed} failed`);
  process.exit(failed > 0 ? 1 : 0);
}

run();
