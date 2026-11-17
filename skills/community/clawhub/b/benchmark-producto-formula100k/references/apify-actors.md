# Apify Actors curados · Benchmark de Producto F100K

Lista de actors de Apify que esta skill usa. Cada uno se invoca vía MCP `mcp__apify__*`.

---

## 🌟 ACTORS PRIORITARIOS

### 1. Skool Posts Scraper

**Para qué:** extraer posts, miembros y estructura de comunidades de Skool.

**Requiere:** credenciales del miembro (el cliente debe estar adentro, o pagar 1 mes para research).

**Input típico:**
```json
{
  "community_url": "https://www.skool.com/nombre-comunidad",
  "email": "cliente@email.com",
  "password": "***",
  "max_posts": 50
}
```

**Output:** lista de posts con autor, fecha, likes, comments, contenido. Categorías del foro. Lista de cohortes/levels.

---

### 2. Software Review Scraper (G2 / Capterra / Trustpilot)

**Actor:** `zen-studio/software-review-scraper`

**Para qué:** reviews de software / SaaS / herramientas.

**Input:**
```json
{
  "product_name": "Kajabi",
  "platforms": ["g2", "capterra", "trustpilot"],
  "max_reviews_per_platform": 50
}
```

**Output:** rating promedio, # reviews, fecha, pros, cons, reviewer metadata.

**Útil cuando:** el competidor es SaaS o plataforma con reviews públicas.
**NO útil cuando:** el competidor es un curso/comunidad/coaching (no aparecen en G2).

---

### 3. Facebook Ads Library Scraper

**Actor:** `aurumworks/facebook-ads-library`

**Para qué:** ver todos los ads activos de un competidor en Meta (FB + IG).

**Input:**
```json
{
  "page_name": "nombre-página-fb",
  "country": "US",
  "ad_type": "all",
  "max_ads": 100
}
```

**Output:** lista de ads con creativo (imagen/video URL), copy, CTA, fecha de inicio, plataformas donde corre.

**Útil para:** entender qué hooks usa, qué creatividades dominantes, qué ofertas promueve activamente.

---

### 4. TikTok Profile Scraper

**Para qué:** métricas de cuentas de competidores (followers, videos, engagement promedio).

**Útil para:** mapear quién está creciendo, qué tipo de contenido tracciona.

---

### 5. Instagram Profile Scraper

**Para qué:** posts recientes, métricas, hashtags, mentions.

**Útil para:** comparar mix de contenido (reels / carruseles / fotos), frecuencia, engagement.

---

### 6. YouTube Channel Scraper

**Para qué:** videos del canal, views, suscriptores, frecuencia de upload.

**Útil para:** competidores con presencia fuerte en YouTube (cursos/coaches).

---

### 7. Google Search Results Scraper

**Para qué:** ver SERPs reales de queries del nicho — qué dominios rankean.

**Útil para:** detectar quién paga por SEO, qué competidores están invisibles en orgánico.

---

### 8. LinkedIn Profile Scraper

**Para qué:** bio, experiencia, posts del fundador del competidor.

**Útil para:** validar autoridad real ("decían 10 años de experiencia, pero en LinkedIn dice 2") y ver de qué hablan profesionalmente.

---

### 9. Web Scraper (genérico)

**Para qué:** cualquier sitio sin actor especializado.

**Útil cuando:** el competidor tiene plataforma propia (no Skool/Kajabi/etc.) y queremos extraer su pricing/landings.

---

## 💰 COSTOS APROXIMADOS

Apify cobra por uso. Free tier de $5/mes generalmente alcanza para 1-2 benchmarks pequeños.

| Actor | Costo aprox |
|-------|-------------|
| Skool scraper | $0.50 por 100 posts |
| G2 reviews | $0.30 por 100 reviews |
| FB Ads Library | $0.50 por 100 ads |
| TikTok profile | $0.10 por perfil |
| IG profile | $0.10 por perfil |
| YouTube channel | $0.20 por canal con 100 videos |
| Google SERP | $0.05 por query |
| LinkedIn profile | $0.30 por perfil |
| Web scraper genérico | $0.25 por página |

**Estimación para benchmark Estándar (10 competidores):**
- Skool scrape (3 comunidades con login): $1.50
- G2/Capterra reviews (5 SaaS): $1.50
- FB Ads (10 páginas): $5
- IG profiles (10): $1
- YouTube (5 canales): $1
- Google SERPs (20 queries): $1
- Web scraper (10 landings extras): $2.50
- **TOTAL: ~$13-15** (sale del free tier de $5, requiere $10 extras)

**Estimación Express (5 competidores):**
- $5-8 total — entra en free tier

**Estimación Deep (15-20 competidores):**
- $25-35

---

## 📚 DOCUMENTACIÓN OFICIAL

- Apify MCP server: https://mcp.apify.com/
- Apify Store: https://apify.com/store
- Setup con Claude: https://use-apify.com/blog/apify-mcp-claude-desktop
