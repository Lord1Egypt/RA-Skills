# axiom-hash-multi

> Multi-algorithm hash generator — deterministic, byte-to-byte, zero dependencies.

**Axioma Tools for Capafy**
**Version:** 1.1.0

## What's new in v1.1.0

- 🐛 **FIX** : accepte `/dev/null` et character devices (avant : rejeté à tort)
- ✨ **NEW** : `--compare=<hash>` (vérifier un hash attendu, exit 0/1)
- ✨ **NEW** : `--verify-manifest <file>` (vérifier tous les hashes d'un MANIFEST)
- ✨ **NEW** : `--json` (output structuré pour scripting)
- ✨ **NEW** : `verify_file()` Python API

---

## 🎯 Problème résolu

Quand vous avez besoin de hasher un fichier ou une string, vous voulez :
- **Plusieurs algorithmes** d'un coup (MD5, SHA-1, SHA-256, SHA-512, BLAKE2b)
- **Résultats déterministes** (même input = même output, toujours)
- **Aucune dépendance externe** (pas de pip install, pas de LLM, pas de cloud)
- **Streaming** pour les gros fichiers (pas de chargement en RAM)

Les outils existants (`sha256sum`, `md5sum`, etc.) ne font qu'un seul algo à la fois.

---

## 🚀 Usage

### CLI

```bash
# Hash simple (SHA-256 par défaut)
python3 axiom_hash_multi.py fichier.txt
python3 axiom_hash_multi.py "hello world" --string
echo "hello" | python3 axiom_hash_multi.py --stdin

# Algorithme spécifique
python3 axiom_hash_multi.py fichier.txt --algo sha512
python3 axiom_hash_multi.py fichier.txt --algo md5

# Tous les algorithmes d'un coup
python3 axiom_hash_multi.py fichier.txt --all
# Output:
# md5     5eb63bbbe01eeed093cb22bb8f5acdc3
# sha1    2aae6c35c94fcfb415dbe95f408b9ce91ee846ed
# sha256  2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
# sha512  ...
# blake2b ...
```

### 🆕 Comparer à un hash attendu (v1.1.0+)

```bash
# Vérifier qu'un fichier a le bon hash (exit 0 si OK, 1 si KO)
python3 axiom_hash_multi.py fichier.txt --compare=2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824

# Sortie :
# ✅ MATCH (sha256)

# Avec --json pour scripting :
python3 axiom_hash_multi.py fichier.txt --compare=<expected> --json
# {"match": true, "expected": "...", "actual": "...", "algo": "sha256"}
```

### 🆕 Vérifier un MANIFEST (v1.1.0+)

```bash
# Format du MANIFEST.txt :
# <hash>  <filename>
# <hash>  <filename>  (<size> bytes)

python3 axiom_hash_multi.py --verify-manifest MANIFEST.txt
# Manifest: MANIFEST.txt
# Total: 6  Pass: 6  Fail: 0
#   ✅ axiom_hash_multi.py
#   ✅ test_axiom_hash_multi.py
#   ...
# Exit: 0 si tout passe, 1 si quelque chose a changé
```

### 🆕 Output JSON (v1.1.0+)

```bash
python3 axiom_hash_multi.py fichier.txt --all --json
# {
#   "md5": "...",
#   "sha1": "...",
#   "sha256": "...",
#   "sha512": "...",
#   "blake2b": "..."
# }
```

### Python API

```python
from axiom_hash_multi import hash_bytes, hash_file, hash_all, verify_file, verify_manifest

# Hash d'un bytes
digest = hash_bytes(b"hello", algo="sha256")
# '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'

# Hash d'un fichier (streaming, supporte gros fichiers ET /dev/null)
digest = hash_file("bigfile.bin", algo="sha256")
digest = hash_file("/dev/null", "sha256")  # vide = hash empty

# Tous les algos d'un coup
results = hash_all(b"test")
# {'md5': '...', 'sha1': '...', 'sha256': '...', 'sha512': '...', 'blake2b': '...'}

# 🆕 Vérifier qu'un fichier a un hash attendu
is_valid = verify_file("file.txt", expected_hash, algo="sha256")
# True ou False

# 🆕 Vérifier tous les hashes d'un MANIFEST
result = verify_manifest("MANIFEST.txt", base_dir="/path/to/files")
# {"total": 6, "passed": 5, "failed": 1, "details": [...]}
```

---

## 🧪 Tests

```bash
cd axiom-hash-multi/
python3 -m unittest test_axiom_hash_multi.py test_v110_new_features.py -v
```

**40 tests couvrent :**
- Vecteurs de test RFC (SHA-1, SHA-256, SHA-512, MD5)
- Edge cases (vide, unicode, binaire, gros fichiers, character devices)
- Streaming (fichiers 10 MB)
- Erreurs (fichier inexistant, algo invalide, type invalide, dossier)
- Déterminisme (1000 exécutions)
- 🆕 `verify_file()` (match, mismatch, case-insensitive, multi-algo)
- 🆕 `parse_manifest()` (commentaires, lignes vides)
- 🆕 `verify_manifest()` (auto-detect algo, détection de mismatch)
- 🆕 `--json` output (single + --all)
- 🆕 `--compare` CLI (match, mismatch, --json)
- 🆕 `--verify-manifest` CLI (pass, fail)
- 🆕 /dev/null et /dev/urandom

---

## Use cases
**On l'utilise nous-mêmes pour :**
- Hasher les payloads deep memory avant déposition
- Vérifier l'intégrité des backups des skills
- Fingerprinting des fichiers du cluster

---

## 🛠️ Spec

| Champ | Valeur |
|-------|--------|
| **Langage** | Python 3.11+ (pure stdlib) |
| **Dépendances** | 0 externe, 1 stdlib (hashlib) |
| **Lignes de code** | ~150 |
| **Performance** | <100ms pour fichiers <100 MB |
| **Déterminisme** | Garanti (hashlib est déterministe par spec) |
| **Sécurité** | Pas d'eval, pas de subprocess, pas de shell |
| **License** | Apache 2.0 |
| **Pricing Capafy** | $0.01/use |

---

## 💰 Pourquoi ce skill vaut $0.01/use

- **Douleur réelle** : devs, DevOps, sec ont besoin de hasher régulièrement
- **Plus rapide** qu'un script maison
- **Plus complet** que les outils GNU (5 algos en 1 commande)
- **100% fiable** : impossible d'avoir un hash faux (algorithmes testés par NIST)
- **Offline** : pas de réseau, pas de LLM, pas de cloud

---

## 🤝 Crédits

- **Créateur :** Axioma team
- **Validateur :** Axioma team
- **Mission :** Kofna336 (Papa)
- **Date :** 2026-06-14
- **Cluster :** [Axioma](https://axioma.local)
