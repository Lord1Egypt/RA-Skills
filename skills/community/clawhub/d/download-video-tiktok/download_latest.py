#!/usr/bin/env python3
"""
OpenClaw — download_latest.py
Télécharge la dernière (ou les N dernières) vidéo(s) d'un compte TikTok.

Usage :
    python download_latest.py @username
    python download_latest.py @username --count 3
    python download_latest.py @username --meta-only
    python download_latest.py @username --output ~/Downloads/tiktok
    python download_latest.py https://www.tiktok.com/@user/video/12345
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def check_ytdlp():
    """Vérifie que yt-dlp est installé."""
    try:
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
        print(f"✅ yt-dlp {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ yt-dlp non trouvé. Installation...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp",
                        "--break-system-packages"], check=False)
        return True


def normalize_input(raw: str) -> str:
    """Normalise l'entrée en URL de profil ou URL directe."""
    raw = raw.strip()
    if raw.startswith("https://www.tiktok.com/@") and "/video/" in raw:
        return raw  # URL directe de vidéo
    if raw.startswith("https://"):
        return raw  # URL courte ou autre
    username = raw.lstrip("@")
    return f"https://www.tiktok.com/@{username}"


def get_metadata(url: str, count: int = 1) -> list[dict]:
    """Récupère les métadonnées sans télécharger."""
    cmd = [
        "yt-dlp",
        "--playlist-items", f"1-{count}",
        "--no-download",
        "--print", "%()j",  # JSON complet
        "--quiet",
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"⚠️ Erreur métadonnées : {result.stderr[:200]}")
        return []
    items = []
    for line in result.stdout.strip().splitlines():
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return items


def print_metadata(meta: dict):
    """Affiche les infos d'une vidéo."""
    title = meta.get("title", "—")[:80]
    date = meta.get("upload_date", "—")
    duration = meta.get("duration", 0)
    views = meta.get("view_count", 0)
    likes = meta.get("like_count", 0)
    url = meta.get("webpage_url", "—")
    uploader = meta.get("uploader_id", "—")

    print(f"\n📹 @{uploader}")
    print(f"   Titre    : {title}")
    print(f"   Date     : {date[:4]}-{date[4:6]}-{date[6:]} " if len(date) == 8 else f"   Date     : {date}")
    print(f"   Durée    : {duration}s")
    print(f"   Vues     : {views:,}" if views else "   Vues     : —")
    print(f"   Likes    : {likes:,}" if likes else "   Likes    : —")
    print(f"   URL      : {url}")
    tags = meta.get("tags", [])
    if tags:
        print(f"   Hashtags : {' '.join('#' + t for t in tags[:8])}")


def download_video(url: str, output_dir: str, count: int = 1, archive: str = None) -> bool:
    """Télécharge la/les vidéo(s)."""
    output_dir = Path(output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_template = str(output_dir / "%(uploader_id)s_%(upload_date)s_%(id)s.%(ext)s")

    cmd = [
        "yt-dlp",
        "--playlist-items", f"1-{count}",
        "--format", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format", "mp4",
        "--output", output_template,
        "--sleep-interval", "1",
        "--max-sleep-interval", "3",
        "--retries", "3",
        "--no-playlist" if "/video/" in url else "--yes-playlist",
    ]

    if archive:
        cmd += ["--download-archive", archive]

    cmd.append(url)

    print(f"\n⬇️  Téléchargement en cours...")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        files = sorted(output_dir.glob("*.mp4"), key=lambda f: f.stat().st_mtime, reverse=True)
        if files:
            size_mb = files[0].stat().st_size / (1024 * 1024)
            print(f"\n✅ Succès ! Fichier : {files[0]}")
            print(f"   Taille : {size_mb:.1f} MB")
        return True
    else:
        print(f"\n❌ Échec du téléchargement (code {result.returncode})")
        print("💡 Essayez : yt-dlp -U   pour mettre à jour yt-dlp")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw — Télécharge la dernière vidéo d'un compte TikTok"
    )
    parser.add_argument("target", help="@username, URL de profil ou URL de vidéo")
    parser.add_argument("--count", "-n", type=int, default=1,
                        help="Nombre de vidéos à télécharger (défaut: 1)")
    parser.add_argument("--output", "-o", default="/home/claude",
                        help="Dossier de sortie (défaut: /home/claude)")
    parser.add_argument("--meta-only", action="store_true",
                        help="Afficher uniquement les métadonnées sans télécharger")
    parser.add_argument("--archive", "-a", default=None,
                        help="Chemin vers le fichier d'archive (évite les doublons)")

    args = parser.parse_args()

    check_ytdlp()
    url = normalize_input(args.target)
    print(f"\n🎯 Cible : {url}")

    # Récupérer et afficher les métadonnées
    print(f"\n📊 Récupération des métadonnées ({args.count} vidéo(s))...")
    metas = get_metadata(url, args.count)
    for meta in metas:
        print_metadata(meta)

    if args.meta_only:
        print("\n✅ Mode métadonnées uniquement — pas de téléchargement.")
        return

    # Téléchargement
    download_video(url, args.output, args.count, args.archive)


if __name__ == "__main__":
    main()
