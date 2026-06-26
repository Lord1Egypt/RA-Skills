# dddparser Build Guide

Anleitung zum Bauen des EU-zertifizierten Tachograph-Parsers.

## Voraussetzungen

- **Go 1.21+** – https://go.dev/dl/
- **Git**

## Build-Schritte

```bash
# 1. Repository klonen
git clone https://github.com/traconiq/tachoparser.git /tmp/tachoparser
cd /tmp/tachoparser

# 2. Binary bauen
go build -o dddparser ./cmd/dddparser

# 3. Binary kopieren
cp dddparser ~/.openclaw/workspace/skills/driver-card-tachograph/bin/
chmod +x ~/.openclaw/workspace/skills/driver-card-tachograph/bin/dddparser

# 4. Aufräumen
rm -rf /tmp/tachoparser
```

## Verifizieren

```bash
./bin/dddparser --help
```

## Hinweise

- **Zertifikate:** 1.640 EU JRC Zertifikate werden automatisch eingebettet
- **Unterstützung:** Gen 1 + Gen 2 Tachograph-Karten
- **Lizenz:** MIT