# Fluxos práticos em PT-BR

## Atualizar sobre o status de um projeto

Prompt exemplo:
- `Me atualize sobre o status do projeto X no flow`

Fluxo:
1. Rodar `python3 scripts/flowboard_status.py "X"`
2. Se houver match claro, usar o campo `brief` como resposta base
3. Se precisar aprofundar, usar `summary` para detalhar:
   - status do projeto
   - prazo, se existir
   - cycle atual
   - quantidade ou panorama das tasks
   - riscos ou pendências óbvias
4. Se houver ambiguidade, pedir confirmação curta ao usuário

## Verificar o cycle atual

Prompt exemplo:
- `Verifique o status do cycle atual do projeto X`

Fluxo:
1. Resolver o projeto
2. Rodar `python3 scripts/flowboard_lookup.py active-cycle <project_id>`
3. Se existir cycle ativo, resumir progresso, datas, escopo e escopo concluído
4. Se não existir, avisar claramente e citar o último cycle disponível se útil

## Criar task

Prompt exemplo:
- `Crie uma nova task no flow para implementar login social no projeto Portal`

Fluxo:
1. Resolver o projeto
2. Extrair do prompt o máximo possível: título, descrição, prioridade, tipo, prazo, cycle
3. Pedir só o mínimo faltante
4. Criar via `POST /projects/{projectId}/tasks`
5. Confirmar com identificador gerado, título e status final

## Implementar a task do Flow

Prompt exemplo:
- `Vamos implementar o que está na task PRJ-42 do projeto Portal`

Fluxo:
1. Resolver projeto
2. Resolver task por identifier ou título com `flowboard_lookup.py task`
3. Buscar a task completa
4. Traduzir a task para um brief de implementação:
   - objetivo
   - escopo
   - restrições
   - critérios implícitos
5. Executar o trabalho pedido
6. Ao final, sugerir atualização de status no Flow se fizer sentido

## Ambiguidade

Se houver múltiplos matches próximos:
- não inventar
- listar 2 a 5 opções com nome, ID e sinal distintivo
- pedir confirmação curta

## Segurança em mutações destrutivas

Antes de deletar project, cycle ou task:
- confirmar explicitamente, a menos que o usuário já tenha pedido isso sem ambiguidade
