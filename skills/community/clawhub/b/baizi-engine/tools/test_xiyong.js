// test_xiyong.js
// 2026-08-16 验收发现回归测试：身中和 bug 修复后 xiYong/jiYong 不应五行全列/空
// 根因：build_ui.py 原 `else { xiYong=WX_NAMES.slice(); }` 让身中和盘喜用五行全列
// 修复：中和分支按 ratio 细分偏强(ratio>0.5)/偏弱(ratio<0.5)/真中和(ratio≈0.5)

const fs=require('fs');
const html=fs.readFileSync(__dirname+'/../ui/index.html','utf8');
const m=html.match(/<script>([\s\S]*?)<\/script>/);
let code=m[1];
const stub=`globalThis._inp=globalThis._inp||{};
globalThis._els=globalThis._els||{};
globalThis._alerts=[];
function _getEl(id){if(!globalThis._els[id])globalThis._els[id]={value:"",textContent:"",innerHTML:"",style:{},classList:{add(){},remove(){}},onclick:null};if(globalThis._inp[id]!==undefined)globalThis._els[id].value=globalThis._inp[id];return globalThis._els[id];}
var document={getElementById:_getEl,querySelectorAll:()=>[],querySelector:()=>null};
var alert=(m)=>{globalThis._alerts.push(String(m));};`;
const expose=';globalThis.paipan=paipan;globalThis.WX_NAMES=WX_NAMES;';
eval(stub+code+expose);

let fails=0;
function assert(name, cond, extra){ console.log((cond?'  PASS ':'  FAIL ')+name+(extra?'  ['+extra+']':'')); if(!cond) fails++; }

console.log('=== 截图样本：1995-05-15 10:00 广州（验收触发盘）===');
const c1=paipan('测','男',1995,5,15,10,0,'广东省广州市','yes');
console.log(`  strength=${c1.strength}, xiYong=[${c1.xiYong.join('、')}] (${c1.xiYong.length}), jiYong=[${c1.jiYong.join('、')}] (${c1.jiYong.length})`);
// 修复后中和分支按 ratio 细分：偏强 xiYong=3 jiYong=2，偏弱 xiYong=2 jiYong=3，真中和 xiYong=0 jiYong=0
assert('中和盘 xiYong 不五行全列（不再 length=5）', !(c1.strength==='中和' && c1.xiYong.length===5), `strength=${c1.strength}, xiYong.length=${c1.xiYong.length}`);
assert('中和盘 jiYong 不空（除非真中和 ratio≈0.5）', !(c1.strength==='中和' && c1.jiYong.length===0 && c1.xiYong.length>0), `jiYong.length=${c1.jiYong.length}`);
// 中和分支 xiYong+jiYong 仍能覆盖五个可能性（除真中和外）
if(c1.strength==='中和' && c1.xiYong.length>0){
  assert('中和偏强/偏弱：xiYong+jiYong = 5 个元素', c1.xiYong.length + c1.jiYong.length === 5, `${c1.xiYong.length}+${c1.jiYong.length}=${c1.xiYong.length+c1.jiYong.length}`);
}

console.log('\n=== 批量验证：10 个盘 xiYong/jiYong 结构合理性 ===');
const cases = [
  [1995,5,15,10,0,'男','广东省广州市'],   // 截图样本
  [1990,5,15,10,0,'男','广州市'],
  [2000,1,1,0,0,'男','北京市'],
  [1985,7,7,12,0,'女','上海市'],
  [1972,3,3,6,0,'男','成都市'],
  [2003,11,11,18,0,'男','武汉市'],
  [1965,8,8,14,0,'女','杭州市'],
  [1998,9,9,9,0,'男','西安市'],
  [1978,2,2,2,0,'女','南京市'],
  [1988,12,25,23,0,'男','重庆市'],
];
let byStrength={强:0,弱:0,中和:0,其他:0};
let byXiLen={};
cases.forEach(([y,m,d,h,mi,s,p])=>{
  const c=paipan('测',s,y,m,d,h,mi,p,'yes');
  byStrength[c.strength]=(byStrength[c.strength]||0)+1;
  byXiLen[c.xiYong.length]=(byXiLen[c.xiYong.length]||0)+1;
  console.log(`  ${y}-${String(m).padStart(2,'0')}-${String(d).padStart(2,'0')} ${s} → strength=${c.strength}, xiYong=[${c.xiYong.join('、')}] (${c.xiYong.length}), jiYong=[${c.jiYong.join('、')}] (${c.jiYong.length})`);
});
console.log(`\n  strength 分布: 强=${byStrength.强||0}, 弱=${byStrength.弱||0}, 中和=${byStrength.中和||0}`);
console.log(`  xiYong.length 分布: ${Object.entries(byXiLen).map(([k,v])=>`${k}=${v}`).join(', ')}`);
// 不变量：身强 xiYong=3 jiYong=2；身弱 xiYong=2 jiYong=3；中和按 ratio 细分
let xiOk=true;
cases.forEach(([y,m,d,h,mi,s,p])=>{
  const c=paipan('测',s,y,m,d,h,mi,p,'yes');
  if(c.strength==='强' && (c.xiYong.length!==3 || c.jiYong.length!==2)) xiOk=false;
  else if(c.strength==='弱' && (c.xiYong.length!==2 || c.jiYong.length!==3)) xiOk=false;
  else if(c.strength==='中和' && c.xiYong.length===5) xiOk=false;
});
assert('10 盘 xiYong/jiYong 结构符合强/弱/中和规则', xiOk);

console.log('\n=== 汇总 ===');
console.log('FAIL: '+fails);
process.exit(fails===0?0:1);