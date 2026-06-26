# dev-backup

Crea snapshot dei progetti in sviluppo per avere un punto di rollback sicuro.

## A cosa serve

- Backup prima di cambiamenti rischiosi o refactoring
- Snapshot "salva lo stato attuale" del progetto
- Ripristino rapido in caso di problemi
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

Chiedi all'agente con frasi naturali:

- **"Fai un backup di [nome-progetto]"** → l'agente esegue lo snapshot
- **"Salva lo stato attuale di [nome-progetto]"** → stesso risultato
- **"Fai un backup dello sviluppo"** → l'agente identifica il progetto attivo
- **"Ripristina il backup di [nome-progetto]"** → l'agente copia lo snapshot

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

### Ripristinare un backup

```bash
# Dallo snapshot specifico:
cp -r <backups-dir>/<nome-progetto>-snapshot-2/ <percorso-app>/

# O dallo snapshot più recente (.latest):
cp -r <backups-dir>/.latest/ <percorso-app>/
```

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
    └── dev-backup.sh # Script di snapshot
```
