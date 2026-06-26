"""
Cliente async para API de Dados Abertos da Câmara dos Deputados.
Base: https://dadosabertos.camara.leg.br/api/v2

Uso:
    from camara_client import get_camara_client
    
    async def main():
        client = get_camara_client()
        try:
            # Listar deputados
            deps = await client.lista_deputados()
            
            # Pesquisar proposições
            props = await client.pesquisar_proposicoes(
                keywords="transporte",
                ano=2026
            )
            
            # Eventos de hoje
            from datetime import date, timedelta
            eventos = await client.get_eventos_periodo(
                date.today(),
                date.today() + timedelta(days=7)
            )
        finally:
            await client.close()
"""
import asyncio
import logging
from datetime import date, timedelta
from typing import Any

import httpx


# Configurar logger
logger = logging.getLogger(__name__)


# Exceções customizadas
class CamaraAPIError(Exception):
    """Erro base para erros da API da Câmara."""
    pass


class CamaraConnectionError(CamaraAPIError):
    """Erro de conexão com a API."""
    pass


class CamaraTimeoutError(CamaraAPIError):
    """Timeout ao conectar com a API."""
    pass


class CamaraNotFoundError(CamaraAPIError):
    """Recurso não encontrado."""
    pass


class CamaraValidationError(CamaraAPIError):
    """Erro de validação de parâmetros."""
    pass


BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"

# Timeout padrão para requisições (45s)
DEFAULT_TIMEOUT = 45.0


class CamaraClient:
    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        self.client: httpx.AsyncClient | None = None
        self.timeout = timeout

    async def _get_client(self) -> httpx.AsyncClient:
        if self.client is None or self.client.is_closed:
            self.client = httpx.AsyncClient(
                base_url=BASE_URL,
                timeout=httpx.Timeout(self.timeout),
                follow_redirects=True
            )
        return self.client

    async def close(self):
        if self.client and not self.client.is_closed:
            await self.client.aclose()

    async def _get(self, path: str, params: dict | None = None, retries: int = 3) -> dict:
        """
        Executa GET com retry logic e tratamento de erros.
        
        Args:
            path: Caminho do endpoint
            params: Parâmetros da query
            retries: Número de tentativas em caso de falha
            
        Raises:
            CamaraTimeoutError: Timeout na requisição
            CamaraNotFoundError: Recurso não encontrado (404)
            CamaraConnectionError: Erro de conexão
            CamaraAPIError: Outros erros da API
        """
        client = await self._get_client()
        last_error = None
        
        for attempt in range(retries):
            try:
                logger.debug(f"Requisição para {path}, tentativa {attempt + 1}/{retries}")
                response = await client.get(path, params=params)
                response.raise_for_status()
                data = response.json()
                # API v2 retorna { dados: [...] }
                return data.get("dados", data)
                
            except httpx.TimeoutException as e:
                last_error = CamaraTimeoutError(f"Timeout ao acessar {path}: {e}")
                logger.warning(f"Timeout na tentativa {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Backoff exponencial
                    
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise CamaraNotFoundError(f"Recurso não encontrado: {path}")
                last_error = CamaraAPIError(f"Erro HTTP {e.response.status_code}: {e}")
                if e.response.status_code >= 500:
                    logger.warning(f"Erro {e.response.status_code} na tentativa {attempt + 1}/{retries}")
                    if attempt < retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                logger.error(f"Erro HTTP: {e}")
                break
                
            except httpx.ConnectError as e:
                last_error = CamaraConnectionError(f"Erro de conexão: {e}")
                logger.warning(f"Erro de conexão na tentativa {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    
            except Exception as e:
                last_error = CamaraAPIError(f"Erro inesperado: {e}")
                logger.error(f"Erro inesperado: {e}")
                break
        
        if last_error:
            raise last_error
        
        raise CamaraAPIError("Falha após todas as tentativas")

    async def _get_raw(self, path: str, params: dict | None = None, retries: int = 3) -> dict:
        """GET com retry que retorna o JSON completo (sem extrair 'dados')."""
        client = await self._get_client()
        last_error = None

        for attempt in range(retries):
            try:
                logger.debug(f"Requisição raw para {path}, tentativa {attempt + 1}/{retries}")
                response = await client.get(path, params=params)
                response.raise_for_status()
                return response.json()

            except httpx.TimeoutException as e:
                last_error = CamaraTimeoutError(f"Timeout ao acessar {path}: {e}")
                logger.warning(f"Timeout na tentativa {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise CamaraNotFoundError(f"Recurso não encontrado: {path}")
                last_error = CamaraAPIError(f"Erro HTTP {e.response.status_code}: {e}")
                if e.response.status_code >= 500:
                    logger.warning(f"Erro {e.response.status_code} na tentativa {attempt + 1}/{retries}")
                    if attempt < retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                logger.error(f"Erro HTTP: {e}")
                break

            except httpx.ConnectError as e:
                last_error = CamaraConnectionError(f"Erro de conexão: {e}")
                logger.warning(f"Erro de conexão na tentativa {attempt + 1}/{retries}")
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)

            except Exception as e:
                last_error = CamaraAPIError(f"Erro inesperado: {e}")
                logger.error(f"Erro inesperado: {e}")
                break

        if last_error:
            raise last_error
        raise CamaraAPIError("Falha após todas as tentativas")

    async def _get_list(self, path: str, params: dict | None = None, max_pages: int = 50) -> list:
        """Retorna lista de resultados com paginação automática e retry.

        Args:
            max_pages: limite de páginas para evitar loops infinitos (default 50).
        """
        params = params or {}
        params.setdefault("itens", 100)

        results = []
        pagina = 1
        while pagina <= max_pages:
            params["pagina"] = pagina
            data = await self._get_raw(path, params)
            dados = data.get("dados", [])
            if not dados:
                break
            results.extend(dados)
            if len(dados) < params["itens"]:
                break
            pagina += 1
        return results

    # ========== DEPUTADOS ==========

    async def lista_deputados(self, legislatura: int | None = None) -> list[dict]:
        """Lista de deputados. Default: legislatura atual (57ª, 2023-2027)."""
        params: dict[str, Any] = {}
        if legislatura is not None:
            params["idLegislatura"] = str(legislatura)
        return await self._get_list("/deputados", params)

    async def buscar_deputado_por_nome(self, nome: str, legislatura: int | None = None) -> list[dict]:
        """Busca deputados pelo nome (contém)."""
        params: dict[str, Any] = {"nome": nome, "itens": 10}
        if legislatura is not None:
            params["idLegislatura"] = str(legislatura)
        return await self._get_list("/deputados", params)

    async def get_deputado_detalhe(self, id_deputado: str | int) -> dict:
        """Detalhe de um deputado pelo ID."""
        return await self._get(f"/deputados/{id_deputado}")

    async def get_despesas_deputado(self, id_deputado: str | int, ano: int | None = None) -> list[dict]:
        """Despesas de um deputado (CEAP)."""
        params: dict[str, Any] = {"ordem": "ASC", "ordenarPor": "ano"}
        if ano:
            params["ano"] = str(ano)
        return await self._get_list(f"/deputados/{id_deputado}/despesas", params)

    async def get_frentes_deputado(self, id_deputado: str | int) -> list[dict]:
        """Frentes parlamentares que o deputado participa."""
        return await self._get_list(f"/deputados/{id_deputado}/frentes")

    async def get_discursos_deputado(self, id_deputado: str | int, data_inicio: date | None = None, data_fim: date | None = None) -> list[dict]:
        """Discursos de um deputado."""
        params = {}
        if data_inicio:
            params["dataIni"] = data_inicio.isoformat()
        if data_fim:
            params["dataFim"] = data_fim.isoformat()
        return await self._get_list(f"/deputados/{id_deputado}/discursos", params)

    async def get_presenca_deputado(self, id_deputado: str | int, data_inicio: date, data_fim: date) -> dict:
        """Presença em sessões."""
        return await self._get(f"/deputados/{id_deputado}/presenca", {
            "dataIni": data_inicio.isoformat(),
            "dataFim": data_fim.isoformat()
        })

    # ========== PROPOSIÇÕES ==========

    async def pesquisar_proposicoes(
        self,
        keywords: str | None = None,
        sigla_tipo: str | None = None,
        numero: str | None = None,
        ano: int | None = None,
        autor: str | None = None,
        tramitando: bool = False,
        tema: int | None = None,
        tramitacao_senado: bool = False,
    ) -> list[dict]:
        """Pesquisa proposições."""
        params: dict[str, Any] = {
            "ordem": "DESC",
            "ordenarPor": "id",
            "itens": 20
        }
        if keywords:
            params["keywords"] = keywords
        if sigla_tipo:
            params["siglaTipo"] = sigla_tipo
        if numero:
            params["numero"] = str(numero)
        if ano:
            params["ano"] = str(ano)
        if autor:
            params["autor"] = autor
        if tramitando:
            # Código 903 = "Aguardando Deliberação" (em tramitação)
            params["codSituacao"] = "903"
        if tema:
            params["tema"] = str(tema)
        if tramitacao_senado:
            params["tramitacaoSenado"] = "true"

        return await self._get_list("/proposicoes", params)

    async def get_proposicao_detalhe(self, id_proposicao: str | int) -> dict:
        """Detalhe de uma proposição."""
        return await self._get(f"/proposicoes/{id_proposicao}")

    async def get_proposicao_tramitacao(self, id_proposicao: str | int) -> list[dict]:
        """Tramitações de uma proposição."""
        return await self._get_list(f"/proposicoes/{id_proposicao}/tramitacoes")

    async def get_proposicao_votacoes(self, id_proposicao: str | int) -> list[dict]:
        """Votações de uma proposição."""
        return await self._get_list(f"/proposicoes/{id_proposicao}/votacoes")

    async def get_proposicao_autores(self, id_proposicao: str | int) -> list[dict]:
        """Autores de uma proposição."""
        return await self._get_list(f"/proposicoes/{id_proposicao}/autores")

    async def get_proposicao_temas(self, id_proposicao: str | int) -> list[dict]:
        """Temas de uma proposição."""
        return await self._get_list(f"/proposicoes/{id_proposicao}/temas")

    async def get_proposicao_relacionadas(self, id_proposicao: str | int) -> list[dict]:
        """Proposicoes relacionadas a uma proposicao."""
        return await self._get_list(f"/proposicoes/{id_proposicao}/relacionadas")

    # ========== EVENTOS / SESSÕES ==========

    async def get_eventos_dia(self, data: date | None = None) -> list[dict]:
        """Eventos do dia (sessões, audiências, etc)."""
        if data is None:
            data = date.today()
        return await self._get_list("/eventos", {
            "dataInicio": data.isoformat(),
            "dataFim": data.isoformat(),
            "ordem": "ASC",
            "ordenarPor": "dataHoraInicio"
        })

    async def get_eventos_periodo(self, data_inicio: date, data_fim: date) -> list[dict]:
        """Eventos em um período."""
        return await self._get_list("/eventos", {
            "dataInicio": data_inicio.isoformat(),
            "dataFim": data_fim.isoformat(),
            "ordem": "ASC",
            "ordenarPor": "dataHoraInicio"
        })

    async def get_evento_detalhe(self, id_evento: str | int) -> dict:
        """Detalhe de um evento."""
        return await self._get(f"/eventos/{id_evento}")

    async def get_evento_deputados(self, id_evento: str | int) -> list[dict]:
        """Deputados presentes em um evento."""
        return await self._get_list(f"/eventos/{id_evento}/deputados")

    async def get_evento_orgaos(self, id_evento: str | int) -> list[dict]:
        """Orgaos organizadores de um evento."""
        return await self._get_list(f"/eventos/{id_evento}/orgaos")

    async def get_evento_votacoes(self, id_evento: str | int) -> list[dict]:
        """Votacoes realizadas em um evento."""
        return await self._get_list(f"/eventos/{id_evento}/votacoes")

    # ========== VOTAÇÕES ==========

    async def get_votacoes_periodo(self, data_inicio: date, data_fim: date, id_orgao: int | None = None) -> list[dict]:
        """Votações em um período."""
        params: dict[str, Any] = {
            "dataInicio": data_inicio.isoformat(),
            "dataFim": data_fim.isoformat(),
            "ordem": "DESC",
            "ordenarPor": "dataHoraRegistro"
        }
        if id_orgao:
            params["idOrgao"] = str(id_orgao)
        return await self._get_list("/votacoes", params)

    async def get_votacao_detalhe(self, id_votacao: str | int) -> dict:
        """Detalhe de uma votação."""
        return await self._get(f"/votacoes/{id_votacao}")

    async def get_votos_votacao(self, id_votacao: str | int) -> list[dict]:
        """Votos de uma votação."""
        return await self._get_list(f"/votacoes/{id_votacao}/votos")

    # ========== ÓRGÃOS / COMISSÕES ==========

    async def lista_orgaos(self) -> list[dict]:
        """Lista de órgãos da Câmara."""
        return await self._get_list("/orgaos")

    async def get_orgao_detalhe(self, id_orgao: str | int) -> dict:
        """Detalhe de um órgão."""
        return await self._get(f"/orgaos/{id_orgao}")

    async def get_eventos_orgao_periodo(self, id_orgao: str | int, data_inicio: date, data_fim: date) -> list[dict]:
        """Eventos de um órgão em período."""
        return await self._get_list(f"/orgaos/{id_orgao}/eventos", {
            "dataInicio": data_inicio.isoformat(),
            "dataFim": data_fim.isoformat(),
            "ordem": "ASC",
            "ordenarPor": "dataHoraInicio"
        })

    # ========== LEGISLATURAS ==========

    async def lista_legislaturas(self) -> list[dict]:
        """Lista de legislaturas."""
        return await self._get_list("/legislaturas")

    async def get_legislatura_detalhe(self, id_legislatura: str | int) -> dict:
        """Detalhe de uma legislatura."""
        return await self._get(f"/legislaturas/{id_legislatura}")

    async def get_legislatura_mesa(self, id_legislatura: str | int) -> list[dict]:
        """Mesa diretora de uma legislatura."""
        return await self._get_list(f"/legislaturas/{id_legislatura}/mesa")

    # ========== PARTIDOS ==========

    async def lista_partidos(self) -> list[dict]:
        """Lista de partidos."""
        return await self._get_list("/partidos")

    async def get_partido_detalhe(self, id_partido: str | int) -> dict:
        """Detalhes de um partido."""
        return await self._get(f"/partidos/{id_partido}")

    async def get_partido_membros(self, id_partido: str | int) -> list[dict]:
        """Membros de um partido (deputados)."""
        return await self._get_list(f"/partidos/{id_partido}/membros")

    # ========== BLOCOS ==========

    async def lista_blocos(self) -> list[dict]:
        """Lista de blocos parlamentares."""
        return await self._get_list("/blocos")

    async def get_bloco_detalhe(self, id_bloco: str | int) -> dict:
        """Detalhes de um bloco parlamentar."""
        return await self._get(f"/blocos/{id_bloco}")

    # ========== FRENTES ==========

    async def lista_frentes(self, id_legislatura: int | None = None) -> list[dict]:
        """Lista de frentes parlamentares."""
        params: dict[str, Any] = {}
        if id_legislatura:
            params["idLegislatura"] = str(id_legislatura)
        return await self._get_list("/frentes", params)

    async def get_frente_detalhe(self, id_frente: str | int) -> dict:
        """Detalhes de uma frente parlamentar."""
        return await self._get(f"/frentes/{id_frente}")

    async def get_frente_membros(self, id_frente: str | int) -> list[dict]:
        """Membros de uma frente parlamentar."""
        return await self._get_list(f"/frentes/{id_frente}/membros")

    # ========== NOVOS ENDPOINTS ==========

    async def get_orientacoes_votacao(self, id_votacao: str | int) -> list[dict]:
        """Orientações dos partidos em uma votação."""
        return await self._get_list(f"/votacoes/{id_votacao}/orientacoes")

    async def get_membros_orgao(self, id_orgao: str | int) -> list[dict]:
        """Membros de um órgão/comissão."""
        return await self._get_list(f"/orgaos/{id_orgao}/membros")

    async def get_pauta_evento(self, id_evento: str | int) -> list[dict]:
        """Pauta de um evento (sessão/audiência)."""
        return await self._get_list(f"/eventos/{id_evento}/pauta")

    async def get_orgao_membros_periodo(self, id_orgao: str | int, data_inicio: date, data_fim: date) -> list[dict]:
        """Membros de uma comissão em um período."""
        return await self._get_list(f"/orgaos/{id_orgao}/membros", {
            "dataInicio": data_inicio.isoformat(),
            "dataFim": data_fim.isoformat()
        })

    async def get_deputado_orgaos(self, id_deputado: str | int) -> list[dict]:
        """Órgãos/comissões em que o deputado participa."""
        return await self._get_list(f"/deputados/{id_deputado}/orgaos")

    async def get_deputado_ocupacoes(self, id_deputado: str | int) -> list[dict]:
        """Historico de ocupacoes/profissoes de um deputado."""
        return await self._get_list(f"/deputados/{id_deputado}/ocupacoes")

    async def get_votacoes_orgao(self, id_orgao: str | int, data_inicio: date | None = None, data_fim: date | None = None) -> list[dict]:
        """Votacoes de um orgao/comissao."""
        params: dict[str, Any] = {}
        if data_inicio:
            params["dataInicio"] = data_inicio.isoformat()
        if data_fim:
            params["dataFim"] = data_fim.isoformat()
        return await self._get_list(f"/orgaos/{id_orgao}/votacoes", params)

    # ========== REFERÊNCIAS ==========

    async def get_referencias_situacao_deputado(self) -> list[dict]:
        """Codigos de situacao de deputados."""
        return await self._get_list("/referencias/deputados/codSituacao")

    async def get_referencias_situacao_proposicao(self) -> list[dict]:
        """Codigos de situacao de proposicoes."""
        return await self._get_list("/referencias/proposicoes/codSituacaoProposicao")

    async def get_referencias_tipo_proposicao(self) -> list[dict]:
        """Siglas de tipo de proposicao (PL, PEC, etc)."""
        return await self._get_list("/referencias/proposicoes/siglaTipo")

    async def get_referencias_temas(self) -> list[dict]:
        """Lista de temas/assuntos."""
        return await self._get_list("/referencias/proposicoes/tema")

    async def get_referencias_tipos_evento(self) -> list[dict]:
        """Tipos de evento."""
        return await self._get_list("/referencias/tiposEvento")

    async def get_referencias_tipos_orgao(self) -> list[dict]:
        """Tipos de orgao."""
        return await self._get_list("/referencias/tiposOrgao")

    async def get_referencias_uf(self) -> list[dict]:
        """Lista de UFs."""
        return await self._get_list("/referencias/uf")

    # ========== UTILITÁRIOS ==========

    async def get_proposicoes_recentes(self, dias: int = 7) -> list[dict]:
        """Busca proposições apresentadas nos últimos N dias."""
        hoje = date.today()
        inicio = hoje - timedelta(days=dias)

        params: dict[str, Any] = {
            "dataApresentacaoInicio": inicio.isoformat(),
            "dataApresentacaoFim": hoje.isoformat(),
            "ordem": "DESC",
            "ordenarPor": "id",
            "itens": 50,
        }
        return await self._get_list("/proposicoes", params)

    async def get_votacoes_semana(self) -> list[dict]:
        """Votações da última semana."""
        return await self.get_votacoes_periodo(
            date.today() - timedelta(days=7),
            date.today()
        )

    async def get_eventos_semana(self) -> list[dict]:
        """Eventos da semana atual."""
        hoje = date.today()
        return await self.get_eventos_periodo(hoje, hoje + timedelta(days=7))


# Instância global
_client: CamaraClient | None = None


def get_camara_client() -> CamaraClient:
    """Retorna instância singleton do cliente."""
    global _client
    if _client is None:
        _client = CamaraClient()
    return _client


async def close_camara_client():
    """Fecha o cliente global."""
    global _client
    if _client:
        await _client.close()
        _client = None


# ========== FACADE FUNCTIONS (uso direto) ==========

async def lista_deputados() -> list[dict]:
    """Facade: lista de deputados."""
    client = get_camara_client()
    return await client.lista_deputados()


async def buscar_deputado(nome: str) -> list[dict]:
    """Facade: busca deputados por nome."""
    client = get_camara_client()
    return await client.buscar_deputado_por_nome(nome)


async def pesquisar_proposicoes(keywords: str | None = None, ano: int | None = None, sigla_tipo: str | None = None) -> list[dict]:
    """Facade: pesquisa proposições."""
    client = get_camara_client()
    return await client.pesquisar_proposicoes(keywords=keywords, ano=ano, sigla_tipo=sigla_tipo)


async def get_votacoes_semana() -> list[dict]:
    """Facade: votações da semana."""
    client = get_camara_client()
    return await client.get_votacoes_semana()


async def get_eventos_semana() -> list[dict]:
    """Facade: eventos da semana."""
    client = get_camara_client()
    return await client.get_eventos_semana()


async def get_proposicoes_recentes(dias: int = 7) -> list[dict]:
    """Facade: proposições recentes."""
    client = get_camara_client()
    return await client.get_proposicoes_recentes(dias)
