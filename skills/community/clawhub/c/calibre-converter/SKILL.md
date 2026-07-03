# Calibre Converter

Use este skill sempre que o usuário pedir para converter um livro, e-book ou documento já cadastrado no Calibre para outro formato. Acione também quando o usuário mencionar conversão para formatos como `epub`, `mobi`, `azw3`, `pdf`, `docx`, `txt`, `html`, `rtf`, `fb2`, `lit`, `lrf`, `pdb`, `rb`, `snb`, `tcr` ou qualquer outro formato suportado pelo Calibre.

O objetivo deste skill é receber a intenção do usuário, identificar o livro de forma única e pedir ao `calibre-openclaw-server` que faça toda a operação. O skill não deve executar `ebook-convert` nem `calibredb` diretamente.

## Responsabilidade do skill

- Entender qual livro o usuário quer converter.
- Identificar o livro por `book_id`, `calibre_id` ou pelo título exato quando o título identificar um único cadastro.
- Entender o formato de destino solicitado.
- Chamar o endpoint do `calibre-openclaw-server`.
- Informar ao usuário o resultado retornado pelo servidor.

## Responsabilidade do calibre-openclaw-server

- Localizar o livro no catálogo pelo ID ou pelo título exato.
- Escolher o arquivo de origem disponível no cadastro do Calibre.
- Executar a conversão com as ferramentas do Calibre.
- Cadastrar o novo formato no Calibre.
- Sincronizar o estado do servidor com a biblioteca.
- Retornar ao skill o status, mensagem, livro identificado, formato gerado e caminho cadastrado.

## Quando usar

- O usuário pede para converter um livro de um formato para outro.
- O usuário fornece o título exato ou o ID do livro e solicita um formato final específico.
- O usuário quer preparar um e-book para Kindle, Kobo, celular, tablet ou outro leitor.
- O usuário quer que o novo formato fique cadastrado na biblioteca do Calibre.
- O usuário menciona Calibre, `calibre-openclaw-server`, conversão de e-book ou cadastro de novo formato.

## Endpoint esperado

O skill deve chamar:

```http
POST /api/books/convert-format
```

Payload:

```json
{
  "book_id": 123,
  "calibre_id": 456,
  "title": "Título exato do livro",
  "target_format": "epub",
  "source_format": "pdf",
  "force": false
}
```

Regras do payload:

- Envie apenas um identificador principal quando possível: `book_id`, `calibre_id` ou `title`.
- Use `title` somente quando o usuário fornecer o título exato ou quando uma busca anterior confirmar um único livro.
- `target_format` é obrigatório.
- `source_format` é opcional e só deve ser usado quando o usuário pedir ou quando houver necessidade técnica clara.
- `force` deve ficar `false` por padrão. Use `true` apenas quando o usuário pedir para substituir/regerar um formato que já existe.

Resposta esperada:

```json
{
  "success": true,
  "message": "Converted and registered EPUB for book 456.",
  "book_id": 123,
  "calibre_id": 456,
  "title": "Título exato do livro",
  "source_format": "PDF",
  "target_format": "EPUB",
  "output_path": "/caminho/para/o/livro.epub",
  "already_available": false,
  "registered": true,
  "synced_count": 1
}
```

## Script de apoio

Use o script `scripts/calibre_converter_client.py` quando precisar chamar o servidor pela linha de comando:

```bash
python3 scripts/calibre_converter_client.py --calibre-id 456 --target-format epub
```

Também é possível identificar por título exato:

```bash
python3 scripts/calibre_converter_client.py --title "Título exato do livro" --target-format azw3
```

Variáveis de ambiente suportadas:

- `CALIBRE_OPENCLAW_SERVER_URL`: URL base do servidor. Padrão: `http://127.0.0.1:6180`.
- `CALIBRE_OPENCLAW_API_KEY`: chave usada no cabeçalho `Authorization: Bearer`.

O script carrega automaticamente o arquivo `.env` da raiz deste skill antes de ler essas variáveis. Variáveis já exportadas no ambiente têm prioridade sobre o `.env`.

## Regras de comportamento

- Se o usuário especificar o formato de saída, use exatamente esse formato.
- Se o usuário não especificar formato, pergunte qual formato deseja antes de chamar o servidor.
- Se o usuário mencionar Kindle sem especificar formato, prefira `azw3`, salvo se ele pedir explicitamente `mobi`, `epub` ou `pdf`.
- Se o usuário mencionar Kobo, Apple Books ou leitura geral em e-readers, prefira `epub` quando o formato não for especificado.
- Se houver mais de um livro com o mesmo título, não escolha sozinho: peça o ID ou uma confirmação do livro correto.
- Não prometa que a conversão foi feita antes de receber sucesso do servidor.
- Ao final, informe o título, formato gerado e caminho retornado pelo servidor.

## Observações

Conversões de PDF para EPUB podem exigir ajustes manuais de layout, sumário e quebras de página. Quando a qualidade do resultado for importante, recomende revisar o arquivo convertido no Calibre ou em um leitor compatível.
