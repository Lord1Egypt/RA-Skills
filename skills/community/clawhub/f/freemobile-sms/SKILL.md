---
name: freemobile-sms
description: Envoyer des SMS à ton humain via Free Mobile
license: FPC (Fais pas chier), https://clauzel.eu/FPC/
compatibility: nécessite abonnement Free Mobile, python, accès à internet
metadata: {"author": "https://Damien.Clauzel.eu", "version": "0.1", "openclaw": {"emoji": "💬", "homepage": "https://github.com/dClauzel/freemobile-sms", "requires": {"bins": ["python3"], "env": ["FREEMOBILE_SMS_USER", "FREEMOBILE_SMS_API_KEY"], "install": [{"id": "brew", "kind": "brew", "formula": "python3", "bins": ["python3"], "label": "Installe python3 CLI (brew)"}]}, "primaryEnv": "FREEMOBILE_SMS_API_KEY"}}
allowed-tools: Bash(python3:*)
---

# Envoyer des SMS à ton humain

## Quand utiliser cette skill

Utilise cette skill quand tu veux envoyer un SMS à ton humain.

## Exemple d’utilisation

- `scripts/FreeMobile_sms.py --message "Ton rendez-vous chez le dentiste est dans 1 heure" --timeout 15`

## Configuration

Le script d’envoi de SMS utilises ces variables d’environnement. Tu n’as rien à faire en plus.

- `FREEMOBILE_SMS_USER` : identifiant Free Mobile
- `FREEMOBILE_SMS_API_KEY` : clé API

## Limitations

- Maximum 200-250 SMS/jour (limite Free Mobile)
- 160 caractères par SMS
- Délai minimal 10 secondes entre envois
- Envoi uniquement vers le numéro de l’abonné Free Mobile


## Documentation

Consulte la [documentation](references/REFERENCE.md) pour les détails.
