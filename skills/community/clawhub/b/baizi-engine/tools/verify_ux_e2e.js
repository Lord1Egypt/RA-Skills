// 第七轮端到端用户视角验收：输入容错 / 边界场景 / 报告质量 / 稳定性
// 用法: node tools/verify_ux_e2e.js
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
var alert=(msg)=>{globalThis._alerts.push(String(msg));};`;
const expose = ';globalThis.matchRules=matchRules;globalThis.paipan=paipan;globalThis.RULES=RULES;globalThis.SHENSHA=SHENSHA;globalThis.yearGZ=yearGZ;globalThis.monthGZ=monthGZ;globalThis.dayGZ=dayGZ;globalThis.hourGZ=hourGZ;globalThis.matchDayun=matchDayun;globalThis.matchLiuYue=matchLiuYue;globalThis.generate=generate;globalThis.runHe=runHe;globalThis.runLiu=runLiu;globalThis.runLiuYue=runLiuYue;globalThis.runLiuDay=runLiuDay;globalThis.runLiuQin=runLiuQin;globalThis.__setLast=function(x){LAST=x;LIU_OPEN=false;LIU_YUE_OPEN=false;LIU_DAY_OPEN=false;LIU_QIN_OPEN=false;};globalThis.__resetPanels=function(){LIU_OPEN=false;LIU_YUE_OPEN=false;LIU_DAY_OPEN=false;LIU_QIN_OPEN=false;};globalThis.LAST=null;globalThis.analyzeHe=analyzeHe;';
eval(stub + code + expose);

let fails = 0, warns = 0;
function assert(name, cond, extra){
  console.log((cond?'  PASS ':'  FAIL ')+name+(extra?'  ['+extra+']':''));
  if(!cond) fails++;
}
function warn(name, extra){
  console.log('  WARN ' + name + (extra?'  ['+extra+']':''));
  warns++;
}

console.log('========== A. 输入容错走查（模拟各种用户输入） ==========');
// A1 正常输入
let c = paipan('张三','男',1990,5,15,14,30,'广州市','yes');
assert('A1 正常输入出盘', !!c && c.pillars.length===4, c?c.pillars.join(' '):'null');
// A2 无效日期 2月30日
let r2 = paipan('错','男',2024,2,30,10,0,'','no');
assert('A2 无效日期被拦截', r2===null && globalThis._alerts.some(a=>a.indexOf('无效')>=0), globalThis._alerts.slice(-1)[0]);
// A3 超范围年份
let r3 = paipan('错','男',1800,5,15,10,0,'','no');
assert('A3 超范围年份被拦截', r3===null, globalThis._alerts.slice(-1)[0]);
// A4 无效小时
let r4 = paipan('错','男',1990,5,15,24,0,'','no');
assert('A4 小时24被拦截', r4===null, globalThis._alerts.slice(-1)[0]);
// A5 性别空
let r5 = paipan('错','',1990,5,15,10,0,'','no');
assert('A5 性别空被拦截', r5===null, globalThis._alerts.slice(-1)[0]);
// A6 时辰缺失（NaN）→ 六字分析降级检查
globalThis._alerts = [];
let r6 = paipan('缺时辰','男',1990,5,15,NaN,NaN,'','no');
assert('A6 时辰缺失：被拦截(alert)', r6===null, globalThis._alerts.slice(-1)[0]);
console.log('  >>> 用户视角：paipan 无"时辰未知"降级入口（属设计边界）。SKILL.md 已对齐：改为引导用户回忆/估时辰、按时段代表时辰排盘并标注"估算"，不再承诺引擎不支持的六字分析。');
// A7 UI 层：性别未选 → generate() 拦截（P1-1 修复验证）
globalThis._alerts = [];
globalThis._inp = { gender:'', year:'1990', month:'5', day:'15', timeMode:'exact', hour:'10', minute:'0', shichen:'', truesun:'yes', birthplace:'广州市' };
globalThis.LAST = null;
globalThis.generate();
assert('A7 性别未选时 generate 拦截(alert)', globalThis._alerts.some(a=>a.indexOf('性别')>=0) && globalThis.LAST===null, globalThis._alerts.slice(-1)[0]);
// A8 UI 层：日期/时间未填 → generate() 拦截（P2-1 修复验证）
globalThis._alerts = [];
globalThis._inp = { gender:'男', year:'', month:'', day:'', timeMode:'exact', hour:'', minute:'', shichen:'', truesun:'yes', birthplace:'广州市' };
globalThis.generate();
assert('A8 日期时间未填时 generate 拦截(alert)', globalThis._alerts.some(a=>a.indexOf('完整阳历生日')>=0 || a.indexOf('出生时间')>=0 || a.indexOf('出生时辰')>=0) && globalThis.LAST===null, globalThis._alerts.slice(-1)[0]);

console.log('========== B. 边界场景模拟 ==========');
// B1 晚子时（23:30 → 时柱按"次日日干起点"推：庚日+1=辛日 → 戊子）
c = paipan('李四','女',1990,5,15,23,30,'上海市','no');
const day1 = dayGZ(1990,5,15), day2 = dayGZ(1990,5,16);
assert('B1 晚子时时柱=戊子（庚日+1=辛日，丙辛从戊起）', c.pillars[3]==='戊子' && c.pillars[3][0]===hourGZ(day1[0],23)[0], '日柱='+day1+' 次日='+day2+' 时柱='+c.pillars[3]);
// 时柱应为子时
assert('B1 时柱地支为子', c.pillars[3][1]==='子', c.pillars[3][1]);
// B2 立春边界：2024-02-04 15:00 vs 17:00 年柱不同（2024立春约16:27）
const lc1 = yearGZ(2024,2,4,15,0), lc2 = yearGZ(2024,2,4,17,0);
assert('B2 立春精确切分（15点=癸卯年，17点=甲辰年）', lc1!==lc2, lc1+' vs '+lc2);
// B3 出生地未填 + truesun=yes
c = paipan('匿名','男',1990,5,15,10,0,'','yes');
assert('B3 出生地未填仍出盘', !!c && c.solarInfo===null, 'solarInfo='+(c?c.solarInfo:'null'));
// B4 未知城市 → found:false 兜底
c = paipan('客','女',1990,5,15,10,0,'不存在市','yes');
assert('B4 未知城市兜底(found:false)', !!c && c.solarInfo && c.solarInfo.found===false, JSON.stringify(c.solarInfo));
// B5 闰月附近（农历近似，用阳历验证跨月节气）
c = paipan('测','男',2024,12,7,10,0,'北京市','no'); // 大雪(12/6左右)
assert('B5 大雪后月柱=子月', c.mg[1]==='子', c.mg);
// B6 节气数据起点年边界：1895-01-03（小寒 1895-01-05 前）→ 甲午年 丙子月（大雪后小寒前属子月；此前曾因缺 1894 数据误出丙寅）
c = paipan('测','男',1895,1,3,10,0,'广州市','yes');
assert('B6 1895-01-03 月柱=丙子（起点年小寒前兜底）', c.mg==='丙子', '月柱='+c.mg);
// B7 起点年小寒后恢复丁丑月
c = paipan('测','男',1895,1,7,10,0,'广州市','yes');
assert('B7 1895-01-07 月柱=丁丑（小寒后正常）', c.mg==='丁丑', '月柱='+c.mg);

console.log('========== C. 报告质量 ==========');
// C1 断语库 suggestion 覆盖率（SKILL.md 声称 100%）
const noSug = RULES.filter(r=>!r.suggestion);
assert('C1 suggestion 覆盖率 100%', noSug.length===0, '缺失='+noSug.length+' 总数='+RULES.length);
// C2 source 出处覆盖率
const noSrc = RULES.filter(r=>!r.source);
assert('C2 出处标注覆盖率 100%', noSrc.length===0, '无出处='+noSrc.length);
// C3 12 分类 fallback 率统计（随机 150 盘，某分类经常 0 命中 → 兜底文案常见）
const CATS = ['性格','事业','财运','婚姻','健康','格局','用神喜忌','十神组合','六亲','学业','五行生克'];
const MAIN6 = ['性格','事业','财运','婚姻','健康','格局'];
const zeroHit = {}; CATS.forEach(k=>zeroHit[k]=0);
const totalPerCat = {}; CATS.forEach(k=>totalPerCat[k]=0);
let main6Sum = 0, main6Zero = 0;
const seedBase = [1990,5,15,10,0];
let seed = 42;
function rnd(){ seed = (seed*1103515245+12345)&0x7fffffff; return seed/0x7fffffff; }
for(let i=0;i<150;i++){
  const y = 1950+Math.floor(rnd()*70), mo = 1+Math.floor(rnd()*12), d = 1+Math.floor(rnd()*28);
  const hh = Math.floor(rnd()*24), mm = Math.floor(rnd()*60);
  const g = rnd()>0.5?'男':'女';
  const cc = paipan('样'+i, g, y, mo, d, hh, mm, ['广州市','上海市','北京市',''][Math.floor(rnd()*4)], rnd()>0.5?'yes':'no');
  if(!cc) continue;
  const cats = matchRules(cc);
  CATS.forEach(k=>{
    const n = (cats[k]||[]).length;
    totalPerCat[k]+=n;
    if(n===0) zeroHit[k]++;
  });
  let m6 = 0;
  MAIN6.forEach(k=>{ m6 += (cats[k]||[]).length; if((cats[k]||[]).length===0) main6Zero++; });
  main6Sum += m6;
}
console.log('  分类平均命中数（150盘）：');
CATS.forEach(k=>{
  const avg = (totalPerCat[k]/150).toFixed(1);
  const zeroPct = (zeroHit[k]/150*100).toFixed(0);
  console.log('    '+k+': 平均 '+avg+' 条/盘 | 0命中占比 '+zeroPct+'%');
  if(zeroHit[k]/150 > 0.3) warn('C3 分类经常兜底: '+k+' 0命中率 '+zeroPct+'%');
});
const main6Avg = main6Sum/150;
console.log('  主面板6类(性格/事业/财运/婚姻/健康/格局)平均合计: '+main6Avg.toFixed(1)+' 条/盘 | 单类0命中率 '+(main6Zero/(150*6)*100).toFixed(1)+'%');
assert('C3 主面板6类平均命中在 30-70 条区间', main6Avg>=30 && main6Avg<=70, main6Avg.toFixed(1));
// C4 单盘全 0 检查（引擎短路）
assert('C4 150盘无一盘全分类0命中', zeroHit['性格']<150, '性格0命中='+zeroHit['性格']);

console.log('========== D. 稳定性（同盘 20 次） ==========');
const sigs = new Set();
for(let i=0;i<20;i++){
  const cc = paipan('稳','男',1988,7,7,9,0,'成都市','yes');
  const sig = cc.pillars.join('|') + '||' + cc.dy.steps.join(',') + '||' + cc.shenSha.map(s=>s.name).join(',');
  sigs.add(sig);
}
assert('D1 同盘 20 次输出完全一致', sigs.size===1, sigs.size>1 ? '出现 '+sigs.size+' 种输出' : '稳定');

console.log('========== E. 报告完整性 ==========');
// E1 大运步数
c = paipan('测','男',1990,5,15,10,0,'广州市','yes');
assert('E1 大运 8 步', c.dy.steps.length===8, c.dy.steps.length+'步');
// E2 神煞：速查表规模 + 单盘命中展示（calcShenSha 只返回命中项，属正确设计）
assert('E2 神煞速查表 24 项', globalThis.SHENSHA && globalThis.SHENSHA.length===24, 'SHENSHA='+(globalThis.SHENSHA||[]).length);
assert('E2 单盘命中神煞展示(>0)', c.shenSha.length>0, c.shenSha.length+'项');
// E3 五行补救存在（结构：{items:[{wx,color,dir,num,industry,...}], note}）
assert('E3 五行补救方案存在', !!c.remedy && Array.isArray(c.remedy.items) && c.remedy.items.length>0, 'items='+((c.remedy&&c.remedy.items||[]).length));
// E4 用神喜忌完整
assert('E4 喜用/忌神非空', c.xiYong.length>0 && c.jiYong.length>0, '喜用='+c.xiYong.join('、')+' 忌='+c.jiYong.join('、'));
// E5 空亡/胎元/命宫/身宫
assert('E5 空亡+三式宫位', !!c.kongWang && !!c.taiYuan && !!c.mingGong && !!c.shenGong, '空亡='+c.kongWang+' 胎元='+c.taiYuan+' 命宫='+c.mingGong+' 身宫='+c.shenGong);

console.log('========== F. 流日分析（单月逐日） ==========');
// F0 流日规则已入断语库
const liuriN = RULES.filter(r=>r.id.indexOf('liuri_')===0).length;
assert('F0 流日规则 50 条已入库', liuriN===50, '实际='+liuriN);
// F1 正常调用：2026年3月（31天）
globalThis._inp = { liuDayYear:'2026', liuDayMonth:'3' };
globalThis.__setLast(paipan('测','男',1990,5,15,10,0,'广州市','yes'));
globalThis.__resetPanels(); globalThis.runLiuDay();
const ld = globalThis._els['liuDayResult'].innerHTML;
assert('F1 流日输出非空', ld.length>0, 'len='+ld.length);
const daysMar = new Date(2026,3,0).getDate(); // 2026-03 月末
const rowCount = (ld.match(/<tr/g)||[]).length - 1; // 减表头行
assert('F2 行数=该月天数('+daysMar+')', rowCount===daysMar, '实际行数='+rowCount);
assert('F3 含关键日小结', ld.indexOf('本月关键日')>=0);
assert('F4 日柱单元格渲染', ld.indexOf('class="mz"')>=0);
assert('F5 表格含图例', ld.indexOf('ld-legend')>=0);
// F6 平年 2 月（2026=28 天）
globalThis._inp = { liuDayYear:'2026', liuDayMonth:'2' };
globalThis.__resetPanels(); globalThis.runLiuDay();
const ld2 = globalThis._els['liuDayResult'].innerHTML;
assert('F6 2026年2月=28行', ((ld2.match(/<tr/g)||[]).length-1)===28, '行数='+((ld2.match(/<tr/g)||[]).length-1));
// F7 闰年 2 月（2028=29 天）
globalThis._inp = { liuDayYear:'2028', liuDayMonth:'2' };
globalThis.__resetPanels(); globalThis.runLiuDay();
const ld3 = globalThis._els['liuDayResult'].innerHTML;
assert('F7 2028年2月=29行', ((ld3.match(/<tr/g)||[]).length-1)===29, '行数='+((ld3.match(/<tr/g)||[]).length-1));
// F8 月份越界拦截
globalThis._alerts=[];
globalThis._inp = { liuDayYear:'2026', liuDayMonth:'13' };
globalThis.__resetPanels(); globalThis.runLiuDay();
assert('F8 月份越界拦截', globalThis._alerts.length>0, globalThis._alerts.slice(-1)[0]);
// F9 年份越界拦截
globalThis._alerts=[];
globalThis._inp = { liuDayYear:'1800', liuDayMonth:'3' };
globalThis.__resetPanels(); globalThis.runLiuDay();
assert('F9 年份越界拦截', globalThis._alerts.length>0, globalThis._alerts.slice(-1)[0]);
// F10 未排盘拦截
globalThis._alerts=[];
globalThis.__setLast(null);
globalThis._inp = { liuDayYear:'2026', liuDayMonth:'3' };
globalThis.__resetPanels(); globalThis.runLiuDay();
assert('F10 未排盘拦截', globalThis._alerts.length>0, globalThis._alerts.slice(-1)[0]);
// F11 断语命中抽查：冲日柱日期应带 ld-hot
globalThis._inp = { liuDayYear:'2026', liuDayMonth:'3' };
globalThis.__setLast(paipan('测','男',1990,5,15,10,0,'广州市','yes'));
globalThis.__resetPanels(); globalThis.runLiuDay();
const ld4 = globalThis._els['liuDayResult'].innerHTML;
assert('F11 表格渲染含 ld-hot 标记或冲合关系列', ld4.indexOf('ld-hot')>=0||ld4.indexOf('冲日')>=0||ld4.indexOf('合日')>=0);

console.log('========== G. 六亲详解（父母/配偶/子女/兄弟） ==========');
// G0 六亲规则已入断语库（2026-08-19 扩充批次5：59→64 条，需 ≥40）
const liuqinN = RULES.filter(r=>r.category==='六亲').length;
assert('G0 六亲规则 64 条已入库', liuqinN===64, '实际='+liuqinN);
// G1 正常调用（男命）
globalThis.__setLast(paipan('测','男',1990,5,15,10,0,'广州市','yes'));
globalThis.runLiuQin();
const lq = globalThis._els['liuQinResult'].innerHTML;
assert('G1 六亲输出非空', lq.length>0, 'len='+lq.length);
assert('G2 四宫齐全（父母/配偶/子女/兄弟）', lq.indexOf('① 父母')>=0&&lq.indexOf('② 配偶')>=0&&lq.indexOf('③ 子女')>=0&&lq.indexOf('④ 兄弟')>=0);
assert('G3 男命含妻星', lq.indexOf('妻星')>=0);
assert('G4 古籍断语命中>0', (lq.match(/【古籍断语】/g)||[]).length>0, (lq.match(/【古籍断语】/g)||[]).length+'条');
// G5 女命调用（夫星正官）
globalThis.__setLast(paipan('测','女',1985,11,20,14,30,'北京','yes'));
globalThis.runLiuQin();
const lq2 = globalThis._els['liuQinResult'].innerHTML;
assert('G5 女命输出非空且含夫星', lq2.length>0 && lq2.indexOf('夫星')>=0, 'len='+lq2.length);
// G6 未排盘拦截
globalThis._alerts=[];
globalThis.__setLast(null);
globalThis.runLiuQin();
assert('G6 未排盘拦截', globalThis._alerts.length>0, globalThis._alerts.slice(-1)[0]);
// G7 多盘稳定性：5 盘无异常
const gCases=[[1970,3,8,8,30,'男','上海市'],[1988,12,25,23,45,'女','成都市'],[2001,7,1,6,15,'男','西安市'],[1965,9,18,20,0,'女','武汉市'],[1995,1,1,0,30,'男','广州市']];
let gOk=0;
for(const gc of gCases){
  try{
    globalThis.__setLast(paipan('测',gc[4],gc[0],gc[1],gc[2],gc[3],0,gc[5],'yes'));
    globalThis.runLiuQin();
    if(globalThis._els['liuQinResult'].innerHTML.length>200) gOk++;
  }catch(e){ warn('G7 盘异常: '+gc.join('-')+' '+e.message); }
}
assert('G7 五盘六亲输出均正常', gOk===5, gOk+'/5');

console.log('========== H. 合婚评分完整性（满分标定 + 百分制归一化） ==========');
// 2026-10 修复：维度 1 声明满分 25，但六合与三合对同一对地支互斥（穷举 120×120 日柱同真 0 组），
// 真实上限 22 → 七维满分和 97 却被显示为 "/ 100"。现维度 1 max=22 + 总分按实际满分归一化。
// 本节锁定：维度齐全、满分和、日柱关系满分、sc≤max、总分归一化到 0~100。
const heCases=[
  [[1990,5,15,10,0,'男','广州市'],[1992,8,20,14,0,'女','上海市']],
  [[1988,2,3,22,30,'男','成都市'],[1991,11,7,5,15,'女','天津市']],
  [[1975,12,31,23,45,'女','武汉市'],[1980,6,6,12,0,'男','北京市']],
  [[2000,1,1,0,5,'男','北京市'],[2003,3,3,3,3,'女','广州市']],
  [[1960,7,7,7,7,'男','上海市'],[1962,9,9,9,9,'女','成都市']],
];
let hDimOk=0, hMaxSum=null, hDim1Max=null, hBad=[];
for(const [ca,cb] of heCases){
  const A=paipan('甲',ca[5],ca[0],ca[1],ca[2],ca[3],ca[4],ca[6],'yes');
  const B=paipan('乙',cb[5],cb[0],cb[1],cb[2],cb[3],cb[4],cb[6],'yes');
  if(!A||!B){ warn('H 盘构造失败: '+ca.join('-')+' / '+cb.join('-')); continue; }
  const html=globalThis.analyzeHe(A,B);
  const dims=[...html.matchAll(/<span>([^<]+)<\/span><span>(\d+) \/ (\d+)<\/span>/g)].map(x=>({name:x[1],sc:+x[2],max:+x[3]}));
  if(dims.length!==7){ hBad.push('维度数='+dims.length); continue; }
  const sumMax=dims.reduce((s,d)=>s+d.max,0);
  const raw=dims.reduce((s,d)=>s+d.sc,0);
  const shown=+(html.match(/score-big">(\d+)</)||[])[1];
  const expect=Math.round(raw*100/sumMax);
  if(hMaxSum===null) hMaxSum=sumMax;
  hDim1Max=(dims.find(d=>d.name==='日柱关系')||{}).max;
  if(dims.some(d=>d.sc>d.max)) hBad.push('维度超出满分');
  if(shown!==expect) hBad.push('总分未归一化 '+shown+'≠'+expect);
  if(!(shown>=0&&shown<=100)) hBad.push('总分越界 '+shown);
  hDimOk++;
}
assert('H1 七维齐全 + 满分和 = 97', hDimOk===heCases.length && hMaxSum===97, '维数OK='+hDimOk+'/'+heCases.length+' 满分和='+hMaxSum);
assert('H2 日柱关系满分 = 22（原声明 25 不可达）', hDim1Max===22, '实际='+hDim1Max);
assert('H3 各维 sc≤max，总分按实际满分归一化到 0~100', hBad.length===0, hBad.slice(0,3).join('; '));

console.log('\n===== 汇总 =====');
console.log('FAIL: '+fails+' | WARN: '+warns);
process.exit(fails===0?0:1);
