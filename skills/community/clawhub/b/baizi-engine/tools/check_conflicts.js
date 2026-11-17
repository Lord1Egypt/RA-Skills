// 大样本矛盾断语检测：同一盘命中互为反义的断语
const fs=require('fs');
const html=fs.readFileSync(__dirname+'/../ui/index.html','utf8');
const code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const stub='var document={getElementById:()=>({value:"",innerHTML:"",style:{},classList:{add(){},remove(){}}}),querySelectorAll:()=>[],querySelector:()=>null};var alert=()=>{};';
eval(stub+code+';globalThis.matchRules=matchRules;globalThis.paipan=paipan;');
// 反义断语对：20 对 强/弱
const pairs=[];
for(const dm of ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸']){
  pairs.push(['char_'+dm+'_强','char_'+dm+'_弱']);
  pairs.push(['yongshen_'+dm+['木','木','火','火','土','土','金','金','水','水'][['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'].indexOf(dm)]+'_强','yongshen_'+dm+['木','木','火','火','土','土','金','金','水','水'][['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'].indexOf(dm)]+'_弱']);
}
let total=0, conflicts=0;
const seeds=[1980,1983,1986,1989,1992,1995,1998,2001,2004,2007];
for(let si=0; si<10; si++){
  for(let i=0;i<100;i++){
    const y=seeds[si]+(i%20), m=1+(i*7)%12, d=1+(i*13)%28, hh=i%24, mm=(i*17)%60;
    const c=paipan('测','男',y,m,d,hh,mm,'广州','no');
    if(!c) continue;
    total++;
    // 2026-08-19 修复（工具链审计）：原 matchRules(c,{id:a}) 第二参数被忽略、返回值对象无 .length
    // → ra.length 恒 undefined → conflicts 恒 0，检测整体失效恒绿。改为每盘 matchRules 一次 + Set 查 id。
    const all = new Set(Object.values(matchRules(c)).flat().map(r => r.id));
    for(const [a,b] of pairs){
      if(all.has(a) && all.has(b)){ conflicts++; console.log(`冲突: 盘${y}-${m}-${d} ${c.dg} 同时命中 ${a}+${b}`); }
    }
  }
}
console.log(`\n共 ${total} 盘，成对规则 ${pairs.length*2} 条，矛盾命中 ${conflicts} 次`);
// 门禁退出码（2026-08-19 修复：此前冲突>0 也恒 exit 0，CI 中不失败）
if (conflicts > 0) process.exit(1);
process.exit(0);
