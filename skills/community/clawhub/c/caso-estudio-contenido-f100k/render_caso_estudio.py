#!/usr/bin/env python3
"""
Render del CASO DE ESTUDIO de FÓRMULA 100K (Reto Final del módulo de contenido).

Toma un data.json estructurado y produce un index.html autocontenido (CSS inline,
sin React/Babel) listo para subir a Netlify/Vercel como portafolio.

Uso:
    python3 render_caso_estudio.py data.json index.html

Esquema de data.json (todas las listas pueden venir vacías; lo que falte se omite):
{
  "nicho": "Repostería creativa para eventos",
  "handle": "@tu_cuenta",
  "autora": "Tu nombre (@tu_cuenta)",
  "fecha": "2026-06-22",
  "proposito": "Crecimiento",
  "avatar": {
    "nombre": "Laura", "edad": "28-40",
    "creencia": "Un pastel de diseño es imposible de hacer en casa",
    "deseo": "Lucirse en la fiesta de sus hijos sin pagar una fortuna"
  },
  "resumen": {"referencias": 12, "guiones": 5, "variantes": 15, "reels": 30},
  "patrones_cuenta": {
    "handle": "@mi_cuenta",
    "ganadores": ["Gancho de pregunta abierta en el primer frame", "Reels < 18s"],
    "negativos": ["Intros largas con saludo", "Texto en pantalla > 8 palabras"],
    "voz": "Cercana, directa, con humor",
    "fusion": ["Tu gancho de pregunta coincide con el patrón del nicho → duplícalo",
               "El nicho usa 'antes/después' y tú aún no → oportunidad"]
  },
  "patrones": [
    {"emoji": "⚔️", "nombre": "Enemigo común", "desc": "Atacar la creencia de que es caro"}
  ],
  "virales": [
    {"plataforma": "Instagram", "url": "https://...", "reproducciones": "3.7M",
     "comentarios": "12.4K", "engagement": "8.2%", "gancho": "Nadie te dice que..."}
  ],
  "guiones": [
    {"n": 1, "pilar": "Educativo", "gancho": "...", "texto_pantalla": "...",
     "proposito": "Crecimiento", "cuerpo": "Texto del guion (opcional)"}
  ],
  "ganchos": [
    {"guion": 1,
     "variantes": [{"texto": "...", "tecnica": "Enemigo común"}],
     "ganador": 0, "porque": "Activa la creencia restrictiva de entrada"}
  ],
  "calendario": [
    {"dia": 1, "semana": 1, "pilar": "Educativo", "titulo": "...", "cta": "Guarda esto", "formato": "Curiosidad"}
  ],
  "sheets_url": "https://docs.google.com/...",
  "plan_mes2": {
    "ancla": "Podcast de entrevistas a reposteras",
    "sistema": "1 episodio = 8-10 reels",
    "detalle": "Texto explicativo (opcional)"
  }
}
"""
import json
import sys
import html


def esc(x):
    return html.escape(str(x if x is not None else ""))


def section(title, num, body):
    return f"""
    <section class="step">
      <div class="step-head"><span class="step-num">{num}</span><h2>{esc(title)}</h2></div>
      {body}
    </section>"""


def render(data):
    nicho = esc(data.get("nicho", "Tu nicho"))
    handle = esc(data.get("handle", ""))
    autora = esc(data.get("autora", ""))
    fecha = esc(data.get("fecha", ""))
    proposito = esc(data.get("proposito", ""))
    av = data.get("avatar", {}) or {}
    res = data.get("resumen", {}) or {}

    # ---- Resumen ejecutivo (chips) ----
    chips = []
    labels = [("referencias", "referencias virales"), ("guiones", "guiones"),
              ("variantes", "variantes de gancho"), ("reels", "reels en el calendario")]
    for key, lab in labels:
        if res.get(key) is not None:
            chips.append(f'<div class="chip"><div class="chip-n">{esc(res[key])}</div>'
                         f'<div class="chip-l">{esc(lab)}</div></div>')
    chips_html = f'<div class="chips">{"".join(chips)}</div>' if chips else ""

    # ---- Avatar ----
    avatar_html = ""
    if av:
        avatar_html = f"""
      <div class="avatar">
        <div class="avatar-emoji">🎯</div>
        <div>
          <div class="avatar-name">{esc(av.get('nombre','Avatar'))}<span class="avatar-age">{esc(av.get('edad',''))}</span></div>
          <p class="avatar-line"><b>Cree que:</b> {esc(av.get('creencia',''))}</p>
          <p class="avatar-line"><b>Desea:</b> {esc(av.get('deseo',''))}</p>
        </div>
      </div>"""

    # ---- Patrones de tu cuenta (ADN) ----
    pc = data.get("patrones_cuenta", {}) or {}
    adn_html = ""
    if pc and (pc.get("ganadores") or pc.get("negativos") or pc.get("fusion")):
        def _lis(items, cls):
            return "".join(f'<li class="{cls}">{esc(i)}</li>' for i in (items or []))
        voz = f'<p class="adn-voz"><b>Tu voz:</b> {esc(pc.get("voz",""))}</p>' if pc.get("voz") else ""
        fusion = ""
        if pc.get("fusion"):
            fusion = f'<div class="fusion"><div class="fusion-t">🧬 Fusión: tu ADN × el nicho</div><ul>{_lis(pc.get("fusion"), "fz")}</ul></div>'
        handle_pc = esc(pc.get("handle", ""))
        adn_html = f"""
    <section class="step adn">
      <div class="step-head"><span class="step-num">🔍</span><h2>Patrones de tu cuenta {('· ' + handle_pc) if handle_pc else ''}</h2></div>
      <div class="adn-grid">
        <div class="adn-col win"><div class="adn-h">✓ Tus patrones ganadores</div><ul>{_lis(pc.get('ganadores'), 'g')}</ul></div>
        <div class="adn-col bad"><div class="adn-h">✗ Patrones a evitar</div><ul>{_lis(pc.get('negativos'), 'b')}</ul></div>
      </div>{voz}{fusion}
    </section>"""

    # ---- Paso 1: virales ----
    virales = data.get("virales", []) or []
    rows = ""
    for v in virales:
        rows += f"""<tr>
          <td><span class="plat">{esc(v.get('plataforma',''))}</span></td>
          <td class="gancho">{esc(v.get('gancho',''))}</td>
          <td class="num">{esc(v.get('reproducciones',''))}</td>
          <td class="num">{esc(v.get('comentarios',''))}</td>
          <td class="num">{esc(v.get('engagement',''))}</td>
          <td>{'<a href="'+esc(v.get('url',''))+'" target="_blank" rel="noopener">ver ↗</a>' if v.get('url') else ''}</td>
        </tr>"""
    virales_html = ""
    if rows:
        virales_html = f"""
      <div class="tablewrap"><table>
        <thead><tr><th>Plataforma</th><th>Gancho (primeros 3s)</th><th>Reprod.</th><th>Coment.</th><th>Engagement</th><th>Link</th></tr></thead>
        <tbody>{rows}</tbody></table></div>"""

    # ---- Patrones ----
    patrones = data.get("patrones", []) or []
    pat_cards = ""
    for p in patrones:
        pat_cards += f"""<div class="pat">
          <div class="pat-emoji">{esc(p.get('emoji','✨'))}</div>
          <div class="pat-name">{esc(p.get('nombre',''))}</div>
          <p class="pat-desc">{esc(p.get('desc',''))}</p>
        </div>"""
    patrones_html = f'<div class="pats">{pat_cards}</div>' if pat_cards else ""
    paso1 = section("Análisis de virales", "1", patrones_html + virales_html) if (patrones_html or virales_html) else ""

    # ---- Paso 2: guiones ----
    guiones = data.get("guiones", []) or []
    g_cards = ""
    for g in guiones:
        cuerpo = f'<p class="g-body">{esc(g.get("cuerpo",""))}</p>' if g.get("cuerpo") else ""
        g_cards += f"""<div class="guion">
          <div class="g-head"><span class="g-num">Guion {esc(g.get('n',''))}</span>
            <span class="g-pilar">{esc(g.get('pilar',''))}</span>
            <span class="g-prop">{esc(g.get('proposito',''))}</span></div>
          <p class="g-line"><b>Gancho:</b> {esc(g.get('gancho',''))}</p>
          <p class="g-line"><b>Texto en pantalla:</b> {esc(g.get('texto_pantalla',''))}</p>
          {cuerpo}
        </div>"""
    paso2 = section("Desarrollo de guiones", "2", f'<div class="guiones">{g_cards}</div>') if g_cards else ""

    # ---- Paso 3: ganchos ----
    ganchos = data.get("ganchos", []) or []
    gh_blocks = ""
    for gh in ganchos:
        vs = gh.get("variantes", []) or []
        winner = gh.get("ganador", -1)
        vlist = ""
        for i, var in enumerate(vs):
            win = " win" if i == winner else ""
            badge = '<span class="win-badge">★ ganador</span>' if i == winner else ""
            vlist += f"""<div class="var{win}">
              <div class="var-tec">{esc(var.get('tecnica',''))}{badge}</div>
              <p class="var-txt">{esc(var.get('texto',''))}</p>
            </div>"""
        porque = f'<p class="gh-why"><b>Por qué gana:</b> {esc(gh.get("porque",""))}</p>' if gh.get("porque") else ""
        gh_blocks += f"""<div class="gh">
          <div class="gh-title">Ganchos del Guion {esc(gh.get('guion',''))}</div>
          <div class="vars">{vlist}</div>{porque}
        </div>"""
    paso3 = section("Ingeniería de ganchos", "3", gh_blocks) if gh_blocks else ""

    # ---- Paso 4: calendario ----
    cal = data.get("calendario", []) or []
    crows = ""
    for c in cal:
        crows += f"""<tr>
          <td class="num">{esc(c.get('dia',''))}</td>
          <td class="num">{esc(c.get('semana',''))}</td>
          <td>{esc(c.get('pilar',''))}</td>
          <td class="titulo">{esc(c.get('titulo',''))}</td>
          <td>{esc(c.get('formato',''))}</td>
          <td class="cta">{esc(c.get('cta',''))}</td>
        </tr>"""
    sheets = data.get("sheets_url", "")
    sheets_btn = (f'<a class="btn" href="{esc(sheets)}" target="_blank" rel="noopener">'
                  f'📄 Abrir calendario completo en Google Sheets</a>') if sheets else ""
    cal_html = ""
    if crows:
        cal_html = f"""
      <div class="tablewrap"><table>
        <thead><tr><th>Día</th><th>Sem.</th><th>Pilar</th><th>Título</th><th>Formato</th><th>CTA</th></tr></thead>
        <tbody>{crows}</tbody></table></div>{sheets_btn}"""
    paso4 = section("Calendario de 30 días", "4", cal_html) if cal_html else ""

    # ---- Plan mes 2 ----
    pm = data.get("plan_mes2", {}) or {}
    plan_html = ""
    if pm:
        detalle = f'<p class="plan-detalle">{esc(pm.get("detalle",""))}</p>' if pm.get("detalle") else ""
        plan_html = f"""
    <section class="plan">
      <h2>📈 Planificación — Mes 2</h2>
      <div class="plan-grid">
        <div class="plan-card"><div class="plan-k">Formato ancla</div><div class="plan-v">{esc(pm.get('ancla',''))}</div></div>
        <div class="plan-card"><div class="plan-k">Sistema de reutilización</div><div class="plan-v">{esc(pm.get('sistema',''))}</div></div>
      </div>{detalle}
    </section>"""

    meta = " · ".join([x for x in [handle, proposito, fecha] if x])

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Caso de Estudio — {nicho} · FÓRMULA 100K</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    color:#1a1a2e;background:#f6f6fb;line-height:1.6;-webkit-font-smoothing:antialiased}}
  .wrap{{max-width:980px;margin:0 auto;padding:0 20px 80px}}
  header.hero{{background:linear-gradient(135deg,#4338ca,#7c3aed,#db2777);color:#fff;padding:64px 20px 56px;text-align:center}}
  .hero .kicker{{text-transform:uppercase;letter-spacing:.18em;font-size:12px;font-weight:800;opacity:.85}}
  .hero h1{{font-size:clamp(28px,5vw,46px);font-weight:900;margin:10px 0 8px;line-height:1.1}}
  .hero .meta{{font-size:14px;opacity:.9}}
  .chips{{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:34px 0 4px}}
  .chip{{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);border-radius:16px;
    padding:14px 22px;min-width:120px;backdrop-filter:blur(6px)}}
  .chip-n{{font-size:30px;font-weight:900;line-height:1}}
  .chip-l{{font-size:11px;text-transform:uppercase;letter-spacing:.06em;opacity:.9;margin-top:4px}}
  .avatar{{display:flex;gap:16px;align-items:flex-start;background:#fff;border:1px solid #e6e6f0;
    border-radius:18px;padding:20px;margin:-32px auto 0;max-width:760px;box-shadow:0 12px 30px rgba(60,40,120,.08);position:relative}}
  .avatar-emoji{{font-size:34px}}
  .avatar-name{{font-size:20px;font-weight:900}}
  .avatar-age{{font-size:13px;font-weight:700;color:#7c3aed;margin-left:8px;background:#f3e8ff;padding:2px 8px;border-radius:999px}}
  .avatar-line{{font-size:14px;color:#444;margin-top:4px}}
  section.step{{background:#fff;border:1px solid #ececf4;border-radius:20px;padding:28px;margin-top:24px;
    box-shadow:0 6px 18px rgba(60,40,120,.05)}}
  .step-head{{display:flex;align-items:center;gap:14px;margin-bottom:20px}}
  .step-num{{width:42px;height:42px;border-radius:12px;background:linear-gradient(135deg,#4338ca,#7c3aed);
    color:#fff;font-weight:900;font-size:20px;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
  .step-head h2{{font-size:22px;font-weight:900}}
  section.plan{{background:linear-gradient(135deg,#4338ca,#7c3aed,#db2777);color:#fff;border-radius:20px;padding:28px;margin-top:24px}}
  section.plan h2{{font-size:20px;font-weight:900;margin-bottom:16px}}
  .plan-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
  .plan-card{{background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);border-radius:14px;padding:16px}}
  .plan-k{{font-size:11px;text-transform:uppercase;letter-spacing:.08em;opacity:.85;font-weight:800}}
  .plan-v{{font-size:17px;font-weight:800;margin-top:6px}}
  .plan-detalle{{margin-top:14px;font-size:14px;opacity:.95}}
  .adn{{border:2px solid #ddd6fe}}
  .adn-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
  .adn-col{{border-radius:14px;padding:14px}}
  .adn-col.win{{background:#ecfdf5;border:1px solid #a7f3d0}}
  .adn-col.bad{{background:#fef2f2;border:1px solid #fecaca}}
  .adn-h{{font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;margin-bottom:8px}}
  .adn-col.win .adn-h{{color:#059669}}
  .adn-col.bad .adn-h{{color:#dc2626}}
  .adn-col ul{{list-style:none;display:grid;gap:6px}}
  .adn-col li{{font-size:13px;padding-left:16px;position:relative}}
  .adn-col li.g:before{{content:'✓';position:absolute;left:0;color:#059669;font-weight:900}}
  .adn-col li.b:before{{content:'✗';position:absolute;left:0;color:#dc2626;font-weight:900}}
  .adn-voz{{font-size:13px;color:#555;margin-top:12px}}
  .fusion{{margin-top:14px;background:linear-gradient(135deg,#4338ca,#7c3aed);color:#fff;border-radius:14px;padding:16px}}
  .fusion-t{{font-weight:900;font-size:14px;margin-bottom:8px}}
  .fusion ul{{list-style:none;display:grid;gap:6px}}
  .fusion li.fz{{font-size:13px;padding-left:16px;position:relative}}
  .fusion li.fz:before{{content:'→';position:absolute;left:0;font-weight:900}}
  @media(max-width:560px){{.adn-grid{{grid-template-columns:1fr}}}}
  .pats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:22px}}
  .pat{{background:#faf8ff;border:1px solid #ece6fb;border-radius:14px;padding:14px}}
  .pat-emoji{{font-size:24px}}
  .pat-name{{font-weight:800;font-size:14px;margin:6px 0 4px}}
  .pat-desc{{font-size:13px;color:#555}}
  .tablewrap{{overflow-x:auto;border:1px solid #eee;border-radius:14px}}
  table{{width:100%;border-collapse:collapse;font-size:13px;min-width:560px}}
  th{{background:#f3f1fb;text-align:left;padding:10px 12px;font-weight:800;color:#4338ca;font-size:11px;
    text-transform:uppercase;letter-spacing:.04em}}
  td{{padding:10px 12px;border-top:1px solid #f0f0f6;vertical-align:top}}
  td.num{{text-align:center;font-variant-numeric:tabular-nums;color:#7c3aed;font-weight:700;white-space:nowrap}}
  td.gancho,td.titulo{{font-weight:600}}
  td.cta{{color:#db2777;font-weight:700}}
  .plat{{background:#eef2ff;color:#4338ca;font-weight:700;font-size:11px;padding:3px 8px;border-radius:999px;white-space:nowrap}}
  a{{color:#7c3aed;text-decoration:none;font-weight:700}}
  a:hover{{text-decoration:underline}}
  .guiones{{display:grid;gap:14px}}
  .guion{{background:#faf8ff;border:1px solid #ece6fb;border-radius:14px;padding:16px}}
  .g-head{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px}}
  .g-num{{font-weight:900;font-size:15px}}
  .g-pilar{{background:#eef2ff;color:#4338ca;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px}}
  .g-prop{{background:#fce7f3;color:#db2777;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px}}
  .g-line{{font-size:14px;margin-top:2px}}
  .g-body{{font-size:13px;color:#555;margin-top:8px;white-space:pre-wrap}}
  .gh{{background:#faf8ff;border:1px solid #ece6fb;border-radius:14px;padding:16px;margin-bottom:12px}}
  .gh-title{{font-weight:900;font-size:15px;margin-bottom:10px}}
  .vars{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:10px}}
  .var{{background:#fff;border:1px solid #eee;border-radius:12px;padding:12px}}
  .var.win{{border-color:#7c3aed;box-shadow:0 0 0 2px #ede9fe}}
  .var-tec{{font-size:11px;font-weight:800;color:#7c3aed;text-transform:uppercase;letter-spacing:.04em;margin-bottom:6px}}
  .win-badge{{background:#7c3aed;color:#fff;font-size:9px;padding:1px 6px;border-radius:999px;margin-left:6px}}
  .var-txt{{font-size:13px}}
  .gh-why{{font-size:13px;color:#444;margin-top:10px}}
  .btn{{display:inline-block;margin-top:16px;background:linear-gradient(135deg,#4338ca,#7c3aed);color:#fff;
    padding:12px 22px;border-radius:12px;font-weight:800;font-size:14px}}
  footer{{text-align:center;margin-top:40px;font-size:13px;color:#888}}
  footer b{{color:#7c3aed}}
  @media(max-width:560px){{.plan-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
  <header class="hero">
    <div class="kicker">Caso de Estudio · FÓRMULA 100K</div>
    <h1>{nicho}</h1>
    <div class="meta">{meta}</div>
    {chips_html}
  </header>
  <div class="wrap">
    {avatar_html}
    {adn_html}
    {paso1}
    {paso2}
    {paso3}
    {paso4}
    {plan_html}
    <footer>
      Caso de estudio creado con la metodología <b>FÓRMULA 100K</b>{(' · por ' + autora) if autora else ''}.
    </footer>
  </div>
</body>
</html>"""


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 render_caso_estudio.py <data.json> <salida.html>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    html_out = render(data)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"✓ Caso de estudio renderizado → {sys.argv[2]}")


if __name__ == "__main__":
    main()
