# Schema de Dados Normalizados

Este documento descreve o schema interno de dados utilizado pela skill CNPJ Lookup, incluindo mapeamentos de campos entre provedores.

## Schema Principal

```json
{
  "cnpj": "string",
  "razao_social": "string",
  "nome_fantasia": "string",
  "situacao_cadastral": "string",
  "data_situacao": "string (YYYY-MM-DD)",
  "data_inicio_atividade": "string (DD/MM/YYYY ou YYYY-MM-DD)",
  "cnae_principal": {
    "codigo": "string",
    "descricao": "string"
  },
  "cnaes_secundarios": [
    {
      "codigo": "string",
      "descricao": "string"
    }
  ],
  "natureza_juridica": "string",
  "porte": "string",
  "capital_social": "string (valor em reais)",
  "endereco": {
    "logradouro": "string",
    "numero": "string",
    "complemento": "string",
    "bairro": "string",
    "municipio": "string",
    "uf": "string (sigla)",
    "cep": "string"
  },
  "contato": {
    "email": "string",
    "telefone": "string"
  },
  "qsa": [
    {
      "nome": "string",
      "qualificacao": "string"
    }
  ],
  "fonte": "string (BrasilAPI | CNPJ.ws | OpenCNPJ)",
  "fetched_at": "string (ISO datetime)",
  "cached": "boolean"
}
```

## Mapeamento por Provedor

### BrasilAPI → Schema Normalizado

| Campo BrasilAPI           | Campo Normalizado         | Observações                    |
|--------------------------|--------------------------|--------------------------------|
| cnpj                     | cnpj                    | Já formatado                  |
| razao_social             | razao_social            |                                |
| nome_fantasia            | nome_fantasia           |                                |
| situacao_cadastral       | situacao_cadastral      |                                |
| data_situacao            | data_situacao           |                                |
| data_inicio_atividade    | data_inicio_atividade   |                                |
| cnae_fiscal              | cnae_principal.codigo   |                                |
| cnae_fiscal_descricao   | cnae_principal.descricao|                                |
| cnaes_secundarios       | cnaes_secundarios       | Lista de objetos              |
| natureza_juridica        | natureza_juridica       |                                |
| porte                    | porte                   |                                |
| capital_social           | capital_social          | String com valor              |
| logradouro               | endereco.logradouro     |                                |
| numero                   | endereco.numero         |                                |
| complemento              | endereco.complemento   |                                |
| bairro                   | endereco.bairro        |                                |
| municipio                | endereco.municipio      |                                |
| uf                       | endereco.uf             |                                |
| cep                      | endereco.cep            |                                |
| email                    | contato.email           |                                |
| telefone1 / telefone2    | contato.telefone       | Prioriza telefone1            |
| qsa                      | qsa                     | Lista de sócios               |

### CNPJ.ws → Schema Normalizado

| Campo CNPJ.ws          | Campo Normalizado         | Observações                    |
|-----------------------|--------------------------|--------------------------------|
| cnpj                  | cnpj                    |                                |
| razao_social          | razao_social            |                                |
| estabelecimento.nome_fantasia | nome_fantasia |                                |
| estabelecimento.situacao_cadastral | situacao_cadastral |                    |
| estabelecimento.data_situacao_cadastral | data_situacao |                     |
| estabelecimento.data_inicio_atividade | data_inicio_atividade |                 |
| estabelecimento.cnae_fiscal | cnae_principal.codigo |                         |
| estabelecimento.cnaes_secundarios | cnaes_secundarios |                       |
| natureza_juridica.codigo | natureza_juridica     |                                |
| porte.descricao       | porte                   |                                |
| capital_social        | capital_social          |                                |
| estabelecimento.logradouro | endereco.logradouro |                                |
| estabelecimento.numero | endereco.numero        |                                |
| estabelecimento.complemento | endereco.complemento |                              |
| estabelecimento.bairro | endereco.bairro        |                                |
| estabelecimento.cidade.nome | endereco.municipio |                                |
| estabelecimento.estado.sigla | endereco.uf       |                                |
| estabelecimento.cep   | endereco.cep            |                                |
| estabelecimento.email | contato.email           |                                |
| socios                | qsa                     | Lista com nome e qualificação |

### OpenCNPJ → Schema Normalizado

| Campo OpenCNPJ        | Campo Normalizado         | Observações                    |
|---------------------|--------------------------|--------------------------------|
| cnpj                | cnpj                    |                                |
| razao_social        | razao_social            |                                |
| nome_fantasia       | nome_fantasia           |                                |
| status              | situacao_cadastral      |                                |
| updated_at          | data_situacao           | Truncado para YYYY-MM-DD      |
| abertura            | data_inicio_atividade   |                                |
| cnae                | cnae_principal.codigo  | Apenas código, sem descrição  |
| natureza_juridica   | natureza_juridica       |                                |
| porte               | porte                   |                                |
| capital_social      | capital_social         |                                |
| logradouro          | endereco.logradouro     |                                |
| numero              | endereco.numero         |                                |
| complemento         | endereco.complemento   |                                |
| bairro              | endereco.bairro        |                                |
| municipio           | endereco.municipio      |                                |
| uf                  | endereco.uf             |                                |
| cep                 | endereco.cep           |                                |
| email               | contato.email           |                                |
| telefone            | contato.telefone        |                                |
| (não disponível)    | qsa                     | ❌ Não disponível              |
| (não disponível)   | cnaes_secundarios       | ❌ Não disponível              |

## Divergências Known

### QSA (Quadro de Sócios)
- **BrasilAPI**: ✅ Completo
- **CNPJ.ws**: ✅ Completo
- **OpenCNPJ**: ❌ Não disponível

### CNAE Secundários
- **BrasilAPI**: ✅ Completo (com descrições)
- **CNPJ.ws**: ✅ Completo (apenas códigos)
- **OpenCNPJ**: ❌ Não disponível

### Descrições de CNAE
- **BrasilAPI**: ✅ Inclui descrição
- **CNPJ.ws**: ❌ Apenas códigos
- **OpenCNPJ**: ❌ Apenas código principal

### Dados de Contato
- **BrasilAPI**: Email + Telefone(s)
- **CNPJ.ws**: Apenas Email
- **OpenCNPJ**: Email + Telefone

## Campos Obrigatórios

Os seguintes campos devem sempre estar presentes no output (mesmo que vazios):
- `cnpj`
- `razao_social`
- `situacao_cadastral`
- `fonte`
- `fetched_at`
- `cached`

## Notas de Implementação

1. **CNPJ formatado**: Sempre salvar como 14 dígitos (sem pontuação) para cache e busca
2. **Display**: Formatar como XX.XXX.XXX/XXXX-XX para exibição
3. **Capital Social**: Manter como string, formatar como "R$ X.XXX,XX" na saída Markdown
4. **CEP**: Manter como string sem pontuação (8 dígitos)
5. **UF**: Sempre em maiúsculas (sigla de 2 letras)
