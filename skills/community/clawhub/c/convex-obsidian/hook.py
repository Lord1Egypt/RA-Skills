#!/usr/bin/env python3
"""
OpenClaw Memory Hook - Integração automática Convex + Obsidian
Salva conversas automaticamente e busca contexto quando relevante.
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

CONVEX_URL = os.getenv("CONVEX_DEPLOYMENT_URL", "https://energized-goshawk-977.convex.cloud")
VAULT_PATH = os.getenv("VAULT_PATH", "/home/andrey/Vault")

def convex_query(action: str, args: Dict) -> Any:
    """Query Convex via HTTP."""
    try:
        resp = requests.post(
            f"{CONVEX_URL}/api/query",
            json={"path": action, "args": args},
            timeout=10
        )
        return resp.json().get("value") if resp.status_code == 200 else None
    except:
        return None

def convex_mutation(action: str, args: Dict) -> Any:
    """Mutation Convex via HTTP."""
    try:
        resp = requests.post(
            f"{CONVEX_URL}/api/mutation",
            json={"path": action, "args": args},
            timeout=10
        )
        return resp.json().get("value") if resp.status_code == 200 else None
    except:
        return None

def save_conversation_turn(
    session_id: str,
    user_message: str,
    ai_response: str,
    tags: List[str] = None,
    importance: int = 5
) -> bool:
    """Salva um turno de conversa no Convex."""
    content = f"User: {user_message}\nAI: {ai_response[:500]}"
    
    result = convex_mutation("memory:saveMemory", {
        "sessionId": session_id,
        "content": content,
        "source": "conversation",
        "tags": tags or ["auto-saved"],
        "importance": importance,
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "has_response": len(ai_response) > 0
        }
    })
    
    return result is not None

def get_relevant_context(query: str, session_id: str = None, limit: int = 5) -> str:
    """Busca contexto relevante das memórias."""
    # Busca no Convex
    convex_results = convex_query("memory:searchMemories", {
        "query": query,
        "limit": limit,
        **({"sessionId": session_id} if session_id else {})
    }) or []
    
    # Busca no Obsidian (simple text search)
    vault = Path(VAULT_PATH)
    obsidian_results = []
    
    if vault.exists():
        query_terms = query.lower().split()
        for md_file in vault.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8').lower()
                score = sum(content.count(term) for term in query_terms)
                if score > 0:
                    obsidian_results.append({
                        "file": md_file.name,
                        "preview": md_file.read_text(encoding='utf-8')[:300]
                    })
            except:
                pass
        obsidian_results = sorted(obsidian_results, 
            key=lambda x: sum(x["preview"].lower().count(t) for t in query_terms), 
            reverse=True)[:3]
    
    # Formata contexto
    context_parts = []
    
    if convex_results:
        context_parts.append("## Memórias Recentes (Convex):")
        for r in convex_results[:3]:
            context_parts.append(f"- {r.get('content', '')[:200]}...")
    
    if obsidian_results:
        context_parts.append("\n## Conhecimento do Vault (Obsidian):")
        for r in obsidian_results[:2]:
            context_parts.append(f"- [{r['file']}]: {r['preview'][:150]}...")
    
    return "\n".join(context_parts) if context_parts else ""

def should_search_memory(message: str) -> bool:
    """Detecta se a mensagem sugere busca de memória."""
    triggers = [
        "lembr", "antes", "ontem", "outro dia", "da última vez",
        "já falamos", "como eu te disse", "você mencionou",
        "o que aconteceu", "quando foi", "aquele projeto",
        "lembra quando", "a gente conversou"
    ]
    msg_lower = message.lower()
    return any(t in msg_lower for t in triggers)

def auto_save_and_context(session_id: str, user_msg: str, ai_msg: str) -> Optional[str]:
    """
    Função principal chamada automaticamente após cada turno.
    Retorna contexto relevante se detectar necessidade.
    """
    # Sempre salva no Convex
    save_conversation_turn(session_id, user_msg, ai_msg)
    
    # Se parece que precisa de contexto, busca
    if should_search_memory(user_msg):
        context = get_relevant_context(user_msg, session_id)
        if context:
            return f"\n\n[Contexto de memórias anteriores]:\n{context}"
    
    return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--ai", required=True)
    parser.add_argument("--check-context", action="store_true")
    
    args = parser.parse_args()
    
    result = auto_save_and_context(args.session, args.user, args.ai)
    
    if args.check_context and result:
        print(result)
    else:
        print("Saved" if result is not None else "Error")
