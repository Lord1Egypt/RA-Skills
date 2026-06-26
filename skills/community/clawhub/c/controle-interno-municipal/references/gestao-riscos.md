# Gestão de Riscos no Setor Público Municipal

## Fundamento
- **IN Conjunta MP/CGU nº 01/2016** — controles internos e gestão de riscos no Executivo Federal (referência)
- **COSO ERM 2017** — framework internacional de gestão de riscos
- **NBC TSP** — menções a riscos nas normas contábeis do setor público
- **ISO 31000:2018** — gestão de riscos (referência)
- **TCU Acórdão 2.467/2013-Plenário** — recomenda adoção de gestão de riscos

## Conceitos

### Risco
Evento futuro e incerto que, caso ocorra, pode afetar negativamente os objetivos da instituição.

### Categorias de risco no setor público

| Categoria | Exemplos |
|---|---|
| **Operacional** | Falha em processos, erro humano, falta de capacitação |
| **Legal/Compliance** | Descumprimento de norma, irregularidade em licitação |
| **Financeiro/Orçamentário** | Indisponibilidade de caixa, frustração de receita |
| **Reputacional** | Notícia negativa, condenação pelo TCE, baixo PNTP |
| **Integridade** | Fraude, conflito de interesses, nepotismo |
| **Tecnológico** | Perda de dados, sistema fora do ar, ciberataque |

## Matriz de Riscos

### Classificação de probabilidade
| Nível | Descrição | Critério |
|---|---|---|
| 1 — Raro | Evento excepcional | Nunca ocorreu |
| 2 — Improvável | Pode ocorrer esporadicamente | Ocorreu 1-2x em 5 anos |
| 3 — Possível | Pode ocorrer eventualmente | Ocorreu algumas vezes |
| 4 — Provável | Esperado em algum momento | Ocorre com frequência |
| 5 — Quase certo | Ocorrerá certamente | Ocorre rotineiramente |

### Classificação de impacto
| Nível | Descrição | Critério |
|---|---|---|
| 1 — Insignificante | Sem impacto relevante | Sem dano financeiro/reputacional |
| 2 — Baixo | Impacto menor | Dano facilmente recuperável |
| 3 — Médio | Impacto moderado | Requer ação corretiva formal |
| 4 — Alto | Impacto significativo | Comprometimento de objetivos |
| 5 — Crítico | Impacto catastrófico | Responsabilização, multa TCE, inelegibilidade |

### Mapa de calor (Probabilidade × Impacto)

```
           IMPACTO →
        1    2    3    4    5
P  5 |  5 | 10 | 15 | 20 | 25 |  ← Quase certo
R  4 |  4 |  8 | 12 | 16 | 20 |  ← Provável
O  3 |  3 |  6 |  9 | 12 | 15 |  ← Possível
B  2 |  2 |  4 |  6 |  8 | 10 |  ← Improvável
.  1 |  1 |  2 |  3 |  4 |  5 |  ← Raro
```

**Faixas de risco:**
- 🟢 1-4: **Baixo** — monitorar
- 🟡 5-9: **Médio** — tratar oportunamente
- 🟠 10-16: **Alto** — tratar com prioridade
- 🔴 17-25: **Crítico** — ação imediata

## Riscos Típicos em Câmaras Municipais

| Risco | Prob. | Imp. | Score | Controle sugerido |
|---|---|---|---|---|
| Ultrapassar limite de pessoal (6% RCL) | 3 | 5 | 🔴 15 | Monitoramento mensal da RCL |
| Fracionamento de despesa | 4 | 4 | 🔴 16 | Planejamento anual de compras |
| Licitação sem ETP/TR completo | 3 | 3 | 🟡 9 | Checklist obrigatório pré-edital |
| Portal de transparência desatualizado | 4 | 3 | 🟠 12 | Auditoria mensal do portal |
| Pagamento sem liquidação | 2 | 4 | 🟡 8 | Segregação empenho/liquidação/pagamento |
| Ausência de inventário patrimonial | 3 | 4 | 🟠 12 | Inventário rotativo trimestral |
| RP sem disponibilidade de caixa | 3 | 5 | 🔴 15 | Conciliação mensal RP × caixa |
| Admissão sem concurso (efetivo) | 1 | 5 | 🟡 5 | Conferência de todas as admissões |
| Contrato sem fiscal designado | 4 | 3 | 🟠 12 | Checklist de formalização |
| Atraso no envio SINC/SICONFI | 3 | 4 | 🟠 12 | Alertas automatizados |

## Tratamento dos Riscos

| Estratégia | Quando usar |
|---|---|
| **Evitar** | Risco inaceitável — eliminar a atividade que gera o risco |
| **Mitigar** | Reduzir probabilidade ou impacto com controles |
| **Transferir** | Compartilhar com terceiro (seguro, garantia contratual) |
| **Aceitar** | Risco baixo, custo do controle maior que o risco |

## Monitoramento

### Indicadores de risco (exemplos)
- % de despesa com pessoal / RCL (meta: < 5,4%)
- Nº de dispensas de licitação / total de contratações
- Dias de atraso no envio de relatórios ao TCE
- Score do portal de transparência (meta: > 80%)
- Nº de recomendações pendentes do controle interno
- % de contratos com fiscal designado formalmente

### Frequência de revisão
- **Mensal**: indicadores de pessoal e financeiro
- **Trimestral**: revisão da matriz de riscos
- **Anual**: revisão completa do plano de riscos
