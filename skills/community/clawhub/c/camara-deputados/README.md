# Câmara dos Deputados - Cliente Python

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Cliente Python assíncrono para a [API de Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br).

## 📋 Características

- ✅ Cliente assíncrono com `httpx`
- ✅ Tratamento robusto de erros com retry automático
- ✅ Logging estruturado
- ✅ Type hints completos
- ✅ Paginação automática
- ✅ Sem necessidade de autenticação
- ✅ Suporte a todas as principais funcionalidades da API v2

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/olegantonov/camara-deputados.git
cd camara-deputados

# Instale as dependências
pip install -r requirements.txt

# Para desenvolvimento
pip install -r requirements-dev.txt
```

## 📖 Uso Básico

### Buscar Deputados

```python
import asyncio
from camara_client import get_camara_client

async def main():
    client = get_camara_client()
    try:
        # Listar todos os deputados (legislatura 57)
        deputados = await client.lista_deputados()
        
        # Buscar por nome
        resultado = await client.buscar_deputado_por_nome("Lula")
        
        for dep in resultado:
            print(f"{dep['nome']} ({dep['siglaPartido']}-{dep['siglaUf']})")
            
        # Detalhes de um deputado
        detalhe = await client.get_deputado_detalhe(dep['id'])
        print(f"Email: {detalhe['ultimoStatus']['email']}")
    finally:
        await client.close()

asyncio.run(main())
```

### Pesquisar Proposições

```python
# Buscar PLs de 2026 com palavras-chave
proposicoes = await client.pesquisar_proposicoes(
    keywords="transporte público",
    sigla_tipo="PL",
    ano=2026,
    tramitando=True
)

for prop in proposicoes:
    print(f"{prop['siglaTipo']} {prop['numero']}/{prop['ano']}")
    print(f"Ementa: {prop['ementa']}")
```

### Eventos e Agenda

```python
from datetime import date, timedelta

# Eventos de hoje
eventos = await client.get_eventos_dia()

# Próximos 7 dias
eventos_semana = await client.get_eventos_periodo(
    date.today(),
    date.today() + timedelta(days=7)
)

for evento in eventos_semana:
    print(f"{evento['dataHoraInicio']}: {evento['descricaoTipo']}")
    print(f"Local: {evento['localExterno']['nome']}")
```

### Votações

```python
from datetime import date, timedelta

# Votações da última semana
votacoes = await client.get_votacoes_periodo(
    date.today() - timedelta(days=7),
    date.today(),
    id_orgao=180  # 180 = Plenário
)

for votacao in votacoes:
    print(f"{votacao['data']}: {votacao['descricao']}")
    
# Votos individuais
votos = await client.get_votos_votacao(votacao['id'])
for voto in votos:
    print(f"{voto['deputado_']['nome']}: {voto['tipoVoto']}")
```

### Despesas Parlamentares (CEAP)

```python
# Despesas de um deputado em 2026
despesas = await client.get_despesas_deputado(
    id_deputado=204554,
    ano=2026
)

total = sum(float(d['valorDocumento']) for d in despesas)
print(f"Total gasto: R$ {total:,.2f}")

# Agrupar por tipo
from collections import Counter
tipos = Counter(d['tipoDespesa'] for d in despesas)
for tipo, count in tipos.most_common(5):
    print(f"{tipo}: {count} despesas")
```

### Tramitação de Proposição

```python
# Histórico completo de tramitação
tramitacoes = await client.get_proposicao_tramitacao(id_proposicao=2366661)

for tram in tramitacoes:
    print(f"{tram['dataHora']}: {tram['descricaoTramitacao']}")
    print(f"Situação: {tram['descricaoSituacao']}")
```

## 🔧 Funcionalidades Principais

### Deputados
- `lista_deputados(legislatura)` - Lista de deputados
- `buscar_deputado_por_nome(nome)` - Busca por nome
- `get_deputado_detalhe(id)` - Perfil completo
- `get_despesas_deputado(id, ano)` - CEAP/despesas
- `get_discursos_deputado(id)` - Discursos
- `get_frentes_deputado(id)` - Frentes parlamentares
- `get_deputado_orgaos(id)` - Comissões do deputado
- `get_deputado_ocupacoes(id)` - Histórico profissional

### Proposições
- `pesquisar_proposicoes(keywords, tipo, ano, tema, tramitacao_senado)` - Busca de bills
- `get_proposicao_detalhe(id)` - Detalhes completos
- `get_proposicao_tramitacao(id)` - Histórico de tramitação
- `get_proposicao_votacoes(id)` - Votações da proposição
- `get_proposicao_autores(id)` - Autores
- `get_proposicao_temas(id)` - Temas/tags
- `get_proposicao_relacionadas(id)` - Proposições relacionadas

### Eventos
- `get_eventos_dia(data)` - Agenda do dia
- `get_eventos_periodo(inicio, fim)` - Eventos em período
- `get_evento_detalhe(id)` - Detalhes do evento
- `get_evento_deputados(id)` - Deputados no evento
- `get_evento_orgaos(id)` - Órgãos organizadores
- `get_evento_votacoes(id)` - Votações do evento

### Votações
- `get_votacoes_periodo(inicio, fim, orgao)` - Votações em período
- `get_votacao_detalhe(id)` - Detalhes da votação
- `get_votos_votacao(id)` - Votos individuais por deputado
- `get_orientacoes_votacao(id)` - Orientações de bancada

### Órgãos/Comissões
- `lista_orgaos()` - Lista de comissões e órgãos
- `get_orgao_detalhe(id)` - Detalhes do órgão
- `get_eventos_orgao_periodo(id, inicio, fim)` - Agenda da comissão
- `get_membros_orgao(id)` - Membros atuais
- `get_votacoes_orgao(id, inicio, fim)` - Votações da comissão

### Legislaturas
- `lista_legislaturas()` - Lista de legislaturas
- `get_legislatura_detalhe(id)` - Detalhes da legislatura
- `get_legislatura_mesa(id)` - Mesa diretora

### Partidos
- `lista_partidos()` - Lista de partidos
- `get_partido_detalhe(id)` - Detalhes do partido
- `get_partido_membros(id)` - Deputados do partido

### Blocos Parlamentares
- `lista_blocos()` - Lista de blocos
- `get_bloco_detalhe(id)` - Detalhes do bloco

### Frentes Parlamentares
- `lista_frentes(legislatura)` - Lista de frentes
- `get_frente_detalhe(id)` - Detalhes da frente
- `get_frente_membros(id)` - Membros da frente

### Referências
- `get_referencias_situacao_deputado()` - Códigos de situação
- `get_referencias_situacao_proposicao()` - Status de proposições
- `get_referencias_tipo_proposicao()` - Tipos (PL, PEC, etc)
- `get_referencias_temas()` - Temas/assuntos
- `get_referencias_tipos_evento()` - Tipos de evento
- `get_referencias_tipos_orgao()` - Tipos de órgão
- `get_referencias_uf()` - Unidades federativas

## ⚠️ Tratamento de Erros

O cliente possui exceções específicas:

```python
from camara_client import (
    CamaraAPIError,         # Erro genérico
    CamaraTimeoutError,     # Timeout
    CamaraNotFoundError,    # 404
    CamaraConnectionError,  # Erro de conexão
    CamaraValidationError   # Validação de parâmetros
)

try:
    deputados = await client.lista_deputados()
except CamaraTimeoutError:
    print("A API está demorando para responder")
except CamaraNotFoundError:
    print("Recurso não encontrado")
except CamaraAPIError as e:
    print(f"Erro na API: {e}")
```

## 📝 Logging

Para habilitar logs:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🔗 Recursos

- [Documentação da API](https://dadosabertos.camara.leg.br)
- [Swagger UI](https://dadosabertos.camara.leg.br/swagger/api.html)
- [SKILL.md](SKILL.md) - Referência completa de endpoints
- [Portal de Dados Abertos](https://www2.camara.leg.br/transparencia/dados-abertos)

## 🧪 Testes

```bash
# Executar testes
pytest

# Com coverage
pytest --cov=camara_client --cov-report=html

# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integration/
```

## 💡 Exemplos Avançados

### Análise de Gastos por Partido

```python
from collections import defaultdict

deputados = await client.lista_deputados()
gastos_partido = defaultdict(float)

for dep in deputados[:10]:  # Top 10 para exemplo
    despesas = await client.get_despesas_deputado(dep['id'], ano=2026)
    total = sum(float(d['valorDocumento']) for d in despesas)
    gastos_partido[dep['siglaPartido']] += total

for partido, total in sorted(gastos_partido.items(), key=lambda x: x[1], reverse=True):
    print(f"{partido}: R$ {total:,.2f}")
```

### Monitor de Votações em Tempo Real

```python
import asyncio
from datetime import date

async def monitor_votacoes():
    client = get_camara_client()
    try:
        while True:
            votacoes = await client.get_votacoes_periodo(
                date.today(),
                date.today(),
                id_orgao=180  # Plenário
            )
            
            print(f"Votações hoje: {len(votacoes)}")
            for v in votacoes[-5:]:  # Últimas 5
                print(f"  - {v['dataHoraRegistro']}: {v['descricao']}")
            
            await asyncio.sleep(300)  # Check a cada 5 minutos
    finally:
        await client.close()

asyncio.run(monitor_votacoes())
```

### Blocos e Frentes Parlamentares

```python
# Listar blocos parlamentares
blocos = await client.lista_blocos()
for bloco in blocos:
    print(f"{bloco['id']}: {bloco['nome']}")

# Frentes parlamentares da legislatura atual
frentes = await client.lista_frentes(id_legislatura=57)
for frente in frentes[:10]:
    print(f"{frente['titulo']}")

# Membros de uma frente
membros = await client.get_frente_membros(frente['id'])
for m in membros:
    print(f"  {m['nome']} ({m.get('titulo', 'membro')})")
```

### Mesa Diretora

```python
# Mesa da legislatura atual
mesa = await client.get_legislatura_mesa(57)
for membro in mesa:
    print(f"{membro['titulo']}: {membro['nome']} ({membro['siglaPartido']}-{membro['siglaUf']})")
```

### Dados de Referência

```python
# Listar todos os temas disponíveis para filtro
temas = await client.get_referencias_temas()
for tema in temas:
    print(f"  {tema['cod']}: {tema['nome']}")

# Listar UFs
ufs = await client.get_referencias_uf()
```

### Proposições em Tramitação no Senado

```python
# Buscar projetos originados na Câmara que estão no Senado
no_senado = await client.pesquisar_proposicoes(
    sigla_tipo="PL",
    tramitacao_senado=True
)
for prop in no_senado:
    print(f"PL {prop['numero']}/{prop['ano']}: {prop['ementa'][:60]}")
```

## 📄 Licença

MIT License

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 👨💻 Autor

Daniel Marques - [@olegantonov](https://github.com/olegantonov)

## 🙏 Agradecimentos

- Câmara dos Deputados pela disponibilização da API de Dados Abertos
- Comunidade Python Brasil
