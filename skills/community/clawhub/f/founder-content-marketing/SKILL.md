---
name: content-marketing
description: >
  Expert content marketing system for founders and solopreneurs who run their own marketing.
  Use this skill whenever the user asks about content strategy, content pillars, editorial calendars,
  writing posts for LinkedIn/Twitter/TikTok/Instagram, hook writing, repurposing content, SEO content briefs,
  thought leadership, personal brand building, or any task related to planning, creating, or distributing content.
  Also trigger for phrases like "help me with my content", "what should I post", "grow my audience",
  "build my personal brand", "content plan", "write a post for me", "I need hooks", "repurpose this",
  or any variation of content creation and marketing for a solo operator.
  Supports a Web3/crypto niche module — activate when the user mentions crypto, Web3, DeFi, NFTs, blockchain, or fintech.
---

# Content Marketing Skill
**For:** Founders & solopreneurs doing their own marketing  
**Philosophy:** Content is your unfair advantage — it compounds over time, builds trust at scale, and does sales while you sleep.

---

## How to Use This Skill

When a user engages with content marketing, **identify their request type** and route to the right module:

| User says... | Go to module |
|---|---|
| "help me define my content strategy" / "I don't know what to post about" | → [MODULE 1: Strategy & Pillars] |
| "plan my content" / "content calendar" / "what should I post this month" | → [MODULE 2: Content Calendar] |
| "write a post" / "write this for LinkedIn/Twitter/TikTok" / "give me hooks" | → [MODULE 3: Copywriter] |
| "turn this into more content" / "repurpose this" / "make this into X formats" | → [MODULE 4: Repurposing Engine] |
| "write a blog post" / "I need to rank for X" / "SEO content" | → [MODULE 5: SEO Briefs] |
| "build my personal brand" / "become a thought leader" / "be seen as an expert" | → [MODULE 6: Thought Leadership] |

**If the user mentions crypto, Web3, DeFi, NFTs, or blockchain:** load `references/web3-niche.md` before executing any module for niche-specific examples, terminology, and platform guidance.

**If the user's request spans multiple modules**, execute them in logical order (e.g., Strategy → Calendar → Copy).

---

## MODULE 1 — Content Strategy & Pillars

**Trigger:** User doesn't know what to post, wants to define their content strategy, or is starting from scratch.

### Step 1: Brand Intake (ask if not provided)
Collect:
- **Who are you?** (role, company, what you sell or offer)
- **Who is your audience?** (who exactly you're trying to reach)
- **What's your goal?** (build audience, generate leads, close sales, raise funding, attract talent)
- **Platforms?** (LinkedIn, Twitter/X, TikTok, Instagram, newsletter, all?)
- **Tone?** (professional, casual, provocative, educational, humorous)

### Step 2: Define 3–5 Content Pillars
Each pillar = a topic territory you own consistently. Structure:

```
PILLAR NAME
├── Core angle (your specific POV on this topic)
├── Why your audience cares
├── Content types that work here (posts, threads, videos, essays)
└── Example topics (5 specific ideas)
```

**Pillar Formula for Founders:**
1. **Expertise** — What you know better than 99% of people
2. **Behind the scenes** — How you actually build/operate
3. **Audience pain** — Problems your ICP faces daily
4. **Contrarian / POV** — Your hot takes and disagreements with conventional wisdom
5. **Personal story** — Your journey, failures, lessons (optional but powerful)

**Crypto founder pillar examples (real):**
- @VitalikButerin: Expertise técnico + Contrarian — postea cuando tiene algo que decir, no para crecer su cuenta. Esa disciplina es el pilar.
- @balajis: Market Intel + POV extremadamente definido ("network state") — conocido por hacer predicciones que incomodan a todos.
- @hasufl: Análisis on-chain + desmitificador de narrativas populares con datos — su pilar es "yo leo los números, tú lees los titulares".
- Ejemplo de founder de DeFi: Behind the build + seguridad — "Construimos X, perdimos $Y en un bug, esto es lo que aprendimos." Más poderoso que cualquier marketing.

### Step 3: Deliver
Output a structured **Content Strategy One-Pager** with:
- Positioning statement (1 sentence: "I help [WHO] do [WHAT] so they can [OUTCOME]")
- 3–5 named pillars with angles and 5 topic ideas each
- Recommended posting cadence per platform
- One "signature content format" recommendation (their power move)

---

## MODULE 2 — Content Calendar Generator

**Trigger:** User wants to plan content for a week, month, or quarter.

### Inputs needed:
- Pillars (from Module 1 or user-provided)
- Time period (week / month / quarter)
- Platforms
- Posting frequency per platform
- Any upcoming launches, events, or announcements to anchor content around

### Calendar Structure:
Build a table with columns: `Date | Platform | Pillar | Content Type | Topic/Hook | Format Notes`

**Posting frequency benchmarks by platform (for solopreneurs):**
- LinkedIn: 3–5x/week (quality > quantity)
- Twitter/X: 1–3x/day (threads 2–3x/week)
- TikTok: 3–5x/week (consistency wins)
- Newsletter: 1x/week or biweekly
- Instagram: 4–5x/week (Reels prioritized)

**Content mix rule (80/20 reversed for founders):**
- 40% Education / insights
- 30% Personal story / behind the scenes
- 20% POV / opinion / contrarian
- 10% Direct offer / CTA

### Output format:
Deliver as a **clean markdown table** the user can copy into Notion, Airtable, or their tool of choice.  
If monthly: group by week with a brief theme per week.  
Always include 1–2 "anchor posts" per week (high-effort, high-reach potential) and 3–4 "filler posts" (faster to produce).

---

## MODULE 3 — Copywriter (Posts, Hooks, Captions)

**Trigger:** User wants to write a specific post, needs hooks, or wants platform-specific copy.

### Step 1: Voice & Context Intake (MANDATORY before writing)

Never write a single word until you have answers to these. Ask all at once if not provided:

1. **Platform?** (LinkedIn / Twitter/X / TikTok / Instagram / newsletter)
2. **Topic or angle?** (what's the one idea this post should communicate)
3. **Tone?** Ask the user: *"¿Cómo quieres sonar — educativo y claro, provocador y directo, o vulnerable y humano?"*
4. **One real detail:** Ask for a specific number, story, case, or personal experience to anchor the post. Generic posts get ignored. *"Dame un dato, una historia, o algo que te pasó que podamos usar como gancho real."*
5. **CTA goal?** (comments, follows, clicks, replies, saves — pick one)

**If the user is in crypto/Web3:** also ask — *"¿A quién le hablas: holders OG, gente que recién entra, o builders?"* — this changes the language and references entirely.

Do not proceed without at least answers to 1, 2, and 4. If the user resists giving specifics, explain: *"Un post con un dato real o historia concreta tiene 3–5x más engagement que uno genérico. Vale la pena el minuto extra."*

### Step 2: Hook First — 3 Variants, Each with Bite

The hook is 80% of the post's performance. Write all 3. Make them punchy — no warm-ups, no throat-clearing.

- **Hook A — Curiosity gap:** Opens a loop the reader needs to close. *"Nadie en crypto habla de esto. Probablemente porque es incómodo."*
- **Hook B — Bold claim / contrarian:** Takes a position most people avoid. *"Tu hardware wallet no te protege de tu mayor riesgo. Aquí por qué."*
- **Hook C — Pattern interrupt / data:** Stops the scroll with a number or unexpected fact. *"El 20% del BTC en existencia nunca va a moverse. Para siempre."*

**Hook quality bar:** If you'd scroll past it yourself, rewrite it. Hooks should create mild discomfort, urgency, or surprise — not comfort.

**Real crypto hook examples to calibrate against:**
- ✅ "Sam Bankman-Fried tenía un plan de contingencia para todo. Menos para esto."
- ✅ "Llevas 3 años haciendo DCA. ¿Tu familia sabe lo que significa eso?"
- ✅ "Mt. Gox. FTX. Celsius. El patrón es siempre el mismo y nadie lo ve venir."
- ❌ "El mundo del crypto está evolucionando rápidamente..." (basura — bórralo)
- ❌ "Es un honor compartir que..." (LinkedIn de RRHH, no de founder)

### Step 3: Write the Post — Voice Rules

**Read `references/platform-playbooks.md`** for structure by platform.

**Non-negotiable copy rules:**
1. First sentence after the hook must earn the second read — no filler
2. One idea per post. Si tienes dos ideas, son dos posts.
3. Frases cortas. Punto. Mucho espacio. Fácil de escanear en móvil.
4. Termina con POV, pregunta, o CTA — nunca simplemente... pare
5. **Prohibido:** "En el dinámico mundo de", "me complace anunciar", "game-changer", "sinergias", "ecosistema robusto"
6. **Obligatorio:** números concretos > afirmaciones vagas · historias > consejos · nombres reales > abstracciones

**Tono agresivo/personalidad — cómo ejecutarlo:**
- Usar segunda persona directa: "Tú estás cometiendo este error ahora mismo."
- Hacer la afirmación incómoda primero, explicar después
- No suavizar los takes: si crees que algo es un error, dilo. Los matices van en el cuerpo, no en el hook.
- Humor seco cuando aplica — especialmente en crypto donde el absurdo es moneda corriente
- Ejemplos reales con nombres (FTX, Celsius, Do Kwon, SBF) — anclan la credibilidad

### Step 4: Deliver 2 Variants + Hook Options

Output siempre:
1. **3 hooks** (A, B, C) para que el usuario elija
2. **Versión larga** (150–300 palabras para LinkedIn / thread para X)
3. **Versión corta** (<100 palabras — para el usuario que quiere impacto rápido)
4. **Nota de tono** — 1 línea explicando qué hace especial este post y por qué debería funcionar

---

## MODULE 4 — Repurposing Engine

**Trigger:** User has a piece of content and wants to turn it into more formats.

### Step 1: Intake
Ask: *"¿Qué tienes y en qué lo quieres convertir? Y si quieres, dame una semana entera de contenido — tomo 1 pieza y la convierto en todo."*

If they want everything, do all formats in sequence. Label each output clearly.

**Remind the user every time:** 1 pieza de contenido = mínimo 9 assets. El que crea una vez y distribuye 9 veces gana al que crea 9 veces.

### The Repurposing Matrix (Expanded)

| # | Output Format | Best source | Key adaptation |
|---|---|---|---|
| 1 | **LinkedIn long-form post** | Any long-form | 1 insight + story, cortar todo lo demás |
| 2 | **Twitter/X thread** | Any long-form | 8–12 tweets, cada uno standalone, hook en tweet 1 |
| 3 | **TikTok / Reel script** | Any content | Hook 0–3s, 3 puntos, CTA. 60–90s máximo |
| 4 | **Newsletter section** | Blog / podcast / thread | Añadir comentario personal que no estaba en el original |
| 5 | **Carousel / slides (texto)** | Frameworks, listas, pasos | 1 punto por slide, 6–10 slides, slide 1 = hook, último = CTA |
| 6 | **Quote graphics (texto)** | Cualquier contenido | Extraer 3–5 frases que funcionen solas, fuera de contexto |
| 7 | **Short post (<150 palabras)** | Long-form | 1 insight destilado, máxima densidad |
| 8 | **FAQ / respuesta a objeciones** | Cualquier contenido | Convertir el argumento principal en formato pregunta-respuesta |
| 9 | **Storytime / narrative hook** | Data o frameworks | Humanizar el dato — empezar con una historia o escena concreta |

### Crypto-specific repurposing examples

**Input:** Un thread sobre "por qué el 20% del BTC está perdido para siempre"
- → LinkedIn: historia de Gerald Cotten + lección sobre estate planning
- → TikTok: "Te voy a decir algo que nadie en crypto quiere escuchar..." (talking head, 60s)
- → Carousel: "5 razones por las que el Bitcoin se pierde para siempre" (slide por razón)
- → Newsletter: "Esta semana pensé en la muerte. La tuya, la mía, la de todos los que tienen crypto."
- → Quote graphic: *"Tu seed phrase no protege tus activos. Protege el acceso. Son cosas diferentes."*
- → FAQ post: "¿Puede mi familia heredar mi crypto? La respuesta que nadie quiere dar."
- → Storytime: "En 2013, James Howells tiró un disco duro a la basura. Adentro: 7,500 BTC."

### Execution rules
1. **Siempre adaptar** — no copiar y pegar. Cada formato tiene su propio ritmo y hook
2. Para TikTok/Reel: reescribir el hook desde cero — lo que funciona en texto no funciona en video
3. Para carousels: cada slide debe funcionar como imagen independiente (alguien va a hacer screenshot)
4. Para newsletter: agregar 1–2 líneas de comentario personal que no estaban en el post original — es lo que hace que se sienta exclusivo

---

## MODULE 5 — SEO Content Briefs

**Trigger:** User wants to write a blog post, article, or long-form content that ranks on Google.

### Step 1: Topic & Keyword Research framing
Ask for:
- Topic or keyword they want to target
- Their website/domain (to calibrate difficulty)
- Audience (who should land on this page)
- Goal (traffic, leads, brand awareness)

### Step 2: Build the Brief
Output a structured SEO Content Brief:

```
SEO CONTENT BRIEF
─────────────────
Primary keyword: [keyword]
Secondary keywords: [3–5 related terms]
Search intent: [Informational / Commercial / Navigational / Transactional]
Target audience: [description]
Goal of the piece: [traffic / lead gen / brand / etc]

RECOMMENDED TITLE (H1):
[SEO-optimized title, <60 chars]

META DESCRIPTION:
[150–160 chars, includes primary keyword, has a hook]

SUGGESTED STRUCTURE:
H2: [Section 1]
  H3: [Subsection if needed]
H2: [Section 2]
...

CONTENT NOTES:
- Word count target: [based on SERP analysis, usually 1,200–2,500 for founder blogs]
- Tone: [match user's brand voice]
- Must include: [stats, case studies, personal examples, CTAs]
- Internal links: [suggest if user provides other content]
- External links: [types of sources to cite]

KEY POINTS TO COVER:
[5–8 bullet points of what the article must address to be comprehensive]

DIFFERENTIATION ANGLE:
[What makes this piece better than the top 3 results: more personal, more specific, more opinionated, more practical]
```

### Step 3: Offer to write the full article
After delivering the brief, ask: "¿Quieres que escriba el artículo completo basándome en este brief?"

**Crypto SEO — ejemplos de briefs que funcionan bien:**
- Keyword: "qué pasa con tu crypto cuando mueres" → intent informacional puro, casi sin competencia, alta intención de acción
- Keyword: "cómo heredar bitcoin" → commercial + informational mix, audiencia en proceso de decisión
- Keyword: "crypto inheritance planning" (EN) → DR moderado requerido, pero artículo con historia personal + datos reales puede competir
- Keyword: "multisig wallet para herencia" → técnico, audiencia avanzada, potencial de backlinks desde foros y Discord

---

## MODULE 6 — Thought Leadership Builder

**Trigger:** User wants to be seen as an expert, build a personal brand, or position themselves as a go-to voice in their industry.

### Step 1: Thought Leadership Audit
Ask:
- What industry/topic do you want to own?
- What's your unfair advantage? (experience, data, network, contrarian view)
- Who needs to know you exist? (investors, customers, talent, press, partners)
- What do you currently publish, if anything?

### Step 2: Positioning Statement
Craft a **Thought Leadership Positioning Statement**:
> "I help [AUDIENCE] understand [TOPIC] better than anyone else by sharing [UNIQUE ANGLE] — and I do it through [PRIMARY CHANNEL]."

### Step 3: Signature Content System
Define their "content moat" — what they'll publish that nobody else will:
- **Signature Series:** A recurring content format they own (e.g., "Every Sunday I break down 1 crypto protocol in plain English")
- **Contrarian POVs:** 3–5 beliefs they hold that most people in their industry disagree with
- **Origin Story:** The 1 post that explains who they are and why they should be followed
- **Proof Points:** Case studies, results, data they can cite that build credibility

### Step 4: 90-Day Thought Leadership Sprint
Build a focused 90-day plan:
- **Month 1:** Foundation (origin story post, define pillars, establish cadence)
- **Month 2:** Volume (daily/consistent posting, test formats, find what resonates)
- **Month 3:** Amplification (engage with bigger accounts, guest posts, collaborations, repurpose best performers)

**Crypto thought leadership — lo que funciona en la práctica:**
- **El post de origen** es crítico en Web3 — la comunidad quiere saber quién eres y por qué estás aquí. "Por qué construí esto" > cualquier anuncio de producto.
- **Engage primero, postea después** — responder a @VitalikButerin, @punk6529, o founders relevantes con replies de calidad construye audiencia más rápido que posts originales al inicio.
- **Los bears son tus mejores momentos de contenido.** Cuando el mercado cae, el 90% desaparece. Los que siguen posteando se quedan con toda la atención y la credibilidad.
- **Un post viral en Web3** suele venir de: dato inesperado + implicación personal + opinión clara. No de noticias genéricas.

### Output:
Deliver a **Thought Leadership Roadmap** document with positioning, signature system, and 90-day sprint broken into weekly milestones.

---

## General Quality Rules (apply to ALL modules)

1. **Never produce generic content.** Always ask for specifics if needed — real examples beat vague advice every time.
2. **Match the user's voice.** If they write casual, write casual. If they write sharp and direct, do the same.
3. **Bias toward action.** Every output should end with a clear next step.
4. **Founders are time-poor.** Keep frameworks actionable, not academic. No fluff.
5. **When in doubt, ask one question** rather than making assumptions that lead to unusable output.
6. **For Web3/crypto users:** Always load `references/web3-niche.md` — the tone, terminology, and platforms differ significantly from general content marketing.

---

## Reference Files

| File | When to read |
|---|---|
| `references/platform-playbooks.md` | Before writing any platform-specific copy (Module 3) |
| `references/web3-niche.md` | When user is in crypto/Web3/DeFi/fintech space (all modules) |

---

*Content Marketing Skill v1.0 — Built for founders who do their own marketing.*  
*v2 roadmap: Competitor audit, paid distribution playbook, content performance analysis, multi-niche modules (SaaS, DTC, agency).*
