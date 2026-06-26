# Datenquellen für feeds-digest (Stand 2026-06-07)

Welche Quellen funktionieren, welche nicht, und was stattdessen geht.

## ✅ Funktionierende Quellen

### Offizielle Microsoft-Blogs (RSS)
| Quelle | URL | Topics | Bemerkung |
|---|---|---|---|
| Dynamics 365 Blog | `https://cloudblogs.microsoft.com/dynamics365/feed/` | bc, dynamics | Hauptsächlich BC + Customer Engagement |
| Power BI Blog | `https://powerbi.microsoft.com/en-us/blog/feed/` | powerbi | Aktualisiert wöchentlich |

### GitHub Releases (Atom)
- Format: `https://github.com/<owner>/<repo>/releases.atom`
- Liefert Tag, Datum, Release Notes (Body)
- Verifizierte Repos:
  - `microsoft/fabric-samples` — Microsoft-Fabric-Notebooks
  - `microsoft/fabric-toolbox` — Fabric-Tools
  - `openclaw/openclaw` — OpenClaw-Framework
  - `yt-dlp/yt-dlp` — yt-dlp

### YouTube (RSS)
- Format: `https://www.youtube.com/feeds/videos.xml?channel_id=UC...`
- Siehe `youtube-channel-discovery.md` für ID-Finding
- Mögliche Kanäle (IDs selbst finden): Microsoft Dynamics 365, Microsoft Fabric, Power BI, etc.

## ❌ Nicht mehr verfügbar (Stand 2026-06-07)

### Microsoft Tech Community
- **Status:** RSS seit 2025er Redesign abgeschaltet
- Alte URLs (`page_news_rss?category=...`) liefern 404
- Diskussion dazu: `https://techcommunity.microsoft.com/discussions/communityquestions/list-of-all-rss-feeds/4361054`
- **Ersatz:** Offizielle Microsoft-Blogs oben, GitHub Releases für Code-News

### blog.fabric.microsoft.com
- **Status:** Kein RSS-Feed mehr
- Alle üblichen Feed-URLs (`/feed`, `/feed.xml`, `/rss`, etc.) liefern 404
- **Ersatz:** GitHub `microsoft/fabric-samples` + `microsoft/fabric-toolbox` Releases

### community.fabric.microsoft.com (Fabric Updates Blog)
- **Status:** JS-rendered, RSS nicht direkt abrufbar
- URL gibt zwar 200, aber HTML (kein XML) zurück
- **Ersatz:** Manuell checken oder per Browser-Automation scrapen (Phase 4)

## 🔍 Eigene Quellen finden

### RSS-Validierung
```bash
# Schnelltest: gibt die URL valides XML zurück?
curl -sI "<url>" | head -3
# 200 + application/rss+xml oder application/atom+xml = ok
```

### Häufige RSS-Pattern
- WordPress: `/feed/`
- Ghost: `/rss/`
- GitHub: `/releases.atom`, `/commits.atom`, `/issues.atom`
- YouTube: `/feeds/videos.xml?channel_id=...`
- Substack: `/feed`
- Reddit: `https://www.reddit.com/r/<sub>/.rss`

## 📝 Nächste Recherche-Schritte

1. **Dynamics 365 BC-spezifisch:** Suche `businesscentral` in der offiziellen Doku — gibt es einen eigenen RSS-Endpoint?
2. **Power BI Updates:** Wöchentlicher Update-Post wird auf dem Power BI Blog veröffentlicht (gefunden ✅)
3. **Fabric Release Notes:** Werden auf GitHub in `microsoft/fabric-samples` und `microsoft/fabric-toolbox` aktualisiert (gefunden ✅)
4. **OpenClaw:** Releases auf GitHub (gefunden ✅)
