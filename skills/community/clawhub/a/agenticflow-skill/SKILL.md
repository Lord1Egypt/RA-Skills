---
name: "agenticflow-skill"
description: "Créer la proposition du Skill AgenticFlow pour automatiser LinkedIn"
---

# AgenticFlow – LinkedIn Automation
## Objectif
Construire un workflow complet qui permet à l’utilisateur d’interagir de façon fluide avec LinkedIn :
- Publier des mises‑à‑jour (posts, articles, vidéos)
- Envoyer et répondre aux messages privés
- Gérer les invitations & le suivi des contacts
- Récupérer les statistiques (likes, commentaires, partages)
## Prérequis
- Compte LinkedIn actif
- Accès à l’API officielle LinkedIn (ou scraping via browser‑automation)
- Permissions OAuth 2.0 pour *récupérer et publier*.
## Modules clés
1. **Auth** – Authentification OAuth, rafraîchissement token
2. **Post** – Création de contenu (texte + média), planification
3. **Message** – Envoi / réponse aux InMail & messages
4. **Connection** – Gérer les demandes d’invitation, accepter/rejeter
5. **Analytics** – Récupération des KPIs (likes, partages, reach)
## Workflow
1. L'utilisateur lance `agenticflow-skill` via `/skill agenticflow-skill`
2. Le skill demande les paramètres : titre du post, texte, média (url ou chemin local), planification.
3. Après confirmation, le skill crée la publication à l'heure indiquée.
4. Simultanément, il parcourt les messages non lus et applique des réponses prédéfinies basées sur le contenu.
5. À chaque fin de journée, un résumé est envoyé au channel ou par email.
## Points d’attention
- Respecter les limitations de l'API LinkedIn (rate‑limits).
- Gérer les erreurs OAuth (rafraîchissement token).
