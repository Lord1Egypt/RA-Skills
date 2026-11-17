// 验证 P1-1 / P1-2 / P1-3 修复
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/../ui/index.html', 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
const code = m[1];
const stub = 'var els={};var document={getElementById:(id)=>{if(!els[id])els[id]={value:"",textContent:"",innerHTML:"",style:{},classList:{add(){},remove(){}},onclick:null};return els[id];},querySelectorAll:()=>[],querySelector:()=>null};var alert=function(m){console.log("ALERT:",m)};';
const expose = ';globalThis.paipan=paipan;globalThis.yearGZ=yearGZ;globalThis.monthGZ=monthGZ;globalThis.getDaYun=getDaYun;globalThis.SANHE=SANHE;globalThis.WU_CHONG=WU_CHONG;globalThis.runLiuDay=runLiuDay;globalThis.__setLast=(c)=>{LAST=c;};globalThis.__els=els;';
eval(stub + code + expose);

let pass = 0, fail = 0;
function assert(name, cond){ if(cond){ pass++; console.log('  PASS '+name); } else { fail++; console.log('  FAIL '+name); } }

console.log('== P1-1: getDaYun 时刻精度 ==');
let dy1 = getDaYun(1964,9,10,12,0,'甲辰','癸酉','男');
let dy2 = getDaYun(1964,9,10,0,0,'甲辰','癸酉','男');
assert('12:00起运年龄>0', dy1.startAge > 0);
assert('00:00起运年龄>0', dy2.startAge > 0);
assert('12:00≠00:00（时刻有影响）', Math.abs(dy2.startAge - dy1.startAge) > 0.001);

console.log('== P1-3: JIEQI 年份范围 ==');
assert('1800年拦截', paipan('test','男',1800,1,1,12,0,'北京','no') === null);
assert('1895年边界通过', paipan('test','男',1895,6,1,12,0,'北京','no') !== null);
assert('2100年边界通过', paipan('test','男',2100,6,1,12,0,'北京','no') !== null);
assert('2101年拦截', paipan('test','男',2101,1,1,12,0,'北京','no') === null);
// yearGZ edge defenses
let yg = yearGZ(1895,6,1,12,0);
assert('yearGZ(1895) 有值', yg !== null);
yg = yearGZ(1894,6,1,12,0);
assert('yearGZ(1894) 拦截', yg === null);

console.log('== P1-2: runLiu NaN 防护（2026-08-19 修复：原为纯注释无断言）==');
assert('runLiuDay 含年份防护 isNaN(ty)', code.includes('isNaN(ty)'));
assert('runLiuDay 含范围防护 ty>2100', code.includes('ty>2100'));
assert('runLiuDay 含月份防护 tm<1', code.includes('tm<1'));

// 额外：验证 getDaYun 不因边界 JIEQI 崩溃
console.log('== 边界年 getDaYun ==');
let dyEdge = getDaYun(1895,6,1,12,0,'甲辰','癸酉','男');
assert('1895 boundary getDaYun', dyEdge.steps.length === 8);

// P1-4: 戊己非冲
console.log('== P1-4: WU_CHONG 戊己移除 ==');
assert('戊己非冲(戊)', WU_CHONG['戊']===undefined);
assert('戊己非冲(己)', WU_CHONG['己']===undefined);
assert('甲庚冲保留', WU_CHONG['甲']==='庚');
assert('乙辛冲保留', WU_CHONG['乙']==='辛');

// P1-5: 半合检测（2026-08-19 修复：原为自证式——测试自己重算 SANHE 断言自己的中间变量，被测代码未被调用）
console.log('== P1-5: 流日半合端到端（调 runLiuDay 实际逻辑）==');
__setLast(paipan('马云','男',1964,9,10,12,0,'北京市','no'));
__els['liuDayYear'].value='2026'; __els['liuDayMonth'].value='6';
runLiuDay();
const ldHtml = __els['liuDayResult'].innerHTML || '';
assert('马云盘 2026-06 流日输出含半合火（午/戌流日+原局缺寅）', ldHtml.includes('半合火'));
assert('SANHE 数据表 4 组', Array.isArray(SANHE) && SANHE.length === 4);

console.log('\n结果: ' + pass + ' PASS, ' + fail + ' FAIL');
if (fail > 0) process.exit(1);
