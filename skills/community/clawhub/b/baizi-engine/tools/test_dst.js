// 夏令时（1986-1991 中国）自动校正专项测试
// 用法: node tools/test_dst.js
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/../ui/index.html', 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if(!m){ console.error('未找到 script'); process.exit(1); }
let code = m[1];
const stub = `globalThis._inp=globalThis._inp||{};
globalThis._els=globalThis._els||{};
globalThis._alerts=[];
function _getEl(id){
  if(!globalThis._els[id]) globalThis._els[id]={value:"",textContent:"",innerHTML:"",style:{},classList:{add(){},remove(){}},onclick:null};
  if(globalThis._inp[id]!==undefined) globalThis._els[id].value=globalThis._inp[id];
  return globalThis._els[id];
}
var document={getElementById:_getEl,querySelectorAll:()=>[],querySelector:()=>null};
var getComputedStyle=()=>({getPropertyValue:()=>''});
var alert=(msg)=>{globalThis._alerts.push(String(msg));};`;
const expose = ';globalThis.dstOffset=dstOffset;globalThis.applyDst=applyDst;globalThis.paipan=paipan;globalThis.generate=generate;globalThis.__getLast=function(){return LAST;};globalThis.LAST=null;';
eval(stub + code + expose);

let fails = 0;
function assert(name, cond, extra){
  console.log((cond?'  PASS ':'  FAIL ')+name+(extra?'  ['+extra+']':''));
  if(!cond) fails++;
}

console.log('========== A. dstOffset 窗口判定 ==========');
assert('A1 1985 非窗口年', dstOffset(1985,7,15,10)===0, '='+dstOffset(1985,7,15,10));
assert('A2 1986 开始日前一天', dstOffset(1986,5,3,12)===0, '='+dstOffset(1986,5,3,12));
assert('A3 1986 开始日 02:00 前', dstOffset(1986,5,4,1)===0, '='+dstOffset(1986,5,4,1));
assert('A4 1986 开始日 02:00 起', dstOffset(1986,5,4,2)===1, '='+dstOffset(1986,5,4,2));
assert('A5 1986 结束日 02:00 前', dstOffset(1986,9,14,1)===1, '='+dstOffset(1986,9,14,1));
assert('A6 1986 结束日 02:00 起', dstOffset(1986,9,14,2)===0, '='+dstOffset(1986,9,14,2));
assert('A7 1988 窗口中间', dstOffset(1988,8,1,10)===1, '='+dstOffset(1988,8,1,10));
// 2026-10 修正回归：1988 年夏令时实际自 4/17 02:00 起（原表写 4/10，错 7 天 → 4/10~4/16 出生者时柱错、跨零点者日柱错）
assert('A7b 1988 起始日前一天(4/16) 不校正', dstOffset(1988,4,16,12)===0, '='+dstOffset(1988,4,16,12));
assert('A7c 1988 起始日(4/17) 02:00 起校正', dstOffset(1988,4,17,2)===1, '='+dstOffset(1988,4,17,2));
assert('A7d 1988 4/10 不在窗口内（旧表误判点）', dstOffset(1988,4,10,10)===0, '='+dstOffset(1988,4,10,10));
assert('A8 1991 最后一年窗口内', dstOffset(1991,6,20,10)===1, '='+dstOffset(1991,6,20,10));
assert('A9 1992 制度停止后', dstOffset(1992,6,1,10)===0, '='+dstOffset(1992,6,1,10));

console.log('========== B. applyDst 校正结果 ==========');
let b1=applyDst(1986,7,15,10);
assert('B1 窗口内减1小时', b1.hh===9&&b1.dst===1, JSON.stringify(b1));
let b2=applyDst(1985,7,15,10);
assert('B2 窗口外不动', b2.hh===10&&b2.dst===0, JSON.stringify(b2));
let b3=applyDst(1986,9,14,0);
assert('B3 跨天回退一日', b3.y===1986&&b3.m===9&&b3.d===13&&b3.hh===23&&b3.dst===1, JSON.stringify(b3));
// 2026-11（v1.3.12）修正回归：applyDst 原先只返回 {y,m,d,hh,dst}，调用方写 paipan(...,d.mm,...) 得到 undefined
// → Number(undefined)=NaN → paipan 静默返回 null（真实对接事故：Cannot read properties of null）
let b4=applyDst(1986,7,15,10,30);
assert('B4 透传分钟 mm=30（窗口内）', b4.mm===30&&b4.hh===9&&b4.dst===1, JSON.stringify(b4));
let b5=applyDst(1992,7,15,10,37);
assert('B5 透传分钟 mm=37（窗口外）', b5.mm===37&&b5.hh===10&&b5.dst===0, JSON.stringify(b5));
let b6=applyDst(1986,9,14,0,45);
assert('B6 跨天回退时分钟仍透传 mm=45', b6.d===13&&b6.hh===23&&b6.mm===45, JSON.stringify(b6));
assert('B7 不传 mm 时默认 0（旧调用方行为不变）', applyDst(1986,7,15,10).mm===0, JSON.stringify(applyDst(1986,7,15,10)));
// 端到端：applyDst 返回值原样喂 paipan（这是最容易踩的对接写法）
let b8=applyDst(1986,7,15,10,30);
let cb8=paipan('透传','男',b8.y,b8.m,b8.d,b8.hh,b8.mm,'广州市','no');
assert('B8 applyDst→paipan 分钟真的入盘（useH=9/useMin=30）', cb8!==null&&cb8.useH===9&&cb8.useMin===30, cb8?('时柱='+cb8.pillars[3]+' useH='+cb8.useH+' useMin='+cb8.useMin):'null');
// 分钟不是装饰：10:30 →(DST 9:30)→(真太阳时 9:03)= 巳时；10:00 →(9:00)→(8:33)= 辰时。
// 若 mm 丢失（旧 applyDst），后者会被当成 9:00 之外的乱值甚至直接 null。
let b9a=applyDst(1986,7,15,10,30), b9b=applyDst(1986,7,15,10,0);
let c9a=paipan('分钟30','男',b9a.y,b9a.m,b9a.d,b9a.hh,b9a.mm,'广州市','yes');
let c9b=paipan('分钟0','男',b9b.y,b9b.m,b9b.d,b9b.hh,b9b.mm,'广州市','yes');
assert('B9 分钟参与真太阳时校正并跨时辰（10:30→巳时 / 10:00→辰时）',
  !!c9a&&!!c9b&&c9a.pillars[3][1]==='巳'&&c9b.pillars[3][1]==='辰',
  (c9a?c9a.pillars[3]+'/useMin='+c9a.useMin:'null')+' vs '+(c9b?c9b.pillars[3]+'/useMin='+c9b.useMin:'null'));

console.log('========== C. 集成：UI 层链路(applyDst→paipan) 时柱变化 ==========');
let r1=applyDst(1986,7,15,10);
let c1=paipan('夏令时','男',r1.y,r1.m,r1.d,r1.hh,0,'广州市','yes');
assert('C1 1986 窗口内 10:00 → 辰时', c1&&c1.pillars[3][1]==='辰', c1?'时柱='+c1.pillars[3]+' useH='+c1.useH:'null');
let c2=paipan('对照','男',1992,7,15,10,0,'广州市','yes');
assert('C2 1992 无夏令时 10:00 → 巳时', c2&&c2.pillars[3][1]==='巳', c2?'时柱='+c2.pillars[3]+' useH='+c2.useH:'null');
let c3=paipan('对照2','男',1986,3,15,10,0,'广州市','yes');
assert('C3 1986 窗口外(3月) 10:00 → 巳时', c3&&c3.pillars[3][1]==='巳', c3?'时柱='+c3.pillars[3]+' useH='+c3.useH:'null');
let c4=paipan('辰时直接','男',1986,7,15,9,0,'广州市','yes');
assert('C4 同盘 9:00 不校正参照 = 辰时', c4&&c4.pillars[3][1]==='辰', c4?'时柱='+c4.pillars[3]:'null');
assert('C5 C1 与 C4 时柱一致(等价性)', c1.pillars[3][0]===c4.pillars[3][0], c1.pillars[3]+' vs '+c4.pillars[3]);

console.log('========== D. UI 层 generate 走通 ==========');
globalThis._inp = { gender:'男', year:'1986', month:'7', day:'15', timeMode:'exact', hour:'10', minute:'0', truesun:'yes', birthplace:'广州市' };
globalThis.generate();
let d1=globalThis.__getLast();
assert('D1 1986 窗口内 generate 时柱=辰', d1&&d1.pillars[3][1]==='辰', d1?'时柱='+d1.pillars[3]+' useH='+d1.useH+' dst='+d1.dst:'null');
assert('D2 ctx.dst 标记=1', d1&&d1.dst===1, 'dst='+(d1&&d1.dst));
assert('D5 结果页显示夏令时提示', (globalThis._els['rSolar'].innerHTML||'').indexOf('夏令时')>=0, (globalThis._els['rSolar'].innerHTML||'').slice(0,40));
globalThis._inp = { gender:'男', year:'1992', month:'7', day:'15', timeMode:'exact', hour:'10', minute:'0', truesun:'yes', birthplace:'广州市' };
globalThis.generate();
let d2=globalThis.__getLast();
assert('D3 1992 无窗口 时柱=巳', d2&&d2.pillars[3][1]==='巳', d2?'时柱='+d2.pillars[3]+' useH='+d2.useH+' dst='+d2.dst:'null');
assert('D4 ctx.dst 标记=0', d2&&d2.dst===0, 'dst='+(d2&&d2.dst));

console.log('========== E. 时辰模式：跳过 DST + 真太阳时 ==========');
// 验收案例 A：1991-05-23 约 9 点多（按太阳位置 / 农活时间估算）→ 巳时
// 精确模式：10:00 是钟表时间 → DST −1h → 09:00 → 真太阳时 → 08:32 → 辰时
// 时辰模式：选巳时 → midpoint 10:00 是真太阳时 → 跳过所有校正 → 巳时
globalThis._inp = { gender:'男', year:'1991', month:'5', day:'23', timeMode:'exact', hour:'10', minute:'0', truesun:'yes', birthplace:'广州市' };
globalThis.generate();
let e1=globalThis.__getLast();
assert('E1 精确模式 1991-05-23 10:00 广州 → DST校正 → 辰时', e1&&e1.pillars[3][1]==='辰', e1?'时柱='+e1.pillars[3]+' dst='+e1.dst+' useH='+e1.useH:'null');
assert('E2 精确模式 dst=1（夏令时已校正）', e1&&e1.dst===1, 'dst='+(e1&&e1.dst));
assert('E3 精确模式 shichenMode=false', e1&&e1.shichenMode===false, 'shichenMode='+(e1&&e1.shichenMode));

globalThis._inp = { gender:'男', year:'1991', month:'5', day:'23', timeMode:'shichen', shichen:'巳', truesun:'yes', birthplace:'广州市' };
globalThis.generate();
let e2=globalThis.__getLast();
assert('E4 时辰模式 1991-05-23 巳时 → 跳过校正 → 巳时', e2&&e2.pillars[3][1]==='巳', e2?'时柱='+e2.pillars[3]+' dst='+e2.dst+' useH='+e2.useH:'null');
assert('E5 时辰模式 dst=0（未做夏令时校正）', e2&&e2.dst===0, 'dst='+(e2&&e2.dst));
assert('E6 时辰模式 shichenMode=true', e2&&e2.shichenMode===true, 'shichenMode='+(e2&&e2.shichenMode));
assert('E7 时辰模式时柱≠精确模式时柱', e1&&e2&&e1.pillars[3][1]!==e2.pillars[3][1], e1.pillars[3][1]+' vs '+e2.pillars[3][1]);

// 结果页提示验证
let solarHtml=(globalThis._els['rSolar'].innerHTML||'');
assert('E8 结果页显示"以时辰直接排盘"', solarHtml.indexOf('以时辰直接排盘')>=0, solarHtml.slice(0,50));
assert('E9 结果页不含"已自动校正夏令时"', solarHtml.indexOf('已自动校正夏令时')<0, solarHtml.slice(0,50));

// 对照：1992年（无DST）时辰模式与精确模式结果一致
globalThis._inp = { gender:'男', year:'1992', month:'5', day:'23', timeMode:'exact', hour:'10', minute:'0', truesun:'no', birthplace:'广州市' };
globalThis.generate();
let e3=globalThis.__getLast();
globalThis._inp = { gender:'男', year:'1992', month:'5', day:'23', timeMode:'shichen', shichen:'巳', truesun:'yes', birthplace:'广州市' };
globalThis.generate();
let e4=globalThis.__getLast();
assert('E10 1992无DST 精确模式(truesun=no)与时辰模式 时柱一致', e3&&e4&&e3.pillars[3][0]===e4.pillars[3][0], e3.pillars[3]+' vs '+e4.pillars[3]);

console.log(fails===0 ? '\n全部通过' : '\n失败 ' + fails + ' 项');
process.exit(fails===0?0:1);
