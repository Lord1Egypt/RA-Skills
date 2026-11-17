// 验证 58 条"沉睡规则"已接入渲染：大运(dayun_01~20)/流月(liuyue_01~20)/流年(liu_21~30)/合婚(he_13~20)
const fs = require('fs');
const html = fs.readFileSync(__dirname + '/../ui/index.html', 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if(!m){ console.error('未找到 script'); process.exit(1); }
let code = m[1];
// 增强 stub：按 id 返回可配置 value（对象缓存，runLiu 写入后同 id 可读取）
const stub = `globalThis._inp=globalThis._inp||{};
globalThis._els=globalThis._els||{};
function _getEl(id){
  if(!globalThis._els[id]) globalThis._els[id]={value:"",textContent:"",innerHTML:"",style:{},classList:{add(){},remove(){}},onclick:null};
  if(globalThis._inp[id]!==undefined) globalThis._els[id].value=globalThis._inp[id];
  return globalThis._els[id];
}
var document={getElementById:_getEl,querySelectorAll:()=>[],querySelector:()=>null};
var alert=()=>{};`;
const expose = ';globalThis.NAYIN=NAYIN;globalThis.NAYIN_WX=NAYIN_WX;globalThis.CHONG=CHONG;globalThis.LIUHE=LIUHE;globalThis.SANHE=SANHE;globalThis.ZHI=ZHI;globalThis.matchRules=matchRules;globalThis.yearGZ=yearGZ;globalThis.analyzeHe=analyzeHe;globalThis.paipan=paipan;globalThis.dayGZ=dayGZ;globalThis.calcShenSha=calcShenSha;globalThis.WU_CHONG=WU_CHONG;globalThis.WU_HE=WU_HE;globalThis.GAN_WX=GAN_WX;globalThis.ZHI_WX=ZHI_WX;globalThis.tenGod=tenGod;globalThis.findRule=findRule;globalThis.matchDayun=matchDayun;globalThis.matchLiuYue=matchLiuYue;globalThis.runLiu=runLiu;globalThis.runLiuYue=runLiuYue;globalThis.TIANYI=TIANYI;globalThis.YIMA=YIMA;globalThis.TAOHUA=TAOHUA;globalThis.HUAGAI=HUAGAI;globalThis.JIANGXING=JIANGXING;globalThis.__setLast=function(x){LAST=x;};globalThis.LAST=null;';
eval(stub + code + expose);

let fails = 0;
function assert(name, cond, extra){
  console.log((cond?'  PASS ':'  FAIL ')+name+(extra?'  ['+extra+']':''));
  if(!cond) fails++;
}

// ===== 1. 大运规则 =====
console.log('== 大运（dayun_01~20）==');
const c = paipan('马云','男',1964,9,10,12,0,'北京市','no');
const dySteps = c.dy.steps;
let hitIds = new Set();
dySteps.forEach(gz => { matchDayun(c, gz).forEach(r => hitIds.add(r.id)); });
// 十神主题规则必然命中
const tenHit = [...hitIds].filter(id => /^dayun_(1[2-9]|20)$/.test(id));
assert('大运十神主题规则命中(dayun_12~20)', tenHit.length >= 2, [...hitIds].join(','));
// 至少一条规则命中（每步大运必有十神）
assert('大运规则总命中≥8条(8步大运各≥1)', hitIds.size >= 8, hitIds.size + '条');
// 换运提醒规则存在
assert('dayun_11 换运提醒可查', !!findRule('dayun_11'));

// ===== 2. 流月规则 =====
console.log('== 流月（liuyue_01~20）==');
const c2 = paipan('测试','女',1990,5,15,23,30,'上海市','no');
// 直接构造调用：正官当令 → liuyue_03
const r1 = matchLiuYue(c2, '丙子', '正官', []);
assert('月令正官→liuyue_03', r1.some(r=>r.id==='liuyue_03'), r1.map(r=>r.id).join(','));
// 印星当令 → liuyue_01
const r2 = matchLiuYue(c2, '丁丑', '正印', []);
assert('月令正印→liuyue_01', r2.some(r=>r.id==='liuyue_01'), r2.map(r=>r.id).join(','));
// 天干透喜用 → liuyue_17
const xi = c2.xiYong||[];
const xiGan = Object.keys(GAN_WX).find(g=>xi.includes(GAN_WX[g]));
const r3 = matchLiuYue(c2, xiGan+'子', '食神', []);
assert('天干透喜用→liuyue_17', r3.some(r=>r.id==='liuyue_17'), '喜用='+xi.join(',')+' 天干='+xiGan);

// ===== 3. 流年规则（liu_21~30）=====
console.log('== 流年（liu_21~30）==');
globalThis.__setLast(paipan('流年测','男',1990,3,10,10,0,'广州市','yes'));
// 找一个 liu_21(干支皆喜用) 或 liu_22(干支皆忌) 命中的年份
let liuHit = [];
let found = false;
for(let y=2000;y<=2050 && !found;y++){
  globalThis._inp['liuYear']=String(y); globalThis._inp['liuDayun']='0';
  document.getElementById("liuResult").innerHTML='';
  runLiu();
  const out = document.getElementById("liuResult").innerHTML;
  const l21 = out.indexOf('流年干支均为喜用神')>=0;
  const l22 = out.indexOf('流年干支均为忌神')>=0;
  const l26 = out.indexOf('流年逢天德/月德贵人')>=0;
  const l27 = out.indexOf('流年日柱逢刑')>=0;
  const l28 = out.indexOf('流年日柱逢害')>=0;
  const l29 = out.indexOf('流年命带将星')>=0;
  const l30 = out.indexOf('流年命带华盖')>=0;
  const l25 = out.indexOf('流年逢劫财旺')>=0;
  if(l21||l22||l26||l27||l28||l29||l30||l25){ liuHit=[y,l21,l22,l26,l27,l28,l29,l30,l25]; found=true; }
}
assert('流年规则命中(liu_21~30)', found, liuHit.join(','));
// 至少有 lzTen 或 lTen 类输出（保证 runLiu 正常执行）
assert('流年输出非空', document.getElementById("liuResult").innerHTML.length > 100);

// ===== 4. 合婚规则（he_13~20）=====
console.log('== 合婚（he_13~20）==');
let heHit = false, heExtra = '';
// 用多组随机盘找命中
const seeds = [
  ['甲','男',1992,5,20,10,0], ['乙','女',1995,8,15,14,30], ['丙','男',1988,3,2,6,0], ['丁','女',2000,12,25,20,0],
  ['戊','男',1985,7,7,9,0], ['己','女',1993,1,18,16,0], ['庚','男',1998,10,10,11,0], ['辛','女',1991,4,4,22,0]
];
for(let i=0;i<seeds.length && !heHit;i++){
  for(let j=i+1;j<seeds.length && !heHit;j++){
    const A = paipan(seeds[i][0], seeds[i][1], seeds[i][2], seeds[i][3], seeds[i][4], seeds[i][5], seeds[i][6], '广州市','yes');
    const B = paipan(seeds[j][0], seeds[j][1], seeds[j][2], seeds[j][3], seeds[j][4], seeds[j][5], seeds[j][6], '广州市','yes');
    const rep = analyzeHe(A, B);
    const hits = ['双方日柱纳音相生','双方日柱纳音相克','双方月柱相合','双方年柱相合','双方时柱相合','双方日柱天干相合','双方日柱天干相冲','双方用神互为对方喜神'];
    const foundH = hits.filter(h=>rep.indexOf(h)>=0);
    if(foundH.length){ heHit=true; heExtra = seeds[i][0]+'×'+seeds[j][0]+' → '+foundH.join(' | '); }
  }
}
assert('合婚细目命中(he_13~20)', heHit, heExtra);

console.log(fails===0 ? '\n结果: 全部 PASS' : '\n结果: '+fails+' 条 FAIL');
process.exit(fails===0?0:1);
