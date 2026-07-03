#!/usr/bin/env node
/**
 * english-daily — 晚间复习提示语生成器（无文件写入/读取版）
 * 纯计算：只根据今天日期输出一条 prompt，档案由 Agent 从 MEMORY.md 读取。
 */
'use strict';
function sanitizeId(v){if(typeof v!=='string'||!/^[a-zA-Z0-9_-]{1,128}$/.test(v)){console.error('invalid userId');process.exit(1);}return v;}
const userId=sanitizeId(process.argv[2]||'default');
const now=new Date();
const date=`${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
console.log(`英语晚间复习时间🌙（${date}）。请为用户 ${userId} 生成今日词汇测验：先从 MEMORY.md 读取该用户 <!-- english-daily:profile:${userId} --> 区块的 等级/SRS进度/积分，再运行 node scripts/quiz.js ${userId} mixed --level <等级> --progress '<SRS进度JSON>'。逐题互动，完成后调用 node scripts/quiz.js ${userId} --score <分数> --level <等级> --progress '<SRS进度JSON>' --points <累计积分> 记录成绩，并用脚本输出的 MEMORY.md 区块回写原生记忆。附今日学习打卡总结和明日预告。`);
