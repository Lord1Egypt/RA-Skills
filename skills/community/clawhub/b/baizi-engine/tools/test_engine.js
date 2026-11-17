// 验证独立引擎库 engine/engine.dist.js 在 Node 下可直接使用（C 端复用入口）
// 覆盖：排盘、断语匹配、神煞、大运、流年深度、流月、流日、夏令时、真太阳时、数据表完整性
const BaziEngine = require('../engine/engine.dist.js');

let pass = 0, fail = 0;
function assert(name, cond, extra){
  if(cond){ pass++; console.log('  PASS ' + name); }
  else { fail++; console.log('  FAIL ' + name + (extra?('  ['+extra+']'):'')); }
}

console.log('== 独立库加载 ==');
assert('module.exports 为对象', typeof BaziEngine === 'object' && BaziEngine !== null);
// 2026-08-19 修复（工具链审计）：原断言 try{return true} 恒真，改真实检查 dist 源码不含 DOM 引用
const fs = require('fs');
const distSrc = fs.readFileSync(__dirname + '/../engine/engine.dist.js', 'utf8');
assert('dist 不引用 DOM（document/getElementById）', !/document\.|getElementById/.test(distSrc));

console.log('== 核心排盘（真值=lunar-python 马云盘）==');
const c1 = BaziEngine.paipan('马云','男',1964,9,10,12,0,'北京市','no');
assert('四柱 甲辰/癸酉/壬戌/丙午', c1.yg==='甲辰'&&c1.mg==='癸酉'&&c1.dg==='壬戌'&&c1.hg==='丙午');
assert('日主壬水', c1.dayMaster==='壬' && c1.dmWx==='水');
assert('大运 8 步', c1.dy.steps.length===8);
assert('神煞 8 项', (c1.shenSha||[]).length===8);
assert('空亡 子丑', (c1.kongWang||[]).join()==='子,丑');
assert('藏干五行五维', Object.keys(c1.five).length===5);

console.log('== 断语匹配 ==');
const cats = BaziEngine.matchRules(c1);
const total = Object.values(cats).reduce((s,a)=>s+a.length,0);
assert('命中分类非空', Object.keys(cats).length>=8);
assert('总断语数>10', total>10, 'total='+total);

console.log('== 夏令时校正 ==');
const d1 = BaziEngine.applyDst(1986,7,15,10);
assert('1986 窗口内 −1 小时', d1.hh===9 && d1.dst===1);
const d2 = BaziEngine.applyDst(1992,7,15,10);
assert('1992 无夏令时', d2.hh===10 && d2.dst===0);
const d3 = BaziEngine.applyDst(1986,9,13,0);
assert('跨天回退一日', d3.d===12 && d3.hh===23);

console.log('== 真太阳时 ==');
const gz = BaziEngine.paipan('广州人','男',1990,1,1,10,0,'广州市','yes');
assert('广州校正后约09:33', gz.solarInfo.time.getHours()===9 && gz.solarInfo.time.getMinutes()>=30 && gz.solarInfo.time.getMinutes()<=36);

console.log('== 流年深度规则 ==');
const deep = BaziEngine.analyzeLiuDeep(c1, '甲', '辰', '庚午');
assert('伏吟·年柱命中（甲辰流年=甲辰年柱）', deep.some(r=>r.type==='fuyin'));

console.log('== 大运/流月/流日规则匹配器可用 ==');
assert('matchDayun 返回数组', Array.isArray(BaziEngine.matchDayun(c1, c1.dy.steps[0])));
assert('matchLiuYue 为函数', typeof BaziEngine.matchLiuYue==='function');
assert('matchLiuDay 为函数', typeof BaziEngine.matchLiuDay==='function');

console.log('== 时辰映射 & 数据表 ==');
assert('SHI_CHEN_MAP 子时→0:00', BaziEngine.SHI_CHEN_MAP['子'][0]===0);
assert('SHI_CHEN_MAP 亥时→22:00', BaziEngine.SHI_CHEN_MAP['亥'][0]===22);
assert('RULES 共 1001 条', BaziEngine.RULES.length===1001, 'len='+BaziEngine.RULES.length);
assert('JIEQI 覆盖 206 年', Object.keys(BaziEngine.JIEQI.data).length===206, 'len='+Object.keys(BaziEngine.JIEQI.data).length);
assert('SHENSHA 24 项', BaziEngine.SHENSHA.length===24);
assert('NAYIN 60 条', Object.keys(BaziEngine.NAYIN).length===60);
assert('CITY_LON 含广州', !!BaziEngine.CITY_LON['广州']);
// 2026-08-28 CITY_LON 扩充至 724 城（345 地级市 + 379 县级市）：关键县级市防回退断言
assert('CITY_LON 共 724 城', Object.keys(BaziEngine.CITY_LON).length===724, 'len='+Object.keys(BaziEngine.CITY_LON).length);
assert('CITY_LON 含黄冈(地级)', BaziEngine.CITY_LON['黄冈']===114.9, '黄冈='+BaziEngine.CITY_LON['黄冈']);
assert('CITY_LON 含义乌市(县级)', BaziEngine.CITY_LON['义乌市']===120.1, '义乌市='+BaziEngine.CITY_LON['义乌市']);
assert('CITY_LON 含昆山市(县级)', BaziEngine.CITY_LON['昆山市']===121, '昆山市='+BaziEngine.CITY_LON['昆山市']);
assert('CITY_LON 含神木市(县级)', BaziEngine.CITY_LON['神木市']===110.3, '神木市='+BaziEngine.CITY_LON['神木市']);
assert('CITY_LON 含喀什(西部)', BaziEngine.CITY_LON['喀什']===75.9, '喀什='+BaziEngine.CITY_LON['喀什']);
// 匹配逻辑：最长名称优先 + 去"市"后缀兼容（填"义乌"命中"义乌市"）
const yw = BaziEngine.paipan('测试','男',1990,6,1,14,0,'义乌','yes');
assert('填"义乌"命中义乌市 120.1°', yw.solarInfo && yw.solarInfo.found && yw.solarInfo.lon===120.1, JSON.stringify(yw.solarInfo));
const yid = BaziEngine.paipan('测试','男',1990,6,1,14,0,'湖北省宜昌市宜都市','yes');
assert('最长匹配:宜都市(111.4)优先于宜昌', yid.solarInfo && yid.solarInfo.found && yid.solarInfo.lon===111.4, JSON.stringify(yid.solarInfo));
assert('findRule 可用', BaziEngine.findRule('liuyue_01')!==null);
assert('getRemedy 可用', BaziEngine.getRemedy('弱', c1.five, c1.avgFive, c1.xiYong, c1.pillars[1][1]).items!==undefined);

console.log('== 五行补救 ==');
const rem = BaziEngine.getRemedy('弱', c1.five, c1.avgFive, c1.xiYong, c1.pillars[1][1]);
assert('弱态按喜用神输出补救项', rem.items.length>0 && rem.note.length>0);

console.log('== 2026-10 修复回归 ==');
// ① "天津市"经度曾被"津市市"(111.9°) 抢占（匹配时比较的是"键长"而非"实际命中串长"），正确应为 天津 117.2°
const tj = BaziEngine.paipan('测试','男',1990,6,1,14,0,'天津市','yes');
assert('填"天津市"解析为天津 117.2°（不被津市市抢占）', tj.solarInfo && tj.solarInfo.lon===117.2, JSON.stringify(tj.solarInfo));
const tjq = BaziEngine.paipan('测试','男',1990,6,1,14,0,'天津市和平区','yes');
assert('填"天津市和平区"同样解析为 117.2°', tjq.solarInfo && tjq.solarInfo.lon===117.2, JSON.stringify(tjq.solarInfo));
// ② 可克达拉市经度修正（原 90.9 与所在伊犁地区邻市 80.5~85 矛盾，偏东约 10.2°≈41 分钟）
assert('CITY_LON 可克达拉市≈80.7', Math.abs(BaziEngine.CITY_LON['可克达拉市']-80.7)<0.001, 'v='+BaziEngine.CITY_LON['可克达拉市']);
// ③ 真太阳时校正把日期推出节气库范围时应安全返回 null，不得抛异常
let cyThrew=false, cyNull=false;
try { const r=BaziEngine.paipan('测试','男',1895,1,1,1,0,'喀什','yes'); cyNull=(r===null); } catch(e){ cyThrew=true; }
assert('1895-01-01 喀什 真太阳时跨年 → 返回 null 不抛异常', !cyThrew && cyNull, 'threw='+cyThrew);
// ④ 勾绞在"子年"不再丢失（ZHI[(0-1+12)%12] 曾产生 undefined）
const gz08 = BaziEngine.paipan('测试','男',2008,6,28,22,0,'北京市','no');
assert('2008 戊子年神煞含勾绞（子年支越界修复）', (gz08.shenSha||[]).some(s=>s.name==='勾绞'), (gz08.shenSha||[]).map(s=>s.name).join(','));
// ⑤ 专旺格须"主导五行 == 日主五行"（曾把日主癸水、金旺的盘标成"专旺·从革格"）
const WX5=['木','火','土','金','水'];
let zwSeen=0, zwBad=0;
for(let i=0;i<3000;i++){
  const y=1950+(i*7)%150, m=1+(i*5)%12, d=1+(i*11)%28, hh=i%24, mm=(i*13)%60;
  const c=BaziEngine.paipan('T', i%2?'男':'女', y,m,d,hh,mm,'北京市','no');
  if(!c) continue;
  const f=c.five, mx=Math.max(...WX5.map(k=>f[k])), dom=WX5.find(k=>f[k]===mx);
  if(c.special && c.special.zhuanwang){ zwSeen++; if(dom!==c.dmWx) zwBad++; }
}
assert('专旺格主导五行恒等于日主五行（3000 盘抽样）', zwBad===0, 'zwSeen='+zwSeen+' zwBad='+zwBad);
// ⑥ 极端边界年：起运不再静默算 0 岁，而是标记 valid=false 供 UI 提示
const edge = BaziEngine.paipan('T','男',2100,12,31,12,0,'北京市','no');
assert('2100 年末起运标记 valid=false（不再静默 0 岁）', edge && edge.dy && edge.dy.valid===false, edge?JSON.stringify({v:edge.dy.valid,age:Math.round(edge.dy.startAge*100)/100}):'null');

console.log('== 排盘失败可读诊断（v1.3.12）==');
// ⑦ 回归自真实对接事故：applyDst 原先不返回 mm，调用方写 paipan(...,d.mm,...) 得到 undefined
//    → Number(undefined)=NaN → 校验失败返回 null（静默）→ 调用方堆栈落在后一行"Cannot read properties of null"
const dd = BaziEngine.applyDst(1986,7,15,10,30);
assert('applyDst 透传分钟 mm=30', dd.mm===30, JSON.stringify(dd));
assert('applyDst 结果可直接喂 paipan（v1.3.12 前此处必为 null）',
  BaziEngine.paipan('夏令时链路','男',dd.y,dd.m,dd.d,dd.hh,dd.mm,'广州市','no') !== null);
assert('applyDst 不传 mm 时默认 0', BaziEngine.applyDst(1992,7,15,10).mm===0, JSON.stringify(BaziEngine.applyDst(1992,7,15,10)));
// ⑧ 校验失败必须留下可读原因（原实现 Node 下只调 no-op alert 后 return null，原因彻底丢失）
assert('paipan 非法月份仍返回 null（旧契约不变）', BaziEngine.paipan('T','男',1990,13,15,10,30,'','no')===null);
assert('getLastError 记录 code=INVALID_MONTH', (BaziEngine.getLastError()||{}).code==='INVALID_MONTH', JSON.stringify(BaziEngine.getLastError()));
assert('getLastError 消息可读（含"月份"）', /月份/.test((BaziEngine.getLastError()||{}).message||''));
assert('getLastError 带 detail 上下文', (BaziEngine.getLastError()||{}).detail && BaziEngine.getLastError().detail.m===13, JSON.stringify(BaziEngine.getLastError().detail));
assert('getLastError 记录 INVALID_DATE（2/30）', (BaziEngine.paipan('T','男',2024,2,30,10,0,'','no')===null) && BaziEngine.getLastError().code==='INVALID_DATE');
assert('getLastError 记录 YEAR_OUT_OF_RANGE', (BaziEngine.paipan('T','男',1800,1,1,12,0,'','no')===null) && BaziEngine.getLastError().code==='YEAR_OUT_OF_RANGE');
// ⑨ paipanStrict：同样的诊断信息，但 fail-fast 抛错（服务端推荐入口）
let strictCode='', strictMsg='';
try { BaziEngine.paipanStrict('T','男',1990,5,15,10,70,'','no'); } catch(e){ strictCode=e.code; strictMsg=e.message; }
assert('paipanStrict 参数非法时抛错', strictCode==='INVALID_MINUTE', 'code='+strictCode);
assert('paipanStrict 错误消息可读', /分钟/.test(strictMsg), strictMsg);
assert('paipanStrict 合法输入正常返回 ctx', BaziEngine.paipanStrict('T','男',1990,5,15,10,30,'北京市','no')!==null);
// ⑩ 真太阳时被静默跳过时给出警告（原实现只把 solarInfo 置 found:false，无任何提示）
const wk = BaziEngine.paipan('客','女',1990,5,15,10,0,'不存在市','yes');
assert('未知地名 → 仍出盘 + found:false', wk && wk.solarInfo && wk.solarInfo.found===false);
assert('未知地名 → getLastWarning=SOLAR_TIME_SKIPPED', (BaziEngine.getLastWarning()||{}).code==='SOLAR_TIME_SKIPPED', JSON.stringify(BaziEngine.getLastWarning()));
assert('警告 detail 回传原始地名与城市数', (BaziEngine.getLastWarning()||{}).detail.place==='不存在市' && BaziEngine.getLastWarning().detail.cityCount===724);
assert('合法排盘后警告被清空', BaziEngine.paipan('T','男',1990,5,15,10,30,'北京市','no') && BaziEngine.getLastWarning()===null);
assert('未填地名 + truesun=yes → 结构不变（solarInfo 仍为 null）', BaziEngine.paipan('匿名','男',1990,5,15,10,0,'','yes').solarInfo===null);

console.log('== ctx 体检 validateCtx（v1.3.14）==');
const clone = o => JSON.parse(JSON.stringify(o));
const vGood = BaziEngine.validateCtx(c1);
// ⑪ 最重要的一条：正常盘必须零误报（体检工具一旦误报就没人用了）
assert('正常盘 ok=true 且 errors=0', vGood.ok===true && vGood.errors.length===0, JSON.stringify(vGood.errors.slice(0,2)));
assert('正常盘 warnings=0', vGood.warnings.length===0, JSON.stringify(vGood.warnings.slice(0,3)));
// ⑫ 十神基准错（本项目《接入说明》第 1 条注意）：必须被抓到，并给出正确值
const vTens = clone(c1); vTens.tens = [vTens.tens[1], vTens.tens[0], vTens.tens[2], vTens.tens[3]];
const rTens = BaziEngine.validateCtx(vTens);
assert('十神错位 → ok=false', rTens.ok===false);
assert('十神错位 → 报错字段为 tens', rTens.errors.some(x=>x.field==='tens'), JSON.stringify(rTens.errors.map(x=>x.field)));
assert('十神错位 → expected.tens 给出正确值', Array.isArray(rTens.expected.tens) && rTens.expected.tens.join()===c1.tens.join(), (rTens.expected.tens||[]).join());
assert('十神错位 → 错误信息含"哪一柱错了"', /年干|月干|日干|时干/.test(rTens.errors.map(x=>x.message).join('')));
// ⑬ 其余自洽性检查
const vDm = clone(c1); vDm.dayMasterFull='甲木';
assert('dayMasterFull 与日柱不符 → error', BaziEngine.validateCtx(vDm).errors.some(x=>x.field==='dayMasterFull'));
const vXs = clone(c1); vXs.xiYong=['火','火','金']; vXs.jiYong=['火'];
assert('喜用与忌神重叠 → error', BaziEngine.validateCtx(vXs).errors.some(x=>x.field==='xiYong/jiYong'));
const vSs = clone(c1); vSs.shenSha=[{type:'吉'}];
assert('神煞项缺 name → error', BaziEngine.validateCtx(vSs).errors.some(x=>x.field==='shenSha'));
const vP5 = clone(c1); vP5.pillars=['庚午','辛巳','庚辰','辛巳','甲子'];
assert('支柱数≠4 → error', BaziEngine.validateCtx(vP5).errors.some(x=>x.field==='pillars'));
const vAlt = clone(c1); vAlt.pillars=c1.pillars.map(p=>[p[0],p[1]]);
assert('[天干,地支] 数组形状也接受（ok=true）', BaziEngine.validateCtx(vAlt).ok===true, JSON.stringify(BaziEngine.validateCtx(vAlt).errors.slice(0,2)));
// ⑭ 缺字段：崩溃类报 error、静默偏差类报 warning（且 matchRules 对后者行为不变）
const vNoSS = clone(c1); delete vNoSS.shenSha;
const rNoSS = BaziEngine.validateCtx(vNoSS);
assert('缺 shenSha → warning（非 error）', rNoSS.warnings.some(x=>x.field==='shenSha') && !rNoSS.errors.some(x=>x.field==='shenSha'));
assert('缺 shenSha → matchRules 仍可用（行为不变，命中减少）', Object.values(BaziEngine.matchRules(vNoSS)).reduce((s,a)=>s+a.length,0) < Object.values(cats).reduce((s,a)=>s+a.length,0));
// ⑮ validateCtx 自身绝不能在非法输入上崩
assert('validateCtx(null) 不抛且 ok=false', BaziEngine.validateCtx(null).ok===false);
assert('validateCtx({}) 不抛且列出缺失字段', (()=>{ const r=BaziEngine.validateCtx({}); return r.ok===false && r.missing.length>0; })());
assert('validateCtx("字符串") 不抛', BaziEngine.validateCtx('x').ok===false);
// ⑯ matchRules 入口：把原始 TypeError 换成可读错误
let e1=null; try{ BaziEngine.matchRules({}); }catch(e){ e1=e; }
assert('matchRules({}) → CTX_MISSING_FIELD 且列出字段', e1 && e1.code==='CTX_MISSING_FIELD' && e1.fields.includes('pillars'), e1?e1.code:'未抛错');
assert('matchRules({}) 错误信息可读（含字段名，不再是 reading \'includes\'）', e1 && /pillars/.test(e1.message) && !/reading '/.test(e1.message));
let e2=null; try{ BaziEngine.matchRules(null); }catch(e){ e2=e; }
assert('matchRules(null) → CTX_INVALID', e2 && e2.code==='CTX_INVALID', e2?e2.code:'未抛错');
assert('合法 ctx 不受入口检查影响（命中数不变）', Object.values(BaziEngine.matchRules(c1)).reduce((s,a)=>s+a.length,0)===Object.values(cats).reduce((s,a)=>s+a.length,0));

console.log('== 用神被冲克合 计量修复（v1.3.17）==');
// ⑰ 缺陷①：两个用神柱互相合，原实现按"关系对"累加两次 → 单独凑够阈值，误判"格局破损"
const fxA = BaziEngine.paipan('A','男',2059,2,20,17,41,'','no');
assert('用神×用神互合不再判为用神被冲克合', BaziEngine.yongShenChong(fxA)===false, fxA.pillars.join(' '));
assert('该盘不再命中 pattern_yongshen_chong', !(BaziEngine.matchRules(fxA)['格局']||[]).some(r=>r.id==='pattern_yongshen_chong'));
// ⑱ 缺陷②：只有 1 个"对手柱"时，原实现因该柱同时冲/合不同用神而算成 2 处
const fxB = BaziEngine.paipan('B','女',1996,5,5,8,44,'','no');
assert('仅 1 个对手柱不再判为用神被冲克合', BaziEngine.yongShenChong(fxB)===false, fxB.pillars.join(' '));
assert('该盘不再命中 career_用神被冲', !(BaziEngine.matchRules(fxB)['事业']||[]).some(r=>r.id==='career_用神被冲'));
// ⑲ 反向哨兵：真·≥2 个对手柱仍须命中（证明规则没被改死）
const fxC = BaziEngine.paipan('C','女',1940,1,1,0,0,'','no');
assert('≥2 个对手柱仍判为用神被冲克合', BaziEngine.yongShenChong(fxC)===true, fxC.pillars.join(' '));
assert('该盘仍命中 pattern_yongshen_chong', (BaziEngine.matchRules(fxC)['格局']||[]).some(r=>r.id==='pattern_yongshen_chong'));

console.log('== 组合匹配排除日干 + 「中和」文案口径（v1.3.18）==');
// ⑳ 客户 N02 样本（1988-01-24 07:00 男 / 丁卯 癸丑 戊寅 丙辰）：日主中和、偏印透时干、官杀只藏不透
const fxN02 = BaziEngine.paipan('N02','男',1988,1,24,7,0,'','no');
assert('N02 四柱 = 丁卯 癸丑 戊寅 丙辰', fxN02.yg==='丁卯'&&fxN02.mg==='癸丑'&&fxN02.dg==='戊寅'&&fxN02.hg==='丙辰', fxN02.pillars.join(' '));
assert('N02 日主中和（「中和」键判的是日主，不是十神）', fxN02.strength==='中和');
const n02 = new Set(Object.values(BaziEngine.matchRules(fxN02)).flat().map(r=>r.id));
assert('N02 命中 career_偏印_时干（时干丙=偏印）', n02.has('career_偏印_时干'));
assert('N02 命中 career_偏印_中和（日主中和 + 偏印透干）', n02.has('career_偏印_中和'));
assert('N02 不命中 career_pianyin（偏印=火为忌神，非"为用神有力"）', !n02.has('career_pianyin'));
assert('N02 不命中 combo_偏印_比肩（除日主外无真实比劫）', !n02.has('combo_偏印_比肩'));
assert('N02 不命中 combo_偏印_七杀 / combo_偏印_正官 / combo_30（官杀只藏地支、不透干）',
  !n02.has('combo_偏印_七杀') && !n02.has('combo_偏印_正官') && !n02.has('combo_30'));
assert('「中和」文案口径：不再写成"偏印中和"',
  (BaziEngine.matchRules(fxN02)['事业']||[]).find(r=>r.id==='career_偏印_中和').conclusion.startsWith('日主中和、偏印透干'));
// ㉑ 反向哨兵：年干另有真实比肩时必须仍命中（防止规则被改死）
const fxBi = BaziEngine.paipan('BI','男',1993,1,1,0,36,'','no');
assert('年干有真实比肩时 combo_偏印_比肩 仍命中', (BaziEngine.matchRules(fxBi)['十神组合']||[]).some(r=>r.id==='combo_偏印_比肩'), fxBi.pillars.join(' '));
// ㉒ 透干 vs 藏干：官杀透干才参与组合
const fxGuan = BaziEngine.paipan('G','男',2019,2,24,19,23,'','no');
assert('正官透干时 combo_偏印_正官 命中', (BaziEngine.matchRules(fxGuan)['十神组合']||[]).some(r=>r.id==='combo_偏印_正官'), fxGuan.pillars.join(' '));

console.log('== 财印组合接喜忌：同组合正负两断语互斥分流（v1.3.19）==');// ㉓ N02：偏印（火）为忌神 → 出「财星制枭」（正向），不出「财星坏印」（负向）
assert('N02 命中 combo_正财_偏印_制枭（偏印为忌，财制枭）', n02.has('combo_正财_偏印_制枭'));
assert('N02 不命中 combo_正财_偏印（偏印为忌时不判坏印）', !n02.has('combo_正财_偏印'));
// ㉔ 反向：身弱印为用 → 出「财星坏印」，不出「制枭」
const fxWeak = BaziEngine.paipan('W','男',2010,3,3,14,10,'','no');
const sWeak = new Set(Object.values(BaziEngine.matchRules(fxWeak)).flat().map(r=>r.id));
assert('身弱印为用之盘命中 combo_正财_偏印（财星坏印）', sWeak.has('combo_正财_偏印'), fxWeak.pillars.join(' '));
assert('身弱印为用之盘不命中 combo_正财_偏印_制枭', !sWeak.has('combo_正财_偏印_制枭'));
// ㉕ 互斥性：同一盘不可能同时命中同一组合的 正/负 两半（财印五行喜忌恒互斥）
for (const fx of [['A','男',1988,1,24,7,0],['B','女',1975,6,9,3,20],['C','男',2001,11,17,22,45],['D','女',1966,4,2,9,5],['E','男',1992,8,28,17,30]]) {
  const c = BaziEngine.paipan(fx[0],fx[1],fx[2],fx[3],fx[4],fx[5],fx[6],'','no');
  const s = new Set(Object.values(BaziEngine.matchRules(c)).flat().map(r=>r.id));
  assert(`${fx[0]} 财印组合正负两半互斥（${c.pillars.join(' ')}）`,
    !(s.has('combo_正财_偏印') && s.has('combo_正财_偏印_制枭')) &&
    !(s.has('combo_正财_正印') && s.has('combo_财星破印')));
}

console.log('== 十神键排除日干：比肩规则不再对每张盘恒真（v1.3.20）==');
// ㉖ N02 只有日干是比肩（tens=[正印,正财,比肩,偏印]，日干戊=比肩）→ 比肩类规则必须全不命中
[['career_比肩_中和', 'career_比肩_中和'], ['career_bijian', 'career_bijian'],
 ['char_ten_比肩', 'char_ten_比肩'], ['study_比劫重', 'study_比劫重'],
 ['marriage_bijie_duo', 'marriage_bijie_duo']].forEach(([id, label]) => {
  assert(`N02 不命中 ${label}（除日干外无比劫）`, !n02.has(id));
});
// ㉗ 反向哨兵：真有比肩透干时必须仍命中（防止规则被修死）
const fxBiStrong = BaziEngine.paipan('BIS', '男', 1993, 1, 1, 0, 36, '', 'no');
const biStrong = new Set(Object.values(BaziEngine.matchRules(fxBiStrong)).flat().map(r => r.id));
assert('年/月干有真实比肩且日主强 → career_比肩_强 命中', biStrong.has('career_比肩_强'), fxBiStrong.pillars.join(' '));
assert('年/月干有真实比肩 → kin_sibling_jie 命中', biStrong.has('kin_sibling_jie'));
// ㉘ 中和 + 真实比肩透干 → career_比肩_中和 仍可达（不是被一刀切掉）
const fxBiZhong = BaziEngine.paipan('BIZ', '男', 1960, 6, 7, 15, 10, '', 'no');
const biZhong = new Set(Object.values(BaziEngine.matchRules(fxBiZhong)).flat().map(r => r.id));
assert('中和 + 真实比肩透干 → career_比肩_中和 命中', biZhong.has('career_比肩_中和'), fxBiZhong.pillars.join(' '));
// ㉙ 状态计数同样不含日干：只有日干是比肩时「比劫重重」类不成立
assert('N02 不命中 kin_兄弟_比肩得力（旺衰+比肩条件，日干不算）', !n02.has('kin_兄弟_比肩得力'));
assert('N02 总命中 = 100 条（v1.3.20 实测，去掉 5 条被日干污染的比肩规则）', n02.size === 100, 'size=' + n02.size);

console.log('\n结果: ' + pass + ' PASS, ' + fail + ' FAIL');
if (fail > 0) process.exit(1);
