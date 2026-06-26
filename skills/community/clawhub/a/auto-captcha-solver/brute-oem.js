const fs = require('fs');
const sharp = require('sharp');
const { createWorker } = require('tesseract.js');

const img = fs.readFileSync('D:/www/openclaw/captcha-solver/captcha.png');

async function make() {
  const out=[];
  const base = sharp(img).grayscale().normalise().resize(600,180,{fit:'fill'}).median(1).sharpen();
  out.push({name:'base',buf:await base.clone().png().toBuffer()});
  out.push({name:'neg',buf:await base.clone().negate().png().toBuffer()});
  for (const t of [100,120,140,160,180,200]) {
    out.push({name:'thr'+t,buf:await base.clone().threshold(t).png().toBuffer()});
    out.push({name:'negthr'+t,buf:await base.clone().negate().threshold(t).png().toBuffer()});
  }
  const crop = sharp(img).extract({left:10,top:5,width:136,height:34}).resize(680,220,{fit:'fill'}).grayscale().normalise().median(1).sharpen();
  out.push({name:'crop',buf:await crop.clone().png().toBuffer()});
  out.push({name:'cropneg',buf:await crop.clone().negate().png().toBuffer()});
  for (const t of [100,120,140,160,180,200]) {
    out.push({name:'cropthr'+t,buf:await crop.clone().threshold(t).png().toBuffer()});
    out.push({name:'cropnegthr'+t,buf:await crop.clone().negate().threshold(t).png().toBuffer()});
  }
  return out;
}

(async()=>{
  const vars=await make();
  const psms=[7,8,6,13,10];
  const oems=[0,1,2,3];
  const results=[];
  for(const oem of oems){
    const w=await createWorker('eng',oem,{logger:()=>{}});
    await w.setParameters({tessedit_char_whitelist:'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',preserve_interword_spaces:'0',user_defined_dpi:'300'});
    for(const v of vars){
      for(const psm of psms){
        await w.setParameters({tessedit_pageseg_mode:String(psm)});
        const r=await w.recognize(v.buf);
        const text=String(r.data.text||'').replace(/\s+/g,'').replace(/[^A-Za-z0-9]/g,'').toUpperCase();
        if(!text) continue;
        const score=(r.data.confidence||0)-Math.abs(text.length-4)*15;
        results.push({oem,psm,name:v.name,text,conf:Number((r.data.confidence||0).toFixed(2)),score:Number(score.toFixed(2))});
      }
    }
    await w.terminate();
  }

  results.sort((a,b)=>b.score-a.score);
  const hit=results.filter(x=>x.text==='2VM9');
  console.log('hits',hit.length);
  if (hit.length) console.log(JSON.stringify(hit.slice(0,10),null,2));
  console.log(JSON.stringify(results.slice(0,50),null,2));
  process.exit(0);
})().catch(e=>{console.error(e);process.exit(1);});
