#!/usr/bin/env node
/**
 * english-daily — 早间推送提示语生成器（无文件写入/读取版）
 * 纯计算：只根据今天日期输出一条 prompt，档案由 Agent 从 MEMORY.md 读取。
 */
'use strict';
function sanitizeId(v){if(typeof v!=='string'||!/^[a-zA-Z0-9_-]{1,128}$/.test(v)){console.error('invalid userId');process.exit(1);}return v;}
const userId=sanitizeId(process.argv[2]||'default');
const now=new Date();
const WEEKDAYS=['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
const date=`${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const weekday=WEEKDAYS[now.getDay()];
console.log(`今天是${weekday}（${date}）。请为用户 ${userId} 运行今日英语学习推送：先从 MEMORY.md 读取该用户 <!-- english-daily:profile:${userId} --> 区块的 等级/每日目标/streak/last/points/SRS进度，再运行 node scripts/daily-push.js ${userId} --level <等级> --goal <目标> --progress '<SRS进度JSON>' --streak <n> --longest <n> --last <日期> --points <n>。输出今日复习词汇+新词列表，附早间学习激励一句话（英文），并用脚本输出的 MEMORY.md 区块回写原生记忆。`);
