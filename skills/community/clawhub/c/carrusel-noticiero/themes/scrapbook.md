# Tema: scrapbook (default)

Estilo visual del CUERPO (slides 2-8) del carrusel noticiero. Paleta crema, tipografías
Caveat + Poppins, post-its, washi tape y stickers emoji. Es el brandkit scrapbook de FÓRMULA 100K.

**Cómo usarlo:** copia el bloque HTML completo de abajo a `<carpeta>/carrusel.html`, y reemplaza
SOLO el copy marcado con `‹…›`. NO toques el `<style>` (está probado). Cada slide ya trae su
`num` (X / 8), `handle` (@tuhandle), tapes, stickers y post-its posicionados.

La portada (slide 1) NO va aquí — se arma con `cover/cover-news.html`. Este archivo cubre slides 2-8.

Roles de slide (deben respetarse aunque cambies el tema): 2=QUÉ PASÓ · 3=EL MOTIVO ·
4=EL DATO QUE ASUSTA · 5=¿Y A TI QUÉ? · 6=CÓMO APROVECHARLO (3 jugadas) ·
7=LA REGLA DE ORO · 8=CIERRE CTA.

---

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Carrusel noticiero — cuerpo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@400;500;600;700&family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --cream: #F5EFE0; --cream-dark: #EDE4CE; --ink: #2B2218;
    --terracota: #C17F5A; --salvia: #8FAF8A; --rojo: #D85A4E;
    --amarillo: #F4C75B; --morado: #B68EC8; --verde: #9BC289;
    --azul: #7FA9C9; --rosa: #E8A8B8;
    --postit-yellow: #FFE881; --postit-pink: #FFCAD4; --postit-green: #CCE3B5;
    --postit-blue: #BFD8E8; --postit-purple: #DCC8E8;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background:#1a1a1a; font-family:'Poppins',sans-serif; padding:40px 0;
    display:flex; flex-direction:column; align-items:center; gap:40px; }
  .slide { width:1080px; height:1350px; position:relative; overflow:hidden;
    background: var(--cream);
    background-image:
      radial-gradient(circle at 20% 30%, rgba(193,127,90,0.04) 0%, transparent 40%),
      radial-gradient(circle at 80% 70%, rgba(143,175,138,0.04) 0%, transparent 40%),
      url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.2  0 0 0 0 0.15  0 0 0 0 0.1  0 0 0 0.08 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
    color: var(--ink); box-shadow:0 20px 60px rgba(0,0,0,0.4); }
  .tape { position:absolute; width:140px; height:32px; background:rgba(255,232,129,0.55);
    border-left:1px dashed rgba(0,0,0,0.08); border-right:1px dashed rgba(0,0,0,0.08);
    box-shadow:0 2px 4px rgba(0,0,0,0.08); }
  .postit { position:absolute; padding:18px 22px; box-shadow:3px 5px 12px rgba(0,0,0,0.18);
    font-family:'Caveat',cursive; font-weight:600; }
  .postit::after { content:''; position:absolute; top:-8px; left:50%; transform:translateX(-50%);
    width:60px; height:16px; background:rgba(255,232,129,0.6); }
  .doodle { position:absolute; pointer-events:none; }
  .sticker { position:absolute; font-size:80px; filter:drop-shadow(2px 4px 6px rgba(0,0,0,0.2)); }
  .num { position:absolute; bottom:28px; right:36px; font-family:'Caveat',cursive; font-size:28px; color:rgba(43,34,24,0.45); }
  .handle { position:absolute; bottom:28px; left:36px; font-family:'Poppins',sans-serif; font-size:18px; font-weight:500; color:rgba(43,34,24,0.55); letter-spacing:0.5px; }

  /* S2 — QUÉ PASÓ (tag rojo) */
  .s2 .tape-1 { top:60px; left:400px; transform:rotate(-3deg); background:rgba(216,90,78,0.45); }
  .s2-tag { position:absolute; top:108px; left:80px; background:var(--rojo); color:#fff; padding:14px 32px; font-family:'Poppins'; font-weight:800; font-size:26px; letter-spacing:2px; transform:rotate(-3deg); box-shadow:4px 6px 12px rgba(0,0,0,0.2); }
  .s2-title { position:absolute; top:210px; left:70px; width:940px; font-family:'Caveat'; font-weight:700; font-size:118px; line-height:0.95; color:var(--ink); transform:rotate(-1deg); }
  .s2-title .red { color:var(--rojo); display:inline-block; transform:rotate(2deg); }
  .s2-content { position:absolute; top:560px; left:90px; width:900px; font-family:'Poppins'; font-size:31px; line-height:1.5; color:var(--ink); }
  .s2-content p { margin-bottom:26px; } .s2-content .bold { font-weight:700; } .s2-content .hl { background:var(--postit-yellow); padding:2px 10px; }
  .s2-postit { bottom:120px; right:80px; background:var(--postit-yellow); width:300px; transform:rotate(4deg); font-size:32px; color:var(--ink); text-align:center; line-height:1.15; }
  .s2 .sticker-1 { top:66px; right:100px; font-size:92px; transform:rotate(-10deg); }
  .s2 .sticker-2 { bottom:300px; left:70px; font-size:78px; transform:rotate(12deg); }

  /* S3 — EL MOTIVO (tag amarillo) */
  .s3 .tape-1 { top:50px; right:380px; transform:rotate(8deg); background:rgba(244,199,91,0.55); }
  .s3-tag { position:absolute; top:108px; right:80px; background:var(--amarillo); color:var(--ink); padding:14px 32px; font-family:'Poppins'; font-weight:800; font-size:24px; letter-spacing:2px; transform:rotate(3deg); box-shadow:4px 6px 12px rgba(0,0,0,0.2); }
  .s3-title { position:absolute; top:210px; left:70px; width:940px; font-family:'Caveat'; font-weight:700; font-size:120px; line-height:0.95; color:var(--ink); text-align:center; transform:rotate(-1deg); }
  .s3-title .yellow { background:var(--postit-yellow); padding:0 16px; display:inline-block; transform:rotate(2deg); }
  .s3-emoji { position:absolute; top:470px; left:50%; transform:translateX(-50%) rotate(-5deg); font-size:128px; filter:drop-shadow(2px 4px 6px rgba(0,0,0,0.2)); }
  .s3-content { position:absolute; top:680px; left:90px; width:900px; font-family:'Poppins'; font-size:31px; line-height:1.5; color:var(--ink); text-align:center; }
  .s3-content p { margin-bottom:26px; } .s3-content .bold { font-weight:700; } .s3-content .hl { background:var(--postit-pink); padding:2px 10px; }
  .s3-postit { bottom:110px; left:80px; background:var(--postit-pink); width:330px; transform:rotate(-4deg); font-size:30px; color:var(--ink); text-align:center; line-height:1.15; }
  .s3 .sticker-1 { top:90px; left:90px; font-size:82px; transform:rotate(-12deg); }
  .s3 .sticker-2 { bottom:300px; right:90px; font-size:76px; transform:rotate(10deg); }

  /* S4 — EL DATO QUE ASUSTA (hero) */
  .s4 .tape-1 { top:50px; left:100px; transform:rotate(-7deg); background:rgba(216,90,78,0.45); }
  .s4 .tape-2 { top:70px; right:90px; transform:rotate(6deg); background:rgba(244,199,91,0.55); }
  .s4-tag { position:absolute; top:140px; left:50%; transform:translateX(-50%) rotate(-2deg); background:var(--ink); color:#fff; padding:14px 34px; font-family:'Poppins'; font-weight:800; font-size:24px; letter-spacing:2px; box-shadow:4px 6px 12px rgba(0,0,0,0.2); white-space:nowrap; }
  .s4-intro { position:absolute; top:300px; left:90px; width:900px; font-family:'Poppins'; font-size:32px; line-height:1.45; color:var(--ink); text-align:center; }
  .s4-intro .bold { font-weight:700; } .s4-intro .hl { background:var(--postit-yellow); padding:2px 10px; }
  .s4-title { position:absolute; top:560px; left:60px; width:960px; font-family:'Caveat'; font-weight:700; font-size:150px; line-height:0.9; color:var(--ink); text-align:center; transform:rotate(-1deg); }
  .s4-title .red { color:var(--rojo); display:inline-block; transform:rotate(2deg); }
  .s4-sub { position:absolute; top:960px; left:50%; transform:translateX(-50%) rotate(-1deg); font-family:'Caveat'; font-size:52px; color:var(--terracota); text-align:center; width:860px; }
  .s4 .sticker-1 { top:250px; right:90px; font-size:84px; transform:rotate(12deg); }
  .s4 .sticker-2 { bottom:210px; left:90px; font-size:80px; transform:rotate(-12deg); }
  .s4 .sticker-3 { bottom:220px; right:110px; font-size:74px; transform:rotate(10deg); }

  /* S5 — ¿Y A TI QUÉ? (tag salvia) */
  .s5 .tape-1 { top:56px; right:200px; transform:rotate(6deg); background:rgba(143,175,138,0.5); }
  .s5-tag { position:absolute; top:108px; left:80px; background:var(--salvia); color:#fff; padding:14px 32px; font-family:'Poppins'; font-weight:800; font-size:24px; letter-spacing:2px; transform:rotate(-3deg); box-shadow:4px 6px 12px rgba(0,0,0,0.2); }
  .s5-title { position:absolute; top:210px; left:70px; width:940px; font-family:'Caveat'; font-weight:700; font-size:124px; line-height:0.92; color:var(--ink); transform:rotate(-1deg); }
  .s5-title .amp { background:var(--postit-yellow); padding:0 14px; display:inline-block; transform:rotate(2deg); }
  .s5-content { position:absolute; top:620px; left:90px; width:900px; font-family:'Poppins'; font-size:32px; line-height:1.5; color:var(--ink); }
  .s5-content p { margin-bottom:26px; } .s5-content .bold { font-weight:700; } .s5-content .hl { background:var(--postit-green); padding:2px 10px; }
  .s5-postit { bottom:120px; right:80px; background:var(--postit-green); width:330px; transform:rotate(4deg); font-size:32px; color:var(--ink); text-align:center; line-height:1.15; }
  .s5 .sticker-1 { top:80px; left:110px; font-size:80px; transform:rotate(-10deg); }
  .s5 .sticker-2 { bottom:300px; left:80px; font-size:74px; transform:rotate(12deg); }

  /* S6 — CÓMO APROVECHARLO (lista numerada) */
  .s6 .tape-1 { top:50px; left:90px; transform:rotate(-6deg); background:rgba(244,199,91,0.55); }
  .s6 .tape-2 { top:60px; right:100px; transform:rotate(7deg); background:rgba(193,127,90,0.4); }
  .s6-tag { position:absolute; top:120px; left:50%; transform:translateX(-50%) rotate(-2deg); background:var(--amarillo); color:var(--ink); padding:14px 34px; font-family:'Poppins'; font-weight:800; font-size:24px; letter-spacing:2px; box-shadow:4px 6px 12px rgba(0,0,0,0.2); white-space:nowrap; }
  .s6-title { position:absolute; top:210px; left:70px; width:940px; font-family:'Caveat'; font-weight:700; font-size:112px; line-height:0.92; color:var(--ink); text-align:center; transform:rotate(-1deg); }
  .s6-title .hl { background:var(--postit-yellow); padding:0 14px; display:inline-block; transform:rotate(2deg); }
  .s6-list { position:absolute; top:470px; left:110px; width:860px; font-family:'Poppins'; font-size:31px; line-height:1.4; color:var(--ink); }
  .s6-list .item { margin-bottom:40px; padding-left:96px; position:relative; min-height:84px; }
  .s6-list .n { position:absolute; left:0; top:-6px; width:64px; height:64px; border-radius:50%; background:var(--rojo); color:#fff; font-weight:800; font-size:34px; display:flex; align-items:center; justify-content:center; box-shadow:3px 4px 8px rgba(0,0,0,0.2); transform:rotate(-4deg); }
  .s6-list .bold { font-weight:700; color:var(--terracota); } .s6-list .hl { background:var(--postit-yellow); padding:1px 8px; }
  .s6 .sticker-1 { bottom:150px; right:90px; font-size:92px; transform:rotate(12deg); }
  .s6 .sticker-2 { bottom:160px; left:90px; font-size:76px; transform:rotate(-12deg); }

  /* S7 — LA REGLA DE ORO (hero) */
  .s7hero .tape-1 { top:54px; left:120px; transform:rotate(-7deg); background:rgba(216,90,78,0.5); }
  .s7hero .tape-2 { top:66px; right:110px; transform:rotate(8deg); background:rgba(244,199,91,0.55); }
  .s7hero-tag { position:absolute; top:140px; left:50%; transform:translateX(-50%) rotate(-2deg); background:var(--rojo); color:#fff; padding:14px 34px; font-family:'Poppins'; font-weight:800; font-size:24px; letter-spacing:2px; box-shadow:4px 6px 12px rgba(0,0,0,0.2); white-space:nowrap; }
  .s7hero-intro { position:absolute; top:290px; left:90px; width:900px; font-family:'Poppins'; font-size:32px; line-height:1.5; color:var(--ink); text-align:center; }
  .s7hero-intro .bold { font-weight:700; } .s7hero-intro .hl { background:var(--postit-yellow); padding:2px 10px; }
  .s7hero-title { position:absolute; top:640px; left:60px; width:960px; font-family:'Caveat'; font-weight:700; font-size:170px; line-height:0.88; color:var(--ink); text-align:center; transform:rotate(-1.5deg); }
  .s7hero-title .red { color:var(--rojo); }
  .s7hero-sub { position:absolute; top:940px; left:50%; transform:translateX(-50%) rotate(-1deg); font-family:'Caveat'; font-size:52px; color:var(--terracota); text-align:center; width:860px; }
  .s7hero .sticker-1 { top:250px; right:100px; font-size:82px; transform:rotate(12deg); }
  .s7hero .sticker-2 { bottom:200px; left:100px; font-size:80px; transform:rotate(-12deg); }
  .s7hero .sticker-3 { bottom:210px; right:120px; font-size:74px; transform:rotate(10deg); }

  /* S8 — CIERRE CTA */
  .s8 .tape-1 { top:50px; left:90px; transform:rotate(-6deg); background:rgba(193,127,90,0.45); }
  .s8 .tape-2 { top:50px; right:90px; transform:rotate(8deg); background:rgba(244,199,91,0.55); }
  .s8-pretag { position:absolute; top:128px; left:50%; transform:translateX(-50%) rotate(-2deg); font-family:'Caveat'; font-size:46px; color:var(--terracota); }
  .s8-title { position:absolute; top:205px; left:70px; width:940px; font-family:'Caveat'; font-weight:700; font-size:118px; line-height:0.92; color:var(--ink); text-align:center; transform:rotate(-1deg); }
  .s8-title .hl { background:var(--postit-yellow); padding:0 18px; display:inline-block; transform:rotate(2deg); }
  .s8-intro { position:absolute; top:470px; left:90px; width:900px; font-family:'Poppins'; font-size:30px; line-height:1.45; color:var(--ink); text-align:center; }
  .s8-intro .bold { font-weight:700; }
  .s8-list { position:absolute; top:660px; left:150px; width:780px; font-family:'Poppins'; font-size:28px; line-height:1.5; color:var(--ink); }
  .s8-list .item { margin-bottom:16px; padding-left:50px; position:relative; }
  .s8-list .item::before { content:'→'; position:absolute; left:0; color:var(--terracota); font-weight:700; font-size:30px; }
  .s8-list .bold { font-weight:700; color:var(--terracota); }
  .s8-cta { position:absolute; bottom:236px; left:50%; transform:translateX(-50%) rotate(-1deg); background:var(--rojo); color:#fff; padding:22px 50px; font-family:'Poppins'; font-weight:800; font-size:32px; box-shadow:5px 7px 14px rgba(0,0,0,0.25); text-align:center; letter-spacing:0.5px; }
  .s8-save { position:absolute; bottom:124px; left:50%; transform:translateX(-50%) rotate(-2deg); font-family:'Caveat'; font-size:42px; color:var(--ink); text-align:center; width:760px; }
  .s8-save .pin { background:var(--postit-pink); padding:2px 14px; transform:rotate(-2deg); display:inline-block; }
  .s8 .sticker-1 { top:96px; right:210px; font-size:92px; transform:rotate(-10deg); }
  .s8 .sticker-2 { top:104px; left:210px; font-size:80px; transform:rotate(14deg); }
  .s8 .sticker-3 { bottom:210px; right:100px; font-size:70px; transform:rotate(15deg); }
</style>
</head>
<body>

<!-- S2 — QUÉ PASÓ -->
<div class="slide s2">
  <div class="tape tape-1"></div>
  <div class="sticker sticker-1">‹⚡›</div>
  <div class="sticker sticker-2">‹🔌›</div>
  <div class="s2-tag">QUÉ PASÓ 📰</div>
  <div class="s2-title">‹titular corto<br><span class="red">clave›</span></div>
  <div class="s2-content">
    <p>‹Frase 1 del hecho con <span class="bold">nombre real</span> y <span class="hl">dato clave</span>.›</p>
    <p>‹Frase 2: cuándo/quién, hechos verificables.›</p>
  </div>
  <div class="postit s2-postit">‹dato<br>en post-it ✅›</div>
  <div class="num">2 / 8</div>
  <div class="handle">@tuhandle</div>
</div>

<!-- S3 — EL MOTIVO -->
<div class="slide s3">
  <div class="tape tape-1"></div>
  <div class="sticker sticker-1">‹🔒›</div>
  <div class="sticker sticker-2">‹😳›</div>
  <div class="s3-tag">EL MOTIVO ⚠️</div>
  <div class="s3-title">‹El giro<br>con <span class="yellow">énfasis›</span></div>
  <div class="s3-emoji">‹🚫›</div>
  <div class="s3-content">
    <p>‹Por qué pasó, frase corta.›</p>
    <p>¿La razón? <span class="hl">‹la causa real›</span>.</p>
  </div>
  <div class="postit s3-postit">‹remate<br>en post-it 😵›</div>
  <div class="num">3 / 8</div>
  <div class="handle">@tuhandle</div>
</div>

<!-- S4 — EL DATO QUE ASUSTA -->
<div class="slide s4">
  <div class="tape tape-1"></div>
  <div class="tape tape-2"></div>
  <div class="sticker sticker-1">‹🌎›</div>
  <div class="sticker sticker-2">‹🏛️›</div>
  <div class="sticker sticker-3">‹😬›</div>
  <div class="s4-tag">EL DATO QUE ASUSTA</div>
  <div class="s4-intro">‹Contexto del insight con <span class="hl">frase clave</span>. Y <span class="bold">el giro…</span>›</div>
  <div class="s4-title">‹es <span class="red">lo hero›</span></div>
  <div class="s4-sub">~ ‹subtítulo que resume el insight› ~</div>
  <div class="num">4 / 8</div>
  <div class="handle">@tuhandle</div>
</div>

<!-- S5 — ¿Y A TI QUÉ? -->
<div class="slide s5">
  <div class="tape tape-1"></div>
  <div class="sticker sticker-1">‹👀›</div>
  <div class="sticker sticker-2">‹📈›</div>
  <div class="s5-tag">¿Y A TI QUÉ? 🤔</div>
  <div class="s5-title">‹Aquí está lo<br>que nadie <span class="amp">te dice›</span></div>
  <div class="s5-content">
    <p>‹Cada vez que la IA es noticia, <span class="bold">la atención se dispara.</span>›</p>
    <p>‹Y la atención es la <span class="hl">materia prima</span> de tu contenido.›</p>
    <p>‹La noticia trabaja para ti… <span class="bold">si te subes a tiempo.</span>›</p>
  </div>
  <div class="postit s5-postit">‹analogía<br>en post-it 🌊›</div>
  <div class="num">5 / 8</div>
  <div class="handle">@tuhandle</div>
</div>

<!-- S6 — CÓMO APROVECHARLO -->
<div class="slide s6">
  <div class="tape tape-1"></div>
  <div class="tape tape-2"></div>
  <div class="sticker sticker-1">‹🚀›</div>
  <div class="sticker sticker-2">‹✍️›</div>
  <div class="s6-tag">CÓMO APROVECHARLO</div>
  <div class="s6-title"><span class="hl">‹3 jugadas›</span><br>‹para hoy›</div>
  <div class="s6-list">
    <div class="item"><span class="n">1</span><span class="bold">‹Jugada 1.›</span> ‹Explicación con <span class="hl">término</span>.›</div>
    <div class="item"><span class="n">2</span><span class="bold">‹Jugada 2.›</span> ‹Explicación accionable.›</div>
    <div class="item"><span class="n">3</span><span class="bold">‹Jugada 3.›</span> ‹Explicación con <span class="hl">término</span>.›</div>
  </div>
  <div class="num">6 / 8</div>
  <div class="handle">@tuhandle</div>
</div>

<!-- S7 — LA REGLA DE ORO -->
<div class="slide s7hero">
  <div class="tape tape-1"></div>
  <div class="tape tape-2"></div>
  <div class="sticker sticker-1">‹⏳›</div>
  <div class="sticker sticker-2">‹🔥›</div>
  <div class="sticker sticker-3">‹⚡›</div>
  <div class="s7hero-tag">LA REGLA DE ORO</div>
  <div class="s7hero-intro">‹La urgencia: la ventana dura <span class="hl">días, no semanas.</span> El que llega tarde, <span class="bold">llega al vacío.</span>›</div>
  <div class="s7hero-title">‹Muévete<br><span class="red">ahora›</span></div>
  <div class="s7hero-sub">~ ‹remate de urgencia› ~</div>
  <div class="num">7 / 8</div>
  <div class="handle">@tuhandle</div>
</div>

<!-- S8 — CIERRE CTA -->
<div class="slide s8">
  <div class="tape tape-1"></div>
  <div class="tape tape-2"></div>
  <div class="sticker sticker-1">‹🤖›</div>
  <div class="sticker sticker-2">‹📌›</div>
  <div class="sticker sticker-3">‹💬›</div>
  <div class="s8-pretag">~ pero esto es lo importante ~</div>
  <div class="s8-title">‹Convierte cada<br>noticia en <span class="hl">contenido›</span></div>
  <svg class="doodle" style="top:450px; left:50%; transform:translateX(-50%); width:400px; height:30px;" viewBox="0 0 400 30">
    <path d="M5,18 Q100,4 200,15 T395,12" stroke="#C17F5A" stroke-width="4" fill="none" stroke-linecap="round"/>
  </svg>
  <div class="s8-intro">‹Los creadores que crecen no persiguen ideas: convierten <span class="bold">cada tendencia de IA</span> en piezas que venden 👇›</div>
  <div class="s8-list">
    <div class="item"><span class="bold">‹Detectar›</span> ‹la noticia antes que nadie›</div>
    <div class="item"><span class="bold">‹Traducirla›</span> ‹a tu nicho en minutos›</div>
    <div class="item"><span class="bold">‹Producir›</span> ‹el reel + carrusel el mismo día›</div>
  </div>
  <div class="s8-cta">Comenta <strong>"100K"</strong> y te enseño cómo 🚀</div>
  <div class="s8-save">📌 <span class="pin">Guárdalo</span> para tu<br>próxima ola de contenido</div>
  <div class="num">8 / 8</div>
  <div class="handle">@tuhandle · Fórmula 100K</div>
</div>

</body>
</html>
```
