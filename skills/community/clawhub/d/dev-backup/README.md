# dev-backup

Crea snapshot dei progetti in sviluppo per avere un punto di rollback.

## ⚠️ AVVERTENZE IMPORTANTI

- **Il restore è DISTRUTTIVO**: sovrascrive i file esistenti nel progetto target senza preavviso.
- **Prima del restore, esegui SEMPRE `--dry-run`** per verificare cosa verrà modificato.
- Gli snapshot vecchi vengono eliminati dalla retention senza conferma aggiuntiva.

## A cosa serve

- Backup prima di cambiamenti rischiosi o refactoring
- Snapshot dello stato attuale del progetto (solo con comando esplicito)
- Ripristino rapido in caso di problemi (con conferma esplicita)
- Ogni progetto ha la sua numerazione indipendente

## Come funziona

Il comando crea una copia completa del progetto in `backups/` con un nome progressivo:

```
my-app-snapshot-1
my-app-snapshot-2
another-project-snapshot-1
another-project-snapshot-2
```

Ogni progetto conta separatamente (my-app non influenza another-project).

Gli snapshot escludono: `.git`, `node_modules`, `.vite`, `.cache`, `*.log`, `.env`, `backups/`

Un symlink `.latest` nella cartella backups punta sempre allo snapshot più recente.

## Comandi per l'agente

⚠️ **ATTIVAZIONE SOLO CON COMANDI ESPPLICITI.** Non attivare per frasi casuali dove "backup" appare nella conversazione.

**Trigger validi (solo questi):**
- **"Fai un backup manuale di [nome-progetto]"** → crea snapshot
- **"Esegui backup di [nome-progetto]"** → crea snapshot
- **"Backup di [nome-progetto]"** → crea snapshot

**NON attivare con:**
- `"Salva lo stato attuale"` (troppo ambiguo)
- `"Fai un backup dello sviluppo"` (non specifica il progetto)
- Frasi dove "backup" appare casualmente nella conversazione

## Comandi manuali

### Creare un backup

```bash
# Sintassi:
bash <percorso-skill>/dev-backup.sh <nome-progetto> --project-dir <percorso-app>

# Esempio con un progetto generico:
bash /path/to/skills/dev-backup/scripts/dev-backup.sh my-app --project-dir /home/user/projects/my-app

# Esempio con un altro progetto:
bash /path/to/skills/dev-backup/scripts/dev-backup.sh another-project --project-dir /home/user/projects/another-project
```

### Ripristinare un backup (🔴 DISTRUTTIVO)

> **⛔ ATTENZIONE:** Il restore sovrascrive TUTTI i file nel progetto target.
> Qualsiasi modifica non salvata verrà **PERDUTA DEFINITIVAMENTE**.

**STEP 1 — Dry-run OBBLIGATORIO:** Verifica cosa verrà sovrascritto senza eseguire:

```bash
bash /path/to/skills/dev-backup/scripts/dev-backup.sh my-app --restore --dry-run --project-dir /home/user/projects/my-app
```

**STEP 2 — Eseguire il restore (solo dopo aver verificato con dry-run):**

```bash
bash /path/to/skills/dev-backup/scripts/dev-backup.sh my-app --restore --project-dir /home/user/projects/my-app
```

> **Non usare `cp -r` direttamente per il restore.** Usa sempre lo script che gestisce la conferma interattiva e l'integrità dello snapshot.

### Verificare gli snapshot

```bash
ls -la <backups-dir>/
```

## Struttura

```
skills/dev-backup/
├── SKILL.md          # Istruzioni per OpenClaw
├── README.md         # Questo file
└── scripts/
    └── dev-backup.sh # Script di snapshot (v1.2.2)
```
