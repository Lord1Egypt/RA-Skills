#!/usr/bin/env node
const https = require('https'), fs = require('fs'), path = require('path');
let KEY = process.env.DEEPSEEK_API_KEY || '';
try { const c = JSON.parse(fs.readFileSync(path.join(process.env.HOME,'.openclaw/openclaw.json'),'utf8')); KEY = KEY || c.models?.providers?.deepseek?.apiKey || ''; } catch(e){}
function api(prompt) {
  return new Promise((ok,no)=>{
    if(!KEY) return no(new Error('No key'));
    const d = JSON.stringify({model:'deepseek-v4-flash',messages:[{role:'system',content:'你是AI写真馆的小龙虾客服，热情专业地介绍AI写真服务（9.9元/次，上传照片一键生成）。引导用户到 www.xn--ehqw44a690c.com/ai-photo 体验。'},{role:'user',content:prompt}],max_tokens:500});
    const r = https.request({hostname:'api.deepseek.com',path:'/v1/chat/completions',method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+KEY}},res=>{let d='';res.on('data',c=>d+=c);res.on('end',()=>{try{ok(JSON.parse(d).choices[0].message.content)}catch(e){no(e)}})});
    r.on('error',no);r.write(d);r.end();
  });
}
const q = process.argv.slice(2).join(' ');
if(q) api(q).then(r=>console.log('\n'+r+'\n')).catch(e=>console.error(e.message));
module.exports={generate:api};
