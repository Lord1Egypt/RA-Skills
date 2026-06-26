# Tabela FIPE Skill

Consulta preços de veículos (carros, motos, caminhões) na Tabela FIPE brasileira.

## O que é a Tabela FIPE?

A **Tabela FIPE** é uma referência oficial de preços médios de veículos no Brasil, calculada pela **Fundação Instituto de Pesquisas Econômicas (FIPE)** ligada à USP. Atualizada mensalmente, é usada para:
- Compra e venda de veículos
- Financiamentos e consórcios
- Cálculo de seguros
- Base para IPVA

## Gatilhos

Ative a skill usando:
- `"fipe"`, `"tabela fipe"` — buscar preço
- `"preço carro"`, `"valor carro"` — consultar
- `"carro tá quanto"` — consulta informal

## Como Usar

```bash
# Listar marcas de carros
node src/index.js marcas

# Listar modelos de uma marca
node src/index.js modelos 59  # 59 = Volkswagen

# List anos de um modelo
node src/index.js anos 59 5940

# Ver preço de um veículo
node src/index.js preco 59 5940 2014-3

# Busca rápida por nome (pesquisa em todas as marcas)
node src/index.js search "Hilux"
```

## Busca Inteligente

A skill suporta busca por nome que retorna modelos compatíveis:
```bash
node src/index.js search "Toyota Corolla"
node src/index.js search "Honda Civic"
```

## API

- **URL Base:** https://parallelum.com.br/fipe/api/v1
- **Autenticação:** Não requer API key
- **Veículos:** carros, motos, caminhoes

## Exemplos de Códigos de Marcas

| Código | Marca |
|--------|-------|
| 59 | Volkswagen |
| 21 | Chevrolet |
| 23 | Ford |
| 33 | Fiat |
| 2 | Honda (motos) |
| 1 | Yamaha (motos) |
