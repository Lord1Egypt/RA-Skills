# Football Tracker - Pacote de Saída em Português

Use este pacote quando o usuário pedir saída em português ou o agente estiver operando em pt-BR.

## Estrutura da saída

- ⚽ Time
- 🏟️ Último jogo
- 📅 Próxima partida
- 📺 Transmissão
- 🏆 Campeonato
- 📊 Posição
- 📰 Últimas notícias

## Regras

- Manter o formato curto e com emojis.
- Se a transmissão não for encontrada, mostrar `Indisponível`.
- Para seleções da Copa do Mundo 2026, traduzir o nome do time para pt-BR quando a saída estiver em português.
- Se a localização da próxima partida estiver na base interna, exibir estado/cidade com `🏟️`; se não houver confiança, mostrar `Indisponível` e não adivinhar.
- A tabela/posição deve aparecer sempre antes do bloco de notícias.
- Para a Copa do Mundo 2026, o horário deve ficar embutido na linha da próxima partida, sem um campo separado de horário.
- Se os dados do time forem incertos, manter `N/A` nos campos faltantes e ainda trazer notícias.
- Priorizar notícias recentes, específicas de futebol e com fonte identificada.
