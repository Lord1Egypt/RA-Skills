const fs = require('fs');
const { solveCaptchaImage } = require('./solve');

(async () => {
  const img = fs.readFileSync('D:/www/openclaw/captcha-solver/captcha.png');
  const r = await solveCaptchaImage(img, { debug: true, multiPass: false, ocr: { psmModes: [7] } });
  console.log(JSON.stringify(r, null, 2));
  process.exit(0);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
