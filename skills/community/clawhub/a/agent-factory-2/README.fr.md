# 🏭 Usine à Sous-Agents pour OpenClaw (Agent Factory)

<p align="center">
  <a href="README.md"><b>English</b></a> •
  <a href="README.fr.md"><b>Français</b></a>
</p>

<p align="center">
  <a href="https://clawhub.ai"><img src="https://img.shields.io/badge/ClawHub-Ready-brightgreen" alt="ClawHub Ready"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License MIT"></a>
  <a href="https://openclaw.ai"><img src="https://img.shields.io/badge/OpenClaw-%E2%89%A50.4.0-purple.svg" alt="Compatibilité OpenClaw"></a>
  <a href="tests"><img src="https://img.shields.io/badge/Tests-8%20R%C3%A9ussis-success" alt="Tests Réussis"></a>
</p>

Skill officiel **Agent Factory** pour l'écosystème **OpenClaw / ClawHub**. Permet aux orchestrateurs OpenClaw de s'auto-spécialiser en continu : interception transparente des requêtes, détection autonome des charges récurrentes, génération sandboxée en conteneur, banc de test 4D avec Red Teaming adversarial, exécution multi-modèles LLM réelle, cache sémantique à 0 token et cartographie visuelle interactive en temps réel.

---

## 🌟 Architecture & Piliers Fondamentaux

```mermaid
graph TD
    User([Requête Client / Entrée]) --> Hook[Middleware Hook OpenClaw Gateway]
    Hook --> Cache{Cache Sémantique >0.98}
    Cache -->|Succès Cache| FastReturn[Réponse Instantanée 0 Tokens]
    Cache -->|Échec Cache| Router[Routeur Vectoriel Dense 64d]
    
    subgraph "Exécution & Télémétrie"
        Router -->|Correspondance Domaine Haute Confiance| SubAgent[Sous-Agent Spécialisé]
        Router -->|Fallback / Hors Périmètre| Generalist[Orchestrateur Généraliste]
        SubAgent --> Container[Sandbox d'Isolation Conteneur]
        Container --> LLM[Moteur LLM Multi-Fournisseurs OpenAI/Anthropic/Gemini/Local]
        LLM --> Telemetry[Collecteur de Télémétrie Réelle]
        Generalist --> Telemetry
    end

    subgraph "Pipeline Usine à Agents (Asynchrone)"
        Telemetry --> StreamCluster[1. Clustering Streaming Non-Supervisé]
        StreamCluster -->|Seuil Dépassé| Synthesizer[2. Synthèse Sandboxée & Tool Pruning]
        Synthesizer --> RedTeam[3. Red Teaming Adversarial & Banc 4D]
        RedTeam -->|Succès: >=2 Gains + 0 Régression| Signer[Signataire Cryptographique HMAC]
        Signer --> MeshRegistry[4. Registre Mesh & Alertes Webhook]
        RedTeam -->|Échec / Faille Sécurité| Rejected[Rejet / Quarantaine]
    end

    subgraph "Gestion du Cycle de Vie & Observabilité"
        Telemetry --> Lifecycle[5. Moniteur de Dérive & Archivage LRU]
        Telemetry --> Dashboard[Topologie Réseau Interactive Canvas]
        Lifecycle -->|Dérive Détectée| Rollback[Pause / Rollback Automatique]
        Rollback --> MeshRegistry
    end
```

---

## 📁 Structure du Dépôt

```text
.
├── clawhub.json                      # Manifeste racine du registre ClawHub
├── LICENSE                           # Licence open-source MIT
├── README.md                         # Documentation principale (English)
├── README.fr.md                      # Documentation (Français)
├── requirements.txt                  # Dépendances de développement optionnelles
├── .gitignore                        # Exclusion des caches, logs et fuites de clés
├── .github/
│   └── workflows/
│       └── clawhub-publish.yml       # Déploiement automatique sur ClawHub via GitHub Actions
├── tests/
│   └── test_factory_e2e.py           # 8/8 tests unitaires & d'intégration Pytest
└── skills/
    └── agent-factory/
        ├── SKILL.md                  # Spécification OpenClaw & ClawHub (Point d'entrée)
        ├── clawhub.json              # Manifeste du package skill
        ├── references/
        │   └── manifest_schema.json  # Schéma JSON de validation des sous-agents
        ├── dashboard/
        │   ├── app.py                # Serveur Dashboard zéro-dépendance
        │   └── static/               # Topologie Canvas & Interface Dark Glassmorphism
        └── scripts/
            ├── openclaw_hook.py      # Middleware d'interception de la passerelle OpenClaw
            ├── llm_engine.py         # Moteur d'exécution LLM réel multi-fournisseurs
            ├── embedding_engine.py   # Moteur d'embeddings denses 64d & indexeur HNSW
            ├── telemetry.py          # Moteur de télémétrie réelle & scoring de clusters
            ├── clustering_engine.py  # Clustering streaming non-supervisé
            ├── semantic_cache.py     # Cache sémantique 0-token
            ├── synthesizer.py        # Synthétiseur en sandbox & élagage d'outils
            ├── container_sandbox.py  # Sandbox d'isolation de processus & quotas
            ├── red_team_fuzzer.py    # Fuzzer adversarial & sondes d'injection
            ├── evaluator.py          # Banc d'évaluation 4D & signature cryptographique
            ├── crypto_signer.py      # Signature HMAC-SHA256 & intégrité
            ├── security_sandbox.py   # Quotas, limitation de débit & Circuit Breaker
            ├── router.py             # Routeur sémantique vectoriel & Canary
            ├── alerts.py             # Dispatcher d'alertes Webhook (Discord, Slack, HTTP)
            └── lifecycle.py          # Surveillance des dérives de prod & archivage LRU
```

---

## 🖥️ Dashboard & Topologie Réseau Canvas

Lancer le Dashboard temps réel sans dépendance externe :

```bash
python3 skills/agent-factory/dashboard/app.py
```
👉 Accédez à la cartographie interactive sur **`http://localhost:8000`**.

---

## 🧪 Tests Automatisés

```bash
python3 -m pytest -v tests/test_factory_e2e.py
```

---

## 📄 Licence

Distribué sous la licence [MIT](LICENSE).
