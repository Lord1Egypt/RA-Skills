// test_liuyue_v2.js — 流月 v2 引擎回归测试（批次2：25 条细分规则）
// 运行: node tools/test_liuyue_v2.js
const fs=require('fs');
const html=fs.readFileSync(__dirname+'/../ui/index.html','utf8');
const code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const stub='var document={getElementById:()=>({value:"",innerHTML:"",style:{},classList:{add(){},remove(){}}}),querySelectorAll:()=>[],querySelector:()=>null};var alert=()=>{};';
eval(stub+code+';globalThis.matchLiuYue=matchLiuYue;globalThis.paipan=paipan;globalThis.RULES=RULES;globalThis.findRule=findRule;globalThis.CHONG=CHONG;globalThis.LIUHE=LIUHE;globalThis.WU_HE=WU_HE;globalThis.GAN_WX=GAN_WX;globalThis.ZHI_WX=ZHI_WX;globalThis.ZHI=ZHI;globalThis.monthGZ=monthGZ;globalThis.yearGZ=yearGZ;globalThis.tenGod=tenGod;');

let pass=0, fail=0;
const T=(name,cond)=>{
  if(cond){pass++; console.log('  ✓ '+name);}
  else {fail++; console.log('  ✗ FAIL: '+name);}
};

// 规则存在性（25 条新 id 全在 RULES 中）
const newIds=[
  'liuyue_cs_长生','liuyue_cs_沐浴','liuyue_cs_冠带','liuyue_cs_临官','liuyue_cs_帝旺','liuyue_cs_衰','liuyue_cs_病','liuyue_cs_死','liuyue_cs_墓','liuyue_cs_绝','liuyue_cs_胎','liuyue_cs_养',
  'liuyue_chong_子午','liuyue_chong_丑未','liuyue_chong_寅申','liuyue_chong_卯酉','liuyue_chong_辰戌','liuyue_chong_巳亥',
  'liuyue_wuhe_甲己','liuyue_wuhe_乙庚','liuyue_wuhe_丙辛','liuyue_wuhe_丁壬','liuyue_wuhe_戊癸',
  'liuyue_fuyin_day','liuyue_wangxiang'
];
console.log('--- 规则存在性（25 条）---');
let missing=newIds.filter(id=>!findRule(id));
T('25 条新规则全部入库', missing.length===0);
if(missing.length) console.log('    缺失: '+missing.join(','));

// 构造 10 个不同日主样本盘，测真实命中（2026 年 12 流月）
console.log('\n--- 真实排盘命中测试（10 盘 × 12 流月扫描 2026 年）---');
let hitStat={};
const refMs=[2,3,4,5,6,7,8,9,10,11,12,1];
const midDays=[4,5,5,5,6,6,7,8,8,8,7,6];
const seeds=[1985,1988,1991,1994,1997,2000,2003,2006,2009,2012];
for(let si=0; si<10; si++){
  const c=paipan('测','男',seeds[si],(si%12)+1,(si%28)+1,si%24,(si*17)%60,'广州','no');
  if(!c){ T('排盘成功 盘'+seeds[si], false); continue; }
  for(let i=0; i<12; i++){
    const rm=refMs[i], rd=midDays[i];
    const yg=yearGZ(2026,rm,rd,12,0);
    if(!yg) continue;
    const mgz=monthGZ(2026,rm,rd,12,0,yg[0]);
    if(!mgz) continue;
    const mTen=tenGod(mgz[0], c.dmWx, c.dmYin);
    const rels=[];
    c.pillars.forEach((p,j)=>{
      if(CHONG[mgz[1]]===p[1]) rels.push('冲'+['年','月','日','时'][j]);
      if(LIUHE.some(pr=>pr.includes(mgz[1])&&pr.includes(p[1]))) rels.push('合'+['年','月','日','时'][j]);
    });
    const mrs=matchLiuYue(c, mgz, mTen, rels);
    for(const r of mrs){ if(r) hitStat[r.id]=(hitStat[r.id]||0)+1; }
  }
}

// 统计各维度是否至少命中一次
const dims={十二长生:newIds.slice(0,12),六冲:newIds.slice(12,18),五合:newIds.slice(18,23),特殊:newIds.slice(23)};
console.log('--- 各维度命中覆盖率 ---');
for(const [dim,ids] of Object.entries(dims)){
  const hit=ids.filter(id=>hitStat[id]>0);
  T(`${dim}维度（${ids.length} 条中命中 ${hit.length} 条）`, hit.length>=1);
  const noHit=ids.filter(id=>!hitStat[id]);
  if(noHit.length) console.log('    未命中（可能因样本盘未覆盖）: '+noHit.join(','));
}
const totalHits=Object.values(hitStat).reduce((a,b)=>a+b,0);
console.log('\n10 盘 × 12 月共产生流月断语命中: '+totalHits+' 次，覆盖 '+Object.keys(hitStat).length+' 条不同规则');
T('总命中数 > 60（引擎确在输出新规则）', totalHits>60);

// 基础规则仍然工作（liuyue_02 财星当令）
const c0=paipan('测','男',1990,5,15,10,0,'广州','no');
const mgz0=monthGZ(2026,5,5,12,0,yearGZ(2026,5,5,12,0)[0]);
const mTen0=tenGod(mgz0[0], c0.dmWx, c0.dmYin);
let baseTen=false;
if(mTen0==='正财'||mTen0==='偏财') baseTen=true;
const mrs0=matchLiuYue(c0, mgz0, mTen0, []);
T('基础规则 liuyue_02（财星当令）仍生效', mrs0.some(r=>r&&r.id==='liuyue_02')||!baseTen);

// 定向补测：构造流月干支验证未覆盖规则（绕开节气参考日偏差）
console.log('\n--- 定向补测（构造流月干支）---');
let found={};
outer:
for(let y=1960;y<2010;y++){
  for(let m=1;m<=12;m++){
    const c=paipan('测','男',y,m,15,10,0,'广州','no');
    if(!c) continue;
    const rz=c.pillars[2][1], rg=c.pillars[2][0];
    if(!found.chen&&rz==='辰') found.chen=c;
    if(!found.bing&&rg==='丙') found.bing=c;
    if(!found.wu&&rg==='戊') found.wu=c;
    if(found.chen&&found.bing&&found.wu) break outer;
  }
}
if(found.chen) T('辰日盘+戊戌月 → liuyue_chong_辰戌', matchLiuYue(found.chen,'戊戌','食神',[]).some(r=>r&&r.id==='liuyue_chong_辰戌'));
if(found.bing) T('丙日盘+辛卯月 → liuyue_wuhe_丙辛', matchLiuYue(found.bing,'辛卯','正财',[]).some(r=>r&&r.id==='liuyue_wuhe_丙辛'));
if(found.wu) T('戊日盘+癸巳月 → liuyue_wuhe_戊癸', matchLiuYue(found.wu,'癸巳','正官',[]).some(r=>r&&r.id==='liuyue_wuhe_戊癸'));

console.log(`\n===== 结果: ${pass} 通过 / ${fail} 失败 =====`);
process.exit(fail?1:0);
