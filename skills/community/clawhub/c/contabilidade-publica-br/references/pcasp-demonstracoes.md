# PCASP e Demonstrações Contábeis do Setor Público

## PCASP — Plano de Contas Aplicado ao Setor Público

### Estrutura de Classes

| Classe | Natureza | Descrição |
|---|---|---|
| **1** | Devedora | Ativo |
| **2** | Credora | Passivo e PL |
| **3** | Devedora | Variações Patrimoniais Diminutivas (VPD) |
| **4** | Credora | Variações Patrimoniais Aumentativas (VPA) |
| **5** | Devedora | Controles da aprovação do planejamento e orçamento |
| **6** | Credora | Controles da execução do planejamento e orçamento |
| **7** | Devedora | Controles devedores (compensação) |
| **8** | Credora | Controles credores (compensação) |

### Natureza da informação

- **Classes 1-4**: Informação patrimonial
- **Classes 5-6**: Informação orçamentária
- **Classes 7-8**: Informação de controle (compensação)

### Codificação (9 dígitos)

```
X . X . X . X . X . XX . XX
│   │   │   │   │    │    └── 7º nível: Subitem
│   │   │   │   │    └────── 6º nível: Item
│   │   │   │   └─────────── 5º nível: Subtítulo
│   │   │   └──────────────── 4º nível: Título
│   │   └───────────────────── 3º nível: Subgrupo
│   └────────────────────────── 2º nível: Grupo
└─────────────────────────────── 1º nível: Classe
```

### Contas mais utilizadas (Legislativo Municipal)

#### Ativo (Classe 1)
- 1.1.1.1.1.xx.xx — Caixa e Equivalentes de Caixa
- 1.1.2.1.x.xx.xx — Créditos a Curto Prazo (duodécimos a receber)
- 1.1.3.x.x.xx.xx — Estoques (almoxarifado)
- 1.2.3.x.x.xx.xx — Imobilizado (bens móveis e imóveis)
- 1.2.4.x.x.xx.xx — Intangível (software)

#### Passivo (Classe 2)
- 2.1.1.x.x.xx.xx — Obrigações trabalhistas a pagar
- 2.1.2.x.x.xx.xx — Fornecedores a pagar
- 2.1.3.x.x.xx.xx — Obrigações fiscais a pagar (INSS, FGTS, IRRF)
- 2.1.8.x.x.xx.xx — Valores restituíveis (consignações)

#### VPD (Classe 3) — Despesas sob enfoque patrimonial
- 3.1.1.x.x.xx.xx — Pessoal e encargos
- 3.1.2.x.x.xx.xx — Benefícios previdenciários e assistenciais
- 3.3.1.x.x.xx.xx — Uso de bens, serviços e consumo de capital fixo
- 3.3.2.x.x.xx.xx — Depreciação, amortização e exaustão

#### VPA (Classe 4) — Receitas sob enfoque patrimonial
- 4.1.1.x.x.xx.xx — Impostos, taxas e contribuições
- 4.5.1.x.x.xx.xx — Transferências recebidas (duodécimos)

---

## Demonstrações Contábeis Obrigatórias (MCASP 10ª ed.)

### 1. Balanço Orçamentário (BO)
**Finalidade:** Demonstrar receitas e despesas previstas/fixadas versus arrecadadas/executadas.

**Estrutura:**
- Receita: prevista → atualizada → arrecadada → diferença
- Despesa: fixada → atualizada → empenhada → liquidada → paga → diferença
- Resultado orçamentário: superávit ou déficit

**Fundamento:** Art. 102, Lei 4.320/64; MCASP Parte V

**Alertas de consistência:**
- Receita arrecadada – Despesa empenhada = Resultado orçamentário do exercício
- O resultado NÃO inclui restos a pagar (estes são extraorçamentários)

### 2. Balanço Financeiro (BF)
**Finalidade:** Demonstrar ingressos e dispêndios orçamentários e extraorçamentários, conjugados com saldo anterior e posterior de caixa.

**Estrutura:**
- Ingressos orçamentários (receita arrecadada)
- Ingressos extraorçamentários (RP inscritos, consignações)
- Dispêndios orçamentários (despesa paga)
- Dispêndios extraorçamentários (RP pagos, devoluções)
- Saldo anterior e posterior de caixa

**Fundamento:** Art. 103, Lei 4.320/64

**Equação fundamental:**
Saldo anterior + Ingressos = Dispêndios + Saldo posterior

### 3. Balanço Patrimonial (BP)
**Finalidade:** Demonstrar a situação patrimonial (ativo, passivo e PL).

**Estrutura:**
- Ativo circulante e não circulante
- Passivo circulante e não circulante
- Patrimônio líquido (resultados acumulados, reservas)
- Quadro dos ativos e passivos financeiros e permanentes (compensação)
- Quadro das contas de compensação

**Fundamento:** Art. 105, Lei 4.320/64; NBC TSP 11

### 4. Demonstração das Variações Patrimoniais (DVP)
**Finalidade:** Demonstrar VPA e VPD, apurando o resultado patrimonial.

**Estrutura:**
- VPA: receitas sob enfoque patrimonial (independente de arrecadação)
- VPD: despesas sob enfoque patrimonial (independente de pagamento)
- Resultado patrimonial: superávit ou déficit

**Fundamento:** Art. 104, Lei 4.320/64

**Diferença importante:** O resultado patrimonial (DVP) ≠ resultado orçamentário (BO). Um pode ser superavitário enquanto o outro é deficitário.

### 5. Demonstração dos Fluxos de Caixa (DFC)
**Finalidade:** Demonstrar entradas e saídas de caixa por atividade.

**Atividades:**
- **Operacionais**: receitas e despesas correntes
- **Investimento**: aquisição/alienação de ativos não circulantes
- **Financiamento**: operações de crédito, amortização de dívidas

**Fundamento:** NBC TSP 12; MCASP Parte V

### 6. Demonstração das Mutações do Patrimônio Líquido (DMPL)
**Finalidade:** Demonstrar a evolução do PL no exercício.

**Obrigatória apenas para:** Empresas estatais dependentes e entes que optem por elaborá-la.

**Fundamento:** MCASP Parte V

### 7. Notas Explicativas
**Finalidade:** Informações complementares às demonstrações.

**Conteúdo mínimo:**
- Bases de elaboração e políticas contábeis
- Critérios de avaliação de ativos e passivos
- Composição de contas relevantes
- Eventos subsequentes ao encerramento

**Fundamento:** NBC TSP 11; MCASP Parte V
