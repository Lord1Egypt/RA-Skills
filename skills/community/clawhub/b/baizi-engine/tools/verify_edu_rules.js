// 验证 edu_17~20 复活后命中逻辑正确性
// 用法: node tools/verify_edu_rules.js
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
const expose = ';globalThis.matchRules=matchRules;globalThis.paipan=paipan;globalThis.RULES=RULES;globalThis.__setLast=function(x){LAST=x;};globalThis.LAST=null;';
eval(stub + code + expose);

let fails = 0;
function assert(name, cond, extra){
  console.log((cond?'  PASS ':'  FAIL ')+name+(extra?'  ['+extra+']':''));
  if(!cond) fails++;
}

// 在随机命盘中统计 edu_17~20 的命中分布（验证有盘能命中、非无条件）
const IDs = ['edu_17','edu_18','edu_19','edu_20'];
const hitMap = {}; IDs.forEach(id=>hitMap[id]={hits:0, samples:[]});
const emptyCond = {};
const total = 400;
let seeded = 0;
function rnd(n){ seeded = (seeded*1103515245+12345) % 2147483648; return seeded % n; }

for(let i=0;i<total;i++){
  const y = 1950 + rnd(60);
  const mo = 1 + rnd(12);
  const d = 1 + rnd(28);
  const hh = rnd(24), mm = rnd(60);
  const gender = rnd(2)===0?'男':'女';
  const c = paipan('测',gender,y,mo,d,hh,mm,'', 'no');
  if(!c) continue;
  const cats = matchRules(c);
  const edu = cats['学业']||[];
  for(const r of edu){
    if(IDs.includes(r.id)){
      hitMap[r.id].hits++;
      if(hitMap[r.id].samples.length<2){
        hitMap[r.id].samples.push({y,mo,d,hh,mm,gender,pillars:c.pillars.join(' '),tens:c.tens,strength:c.strength,xiYong:c.xiYong});
      }
    }
  }
}

console.log('\n========== edu_17~20 命中分布（400 随机盘） ==========');
for(const id of IDs){
  const h = hitMap[id];
  const rate = (h.hits/total*100).toFixed(1);
  console.log(`  ${id}: 命中 ${h.hits}/${total} (${rate}%)`);
  h.samples.forEach(s=>{
    console.log(`    样本: ${s.y}-${s.mo}-${s.d} ${s.hh}:${String(s.mm).padStart(2,'0')} ${s.gender} | ${s.pillars} | tens=[${s.tens}] 强弱=${s.strength} 喜用=[${s.xiYong}]`);
  });
}

// 断言：4 条规则都应至少命中一次（证明可用），且命中率 < 60%（证明非无条件）
for(const id of IDs){
  assert(`${id} 至少命中 1 次（规则可用）`, hitMap[id].hits >= 1, `hits=${hitMap[id].hits}`);
  assert(`${id} 命中率 < 60%（非无条件显示）`, hitMap[id].hits/total < 0.6, `${(hitMap[id].hits/total*100).toFixed(1)}%`);
}

// 额外验证：qinq_27~30 不应再出现在主渲染的六亲类别中
const EMPTY_IDS = ['qinq_27','qinq_28','qinq_29','qinq_30'];
const total2 = 200;
const seenMap = {}; EMPTY_IDS.forEach(id=>seenMap[id]=0);
for(let i=0;i<total2;i++){
  const y = 1950 + rnd(60);
  const mo = 1 + rnd(12);
  const d = 1 + rnd(28);
  const hh = rnd(24), mm = rnd(60);
  const gender = rnd(2)===0?'男':'女';
  const c = paipan('测',gender,y,mo,d,hh,mm,'', 'no');
  if(!c) continue;
  const cats = matchRules(c);
  const liuqin = cats['六亲']||[];
  for(const r of liuqin){
    if(r.id && EMPTY_IDS.includes(r.id)) seenMap[r.id]++;
  }
}
for(const id of EMPTY_IDS){
  assert(`主渲染六亲类别不再出现 ${id}`, seenMap[id]===0, `seen=${seenMap[id]}`);
}

console.log('\n' + (fails===0 ? '全部通过 ✔' : `存在 ${fails} 处失败 ✘`));
process.exit(fails===0?0:1);
