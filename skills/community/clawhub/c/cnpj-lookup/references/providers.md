# Provedores de Consulta CNPJ

Este documento lista os provedores utilizados pela skill CNPJ Lookup, seus endpoints, limites e comportamento em caso de erro.

## Provedor A: BrasilAPI (Primário)

### Endpoint
```
GET https://brasilapi.com.br/api/cnpj/v1/{cnpj}
```

### Características
- **Rate Limit**: 60 req/min (implementamos 30 req/min por segurança)
- **Autenticação**: Não requer API key
- **Formato**: JSON
- **Dados retornados**: Completos (razão social, endereço, QSA, CNAEs, etc.)

### Códigos de Erro
- `200`: Sucesso
- `404`: CNPJ não encontrado
- `429`: Rate limit excedido (Retry-After header presente)
- `500`: Erro interno

### Observações
- Provider mais completo e confiável
- Recomendado como primeira opção

---

## Provedor B: CNPJ.ws (Secundário)

### Endpoint
```
GET https://publica.cnpj.ws/cnpj/{cnpj_sem_pontuacao}
```

### Características
- **Rate Limit**: 3 req/min por IP (implementamos 2 req/min)
- **Autenticação**: Não requer API key
- **Formato**: JSON
- **Dados retornados**: Completos

### Códigos de Erro
- `200`: Sucesso
- `404`: CNPJ não encontrado
- `429`: Rate limit excedido (CRÍTICO - limite muito baixo)
- `500`: Erro interno

### Observações
- **ATENÇÃO**: Rate limit muito agressivo (3 req/min)
- Se receber 429, fazer backoff de pelo menos 30 segundos
- Usar apenas como fallback se BrasilAPI falhar

---

## Provedor C: OpenCNPJ (Terciário)

### Endpoint
```
GET https://api.opencnpj.org/{cnpj}
```
(Aceita CNPJ com ou sem pontuação)

### Características
- **Rate Limit**: 30 req/min
- **Autenticação**: Não requer API key
- **Formato**: JSON
- **Dados retornados**: Básicos (menos completo que os outros)

### Códigos de Erro
- `200`: Sucesso
- `404`: CNPJ não encontrado
- `429`: Rate limit excedido
- `500`: Erro interno

### Observações
- Útil como último recurso
- Pode ter dados menos completos (especialmente QSA)

---

## Estratégia de Fallback

1. **BrasilAPI** → tentar primeiro (mais completo)
2. **CNPJ.ws** → se BrasilAPI falhar (rate limit ou erro)
3. **OpenCNPJ** → se todos anteriores falharem

## Tratamento de Rate Limit

### Ao receber HTTP 429:
1. Verificar header `Retry-After` (se presente, usar esse valor)
2. Se não houver, calcular backoff exponencial:
   - Base: tempo até próximo request possível × 1.5
   - Jitter: +0.5 a 2 segundos aleatório
   - Máximo: 30 segundos
3. Tentar novamente uma única vez
4. Se falhar novamente, pular para próximo provider

### Boas Práticas
- Sempre implementar cache local (24h por padrão)
- Nunca fazer mais requests que o limite permitido
- Logging de rate limits atingidos para debugging

---

## Referência Rápida

| Provider    | Endpoint                              | Rate Limit | Completo | Prioridade |
|------------|---------------------------------------|------------|----------|------------|
| BrasilAPI  | brasilapi.com.br/api/cnpj/v1/         | 30/min     | ✅ Sim    | 1          |
| CNPJ.ws    | publica.cnpj.ws/cnpj/                 | 2/min      | ✅ Sim    | 2          |
| OpenCNPJ   | api.opencnpj.org/                     | 30/min     | ⚠️ Parcial| 3          |
