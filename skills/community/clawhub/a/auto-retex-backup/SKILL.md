---
name: auto-retex-backup
description: Automatise la documentation des problèmes résolus et leur sauvegarde immédiate sur Git pour éviter les régressions lors de nouvelles installations.
---

# Auto Retex & Backup Automation

Ce skill définit la procédure obligatoire à suivre par l'agent **dès qu'un problème est résolu**, une configuration corrigée ou un point de friction identifié dans l'automatisation de KiloClaw.

## 🎯 Objectif
Garantir qu'aucun problème ne se reproduise à l'identique, surtout en cas de réinitialisation, de migration ou d'intervention d'un autre agent. Toute solution doit être **documentée** et **versionnée immédiatement**.

## ⚙️ Procédure d'Exécution (Obligatoire après chaque fix)

Lorsqu'un problème est résolu, l'agent doit exécuter les étapes suivantes dans l'ordre, sans attendre de demande explicite de l'utilisateur :

### 1. Documenter le Retex
Ajouter ou mettre à jour une entrée dans le fichier `skills/auto-retex/SKILL.md` (ou créer le fichier s'il n'existe pas) avec le format suivant :
```markdown
### [Date] - [Nom court du problème]
- **Symptôme** : Description concise de l'erreur ou du comportement observé.
- **Cause racine** : Pourquoi cela a échoué (ex: token expiré, collision cron, dépendance manquante).
- **Solution appliquée** : Les commandes ou modifications de code exactes qui ont résolu le problème.
- **Prévention** : Comment éviter que cela ne se reproduise (ex: récupération dynamique via 1Password, décalage d'horaire, ajout au `.gitignore`).
```

### 2. Vérifier les fichiers modifiés
S'assurer que tous les fichiers corrigés (scripts, configs, `.gitignore`, etc.) sont bien présents dans `/root/.openclaw/workspace`.

### 3. Commit et Push immédiats
Exécuter les commandes Git suivantes pour sauvegarder la correction et la documentation :
```bash
cd /root/.openclaw/workspace
git add -A
git commit -m "docs: retex - [Nom court du problème] + correctifs associés"
git push origin $(git branch --show-current)
```
*Note : Si le push échoue à cause d'un token, appliquer la procédure de récupération dynamique du token GitHub via 1Password avant de réessayer.*

### 4. Confirmation à l'utilisateur
Informer l'utilisateur que le problème est résolu **et** que la solution est désormais documentée et poussée sur GitHub, en fournissant le hash du commit.

## 📂 Fichiers de référence
- Documentation des retex : `skills/auto-retex/SKILL.md`
- Script de backup de référence : `clawflows/workflows/enabled/git-weekly-backup-workflow/scripts/backup.sh`

## ⚠️ Règle d'or
**"Pas de documentation, pas de résolution."** 
Si l'agent résout un problème mais oublie de committer la documentation, la tâche est considérée comme incomplète.