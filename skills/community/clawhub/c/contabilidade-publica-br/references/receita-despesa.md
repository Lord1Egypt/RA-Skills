# Receita e Despesa Orçamentária

## Receita Orçamentária

### Classificação por categoria econômica
- **Receitas Correntes** (código 1): tributária, contribuições, patrimonial, agropecuária, industrial, serviços, transferências correntes, outras
- **Receitas de Capital** (código 2): operações de crédito, alienação de bens, amortização de empréstimos, transferências de capital, outras

### Codificação da natureza (8 dígitos)
```
C . O . EE . DD . TT . SS
│   │    │    │    │    └── Subtipo
│   │    │    │    └─────── Tipo
│   │    │    └──────────── Desdobramento
│   │    └───────────────── Espécie
│   └────────────────────── Origem
└────────────────────────── Categoria econômica
```

### Estágios da receita
1. **Previsão** — estimativa constante da LOA
2. **Lançamento** — identificação do devedor e valor (art. 53, Lei 4.320)
3. **Arrecadação** — pagamento pelo contribuinte ao agente arrecadador
4. **Recolhimento** — transferência dos valores ao caixa do Tesouro

### Receitas do Legislativo Municipal
- **Receita própria**: taxas de serviço (cópias, certidões) — rara
- **Transferência intragovernamental**: duodécimo (repasse do Executivo)
  - Limite: art. 29-A CF — 7% da RCL do Município (pop ≤ 100 mil)
  - Limite: art. 29-A CF — 6% da RCL do Município (pop > 100 mil a 300 mil)
  - Limite: art. 29-A CF — 5% da RCL do Município (pop > 300 mil a 500 mil)

### Deduções da receita
- Renúncia de receita (art. 14 LRF) — exige estimativa de impacto e medida compensatória
- FUNDEB (20% de transferências constitucionais)
- Restituições

---

## Despesa Orçamentária

### Classificação institucional
Identifica o órgão e a unidade orçamentária responsável.
Ex.: 01.001 — Câmara Municipal / Gabinete da Presidência

### Classificação funcional (Portaria SOF 42/1999)
- **Função** (2 dígitos): área de atuação (ex.: 01-Legislativa)
- **Subfunção** (3 dígitos): detalhamento (ex.: 031-Ação Legislativa)

### Classificação por natureza da despesa
```
C . GG . MM . EE . DD
│    │    │    │    └── Desdobramento do elemento
│    │    │    └─────── Elemento de despesa (ND)
│    │    └──────────── Modalidade de aplicação
│    └───────────────── Grupo de natureza da despesa
└────────────────────── Categoria econômica
```

#### Categoria econômica
- **3** — Despesas Correntes
- **4** — Despesas de Capital

#### Grupo de natureza da despesa
| Grupo | Descrição |
|---|---|
| 1 | Pessoal e encargos sociais |
| 2 | Juros e encargos da dívida |
| 3 | Outras despesas correntes |
| 4 | Investimentos |
| 5 | Inversões financeiras |
| 6 | Amortização da dívida |

#### Elementos de despesa mais comuns (Legislativo)
| Código | Elemento |
|---|---|
| 11 | Vencimentos e vantagens fixas |
| 13 | Obrigações patronais (INSS, FGTS) |
| 14 | Diárias |
| 30 | Material de consumo |
| 33 | Passagens e locomoção |
| 35 | Serviços de consultoria |
| 36 | Outros serviços de terceiros — PF |
| 39 | Outros serviços de terceiros — PJ |
| 40 | Serviços de TI e comunicação |
| 46 | Auxílio-alimentação |
| 47 | Obrigações tributárias e contributivas |
| 51 | Obras e instalações |
| 52 | Equipamentos e material permanente |

### Estágios da despesa

#### 1. Fixação
Autorização legislativa na LOA. Créditos adicionais: suplementar, especial, extraordinário.

#### 2. Empenho (art. 58-60, Lei 4.320)
Ato emanado de autoridade competente que cria para o Estado obrigação de pagamento.

**Tipos:**
- **Ordinário**: valor exato e pagamento único
- **Estimativo**: valor estimado (ex.: água, energia)
- **Global**: valor determinado com pagamento parcelado (ex.: contratos)

**Regra de ouro:** Não pode empenhar além do crédito disponível (art. 59).

#### 3. Liquidação (art. 63, Lei 4.320)
Verificação do direito adquirido pelo credor com base em:
- Contrato, ajuste ou acordo
- Nota de empenho
- Comprovantes de entrega (NF, atesto)

#### 4. Pagamento (art. 64-65, Lei 4.320)
Despacho da autoridade competente + ordem de pagamento.
Só pode pagar despesa liquidada (exceção: adiantamento/suprimento de fundos).

### Despesa com pessoal — detalhamento LRF

**Composição (art. 18 LRF):**
- Ativos, inativos e pensionistas
- Vencimentos e vantagens fixas
- Subsídios
- Gratificações, adicionais, horas extras
- Encargos sociais (INSS patronal, FGTS)
- Contribuição ao RPPS
- Outras despesas de pessoal (terceirização com substituição de servidores)

**NÃO compõem despesa com pessoal:**
- Indenizações por demissão e rescisões
- Diárias
- Auxílio-alimentação (quando indenizatório)

---

## Restos a Pagar

### Conceito (art. 36, Lei 4.320)
Despesas empenhadas mas não pagas até 31/12 do exercício.

### Classificação
| Tipo | Critério |
|---|---|
| **Processados (RPP)** | Empenhados E liquidados, não pagos |
| **Não processados (RPNP)** | Empenhados, NÃO liquidados |

### Regras LRF
- Art. 42: nos últimos 2 quadrimestres do mandato, vedado contrair obrigação sem disponibilidade de caixa
- RPNP sem disponibilidade = irregularidade fiscal
- Cancelamento: por ato do gestor ou prescrição (5 anos)

### Escrituração
- Inscrição: D-6.3.x (Controle) / C-6.3.x (Controle)
- Pagamento: D-2.1.x (Passivo) / C-1.1.1 (Caixa)
- Cancelamento: D-2.1.x (Passivo) / C-4.x.x (VPA)
