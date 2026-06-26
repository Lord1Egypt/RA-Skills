#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path');
const USERS_DIR=path.join(__dirname,'../data/users');
function sanitizeId(v){if(typeof v!=='string'||!/^[a-zA-Z0-9_-]{1,128}$/.test(v)){console.error('invalid userId');process.exit(1);}return v;}
function safeUserPath(u){const r=path.resolve(USERS_DIR,u+'.json');if(!r.startsWith(path.resolve(USERS_DIR)+path.sep)){console.error('illegal path');process.exit(1);}return r;}
function loadUser(u){const f=safeUserPath(u);return fs.existsSync(f)?JSON.parse(fs.readFileSync(f,'utf8')):{};}
const userId=sanitizeId(process.argv[2]||'default');
loadUser(userId);
const now=new Date();
const WEEKDAYS=['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
const wd=now.getDay();
const date=`${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const weekday=WEEKDAYS[wd];
const month=now.getMonth()+1;
const day=now.getDate();
const tomorrow_weekday=WEEKDAYS[(wd+1)%7];
console.log(`英语晚间复习时间🌙（${date}）。请为用户生成今日词汇测验：node scripts/quiz.js ${userId} mixed。逐题互动，完成后调用 node scripts/quiz.js ${userId} --score <分数> 记录成绩。附今日学习打卡总结和明日预告。`);
