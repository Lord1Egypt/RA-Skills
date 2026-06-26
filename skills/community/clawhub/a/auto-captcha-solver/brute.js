const fs = require('fs');
const sharp = require('sharp');
const { createWorker } = require('tesseract.js');

const img = fs.readFileSync('D:/www/openclaw/captcha-solver/captcha.png');

async function variants() {
  const list = [];
  const sizes = [2, 3, 4];
  const thresholds = [110, 125, 140, 155, 170, 185, 200];
  for (const s of sizes) {
    const base = sharp(img).grayscale().normalise().resize({ width: 146 * s, height: 48 * s, fit: 'fill' }).median(1).sharpen();
    list.push({ name: `base-s${s}`, buf: await base.png().toBuffer() });
    list.push({ name: `neg-s${s}`, buf: await base.clone().negate().png().toBuffer() });
    for (const t of thresholds) {
      list.push({ name: `thr${t}-s${s}`, buf: await base.clone().threshold(t).png().toBuffer() });
      list.push({ name: `neg-thr${t}-s${s}`, buf: await base.clone().negate().threshold(t).png().toBuffer() });
    }
  }
  return list;
}

(async () => {
  const worker = await createWorker('eng', 1, { logger: () => {} });
  await worker.setParameters({
    tessedit_char_whitelist: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    preserve_interword_spaces: '0',
    user_defined_dpi: '300'
  });
  const vars = await variants();
  const psms = [7, 8, 6, 13];
  const out = [];
  for (const v of vars) {
    for (const psm of psms) {
      await worker.setParameters({ tessedit_pageseg_mode: String(psm) });
      const r = await worker.recognize(v.buf);
      const text = String(r.data.text || '').replace(/\s+/g, '').replace(/[^A-Za-z0-9]/g, '').toUpperCase();
      if (!text) continue;
      const lenPenalty = Math.abs(text.length - 4) * 20;
      const score = (r.data.confidence || 0) - lenPenalty;
      out.push({ name: v.name, psm, text, conf: Number((r.data.confidence||0).toFixed(2)), score: Number(score.toFixed(2)) });
    }
  }
  out.sort((a,b)=>b.score-a.score);
  console.log(JSON.stringify(out.slice(0,30), null, 2));
  await worker.terminate();
  process.exit(0);
})().catch(async (e) => {
  console.error(e);
  process.exit(1);
});
