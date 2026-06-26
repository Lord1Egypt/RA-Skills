# Correios Rastreio Skill

Rastreia pacotes e encomendas dos Correios via API oficial.

## Gatilhos

Ative a skill usando:
- `"rastrear"`, `"rastreio"` — rastrear código
- `"onde está meu pacote"` — verificar último
- `"código dos correios"` — ajuda
- `"pedido"`, `"encomenda"` — consultar

## Como Usar

```bash
# Rastrear por código
node src/index.js track PW123456789BR

# Rastrear múltiplos códigos
node src/index.js track "PW123456789BR,AB987654321BR"

# Ver histórico local
node src/index.js history

# Adicionar aos favoritos (apelido)
node src/index.js save PW123456789BR "Presente aniversário"

# Listar favoritos
node src/index.js favorites
```

## Configuração

### Obtendo a API Key

1. Acesse o portal de desenvolvedores dos Correios:
   https://developers.correios.com.br

2. Crie uma conta ou faça login

3. Solicite acesso à API de Rastreamento

4. Copie sua API Key e configure:
   ```bash
   export CORREIOS_API_KEY="sua_api_key_aqui"
   ```

### Variáveis de Ambiente
- `CORREIOS_API_KEY` — Token de autenticação (obrigatório)

## API

- **URL Base:** https://api.correios.com.br
- **Autenticação:** Bearer Token
- **Rate Limit:** 3 requests/segundo
