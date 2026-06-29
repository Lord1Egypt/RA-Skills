"""
🛠️ axiom-hash-multi — Multi-Algorithm Hash Generator v1.1.0
=============================================================

CHANGELOG v1.1.0 :
- 🐛 FIX: accepte /dev/null et autres character devices (path.is_file() retournait False)
- ✨ NEW: --compare=<expected_hash> (vérifier un hash sans regarder l'output)
- ✨ NEW: --verify-manifest <file> (vérifier tous les hashes d'un MANIFEST)
- ✨ NEW: --json (output structuré pour scripting)

CALCUL HASH MULTI-ALGORITHMES — DÉTERMINISTE, BYTE-TO-BYTE, ZERO DÉPENDANCE

Usage CLI:
    python3 axiom_hash_multi.py <file-or-string> [--algo sha256]
    cat file.txt | python3 axiom_hash_multi.py --stdin
    python3 axiom_hash_multi.py "hello world"
    python3 axiom_hash_multi.py file.txt --compare=<expected-sha256>
    python3 axiom_hash_multi.py --verify-manifest MANIFEST.txt

Usage Python:
    from axiom_hash_multi import hash_bytes, hash_file, hash_all, verify_file
    digest = hash_bytes(b"hello", algo="sha256")
    is_valid = verify_file("file.txt", expected_hash, algo="sha256")
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, Union

# Algorithmes supportés (pure stdlib hashlib)
SUPPORTED_ALGORITHMS = ("md5", "sha1", "sha256", "sha512", "blake2b")

# Tailles de bloc pour lecture par chunks (perf sans charger en RAM)
DEFAULT_CHUNK_SIZE = 65536  # 64 KB


def hash_bytes(data: bytes, algo: str = "sha256") -> str:
    """
    Calcule le hash hex d'un bytes input.

    Args:
        data: les bytes à hasher
        algo: algorithme (md5, sha1, sha256, sha512, blake2b)

    Returns:
        hash hex string (lowercase)

    Raises:
        ValueError: si algo non supporté
        TypeError: si data n'est pas bytes
    """
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Algorithme '{algo}' non supporté. "
            f"Supportés : {SUPPORTED_ALGORITHMS}"
        )
    if not isinstance(data, bytes):
        raise TypeError(
            f"data doit être bytes, reçu {type(data).__name__}"
        )

    h = hashlib.new(algo)
    h.update(data)
    return h.hexdigest()


def hash_file(
    filepath: Union[str, Path],
    algo: str = "sha256",
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> str:
    """
    Calcule le hash hex d'un fichier, en streaming (pas de chargement en RAM).

    Accepte fichiers réguliers, character devices (/dev/null, /dev/urandom), 
    symlinks, pipes — tout ce qui est lisible.

    Args:
        filepath: chemin du fichier
        algo: algorithme (md5, sha1, sha256, sha512, blake2b)
        chunk_size: taille des chunks de lecture (défaut 64KB)

    Returns:
        hash hex string (lowercase)

    Raises:
        FileNotFoundError: si le fichier n'existe pas
        PermissionError: si pas de permission lecture
        IsADirectoryError: si input est un dossier
        ValueError: si algo non supporté
    """
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Algorithme '{algo}' non supporté. "
            f"Supportés : {SUPPORTED_ALGORITHMS}"
        )

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")
    # FIX v1.1.0: utiliser is_dir() au lieu de is_file() pour exclure
    # uniquement les dossiers, pas les character devices (/dev/null, etc.)
    if path.is_dir():
        raise IsADirectoryError(f"Est un dossier, pas un fichier : {filepath}")

    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def hash_all(data: bytes) -> Dict[str, str]:
    """
    Calcule TOUS les algorithmes d'un coup.

    Args:
        data: les bytes à hasher

    Returns:
        dict {algo: hex_digest} pour les 5 algos
    """
    return {algo: hash_bytes(data, algo) for algo in SUPPORTED_ALGORITHMS}


def hash_file_all(
    filepath: Union[str, Path],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> Dict[str, str]:
    """
    Calcule TOUS les algorithmes d'un fichier, en UNE passe (efficient).

    Args:
        filepath: chemin du fichier
        chunk_size: taille des chunks (défaut 64KB)

    Returns:
        dict {algo: hex_digest} pour les 5 algos
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {filepath}")
    if path.is_dir():
        raise IsADirectoryError(f"Est un dossier : {filepath}")

    hashers = {algo: hashlib.new(algo) for algo in SUPPORTED_ALGORITHMS}
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            for h in hashers.values():
                h.update(chunk)

    return {algo: h.hexdigest() for algo, h in hashers.items()}


def verify_file(
    filepath: Union[str, Path],
    expected_hash: str,
    algo: str = "sha256",
) -> bool:
    """
    Vérifie qu'un fichier a bien le hash attendu.

    Args:
        filepath: chemin du fichier
        expected_hash: hash hex attendu (case-insensitive)
        algo: algorithme utilisé

    Returns:
        True si le hash match, False sinon
    """
    actual = hash_file(filepath, algo=algo)
    return actual.lower() == expected_hash.lower()


def parse_manifest(manifest_path: Union[str, Path]) -> list:
    """
    Parse un fichier MANIFEST au format :
        <hash>  <filename>  [(<size> bytes)]
    Une ligne par entrée. Lignes vides et commentaires (#) ignorés.

    Returns:
        list of dicts: [{"hash": "...", "filename": "..."}, ...]
    """
    path = Path(manifest_path)
    if not path.exists():
        raise FileNotFoundError(f"Manifest introuvable : {manifest_path}")

    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Format: <hash>  <filename>  [(<size> bytes)]
        parts = line.split()
        if len(parts) < 2:
            continue
        h, fname = parts[0], parts[1]
        entries.append({"hash": h, "filename": fname, "raw": line})
    return entries


def verify_manifest(
    manifest_path: Union[str, Path],
    base_dir: Union[str, Path] = None,
    algo: str = None,
) -> Dict:
    """
    Vérifie tous les fichiers d'un MANIFEST.

    Le MANIFEST peut être :
    - Hash seul par ligne (algo = mandatory)
    - Hash + filename (algo = detected from hash length, ou spécifié)

    Format du MANIFEST :
        <hash>  <filename>
        <hash>  <filename>  (<size> bytes)
    Ou auto-détection de l'algo par longueur du hash :
        32 chars  = MD5
        40 chars  = SHA-1
        64 chars  = SHA-256
        128 chars = SHA-512 ou BLAKE2b (ambigu, à spécifier)

    Returns:
        dict {"total": N, "passed": M, "failed": K, "details": [...]}
    """
    entries = parse_manifest(manifest_path)
    base = Path(base_dir) if base_dir else Path(manifest_path).parent

    # Auto-detect algo if not specified
    results = []
    passed = 0
    failed = 0
    for entry in entries:
        h = entry["hash"]
        fname = entry["filename"]
        # Detect algo by hash length
        if algo:
            entry_algo = algo
        else:
            l = len(h)
            if l == 32:
                entry_algo = "md5"
            elif l == 40:
                entry_algo = "sha1"
            elif l == 64:
                entry_algo = "sha256"
            elif l == 128:
                entry_algo = "sha512"  # assume SHA-512 (BLAKE2b is rare)
            else:
                results.append({
                    "file": fname, "passed": False,
                    "error": f"unknown hash length: {l}"
                })
                failed += 1
                continue

        filepath = base / fname
        if not filepath.exists():
            results.append({
                "file": fname, "passed": False,
                "error": "file not found"
            })
            failed += 1
            continue

        try:
            actual = hash_file(filepath, entry_algo)
            ok = actual.lower() == h.lower()
            results.append({
                "file": fname, "algo": entry_algo,
                "expected": h, "actual": actual,
                "passed": ok
            })
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            results.append({
                "file": fname, "passed": False,
                "error": str(e)
            })
            failed += 1

    return {
        "total": len(entries),
        "passed": passed,
        "failed": failed,
        "details": results
    }


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="axiom-hash-multi — Hash multi-algorithmes déterministe v1.1.0"
    )
    parser.add_argument(
        "input",
        nargs="?",
        help="Fichier ou string à hasher (utilise --stdin si absent)"
    )
    parser.add_argument(
        "--algo",
        choices=SUPPORTED_ALGORITHMS,
        default="sha256",
        help="Algorithme (défaut: sha256)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Affiche les 5 algorithmes (md5, sha1, sha256, sha512, blake2b)"
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Lit depuis stdin"
    )
    parser.add_argument(
        "--string",
        action="store_true",
        help="Traite l'input comme string (pas fichier)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output en format JSON"
    )
    parser.add_argument(
        "--compare",
        metavar="EXPECTED_HASH",
        help="Compare le hash calculé à un hash attendu. Exit 0 si match, 1 si mismatch."
    )
    parser.add_argument(
        "--verify-manifest",
        metavar="MANIFEST_FILE",
        help="Vérifie tous les hashes d'un fichier MANIFEST. Format: '<hash>  <filename>'"
    )

    args = parser.parse_args()

    try:
        # Mode --verify-manifest
        if args.verify_manifest:
            result = verify_manifest(args.verify_manifest)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"Manifest: {args.verify_manifest}")
                print(f"Total: {result['total']}  Pass: {result['passed']}  Fail: {result['failed']}")
                for d in result["details"]:
                    icon = "✅" if d.get("passed") else "❌"
                    err = d.get("error", "")
                    print(f"  {icon} {d['file']}  ({d.get('algo', '?')})  {err}")
            return 0 if result["failed"] == 0 else 1

        # Détermine les données
        if args.stdin or args.input is None:
            data = sys.stdin.buffer.read()
            mode = "stdin"
        elif args.string:
            data = args.input.encode("utf-8")
            mode = "string"
        else:
            # Traite comme fichier
            if args.all:
                results = hash_file_all(args.input)
            else:
                digest = hash_file(args.input, args.algo)
                results = {args.algo: digest}

            # Output
            if args.compare:
                expected = args.compare.lower()
                if args.all:
                    # Si --all, on compare tous les algos
                    matches = {algo: (h.lower() == expected) for algo, h in results.items()}
                    if args.json:
                        print(json.dumps({"matches": matches, "expected": expected}, indent=2))
                    else:
                        for algo, ok in matches.items():
                            icon = "✅" if ok else "❌"
                            print(f"  {icon} {algo}: {results[algo]}")
                        print(f"Expected: {expected}")
                else:
                    ok = results[args.algo].lower() == expected
                    if args.json:
                        print(json.dumps({
                            "match": ok,
                            "expected": expected,
                            "actual": results[args.algo],
                            "algo": args.algo
                        }, indent=2))
                    else:
                        if ok:
                            print(f"✅ MATCH ({args.algo})")
                        else:
                            print(f"❌ MISMATCH ({args.algo})")
                            print(f"  Expected: {expected}")
                            print(f"  Actual:   {results[args.algo]}")
                return 0 if ok else 1

            if args.json:
                print(json.dumps(results, indent=2))
            elif args.all:
                for algo, digest in results.items():
                    print(f"{algo}  {digest}")
            else:
                print(results[args.algo])
            return 0

        # data = bytes (stdin ou string)
        if args.all:
            results = hash_all(data)
        else:
            results = {args.algo: hash_bytes(data, args.algo)}

        # Output
        if args.compare:
            expected = args.compare.lower()
            matches = {algo: (h.lower() == expected) for algo, h in results.items()}
            if args.json:
                print(json.dumps({"matches": matches, "expected": expected}, indent=2))
            else:
                for algo, ok in matches.items():
                    icon = "✅" if ok else "❌"
                    print(f"  {icon} {algo}: {results[algo]}")
                print(f"Expected: {expected}")
            return 0 if any(matches.values()) else 1

        if args.json:
            print(json.dumps(results, indent=2))
        elif args.all:
            for algo, digest in results.items():
                print(f"{algo}  {digest}")
        else:
            print(results[args.algo])
        return 0

    except FileNotFoundError as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1
    except (ValueError, TypeError, IsADirectoryError) as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
