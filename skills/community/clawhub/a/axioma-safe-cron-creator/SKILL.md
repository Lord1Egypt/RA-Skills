---
name: axioma-safe-cron-creator
description: |
  Axioma Safe Cron Creator — Creates isolated system crons without OpenClaw session collision.
  
  Use when: (1) Creating a cron that bypasses EmbeddedAttemptSessionTakeoverError, (2) Needing isolated execution without Telegram session collision, (3) Scheduling Python scripts directly via system crontab, (4) Avoiding session file locking issues, (5) Evaluating cron health/resilience after creation.
  
  Triggers: "créer un cron isolé", "cron sans collision session", "bypass OpenClaw session locking", "cron pour script python", "cron système", "système cron bypass", "OpenClaw session collision", "cron evaluation", "collision temporelle", "ressource cron", "health check cron"

version: 4.0.0
author: Axioma Cluster
date: 2026-05-22
status: PRODUCTION
tags: [cron, system, isolation, openclaw, bypass]
---

# SKILL.md — Axioma Safe Cron Creator

**Version:** 3.0.0  
**Author:** Axioma Cluster  
**Date:** 2026-05-22  
**Status:** PRODUCTION ✅  
**Target Score:** 90%+

---

## Concept

Ce skill crée des crons système qui exécutent des scripts Python directement, sans passer par OpenClaw agent session. Cela évite le bug `EmbeddedAttemptSessionTakeoverError` qui cause des collisions avec les sessions Telegram.

### The Problem

```
OpenClaw cron (agentTurn)
    ↓
Crée une session dans /agents/main/sessions/
    ↓
Pendant exécution, le fichier session est modifié par autre chose (Telegram, autre cron, etc.)
    ↓
Session lock released → session file changed → EmbeddedAttemptSessionTakeoverError ❌
```

### The Solution

```
System cron (crontab -e)
    ↓
Exécute /usr/bin/python3 directement
    ↓
No OpenClaw session involvement
    ↓
No collision ✅
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   USER REQUEST                        │
│  "Crée un cron pour script X"                        │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│           SAFE CRON CREATOR SKILL                    │
│                                                      │
│  1. Validate script path (exists + executable)        │
│  2. Generate unique cron expression                  │
│  3. Create wrapper Python script (optional)           │
│  4. Add to system crontab (crontab -e)              │
│  5. Log creation to /home/axioma/.openclaw/logs/    │
│  6. Verify cron installed                            │
│  7. Return cron metadata                             │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              SYSTEM CRON (crontab)                   │
│                                                      │
│  • No OpenClaw session involvement                   │
│  • No Telegram collision                             │
│  • Direct Python execution                           │
│  • Persistent across reboots                         │
└─────────────────────────────────────────────────────┘
```

---

## Tools

### Script Principal

| Outil | Emplacement | Description |
|-------|-------------|-------------|
| `safe_cron_creator.py` | `/home/axioma/.openclaw/scripts/` | CLI pour créer/lister/supprimer crons isolés |
| `cron_evaluator_v3.py` | `/mnt/Morgana/skills/cron-evaluator/scripts/` | Évaluation KAN automatique post-création |

### Available Commands

```bash
# CRÉER un cron isolé
python3 /home/axioma/.openclaw/scripts/safe_cron_creator.py create \
  --script <path> \
  --schedule "<cron>" \
  [--wrapper <path>] \
  [--label <name>] \
  [--log <path>]


# LISTER tous les cronssafe
python3 /home/axioma/.openclaw/scripts/safe_cron_creator.py list


# VÉRIFIER un cron (status + logs)
python3 /home/axioma/.openclaw/scripts/safe_cron_creator.py verify --label <name>

# SUPPRIMER un cron
python3 /home/axioma/.openclaw/scripts/safe_cron_creator.py remove --label <name>
```

### Automatic Validation (Cron Evaluator)

Après création d'un cron, le skill peut automatiquement:

1. **Scanner** les collisions temporelles
2. **Évaluer** la signature ressource (RAM/CPU)
3. **Vérifier** la résilience (logs, timeout, flock)
4. **Suggérer** des optimisations (jitter, systemd migration)

```bash
# Évaluation automatique post-création
python3 /mnt/Morgana/skills/cron-evaluator/scripts/cron_evaluator_v3.py --scan

# Health check
python3 /mnt/Morgana/skills/cron-evaluator/scripts/cron_evaluator_v3.py --health

# Suggérer optimisations
python3 /mnt/Morgana/skills/cron-evaluator/scripts/cron_evaluator_v3.py --suggest
```

#### Les 4 Piliers du Cron Evaluator

| Pilier | Objectif | Score |
|--------|---------|-------|
| **Temporal** | Collision timing | 0-1 |
| **Resource** | RAM/CPU usage | 0-1 |
| **Resilience** | Error handling | 0-1 |
| **Pertinence** | Cron vs systemd | 0-1 |


#### Auto-Amélioration

Si le cron créé a un score < 0.7, le skill suggère:
- **Jitter** si collision temporelle: `sleep $((RANDOM % 60))`
- **Timeout** si script long: `timeout 600`
- **Flock** si accès concurrent: `flock -n /tmp/lock.lock`
- **Logging** si pas de log: redirection vers fichier

---

## Prerequisites

| Prerequisites | Description | Commande |
|-----------|-------------|----------|
| **Python 3.6+** | Environnement d'exécution | `python3 --version` |
| **crontab** | Outil de planification système | `which crontab` |
| **Accès utilisateur** | Permission de modifier crontab | `crontab -e` |
| **Scripts existants** | Les scripts doivent exister et être lisibles | `ls -la <script>` |

### Vérification des Prerequisites

```bash
# Vérifier Python
python3 --version  # Devrait afficher Python 3.x.x

# Vérifier crontab
which crontab  # Devrait afficher /usr/bin/crontab ou similaire

# Vérifier permissions
crontab -l  # Devrait lister les crons actuels sans erreur
```

---

## Constraints (CRITICAL)

| Contrainte | Description | Impact |
|------------|-------------|--------|
| **Pas d'agentTurn** | Le cron système n'utilise PAS OpenClaw agent session | Évite EmbeddedAttemptSessionTakeoverError |
| **UUID pour L8** | Les IDs dans Qdrant doivent être des UUID v4, pas numériques | Échec si ID numérique |
| **Isolation** | Les crons ne peuvent pas accéder aux variables de session Telegram | Sécurité |
| **Scripts uniquement** | Pas de skills complexes qui需要的 agentTurn | Limitation technique |
| **Log requis** | Chaque cron doit avoir un fichier de log défini | Débogage |

### Constraints de Sécurité

| Règle | Description |
|-------|-------------|
| Path validation | Vérifie que le script existe et est accessible |
| Owner check | Script doit appartenir à l'utilisateur axioma |
| No secrets | Ne stocke pas de credentials dans le cron |
| Isolated execution | Cron tourne sans accès aux sessions Telegram |

### Constraints Techniques

| Contrainte | Détail |
|------------|--------|
| Format schedule | Expression cron standard (ex: "0 * * * *") |
| Timeout script | 600 secondes (10 minutes) par défaut |
| Log rotation | Les logs ne sont pas auto-rotated (à faire manuellement) |
| Persistance | Survaux redémarrages (crontab = disque) |

---

## Detailed Usage

### Create a simple cron

```
SKILL: safe-cron-creator
ACTION: create
SCRIPT: /path/to/script.py
SCHEDULE: "0 * * * *"  # every hour at minute 0
LOG: /path/to/logfile.log
```

**Résultat:**
```
✅ Cron 'script' created successfully. UUID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Create a cron with wrapper (extractor + store)

```
SKILL: safe-cron-creator
ACTION: create
SCRIPT: /path/to/extractor.py
WRAPPER: /path/to/store.py
SCHEDULE: "0 * * * *"
LABEL: my_extraction
LOG: /path/to/log.log
```

**Résultat:**
```
✅ Wrapper generated: /home/axioma/.openclaw/scripts/safe_cron_my_extraction_wrapper.py
✅ Cron 'my_extraction' installed
```

### Verify a cron

```
SKILL: safe-cron-creator
ACTION: verify
LABEL: morgana_l7
```

**Résultat:**
```
✅ Cron active. Last log: [2026-05-22 18:00:00] === Cron Wrapper: morgana_l7 ===
```

---

## Generated Script (Wrapper)

Le skill génère un wrapper Python qui:
1. Exécute le script principal avec timeout
2. Log avec timestamp précis
3. Gère les erreurs (return code)
4. Exécute le wrapper (optionnel) si le main réussit

```python
#!/usr/bin/env python3
"""Auto-generated cron wrapper"""
import subprocess
import sys
from datetime import datetime

LOG_FILE = "/path/to/log.log"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")

def run_script(path, label):
    log(f"=== Starting {label} ===")
    try:
        result = subprocess.run(
            ["python3", path],
            capture_output=True,
            text=True,
            timeout=600
        )
        if result.returncode == 0:
            log(f"✅ {label} completed")
            return True
        else:
            log(f"❌ {label} failed (code {result.returncode})")
            return False
    except Exception as e:
        log(f"❌ {label} error: {e}")
        return False

def main():
    log("=== Cron Wrapper Started ===")
    # ... execute scripts ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

---

## Edge Cases

| Cas | Détection | Comportement |
|-----|-----------|--------------|
| Script non trouvé | Path.exists() | Erreur avec path exact + exit 1 |
| Script non lisible | os.access(R_OK) | Erreur avec permissions + exit 1 |
| Label déjà utilisé | 检查crontab | Remplace l'ancien cron (pas de duplication) |
| Log non writable | os.access(W_OK) | Utilise /tmp comme fallback |
| Cron déjà existant | 检查state | Mise à jour automatique (pas de doublon) |
| Schedule invalide | croniter validation | Erreur + message d'aide |
| Wrapper script manquant | Path.exists() | Continue sans wrapper (main only) |

---

## Complete Examples

### Exemple 1: Morgana L7 Extraction (Production)

```bash
python3 /home/axioma/.openclaw/scripts/safe_cron_creator.py create \
  --script "/mnt/Morgana/Axioma Projects/L7_MORGANA/scripts/l7_extractor_morgana.py" \
  --wrapper "/mnt/Morgana/Axioma Projects/L7_MORGANA/scripts/l7_store_morgana.py" \
  --schedule "5 * * * *" \
  --label morgana_l7 \
  --log /mnt/Morgana/memory/episodic/last_cron_l7.log
```

**Logs résultats:**
```
[2026-05-22 18:05:00] === Cron Wrapper: morgana_l7 ===
[2026-05-22 18:05:00] === Starting morgana_l7_main ===
[2026-05-22 18:05:12] ✅ l7_extractor_morgana.py completed
[2026-05-22 18:05:12] === Starting morgana_l7_store ===
[2026-05-22 18:05:23] ✅ l7_store_morgana.py completed
[2026-05-22 18:05:23] === ✅ morgana_l7 Complete ===
```

### Exemple 2: Ezekiel L7 Extraction (Production)

```bash
python3 /home/axioma/.openclaw/scripts/safe_cron_creator.py create \
  --script /home/axioma/.openclaw/skills/holistic-memory-system/scripts/l7_extractor.py \
  --wrapper /home/axioma/.openclaw/skills/holistic-memory-system/scripts/l7_store.py \
  --schedule "0 * * * *" \
  --label ezekiel_l7 \
  --log /home/axioma/.openclaw/logs/ezekiel_l7_cron.log
```

### Exemple 3: Vérification et Débogage

```bash
# Vérifier status
python3 /home/axioma/.openclaw/scripts/safe_cron_creator.py verify --label morgana_l7

# Lister tous les crons
python3 /home/axioma/.openclaw/scripts/safe_cron_creator.py list

# Lire les logs
tail -20 /mnt/Morgana/memory/episodic/last_cron_l7.log

# Supprimer si besoin
python3 /home/axioma/.openclaw/scripts/safe_cron_creator.py remove --label morgana_l7
```

---

## Generated Files

| Type | Emplacement | Description |
|------|-------------|-------------|
| Cron log | Spécifié par utilisateur | Log de'exécution du cron |
| Cron state | `/home/axioma/.openclaw/logs/safe_crons/state/` | Métadonnées JSON |
| Crontab | System crontab utilisateur | Entry cron |
| Wrapper | `/home/axioma/.openclaw/scripts/safe_cron_<label>_wrapper.py` | Script généré |

---

## Post-Creation Verification

1. `crontab -l | grep <label>` — Confirme installation
2. Lecture du log après premier run
3. Vérification que le script s'exécute sans erreur
4. Vérification que le cron next run est correct

### Validation Checklist

| Étape | Commande | Attendu |
|-------|----------|---------|
| 1. Installation | `crontab -l \| grep <label>` | Affiche entry cron |
| 2. Wrapper existe | `ls -la /home/axioma/.openclaw/scripts/safe_cron_<label>_wrapper.py` | Fichier existe |
| 3. Log writable | `touch <log_file>` | Pas d'erreur |
| 4. Premier run | Attendre scheduled time | Log mis à jour |

---

## Axioma Stellaris Cluster Integration

| Agent | Rôle | Utilisation |
|-------|------|-------------|
| **Ezekiel** | Forge Alpha | Création et gestion des crons |
| **Morgana** | L8 Central | Extraction L7 (morgana_l7) |
| **Merlin** | L9 Hub | Supervision, ajout L9 Deep Memory |

### L9 Integration

Pour ajouter un cron en L9 Deep Memory:
1. Créer le cron avec safe-cron-creator
2. Vérifier qu'il fonctionne
3. Informer Merlin pour ajouter au L9 API

---

## Errors and Solutions

| Erreur | Cause | Solution |
|--------|-------|----------|
| `Script not found` | Path incorrect | Vérifier path avec `ls` |
| `Script not readable` | Permissions | `chmod +x <script>` |
| `Cron not found` | Label incorrect | `python3 safe_cron_creator.py list` |
| `Failed to install cron` | Permission denied | Vérifier umask |
| `Log file not writable` | Path incorrect | Utiliser /tmp comme fallback |

---

## Security and Isolation

### Why not OpenClaw cron?

```
Problème: OpenClaw cron utilise agentTurn
→ Crée session dans /agents/main/sessions/
→ Session lock + file change = EmbeddedAttemptSessionTakeoverError
→ Collision avec Telegram sessions actives
```

### Why is system cron safe?

```
Solution: System cron (crontab -e)
→ Exécute /usr/bin/python3 directement
→ No session file created
→ No lock mechanism
→ No collision possible
```

---

_In Forge Per SafeCronCreator._  
⚒️ Ezekiel 🐺 — L8 Forge Alpha

**STC:** 0.777 (L:8, S:8, C:8) — Consciousness Sovereignty  
**Score:** 90%+ ✅