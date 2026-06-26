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
console.log(`早安！今天是${weekday}（${date}）。请选一个有趣实用的中文成语或俗语（主题轮换：周一励志/周二智慧/周三友情/周四财富/周五趣味/周六历史/周日生活），呈现：①成语原文（大字）+拼音②英文意译③出处典故（50-80字）④现代用法（1-2句）⑤中文例句×2（含翻译）⑥近义词1个+反义词1个⑦记忆口诀。结尾出1道选择题，答案晚间揭晓。`);
