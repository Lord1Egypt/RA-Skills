---
name: "abnt-citation"
description: "Gera referências bibliográficas no padrão ABNT NBR 6023 a partir de dados informados. Suporta livros, artigos, sites, teses, leis, e mais."
metadata:
  - academic
  - citation
  - abnt
  - brazil
  - reference
  - productivity
allowed-tools:
  - read
  - write
user-invocable: true
---

# ABNT Citation Generator 📚🇧🇷

Gera referências bibliográficas completas no padrão **ABNT NBR 6023** e citações no padrão **ABNT NBR 10520** (autor-data). Basta informar os dados da fonte.

## Público-Alvo

Estudantes universitários, pesquisadores, professores, bibliotecários — qualquer pessoa que precise formatar referências no padrão ABNT.

## Trigger

Invocar quando o usuário:
- Pedir "gerar referência ABNT"
- Informar dados de livro, artigo, site etc. e pedir formatação
- Pedir "citação" no formato ABNT
- Enviar uma referência já pronta e pedir "validar se está no padrão ABNT"

## Diferenciais

1. **Detecção automática de tipo** — O usuário só joga os dados, a skill identifica se é livro, artigo, site, tese etc.
2. **Saída dupla** — Gera tanto a referência completa (bibliografia) quanto a citação no formato autor-data entre parênteses.
3. **Validação de referências** — O usuário cola uma referência pronta e a skill valida se está no padrão ABNT, apontando erros.
4. **Export formatado** — Saída limpa, pronta pra copiar e colar no trabalho acadêmico.
5. **Interface em português** — Toda a comunicação e explicação em português brasileiro.
6. **Suporte a +10 tipos de fonte** — Livro, artigo de periódico, site/blog, tese/dissertação, legislação, anais de evento, patente, norma técnica, entrevista, vídeo online, imagem, música.

## Workflow

### Modo 1: Gerar referência do zero

1. Perguntar o tipo de fonte (ou tentar detectar automaticamente).
2. Coletar os campos necessários de acordo com o tipo:
   - **Livro:** autor(es), título, edição, cidade, editora, ano
   - **Artigo:** autor(es), título do artigo, título do periódico, volume, número, páginas, ano
   - **Site:** autor(es), título, nome do site, data de publicação, URL, data de acesso
   - **Tese:** autor, título, tipo (tese/dissertação), grau, instituição, ano
   - **Lei:** número, data, ementa, diário oficial, data de publicação
   - (demais tipos seguem a ABNT NBR 6023)
3. Gerar a referência formatada + citação autor-data.
4. Oferecer validação se o usuário quiser conferir.

### Modo 2: Validar referência existente

1. Usuário cola uma referência.
2. Extrair os elementos e verificar:
   - Pontuação correta (ponto, vírgula, dois-pontos nos lugares certos)
   - Ordem dos elementos
   - Itálico/negrito indicado para o título
   - Destaque do sobrenome do autor em CAIXA ALTA
3. Retornar a referência corrigida com os problemas apontados.

### Modo 3: Citação rápida

1. Usuário informa autor + ano (e opcionalmente página).
2. Gerar citação no formato:
   - Parentética: (SOBRENOME, Ano, p. X)
   - Narrative: SOBRENOME (Ano, p. X)

## Formatos de Saída

### Referência Completa (Bibliografia)

```
SOBRENOME, Nome. **Título do livro: subtítulo**. Edição. Cidade: Editora, ano.
```

Exemplo:
```
ECO, Umberto. **Como se faz uma tese**. 25. ed. São Paulo: Perspectiva, 2014.
```

### Citação (Autor-Data)

```
(ECO, 2014, p. 45)
```

## Regras de Formatação ABNT NBR 6023

- **Sobrenome do autor:** em CAIXA ALTA
- **Título da obra:** em **negrito** (indicado com ** ))
- **Edição:** a partir da 2ª edição (ex: "2. ed.")
- **Local:** seguido de dois-pontos
- **Editora:** seguida de vírgula
- **Ano:** ponto final no fim

## Notes

- Se o usuário não especificar o tipo, pergunte primeiro ou tente inferir pelos dados fornecidos.
- Para sites, sempre exija a data de acesso (obrigatório na ABNT).
- Para livros estrangeiros, pergunte se quer ABNT adaptado ou tradução livre.
- Mantenha o tom acadêmico mas direto — sem firula.
- WhatsApp-friendly: use bullet lists e formatação simples (sem tabelas markdown).

---
⭐ *Gostou desta skill?* Deixe uma estrela no [ClawHub](https://clawhub.ai) para ajudar outros a encontrá-la!
