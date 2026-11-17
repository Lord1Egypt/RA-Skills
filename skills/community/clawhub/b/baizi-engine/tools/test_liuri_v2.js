// test_liuri_v2.js — 流日 v2 引擎回归测试（批次1：45 条细分规则）
// 运行: node tools/test_liuri_v2.js
const fs=require('fs');
const html=fs.readFileSync(__dirname+'/../ui/index.html','utf8');
const code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const stub='var document={getElementById:()=>({value:"",innerHTML:"",style:{},classList:{add(){},remove(){}}}),querySelectorAll:()=>[],querySelector:()=>null};var alert=()=>{};';
eval(stub+code+';globalThis.matchLiuDay=matchLiuDay;globalThis.paipan=paipan;globalThis.RULES=RULES;globalThis.findRule=findRule;globalThis.CHONG=CHONG;globalThis.LIUHE=LIUHE;globalThis.WU_HE=WU_HE;globalThis.GAN_WX=GAN_WX;globalThis.ZHI_WX=ZHI_WX;globalThis.ZHI=ZHI;');

let pass=0, fail=0;
const T=(name,cond)=>{
  if(cond){pass++; console.log('  ✓ '+name);}
  else {fail++; console.log('  ✗ FAIL: '+name);}
};

// 规则存在性（45 条新 id 全在 RULES 中）
const newIds=[
  'liuri_ten_比肩','liuri_ten_劫财','liuri_ten_食神','liuri_ten_伤官','liuri_ten_偏财','liuri_ten_正财','liuri_ten_七杀','liuri_ten_正官','liuri_ten_偏印','liuri_ten_正印',
  'liuri_chong_子午','liuri_chong_丑未','liuri_chong_寅申','liuri_chong_卯酉','liuri_chong_辰戌','liuri_chong_巳亥',
  'liuri_he_子丑','liuri_he_寅亥','liuri_he_卯戌','liuri_he_辰酉','liuri_he_巳申','liuri_he_午未',
  'liuri_sanhe_水局','liuri_sanhe_木局','liuri_sanhe_火局','liuri_sanhe_金局',
  'liuri_wuhe_甲己','liuri_wuhe_乙庚','liuri_wuhe_丙辛','liuri_wuhe_丁壬','liuri_wuhe_戊癸',
  'liuri_cs_长生','liuri_cs_沐浴','liuri_cs_冠带','liuri_cs_临官','liuri_cs_帝旺','liuri_cs_衰','liuri_cs_病','liuri_cs_死','liuri_cs_墓','liuri_cs_绝','liuri_cs_胎','liuri_cs_养',
  'liuri_tkdc','liuri_fuyin'
];
console.log('--- 规则存在性（45 条）---');
let missing=newIds.filter(id=>!findRule(id));
T('45 条新规则全部入库', missing.length===0);
if(missing.length) console.log('    缺失: '+missing.join(','));

// 构造 10 个不同日主样本盘，测真实命中
console.log('\n--- 真实排盘命中测试（10 盘 × 逐日扫描 2026 年 8 月）---');
let hitStat={};
const seeds=[1985,1988,1991,1994,1997,2000,2003,2006,2009,2012];
for(let si=0; si<10; si++){
  const c=paipan('测','男',seeds[si],(si%12)+1,(si%28)+1,si%24,(si*17)%60,'广州','no');
  if(!c){ T('排盘成功 盘'+seeds[si], false); continue; }
  const zi=c.pillars[2][1], riGan=c.pillars[2][0];
  // 扫描 2026-08 全月
  for(let d=1; d<=31; d++){
    const gz=dayGZ(2026,8,d);
    const g=gz[0], z=gz[1];
    const ten=tenGod(g, c.dmWx, c.dmYin);
    const xi=c.xiYong||[], ji=c.jiYong||[];
    const kong=(c.kongWang||[]).includes(z);
    const isXi=xi.includes(GAN_WX[g])||xi.includes(ZHI_WX[z]);
    const isJi=ji.includes(GAN_WX[g])||ji.includes(ZHI_WX[z]);
    const mrs=matchLiuDay(c, g, z, ten, [], kong, isXi, isJi);
    for(const r of mrs){ if(r) hitStat[r.id]=(hitStat[r.id]||0)+1; }
  }
}

// 统计各维度是否至少命中一次
const dims={十神:newIds.slice(0,10),六冲:newIds.slice(10,16),六合:newIds.slice(16,22),三合:newIds.slice(22,26),五合:newIds.slice(26,31),长生:newIds.slice(31,43),特殊:newIds.slice(43)};
console.log('--- 各维度命中覆盖率 ---');
for(const [dim,ids] of Object.entries(dims)){
  const hit=ids.filter(id=>hitStat[id]>0);
  T(`${dim}维度（${ids.length} 条中命中 ${hit.length} 条）`, hit.length>=1);
  const noHit=ids.filter(id=>!hitStat[id]);
  if(noHit.length) console.log('    未命中（可能因样本盘未覆盖）: '+noHit.join(','));
}
// 总命中次数
const totalHits=Object.values(hitStat).reduce((a,b)=>a+b,0);
console.log('\n10 盘 × 31 日共产生流日断语命中: '+totalHits+' 次，覆盖 '+Object.keys(hitStat).length+' 条不同规则');
T('总命中数 > 100（引擎确在输出新规则）', totalHits>100);

// 基础五条仍然工作
const c0=paipan('测','男',1990,5,15,10,0,'广州','no');
const zi0=c0.pillars[2][1];
const baseTest=(()=>{
  // 找一个冲日柱的流日地支
  const chongZhi=CHONG[zi0];
  if(!chongZhi) return false;
  const mrs=matchLiuDay(c0, '甲', chongZhi, '比肩', [], false, true, false);
  return mrs.some(r=>r&&r.id==='liuri_01');
})();
T('基础规则 liuri_01（冲日柱）仍生效', baseTest);

console.log(`\n===== 结果: ${pass} 通过 / ${fail} 失败 =====`);
process.exit(fail?1:0);
