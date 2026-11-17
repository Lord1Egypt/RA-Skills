# Librería de Patrones Visuales · Artifacts F100K

Componentes visuales reutilizables extraídos de los 7 artifacts ya creados. Combina al menos 3 patrones distintos por artifact para mantener variedad.

## 1. Caja de Introducción Gradient

Va al inicio de cada sub-tab para dar contexto.

```jsx
<div className="bg-gradient-to-r from-[ACCENT]-50 to-[ACCENT2]-50 border border-[ACCENT]-200 rounded-2xl p-5 mb-5">
  <h2 className="text-sm font-bold text-[ACCENT]-800 uppercase tracking-wider mb-1">{título}</h2>
  <p className="text-sm text-gray-700 leading-relaxed">{descripción}</p>
</div>
```

## 2. Acordeón Expandible

Para listas de fases, condiciones, principios — el más usado.

```jsx
{ITEMS.map((item, i) => (
  <div className={`rounded-2xl border-2 overflow-hidden transition-all ${openIdx===i ? "border-[ACCENT]-300 shadow-md" : "border-gray-200 hover:border-gray-300"}`}>
    <button onClick={() => setOpenIdx(openIdx===i?null:i)}
      className={`w-full text-left flex items-center gap-4 p-4 ${openIdx===i ? "bg-[ACCENT]-50" : "bg-white hover:bg-gray-50"}`}>
      <div className="w-12 h-12 bg-[ACCENT]-600 rounded-xl flex items-center justify-center text-2xl shadow flex-shrink-0">{item.emoji}</div>
      <div className="flex-1 min-w-0">
        <div className="text-base font-black text-gray-900">{item.name}</div>
        <div className="text-sm text-gray-500">{item.desc}</div>
      </div>
      <span className={`text-gray-300 text-xl transition-transform ${openIdx===i?"rotate-90":""}`}>›</span>
    </button>
    {openIdx===i && <div className="bg-[ACCENT]-50 border-t border-[ACCENT]-300 p-4">{detalle}</div>}
  </div>
))}
```

## 3. Decision Matrix por Fase

Para "qué elegir según tu situación" (usado en Plataformas).

```jsx
<div className="space-y-4">
  {STAGES.map((s, i) => (
    <div className="rounded-2xl border-2 overflow-hidden">
      <div className={`bg-gradient-to-r ${s.bg} text-white p-4`}>
        <div className="text-base font-black">{s.stage}</div>
        <div className="text-xs opacity-90">{s.when}</div>
      </div>
      <div className="bg-white p-4">
        <div className="flex flex-wrap gap-1.5 mb-3">
          {s.recommend.map(r => (
            <span className="text-xs px-2 py-0.5 rounded-full font-bold bg-emerald-100 text-emerald-700">✓ {r}</span>
          ))}
        </div>
        <p className="text-sm text-gray-700">{s.why}</p>
      </div>
    </div>
  ))}
</div>
```

## 4. Tabla Comparativa con Header Gradient

Para comparar opciones lado a lado.

```jsx
<div className="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
  <div className="grid grid-cols-12 bg-gradient-to-r from-[ACCENT1]-700 to-[ACCENT2]-700 text-white text-xs font-black uppercase tracking-wider">
    <div className="col-span-3 px-3 py-3">Columna 1</div>
    <div className="col-span-3 px-3 py-3 text-center">Columna 2</div>
    <div className="col-span-6 px-3 py-3">Columna 3</div>
  </div>
  {ROWS.map((row, i) => (
    <div className={`grid grid-cols-12 ${i%2===0?"bg-white":"bg-gray-50"} border-t border-gray-100`}>
      <div className="col-span-3 px-3 py-3 text-sm font-bold">{row.col1}</div>
      <div className="col-span-3 px-3 py-3 text-center">{row.col2}</div>
      <div className="col-span-6 px-3 py-3 text-xs text-gray-600">{row.col3}</div>
    </div>
  ))}
</div>
```

## 5. Flujo Visual con Flechas

Para procesos secuenciales (Dolor → Vehículo → Resultado).

```jsx
<div className="flex flex-wrap items-center justify-center gap-3 p-4 bg-gradient-to-r from-[ACCENT]-50 to-[ACCENT2]-50 rounded-xl">
  <div className="bg-red-100 border-2 border-red-300 rounded-xl px-4 py-3 text-center">
    <div className="text-xl mb-0.5">😣</div>
    <div className="text-xs font-black text-red-700">PASO 1</div>
  </div>
  <div className="text-[ACCENT]-500 font-black text-2xl">→</div>
  <div className="bg-gradient-to-br from-[ACCENT]-600 to-[ACCENT2]-700 rounded-xl px-4 py-3 text-center text-white shadow-lg">
    <div className="text-xl mb-0.5">🚀</div>
    <div className="text-xs font-black">CENTRO</div>
  </div>
  <div className="text-[ACCENT]-500 font-black text-2xl">→</div>
  <div className="bg-emerald-100 border-2 border-emerald-300 rounded-xl px-4 py-3 text-center">
    <div className="text-xl mb-0.5">✨</div>
    <div className="text-xs font-black text-emerald-700">PASO FINAL</div>
  </div>
</div>
```

## 6. Numbered Steps con Badges Circulares

Para procesos paso a paso.

```jsx
{STEPS.map((s, i) => (
  <div className="bg-white border border-gray-200 rounded-2xl p-4 hover:border-[ACCENT]-300 transition shadow-sm flex gap-3">
    <div className="w-10 h-10 bg-gradient-to-br from-[ACCENT]-600 to-[ACCENT2]-600 rounded-xl flex items-center justify-center text-white font-black text-sm flex-shrink-0">
      {s.n}
    </div>
    <div>
      <div className="text-sm font-black text-gray-900">{s.title}</div>
      <p className="text-xs text-gray-600 leading-relaxed mt-1">{s.desc}</p>
    </div>
  </div>
))}
```

## 7. Cards "Cuándo usar / Cuándo NO usar / Principios"

Para guías de decisión (usado en Landing Pages).

```jsx
<div className="space-y-3">
  <div>
    <div className="text-xs font-black text-emerald-700 uppercase mb-1">✓ Cuándo usar</div>
    <p className="text-sm text-gray-700">{cuandoUsar}</p>
  </div>
  <div>
    <div className="text-xs font-black text-red-700 uppercase mb-1">✗ Cuándo NO usar</div>
    <p className="text-sm text-gray-700">{cuandoNo}</p>
  </div>
  <div>
    <div className="text-xs font-black text-[ACCENT]-700 uppercase mb-1.5">Principios clave</div>
    <ul className="space-y-1">
      {principios.map((p, i) => (
        <li className="text-xs text-gray-700 flex gap-1.5"><span className="text-[ACCENT]-500">•</span>{p}</li>
      ))}
    </ul>
  </div>
</div>
```

## 8. Mini Mockup de Pantalla (estilo Landing)

Para mostrar previews visuales (usado en Landing Page).

```jsx
function PreviewMockup() {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 min-h-[280px]">
      {/* Contenido del mockup aquí */}
    </div>
  );
}
```

Variaciones probadas:
- **Squeeze**: caja blanca centrada con headline + email + botón pulse
- **VSL**: fondo dark con video grande y play button
- **Bento**: grid de cells con tamaños mixtos
- **Long-form**: secciones apiladas con líneas que simulan texto
- **Mobile**: marco de teléfono con `phone-frame` class

## 9. Caja de Warning/Tip Destacada

Para resaltar información crítica.

```jsx
<div className="bg-amber-50 border border-amber-200 rounded-2xl p-4">
  <div className="text-xs font-black text-amber-700 uppercase tracking-wider mb-1">⚠ Atención</div>
  <p className="text-sm text-gray-700 leading-relaxed">{texto}</p>
</div>
```

Para tips positivos:
```jsx
<div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4">
  <div className="text-xs font-black text-emerald-700 uppercase mb-1">💡 Tip clave</div>
  <p className="text-sm text-gray-700 leading-relaxed">{texto}</p>
</div>
```

## 10. CTA Banner Final (gradient lleno)

Para cerrar una sección con un mensaje fuerte.

```jsx
<div className="bg-gradient-to-r from-[ACCENT1]-600 via-[ACCENT2]-600 to-[ACCENT3]-500 text-white rounded-2xl p-5">
  <div className="text-xs font-black uppercase tracking-wider opacity-80 mb-2">📌 Idea Central</div>
  <p className="text-sm leading-relaxed">{texto importante}</p>
</div>
```

## 11. Selector con Cards (tipo galería)

Para que el usuario elija entre opciones (usado en Landing Pages).

```jsx
<div className="flex gap-2 mb-5 overflow-x-auto pb-2">
  {OPTIONS.map(o => (
    <button onClick={() => setSelected(o.id)}
      className={`flex-shrink-0 px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center gap-2 ${
        selected===o.id ? `text-white shadow-md bg-gradient-to-r ${o.accent}` : "bg-white border border-gray-200 text-gray-600"
      }`}>
      <span className="text-base">{o.emoji}</span>
      <span>{o.name}</span>
    </button>
  ))}
</div>
```

## 12. Visualización de Fórmula (ecuación visual)

Para mostrar conceptos matemáticos/estructurales (Ecuación de Valor de Hormozi).

```jsx
<div className="flex flex-wrap items-center justify-center gap-3 p-4 bg-gradient-to-r from-[ACCENT]-50 to-[ACCENT2]-50 rounded-xl">
  <div className="text-xs font-bold text-gray-400 uppercase">VALOR =</div>
  <div className="flex flex-col items-center">
    <div className="flex gap-2 items-center">
      <div className="bg-emerald-100 border-2 border-emerald-300 rounded-lg px-3 py-2 text-center">
        <div className="text-xs font-black text-emerald-700">Variable A</div>
      </div>
      <div className="text-[ACCENT]-500 font-black">×</div>
      <div className="bg-emerald-100 border-2 border-emerald-300 rounded-lg px-3 py-2 text-center">
        <div className="text-xs font-black text-emerald-700">Variable B</div>
      </div>
    </div>
    <div className="w-full h-0.5 bg-gray-800 my-1.5" />
    <div className="flex gap-2 items-center">
      <div className="bg-red-100 border-2 border-red-300 rounded-lg px-3 py-2 text-center">
        <div className="text-xs font-black text-red-700">Variable C</div>
      </div>
      <div className="text-[ACCENT]-500 font-black">×</div>
      <div className="bg-red-100 border-2 border-red-300 rounded-lg px-3 py-2 text-center">
        <div className="text-xs font-black text-red-700">Variable D</div>
      </div>
    </div>
  </div>
</div>
```

## 13. Sub-navegación con tabs internos

Para dividir la Guía en sub-secciones.

```jsx
<div className="flex gap-2 mb-6 flex-wrap">
  {SUBTABS.map(t => (
    <button onClick={() => setGuideTab(t.id)}
      className={`px-3 py-2 rounded-xl text-xs sm:text-sm font-semibold transition ${
        guideTab===t.id ? "bg-[ACCENT]-600 text-white shadow" : "bg-white border border-gray-200 text-gray-600 hover:border-[ACCENT]-300"
      }`}>
      {t.label}
    </button>
  ))}
</div>
```

## 14. Stats Grid (3 columnas con números clave)

Para mostrar métricas/datos destacados.

```jsx
<div className="grid gap-2 sm:grid-cols-3">
  {STATS.map((s, i) => (
    <div className={`${s.bg} border ${s.border} rounded-xl p-3 text-center`}>
      <div className={`text-xs font-black ${s.text} uppercase mb-1`}>{s.label}</div>
      <div className={`text-lg font-bold ${s.dark}`}>{s.value}</div>
      <div className={`text-xs ${s.text}`}>{s.unit}</div>
    </div>
  ))}
</div>
```

## 15. Botón de Copiar con Feedback

Para copiar prompts o markdown al clipboard.

```jsx
const [copied, setCopied] = useState(false);
const handleCopy = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  });
};

<button onClick={() => handleCopy(content)}
  className="flex items-center gap-1.5 bg-white/20 hover:bg-white/30 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition">
  {copied ? "✓ Copiado!" : "📋 Copiar"}
</button>
```

## Combinaciones recomendadas por tipo de tema

- **Tema con FRAMEWORK central**: Caja intro + Acordeón expandible + CTA Banner Final
- **Tema COMPARATIVO**: Caja intro + Tabla comparativa + Decision matrix + Stats grid
- **Tema VISUAL/DISEÑO**: Caja intro + Selector con cards + Mockups + Botón copiar
- **Tema PROCESO/PASO A PASO**: Caja intro + Numbered steps + Cards cuándo usar + Warning final
- **Tema CON FÓRMULA**: Caja intro + Visualización de fórmula + Acordeón + Stats grid

## 16. Mini Curva de Retención (SVG inline)

Para mostrar curvas pequeñas de retención/atención por estructura/concepto. Estrenado en `f100k-guionizacion.html` para visualizar la curva típica de cada una de las 35 estructuras de guion.

```jsx
function RetentionCurve({ values, color = "#db2777" }) {
  const [a, b, c] = values; // valores 0-100 (inicio, medio, final)
  const points = `0,${100 - a} 50,${100 - b} 100,${100 - c}`;
  return (
    <svg viewBox="0 0 100 100" className="w-full h-12" preserveAspectRatio="none">
      <defs>
        <linearGradient id={`grad-${color.replace('#','')}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.4" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>
      <polyline points={`0,100 ${points} 100,100`} fill={`url(#grad-${color.replace('#','')})`} />
      <polyline points={points} fill="none" stroke={color} strokeWidth="2.5" strokeLinejoin="round" strokeLinecap="round" />
      <circle cx="0" cy={100 - a} r="2.5" fill={color} />
      <circle cx="50" cy={100 - b} r="2.5" fill={color} />
      <circle cx="100" cy={100 - c} r="2.5" fill={color} />
    </svg>
  );
}
```

Uso típico dentro de una card:
```jsx
<div className="bg-gray-50 rounded-lg p-2">
  <div className="text-[10px] font-bold text-gray-500 uppercase mb-1">Curva de retención típica</div>
  <RetentionCurve values={[95, 70, 85]} color="#db2777" />
  <div className="flex justify-between text-[10px] text-gray-400 mt-0.5">
    <span>Inicio 95%</span><span>Medio 70%</span><span>Final 85%</span>
  </div>
</div>
```

## 17. Embudo SVG (Funnel) — 3 a 4 niveles

Para representar visualmente embudos de propósito (TOFU/MOFU/BOFU) o filtros progresivos (escala viral, niveles de calidad). Estrenado en `f100k-guionizacion.html` para el embudo de propósitos y para la Escala Viral.

```jsx
function Funnel({ levels }) {
  // levels: [{label, sub, color}] de arriba (más ancho) hacia abajo (más estrecho)
  const n = levels.length;
  const totalH = 320;
  const stepH = totalH / n;
  const maxW = 360;
  const minW = 120;
  const wStep = (maxW - minW) / n;
  return (
    <svg viewBox={`0 0 400 ${totalH + 20}`} className="w-full h-auto" preserveAspectRatio="xMidYMid meet">
      {levels.map((lvl, i) => {
        const w1 = maxW - i * wStep;
        const w2 = maxW - (i + 1) * wStep;
        const x1 = (400 - w1) / 2;
        const x2 = (400 - w2) / 2;
        const y1 = i * stepH + 10;
        const y2 = (i + 1) * stepH + 10;
        const points = `${x1},${y1} ${x1 + w1},${y1} ${x2 + w2},${y2} ${x2},${y2}`;
        return (
          <g key={i}>
            <polygon points={points} fill={lvl.color} opacity="0.92" />
            <text x="200" y={y1 + stepH/2 - 3} textAnchor="middle" fill="white" fontSize="14" fontWeight="900" style={{textTransform:"uppercase",letterSpacing:"1px"}}>{lvl.label}</text>
            <text x="200" y={y1 + stepH/2 + 14} textAnchor="middle" fill="white" fontSize="10" opacity="0.9">{lvl.sub}</text>
          </g>
        );
      })}
    </svg>
  );
}
```

Uso típico (lado a lado con descripción):
```jsx
<div className="grid md:grid-cols-2 gap-4 items-center bg-gradient-to-br from-gray-50 to-fuchsia-50 border border-fuchsia-200 rounded-2xl p-4">
  <Funnel levels={[
    { label: "TOFU", sub: "Atracción", color: "#ea580c" },
    { label: "MOFU", sub: "Nutrición", color: "#c026d3" },
    { label: "BOFU", sub: "Conversión", color: "#059669" },
  ]} />
  <div className="text-xs text-gray-700 leading-relaxed space-y-2">{...}</div>
</div>
```

## 18. Workflow Horizontal con Flechas (mapa de proceso)

Para mostrar un proceso secuencial de N pasos con flechas conectoras. Estrenado en `f100k-guionizacion.html` para el "Mapa del proceso" del workflow de guionización.

```jsx
<div className="flex flex-wrap items-stretch justify-center gap-2 p-4 bg-gradient-to-r from-fuchsia-50 via-pink-50 to-rose-50 rounded-2xl">
  {STEPS.map((w, i) => (
    <React.Fragment key={i}>
      <div className="bg-white border-2 border-fuchsia-300 rounded-xl px-3 py-3 text-center shadow-sm flex-1 min-w-[110px]">
        <div className="text-2xl mb-1">{w.icon}</div>
        <div className="text-[10px] font-black text-fuchsia-600 uppercase mb-0.5">Paso {w.n}</div>
        <div className="text-xs font-black text-gray-800 mb-1 leading-tight">{w.title}</div>
        <p className="text-[10px] text-gray-600 leading-snug">{w.desc}</p>
      </div>
      {i < STEPS.length - 1 && <div className="text-fuchsia-400 font-black text-2xl flex items-center">→</div>}
    </React.Fragment>
  ))}
</div>
```

## 19. Mockup de Chat Claude (captura falsa, 100% CSS)

Para mostrar EJEMPLOS visuales de uso de Claude/IA sin usar capturas reales ni stock. Estrenado en la serie `f100k-claude-*` (lead magnet "Domina Claude"). Simula la ventana de claude.ai con prompt→respuesta. Ideal para enseñar "prompt vago vs prompt con contexto", selector de modelo, pegar archivos, etc.

```jsx
function Win({ title = "claude.ai", children, accent = "#c2410c" }) {
  return (
    <div className="rounded-xl overflow-hidden border border-gray-200 shadow-sm bg-white">
      <div className="flex items-center gap-2 px-3 py-2 bg-gray-100 border-b border-gray-200">
        <span className="w-2.5 h-2.5 rounded-full bg-red-400"></span>
        <span className="w-2.5 h-2.5 rounded-full bg-amber-400"></span>
        <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
        <span className="ml-2 text-[11px] font-semibold text-gray-400 flex items-center gap-1">
          <span className="w-3.5 h-3.5 rounded-full inline-flex items-center justify-center text-white text-[8px] font-black" style={{background:accent}}>✦</span>
          {title}
        </span>
      </div>
      <div className="p-3 bg-gray-50">{children}</div>
    </div>
  );
}
function UserMsg({ children }) {
  return <div className="flex justify-end mb-2"><div className="bg-gray-200 text-gray-800 text-xs rounded-2xl rounded-br-sm px-3 py-2 max-w-[85%] leading-relaxed">{children}</div></div>;
}
function ClaudeMsg({ children, accent = "#c2410c" }) {
  return (
    <div className="flex justify-start mb-2 gap-2">
      <span className="w-5 h-5 rounded-full flex-shrink-0 inline-flex items-center justify-center text-white text-[9px] font-black mt-0.5" style={{background:accent}}>✦</span>
      <div className="bg-white border border-gray-200 text-gray-700 text-xs rounded-2xl rounded-tl-sm px-3 py-2 max-w-[85%] leading-relaxed">{children}</div>
    </div>
  );
}
```

Regla: el `accent` debe ser el accent de la paleta del artifact. Úsalo para ejemplos lado-a-lado (grid md:grid-cols-2) mostrando antes/después.

## Cuando agregues un patrón nuevo

Documéntalo aquí con:
- Nombre y propósito
- Cuándo usarlo
- Código JSX completo
- Artifact donde se usó por primera vez

## 20. Mockups de UI 100% CSS (teléfono y navegador con pantallas falsas)

Para enseñar criterio de diseño **comparando pantallas** ("así no / así sí") sin usar capturas reales ni stock. Estrenado en `f100k-crea-tu-aplicacion.html` (onboarding malo vs. bueno, estado vacío mudo vs. que enseña, dashboard de 12 métricas vs. regla 1-3-5). Ventajas: el archivo sigue autocontenido, se ve nítido al grabar video y se imprime bien.

```css
.phone { width: 208px; border: 7px solid #1e293b; border-radius: 26px; overflow: hidden; background: #fff; box-shadow: 0 10px 25px -10px rgba(0,0,0,.35); }
.phone-bar { height: 18px; background: #1e293b; }
```

```jsx
function Phone({ children, label, tone }) {
  return (
    <div className="flex flex-col items-center">
      <div className="phone">
        <div className="phone-bar" />
        <div className={`h-[330px] overflow-hidden ${tone || "bg-white"}`}>{children}</div>
      </div>
      {label && <div className="text-[11px] font-bold text-gray-500 mt-2 text-center max-w-[210px] leading-tight">{label}</div>}
    </div>
  );
}
function Browser({ children, label, title }) { /* barra con 3 semáforos + título, ver artifact */ }
const Ln = ({ w="w-full", h="h-2", c="bg-slate-200" }) => <div className={`${h} ${w} ${c} rounded-full`} />;

function GoodBad({ badLabel, goodLabel, bad, good }) {
  return (
    <div className="grid md:grid-cols-2 gap-4">
      <div className="bg-rose-50 border-2 border-rose-200 rounded-2xl p-4">
        <div className="text-xs font-black text-rose-600 uppercase tracking-wider mb-3">✗ {badLabel}</div>{bad}
      </div>
      <div className="bg-emerald-50 border-2 border-emerald-200 rounded-2xl p-4">
        <div className="text-xs font-black text-emerald-700 uppercase tracking-wider mb-3">✓ {goodLabel}</div>{good}
      </div>
    </div>
  );
}
```

Reglas de las pantallas falsas:
- Tamaños de texto entre `text-[7px]` y `text-[13px]`: a esa escala el mockup se lee como interfaz real, no como texto encogido.
- Usa `Ln` (barras grises) solo para texto de relleno; los textos que enseñan algo van escritos de verdad en español.
- Una torta ilegible se hace con `conic-gradient` inline; barras con divs de `height:%`. Nada de librerías de gráficos.
- Siempre etiqueta cada teléfono con el `label`: el mockup sin leyenda no enseña.
