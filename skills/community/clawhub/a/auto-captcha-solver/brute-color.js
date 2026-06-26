const fs = require('fs');
const sharp = require('sharp');
const { createWorker } = require('tesseract.js');

const img = fs.readFileSync('D:/www/openclaw/captcha-solver/captcha.png');

async function buildVariants() {
  const out = [];
  const scales = [3,4,5];
  const thresholds=[90,110,130,150,170,190,210];
  for (const s of scales) {
    const w=150*s,h=43*s;
    const yellow = sharp(img)
      .resize(w,h,{fit:'fill'})
      .recomb([
        [1.2, 1.2, -1.3],
        [1.2, 1.2, -1.3],
        [1.2, 1.2, -1.3]
      ])
      .grayscale()
      .normalise()
      .median(1)
      .sharpen();
    out.push({name:`yellow-s${s}`,buf:await yellow.clone().png().toBuffer()});
    for (const t of thresholds) {
      out.push({name:`yellow-thr${t}-s${s}`,buf:await yellow.clone().threshold(t).png().toBuffer()});
      out.push({name:`yellow-neg-thr${t}-s${s}`,buf:await yellow.clone().negate().threshold(t).png().toBuffer()});
    }

    const centerCrop = sharp(img)
      .extract({left:8, top:6, width:138, height:33})
      .resize(138*s,33*s,{fit:'fill'})
      .recomb([
        [1.2, 1.2, -1.3],
        [1.2, 1.2, -1.3],
        [1.2, 1.2, -1.3]
      ])
      .grayscale()
      .normalise()
      .median(1)
      .sharpen();
    out.push({name:`crop-yellow-s${s}`,buf:await centerCrop.clone().png().toBuffer()});
    for (const t of thresholds) {
      out.push({name:`crop-yellow-thr${t}-s${s}`,buf:await centerCrop.clone().threshold(t).png().toBuffer()});
      out.push({name:`crop-yellow-neg-thr${t}-s${s}`,buf:await centerCrop.clone().negate().threshold(t).png().toBuffer()});
    }
  }
  return out;
}

(async()=>{
  const worker = await createWorker('eng',1,{logger:()=>{}});
  await worker.setParameters({tessedit_char_whitelist:'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',preserve_interword_spaces:'0',user_defined_dpi:'300'});
  const vars=await buildVariants();
  const psms=[7,8,6,13];
  const rs=[];
  for(const v of vars){
    for(const psm of psms){
      await worker.setParameters({tessedit_pageseg_mode:String(psm)});
      const r=await worker.recognize(v.buf);
      const text=String(r.data.text||'').replace(/\s+/g,'').replace(/[^A-Za-z0-9]/g,'').toUpperCase();
      if(!text) continue;
      const score=(r.data.confidence||0)-Math.abs(text.length-4)*18;
      rs.push({name:v.name,psm,text,conf:Number((r.data.confidence||0).toFixed(2)),score:Number(score.toFixed(2))});
    }
  }
  rs.sort((a,b)=>b.score-a.score);
  const hit=rs.find(x=>x.text==='2VM9');
  console.log('hit',hit||null);
  console.log(JSON.stringify(rs.slice(0,40),null,2));
  await worker.terminate();
  process.exit(0);
})().catch(e=>{console.error(e);process.exit(1);});
