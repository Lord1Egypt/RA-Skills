#!/usr/bin/env node
'use strict';
const path=require('path');
const SKILL='daily-vocab',DEFAULT_MORNING='08:00',DEFAULT_EVENING='21:00';
const ALLOWED_CH=new Set(['telegram','feishu','slack','discord']);
function sanitizeId(v){if(typeof v!=='string'||!/^[a-zA-Z0-9_-]{1,128}$/.test(v)){console.error('❌ 无效userId');process.exit(1);}return v;}
function sanitizeTime(v,l){if(!/^\d{1,2}:\d{2}$/.test(v)){console.error('❌ 无效'+l);process.exit(1);}const[h,m]=v.split(':').map(Number);if(h>23||m>59){console.error('❌ 无效'+l);process.exit(1);}return{h,m};}
function enablePush(userId,opts){
  userId=sanitizeId(userId);
  const mt=opts.morning||DEFAULT_MORNING;
  const et=opts.evening||DEFAULT_EVENING;
  const{h:mh,m:mm}=sanitizeTime(mt,'--morning');
  const{h:eh,m:em}=sanitizeTime(et,'--evening');
  const ch=opts.channel||'telegram';
  if(!ALLOWED_CH.has(ch)){console.error('❌ 不支持渠道:'+ch);process.exit(1);}
  const sk=`agent:main:${ch}:direct:${userId}`;
  console.log('__OPENCLAW_CRON_ADD__:'+JSON.stringify({name:`${SKILL}-morning-${userId}`,cronExpr:`${mm} ${mh} * * *`,tz:'Asia/Shanghai',session:'isolated',sessionKey:sk,channel:ch,to:userId,announce:true,timeoutSeconds:180,message:`node ${path.join(__dirname,'morning-push.js')} ${userId}`}));
  console.log('__OPENCLAW_CRON_ADD__:'+JSON.stringify({name:`${SKILL}-evening-${userId}`,cronExpr:`${em} ${eh} * * *`,tz:'Asia/Shanghai',session:'isolated',sessionKey:sk,channel:ch,to:userId,announce:true,timeoutSeconds:180,message:`node ${path.join(__dirname,'evening-push.js')} ${userId}`}));
  console.log(`\n✅ ${SKILL} 推送已开启\n⏰ 早推: ${mt}  🌙 晚推: ${et}  📡 渠道: ${ch}\n💡 推送开关状态由 cron 任务本身记录；如需在 MEMORY.md 备注，可记下"daily-vocab 推送 ${ch} ${mt}/${et}"。\n关闭: node push-toggle.js off ${userId}`);
}
function disablePush(userId){
  userId=sanitizeId(userId);
  console.log(`__OPENCLAW_CRON_RM__:${SKILL}-morning-${userId}`);
  console.log(`__OPENCLAW_CRON_RM__:${SKILL}-evening-${userId}`);
  console.log(`✅ ${SKILL} 推送已关闭`);
}
function showStatus(userId){
  userId=sanitizeId(userId);
  console.log(`\n📡 ${SKILL} — ${userId}\n推送状态由 cron 任务记录：可用 \`openclaw cron list\` 查看 ${SKILL}-morning-${userId} / ${SKILL}-evening-${userId} 是否存在。\n`);
}
if(require.main!==module)return;
const[cmd,uid,...rest]=process.argv.slice(2);
if(!cmd||!uid){console.log('用法: node push-toggle.js on|off|status <userId>');process.exit(1);}
const opts={};
const mi=rest.indexOf('--morning');if(mi!==-1)opts.morning=rest[mi+1];
const ei=rest.indexOf('--evening');if(ei!==-1)opts.evening=rest[ei+1];
const ci=rest.indexOf('--channel');if(ci!==-1)opts.channel=rest[ci+1];
if(cmd==='on')enablePush(uid,opts);
else if(cmd==='off')disablePush(uid);
else if(cmd==='status')showStatus(uid);
else{console.error('❌ 未知命令:'+cmd);process.exit(1);}
