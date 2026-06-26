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
console.log(`早安！今天是${weekday}（${date}）。请生成今日日记引导。主题按星期轮换：周一=新的开始与意图、周二=感恩与欣赏、周三=挑战与成长、周四=关系与连接、周五=本周收获复盘、周六=梦想与想象、周日=内心独白。输出：①今日日记主题（标题，中英双语）②引导问题3个（由浅入深）③今日写作提示（具体句子开头）④写作小技巧1条。语气温暖，不评判。`);
