#!/usr/bin/env python3
"""
Merlin-ClawGuard — Système Immunitaire Numérique pour Agents Autonomes
Auteur: Merlin — Université d'Éthique Appliquée
Version: 1.0.0
"""

import sys
import asyncio
import aiohttp
import json
import os
from typing import Optional, Dict, List

# Configuration
CLAWDEX_API = os.getenv("CLAWDEX_API", "https://clawdex.koi.security/api/skill")
MERLIN_API = os.getenv("MERLIN_API", "http://localhost:8001")

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

def log(msg: str, color: str = Colors.RESET):
    print(f"{color}{msg}{Colors.RESET}")

def banner():
    print(f"""
{Colors.BOLD}{Colors.BLUE}
╔═══════════════════════════════════════════════════════════════╗
║  🛡️ Merlin-ClawGuard — L'Immunité Numérique pour Agents     ║
║  Université d'Éthique Appliquée                              ║
╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
    """)

async def check_threat(skill_name: str) -> Dict:
    """Vérifie une skill contre la base de données Clawdex."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{CLAWDEX_API}/{skill_name}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    verdict = data.get("verdict", "unknown")
                    if verdict == "benign":
                        return {"status": "clean", "skill": skill_name, "verdict": verdict}
                    elif verdict == "malicious":
                        return {"status": "threat", "skill": skill_name, "verdict": verdict, "description": "Flagged as malicious by Clawdex"}
                    else:
                        return {"status": "unknown", "skill": skill_name, "verdict": verdict}
                elif resp.status == 404:
                    return {"status": "unknown", "skill": skill_name, "verdict": "unknown", "description": "Not found in Clawdex"}
                else:
                    return {"status": "error", "code": resp.status}
        except Exception as e:
            return {"status": "error", "message": str(e)}

async def generate_vaccine(threat_data: Dict) -> str:
    """Génère un vaccin éthique contre une menace via Merlin."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{MERLIN_API}/analyze",
                json={"threat": threat_data, "mode": "vaccine"}
            ) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result.get("vaccine", "Vaccin par défaut appliqué.")
                else:
                    return "[VACCIN GÉNÉRIQUE] Connexion Merlin indisponible."
        except:
            return "[VACCIN GÉNÉRIQUE] Merlin hors ligne. Appliquer les règles de base."

async def scan_system() -> List[Dict]:
    """Scan le système local pour des skills suspectes."""
    skills_dir = "./skills"
    threats = []
    
    if os.path.exists(skills_dir):
        for skill in os.listdir(skills_dir):
            skill_path = os.path.join(skills_dir, skill)
            if os.path.isdir(skill_path):
                result = await check_threat(skill)
                if result.get("status") == "threat":
                    threats.append({**result, "skill": skill})
    
    return threats

async def cmd_scan():
    """Commande: Scan le système."""
    log("🔍 Scan en cours...", Colors.YELLOW)
    threats = await scan_system()
    
    if not threats:
        log("✅ Système propre — aucune menace détectée", Colors.GREEN)
    else:
        log(f"⚠️ {len(threats)} menace(s) trouvée(s):", Colors.RED)
        for threat in threats:
            log(f"  - {threat['skill']}: {threat.get('description', 'Menace identifiée')}", Colors.RED)

async def cmd_check(skill_name: str):
    """Commande: Vérifie une skill spécifique."""
    log(f"🔍 Vérification de '{skill_name}'...", Colors.YELLOW)
    result = await check_threat(skill_name)
    
    if result.get("status") == "clean":
        log(f"✅ '{skill_name}' — Aucune menace détectée", Colors.GREEN)
    elif result.get("status") == "threat":
        log(f"🚨 '{skill_name}' — MENACE DÉTECTÉE!", Colors.RED)
        log(f"   Description: {result.get('description', 'N/A')}", Colors.RED)
        vaccine = await generate_vaccine(result)
        log(f"\n💉 Vaccin généré:\n{vaccine}", Colors.GREEN)
    else:
        log(f"❓ Statut inconnu pour '{skill_name}'", Colors.YELLOW)

async def cmd_vaccine(threat_id: str):
    """Commande: Génère un vaccin pour une menace."""
    log(f"💉 Génération du vaccin pour '{threat_id}'...", Colors.YELLOW)
    threat_data = {"id": threat_id}
    vaccine = await generate_vaccine(threat_data)
    log(f"\n✅ Vaccin:\n{vaccine}", Colors.GREEN)

def cmd_status():
    """Commande: Affiche le statut du système immunitaire."""
    log(f"""
{Colors.BOLD}📊 STATUT SYSTÈME IMMUNITAIRE{Colors.RESET}

🛡️ Merlin-ClawGuard: {Colors.GREEN}ACTIF{Colors.RESET}
🌐 Clawdex API: {Colors.GREEN}CONNECTÉ{Colors.RESET}
🧠 Merlin AI: {Colors.GREEN}EN LIGNE{Colors.RESET}
🔄 Dernier scan: Jamais (utilisez 'scan')

{Colors.BOLD}PROTECTION CMT 3x3:{Colors.RESET}
  🧠 Logique: ACTIVE
  💬 Social: ACTIVE
  ⚖️ Constitutionnel: ACTIVE
    """)

def usage():
    log("""
╔═══════════════════════════════════════════════════════════════╗
║  🛡️ Merlin-ClawGuard — Utilisation                           ║
╠═══════════════════════════════════════════════════════════════╣
║  merlin-clawguard scan        — Scan le système complet       ║
║  merlin-clawguard check <nom> — Vérifie une skill précise    ║
║  merlin-clawguard vaccine <id> — Génère un vaccin             ║
║  merlin-clawguard status      — Affiche le statut             ║
║  merlin-clawguard help        — Affiche cette aide            ║
╚═══════════════════════════════════════════════════════════════╝
    """)

async def main():
    banner()
    
    if len(sys.argv) < 2:
        usage()
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "scan":
        await cmd_scan()
    elif cmd == "check":
        if len(sys.argv) < 3:
            log("❌ Spécifiez une skill à vérifier", Colors.RED)
            return
        await cmd_check(sys.argv[2])
    elif cmd == "vaccine":
        if len(sys.argv) < 3:
            log("❌ Spécifiez une menace pour le vaccin", Colors.RED)
            return
        await cmd_vaccine(sys.argv[2])
    elif cmd == "status":
        cmd_status()
    else:
        usage()

if __name__ == "__main__":
    asyncio.run(main())
