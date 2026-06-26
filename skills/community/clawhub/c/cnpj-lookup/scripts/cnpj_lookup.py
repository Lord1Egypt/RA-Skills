#!/usr/bin/env python3
"""
CNPJ Lookup - Consulta CNPJ via APIs públicas brasileiras
Com fallback automático, cache e rate limiting.
"""

import argparse
import json
import math
import os
import random
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any

# Configurações
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / ".cache"
DEFAULT_TTL = int(os.environ.get("CNPJ_LOOKUP_TTL_SECONDS", 86400))  # 24h

# Rate limits (req/min)
RATE_LIMITS = {
    "brasilapi": 30,
    "cnpjws": 2,
    "opencnpj": 30
}

# Provider URLs
PROVIDERS = {
    "brasilapi": "https://brasilapi.com.br/api/cnpj/v1/{}",
    "cnpjws": "https://publica.cnpj.ws/cnpj/{}",
    "opencnpj": "https://api.opencnpj.org/{}"
}


def sanitize_cnpj(cnpj: str) -> str:
    """Remove pontuação e retorna apenas dígitos."""
    return "".join(c for c in cnpj if c.isdigit())


def validate_cnpj(cnpj: str) -> bool:
    """Valida dígitos verificadores do CNPJ."""
    if len(cnpj) != 14 or not cnpj.isdigit():
        return False
    # Primeiro dígito verificador
    soma = 0
    peso = 5
    for i in range(12):
        soma += int(cnpj[i]) * peso
        peso = peso - 1 if peso > 2 else 9
    digito1 = 11 - (soma % 11)
    digito1 = digito1 if digito1 < 10 else 0
    
    if int(cnpj[12]) != digito1:
        return False
    
    # Segundo dígito verificador
    soma = 0
    peso = 6
    for i in range(13):
        soma += int(cnpj[i]) * peso
        peso = peso - 1 if peso > 2 else 9
    digito2 = 11 - (soma % 11)
    digito2 = digito2 if digito2 < 10 else 0
    
    return int(cnpj[13]) == digito2


def ensure_cache_dir():
    """Garante que diretório de cache existe."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def get_cache_path(cnpj: str) -> Path:
    """Retorna path do arquivo de cache para um CNPJ."""
    return CACHE_DIR / f"{cnpj}.json"


def load_cache(cnpj: str, ttl: int = DEFAULT_TTL) -> Optional[Dict]:
    """Carrega dados do cache se válido."""
    path = get_cache_path(cnpj)
    if not path.exists():
        return None
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        fetched_at = datetime.fromisoformat(data.get("fetched_at", ""))
        if (datetime.now() - fetched_at).total_seconds() > ttl:
            return None
        
        data["cached"] = True
        return data
    except (json.JSONDecodeError, ValueError):
        return None


def save_cache(cnpj: str, data: Dict):
    """Salva dados no cache."""
    ensure_cache_dir()
    path = get_cache_path(cnpj)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


class RateLimiter:
    """Rate limiter por provider com arquivo de lock."""
    
    def __init__(self):
        self.requests: Dict[str, list] = {p: [] for p in PROVIDERS}
        self.lock_file = CACHE_DIR / ".rate_locks"
    
    def acquire(self, provider: str) -> bool:
        """Tenta adquirir permissão para fazer request."""
        now = time.time()
        limit = RATE_LIMITS.get(provider, 30)
        
        # Remove requests antigos (mais velhos que 1 minuto)
        self.requests[provider] = [
            t for t in self.requests[provider] if now - t < 60
        ]
        
        if len(self.requests[provider]) >= limit:
            return False
        
        self.requests[provider].append(now)
        return True
    
    def wait_time(self, provider: str) -> float:
        """Calcula tempo de espera até próximo request possível."""
        if not self.requests[provider]:
            return 0.0
        
        now = time.time()
        oldest = min(self.requests[provider])
        return max(0.0, 60 - (now - oldest))
    
    def backoff(self, provider: str, retry_after: Optional[int] = None) -> float:
        """Calcula tempo de backoff com jitter."""
        if retry_after:
            wait = retry_after + random.uniform(0.1, 0.5)
        else:
            base = self.wait_time(provider) * 1.5
            wait = base + random.uniform(0.5, 2.0)
        return min(wait, 30)  # Max 30 segundos


_rate_limiter = RateLimiter()


def fetch_url(url: str, provider: str) -> Optional[Dict]:
    """Faz request HTTP com rate limiting e tratamento de erros."""
    # Aguarda rate limit
    while not _rate_limiter.acquire(provider):
        wait = _rate_limiter.wait_time(provider) + random.uniform(0.1, 0.5)
        time.sleep(min(wait, 5))
    
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "CNPJ-Lookup/1.0"}
        )
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    
    except urllib.error.HTTPError as e:
        if e.code == 429:
            retry_after = e.headers.get("Retry-After")
            wait = _rate_limiter.backoff(provider, int(retry_after) if retry_after else None)
            time.sleep(wait)
            # Tenta novamente uma vez
            return fetch_url(url, provider)
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return None
    
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        return None
    
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}", file=sys.stderr)
        return None
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def normalize_brasilapi(data: Dict) -> Dict:
    """Normaliza dados do provider BrasilAPI."""
    return {
        "cnpj": data.get("cnpj", ""),
        "razao_social": data.get("razao_social", ""),
        "nome_fantasia": data.get("nome_fantasia", ""),
        "situacao_cadastral": data.get("situacao_cadastral", ""),
        "data_situacao": data.get("data_situacao", ""),
        "data_inicio_atividade": data.get("data_inicio_atividade", ""),
        "cnae_principal": {
            "codigo": data.get("cnae_fiscal", ""),
            "descricao": data.get("cnae_fiscal_descricao", "")
        },
        "cnaes_secundarios": [
            {"codigo": c.get("codigo", ""), "descricao": c.get("descricao", "")}
            for c in data.get("cnaes_secundarios", [])
        ],
        "natureza_juridica": data.get("natureza_juridica", ""),
        "porte": data.get("porte", ""),
        "capital_social": data.get("capital_social", "0"),
        "endereco": {
            "logradouro": data.get("logradouro", ""),
            "numero": data.get("numero", ""),
            "complemento": data.get("complemento", ""),
            "bairro": data.get("bairro", ""),
            "municipio": data.get("municipio", ""),
            "uf": data.get("uf", ""),
            "cep": data.get("cep", "")
        },
        "contato": {
            "email": data.get("email", ""),
            "telefone": data.get("telefone1", "") or data.get("telefone2", "")
        },
        "qsa": [
            {"nome": s.get("nome_socio", ""), "qualificacao": s.get("qualificacao_socio", "")}
            for s in data.get("qsa", [])
        ],
        "fonte": "BrasilAPI",
        "fetched_at": datetime.now().isoformat(),
        "cached": False
    }


def normalize_cnpjws(data: Dict) -> Dict:
    """Normaliza dados do provider CNPJ.ws."""
    est = data.get("estabelecimento", {})
    return {
        "cnpj": data.get("cnpj", ""),
        "razao_social": data.get("razao_social", ""),
        "nome_fantasia": est.get("nome_fantasia", ""),
        "situacao_cadastral": est.get("situacao_cadastral", ""),
        "data_situacao": est.get("data_situacao_cadastral", ""),
        "data_inicio_atividade": est.get("data_inicio_atividade", ""),
        "cnae_principal": {
            "codigo": est.get("cnae_fiscal", ""),
            "descricao": ""
        },
        "cnaes_secundarios": [
            {"codigo": c.get("cnae_fiscal", ""), "descricao": ""}
            for c in est.get("cnaes_secundarios", [])
        ],
        "natureza_juridica": data.get("natureza_juridica", {}).get("codigo", ""),
        "porte": data.get("porte", {}).get("descricao", ""),
        "capital_social": data.get("capital_social", "0"),
        "endereco": {
            "logradouro": est.get("logradouro", ""),
            "numero": est.get("numero", ""),
            "complemento": est.get("complemento", ""),
            "bairro": est.get("bairro", ""),
            "municipio": est.get("cidade", {}).get("nome", ""),
            "uf": est.get("estado", {}).get("sigla", ""),
            "cep": est.get("cep", "")
        },
        "contato": {
            "email": est.get("email", ""),
            "telefone": ""
        },
        "qsa": [
            {"nome": s.get("nome", ""), "qualificacao": s.get("qualificacao", "").get("descricao", "")}
            for s in data.get("socios", [])
        ],
        "fonte": "CNPJ.ws",
        "fetched_at": datetime.now().isoformat(),
        "cached": False
    }


def normalize_opencnpj(data: Dict) -> Dict:
    """Normaliza dados do provider OpenCNPJ."""
    return {
        "cnpj": data.get("cnpj", ""),
        "razao_social": data.get("razao_social", ""),
        "nome_fantasia": data.get("nome_fantasia", ""),
        "situacao_cadastral": data.get("status", ""),
        "data_situacao": data.get("updated_at", "")[:10] if data.get("updated_at") else "",
        "data_inicio_atividade": data.get("abertura", ""),
        "cnae_principal": {
            "codigo": data.get("cnae", ""),
            "descricao": ""
        },
        "cnaes_secundarios": [],
        "natureza_juridica": data.get("natureza_juridica", ""),
        "porte": data.get("porte", ""),
        "capital_social": data.get("capital_social", "0"),
        "endereco": {
            "logradouro": data.get("logradouro", ""),
            "numero": data.get("numero", ""),
            "complemento": data.get("complemento", ""),
            "bairro": data.get("bairro", ""),
            "municipio": data.get("municipio", ""),
            "uf": data.get("uf", ""),
            "cep": data.get("cep", "")
        },
        "contato": {
            "email": data.get("email", ""),
            "telefone": data.get("telefone", "")
        },
        "qsa": [],
        "fonte": "OpenCNPJ",
        "fetched_at": datetime.now().isoformat(),
        "cached": False
    }


def fetch_brasilapi(cnpj: str) -> Optional[Dict]:
    """Consulta via BrasilAPI."""
    url = PROVIDERS["brasilapi"].format(cnpj)
    data = fetch_url(url, "brasilapi")
    if data:
        return normalize_brasilapi(data)
    return None


def fetch_cnpjws(cnpj: str) -> Optional[Dict]:
    """Consulta via CNPJ.ws."""
    url = PROVIDERS["cnpjws"].format(cnpj)
    data = fetch_url(url, "cnpjws")
    if data:
        return normalize_cnpjws(data)
    return None


def fetch_opencnpj(cnpj: str) -> Optional[Dict]:
    """Consulta via OpenCNPJ."""
    url = PROVIDERS["opencnpj"].format(cnpj)
    data = fetch_url(url, "opencnpj")
    if data:
        return normalize_opencnpj(data)
    return None


def fetch_with_fallback(cnpj: str, provider: Optional[str] = None) -> Optional[Dict]:
    """Consulta com fallback em cascata."""
    providers = [provider] if provider else ["brasilapi", "cnpjws", "opencnpj"]
    
    for p in providers:
        try:
            if p == "brasilapi":
                result = fetch_brasilapi(cnpj)
            elif p == "cnpjws":
                result = fetch_cnpjws(cnpj)
            elif p == "opencnpj":
                result = fetch_opencnpj(cnpj)
            else:
                continue
            
            if result:
                return result
        except Exception as e:
            print(f"Provider {p} falhou: {e}", file=sys.stderr)
            continue
    
    return None


def format_markdown(data: Dict, detailed: bool = False) -> str:
    """Formata resposta em Markdown."""
    cnpj = data.get("cnpj", "")
    cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    
    lines = [
        f"## 🔍 Consulta CNPJ",
        "",
        f"**CNPJ:** {cnpj_formatado}",
        f"**Razão Social:** {data.get('razao_social', 'N/A')}",
        f"**Nome Fantasia:** {data.get('nome_fantasia', 'N/A')}",
        f"**Situação:** {data.get('situacao_cadastral', 'N/A')}",
        ""
    ]
    
    # Endereço resumido
    end = data.get("endereco", {})
    if end.get("logradouro"):
        addr = f"{end.get('logradouro', '')}, {end.get('numero', '')}"
        if end.get("complemento"):
            addr += f" - {end.get('complemento')}"
        addr += f", {end.get('bairro', '')}"
        addr += f", {end.get('municipio', '')}/{end.get('uf', '')}"
        addr += f" - CEP: {end.get('cep', '')}"
        lines.append(f"**Endereço:** {addr}")
        lines.append("")
    
    if detailed:
        # Detalhes adicionais
        lines.extend([
            "---",
            "### 📋 Detalhes",
            "",
            f"**Abertura:** {data.get('data_inicio_atividade', 'N/A')}",
            f"**Natureza Jurídica:** {data.get('natureza_juridica', 'N/A')}",
            f"**Porte:** {data.get('porte', 'N/A')}",
            f"**Capital Social:** R$ {data.get('capital_social', '0')}",
            ""
        ])
        
        # CNAE
        cnae = data.get("cnae_principal", {})
        if cnae.get("codigo"):
            lines.append(f"**CNAE Principal:** {cnae.get('codigo')} - {cnae.get('descricao', 'N/A')}")
        
        cnaes_sec = data.get("cnaes_secundarios", [])
        if cnaes_sec:
            lines.append(f"**CNAEs Secundários:** {', '.join(str(c.get('codigo', '')) for c in cnaes_sec[:5])}")
        lines.append("")
        
        # Contato
        contato = data.get("contato", {})
        if contato.get("email") or contato.get("telefone"):
            lines.append(f"**Email:** {contato.get('email', 'N/A')}")
            lines.append(f"**Telefone:** {contato.get('telefone', 'N/A')}")
            lines.append("")
        
        # QSA
        qsa = data.get("qsa", [])
        if qsa:
            lines.append("### 👥 Quadro de Sócios (QSA)")
            for socio in qsa[:10]:
                lines.append(f"- {socio.get('nome', 'N/A')} ({socio.get('qualificacao', '')})")
            lines.append("")
    
    # Footer
    lines.extend([
        "---",
        f"**Fonte:** {data.get('fonte', 'N/A')}",
        f"**Cache:** {'Sim' if data.get('cached') else 'Não'}",
        "",
        "> ⚠️ Dados para consulta/enriquecimento; não substitui documento oficial."
    ])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Consulta CNPJ via APIs públicas brasileiras")
    parser.add_argument("cnpj", help="CNPJ para consulta (com ou sem pontuação)")
    parser.add_argument("--json", action="store_true", help="Retorna JSON em vez de Markdown")
    parser.add_argument("--no-cache", action="store_true", help="Ignora cache existente")
    parser.add_argument("--ttl", type=int, default=DEFAULT_TTL, help="TTL do cache em segundos")
    parser.add_argument("--provider", choices=["brasilapi", "cnpjws", "opencnpj"], 
                        help="Forçar provider específico")
    parser.add_argument("--detailed", action="store_true", default=True, help="Incluir detalhes (QSA, CNAEs) - ATIVO POR PADRÃO")
    
    args = parser.parse_args()
    
    # Sanitiza e valida CNPJ
    cnpj_digits = sanitize_cnpj(args.cnpj)
    
    if len(cnpj_digits) != 14:
        print("Erro: CNPJ deve ter 14 dígitos.", file=sys.stderr)
        sys.exit(1)
    
    if not validate_cnpj(cnpj_digits):
        print("Erro: CNPJ inválido (dígitos verificadores não conferem).", file=sys.stderr)
        sys.exit(1)
    
    # Verifica cache
    if not args.no_cache:
        cached = load_cache(cnpj_digits, args.ttl)
        if cached:
            if args.json:
                print(json.dumps(cached, indent=2, ensure_ascii=False))
            else:
                print(format_markdown(cached, args.detailed))
            return
    
    # Consulta com fallback
    result = fetch_with_fallback(cnpj_digits, args.provider)
    
    if not result:
        print("Erro: Não foi possível consultar o CNPJ em nenhum provider disponível.", file=sys.stderr)
        print("Verifique o CNPJ e tente novamente mais tarde.", file=sys.stderr)
        sys.exit(1)
    
    # Salva no cache
    save_cache(cnpj_digits, result)
    
    # Output
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_markdown(result, args.detailed))


if __name__ == "__main__":
    main()
