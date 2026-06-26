"""Testes unitários para camara_client."""
import pytest
from unittest.mock import AsyncMock, Mock, patch, PropertyMock
from datetime import date

from camara_client import (
    CamaraClient,
    get_camara_client,
    CamaraAPIError,
    CamaraTimeoutError,
    CamaraNotFoundError,
    CamaraConnectionError,
)


def _make_mock_client(responses):
    """Helper: cria mock httpx client com lista de respostas sequenciais."""
    mock_client = AsyncMock()
    type(mock_client).is_closed = PropertyMock(return_value=False)
    if isinstance(responses, list):
        mock_client.get.side_effect = responses
    else:
        mock_client.get.return_value = responses
    return mock_client


def _make_response(json_data, status_code=200):
    """Helper: cria mock de resposta HTTP."""
    resp = Mock()
    resp.json.return_value = json_data
    resp.raise_for_status = Mock()
    resp.status_code = status_code
    return resp


@pytest.mark.asyncio
class TestCamaraClient:
    """Testes do cliente da Câmara."""

    async def test_client_initialization(self):
        """Testa inicialização do cliente."""
        client = CamaraClient()
        assert client.client is None
        assert client.timeout == 45.0

    async def test_custom_timeout(self):
        """Testa timeout customizado."""
        client = CamaraClient(timeout=10.0)
        assert client.timeout == 10.0

    async def test_get_singleton(self):
        """Testa padrão singleton."""
        import camara_client as mod
        mod._client = None
        client1 = get_camara_client()
        client2 = get_camara_client()
        assert client1 is client2
        mod._client = None

    @patch('camara_client.httpx.AsyncClient')
    async def test_lista_deputados_success(self, mock_httpx, mock_camara_response):
        """Testa listagem de deputados com sucesso."""
        mock_client = _make_mock_client(_make_response(mock_camara_response))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.lista_deputados()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['nome'] == "Marcos Pontes"

    @patch('camara_client.httpx.AsyncClient')
    async def test_lista_deputados_sem_legislatura(self, mock_httpx, mock_camara_response):
        """Testa listagem sem especificar legislatura."""
        mock_client = _make_mock_client(_make_response(mock_camara_response))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        await client.lista_deputados()

        call_kwargs = mock_client.get.call_args
        params = call_kwargs.kwargs.get('params', call_kwargs[1].get('params', {}))
        assert 'idLegislatura' not in params

    @patch('camara_client.httpx.AsyncClient')
    async def test_buscar_deputado_por_nome(self, mock_httpx, mock_camara_response):
        """Testa busca de deputado por nome."""
        mock_client = _make_mock_client(_make_response(mock_camara_response))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.buscar_deputado_por_nome("Marcos")

        assert len(result) == 1
        assert "marcos" in result[0]['nome'].lower()

    @patch('camara_client.httpx.AsyncClient')
    async def test_pesquisar_proposicoes_success(self, mock_httpx, mock_proposicao_response):
        """Testa pesquisa de proposições."""
        mock_client = _make_mock_client(_make_response(mock_proposicao_response))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.pesquisar_proposicoes(sigla_tipo="PL", ano=2026)

        assert isinstance(result, list)
        assert result[0]['siglaTipo'] == "PL"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_with_timeout_and_retry(self, mock_httpx):
        """Testa retry após timeout."""
        import httpx
        success_resp = _make_response({"dados": {"id": 1}})
        mock_client = _make_mock_client([
            httpx.TimeoutException("Timeout"),
            success_resp,
        ])
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client._get("/test")
        assert result == {"id": 1}
        assert mock_client.get.call_count == 2

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_timeout_exhausts_retries(self, mock_httpx):
        """Testa que timeout esgota tentativas."""
        import httpx
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = httpx.TimeoutException("Timeout")
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        with pytest.raises(CamaraTimeoutError):
            await client._get("/test", retries=2)
        assert mock_client.get.call_count == 2

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_with_404_error(self, mock_httpx):
        """Testa tratamento de 404 (sem retry)."""
        import httpx
        mock_response = Mock()
        mock_response.status_code = 404
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Not found", request=Mock(), response=mock_response
        )
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        with pytest.raises(CamaraNotFoundError):
            await client._get("/test")
        assert mock_client.get.call_count == 1

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_with_connection_error_and_retry(self, mock_httpx):
        """Testa retry após erro de conexão."""
        import httpx
        mock_client = AsyncMock()
        type(mock_client).is_closed = PropertyMock(return_value=False)
        mock_client.get.side_effect = httpx.ConnectError("Connection failed")
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        with pytest.raises(CamaraConnectionError):
            await client._get("/test", retries=2)
        assert mock_client.get.call_count == 2

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_list_pagination(self, mock_httpx):
        """Testa paginação automática em _get_list."""
        page1 = _make_response({"dados": [{"id": i} for i in range(100)]})
        page2 = _make_response({"dados": [{"id": 100}]})
        mock_client = _make_mock_client([page1, page2])
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client._get_list("/test")

        assert len(result) == 101
        assert mock_client.get.call_count == 2

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_list_uses_retry(self, mock_httpx):
        """Testa que _get_list tem retry via _get_raw."""
        import httpx
        success_resp = _make_response({"dados": [{"id": 1}]})
        mock_client = _make_mock_client([
            httpx.TimeoutException("Timeout"),
            success_resp,
        ])
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client._get_list("/test")

        assert len(result) == 1

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_eventos_dia(self, mock_httpx):
        """Testa busca de eventos do dia."""
        mock_client = _make_mock_client(_make_response({"dados": []}))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_eventos_dia(date(2026, 4, 2))

        assert isinstance(result, list)
        assert len(result) == 0

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_orientacoes_votacao(self, mock_httpx):
        """Testa novo endpoint: orientações de votação."""
        orientacoes = {"dados": [{"siglaPartido": "PT", "orientacao": "Sim"}]}
        mock_client = _make_mock_client(_make_response(orientacoes))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_orientacoes_votacao("12345")

        assert isinstance(result, list)
        assert result[0]['siglaPartido'] == "PT"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_membros_orgao(self, mock_httpx):
        """Testa novo endpoint: membros de órgão."""
        membros = {"dados": [{"nome": "Deputado A"}]}
        mock_client = _make_mock_client(_make_response(membros))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_membros_orgao(123)

        assert len(result) == 1

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_deputado_orgaos(self, mock_httpx):
        """Testa novo endpoint: órgãos do deputado."""
        orgaos = {"dados": [{"sigla": "CCJC", "nome": "Comissão de Constituição e Justiça"}]}
        mock_client = _make_mock_client(_make_response(orgaos))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_deputado_orgaos(204554)

        assert len(result) == 1
        assert result[0]['sigla'] == "CCJC"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_proposicoes_recentes_uses_date_filter(self, mock_httpx):
        """Testa que get_proposicoes_recentes passa filtro de data."""
        mock_client = _make_mock_client(_make_response({"dados": []}))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        await client.get_proposicoes_recentes(dias=7)

        call_kwargs = mock_client.get.call_args
        params = call_kwargs.kwargs.get('params', call_kwargs[1].get('params', {}))
        assert 'dataApresentacaoInicio' in params
        assert 'dataApresentacaoFim' in params

    async def test_close_client(self):
        """Testa fechamento do cliente."""
        client = CamaraClient()
        client.client = AsyncMock()
        client.client.is_closed = False

        await client.close()

        client.client.aclose.assert_called_once()

    async def test_close_when_already_closed(self):
        """Testa close quando já fechado."""
        client = CamaraClient()
        client.client = AsyncMock()
        client.client.is_closed = True

        await client.close()
        client.client.aclose.assert_not_called()

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_deputado_ocupacoes(self, mock_httpx):
        """Testa endpoint: ocupações de deputado."""
        ocupacoes = {"dados": [{"titulo": "Engenheiro", "entidade": "NASA"}]}
        mock_client = _make_mock_client(_make_response(ocupacoes))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_deputado_ocupacoes(204554)

        assert isinstance(result, list)
        assert result[0]['titulo'] == "Engenheiro"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_proposicao_relacionadas(self, mock_httpx):
        """Testa endpoint: proposições relacionadas."""
        relacionadas = {"dados": [{"id": 111, "siglaTipo": "PL", "numero": 99}]}
        mock_client = _make_mock_client(_make_response(relacionadas))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_proposicao_relacionadas(2366661)

        assert len(result) == 1
        assert result[0]['siglaTipo'] == "PL"

    @patch('camara_client.httpx.AsyncClient')
    async def test_pesquisar_proposicoes_com_tema(self, mock_httpx, mock_proposicao_response):
        """Testa pesquisa de proposições com parâmetro tema."""
        mock_client = _make_mock_client(_make_response(mock_proposicao_response))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        await client.pesquisar_proposicoes(tema=62)

        call_kwargs = mock_client.get.call_args
        params = call_kwargs.kwargs.get('params', call_kwargs[1].get('params', {}))
        assert params.get('tema') == '62'

    @patch('camara_client.httpx.AsyncClient')
    async def test_pesquisar_proposicoes_tramitacao_senado(self, mock_httpx, mock_proposicao_response):
        """Testa pesquisa de proposições com tramitacaoSenado."""
        mock_client = _make_mock_client(_make_response(mock_proposicao_response))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        await client.pesquisar_proposicoes(tramitacao_senado=True)

        call_kwargs = mock_client.get.call_args
        params = call_kwargs.kwargs.get('params', call_kwargs[1].get('params', {}))
        assert params.get('tramitacaoSenado') == 'true'

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_evento_deputados(self, mock_httpx):
        """Testa endpoint: deputados em evento."""
        deps = {"dados": [{"id": 204554, "nome": "Marcos Pontes"}]}
        mock_client = _make_mock_client(_make_response(deps))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_evento_deputados(12345)

        assert len(result) == 1
        assert result[0]['nome'] == "Marcos Pontes"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_evento_votacoes(self, mock_httpx):
        """Testa endpoint: votações de evento."""
        vots = {"dados": [{"id": "v1", "descricao": "Votação teste"}]}
        mock_client = _make_mock_client(_make_response(vots))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_evento_votacoes(12345)

        assert len(result) == 1
        assert result[0]['id'] == "v1"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_votacoes_orgao(self, mock_httpx):
        """Testa endpoint: votações de órgão."""
        vots = {"dados": [{"id": "v2", "descricao": "Votação comissão"}]}
        mock_client = _make_mock_client(_make_response(vots))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_votacoes_orgao(180, data_inicio=date(2026, 1, 1), data_fim=date(2026, 1, 31))

        assert len(result) == 1

    @patch('camara_client.httpx.AsyncClient')
    async def test_lista_blocos(self, mock_httpx):
        """Testa endpoint: lista de blocos parlamentares."""
        blocos = {"dados": [{"id": 1, "nome": "Bloco X"}]}
        mock_client = _make_mock_client(_make_response(blocos))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.lista_blocos()

        assert len(result) == 1
        assert result[0]['nome'] == "Bloco X"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_bloco_detalhe(self, mock_httpx):
        """Testa endpoint: detalhe de bloco parlamentar."""
        bloco = {"dados": {"id": 1, "nome": "Bloco X", "idLegislatura": 57}}
        mock_client = _make_mock_client(_make_response(bloco))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_bloco_detalhe(1)

        assert result['nome'] == "Bloco X"

    @patch('camara_client.httpx.AsyncClient')
    async def test_lista_frentes(self, mock_httpx):
        """Testa endpoint: lista de frentes parlamentares."""
        frentes = {"dados": [{"id": 100, "titulo": "Frente da Educação"}]}
        mock_client = _make_mock_client(_make_response(frentes))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.lista_frentes(id_legislatura=57)

        assert len(result) == 1
        assert result[0]['titulo'] == "Frente da Educação"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_frente_membros(self, mock_httpx):
        """Testa endpoint: membros de frente parlamentar."""
        membros = {"dados": [{"nome": "Deputado A", "titulo": "Coordenador"}]}
        mock_client = _make_mock_client(_make_response(membros))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_frente_membros(100)

        assert len(result) == 1
        assert result[0]['titulo'] == "Coordenador"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_partido_detalhe(self, mock_httpx):
        """Testa endpoint: detalhe de partido."""
        partido = {"dados": {"id": 36899, "sigla": "PL", "nome": "Partido Liberal"}}
        mock_client = _make_mock_client(_make_response(partido))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_partido_detalhe(36899)

        assert result['sigla'] == "PL"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_partido_membros(self, mock_httpx):
        """Testa endpoint: membros de partido."""
        membros = {"dados": [{"id": 1, "nome": "Deputado X", "siglaUf": "SP"}]}
        mock_client = _make_mock_client(_make_response(membros))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_partido_membros(36899)

        assert len(result) == 1
        assert result[0]['siglaUf'] == "SP"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_legislatura_mesa(self, mock_httpx):
        """Testa endpoint: mesa diretora da legislatura."""
        mesa = {"dados": [{"nome": "Arthur Lira", "titulo": "Presidente"}]}
        mock_client = _make_mock_client(_make_response(mesa))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_legislatura_mesa(57)

        assert len(result) == 1
        assert result[0]['titulo'] == "Presidente"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_referencias_temas(self, mock_httpx):
        """Testa endpoint: referências de temas."""
        temas = {"dados": [{"cod": 62, "nome": "Educação"}]}
        mock_client = _make_mock_client(_make_response(temas))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_referencias_temas()

        assert len(result) == 1
        assert result[0]['nome'] == "Educação"

    @patch('camara_client.httpx.AsyncClient')
    async def test_get_referencias_uf(self, mock_httpx):
        """Testa endpoint: referências de UFs."""
        ufs = {"dados": [{"sigla": "SP", "nome": "São Paulo"}]}
        mock_client = _make_mock_client(_make_response(ufs))
        mock_httpx.return_value = mock_client

        client = CamaraClient()
        result = await client.get_referencias_uf()

        assert len(result) == 1
        assert result[0]['sigla'] == "SP"
