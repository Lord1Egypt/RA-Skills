# Pinecone Setup - Manuelle Schritte

## 1. Pinecone Account

Gehe zu: **https://www.pinecone.io**

### Schritte:
1. **Sign up** (Free Tier ist perfekt für Testing!)
2. **Verify Email** (Check deine Inbox)
3. **Log in** to Dashboard

### Free Tier Limits:
- ✅ 1 Index (ausreichend!)
- ✅ 100,000 Vectors (mehr als genug für Skills)
- ✅ Serverless oder p1.x1 Pod Type
- ✅ Keine Kreditkarte erforderlich

---

## 2. Index erstellen

### Dashboard → Create Index

Fill in:

| Field | Value | Beschreibung |
|-------|-------|--------------|
| **Name** | `deepallspeak-skills` | Index Name (muss exakt so sein!) |
| **Dimensions** | `1536` | Für OpenAI text-embedding-3-small |
| **Metric** | `cosine` | Für Semantic Search |
| **Pod Type** | `serverless` (empfohlen) ODER `p1.x1` (free tier) | Serverless ist günstiger |
| **Region** | `us-east-1` (oder deine Region) | Wähle nächstgelegene Region |

### Wichtig:
- ⚠️ **Name muss exakt** `deepallspeak-skills` sein!
- ⚠️ **Dimensions muss** `1536` sein (für OpenAI Embeddings)
- ⚠️ **Metric muss** `cosine` sein (für Semantic Search)

### Schritte:
1. Click **"Create Index"**
2. Warte ~1 Minute (Index wird initialisiert)
3. Status sollte **"Ready"** sein

---

## 3. API Credentials holen

### Dashboard → API Keys

Kopiere folgende Werte:

1. **API Key**:
   ```
   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```
   (Format: UUID)

2. **Environment**:
   ```
   us-east-1
   ```
   (oder deine gewählte Region, z.B. `us-west1-gcp`, `eu-west1-gcp`)

### Wichtig:
- ⚠️ Der API Key ist **geheim**! Teile ihn niemals öffentlich.
- ⚠️ Environment muss zur Region deines Index passen.

---

## 4. Credentials in .env eintragen

**Augment wird dies für dich tun!**

Die Datei ist: `C:\Download\speakmcp projekt\SpeakMCP\mcp-servers\.env`

Folgende Werte werden eingetragen:
```bash
PINECONE_API_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=deepallspeak-skills
```

---

## 5. Verifizieren

### Im Pinecone Dashboard:

1. Gehe zu **Indexes** → `deepallspeak-skills`
2. Status sollte **"Ready"** sein
3. **Vectors**: 0 (normal, noch keine Skills erstellt)
4. **Dimensions**: 1536 ✅
5. **Metric**: cosine ✅

---

## 6. Wie funktioniert Semantic Search?

### Beispiel:

**User sucht**: `"analyze customer feedback"`

**Pinecone findet**:
- `sentiment-analysis-tool` (Score: 0.92)
- `customer-review-analyzer` (Score: 0.89)
- `feedback-processor` (Score: 0.85)

**Auch wenn**:
- Keine exakte Keyword-Übereinstimmung
- Verschiedene Wörter verwendet werden
- Synonyme genutzt werden

**Weil**: Pinecone versteht die **Bedeutung** der Wörter, nicht nur die Buchstaben!

---

## 7. Troubleshooting

### Problem: "Index name already exists"
**Lösung**: Wähle einen anderen Namen ODER lösche den existierenden Index.

### Problem: "Dimension mismatch"
**Lösung**: Stelle sicher, dass Dimensions = 1536 (für text-embedding-3-small).

### Problem: "Invalid API Key"
**Lösung**: Kopiere den API Key erneut aus dem Dashboard.

### Problem: "Environment not found"
**Lösung**: Prüfe, dass Environment zur Region deines Index passt.

---

## 8. Kosten

### Free Tier:
- ✅ **Serverless**: $0.00 (bis 100K Vectors)
- ✅ **p1.x1**: $0.00 (1 Pod, begrenzte Kapazität)

### Paid Tier (falls du mehr brauchst):
- **Serverless**: ~$0.10 pro 100K Vectors/Monat
- **p1.x1**: ~$70/Monat (dedicated Pod)

**Für DeepAllSpeak**: Free Tier ist mehr als ausreichend! 🎉

---

## 9. Nächste Schritte

Nach erfolgreichem Setup:
1. ✅ Pinecone Account erstellt
2. ✅ Index `deepallspeak-skills` erstellt
3. ✅ API Credentials kopiert
4. ⏭️ **Weiter zu**: OpenAI API Key Setup

---

**Bereit für OpenAI Setup!** 🚀

