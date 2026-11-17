const fs = require('fs');
const path = require('path');
const DIR = __dirname;

function b64(file){
  try { const b = fs.readFileSync(path.join(DIR, file));
    const ext = file.split('.').pop().toLowerCase();
    const mime = ext==='png'?'image/png':(ext==='jpg'||ext==='jpeg')?'image/jpeg':'image/png';
    return `data:${mime};base64,${b.toString('base64')}`;
  } catch(e){ return null; }
}
const PHOTO = b64('_orig25.jpg');

// ---------- brand icons (inline SVG squircles) ----------
const IC = {
  claude: `<div class="ic" style="background:#D97757">
    <svg viewBox="0 0 100 100" width="60%" height="60%">${Array.from({length:14}).map((_,i)=>{const a=(i/14)*Math.PI*2;const x1=50+13*Math.cos(a),y1=50+13*Math.sin(a),x2=50+40*Math.cos(a),y2=50+40*Math.sin(a);return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#1a1a1a" stroke-width="7" stroke-linecap="round"/>`}).join('')}</svg></div>`,
  v0: `<div class="ic" style="background:#000"><span class="v0t">v0</span></div>`,
  supabase: `<div class="ic" style="background:#141414">
    <svg viewBox="0 0 100 100" width="56%" height="56%"><path d="M56 6 L18 54 h30 L44 94 L82 46 H52 Z" fill="#3ECF8E"/></svg></div>`,
  gemini: `<div class="ic" style="background:#0b0b12">
    <svg viewBox="0 0 100 100" width="66%" height="66%"><defs><linearGradient id="gg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4e8cff"/><stop offset="1" stop-color="#b06cff"/></linearGradient></defs><path d="M50 6 C54 30 70 46 94 50 C70 54 54 70 50 94 C46 70 30 54 6 50 C30 46 46 30 50 6 Z" fill="url(#gg)"/></svg></div>`,
  higgsfield: `<div class="ic" style="background:#fff">
    <svg viewBox="0 0 100 100" width="66%" height="66%"><defs><linearGradient id="hf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b6bff"/><stop offset=".5" stop-color="#e0533a"/><stop offset="1" stop-color="#f0a93a"/></linearGradient></defs><path d="M18 78 L46 20 L54 20 L82 78 L70 78 L50 34 L30 78 Z" fill="url(#hf)"/><path d="M64 78 L82 40 L86 78 Z" fill="url(#hf)"/></svg></div>`,
  vercel: `<div class="ic" style="background:#000"><svg viewBox="0 0 100 100" width="56%" height="56%"><path d="M50 18 L86 80 H14 Z" fill="#fff"/></svg></div>`,
};

const CSS = `
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
.slide{position:relative;width:1080px;height:1350px;overflow:hidden;color:#fff;
  font-family:-apple-system,'Helvetica Neue',Helvetica,Arial}
.bg{position:absolute;inset:0;background-size:cover;background-repeat:no-repeat}
.v0t{font:800 44px/1 -apple-system;color:#fff;letter-spacing:-2px}
.ic{width:100%;height:100%;border-radius:24%;display:flex;align-items:center;justify-content:center;
  box-shadow:0 12px 26px rgba(0,0,0,.55)}
.iconrow{position:absolute;left:60px;right:60px;bottom:74px;display:flex;gap:18px;justify-content:space-between;z-index:6}
.iconrow .cell{width:132px;height:132px}
.eyebrow{position:absolute;top:66px;left:70px;font:700 23px/1 -apple-system;letter-spacing:5px;color:rgba(255,255,255,.72);text-transform:uppercase;z-index:6;text-shadow:0 2px 12px rgba(0,0,0,.8)}
.handle{position:absolute;top:66px;right:70px;font:600 23px/1 -apple-system;color:rgba(255,255,255,.72);letter-spacing:1px;z-index:6;text-shadow:0 2px 12px rgba(0,0,0,.8)}
.serif{font-family:Georgia,'Times New Roman',serif}

/* ---- cover ---- */
.h1{position:absolute;left:70px;top:300px;width:820px;z-index:6;text-shadow:0 4px 30px rgba(0,0,0,.75)}
.h1 .a{font:800 116px/0.96 -apple-system;letter-spacing:-4px}
.h1 .b{font:italic 500 84px/1.06 Georgia,serif;color:#f3efe7}
.h1 .c{font:italic 800 128px/0.98 Georgia,serif}
.h1 .sub{display:block;margin-top:20px;font:italic 500 52px/1 Georgia,serif;color:#efe7d8}

/* ---- app slide ---- */
.num{position:absolute;top:150px;left:0;right:0;text-align:center;font:400 62px/1 Georgia,serif;color:#fff;z-index:6;text-shadow:0 3px 18px rgba(0,0,0,.8)}
.head{position:absolute;top:250px;left:60px;right:60px;display:flex;align-items:center;justify-content:center;gap:26px;z-index:6}
.head .icw{width:132px;height:132px;flex:0 0 auto}
.head .ttl{font:800 78px/0.98 -apple-system;letter-spacing:-2px;text-shadow:0 3px 20px rgba(0,0,0,.8)}
.head .ttl small{display:block;font:400 44px/1.1 Georgia,serif;color:#e9e2d4;letter-spacing:0;margin-top:8px}
.desc{position:absolute;top:430px;left:90px;right:90px;text-align:center;
  font:400 44px/1.35 Georgia,serif;color:#f4f1ea;z-index:6;text-shadow:0 3px 18px rgba(0,0,0,.85)}
.shotwrap{position:absolute;left:50%;transform:translateX(-50%);bottom:150px;width:720px;z-index:6}
.shot{width:100%;border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,.14);
  box-shadow:0 40px 90px rgba(0,0,0,.7);background:#0c0c12}
.shot .bar{height:44px;background:#16161d;display:flex;align-items:center;gap:9px;padding-left:16px;border-bottom:1px solid #24242e}
.shot .bar i{width:12px;height:12px;border-radius:50%}
.shot .body{overflow:hidden;max-height:430px}
.shot .body img{width:100%;display:block}
.shot.contain .body{background:#0b0b10;display:flex;align-items:center;justify-content:center;height:430px}
.shot.contain .body img{width:100%;height:100%;object-fit:contain}
.arrow{position:absolute;z-index:6}
.tag{position:absolute;right:64px;bottom:96px;font:700 20px/1 -apple-system;letter-spacing:2px;color:#7fe3ad;
  border:1px solid rgba(127,227,173,.4);background:rgba(62,207,142,.12);padding:8px 14px;border-radius:999px;z-index:7}

/* ---- cta ---- */
.cta{position:absolute;left:70px;right:70px;top:330px;z-index:6;text-shadow:0 4px 26px rgba(0,0,0,.8)}
.cta .k{font:800 128px/0.95 -apple-system;letter-spacing:-5px}
.cta .s{margin-top:28px;font:italic 500 58px/1.18 Georgia,serif;color:#f3efe7}
.cta .word{color:#F0B24A}
.ctabox{position:absolute;left:70px;right:70px;bottom:200px;padding:34px 40px;border-radius:22px;
  background:rgba(10,8,4,.55);backdrop-filter:blur(4px);border:1px solid rgba(240,178,74,.4);z-index:6}
.ctabox p{font:600 38px/1.35 -apple-system;color:#f6efe1}
`;

// gradient overlays
const COVER_OVL = `background:linear-gradient(180deg, rgba(5,5,9,.64) 0%, rgba(5,5,9,.42) 30%, rgba(5,5,9,.55) 62%, rgba(5,5,9,.93) 100%);position:absolute;inset:0;z-index:2`;
const APP_OVL   = `background:linear-gradient(180deg, rgba(4,4,7,.82) 0%, rgba(4,4,7,.72) 45%, rgba(4,4,7,.9) 100%);position:absolute;inset:0;z-index:2`;

function iconRow(){
  const order=['claude','v0','supabase','gemini','higgsfield','vercel'];
  return `<div class="iconrow">${order.map(k=>`<div class="cell">${IC[k]}</div>`).join('')}</div>`;
}
function coverBg(){return `<div class="bg" style="background-image:url('${PHOTO}');background-position:50% 32%"></div><div style="${COVER_OVL}"></div>`;}
function appBg(){return `<div class="bg" style="background-image:url('${PHOTO}');background-position:50% 20%;filter:blur(22px) saturate(.7) brightness(.7);transform:scale(1.1)"></div><div style="${APP_OVL}"></div>`;}

function cover(){
  return `<div class="slide">${coverBg()}
   <div class="eyebrow">Mi stack de IA</div>
   <div class="handle">@tuhandle</div>
   <div class="h1">
     <div class="a">Las 6 apps</div>
     <div class="b">con las que creo</div>
     <div class="c">mis apps</div>
     <span class="sub">(de contenido con IA)</span>
   </div>
   ${iconRow()}
  </div>`;
}

const APPS=[
  {k:'claude',n:'Claude Code',sub:'(Programador con IA)',d:"Le hablo en español y me escribe el código de la app. Regla #1: entiende tu arquitectura — no le hagas ‘vibe code’ a todo.",shot:'1-claude-code.png',contain:true,pos:'50% 50%'},
  {k:'v0',n:'v0',sub:'(Diseño de interfaz)',d:'Convierte una idea en la interfaz de la app en segundos. Aquí nacen y viven todas mis apps.',shot:'2-v0.png',pos:'50% 0%'},
  {k:'supabase',n:'Supabase',sub:'(Base de datos)',d:'El backend completo: usuarias, contenido y datos, todo guardado y seguro.',shot:'3-supabase.png',pos:'50% 4%'},
  {k:'gemini',n:'Gemini',sub:'(El cerebro de IA)',d:'El motor de inteligencia artificial que corre por dentro de cada app que creo.',shot:'4-gemini.png',pos:'50% 2%'},
  {k:'higgsfield',n:'Higgsfield',sub:'(Imágenes y video IA)',d:'Genera las imágenes y los videos con IA para el contenido de las apps.',shot:'5-higgsfield.png',pos:'50% 0%'},
  {k:'vercel',n:'Vercel',sub:'(Publicación / hosting)',d:'Publica la app en internet, lista para el mundo, en un solo clic.',shot:'6-vercel.png',pos:'50% 0%'},
];

const ARROW = `<svg class="arrow" style="left:730px;bottom:590px" width="150" height="150" viewBox="0 0 150 150"><path d="M20 15 C90 5 130 45 118 110" fill="none" stroke="rgba(255,255,255,.75)" stroke-width="5" stroke-linecap="round"/><path d="M100 100 L120 116 L128 92" fill="none" stroke="rgba(255,255,255,.75)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

function appSlide(app,idx){
  const shot=b64(app.shot);
  let inner;
  if(shot){
    inner = app.contain
      ? `<div class="shot contain"><div class="bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i></div><div class="body"><img src="${shot}"></div></div>`
      : `<div class="shot"><div class="bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i></div><div class="body"><img style="object-fit:cover;object-position:${app.pos}" src="${shot}"></div></div>`;
  } else {
    inner = `<div class="shot contain"><div class="bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i></div><div class="body"><span style="font:600 30px/1.4 -apple-system;color:#777;text-align:center">captura de ${app.n}<br>pendiente</span></div></div>`;
  }
  return `<div class="slide">${appBg()}
    <div class="num">#${idx+1}</div>
    <div class="head"><div class="icw">${IC[app.k]}</div><div class="ttl">${app.n}<small>${app.sub}</small></div></div>
    <div class="desc">${app.d}</div>
    <div class="shotwrap">${inner}</div>
    ${ARROW}
    ${shot?'<div class="tag">CAPTURA REAL</div>':''}
  </div>`;
}

function cta(){
  return `<div class="slide">${coverBg()}
   <div class="eyebrow">Mi stack de IA</div>
   <div class="handle">@tuhandle</div>
   <div class="cta">
     <div class="k">¿Quieres<br>el stack?</div>
     <div class="s">Comenta <span class="word">“APP”</span> y te mando<br>la guía completa por DM 👽</div>
   </div>
   <div class="ctabox"><p>💜 En <b>FÓRMULA 100K</b> te enseño a crear tus propias apps de contenido con IA — sin saber programar.</p></div>
  </div>`;
}

function page(inner){return `<!doctype html><html><head><meta charset="utf-8"><style>${CSS}</style></head><body>${inner}</body></html>`;}
const slides=[cover(),...APPS.map(appSlide),cta()];
slides.forEach((s,i)=>fs.writeFileSync(path.join(DIR,`slide-${String(i+1).padStart(2,'0')}.html`),page(s)));
console.log('wrote',slides.length,'slides');
