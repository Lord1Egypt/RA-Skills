// 农历转公历验证 —— 用 bazi-app 已验证的 12 组用例交叉校验
const BaziEngine = require('../engine/engine.dist.js');

let pass = 0, fail = 0;
function assert(name, cond, extra){
  if(cond){ pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (extra?('  ['+extra+']'):'')); }
}

console.log('== 农历模块导出完整性 ==');
assert('LUNAR_INFO 200 条', BaziEngine.LUNAR_INFO.length === 200, 'len=' + BaziEngine.LUNAR_INFO.length);
assert('LUNAR_MONTH_NAMES 12 条', BaziEngine.LUNAR_MONTH_NAMES.length === 12);
assert('leapMonth 为函数', typeof BaziEngine.leapMonth === 'function');
assert('leapDays 为函数', typeof BaziEngine.leapDays === 'function');
assert('monthDays 为函数', typeof BaziEngine.monthDays === 'function');
assert('lunarToSolar 为函数', typeof BaziEngine.lunarToSolar === 'function');
assert('lunarDayName 为函数', typeof BaziEngine.lunarDayName === 'function');

console.log('== 闰月判断 ==');
// 2017 年有闰六月
assert('2017 闰月为六月', BaziEngine.leapMonth(2017) === 6, 'leap=' + BaziEngine.leapMonth(2017));
assert('2017 闰六月天数 30', BaziEngine.leapDays(2017) === 30, 'days=' + BaziEngine.leapDays(2017));
// 2020 年有闰四月
assert('2020 闰月为四月', BaziEngine.leapMonth(2020) === 4, 'leap=' + BaziEngine.leapMonth(2020));
// 2001 年有闰四月
assert('2001 闰四月', BaziEngine.leapMonth(2001) === 4, 'leap=' + BaziEngine.leapMonth(2001));

console.log('== 农历转公历（非闰月）==');
// 2024年正月初一 → 2024-02-10
let r1 = BaziEngine.lunarToSolar(2024, 1, 1, false);
assert('2024正月初一 → 2024-02-10', r1.y===2024 && r1.m===2 && r1.d===10, JSON.stringify(r1));
// 1990年五月初五 → 1990-05-28
let r2 = BaziEngine.lunarToSolar(1990, 5, 5, false);
assert('1990五月初五 → 1990-05-28', r2.y===1990 && r2.m===5 && r2.d===28, JSON.stringify(r2));
// 2000年腊月十五 → 2001-01-09
let r3 = BaziEngine.lunarToSolar(2000, 12, 15, false);
assert('2000腊月十五 → 2001-01-09', r3.y===2001 && r3.m===1 && r3.d===9, JSON.stringify(r3));

console.log('== 农历转公历（闰月用例）==');
// 2017年闰六月初一 → 2017-07-23
let r4 = BaziEngine.lunarToSolar(2017, 6, 1, true);
assert('2017闰六月初一 → 2017-07-23', r4.y===2017 && r4.m===7 && r4.d===23, JSON.stringify(r4));
// 2017年六月初一（非闰） → 2017-06-24
let r5 = BaziEngine.lunarToSolar(2017, 6, 1, false);
assert('2017六月初一(非闰) → 2017-06-24', r5.y===2017 && r5.m===6 && r5.d===24, JSON.stringify(r5));
// 2020年闰四月初一 → 2020-05-23
let r6 = BaziEngine.lunarToSolar(2020, 4, 1, true);
assert('2020闰四月初一 → 2020-05-23', r6.y===2020 && r6.m===5 && r6.d===23, JSON.stringify(r6));

console.log('== 农历日名映射 ==');
assert('初一', BaziEngine.lunarDayName(1) === '初一');
assert('初十', BaziEngine.lunarDayName(10) === '初十');
assert('十五', BaziEngine.lunarDayName(15) === '十五');
assert('二十', BaziEngine.lunarDayName(20) === '二十');
assert('廿三', BaziEngine.lunarDayName(23) === '廿三');
assert('三十', BaziEngine.lunarDayName(30) === '三十');

console.log('== 边界年份 ==');
// 1900 年正月初一 → 1900-01-31
let r7 = BaziEngine.lunarToSolar(1900, 1, 1, false);
assert('1900正月初一 → 1900-01-31', r7.y===1900 && r7.m===1 && r7.d===31, JSON.stringify(r7));
// 2099 年腊月三十 → 2099 或 2100 边界
let r8 = BaziEngine.lunarToSolar(2099, 12, 30, false);
assert('2099腊月三十 有效日期', r8.y>0 && r8.m>0 && r8.d>0, JSON.stringify(r8));

console.log('== 农历→排盘联动 ==');
// 农历 1990年五月初五 → 公历 1990-05-29，男，广州市，12:00，不校正
let solar = BaziEngine.lunarToSolar(1990, 5, 5, false);
let c = BaziEngine.paipan('测试', '男', solar.y, solar.m, solar.d, 12, 0, '广州市', 'no');
assert('农历转公历后排盘成功', c.yg && c.mg && c.dg && c.hg, JSON.stringify(c.pillars));
assert('日主存在', !!c.dayMaster);

console.log('\n结果: ' + pass + ' PASS, ' + fail + ' FAIL');
if (fail > 0) process.exit(1);
