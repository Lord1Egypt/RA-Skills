# Rapport Bibliotecário Heartbeat

A biblioteca é acessada através do skill calibre-ebooks.

## Periodic Tasks

- Monitorar pasta de biblioteca para novos livros
- Verificar status de processamento na fila
- Reportar estatísticas da biblioteca
- Verificar disponibilidade de serviços (PostgreSQL, Ollama, WhatsApp, Telegram)
- Limpar notificações antigas
- Gerar resumo diário das discussões, temas e livros solicitados no grupo para entrega no início da noite.
- Gerar resumo diário das discussões, temas e livros solicitados no grupo para entrega no início da noite.
- Gerar resumo diário das discussões, temas e livros solicitados no grupo para entrega no início da noite (por volta das 20:00).
- Quando o grupo autorizado estiver muito parado durante horario ativo, puxar
  uma conversa literaria curta a partir de um livro sorteado/selecionado da
  biblioteca confirmada pelo skill `calibre-ebooks`.

## Health Checks

- Conexão com PostgreSQL
- Disponibilidade do Ollama
- Status do WhatsApp API
- Status do Telegram Bot
- Espaço em disco para processamento
- Status da fila de processamento

## Status Reporting

Relatar periodicamente:
- Número de livros na biblioteca
- Livros processados para RAG
- Livros na fila de processamento
- Status dos serviços de notificação
- Último horário de varredura da biblioteca
- Status da conexão com o banco de dados
- Número de livros indexados
- Status da fila de processamento RAG

## Debate de Livro em Grupo Parado

Use somente quando o contexto do heartbeat ou historico recente indicar que o
grupo esta sem movimento relevante por algumas horas. Nao force conversa se ja
houver debate ativo.

Antes de publicar:

- Confirme um livro real da biblioteca pelo skill `calibre-ebooks`.
- Selecione ou sorteie apenas entre livros confirmados; nao invente titulo,
  autor, disponibilidade, resumo ou link.
- Publique uma mensagem curta, sem detalhes operacionais, com titulo e autor
  quando disponivel.
- Faca 1 ou 2 perguntas abertas sobre o livro para provocar leitura e debate:
  ideias centrais, personagens, estilo, contexto, impacto ou trecho marcante.
- Convide os membros a lerem ou comentarem, sem cobrar resposta individual.
- Evite repeticao: no maximo uma provocacao por ciclo relevante de inatividade.

## Segurança de publicação

- Heartbeat so deve gerar mensagem publica quando houver resultado efetivo,
  util e concluido para o usuario ou grupo.
- Nunca publique saida bruta de comandos, listagens de arquivos, paths internos,
  logs, stack traces, mensagens de aprovacao, sandbox/runtime ou estado de
  ferramentas em WhatsApp, Telegram ou grupos.
- Antes de enviar qualquer mensagem publica, valide somente o texto final que
  sera visto pelo usuario ou grupo. Se ele contiver raciocinio interno, plano de
  acao, nomes de ferramentas, parametros como `sessionKey`/`chat_id`, IDs de
  grupo, JSON, paths, comandos, heartbeat, estado operacional ou tentativa/falha
  de execucao, nao envie; registre apenas localmente.
- Se uma tarefa falhar, ficar incompleta ou depender de diagnostico tecnico,
  registre apenas em memoria para recuperar no proximo heartbeat quando
  possivel. Nao envie aviso publico, diagnostico tecnico nem status sanitizado
  de falha.

Run library scans every 2-4 hours during active hours (08:00-22:00).
