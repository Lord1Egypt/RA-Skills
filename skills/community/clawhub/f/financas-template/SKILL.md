# Skill Finanças - Template (Genérica)

Gerenciamento financeiro pessoal com registro por categorias, processamento de extratos/faturas e resumos mensais/anuais.

## Triggers (Ativação Automática)

Esta skill é ativada automaticamente quando o usuário usar palavras-chave relacionadas a finanças:

**Registro de gastos/receitas:**
- "gastei", "paguei", "comprei", "compre", "gasto", "pagamento"
- "recebi", "entrar", "receita", "renda"
- "aluguel", "luz", "água", "internet", "celular", "conta"

**Consultas de resumo:**
- "resumo", "resumir", "balanço", "saldo"
- "quanto gastei", "total", "acumulado"
- "de [mês]", "em [mês]", "[mês] 2026"

**Processamento de arquivos:**
- "fatura", "extrato", "cartão", "banco"

**Categorias financeiras:**
- "alimentação", "mercado", "restaurante", "comida"
- "transporte", "gasolina", "pedágio", "uber"
- "lazer", "cinema", "show", "festa"
- "saúde", "farmácia", "médico"
- "compras", "roupas", "presente"

## Descrição

Skill para gerenciar finanças pessoais, incluindo registro diário de gastos em linguagem natural, processamento de extratos bancários e faturas de cartão, e geração de resumos mensais e anuais.

## Como Funciona

Esta skill é um **conjunto de instruções** que guia a agente quando você faz perguntas ou comandos relacionados a finanças.

**Fluxo de execução:**
1. Você fala algo que ativa um trigger (ex: "gastei 50 no iFood")
2. A agente detecta que é sobre finanças
3. A agente carrega esta skill como guia
4. A agente **segue as instruções**:
   - Lê os arquivos financeiros do workspace
   - Interpreta sua solicitação
   - Faz os cálculos ou registros conforme as regras
   - Atualiza os arquivos se necessário

## Estrutura de Arquivos

```
workspace/financas/
├── 2026-MM.md          # Arquivo mensal (MM = 01, 02, ..., 12)
├── resumo-anual.md     # Consolidado anual
└── metas.md           # Metas financeiras
```

### Formato do Arquivo Mensal

```markdown
# Finanças - Mês 2026

## 📊 Resumo do Mês

| Categoria | Total |
|-----------|-------|
| Receitas | R$ 0,00 |
| Despesas Fixas | R$ 0,00 |
| Parcelamentos | R$ 0,00 |
| Gastos Variáveis | R$ 0,00 |
| **Total Despesas** | **R$ 0,00** |
| **Saldo** | **R$ 0,00** |

---

## 💰 Receitas

| Dia | Data | Descrição | Tipo | Valor | Status | Obs |
|-----|------|-----------|------|-------|--------|-----|

---

## 🏠 Despesas Fixas

| Dia | Vencimento | Descrição | Categoria | Valor | Status | Obs |
|-----|------------|-----------|-----------|-------|--------|-----|

---

## 📦 Parcelamentos

| Dia | Vencimento | Descrição | Parcela | Vl.Parcela | Vl.Total | Status | Obs |
|-----|------------|-----------|---------|------------|----------|--------|-----|

---

## 💸 Gastos Variáveis

| Dia | Data | Descrição | Categoria | Valor | Status | Obs |
|-----|------|-----------|-----------|-------|--------|-----|
```

## Categorias Válidas

### Despesas Fixas
- Moradia
- Energia
- Água
- Internet
- Celular
- Streaming
- Outras Fixas

### Gastos Variáveis
- Alimentação
- Transporte
- Lazer
- Saúde
- Educação
- Compras Pessoais
- Outros

### Receitas
- Salário / Renda Principal
- Rendas Extras

## Fluxo de Trabalho

### 1. Registro Diário (Linguagem Natural)

O usuário informa gastos em linguagem natural, por exemplo:
- "Gastei 350 no Shibata no cartão Santander"
- "Paguei o aluguel de 1500"
- "Recebi meu salário de 8000"
- "Comprei um fone de 300 em 3x no C6"
- "Almocei no Habib's por 45 reais"

**Processo:**
1. Interpretar a frase e classificar (tipo de transação, categoria, valor, data, forma de pagamento)
2. Mostrar resumo ao usuário para confirmação
3. Se aprovado, registrar no arquivo do mês atual
4. Atualizar o resumo do mês
5. Atualizar o resumo anual se necessário

**Regras de interpretação:**
- Se o usuário não informar o mês, usar o mês atual
- Se não informar o dia, usar o dia atual
- Categoria deve ser inferida do contexto (ex: "iFood" → Alimentação)
- Forma de pagamento deve ser explicitada (Santander, C6, PIX, Débito, etc.)

### 2. Processamento de Extratos/Faturas

Quando o usuário enviar extratos bancários ou faturas de cartão:

**Fatura de Cartão (PDF/CSV):**
- Contém APENAS compras no crédito (maquininha, link de pagamento, apps, online)
- NUNCA assumir que transações de fatura são PIX
- Transações com nomes de pessoas são cobranças via link/maquininha, NÃO PIX
- Descrição deve refletir o que aparece na fatura
- **IMPORTANTE:** Faturas de "março" podem conter transações de JAN e FEV (ciclo de cobrança)
- Registrar cada transação no mês REAL da compra, não no mês da fatura

**Extrato Bancário (PDF/CSV):**
- Contém PIX, transferências, débito automático, boletos
- Somente registrar PIX quando fornecido o EXTRATO BANCÁRIO
- Não misturar dados de fatura de cartão com dados de extrato bancário

**Processo:**
1. Ler/interpretar o arquivo
2. Crie uma tabela resumo com as transações
3. Verificar duplicatas com dados existentes (comparar valor + data + mês)
4. Mostrar resumo ao usuário para confirmação
5. Se aprovado, registrar nas seções adequadas
6. Atualizar resumos

### 3. Consultas

Só exibir resumos quando o usuário pedir:
- "Me mostra o resumo de abril"
- "Quanto gastei em alimentação esse mês?"
- "Qual o saldo atual?"

## Regras de Ouro

### Registro
- ✅ UMA LINHA POR COMPRA (nunca agrupar compras diferentes)
- ✅ Descrição = nome REAL do estabelecimento (ex: "Supermercado Shibata", "Atacadão 635")
- ✅ NUNCA usar descrições genéricas como "Mercado", "Barbearia", "Coisas pra casa"
- ✅ Coluna Observações (Obs) SEMPRE com forma de pagamento (Santander, C6, Débito, PIX, Dinheiro)
- ✅ Data da compra REAL no campo Data
- ✅ Formato da data: DD/MM/AAAA
- ✅ Status padrão: "Pago" para despesas, "Recebido" para receitas

### Prevenção de Duplicatas
- ANTES de registrar qualquer gasto, SEMPRE verificar se já existe
- Comparar VALOR + DATA + MÊS → se coincidem, é provável duplicata
- Entradas manuais genéricas podem ser duplicatas de transações de fatura
- NUNCA registrar entradas manuais genéricas se a fatura do cartão já foi processada
- Descrição SEM nome do estabelecimento + SEM cartão na coluna Obs = sinal de alerta
- Ao processar faturas, varrer dados existentes e ALERTAR sobre possíveis duplicatas

### Contexto Pessoal

**IMPORTANTE:** O contexto pessoal (nome, relacionamentos, valores fixos, etc.) deve estar no `USER.md` de cada agente, não nesta skill.

Esta skill é genérica e funciona para QUALQUER pessoa. Cada agente deve ter seu próprio contexto pessoal configurado.

## Comandos Disponíveis

### Registro
- `add-receita` - Registrar receita (salário, freelance, rendas extras)
- `add-fixa` - Registrar despesa fixa (aluguel, luz, água, internet, streaming)
- `add-parcelamento` - Registrar compra parcelada no cartão
- `add-variavel` - Registrar gasto variável (mercado, restaurante, uber, lazer)

### Consulta
- `view [mês]` - Visualizar dados de um mês específico
- `resumo` - Visualizar resumo anual
- `resumo [categoria] [mês]` - Visualizar total de uma categoria no mês

### Processamento
- `processar-fatura` - Processar fatura de cartão (PDF) e registrar compras
- `processar-extrato` - Processar extrato bancário (PDF/CSV)

## Formato de Confirmação

Antes de registrar qualquer transação, SEMPRE mostrar:

```
Interpretação:
- Tipo: Receita / Despesa Fixa / Parcelamento / Gasto Variável
- Categoria: [nome da categoria]
- Valor: R$ [valor]
- Descrição: [nome do estabelecimento]
- Data: [DD/MM/AAAA]
- Status: [Pago/Recebido]
- Obs: [forma de pagamento]

Confirma? [S/N]
```

## Atualização de Resumos

Após cada registro:
1. Atualizar tabela de resumo do mês atual
2. Atualizar `resumo-anual.md` se for necessário (alterar totais do mês)
3. Calcular saldos corretamente

## Notas Importantes

- **Nunca inventar dados** — se não tiver certeza, perguntar ao usuário
- **Sempre confirmar** antes de registrar
- **Verificar duplicatas** antes de cada novo registro
- **Usar descrições reais** dos estabelecimentos
- **Manter consistência** nos formatos (data, valor, status)
- **Contexto pessoal deve estar no USER.md do agente**, não nesta skill genérica
