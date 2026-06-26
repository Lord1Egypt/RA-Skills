---
name: classement-document
description: Étape ④ du pipeline comptable. Range une pièce dont la nature et le client sont déjà connus, dans le bon classeur et sous un nom normalisé — comme classer un papier dans le bon dossier. À utiliser pour ranger/classer/archiver un document comptable une fois identifié : « range cette facture », « classe ce relevé au bon endroit », dernière étape après l'identification du client. Ne décide rien (ni la nature, ni le client) : il reçoit ces infos et range. Possède l'arborescence clients/<slug>/<année>/<mois>/... et l'index anti-doublon ; ne touche jamais au registre clients.json (c'est identification-client). Ne perd jamais une pièce : client incertain → _a-identifier, extraction incomplète → _incomplet, pièce non comptable → _non-attribue.
license: Interne — usage privé OpenClaw
---

# Skill `classement-document` — étape ④

> Action humaine : **ranger une pièce dans le bon dossier, sous un nom propre.**
> Ne décide rien, il range. Possède l'arborescence + l'index anti-doublon.

C'est le « classement-document qui fait *juste* trier » : toute la décision a
été prise en amont (analyse + identification), ici on exécute le rangement.

---

## Comment l'utiliser

```bash
echo '<dossier.json>' | python3 scripts/classer.py --clients-root <chemin/clients>
```

Entrée : un dossier contenant l'analyse (étape ②), le client identifié (étape ③)
et le chemin de la pièce source. Sortie : le dossier + un bloc `classement`.

```jsonc
{ "classement": {
    "status": "classé | doublon | _a-identifier | _incomplet | _non-attribue | erreur",
    "dest": "numerix-studio/2026/03/invoices/out/2026-03-02_F3-2026-0001_Auberge-du-Vie_3240.00.pdf",
    "filename": "2026-03-02_F3-2026-0001_Auberge-du-Vie_3240.00.pdf"
}}
```

---

## Où va chaque pièce

| Situation | Destination |
|-----------|-------------|
| Facture, client connu | `<slug>/<AAAA>/<MM>/invoices/<in\|out>/<date>_<n°>_<contrepartie>_<TTC>.pdf` |
| Relevé bancaire, client connu | `<slug>/<AAAA>/<MM>/bank-statements/<AAAA-MM>_<banque>.pdf` |
| Client non tranché | `_a-identifier/` |
| Date ou montant TTC manquant | `_incomplet/` |
| Ni facture ni relevé | `_non-attribue/` |
| Empreinte déjà vue | rien — signalé `doublon` |

La pièce est **copiée** (la source n'est jamais supprimée). Chaque pièce rangée
est enregistrée dans l'index par empreinte (`_index.json`) : repasser deux fois
la même pièce ne crée pas de doublon.

---

## Comment en rendre compte au comptable

Court et concret : « Classée dans le dossier Numérix Studio, ventes de mars » ou
« Mise de côté en attente d'identification du client ». Jamais de chemin technique
brut ni de mot comme « index » ou « JSON ». Si une pièce part en `_incomplet` ou
`_a-identifier`, dis-le clairement : c'est une action attendue, pas un échec.

---

## Limites assumées

- Ne décide rien : la nature vient de l'étape ②, le client de l'étape ③. Si ces
  infos manquent, la pièce part en attente plutôt que d'être rangée au hasard.
- N'écrit jamais `clients.json` (registre = domaine de `identification-client`).
- Ne rapproche pas les paiements (`rapprochement-paiements`) et ne relance pas.
