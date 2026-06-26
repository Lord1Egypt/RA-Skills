#!/usr/bin/env python3
"""
camara.py - CLI para a API de Dados Abertos da Câmara dos Deputados
Uso: python3 camara.py <comando> [opções]

Comandos:
  agenda [data]           Agenda do dia (default: hoje). Data: YYYY-MM-DD
  deputado <nome>         Busca deputado por nome
  deputado-id <id>        Perfil completo de um deputado
  ocupacoes <id>          Histórico de ocupações/profissões de um deputado
  proposicao <id>         Detalhes de uma proposição
  relacionadas <id>       Proposições relacionadas a uma proposição
  buscar-pl <keywords>    Busca proposições por palavras-chave
  votacoes [data]         Votações no plenário (default: hoje)
  votos <votacao_id>      Votos individuais de uma votação
  comissao <sigla>        Busca comissão por sigla
  blocos                  Lista blocos parlamentares
  frentes [legislatura]   Lista frentes parlamentares (default: legislatura 57)
  frente <id>             Detalhes e membros de uma frente parlamentar
  partido <id>            Detalhes e membros de um partido
  mesa [legislatura]      Mesa diretora (default: legislatura 57)
  referencias <tipo>      Dados de referência (situacao-dep, situacao-prop,
                          tipo-prop, temas, tipos-evento, tipos-orgao, uf)
"""

import sys
import json
import urllib.request
import urllib.parse
from datetime import date

BASE = "https://dadosabertos.camara.leg.br/api/v2"

def get(path, params=None):
    url = f"{BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    with urllib.request.urlopen(url, timeout=15) as r:
        return json.loads(r.read())

def fmt(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def agenda(data=None):
    d = data or date.today().isoformat()
    r = get("/eventos", {"dataInicio": d, "dataFim": d, "ordem": "ASC", "ordenarPor": "dataHoraInicio", "itens": 50})
    eventos = r.get("dados", [])
    if not eventos:
        print(f"Sem eventos para {d}.")
        return
    print(f"\n📅 Agenda da Câmara — {d}\n{'='*50}")
    for e in eventos:
        hora = e.get("dataHoraInicio", "")[-5:] if e.get("dataHoraInicio") else "?"
        orgaos = ", ".join(o.get("sigla","") for o in e.get("orgaos",[]))
        local = e.get("localCamara", {}).get("nome") or e.get("localExterno") or ""
        print(f"  {hora} | {orgaos:10} | {e.get('descricaoTipo',''):30} | {e.get('descricao','')[:60]}")
        if local:
            print(f"         Local: {local}")
    print()

def buscar_deputado(nome):
    r = get("/deputados", {"nome": nome, "idLegislatura": 57, "ordem": "ASC", "ordenarPor": "nome"})
    deps = r.get("dados", [])
    if not deps:
        print(f"Nenhum deputado encontrado para '{nome}'.")
        return
    print(f"\n👤 Deputados — '{nome}'\n{'='*50}")
    for d in deps:
        print(f"  ID {d['id']} | {d['nome']:40} | {d['siglaPartido']:12} | {d['siglaUf']}")
    print()

def deputado_id(dep_id):
    r = get(f"/deputados/{dep_id}")
    d = r.get("dados", {})
    nome = d.get("nomeCivil", d.get("ultimoStatus", {}).get("nome", ""))
    status = d.get("ultimoStatus", {})
    print(f"\n👤 {nome}")
    print(f"  Partido: {status.get('siglaPartido')} | UF: {status.get('siglaUf')}")
    print(f"  Situação: {status.get('situacao')}")
    print(f"  Gabinete: {status.get('gabinete', {}).get('nome')} sala {status.get('gabinete', {}).get('sala')}")
    print(f"  Email: {status.get('email')}")
    print(f"  URL foto: {status.get('urlFoto')}")
    print()

def proposicao(prop_id):
    r = get(f"/proposicoes/{prop_id}")
    p = r.get("dados", {})
    print(f"\n📄 {p.get('siglaTipo')} {p.get('numero')}/{p.get('ano')}")
    print(f"  Ementa: {p.get('ementa')}")
    print(f"  Apresentação: {p.get('dataApresentacao')}")
    print(f"  Status: {p.get('statusProposicao', {}).get('descricaoSituacao')}")
    print(f"  Órgão atual: {p.get('statusProposicao', {}).get('siglaOrgao')}")
    print(f"  Relator: {p.get('statusProposicao', {}).get('uriRelator')}")
    # tramitação
    tr = get(f"/proposicoes/{prop_id}/tramitacoes")
    trams = tr.get("dados", [])[-5:]
    if trams:
        print(f"\n  📋 Últimas 5 tramitações:")
        for t in trams:
            print(f"    {t.get('dataHora','')[:10]} | {t.get('siglaOrgao',''):8} | {t.get('descricaoSituacao','')[:50]}")
    print()

def buscar_pl(keywords, tipo="PL", ano=None):
    params = {"keywords": keywords, "siglaTipo": tipo, "ordem": "DESC", "ordenarPor": "id", "itens": 15}
    if ano:
        params["ano"] = ano
    r = get("/proposicoes", params)
    pls = r.get("dados", [])
    if not pls:
        print(f"Nenhuma proposição encontrada para '{keywords}'.")
        return
    print(f"\n📑 Proposições — '{keywords}'\n{'='*50}")
    for p in pls:
        print(f"  ID {p['id']} | {p['siglaTipo']} {p['numero']}/{p['ano']} | {p.get('dataApresentacao','')[:10]} | {p['ementa'][:70]}")
    print()

def votacoes(data=None):
    d = data or date.today().isoformat()
    r = get("/votacoes", {"dataInicio": d, "dataFim": d, "idOrgao": 180, "ordem": "DESC", "ordenarPor": "dataHoraRegistro", "itens": 20})
    vots = r.get("dados", [])
    if not vots:
        print(f"Sem votações no plenário em {d}.")
        return
    print(f"\n🗳️  Votações — Plenário — {d}\n{'='*50}")
    for v in vots:
        ap = "✅ APROVADA" if v.get("aprovacao") == 1 else "❌ REJEITADA" if v.get("aprovacao") == 0 else "⏳"
        print(f"  {v['id']} | {ap} | {v.get('descricao','')[:70]}")
    print()

def votos(votacao_id):
    r = get(f"/votacoes/{votacao_id}/votos")
    votos_list = r.get("dados", [])
    print(f"\n🗳️  Votos na votação {votacao_id}\n{'='*50}")
    contagem = {}
    for v in votos_list:
        voto = v.get("tipoVoto", "?")
        contagem[voto] = contagem.get(voto, 0) + 1
    for tipo, qtd in sorted(contagem.items(), key=lambda x: -x[1]):
        print(f"  {tipo:10}: {qtd}")
    print(f"  Total: {len(votos_list)}")
    print()

def comissao(sigla):
    r = get("/orgaos", {"sigla": sigla})
    orgs = r.get("dados", [])
    if not orgs:
        print(f"Comissão '{sigla}' não encontrada.")
        return
    org = orgs[0]
    print(f"\n🏛️  {org.get('nome')} ({org.get('sigla')})")
    print(f"  ID: {org['id']} | Tipo: {org.get('tipoOrgao')}")
    # Membros
    try:
        mr = get(f"/orgaos/{org['id']}/membros")
        membros = mr.get("dados", [])
        print(f"  Membros: {len(membros)}")
        for m in membros[:5]:
            print(f"    {m.get('nome',''):40} | {m.get('siglaPartido',''):8} | {m.get('titulo','')}")
        if len(membros) > 5:
            print(f"    ... e mais {len(membros)-5}")
    except Exception:
        pass
    print()

def ocupacoes(dep_id):
    r = get(f"/deputados/{dep_id}/ocupacoes")
    ocups = r.get("dados", [])
    if not ocups:
        print(f"Sem ocupações registradas para deputado {dep_id}.")
        return
    print(f"\n💼 Ocupações — Deputado {dep_id}\n{'='*50}")
    for o in ocups:
        periodo = f"{o.get('anoInicio', '?')}-{o.get('anoFim', 'atual')}"
        print(f"  {periodo:12} | {o.get('titulo', ''):30} | {o.get('entidade', '')}")
    print()

def relacionadas(prop_id):
    r = get(f"/proposicoes/{prop_id}/relacionadas")
    rels = r.get("dados", [])
    if not rels:
        print(f"Sem proposições relacionadas para {prop_id}.")
        return
    print(f"\n🔗 Proposições Relacionadas — {prop_id}\n{'='*50}")
    for p in rels:
        print(f"  ID {p.get('id','')} | {p.get('siglaTipo','')} {p.get('numero','')}/{p.get('ano','')} | {p.get('ementa','')[:60]}")
    print()

def blocos():
    r = get("/blocos")
    blocs = r.get("dados", [])
    if not blocs:
        print("Nenhum bloco parlamentar encontrado.")
        return
    print(f"\n🏛️  Blocos Parlamentares\n{'='*50}")
    for b in blocs:
        print(f"  ID {b.get('id','')} | {b.get('nome',''):50} | Leg. {b.get('idLegislatura','')}")
    print()

def frentes(legislatura=None):
    params = {"itens": 50}
    if legislatura:
        params["idLegislatura"] = legislatura
    else:
        params["idLegislatura"] = 57
    r = get("/frentes", params)
    frs = r.get("dados", [])
    if not frs:
        print("Nenhuma frente parlamentar encontrada.")
        return
    print(f"\n🤝 Frentes Parlamentares\n{'='*50}")
    for f in frs:
        print(f"  ID {f.get('id','')} | {f.get('titulo','')[:70]}")
    print(f"  Total: {len(frs)}")
    print()

def frente(id_frente):
    r = get(f"/frentes/{id_frente}")
    f = r.get("dados", {})
    print(f"\n🤝 {f.get('titulo', '')}")
    print(f"  ID: {id_frente}")
    print(f"  Coordenador: {f.get('coordenador', {}).get('nome', '?')}")
    # Membros
    try:
        mr = get(f"/frentes/{id_frente}/membros")
        membros = mr.get("dados", [])
        print(f"  Membros: {len(membros)}")
        for m in membros[:10]:
            print(f"    {m.get('nome',''):40} | {m.get('siglaPartido',''):8} | {m.get('titulo','')}")
        if len(membros) > 10:
            print(f"    ... e mais {len(membros)-10}")
    except Exception:
        pass
    print()

def partido(id_partido):
    r = get(f"/partidos/{id_partido}")
    p = r.get("dados", {})
    status = p.get("status", {})
    print(f"\n🏛️  {p.get('nome', '')} ({status.get('sigla', '')})")
    print(f"  ID: {id_partido}")
    print(f"  Líder: {status.get('lider', {}).get('nome', '?')}")
    print(f"  Total membros: {status.get('totalMembros', '?')}")
    # Membros
    try:
        mr = get(f"/partidos/{id_partido}/membros", {"itens": 50})
        membros = mr.get("dados", [])
        print(f"\n  Deputados ({len(membros)}):")
        for m in membros[:10]:
            print(f"    {m.get('nome',''):40} | {m.get('siglaUf','')}")
        if len(membros) > 10:
            print(f"    ... e mais {len(membros)-10}")
    except Exception:
        pass
    print()

def mesa(legislatura=None):
    leg = legislatura or "57"
    r = get(f"/legislaturas/{leg}/mesa")
    membros = r.get("dados", [])
    if not membros:
        print(f"Sem dados da mesa para legislatura {leg}.")
        return
    print(f"\n🏛️  Mesa Diretora — Legislatura {leg}\n{'='*50}")
    for m in membros:
        print(f"  {m.get('titulo',''):30} | {m.get('nome',''):30} | {m.get('siglaPartido',''):8} | {m.get('siglaUf','')}")
    print()

def referencias(tipo):
    REF_MAP = {
        "situacao-dep": "/referencias/deputados/codSituacao",
        "situacao-prop": "/referencias/proposicoes/codSituacaoProposicao",
        "tipo-prop": "/referencias/proposicoes/siglaTipo",
        "temas": "/referencias/proposicoes/tema",
        "tipos-evento": "/referencias/tiposEvento",
        "tipos-orgao": "/referencias/tiposOrgao",
        "uf": "/referencias/uf",
    }
    if not tipo or tipo not in REF_MAP:
        print(f"Tipos disponíveis: {', '.join(REF_MAP.keys())}")
        return
    r = get(REF_MAP[tipo])
    dados = r.get("dados", [])
    if not dados:
        print(f"Sem dados para '{tipo}'.")
        return
    print(f"\n📋 Referências — {tipo}\n{'='*50}")
    for item in dados:
        # Formatar de forma genérica
        parts = [str(v) for v in item.values()]
        print(f"  {' | '.join(parts)}")
    print(f"  Total: {len(dados)}")
    print()

COMMANDS = {
    "agenda": lambda args: agenda(args[0] if args else None),
    "deputado": lambda args: buscar_deputado(" ".join(args)),
    "deputado-id": lambda args: deputado_id(args[0]),
    "ocupacoes": lambda args: ocupacoes(args[0]),
    "proposicao": lambda args: proposicao(args[0]),
    "relacionadas": lambda args: relacionadas(args[0]),
    "buscar-pl": lambda args: buscar_pl(" ".join(args)),
    "votacoes": lambda args: votacoes(args[0] if args else None),
    "votos": lambda args: votos(args[0]),
    "comissao": lambda args: comissao(args[0]),
    "blocos": lambda args: blocos(),
    "frentes": lambda args: frentes(args[0] if args else None),
    "frente": lambda args: frente(args[0]),
    "partido": lambda args: partido(args[0]),
    "mesa": lambda args: mesa(args[0] if args else None),
    "referencias": lambda args: referencias(args[0] if args else None),
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    try:
        COMMANDS[cmd](args)
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
