---
name: "expense-report"
description: "Gera relatórios de despesas estruturados a partir de descrições de recibos, notas fiscais ou gastos do dia a dia."
metadata:
  - finance
  - expense
  - report
  - productivity
  - receipt
  - business
allowed-tools:
  - read
  - write
user-invocable: true
---

# Expense Report Generator 💰📋

Transforma descrições soltas de gastos em relatórios de despesas profissionais, organizados por categoria, com totais e resumo executivo.

## Público-Alvo

Profissionais autônomos, PJs, freelancers, estagiários, vendedores externos — qualquer um que precise prestar contas de gastos.

## Trigger

Invocar quando o usuário:
- Falar "gerar relatório de despesas"
- Enviar uma lista de gastos
- Pedir "organizar meus gastos"
- Pedir "quanto gastei esse mês/semana"
- Enviar textos de notas fiscais ou recibos

## Diferenciais

1. **Auto-categorização inteligente** — Identifica automaticamente a categoria de cada gasto (alimentação, transporte, material, hospedagem, etc.)
2. **Múltiplas moedas** — Suporta BRL (R$) e USD (US$) com conversão se informada a cotação.
3. **Dois estilos de relatório** — Simplificado (rápido, para WhatsApp) e Completo (formal, para prestação de contas).
4. **Totais por categoria + geral** — Soma automática com quebra por categoria.
5. **Reembolsável vs Pessoal** — O usuário marca o que é reembolsável, a skill separa.
6. **Detecção de data** — Se o usuário não informar data, usa a data atual ou pergunta.

## Workflow

### Entrada

O usuário pode fornecer os gastos de várias formas:

**Forma 1: Lista simples**
```
almoço com cliente R$ 45,00
uber até o escritório R$ 32,50
material de escritório R$ 120,00
jantar R$ 67,00
pedágio R$ 12,00
```

**Forma 2: Estruturada**
```
Data: 10/06 - Almoço com cliente - R$ 45,00 - reembolsável
Data: 11/06 - Uber escritório - R$ 32,50 - pessoal
```

**Forma 3: Mista (alguns com data, outros sem)**

### Processamento

1. Receber a lista de gastos.
2. Para cada item:
   - Extrair valor (R$ ou US$)
   - Extrair descrição
   - Extrair data (se presente)
   - Classificar categoria automaticamente
   - Marcar reembolsável/pessoal (se informado, senão perguntar ou assumir reembolsável)
3. Agrupar por categoria.
4. Calcular totais.
5. Gerar relatório.

### Categorias Automáticas

| Categoria | Exemplos |
|-----------|----------|
| 🍽️ Alimentação | Restaurante, ifood, lanche, café, jantar, almoço |
| 🚗 Transporte | Uber, táxi, gasolina, pedágio, estacionamento, passagem |
| 📦 Material | Papelaria, material de escritório, software |
| 🏨 Hospedagem | Hotel, Airbnb, hostel |
| 🛒 Compras | Qualquer compra não classificada acima |
| 🏥 Saúde | Farmácia, médico, exame |
| 📡 Comunicação | Internet, telefone, recarga |
| 💼 Serviços | Freela pago, ferramenta, assinatura |

Se não encaixar em nenhuma, usar "Outros".

## Saída

### Relatório Simplificado (WhatsApp-friendly)

```
📋 *RELATÓRIO DE DESPESAS*
📅 Período: 10/06/2026 a 15/06/2026

🍽️ Alimentação: R$ 112,00
🚗 Transporte: R$ 44,50
📦 Material: R$ 120,00
💰 *Total: R$ 276,50*

💼 Reembolsável: R$ 165,00
👤 Pessoal: R$ 111,50

📌 *Detalhes:*
10/06 - Almoço cliente - R$ 45,00 🍽️ ✅
11/06 - Uber escritório - R$ 32,50 🚗 ❌
13/06 - Material escritório - R$ 120,00 📦 ✅
14/06 - Jantar - R$ 67,00 🍽️ ❌
14/06 - Pedágio - R$ 12,00 🚗 ✅
```

### Relatório Completo (para prestação de contas formal)

Inclui:
- Cabeçalho com nome do responsável e período
- Tabela detalhada (data, descrição, categoria, valor, reembolsável)
- Resumo por categoria
- Total geral
- Legenda (✅ reembolsável | ❌ pessoal)
- Assinatura eletrônica: "Gerado por Expense Report Generator em [data]"

## Notes

- Valores sem moeda explícita → assumir R$.
- Datas no formato DD/MM/AAAA ou DD/MM.
- Se o mês não for informado, assumir mês atual.
- Se o usuário disser "pessoal" ou "meu" na descrição, marcar como não reembolsável.
- Para números grandes (>20 itens), sugerir agrupar por semana.
- Emails-friendly: oferecer saída em formato de email formal.

---
⭐ *Gostou desta skill?* Deixe uma estrela no [ClawHub](https://clawhub.ai) para ajudar outros a encontrá-la!
