// 从 ui/index.html 提取 <script> 并校验核心排盘/五行/流年/合婚逻辑（node 运行）
// 真值来源：lunar-python（独立交叉验证）
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/../ui/index.html', 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if(!m){ console.error('未找到 script'); process.exit(1); }
let code = m[1];
const stub = 'var document={getElementById:()=>({value:"",textContent:"",innerHTML:"",style:{},classList:{add(){},remove(){}},onclick:null}),querySelectorAll:()=>[],querySelector:()=>null};var alert=()=>{};';
const expose = ';globalThis.NAYIN=NAYIN;globalThis.NAYIN_WX=NAYIN_WX;globalThis.CHONG=CHONG;globalThis.LIUHE=LIUHE;globalThis.SANHE=SANHE;globalThis.ZHI=ZHI;globalThis.matchRules=matchRules;globalThis.yearGZ=yearGZ;globalThis.analyzeHe=analyzeHe;globalThis.paipan=paipan;globalThis.dayGZ=dayGZ;globalThis.calcShenSha=calcShenSha;globalThis.getRemedy=getRemedy;globalThis.REMEDY=REMEDY;globalThis.SHENSHA=SHENSHA;globalThis.analyzeLiuDeep=analyzeLiuDeep;globalThis.WU_CHONG=WU_CHONG;globalThis.G60=G60;globalThis.CS_NAME=CS_NAME;globalThis.CS_BASE=CS_BASE;globalThis.calcKongWang=calcKongWang;globalThis.calcChangSheng=calcChangSheng;globalThis.calcTaiYuan=calcTaiYuan;globalThis.calcMingGong=calcMingGong;globalThis.calcShenGong=calcShenGong;globalThis.tenGod=tenGod;globalThis.LAST=null;';
eval(stub + code + expose);

function assert(name, cond){ console.log((cond?'  PASS ':'  FAIL ')+name); if(!cond) globalThis.__fail=true; }

console.log('== 四柱排盘校验（真值=lunar-python）==');
// 马云 1964-09-10 12:00（不校正）
let c1 = paipan('马云','男',1964,9,10,12,0,'北京市','no');
assert('马云年柱甲辰', c1.yg==='甲辰');
assert('马云月柱癸酉', c1.mg==='癸酉');
assert('马云日柱壬戌', c1.dg==='壬戌');
assert('马云时柱丙午', c1.hg==='丙午');
assert('马云日主壬水', c1.dayMaster==='壬' && c1.dmWx==='水');

console.log('== 晚子时（23:30 按次日日干起时）==');
let wz = paipan('晚子','男',1990,5,15,23,30,'上海市','no');
assert('晚子年柱庚午', wz.yg==='庚午');
assert('晚子月柱辛巳', wz.mg==='辛巳');
assert('晚子日柱庚辰', wz.dg==='庚辰');
assert('晚子时柱戊子', wz.hg==='戊子'); // 次日日干辛 → 戊子时

console.log('== 立春精确界（2020-02-04 17:03=立春时刻）==');
let ch = paipan('春','男',2020,2,4,17,3,'北京市','no');
assert('立春后年柱庚子', ch.yg==='庚子');
assert('立春月柱戊寅', ch.mg==='戊寅');
assert('立春日柱丁丑', ch.dg==='丁丑');

console.log('== 年界（1990-01-01 在立春前→己巳年）==');
let dn = paipan('冬','男',1990,1,1,8,0,'北京市','no');
assert('年初年柱己巳', dn.yg==='己巳');
assert('子月柱丙子', dn.mg==='丙子');
assert('日柱丙寅', dn.dg==='丙寅');
assert('时柱壬辰', dn.hg==='壬辰');

console.log('== 真太阳时校正（广州）==');
let gz = paipan('广州人','男',1990,1,1,10,0,'广州市','yes');
assert('广州真太阳时晚于北京约26.8分', Math.abs(gz.solarInfo.diffMin-(-26.8))<1.5);
assert('广州校正后约09:33', gz.solarInfo.time.getHours()===9 && gz.solarInfo.time.getMinutes()>=30 && gz.solarInfo.time.getMinutes()<=36);

console.log('== 藏干五行 + 身强身弱 ==');
assert('五行五维齐全', Object.keys(c1.five).length===5);
let sum=0; for(const k in c1.five) sum+=c1.five[k];
assert('五行总和>0', sum>0);
assert('身强身弱为三态之一', ['强','弱','中和'].includes(c1.strength));
assert('喜用神非空', c1.xiYong.length>0);
assert('格局字段存在', c1.pattern===null || typeof c1.pattern==='string');

console.log('== 断语匹配 ==');
let cats = matchRules(c1);
assert('性格命中>0', (cats['性格']||[]).length>0);
assert('事业命中>0', (cats['事业']||[]).length>0);
assert('格局命中>0', (cats['格局']||[]).length>0);

console.log('== 流年干支 ==');
assert('2026流年丙午', yearGZ(2026,7,1,12,0)==='丙午');
assert('2024流年甲辰', yearGZ(2024,7,1,12,0)==='甲辰');
assert('dayGZ(1900,1,1)=甲戌', dayGZ(1900,1,1)==='甲戌');

console.log('== 合婚评分 ==');
let b2 = paipan('乙方','女',1992,8,20,14,0,'上海市','no');
let rep = analyzeHe(c1, b2);
assert('合婚返回评分块', rep.indexOf('/ 100')>=0);
assert('合婚含日柱关系维度', rep.indexOf('日柱关系')>=0);
assert('合婚含综合评级', rep.indexOf('综合评级')>=0);
assert('合婚含生肖维度', rep.indexOf('生肖婚配')>=0);

console.log('== 纳音/地支关系表 ==');
assert('纳音60条', Object.keys(NAYIN).length===60);
assert('甲子海中金', NAYIN['甲子']==='海中金');
assert('纳音五行推导金', NAYIN_WX['甲子']==='金');
assert('子午冲', CHONG['子']==='午');
assert('子丑六合', LIUHE.some(p=>p[0]==='子'&&p[1]==='丑'));
assert('申子辰三合', SANHE.some(g=>g.join('')==='申子辰'));

console.log('== 神煞计算（真值=手工推演 马云 甲辰 癸酉 壬戌 丙午）==');
let ss = c1.shenSha;
assert('神煞总数=8', ss.length===8);
assert('含桃花(月柱酉)', (ss.find(s=>s.name==='桃花')||{}).pos==='月柱');
assert('含华盖(年柱/日柱)', ss.some(s=>s.name==='华盖') && (ss.find(s=>s.name==='华盖').pos.indexOf('年柱')>=0));
assert('含将星(时柱午)', (ss.find(s=>s.name==='将星')||{}).pos==='时柱');
assert('含灾煞(时柱午)', (ss.find(s=>s.name==='灾煞')||{}).pos==='时柱');
assert('含岁破(日柱戌)', (ss.find(s=>s.name==='岁破')||{}).pos==='日柱');
assert('含血刃(日柱戌)', (ss.find(s=>s.name==='血刃')||{}).pos==='日柱');
assert('含勾绞(时柱午)', (ss.find(s=>s.name==='勾绞')||{}).pos==='时柱');
assert('含天罗地网(男/日柱戌)', (ss.find(s=>s.name==='天罗地网')||{}).pos==='日柱');
assert('不含天乙贵人(甲/壬需丑未巳卯,命局无)', !ss.some(s=>s.name==='天乙贵人'));
assert('不含天德(酉月天德寅,命局无寅)', !ss.some(s=>s.name==='天德'));
assert('不含月德(酉月月德庚,命局无庚)', !ss.some(s=>s.name==='月德'));
const ssNames = ss.map(s=>s.name).sort().join(',');
const expSet = ['华盖','将星','勾绞','天罗地网','桃花','灾煞','血刃','岁破'].sort().join(',');
assert('神煞集合正确', ssNames===expSet);

console.log('== 神煞合成盘校验（验证天乙贵人/天德月德干支混合路径）==');
// 年干甲→丑未；年支丑、月支未 → 天乙贵人应在年柱、月柱
let ssSyn = calcShenSha([['甲','丑'],['乙','未'],['甲','寅'],['丙','子']], '男');
assert('合成盘含天乙贵人', ssSyn.some(s=>s.name==='天乙贵人'));
const tyPos=(ssSyn.find(s=>s.name==='天乙贵人')||{}).pos||'';
assert('合成盘天乙在年柱/月柱', tyPos.indexOf('年柱')>=0 && tyPos.indexOf('月柱')>=0);
// 天德/月德 干支混合（按天干匹配）：月支丑→天德庚(干)、月德庚(干)，盘含庚
let ssTiande = calcShenSha([['庚','子'],['辛','丑'],['庚','寅'],['壬','卯']], '男');
assert('天德(干庚)出现', ssTiande.some(s=>s.name==='天德'));
assert('月德(干庚)出现', ssTiande.some(s=>s.name==='月德'));
// 天德/月德 干支混合（按地支匹配）：月支卯→天德申(支)、月德甲(干)，盘含申(支)与甲(干)
let ssTiande2 = calcShenSha([['甲','子'],['乙','卯'],['甲','申'],['丙','寅']], '男');
assert('天德(支申)按地支出现', ssTiande2.some(s=>s.name==='天德'));
assert('月德(干甲)出现', ssTiande2.some(s=>s.name==='月德'));

console.log('== 五行补救（getRemedy 分支 + 调候）==');
assert('REMEDY 五维齐全', Object.keys(REMEDY).length===5);
let rmStrong = getRemedy('强', {木:1,火:1,土:1,金:1,水:1}, 1, ['金','水','木'], '午');
assert('强态取用神金水木(3项)', rmStrong.items.length===3 && rmStrong.items.map(i=>i.wx).join('')==='金水木');
assert('强态午月(夏)含调候补水提示', rmStrong.note.indexOf('水')>=0);
let rmMid = getRemedy('中和', {木:0.5,火:1,土:1,金:1,水:1}, 1, ['木','火','土','金','水'], '辰');
assert('中和态仅取最弱木(1项)', rmMid.items.length===1 && rmMid.items[0].wx==='木');
assert('中和态带中和说明', rmMid.note.indexOf('中和')>=0);
let rmWinter = getRemedy('强', {木:1,火:0.3,土:1,金:1,水:2}, 1, ['金','水'], '子');
assert('冬月子月喜用未含火但调候建议补火', rmWinter.note.indexOf('火')>=0);
assert('马云补救输出存在', c1.remedy && (c1.remedy.items.length>0 || c1.remedy.note));

console.log('== 流年深度规则（岁运并临/伏吟/反吟）==');
const deepCtx={pillars:[['甲','子'],['乙','丑'],['丙','寅'],['丁','卯']], xiYong:['木']};
// 岁运并临：流年甲子 == 大运甲子
let d1=analyzeLiuDeep(deepCtx,'甲','子','甲子');
assert('岁运并临命中', d1.some(r=>r.type==='binglin'));
assert('岁运并临判喜用(甲木为喜)', (d1.find(r=>r.type==='binglin').text.indexOf('喜用')>=0));
// 伏吟：流年甲子 与 年柱甲子 完全相同
let d2=analyzeLiuDeep(deepCtx,'甲','子','丙午');
assert('伏吟命中(年柱)', d2.some(r=>r.type==='fuyin' && r.title.indexOf('年柱')>=0));
// 反吟：流年甲子 天克地冲 年柱庚午（甲庚冲、子午冲）
let d3=analyzeLiuDeep({pillars:[['庚','午'],['乙','丑'],['丙','寅'],['丁','卯']], xiYong:[]},'甲','子','丙午');
assert('反吟命中(年柱)', d3.some(r=>r.type==='fanyin' && r.title.indexOf('年柱')>=0));
// 无匹配：流年丙午 与 四柱(甲乙丙丁/子丑寅卯) 无并临/伏吟/反吟
let d4=analyzeLiuDeep(deepCtx,'丙','午','戊申');
assert('无规则时不误报', d4.length===0);
// 天干相冲表
assert('甲庚冲', WU_CHONG['甲']==='庚');
assert('戊己非冲', WU_CHONG['戊']===undefined);

console.log('== 空亡（旬空）==');
// G60 六十甲子
assert('G60长度60', G60.length===60);
assert('G60[0]=甲子', G60[0]==='甲子');
assert('G60[59]=癸亥', G60[59]==='癸亥');
// 空亡计算：马云日柱壬戌 → 61-65? Let me find index. 甲子(0), 甲戌(10), 甲申(20), 甲午(30), 甲辰(40), 甲寅(50). 
// 壬戌 index = from 甲寅(50): 甲寅50,乙卯51,丙辰52,丁巳53,戊午54,己未55,庚申56,辛酉57,壬戌58,癸亥59. So 壬戌=58, 旬首=50(甲寅旬), 空亡=子(60%12=0),丑(61%12=1)
let kw1=calcKongWang('壬戌');
assert('壬戌日空亡子丑', kw1 && kw1.join('')==='子丑');
// 甲子日：甲子=0, 旬首=0(甲子旬), 空亡=戌(10%12=10),亥(11%12=11)
let kw2=calcKongWang('甲子');
assert('甲子日空亡戌亥', kw2 && kw2.join('')==='戌亥');
// 丙寅日：丙寅=2(甲子旬), 空亡=戌亥
let kw3=calcKongWang('丙寅');
assert('丙寅日空亡戌亥(同旬)', kw3 && kw3.join('')==='戌亥');
// 乙亥日：乙亥=11(甲戌旬), 旬首=10, 空亡=申(20%12=8),酉(21%12=9)
let kw4=calcKongWang('乙亥');
assert('乙亥日空亡申酉', kw4 && kw4.join('')==='申酉');
// 马云 ctx 带空亡
assert('马云排盘含kongWang', c1.kongWang && c1.kongWang.length===2);
assert('马云日柱壬戌空亡子丑', c1.kongWang.join('')==='子丑');

console.log('== 十二长生 ==');
// 甲阳木长生在亥: 亥长生,子沐浴,丑冠带,寅临官,卯帝旺,辰衰,巳病,午死,未墓,申绝,酉胎,戌养
assert('甲在亥=长生', calcChangSheng('甲','亥')==='长生');
assert('甲在寅=临官(禄)', calcChangSheng('甲','寅')==='临官');
assert('甲在卯=帝旺(刃)', calcChangSheng('甲','卯')==='帝旺');
assert('甲在午=死', calcChangSheng('甲','午')==='死');
// 乙阴木长生在午: 午长生,巳沐浴,辰冠带,卯临官,寅帝旺,丑衰,子病,亥死,戌墓,酉绝,申胎,未养
assert('乙在午=长生', calcChangSheng('乙','午')==='长生');
assert('乙在卯=临官', calcChangSheng('乙','卯')==='临官');
assert('乙在亥=死', calcChangSheng('乙','亥')==='死');
// 丙阳火长生在寅
assert('丙在寅=长生', calcChangSheng('丙','寅')==='长生');
assert('丙在午=帝旺', calcChangSheng('丙','午')==='帝旺');
// 庚阳金长生在巳
assert('庚在巳=长生', calcChangSheng('庚','巳')==='长生');
assert('庚在酉=帝旺', calcChangSheng('庚','酉')==='帝旺');
// 辛阴金长生在子: 子长生,亥沐浴,戌冠带,酉临官,申帝旺,未衰,午病,巳死,辰墓,卯绝,寅胎,丑养
assert('辛在子=长生', calcChangSheng('辛','子')==='长生');
assert('辛在申=帝旺', calcChangSheng('辛','申')==='帝旺');
assert('辛在巳=死', calcChangSheng('辛','巳')==='死');
// 壬阳水长生在申
assert('壬在申=长生', calcChangSheng('壬','申')==='长生');
assert('壬在子=帝旺', calcChangSheng('壬','子')==='帝旺');
// 癸阴水长生在卯: 卯长生,寅沐浴,丑冠带,子临官,亥帝旺,戌衰,酉病,申死,未墓,午绝,巳胎,辰养
assert('癸在卯=长生', calcChangSheng('癸','卯')==='长生');
assert('癸在亥=帝旺', calcChangSheng('癸','亥')==='帝旺');
assert('戊寄丙(同寅长生)', calcChangSheng('戊','寅')==='长生');
assert('己寄丁(同酉长生)', calcChangSheng('己','酉')==='长生');
// 马云日主壬水，日支戌 → 壬在戌=冠带
assert('马云壬在戌=冠带', calcChangSheng(c1.dayMaster, c1.dayZhi)==='冠带');

console.log('== 三式宫位（胎元·命宫·身宫）==');
// 胎元：月柱天干顺一、地支进三
assert('癸酉月→胎元甲子', calcTaiYuan('癸酉')==='甲子');
assert('甲寅月→胎元乙巳', calcTaiYuan('甲寅')==='乙巳');
// 马云：年甲辰 月癸酉 时丙午 → 命宫甲寅 身宫丙辰
assert('马云命宫甲寅', calcMingGong('甲辰','癸酉','丙午')==='甲寅');
assert('马云身宫丙辰', calcShenGong('甲辰','癸酉','丙午')==='丙辰');
// 马云排盘 ctx 含三式宫位
assert('马云ctx含胎元', c1.taiYuan && c1.taiYuan.length===2);
assert('马云ctx含命宫', c1.mingGong && c1.mingGong.length===2);
assert('马云ctx含身宫', c1.shenGong && c1.shenGong.length===2);
assert('马云胎元=甲子', c1.taiYuan==='甲子');
assert('马云命宫=甲寅', c1.mingGong==='甲寅');

console.log('== 特殊格局细分 ==');
// 马云身强(ratio>0.6) 但 maxWx不超60%→无专旺
assert('马云无专旺格', !c1.special.zhuanwang);
assert('马云无specialDetail', c1.specialDetail===null);
// 极端格局回归（v1.3.11 补）：此前这里只断言"字段存在"，从未验证专旺细分规则真的可达——
// 后果：pattern_专旺_水 长期缺失、木/火/金细分在 3.9 万盘网格 0 命中却无人发现。
// 下面两个样例盘经 24.4 万盘深搜确认可复现（配套门禁 tools/check_reachability.js）。
const zwMu = paipan('专旺木','男',1938,3,23,21,41,'','no');
assert('专旺·木（曲直格）', zwMu && zwMu.specialDetail==='专旺·曲直格', 'detail='+(zwMu&&zwMu.specialDetail));
const zwShui = paipan('专旺水','男',1948,11,23,0,17,'','no');
assert('专旺·水（润下格）', zwShui && zwShui.specialDetail==='专旺·润下格', 'detail='+(zwShui&&zwShui.specialDetail));
assert('specialDetail字段存在', c1.hasOwnProperty('specialDetail'));

console.log('== 十神真值表（防 tenGod 回归）==');
// 完整真值表：日主壬水(阳) × 10天干
const TENS_CASE=[['壬','比肩'],['癸','劫财'],['甲','食神'],['乙','伤官'],['丙','偏财'],['丁','正财'],['戊','七杀'],['己','正官'],['庚','偏印'],['辛','正印']];
TENS_CASE.forEach(([g,expect])=>{ assert('壬见'+g+'='+expect, tenGod(g,'水',true)===expect); });
// 日主乙木(阴) 抽查
const TENS_CASE2=[['乙','比肩'],['甲','劫财'],['丙','伤官'],['丁','食神'],['戊','正财'],['己','偏财'],['庚','正官'],['辛','七杀'],['壬','正印'],['癸','偏印']];
TENS_CASE2.forEach(([g,expect])=>{ assert('乙见'+g+'='+expect, tenGod(g,'木',false)===expect); });
// 实际命盘：马云 甲辰 癸酉 壬戌 丙午（日主壬水）→ 年干甲=食神、时干丙=偏财
assert('马云年干=食神', c1.tens[0]==='食神');
assert('马云月干=劫财', c1.tens[1]==='劫财');
assert('马云时干=偏财', c1.tens[3]==='偏财');
assert('马云日支本气十神=七杀', c1.dayZhiTG_ten==='七杀'); // 戌中戊土克壬水

console.log(globalThis.__fail ? '\n结果：存在 FAIL' : '\n结果：全部 PASS');
process.exit(globalThis.__fail?1:0);
