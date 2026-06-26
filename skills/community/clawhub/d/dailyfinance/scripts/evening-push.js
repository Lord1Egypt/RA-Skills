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
console.log(`请搜索今日（${date}）全球财经收盘情况，生成晚间财经复盘。包含：美股/A股/港股收盘数据与涨跌、今日最重磅财经事件3-4条复盘、明日重点关注（数据/财报/事件预告）。中英双语。`);
