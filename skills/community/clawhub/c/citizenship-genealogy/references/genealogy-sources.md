# Sites de Árvore Genealógica e Fontes de Documentação Oficial

> **Pesquisa atualizada em julho de 2026 via Composio/Firecrawl.**
> Inclui APIs, arquivos nacionais, e procedimentos para obtenção de certidões.

---

## 1. Plataformas de Árvore Genealógica

### 1.1 FamilySearch (Gratuito)
**Site:** https://www.familysearch.org
**API:** https://developers.familysearch.org
**Dados:** 1,8 bilhão de pessoas pesquisáveis (2025)
**Custo:** Gratuito (organização sem fins lucrativos da Igreja LDS)

#### Recursos principais
- **Family Tree:** árvore global colaborativa
- **Historical Records:** bilhões de registros históricos digitalizados
- **DNA:** Integrated with Ancestry, MyHeritage
- **Memories:** fotos, histórias, documentos enviados por usuários

#### FamilySearch API (REST, gratuita)
**Como obter chave:** https://www.familysearch.org/innovate/apply
**Endpoints principais:**
- `/platform/tree/persons/{pid}` — dados de uma pessoa
- `/platform/tree/ancestry?pid={pid}` — genealogia ascendente
- `/platform/tree/descendancy?pid={pid}` — genealogia descendente
- `/platform/tree/persons/{pid}/matches` — matches potenciais
- `/platform/records/search` — busca em registros históricos
- `/platform/places/search` — busca em 6+ milhões de localidades
- `/platform/memories/search` — busca em fotos/documentos

**Parceiros oficiais da API:** Ancestry, MyHeritage, Findmypast

#### Regras de privacidade
- Registros de nascimento: 100+ anos
- Casamento e morte: 70+ anos
- Acesso a dados de pessoas vivas requer permissão

---

### 1.2 Ancestry.com
**Site:** https://www.ancestry.com
**Dados:** 30 bilhões de registros (2022), 25 milhões de usuários
**Custo:** ~$25–50/mês (assinatura)
**Versões locais:** Ancestry.com.br, .it, .de, .fr, etc.

#### Recursos
- DNA Ancestry: teste genético com matching
- Family Tree Builder: software para construir árvore
- Records Search: busca em registros históricos
- Communities: fóruns por região/origem

---

### 1.3 MyHeritage
**Site:** https://www.myheritage.com
**Dados:** 61 milhões de árvores genealógicas, 19,9 bilhões de registros
**Idiomas:** 42 idiomas (incluindo Português brasileiro)
**Custo:** Freemium (recursos avançados pagos)

#### Recursos
- Smart Matches: matches automáticos com outras árvores
- Record Detective: vincula registros automaticamente
- Deep Nostalgia: animação de fotos antigas
- DNA MyHeritage: 6,5 milhões de kits (2023)

---

### 1.4 Findmypast
**Site:** https://www.findmypast.com
**Especialidade:** Reino Unido e Irlanda
**Dados:** registros britânicos, irlandeses, coloniais
**Custo:** ~$15–30/mês

---

### 1.5 Geneanet
**Site:** https://www.geneanet.org
**Especialidade:** Europa ( França, Bélgica, Holanda, Alemanha)
**Dados:** 2+ bilhões de indivíduos indexados
**Custo:** Freemium

---

### 1.6 Platform Comparison

| Plataforma | Melhor para | Gratuito? | DNA | API |
|------------|-------------|-----------|-----|-----|
| FamilySearch | Pesquisa geral, colaboração | ✅ Sim | Não (parceiros) | ✅ Sim |
| Ancestry | Teste de DNA, registros profundos | ❌ Não | ✅ Sim | ❌ Não |
| MyHeritage | Europeus, interface moderna | Freemium | ✅ Sim | Limitada |
| Findmypast | Britânicos e irlandeses | ❌ Não | Não | ❌ Não |
| Geneanet | Europeus (especialmente franceses) | Freemium | Não | ❌ Não |

---

## 2. Arquivos Nacionais e Fontes de Documentação Oficial

### 2.1 Itália
**Registros civis digitalizados:**
- **Antenati (Portale Antenati):** https://antenati.cultura.gov.it
  - Registros de nascimento, casamento, morte (1809–1900+)
  - Busca por nome, município, data
  - Registros com 100+ anos (nascimento) e 70+ anos (casamento/óbito)

**Como obter certidões:**
- **Ufficio dello Stato Civile** do município (comune) onde ocorreu o evento
- Pedido deve ser escrito em italiano
- Taxa cobrada (varia por comune)
- Envio por courier privado ou serviço postal

**Fontes complementares:**
- **FamilySearch Wiki (Itália):** https://www.familysearch.org/en/wiki/Italy_Genealogy
- **Embassy dos EUA na Itália:** https://it.usembassy.gov/obtaining-vital-records/
- **Stato di Famiglia:** registro familiar (cópia do livro do comune)

**Períodos históricos:**
- Sul da Itália: registros civis desde 1809
- Norte/Centro: registros civis desde 1866 (Vêneto: 1871)
- Antes de 1809: registros paroquiais (igreja)

---

### 2.2 Portugal
**Serviço online oficial:**
- **Civil Online:** https://www.civilonline.mj.pt
- **Portal Justica.gov.pt:** https://justica.gov.pt/Servicos/Request-a-birth-certificate
- **Custo:** €10 (online) ou €20 (papel)
- **Prazo:** 24–48 horas (online)

**Como obter certidões:**
- **Online:** Civil Online (precisa de certificado digital do cidadão português, ou pode pedir sem assinar)
- **Presencial:** Conservatória do Registo Civil, Loja de Cidadão, IRN Espaço Registos
- **No exterior:** Consulado português
- **Por correio:** para qualquer Conservatória

**Tipos de certidão:**
- Nascimento, casamento, óbito
- Com ou sem apostila
- Formato português ou internacional (multilíngue)

**Registros paroquiais (antes de 1910):**
- **Tombo.org:** https://tombo.pt/ (registros paroquiais digitalizados)
- **Arquivos distritais:** pesquisar no arquivo distrital da região

---

### 2.3 Espanha
**Serviço online oficial:**
- **Sede Electrónica do Ministério da Justiça:** https://sede.mjusticia.gob.es
- **Custo:** gratuito (com certificado digital) ou taxa moderada
- **Idiomas:** espanhol, inglês (parcial)

**Como obter certidões:**
- Online com certificado digital Cl@ve
- Presencial no Registro Civil correspondiente
- No exterior: consulado espanhol

**Registros complementares:**
- **FamilySearch:** https://www.familysearch.org/en/wiki/Spain_Genealogy
- **Archivo General de Indias:** para conexões coloniais com as Américas

---

### 2.4 Alemanha
**Serviço online oficial:**
- **Verwaltung.bund.de:** https://verwaltung.bund.de
- **Germany.info (Birth Certificate):** https://www.germany.info/us-en/service/04-familymatters/birth-certificates-895588

**Como obter certidões:**
- **Standesamt** (cartório civil) do local de nascimento
- **Geburtsurkunde** (certidão de nascimento)
- **Heiratsurkunde** (certidão de casamento)
- **Sterbeurkunde** (certidão de óbito)
- **Confidentialidade:** nascimento 110 anos, casamento 80 anos, óbito 30 anos

**Para cidadania (restituição/ascendência):**
- **Bundesverwaltungsamt (BVA):** para Verfahren nach Art. 116 GG
- Formulário específico disponível em https://www.germany.info/

**Registros históricos:**
- **Church Books:** Kirchenbücher (antes de 1894/1918)
- **Bundesarchiv:** https://www.bundesarchiv.de/

---

### 2.5 Hungria
**Serviço online oficial:**
- **AdatbázisokOnline (MNL):** https://adatbazisokonline.mnl.gov.hu
- **Banco de dados de registros civis de Budapeste:** disponível desde 2025
- **3.100 volumes digitalizados** (abril–dezembro de 2024)
- **~1 milhão de imagens**
- **Custo:** Gratuito para pesquisa online

**Como pesquisar:**
- Busca por nome do assentamento, data, tipo de registro
- Registros em húngaro (e até 1906 em formato de minutos; depois em formato tabular)

**Confidentialidade:**
- Óbito: 30 anos após criação
- Nascimento: 110 anos após criação
- Casamento: 86 anos após criação
- ~70% da coleção já está publicamente disponível

**Para cidadania húngara:**
- **Embaixada/Consulado:** Tel Aviv (https://telaviv.mfa.gov.hu), Los Angeles, etc.
- **Documentos necessários:** certidões de nascimento/casamento/óbito (com tradução juramentada)

---

### 2.6 Polônia
**Arquivo nacional:**
- **Archiwa Państwowe:** https://archiwa.gov.pl/en/search-in-archives/genealogy/
- **Genealogia w Archiwach:** https://www.genealogiawarchiwach.pl/
- **Custo:** Gratuito (registros digitalizados)

**Como pesquisar:**
- Busca por nome da localidade, freguesia, paróquia
- Registros em polonês, alemão, russo (dependendo da época)

**Tipos de registros:**
- Registros paroquiais (batismo, casamento, óbito)
- Registros civis (após 1918/1945)
- Registros judiciais (inventários, mudanças de nome)
- Registros notariais

**Para confirmação de cidadania polonesa:**
- **Consulado/Embaixada da Polônia:** https://www.gov.pl/web/diplomacy
- **Certidão de Cidadania (Potwierdzenie Obywatelstwa):** emitida pelo Voivode

---

### 2.7 Irlanda
**Sources:**
- **National Archives of Ireland:** https://nationalarchives.ie/help-with-research/types-of-research/family-history-research/
- **DFA Foreign Birth Registration:** https://www.ireland.ie/en/dfa/citizenship/born-abroad/
- **Griffith's Valuation:** https://www.askaboutireland.ie/griffiths-valuation/
- **IrishGenealogy.ie:** https://www.irishgenealogy.ie/ (certidões online €6–20)

**Como obter certidões:**
- **IrishGenealogy.ie:** certidão online por €6 (nascimento após 1864)
- **General Register Office (GRO):** certidões físicas
- **Consulado irlandês:** para registro de nascimento no exterior (Foreign Birth Registration)

---

### 2.8 Reino Unido
**National Archives:** https://www.nationalarchives.gov.uk/
**General Register Office (GRO):** https://www.gro.gov.uk/
**Scotland's People:** https://www.scotlandspeople.gov.uk/
**Findmypast:** parceria oficial com GRO

**Como obter certidões:**
- **GRO Online:** £7–11 por certidão digital
- **Scotland's People:** £7 por certidão
- **No exterior:** consulado britânico

---

### 2.9 Estados Unidos
**National Archives (NARA):** https://www.archives.gov/
**Ellis Island:** https://www.libertyellisfoundation.org/
**VitalChek:** https://www.vitalchek.com/ (certidões online, $15–30)
**USCIS Genealogy:** https://www.uscis.gov/genealogy

**Tipos de registros:**
- Censos (1790–1950): https://www.census.gov/
- Registros de imigração (Ellis Island, Angel Island)
- Registros militares (WWI, WWII)
- Naturalization records

---

### 2.10 Canadá
**Library and Archives Canada:** https://www.bac-lac.gc.ca/
**Ancestry.ca:** parceria oficial

---

### 2.11 França
**Archives Nationales:** https://www.culture.gouv.fr/Thematiques/Archives
**Department Archives:** https://archives.paris.fr/, https://archives.department.org/
**Geneanet:** forte cobertura francesa

---

### 2.12 Brasil
**Arquivo Nacional:** https://www.arquivonacional.gov.br/
**FamilySearch Brasil:** https://www.familysearch.org/en/wiki/Brazil_Genealogy
**Cartórios de Registro Civil:** https://www.registrocivil.org.br/
**Igrejas católicas:** registros de batismo (FamilySearch tem digitalizados)

**Como obter certidões no Brasil:**
- **Online:** https://registrocivil.org.br/ (2ª via, R$20–50)
- **Cartório:** presencial ou por correio
- **Apostilamento:** cartório autorizado (Convenção de Haia)

---

## 3. Fluxo de Pesquisa em Fontes Oficiais

### 3.1 Etapa 1: Coleta de informações familiares

Perguntar ao usuário:
1. Nome completo dos avós e bisavós (se conhecidos)
2. Cidade/estado/país de origem do ancestral imigrante
3. Data aproximada de nascimento/casamento do ancestral
4. Religião (católica, judaica, protestante, ortodoxa)
5. Se houve mudança de nome na imigração (italianização, aportuguesamento)

### 3.2 Etapa 2: Pesquisa em plataforma genealógica

**Ordem recomendada:**
1. **FamilySearch** (gratuito, maior acervo global) → buscar nome do ancestral
2. **Antenati** (Itália, gratuito) → buscar em registros civis italianos
3. **Tombo.pt** (Portugal, gratuito) → buscar registros paroquiais portugueses
4. **AdatbázisokOnline** (Hungria, gratuito) → buscar registros civis húngaros
5. **Geneanet** (Freemium) → buscar árvores de outras pessoas com mesmo ancestral
6. **Findmypast** (pago gratuito) → RN e Irlanda

### 3.3 Etapa 3: Validação em fontes oficiais

Para cada ancestral confirmado:
1. **Identificar o arquivo detentor** (comune, conservatória, Standesamt, etc.)
2. **Verificar disponibilidade online** (Antenati, Civil Online, GRO, etc.)
3. **Solicitar certidão** se disponível online OU
4. **Contatar o arquivo** por email/formulário para pedidos manuais

### 3.4 Etapa 4: Obtenção de certidões

**Prioridade para processos de cidadania:**
1. **CNN (Certidão Negativa de Naturalização)** — para Itália
2. **Certidão de Nascimento do ascendente estrangeiro** — apostilada + traduzida
3. **Certidão de Casamento** — de toda a cadeia
4. **Certidão de Óbito** — se aplicável
5. **Certidão de Nascimento/Casamento do requerente e pais**

### 3.5 Etapa 5: Legalização e tradução

1. **Apostilamento** em cartório brasileiro (Convenção de Haia)
2. **Tradução juramentada** por tradutor público concursado
3. **Conferência tripla** de nomes, datas e locais
4. **Envio** ao consulado/Ministério competente

---

## 4. Estratégias de Busca por País de Origem

### Imigração italiana (Brasil)
1. **Antenati** → buscar certidão de nascimento no comune
2. **FamilySearch** → buscar índice de passageiros (porto de Santos, Rio)
3. **Museu da Imigração (SP)** → registros de imigrantes desembarcados
4. **Arquivos do Estado** → SP, RS, SC, PR, MG

### Imigração portuguesa (Brasil)
1. **Tombo.pt** → registros paroquiais portugueses
2. **Torre do Tombo** → registros de imigração portuguesa
3. **FamilySearch** → registros de batismo em Portugal
4. **Arquivo Nacional Brasil** → registros de entrada de portugueses

### Imigração alemã (Brasil)
1. **FamilySearch** → registros de imigração (Hamburgo)
2. **Arquivo Nacional** → registros de colônias alemãs
3. **Bundesarchiv** → para documentos na Alemanha
4. **Standesamt** → certidões de nascimento alemãs

### Imigração espanhola (Brasil)
1. **FamilySearch** → registros de imigração na Espanha
2. **Archivo General de Indias** → para conexões coloniais
3. **Registro Civil Espanhol** → certidões online

### Imigração irlandesa/reino unido (Brasil/diáspora)
1. **FamilySearch** → registros-paroquiais britânicos e irlandeses
2. **Findmypast** → registros de emigração (Inglaterra)
3. **National Archives (UK)** → registros de passageiros
4. **GRO** → certidões de nascimento inglesas

### Imigração húngara
1. **AdatbázisokOnline** → registros civis digitais
2. **FamilySearch** → registros paroquiais húngaros (Luteranos, Católicos, Reformados)
3. **Nacional Archives of Hungary** → documentação

### Imigração polonesa
1. **Genealogia w Archiwach** → registros paroquiais
2. **FamilySearch** → registros de batismo
3. **Archiwa Państwowe** → documentação civil posterior

---

## 5. APIs e Ferramentas para Automação

### FamilySearch API
**URL base:** https://api.familysearch.org/platform/
**Auth:** OAuth 2.0 (chave gratuita via aplicação)
**Limite:** razoável para uso pessoal
**Documentação completa:** https://www.familysearch.org/en/developers/docs/api/resources

### MyHeritage API
**Disponível apenas para parceiros comerciais**
**Alternativa:** usar a plataforma web manualmente

### Ancestry API
**Não disponível publicamente**
**Alternativa:** usar a plataforma web manualmente

### Ferramentas complementares
- **GEDCOM:** formato padrão para exportar/importar árvores genealógicas
- **Gramps:** software gratuito de genealogia
- **RootsMagic:** software de genealogia (pago)
- **DNA Painter:** para mapeamento de DNA

---

## 6. Contatos Úteis para Documentação

### Consulados no Brasil
- **Itália:** São Paulo, Rio, Porto Alegre, Belo Horizonte, Curitiba, Recife
- **Portugal:** São Paulo, Rio, Salvador, Belo Horizonte, Curitiba, Recife
- **Espanha:** São Paulo, Rio, Salvador
- **Alemanha:** São Paulo, Rio, Porto Alegre
- **Irlanda:** São Paulo (secção consular)
- **Hungria:** São Paulo (honorary consul)

### Embaixadas no exterior
- Consultar Portal das Relações Exteriores do país de interesse
