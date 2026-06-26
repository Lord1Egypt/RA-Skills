"""Configuração do pytest para testes do camara_client."""
import pytest


@pytest.fixture
def mock_camara_response():
    """Mock de resposta típica da API da Câmara."""
    return {
        "dados": [
            {
                "id": 204554,
                "nome": "Marcos Pontes",
                "siglaPartido": "PL",
                "siglaUf": "SP",
                "urlFoto": "https://...",
                "email": "dep.marcospontes@camara.leg.br"
            }
        ]
    }


@pytest.fixture
def mock_proposicao_response():
    """Mock de resposta de pesquisa de proposições."""
    return {
        "dados": [
            {
                "id": 2366661,
                "siglaTipo": "PL",
                "numero": 1234,
                "ano": 2026,
                "ementa": "Dispõe sobre..."
            }
        ]
    }
