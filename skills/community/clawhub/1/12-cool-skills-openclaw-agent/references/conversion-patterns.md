# Modèles de Conversion de Code

Ce document répertorie les modèles courants et les pièges lors de la conversion de code entre différents langages de programmation.

## Python vers Go

| Concept | Python | Go |
| :--- | :--- | :--- |
| **Typage** | Dynamique | Statique |
| **Gestion d'erreurs** | `try...except` | `if err != nil` |
| **Concurrence** | `threading`, `asyncio` | `goroutines`, `channels` |
| **Structures** | `dict`, `class` | `struct`, `map` |
| **Dépendances** | `pip`, `requirements.txt` | `go mod` |

### Pièges courants (Python → Go)
- **Gestion explicite des erreurs** : Go exige que chaque erreur soit vérifiée. Ne pas ignorer les retours d'erreur.
- **Pointeurs** : Go utilise des pointeurs pour la mutabilité.
- **Interfaces** : Go utilise des interfaces implicites.

## JavaScript/TypeScript vers Rust

| Concept | JS/TS | Rust |
| :--- | :--- | :--- |
| **Mémoire** | Garbage Collector | Ownership & Borrowing |
| **Asynchrone** | `async/await` (Promise) | `async/await` (Future) |
| **Paquets** | `npm`, `package.json` | `cargo`, `Cargo.toml` |

### Pièges courants (JS → Rust)
- **Borrow Checker** : Le concept le plus difficile pour les développeurs JS.
- **Types stricts** : Rust est beaucoup plus strict que TypeScript.

## Java vers Python

| Concept | Java | Python |
| :--- | :--- | :--- |
| **Verbosité** | Élevée | Faible |
| **Compilation** | Bytecode (JVM) | Interprété |
| **Portée** | Accolades `{}` | Indentation |

### Pièges courants (Java → Python)
- **Performance** : Python est généralement plus lent pour les tâches intensives en CPU.
- **Typage dynamique** : Attention aux erreurs de type à l'exécution.
