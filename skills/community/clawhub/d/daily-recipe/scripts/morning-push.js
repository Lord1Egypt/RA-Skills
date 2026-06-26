#!/usr/bin/env node
'use strict';
const fs=require('fs'),path=require('path');
const USERS_DIR=path.join(__dirname,'../data/users');
const VOCAB_THEMES=["情感词汇", "科学词汇", "艺术文化", "商业词汇", "自然生态", "哲学词汇", "日常生活"];
function sanitizeId(v){if(typeof v!=='string'||!/^[a-zA-Z0-9_-]{1,128}$/.test(v)){console.error('❌ 无效userId');process.exit(1);}return v;}
function safeUserPath(u){const r=path.resolve(USERS_DIR,u+'.json');if(!r.startsWith(path.resolve(USERS_DIR)+path.sep)){console.error('❌ 非法路径');process.exit(1);}return r;}
function loadUser(u){const f=safeUserPath(u);return fs.existsSync(f)?JSON.parse(fs.readFileSync(f,'utf8')):{}}
const userId=sanitizeId(process.argv[2]||'default');
loadUser(userId);
const now=new Date();
const WEEKDAYS=['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
const MONTHS_EN=['January','February','March','April','May','June','July','August','September','October','November','December'];
const wd=now.getDay();
const date=`${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;
const weekday=WEEKDAYS[wd];
const month=now.getMonth()+1;
const day=now.getDate();
const month_en=MONTHS_EN[now.getMonth()];
const tomorrow_weekday=WEEKDAYS[(wd+1)%7];
const vocab_theme=VOCAB_THEMES[wd];
const tomorrow_vocab_theme=VOCAB_THEMES[(wd+1)%7];
console.log(`今天是${weekday}（${date}），请推荐今日菜谱。轮换菜系（周一中式家常/周二日韩/周三意式/周四东南亚/周五美式/周六法式/周日早午餐）。搜索一道具体菜品，给出：菜名（中英）、难度🔥、时间、食材（≤12项）、步骤（8-10步）、大厨贴士2条、素食替代方案。中英双语。`);
