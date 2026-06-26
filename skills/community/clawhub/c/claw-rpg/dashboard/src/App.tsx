import { useEffect, useRef, useState } from 'react'
import './App.css'

// ── Types ────────────────────────────────────────────────────────
interface Stats {
  claw: number; antenna: number; shell: number;
  brain: number; foresight: number; charm: number;
}
interface Character {
  name: string; class: string; level: number; prestige: number; xp: number;
  stats: Stats; abilities: string[];
  tokens: { consumed: number; produced: number };
  conversations: number;
  classHistory: Array<{ from: string; to: string; date: string }>;
  levelHistory:  Array<{ level: number; date: string }>;
  updatedAt: string;
  prestigeXpMultiplier?: number;
  hp?: number; ac?: number; bab?: number;
  saves?: { fort: number; ref: number; will: number };
  initiative?: number; feats?: string[];
}

// ── Constants ────────────────────────────────────────────────────
const CLASSES: Record<string, { en: string; icon: string; color: string }> = {
  barbarian: { en: 'Claw Berserker', icon: '🪓', color: '#ea580c' },
  fighter:   { en: 'Claw Fighter',   icon: '⚔️',  color: '#dc2626' },
  paladin:   { en: 'Claw Paladin',   icon: '🛡️',  color: '#d97706' },
  ranger:    { en: 'Claw Ranger',    icon: '🏹',  color: '#16a34a' },
  cleric:    { en: 'Claw Cleric',    icon: '✝️',  color: '#7c3aed' },
  druid:     { en: 'Claw Druid',     icon: '🌿',  color: '#15803d' },
  monk:      { en: 'Claw Monk',      icon: '👊',  color: '#0369a1' },
  rogue:     { en: 'Claw Rogue',     icon: '🗡️',  color: '#ca8a04' },
  bard:      { en: 'Claw Bard',      icon: '🎭',  color: '#be185d' },
  wizard:    { en: 'Claw Wizard',    icon: '🧙',  color: '#1d4ed8' },
  sorcerer:  { en: 'Claw Sorcerer',  icon: '🔮',  color: '#7e22ce' },
}
const CATCHPHRASES: Record<string, string> = {
  barbarian:'Rage first. Think later.',
  fighter:'My claws never missed.',
  paladin:'Justice is a weapon.',
  ranger:'I was watching before you walked in.',
  cleric:'The gods speak through me.',
  druid:'The tide rises for all.',
  monk:'Still water. Deep current.',
  rogue:'They never hear the second claw.',
  bard:"They'll write songs about this.",
  wizard:"I've read 17 books on this mistake.",
  sorcerer:'Born with it. Not learned.',
}


// ── Helpers ──────────────────────────────────────────────────────
function xpForLevel(n: number) { return n <= 1 ? 0 : (n*(n-1)/2)*1000 }
function levelProgress(xp: number, level: number) {
  if (level >= 999) return 100
  const s = xpForLevel(level), e = xpForLevel(level+1)
  return Math.min(100, Math.floor(((xp-s)/(e-s))*100))
}
function xpToNext(xp: number, level: number) {
  return level >= 999 ? 0 : xpForLevel(level+1)-xp
}
function fmtStat(n: number) { return n >= 10000 ? (n/1000).toFixed(1)+'k' : String(n) }
function fmtShort(n: number) { return n >= 10000 ? Math.round(n/1000)+'K' : n >= 1000 ? (n/1000).toFixed(1)+'K' : String(n) }

function deriveMBTI(stats: Stats, bab: number): string {
  return (stats.claw > stats.brain ? 'E' : 'I')
       + (stats.charm > stats.foresight ? 'S' : 'N')
       + (stats.shell > stats.antenna  ? 'T' : 'F')
       + (bab > 5 ? 'J' : 'P')
}
function deriveAlignment(stats: Stats): string {
  const lc = stats.foresight + stats.shell
  const ge = stats.charm + stats.foresight
  const law  = lc >= 26 ? 'Lawful'  : lc <= 18 ? 'Chaotic' : 'Neutral'
  const good = ge >= 26 ? 'Good'    : ge <= 18 ? 'Evil'    : 'Neutral'
  return (law === 'Neutral' && good === 'Neutral') ? 'True Neutral' : `${law} ${good}`
}

// ── Pixel Icons ──────────────────────────────────────────────────
type PxMap = Array<[number,number]>
const PIXEL_HEART: PxMap = [
  [1,0],[2,0],[4,0],[5,0],
  [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],
  [0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],
  [1,3],[2,3],[3,3],[4,3],[5,3],
  [2,4],[3,4],[4,4],
  [3,5],
]
const PIXEL_SHIELD: PxMap = [
  [0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],
  [0,1],[6,1],
  [0,2],[6,2],
  [1,3],[2,3],[3,3],[4,3],[5,3],
  [2,4],[3,4],[4,4],
  [3,5],
]
const PIXEL_SWORD: PxMap = [
  [3,0],
  [3,1],[3,2],[3,3],[3,4],
  [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],
  [3,6],[3,7],
]

function PixelIcon({ pixels, color, size=14 }: { pixels: PxMap; color: string; size?: number }) {
  const px = size / 8
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}
      style={{ imageRendering:'pixelated', display:'inline-block', verticalAlign:'middle', flexShrink:0 }}>
      {pixels.map(([col,row],i)=>(
        <rect key={i} x={col*px} y={row*px} width={px} height={px} fill={color}/>
      ))}
    </svg>
  )
}

// ── Pixel Lobster ────────────────────────────────────────────────
const LOBSTER_PIXELS: [number,number,string][] = [
  [3,0,'A'],[8,0,'A'],[2,1,'A'],[9,1,'A'],[1,2,'A'],[10,2,'A'],
  [4,3,'H'],[5,3,'H'],[6,3,'H'],[7,3,'H'],
  [3,4,'H'],[5,4,'H'],[6,4,'H'],[8,4,'H'],
  [3,5,'H'],[4,5,'H'],[5,5,'H'],[6,5,'H'],[7,5,'H'],[8,5,'H'],
  [4,4,'W'],[7,4,'W'],
  [2,4,'C'],[9,4,'C'],[1,5,'C'],[2,5,'C'],[9,5,'C'],[10,5,'C'],
  [0,6,'C'],[1,6,'C'],[10,6,'C'],[11,6,'C'],
  [0,7,'C'],[1,7,'C'],[10,7,'C'],[11,7,'C'],[1,8,'C'],[10,8,'C'],
  [3,6,'H'],[8,6,'H'],
  [4,6,'B'],[5,6,'B'],[6,6,'B'],[7,6,'B'],
  [4,7,'B'],[5,7,'B'],[6,7,'B'],[7,7,'B'],
  [4,8,'B'],[5,8,'B'],[6,8,'B'],[7,8,'B'],
  [4,9,'B'],[5,9,'B'],[6,9,'B'],[7,9,'B'],
  [3,10,'T'],[4,10,'T'],[5,10,'T'],[6,10,'T'],[7,10,'T'],[8,10,'T'],
  [2,11,'T'],[3,11,'T'],[5,11,'T'],[6,11,'T'],[8,11,'T'],[9,11,'T'],
  [1,12,'T'],[2,12,'T'],[5,12,'T'],[6,12,'T'],[9,12,'T'],[10,12,'T'],
  [0,13,'T'],[1,13,'T'],[10,13,'T'],[11,13,'T'],
]
function LobsterSprite({ classColor, size=160 }: { classColor: string; size?: number }) {
  const COLS=12, ROWS=14, px=size/COLS
  const cm: Record<string,string> = { A:'#94a3b8',H:classColor,W:'#fff',C:classColor,B:classColor,T:classColor }
  const om: Record<string,number> = { A:0.9,H:1,W:1,C:0.72,B:1,T:0.82 }
  return (
    <svg width={size} height={ROWS*px} viewBox={`0 0 ${size} ${ROWS*px}`}
      style={{ imageRendering:'pixelated', display:'block', margin:'0 auto' }}>
      <defs>
        <filter id="lg2" x="-30%" y="-30%" width="160%" height="160%">
          <feGaussianBlur result="blur">
            <animate attributeName="stdDeviation" values="2;4.5;2" dur="2.4s" repeatCount="indefinite"/>
          </feGaussianBlur>
          <feFlood floodColor={classColor} floodOpacity="0.6" result="c"/>
          <feComposite in="c" in2="blur" operator="in" result="g"/>
          <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <g filter="url(#lg2)">
        <animateTransform attributeName="transform" type="translate"
          values="0,0; 0,-3; 0,0" dur="2.4s" repeatCount="indefinite" additive="sum"/>
        {LOBSTER_PIXELS.map(([col,row,type],i)=>(
          <rect key={i} x={col*px} y={row*px} width={px} height={px}
            fill={cm[type]??classColor} opacity={om[type]??1}/>
        ))}
      </g>
    </svg>
  )
}

// ── Matrix Rain ──────────────────────────────────────────────────
function MatrixRain() {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  useEffect(() => {
    const canvas = canvasRef.current!
    const ctx    = canvas.getContext('2d')!
    const CHARS  = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<>{}[]|/\\!@#$%^&*()-=_+;:,.?~`'
    const FS     = 13
    let cols     = 0
    let drops:   number[] = []

    const resize = () => {
      canvas.width  = window.innerWidth
      canvas.height = window.innerHeight
      cols  = Math.floor(canvas.width / FS)
      // keep existing drops, extend if wider
      while (drops.length < cols) drops.push(Math.random() * -50 | 0)
      drops = drops.slice(0, cols)
    }
    resize()
    window.addEventListener('resize', resize)

    const draw = () => {
      // fade trail
      ctx.fillStyle = 'rgba(0,0,0,0.045)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)
      ctx.font = `${FS}px "Courier New", monospace`

      for (let i = 0; i < cols; i++) {
        const ch = CHARS[Math.random() * CHARS.length | 0]
        const y  = drops[i] * FS

        // bright head
        ctx.fillStyle = '#afffaf'
        ctx.fillText(ch, i * FS, y)

        // body (slightly dimmer handled by fade)
        if (y > FS) {
          ctx.fillStyle = '#00cc33'
          ctx.fillText(CHARS[Math.random() * CHARS.length | 0], i * FS, y - FS)
        }

        if (y > canvas.height && Math.random() > 0.975) drops[i] = 0
        else drops[i]++
      }
    }

    const id = setInterval(draw, 45)
    return () => { clearInterval(id); window.removeEventListener('resize', resize) }
  }, [])

  return (
    <canvas ref={canvasRef} style={{
      position: 'fixed', inset: 0,
      width: '100%', height: '100%',
      zIndex: 0, pointerEvents: 'none',
    }}/>
  )
}

// ── App ──────────────────────────────────────────────────────────
export default function App() {
  const [char, setChar]       = useState<Character|null>(null)
  const [skinUrl, setSkinUrl] = useState('/winamp-skin.jpg')
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState<string|null>(null)

  useEffect(() => {
    fetch('/api/character')
      .then(r => r.ok ? r.json() : Promise.reject(r.statusText))
      .then(d => { setChar(d); setError(null) })
      .catch(e => setError(String(e)))
      .finally(() => setLoading(false))
    const es = new EventSource('/api/events')
    es.onmessage = e => {
      try { const d=JSON.parse(e.data); setChar(d); setError(null); setLoading(false) } catch {}
    }
    return () => es.close()
  }, [])

  // Remove white background from the winamp skin JPG so matrix rain shows through
  useEffect(() => {
    const img = new Image()
    img.onload = () => {
      const c   = document.createElement('canvas')
      c.width   = img.naturalWidth
      c.height  = img.naturalHeight
      const ctx = c.getContext('2d')!
      ctx.drawImage(img, 0, 0)
      const id  = ctx.getImageData(0, 0, c.width, c.height)
      const d   = id.data
      const THR = 235          // pixels whiter than this become transparent
      for (let i = 0; i < d.length; i += 4) {
        if (d[i] > THR && d[i+1] > THR && d[i+2] > THR) d[i+3] = 0
      }
      ctx.putImageData(id, 0, 0)
      setSkinUrl(c.toDataURL('image/png'))
    }
    img.src = '/winamp-skin.jpg'
  }, [])

  if (loading) return <div className="skin-msg">🦞 Loading…</div>
  if (error || !char) return <div className="skin-msg">No character data.<br/><code>node scripts/init.mjs</code></div>

  const cls          = CLASSES[char.class] || { en: char.class, icon:'🦞', color:'#dc2626' }
  const lobsterColor = cls.color
  const progress     = levelProgress(char.xp, char.level)
  const toNext       = xpToNext(char.xp, char.level)
  const mbti         = deriveMBTI(char.stats, char.bab??0)
  const alignment    = deriveAlignment(char.stats)
  const phrase       = CATCHPHRASES[char.class] ?? 'Ready.'
  const saves        = char.saves ?? { fort:0, ref:0, will:0 }

  // ── Coordinate map (percentages of 1280×960 image) ─────────────
  // Black screen : x=490, y=85,  w=300, h=285  (center screen, no panel overlap)
  // Left  panel  : x=185, y=195, w=270, h=165  (flat green wing, after speakers ~x=175, before head ~x=470)
  // Right panel  : x=825, y=195, w=270, h=165  (flat green wing, after head ~x=790, before speakers ~x=1110)
  // Face area    : x=450, y=385, w=380, h=290  (chin/face below screen)
  const pct = (x: number, y: number, w: number, h: number) => ({
    position: 'absolute' as const,
    left:   `${(x/1280*100).toFixed(3)}%`,
    top:    `${(y/960*100).toFixed(3)}%`,
    width:  `${(w/1280*100).toFixed(3)}%`,
    height: `${(h/960*100).toFixed(3)}%`,
  })

  return (
    <>
    <MatrixRain/>
    <div className="skin-wrap">
      {/* ── Base image ── */}
      <img src={skinUrl} className="skin-img" alt="Winamp skin"/>

      {/* ════════════════════════════════════════════════════════
          CENTER BLACK SCREEN — Lobster + identity
          ════════════════════════════════════════════════════════ */}
      <div className="skin-screen" style={pct(495,204,299,213)}>
        <div className="screen-scanlines"/>
        <div className="screen-inner">
          <LobsterSprite classColor={lobsterColor} size={100}/>
          <div className="screen-id">
            <span className="sc-mbti">{mbti}</span>
            <span className="sc-dot"> · </span>
            <span className="sc-align">{alignment}</span>
          </div>
          <div className="screen-phrase">"{phrase}"</div>
        </div>
      </div>

      {/* ════════════════════════════════════════════════════════
          LEFT GREEN PANEL — Name · Level · Class
          Most viral: who is this character?
          ════════════════════════════════════════════════════════ */}
      <div className="skin-panel skin-left" style={pct(175,242,286,226)}>
        <div className="lp-name">{char.name}</div>
        <div className="panel-rule"/>
        <div className="lp-core">
          <div className="lp-lv">Lv.{char.level}</div>
          <div className="lp-cls-row">
            <span className="lp-cls-icon">{cls.icon}</span>
            <span className="lp-cls">{cls.en}</span>
          </div>
        </div>
        <div className="panel-rule"/>
        <div className="lp-xp">
          <div className="lp-xpbar">
            <div className="lp-xpfill" style={{width:`${progress}%`}}/>
          </div>
          <div className="lp-xplabel">
            <span className="lp-xp-cur">{fmtShort(char.xp)} XP</span>
            {char.level < 999 && <span className="lp-xp-sep"> · </span>}
            {char.level < 999 && <span className="lp-xp-next">{fmtShort(toNext)} to Lv.{char.level+1}</span>}
            {char.level >= 999 && <span className="lp-xp-next"> MAX</span>}
          </div>
        </div>
        <div className="lp-tokens">
          <div className="lp-token-item">
            <span className="lp-token-label">↓ TOKENS IN</span>
            <span className="lp-token-val">{fmtShort(char.tokens?.consumed ?? 0)}</span>
          </div>
          <div className="lp-tvline"/>
          <div className="lp-token-item">
            <span className="lp-token-label">↑ TOKENS OUT</span>
            <span className="lp-token-val">{fmtShort(char.tokens?.produced ?? 0)}</span>
          </div>
        </div>
      </div>

      {/* ════════════════════════════════════════════════════════
          RIGHT GREEN PANEL — Combat stats
          Most viral: HP / AC / BAB + saves
          ════════════════════════════════════════════════════════ */}
      <div className="skin-panel skin-right" style={pct(835,240,290,232)}>

        {/* ── HP / AC / BAB ── */}
        <div className="rp-combat">
          <div className="rp-cstat">
            <span className="rp-cl"><PixelIcon pixels={PIXEL_HEART} color="#ff4466" size={10}/> HP</span>
            <span className="rp-cv">{char.hp != null ? fmtStat(char.hp) : '—'}</span>
          </div>
          <div className="rp-vline"/>
          <div className="rp-cstat">
            <span className="rp-cl"><PixelIcon pixels={PIXEL_SHIELD} color="#44aaff" size={10}/> AC</span>
            <span className="rp-cv">{char.ac ?? '—'}</span>
          </div>
          <div className="rp-vline"/>
          <div className="rp-cstat">
            <span className="rp-cl"><PixelIcon pixels={PIXEL_SWORD} color="#ffdd44" size={10}/> BAB</span>
            <span className="rp-cv">{char.bab ?? '—'}</span>
          </div>
        </div>
        <div className="panel-rule"/>

        {/* ── FORT / REF / WILL ── */}
        <div className="rp-saves">
          {([['♦','FORT',saves.fort??0],['⚡','REF',saves.ref??0],['★','WILL',saves.will??0]] as [string,string,number][]).map(([icon,l,v])=>(
            <div key={l} className="rp-save">
              <span className="rp-sl"><span className="rp-si">{icon}</span>{l}</span>
              <span className="rp-sv">{v}</span>
            </div>
          ))}
        </div>

        {/* ── CLASS FEATURES (2-col grid, pushed to bottom) ── */}
        <div className="rp-feats">
          {(char.abilities || []).map((a: string, i: number) => (
            <div key={i} className="rp-feat-item">
              <span className="rp-fi">{['⚔','🗡','🛡','✦'][i] ?? '✦'}</span>{a}
            </div>
          ))}
        </div>
        </div>

      {/* ════════════════════════════════════════════════════════
          FACE AREA — Catch phrase + prestige
          ════════════════════════════════════════════════════════ */}
      <div className="skin-face" style={pct(450,385,380,290)}>
        {char.prestige > 0 && <div className="fa-prestige">★ Prestige {char.prestige}</div>}
      </div>
    </div>
    </>
  )
}
