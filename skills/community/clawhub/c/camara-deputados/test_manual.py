#!/usr/bin/env python3
"""Script de teste manual para validar o cliente da Câmara."""
import asyncio
import sys
from datetime import date, timedelta


async def test_client():
    """Testa funcionalidades básicas do cliente."""
    try:
        from camara_client import get_camara_client
        
        print("🧪 Testando Cliente da Câmara dos Deputados\n")
        print("=" * 60)
        
        client = get_camara_client()
        
        # Teste 1: Listar deputados
        print("\n✓ Teste 1: Listando deputados da legislatura 57...")
        try:
            deputados = await client.lista_deputados()
            print(f"  ✓ Encontrados {len(deputados)} deputados")
            if len(deputados) > 0:
                d = deputados[0]
                print(f"  ✓ Exemplo: {d['nome']} ({d['siglaPartido']}-{d['siglaUf']})")
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            return False
        
        # Teste 2: Buscar deputado por nome
        print("\n✓ Teste 2: Buscando deputado por nome...")
        try:
            resultado = await client.buscar_deputado_por_nome("Lula")
            print(f"  ✓ Encontrados {len(resultado)} resultados para 'Lula'")
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            return False
        
        # Teste 3: Pesquisar proposições
        print("\n✓ Teste 3: Pesquisando proposições (PL 2024)...")
        try:
            proposicoes = await client.pesquisar_proposicoes(
                sigla_tipo="PL",
                ano=2024,
                tramitando=True
            )
            print(f"  ✓ Encontradas {len(proposicoes)} proposições")
            if len(proposicoes) > 0:
                p = proposicoes[0]
                print(f"  ✓ Exemplo: {p['siglaTipo']} {p['numero']}/{p['ano']}")
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            return False
        
        # Teste 4: Eventos de hoje
        print("\n✓ Teste 4: Verificando eventos de hoje...")
        try:
            eventos = await client.get_eventos_dia()
            print(f"  ✓ Encontrados {len(eventos)} eventos")
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            return False
        
        # Teste 5: Votações recentes
        print("\n✓ Teste 5: Buscando votações dos últimos 30 dias...")
        try:
            fim = date.today()
            inicio = fim - timedelta(days=30)
            votacoes = await client.get_votacoes_periodo(inicio, fim)
            print(f"  ✓ Encontradas {len(votacoes)} votações")
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            return False
        
        # Teste 6: Listar órgãos
        print("\n✓ Teste 6: Listando órgãos/comissões...")
        try:
            orgaos = await client.lista_orgaos()
            print(f"  ✓ Encontrados {len(orgaos)} órgãos")
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            return False
        
        await client.close()
        
        print("\n" + "=" * 60)
        print("✅ Todos os testes passaram com sucesso!")
        print("=" * 60)
        return True
        
    except ImportError as e:
        print(f"✗ Erro ao importar módulo: {e}")
        print("  Certifique-se de que httpx está instalado: python3 -m pip install httpx")
        return False
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_client())
    sys.exit(0 if success else 1)
