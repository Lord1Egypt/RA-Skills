# RREO e RGF — Relatórios Fiscais

## RREO — Relatório Resumido de Execução Orçamentária

### Fundamento legal
- **CF/88, art. 165, §3º** — publicação até 30 dias após encerramento de cada bimestre
- **LRF arts. 52-53** — conteúdo obrigatório
- **MCASP Parte V** — modelos e instruções de preenchimento

### Periodicidade
**Bimestral** — 6 relatórios por ano

| Bimestre | Período | Prazo publicação |
|---|---|---|
| 1º | Jan-Fev | 30/03 |
| 2º | Mar-Abr | 30/05 |
| 3º | Mai-Jun | 30/07 |
| 4º | Jul-Ago | 30/09 |
| 5º | Set-Out | 30/11 |
| 6º | Nov-Dez | 30/01 (ano seguinte) |

### Composição obrigatória (LRF art. 52)

**Anexos obrigatórios:**
1. Balanço Orçamentário
2. Demonstrativo da Execução das Despesas por Função/Subfunção
3. Demonstrativo da Receita Corrente Líquida (RCL)
4. Demonstrativo das Receitas e Despesas Previdenciárias
5. Demonstrativo do Resultado Nominal
6. Demonstrativo do Resultado Primário
7. Demonstrativo dos Restos a Pagar por Poder e Órgão
8. Demonstrativo das Receitas e Despesas com MDE (art. 212 CF)
9. Demonstrativo das Receitas e Despesas com Saúde (LC 141/2012)
10. Demonstrativo das Parcerias Público-Privadas (se houver)
11. Demonstrativo simplificado do RREO

### Sistema de envio
- **SICONFI** (STN) — obrigatório para todos os entes
- **SINC** (TCE-MA) — obrigatório para entes do Maranhão (cumulativo)

---

## RGF — Relatório de Gestão Fiscal

### Fundamento legal
- **LRF arts. 54-55** — conteúdo e prazos
- **MCASP Parte V** — modelos

### Periodicidade
**Quadrimestral** — 3 relatórios por ano (Municípios com pop. > 50 mil)
**Semestral** — 2 relatórios por ano (Municípios com pop. ≤ 50 mil, opcional)

| Quadrimestre | Período | Prazo publicação |
|---|---|---|
| 1º | Jan-Abr | 30/05 |
| 2º | Mai-Ago | 30/09 |
| 3º | Set-Dez | 30/01 (ano seguinte) |

### Composição obrigatória (LRF art. 55)

**Anexos obrigatórios:**
1. **Demonstrativo da Despesa com Pessoal** (por Poder/Órgão)
2. **Demonstrativo da Dívida Consolidada Líquida** (DCL)
3. **Demonstrativo das Garantias e Contragarantias de Valores**
4. **Demonstrativo das Operações de Crédito**
5. **Demonstrativo da Disponibilidade de Caixa e dos RPP**
6. **Demonstrativo simplificado do RGF**

### Limites fiscais — Poder Legislativo Municipal

#### Despesa com Pessoal (art. 20 LRF)
| Parâmetro | % da RCL |
|---|---|
| Limite máximo | 6,00% |
| Limite prudencial (95% do máximo) | 5,70% |
| Limite de alerta (90% do máximo) | 5,40% |

**Consequências do excesso:**
- Ultrapassou **alerta** (5,40%): TCE comunica ao Poder
- Ultrapassou **prudencial** (5,70%): vedações do art. 22 LRF (proibido: reajuste, hora extra, contratação, criação de cargo)
- Ultrapassou **máximo** (6,00%): eliminação em 2 quadrimestres (1/3 no primeiro), vedações do art. 23 LRF

#### Dívida Consolidada Líquida (Resolução SF 40/2001)
| Ente | Limite |
|---|---|
| Município | 1,2× RCL |
| Estado | 2,0× RCL |

### Cálculo da RCL (art. 2º, IV, LRF)

```
RCL = Receitas Correntes
    - Transferências constitucionais e legais (a outros entes)
    - Contribuições previdenciárias do servidor (RPPS)
    - Compensação financeira entre RGPS e RPPS
    - Receita de FPM/FPE/ICMS destinada ao FUNDEB
```

Período de apuração: **12 meses anteriores** ao mês de referência, incluindo o mês.

---

## SICONFI — Operacionalização

### Acesso
- URL: https://siconfi.tesouro.gov.br
- Login: certificado digital e-CPF ou e-CNPJ (tipo A3)
- Perfis: Declarante, Homologador, Consultor

### Fluxo de envio
1. **Preencher** os demonstrativos no sistema ou importar planilha
2. **Validar** — sistema verifica consistências automáticas
3. **Assinar** — declarante com certificado digital
4. **Homologar** — homologador (geralmente o gestor) confirma
5. **Publicar** — fica disponível publicamente

### Erros comuns
- RCL divergente entre RREO e RGF
- Despesa empenhada ≠ soma das fontes de recurso
- Restos a pagar sem correspondência com exercícios anteriores
- Resultado primário inconsistente com demais demonstrativos
