---
name: doi-search
description: Obter informações sobre artigos, capítulos e livros publicados com DOI, resolvendo DOI informado ou pesquisando metadados na API REST da Crossref.
metadata: '{"openclaw":{"requires":{"network":true,"bins":["curl"]}}}'
homepage: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
---
# DOI Search

Location: `/skills/doi-search/SKILL.md` from the OpenClaw workspace root.

Use este skill quando o usuário pedir informações bibliográficas, metadados,
links ou confirmação de DOI de artigos, capítulos ou livros.

Use `curl` para todas as requisições REST. DOI.org e Crossref REST API não
exigem chave de API para consultas públicas de metadados.

## Processo

1. Se o usuário informar um DOI, normalize o código e abra:
   `curl -L "https://doi.org/<codigo-doi>"`.
2. Use a página resolvida para identificar título, autores, publicação,
   editora/periódico, ano, URL canônica e acesso ao texto quando disponível.
3. Se o DOI não for informado, mas o usuário pedir para localizar uma obra,
   pesquise na Crossref REST API:
   `curl -sG "https://api.crossref.org/works" --data-urlencode "query=<termos>" --data-urlencode "rows=5"`.
4. Para candidatos Crossref, priorize correspondência por título, autores,
   ano, tipo (`journal-article`, `book`, `book-chapter`, etc.) e fonte.
5. Quando encontrar o DOI provável, confirme os metadados em:
   `curl -sL "https://api.crossref.org/works/<codigo-doi>"`.

Opcionalmente use cabeçalho de contato educado quando houver email operacional
disponível:

```bash
curl -sG "https://api.crossref.org/works" \
  -H "User-Agent: OpenClaw doi-search (mailto:<email>)" \
  --data-urlencode "query=<termos>" \
  --data-urlencode "rows=5"
```

## Saída

Responda de forma sucinta com:

- DOI e link `https://doi.org/<doi>`;
- título;
- autores principais;
- ano;
- tipo de obra;
- periódico/editora quando disponível;
- aviso breve se a correspondência for incerta.

Não invente metadados ausentes. Informe quando a Crossref não retornar
resultado confiável.
