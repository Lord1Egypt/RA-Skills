"""Testes de integração (requerem conexão com a API real)."""
import pytest
from datetime import date, timedelta

from camara_client import get_camara_client


@pytest.mark.integration
@pytest.mark.asyncio
class TestCamaraIntegration:
    """Testes de integração com a API real."""

    async def test_lista_deputados_real(self):
        """Testa listagem real de deputados."""
        client = get_camara_client()
        try:
            deputados = await client.lista_deputados()
            
            assert isinstance(deputados, list)
            assert len(deputados) > 400  # Brasil tem 513 deputados
            
            # Verifica estrutura
            deputado = deputados[0]
            assert 'id' in deputado
            assert 'nome' in deputado
            assert 'siglaPartido' in deputado
        finally:
            await client.close()

    async def test_pesquisar_proposicoes_real(self):
        """Testa pesquisa real de proposições."""
        client = get_camara_client()
        try:
            # Busca específica para evitar paginação excessiva
            proposicoes = await client.pesquisar_proposicoes(
                sigla_tipo="PL",
                ano=2024,
                numero="1"
            )

            assert isinstance(proposicoes, list)
            if len(proposicoes) > 0:
                prop = proposicoes[0]
                assert 'siglaTipo' in prop
                assert prop['siglaTipo'] == "PL"
        finally:
            await client.close()

    async def test_get_eventos_dia_real(self):
        """Testa busca real de eventos."""
        client = get_camara_client()
        try:
            eventos = await client.get_eventos_dia()
            
            assert isinstance(eventos, list)
            # Lista pode estar vazia em dias sem eventos
        finally:
            await client.close()

    async def test_get_votacoes_periodo_real(self):
        """Testa busca real de votações."""
        client = get_camara_client()
        try:
            fim = date.today()
            inicio = fim - timedelta(days=30)
            
            votacoes = await client.get_votacoes_periodo(inicio, fim)
            
            assert isinstance(votacoes, list)
            # Pode estar vazio se não houver votações no período
        finally:
            await client.close()

    async def test_buscar_deputado_especifico_real(self):
        """Testa busca de deputado específico."""
        client = get_camara_client()
        try:
            resultado = await client.buscar_deputado_por_nome("Lula")
            
            assert isinstance(resultado, list)
            # Verifica se encontrou algo
            if len(resultado) > 0:
                assert any("lula" in dep['nome'].lower() for dep in resultado)
        finally:
            await client.close()
