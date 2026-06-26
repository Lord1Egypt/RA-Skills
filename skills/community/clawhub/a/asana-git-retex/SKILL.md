---
name: asana-git-retex
description: Rétroaction et résolution des points bloquants pour l'automatisation Asana et Git dans KiloClaw.
---

# Asana & Git Automation Retex

Ce skill documente les points de friction rencontrés lors de l'exécution des workflows automatisés (Asana → KiloClaw et sauvegarde Git) et les solutions appliquées pour garantir une exécution fluide.

## 🔍 Points Bloquants Identifiés & Solutions

### 1. Token GitHub Expiré ou Invalide
- **Symptôme** : Échec silencieux du `git push` lors de la sauvegarde hebdomadaire, erreur HTTP 401.
- **Cause** : Le Personal Access Token (PAT) GitHub stocké dans l'URL du remote était périmé.
- **Solution** : 
  1. Récupérer le nouveau PAT depuis 1Password (`op item get "GitHub Personal Access Token" --vault "KiloClaw" --fields identifiant --reveal`).
  2. Mettre à jour l'URL du remote : `git remote set-url origin "https://x-access-token:<TOKEN>@github.com/rez0/kiloclaw-workspace.git"`.
  3. **Prévention** : Ajouter une vérification de santé du token (`curl -s -H "Authorization: token $TOKEN" https://api.github.com/user`) dans le script de backup avant toute opération Git.

### 2. Token Asana Désynchronisé
- **Symptôme** : Les tâches Asana assignées à KiloClaw ne sont pas traitées, erreur `401 Not Authorized` lors de l'appel API.
- **Cause** : Le fichier local `~/.config/tokens/asana-kiloclaw.txt` contenait un ancien token, tandis que le token à jour était dans 1Password.
- **Solution** : 
  1. Synchroniser systématiquement le token local avec 1Password avant l'exécution du script : `op item get "Asana" --vault "KiloClaw" --fields identifiant --reveal > ~/.config/tokens/asana-kiloclaw.txt`.
  2. **Prévention** : Modifier le script `asana_daily_fetch.sh` pour qu'il récupère dynamiquement le token via 1Password à chaque exécution, éliminant la dépendance à un fichier statique potentiellement obsolète.

### 3. Structure Incohérente du Fichier d'État Asana
- **Symptôme** : Le script `asana_daily.py` échoue avec l'erreur `'completed_gids'` lors de la tentative de marquage d'une tâche comme "done".
- **Cause** : Le fichier `.asana-task-state.json` avait une structure différente (`processed_gids` au lieu de `completed_gids`) de celle attendue par le script Python.
- **Solution** : 
  1. Corriger manuellement la structure du fichier JSON pour qu'elle corresponde au schéma attendu : `{"completed_gids": [...]}`.
  2. **Prévention** : Ajouter une validation de schéma ou une migration automatique dans `asana_daily.py` pour gérer les anciennes versions du fichier d'état sans planter.

### 4. Fichiers Non Versionnés Polluant le Dépôt
- **Symptôme** : Le script de backup tente de committer des dossiers entiers clonés temporairement (ex: `SkillClaw/`) ou des logs locaux (`records/`).
- **Cause** : Absence de règles d'ignorance dans `.gitignore`.
- **Solution** : 
  1. Ajouter explicitement `SkillClaw/` et `records/` au fichier `.gitignore` du workspace.
  2. **Prévention** : Réviser le `.gitignore` lors de l'installation de tout nouvel outil ou workflow pour éviter l'encombrement du dépôt principal.

### 5. Collisions et Échecs de Jobs Cron (Morning Briefing / Backup)
- **Symptôme** : Double exécution ou échec du "Briefing Quotidien" et du backup hebdomadaire le dimanche à 7h00 (erreur 502 ou conflit de ressources).
- **Cause** : Plusieurs jobs cron (GitHub Awesome Check, Morning Briefing, Git Backup) étaient programmés exactement à la même heure, saturant les ressources ou entrant en conflit. De plus, le Morning Briefing tentait d'appeler un plugin inexistant.
- **Solution** : 
  1. Décaler les jobs non critiques (ex: GitHub Awesome Check) à **7h15** pour laisser la priorité absolue au backup hebdomadaire à 7h00.
  2. Reconfigurer le Morning Briefing pour qu'il exécute directement le script Python local (`scripts/morning_brief.py`) via `agentTurn` avec les outils autorisés (`exec`, `read`, `write`, `message`), plutôt que de dépendre d'un plugin externe.
  3. **Prévention** : Lors de l'ajout d'un nouveau job cron, toujours vérifier l'horaire via `cron list` et éviter les chevauchements avec les fenêtres de backup (dimanche 7h00) ou de brief matinal (8h00).

## 🔄 Intégration au Workflow de Sauvegarde
Ce skill et les corrections apportées (scripts mis à jour, `.gitignore` enrichi) font désormais partie intégrante du périmètre de la **sauvegarde hebdomadaire Git**. Toute future modification de ces mécanismes devra être validée par ce référentiel.