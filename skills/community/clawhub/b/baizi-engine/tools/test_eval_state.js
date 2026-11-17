// 回归测试：状态条件引擎（evalState）+ 缺失字段引用 + 文本/逻辑瑕疵修复
// 覆盖 Task #92-94 的修复点，防止回退
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/../ui/index.html', 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if(!m){ console.error('未找到 script'); process.exit(1); }
let code = m[1];
const stub = 'var document={getElementById:()=>({value:"",textContent:"",innerHTML:"",style:{},classList:{add(){},remove(){}},onclick:null}),querySelectorAll:()=>[],querySelector:()=>null,documentElement:{style:{}}};var alert=()=>{};var getComputedStyle=()=>({getPropertyValue:()=>""});';
const expose = ';globalThis.paipan=paipan;globalThis.matchRules=matchRules;globalThis.evalState=evalState;globalThis.RULES=RULES;globalThis.drawWxBar=drawWxBar;globalThis.drawBalance=drawBalance;globalThis.drawDayunTrend=drawDayunTrend;globalThis.getMonthBrief=getMonthBrief;globalThis.analyzeLiuDeep=analyzeLiuDeep;globalThis.GAN_WX_OfTen=GAN_WX_OfTen;globalThis.GAN_WX=GAN_WX;globalThis.JIEQI=JIEQI;';
eval(stub + code + expose);

let fails = 0;
function assert(name, cond, extra){
  if(cond){ console.log('  PASS  ' + name + (extra?'  ['+extra+']':'')); }
  else { console.log('  FAIL  ' + name); fails++; }
}

// 测试命盘（与 test_ui.js 相同的真值盘）
const c1 = paipan('马云','男',1964,9,10,12,0,'北京市','no');      // 壬戌日/丙午时，日主壬水
const wz = paipan('晚子','男',1990,5,15,23,30,'上海市','no');     // 庚辰日/戊子时，日主庚金
const ch = paipan('春','男',2020,2,4,17,3,'北京市','no');         // 丁丑日，日主丁火
const dn = paipan('冬','男',1990,1,1,8,0,'北京市','no');          // 丙寅日/壬辰时，日主丙火
const charts = [c1, wz, ch, dn];

function matchedIds(ctx){
  const ids=[];
  const cats=matchRules(ctx);
  for(const k in cats){ cats[k].forEach(r=>ids.push(r.id)); }
  return ids;
}

console.log('== A. 5条曾"无条件命中所有命盘"的规则应产生区分度 ==');
['marriage_richouse_xi','marriage_richouse_ji','pattern_yongshen_chong','pattern_yongshen_jia','marriage_bijie_duo'].forEach(rid=>{
  const hit = charts.filter(ctx=>matchedIds(ctx).includes(rid)).length;
  assert(rid+' 不再全量命中', hit<4, hit+'/4盘命中（0-3为有区分度）');
});

console.log('== B. evalState 运行时真判断 ==');
// 身旺：仅 strength==='强' 命中
assert('evalState(身旺)===strength为强', evalState('身旺',{日主:'庚金'},wz)===(wz.strength==='强'), 'wz.strength='+wz.strength);
assert('evalState(身旺)对马云盘', evalState('身旺',{日主:'壬水'},c1)===(c1.strength==='强'), 'c1.strength='+c1.strength);
// 为用神有力：十神五行属喜用且分值>=均值
{
  const t='正官'; const w=GAN_WX_OfTen(t,c1);
  const expect = c1.xiYong.includes(w) && c1.five[w]>=c1.avgFive;
  assert('evalState(为用神有力/正官)按喜用+力量判断', evalState('为用神有力',{十神:'正官'},c1)===expect, '正官五行='+w+' expect='+expect);
}
// 为喜用/为忌神（日支本气）
{
  const dwx=GAN_WX[ch.dayZhiTG];
  assert('evalState(为喜用/日支)', evalState('为喜用',{位置:'日支'},ch)===ch.xiYong.includes(dwx));
  assert('evalState(为忌神/日支)', evalState('为忌神',{位置:'日支'},ch)===ch.jiYong.includes(dwx));
}
// 桃花：必须有桃花神煞才命中（位置非日支时不限位置）
assert('evalState(桃花)需神煞存在', evalState('桃花',{},c1)===Boolean(c1.shenSha&&c1.shenSha.some(s=>s.name==='桃花')), 'c1桃花='+(c1.shenSha||[]).filter(s=>s.name==='桃花').length);
// 未知状态 → 不命中（防止静默放行）
assert('evalState(未知状态)不命中', evalState('某未知状态',{},c1)===false);
// 重重：直接验证返回值类型与语义（比劫计数逻辑在 evalState 内）
{
  const hit = evalState('重重',{十神:['比肩','劫财']},c1);
  assert('evalState(重重)有明确布尔结果', typeof hit==='boolean', '='+hit);
}
// 偏枯有药：阈值已收紧（旺≥1.8×avg 且 弱≤0.4×avg），不能人人命中
{
  const n = charts.filter(ctx=>evalState('偏枯有药',{},ctx)).length;
  assert('evalState(偏枯有药)有区分度', n<3, n+'/4盘命中（收紧阈值后应少数命中）');
}
// 财官位置：年月/日时需天干透出（藏而不透不命中）——防止命中率回归 80%+
{
  const srcB = fs.readFileSync(__dirname + '/../tools/build_ui.py', 'utf8');
  assert('位置年月/日时 仅匹配天干透出', srcB.indexOf("pool=[ctx.tens[0],ctx.tens[1]]")>=0 && srcB.indexOf("pool=[ctx.tens[3]]")>=0);
  // 2026-10（v1.3.20）日时池不再含日干：日干对自身恒为"比肩"，计入会让含"比肩"的条件恒真
  assert('日时池排除日干（不含 ctx.tens[2] 的比肩）', srcB.indexOf("pool=[ctx.tens[2],ctx.tens[3]]")<0);
  assert('十神键默认池排除日干（年/月/时三干）', srcB.indexOf("let pool=[ctx.tens[0],ctx.tens[1],ctx.tens[3]];")>=0);
  assert('evalState 计数池排除日干', srcB.indexOf("const allTens=[ctx.tens[0],ctx.tens[1],ctx.tens[3]];")>=0);
}

console.log('== C. 缺失字段引用修复 ==');
assert('ctx.sumFive 存在', typeof c1.sumFive==='number' && c1.sumFive>0);
const bar = drawWxBar(c1);
assert('drawWxBar 不含 NaN', bar.indexOf('NaN')===-1);
assert('drawWxBar 输出百分比', /\d+%/.test(bar));
const bal = drawBalance(c1);
assert('drawBalance 不含 NaN', bal.indexOf('NaN')===-1);
assert('drawBalance 忌神显示 jiYong', (c1.jiYong||[]).length===0 || bal.indexOf(c1.jiYong.join('、'))>=0);
assert('drawBalance 调候显示 special.tiaohouEls', ((c1.special&&c1.special.tiaohouEls)||[]).length===0 || bal.indexOf(c1.special.tiaohouEls.join('、'))>=0);
// getMonthBrief：忌神当令分支可走（ctx.jiYong 存在）
const brief = getMonthBrief(c1.mg, c1.tens[1], c1);
assert('getMonthBrief 正常输出', typeof brief==='string' && brief.length>0);

console.log('== D. 文本/逻辑瑕疵修复 ==');
assert('drawDayunTrend 图例已修正', drawDayunTrend(c1).indexOf('实线=喜用')===-1);
// 岁运并临去重：runLiu 中不再调用 伏吟 规则（analyzeLiuDeep 统一输出）
const src = fs.readFileSync(__dirname + '/../tools/build_ui.py', 'utf8');
assert('liunian_岁运并临_伏吟 不再被 findRule 调用', src.indexOf("findRule('liunian_岁运并临_伏吟')")===-1);
// 岁运并临仍由 analyzeLiuDeep 输出
const dyGz = c1.dy.steps[0];
const deep = analyzeLiuDeep(c1, dyGz[0], dyGz[1], dyGz);
assert('analyzeLiuDeep 岁运并临正常输出', deep.some(r=>r.type==='binglin'));
// 刑检测改双向（源级校验）
assert('流年刑检测已改双向', src.indexOf("(pr[0]===lz&&pr[1]===z)||(pr[0]===z&&pr[1]===lz)")>=0);
assert('调候文本无冗余拼接', src.indexOf("join('调候则命局寒暖燥湿平衡、生机不滞。')")===-1);

console.log('== E. 否决键语义（组合=必须存在，否决=必须不存在）==');
{
  // combo_全无财星：纯否决 → 天干无财星才有区分度（不能 0% 也不能 100%）
  const hits = charts.filter(ctx=>matchedIds(ctx).includes('combo_全无财星')).length;
  assert('combo_全无财星 有区分度', hits>0 && hits<charts.length, hits+'/'+charts.length+'盘命中');
  // 组合键不再被否决反转
  assert('否决键不反转组合键', src.indexOf("if(!c.否决){ const arr=Array.isArray(v)?v:[v]")===-1);
  assert('否决键支持数组与true', src.indexOf("Array.isArray(c.否决)?c.否决:(Array.isArray(c.组合)?c.组合:[])")>=0);
  // 官星一位（有正官无七杀）：不能 4/4 全命中（防回归），4 盘样本小允许 0 命中
  const one = charts.filter(ctx=>matchedIds(ctx).includes('combo_官星一位')).length;
  assert('combo_官星一位 不全量命中', one<charts.length, one+'/'+charts.length+'盘命中');
}

console.log('== F. P0 输入校验（非法输入拦截）==');
{
  const bad = [
    ['月=13', ()=>paipan('T','男',1990,13,15,10,30,'','no')],
    ['2月31日', ()=>paipan('T','男',1990,2,31,10,30,'','no')],
    ['时=25', ()=>paipan('T','男',1990,5,15,25,30,'','no')],
    ['分=70', ()=>paipan('T','男',1990,5,15,10,70,'','no')],
    ['性别=未知', ()=>paipan('T','未知',1990,5,15,10,30,'','no')],
    ['年份越界', ()=>paipan('T','男',JIEQI.range[1]+1,5,15,10,30,'','no')],
  ];
  bad.forEach(([name,fn])=>{
    let r; try{ r=fn(); }catch(e){ r='throw:'+e.message; }
    assert('拦截 '+name, r===null, r===null?'ok':'→ 未拦截');
  });
  // 合法输入 + 边界值正常
  assert('合法输入正常', paipan('T','男',1990,5,15,10,30,'','no')!==null);
  assert('年份下边界正常', paipan('T','男',JIEQI.range[0],1,1,0,0,'','no')!==null);
  assert('年份上边界正常', paipan('T','男',JIEQI.range[1],12,31,23,59,'','no')!==null);
}

console.log('== G. 月劫格 condition 修复 ==');
{
  const db = JSON.parse(fs.readFileSync(__dirname + '/../kb/04-rules-db/rules.json','utf8'));
  const yj = db.rules.find(r=>r.id==='pattern_月劫格');
  assert('月劫格 condition 为 格局=月劫格', yj && yj.condition['格局']==='月劫格', JSON.stringify(yj?yj.condition:null));
  const jl = db.rules.find(r=>r.id==='pattern_建禄格');
  assert('建禄格 condition 为 格局=建禄格', jl && jl.condition['格局']==='建禄格');
}

console.log('\n结果: ' + (fails? fails+' FAIL':'全部 PASS'));
process.exit(fails?1:0);
