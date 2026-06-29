# Supplier Discovery Source Registries

Seed registry of supplier discovery source families for the BigDeal Supplier Finder skill. These entries help agents choose where to search for suppliers; they are not endorsements of any platform, directory, or source.

## Boundary

**Does:**
- Seed source-surface recall for supplier discovery across six source families
- Record where B2B platforms, trade shows, associations, government directories, company websites, and media/community sources may be found
- Expose source metadata and source gaps as raw discovery signals

**Does not:**
- Recommend adopting any listed supplier or platform
- Prove source quality, safety, maintenance, or business readiness
- Replace candidate-level supplier review, due diligence, or procurement gates

---

## Family 1: B2B Platforms and Marketplaces

**id:** `b2b-platforms`

**Examples:** Alibaba, Global Sources, Made-in-China, DHgate, IndiaMART, ThomasNet, Kompass, EC21, TradeWheel, eWorldTrade

**Access notes:**
- Most platforms offer public web browsing without authentication for basic supplier listings
- Some platforms expose search endpoints with filters for product category, region, certification, and minimum order quantity
- Advanced features (contact details, RFQ, messaging) typically require free registration
- Platform-specific search syntax varies; prefer keyword + category + region combinations

**Useful for:**
- Broad supplier pool discovery for common product categories
- OEM/ODM and private-label sourcing
- Cross-border ecommerce supplier identification
- Region-specific supplier filtering (e.g., "Guangdong electronics manufacturer")

**Not for:**
- Supplier trustworthiness or quality verification
- Price benchmarking or contract negotiation
- Bypassing platform registration walls
- Niche or highly specialized components where platforms lack coverage

**Query patterns:**
- `{product category} supplier {region}` (e.g., "LED lighting supplier China")
- `{product} OEM manufacturer site:alibaba.com`
- `{product} wholesale private label {platform name}`
- `{industry} B2B marketplace {country}`

**Caveats:**
- Listings may include trading companies mislabeled as manufacturers; cross-check with company websites
- Search result ordering may be influenced by paid promotion; do not treat rank as quality signal
- Platform content changes frequently; record access failures as source gaps
- Some supplier pages require login to view full contact details

**Status:** unverified

---

## Family 2: Trade Shows and Exhibitions

**id:** `trade-shows`

**Examples:** Canton Fair (China Import and Export Fair), Global Sources Exhibitions, CES, Hannover Messe, Canton Fair Online, TradeKey events, KommMesser, SIAL, Anuga, Canton Fair Spring/Autumn

**Access notes:**
- Exhibitor lists are typically public on official trade show websites
- Some shows publish searchable exhibitor directories with product category filters
- Past exhibitor lists may remain accessible for historical supplier discovery
- Virtual/hybrid trade shows increasingly publish digital exhibitor directories

**Useful for:**
- Identifying suppliers with demonstrated export readiness
- Discovering suppliers in specific product verticals with trade show presence
- Finding regional supplier clusters (e.g., "Canton Fair electronics exhibitors")
- Historical exhibitor lists for suppliers with proven exhibition track records

**Not for:**
- Current contact details (exhibitor information may be outdated)
- Real-time availability or production capacity verification
- Small or local suppliers that do not exhibit at major trade shows
- Suppliers in categories with minimal trade show presence

**Query patterns:**
- `{trade show name} {year} exhibitor list {product category}`
- `{industry} trade show exhibitors {region}`
- `{product} exhibition {city} official exhibitor directory`
- `site:{trade-show-domain} exhibitor {product keyword}`

**Caveats:**
- Exhibitor lists from past years may contain defunct companies; verify with current web presence
- Trade show websites may remove old exhibitor lists; archive sources when possible
- Not all exhibitors are manufacturers; some are distributors or trading companies
- Virtual exhibitor directories may have limited search functionality

**Status:** unverified

---

## Family 3: Industry Associations and Chambers of Commerce

**id:** `associations`

**Examples:** China Chamber of Commerce for Import and Export of Machinery and Electronics (CCCME), China Electronics Chamber of Commerce (CECC), Federation of Indian Export Organisations (FIEO), British Chambers of Commerce, U.S. Chamber of Commerce, European Association of Craft, Small and Medium-sized Enterprises (UEAPME), specific industry associations by vertical

**Access notes:**
- Member directories vary: some are public, some require membership login
- Association websites often publish member lists, industry reports, and supplier guides
- Regional chambers of commerce may maintain local supplier directories
- Industry reports and white papers may reference supplier clusters or member companies

**Useful for:**
- Finding suppliers with industry affiliation and potential credibility signals
- Discovering regional supplier clusters through chamber directories
- Accessing industry-specific supplier guides and buyer resources
- Identifying trade associations that publish member directories or buyer guides

**Not for:**
- Comprehensive supplier databases (membership lists are often partial)
- Supplier quality verification (membership does not imply quality)
- Direct contact enrichment (directory entries may be minimal)
- Suppliers outside the association's geographic or industry scope

**Query patterns:**
- `{industry} association member directory {region}`
- `{product} chamber of commerce supplier list {country}`
- `{industry} trade association buyer guide supplier`
- `site:{association-domain} member {product keyword}`

**Caveats:**
- Member directories may be incomplete or outdated; verify with current web search
- Association membership is a weak signal; do not treat it as quality or trust proof
- Some associations gate member directories behind login or membership fees
- Regional chambers may have limited online presence or non-searchable directories

**Status:** unverified

---

## Family 4: Government and Industry Directories

**id:** `government-directories`

**Examples:** China Customs registration databases, AEO (Authorized Economic Operator) lists, export license holder registries, FDA registered establishments, EU EORI databases, national export promotion agency directories (e.g., ITA, JETRO, KOTRA), ISO certification body databases, business registration databases

**Access notes:**
- Government databases vary widely in accessibility: some are fully public, others require registration
- Many export-related directories are published by trade promotion agencies
- Certification databases (ISO, FDA, CE) may expose registrant company names
- Business registration data may be available through national corporate registries

**Useful for:**
- Verifying export eligibility and regulatory compliance signals
- Finding suppliers with specific certifications (ISO, FDA, CE, etc.)
- Discovering officially registered exporters and manufacturers
- Cross-checking supplier claims against official records

**Not for:**
- Comprehensive supplier discovery (directories are often narrow in scope)
- Real-time verification (government databases may lag behind reality)
- Supplier quality or capability assessment (registration does not imply quality)
- Bypassing official access channels or terms of use

**Query patterns:**
- `{country} export license holder {product category}`
- `AEO certified exporter {region} {industry}`
- `FDA registered manufacturer {product} site:fda.gov`
- `{certification body} certified company {product} {country}`
- `{country} business registration {company name} manufacturer`

**Caveats:**
- Government database interfaces vary; some lack search APIs or advanced filtering
- Data freshness varies; record verification dates and note when data was last updated
- Language barriers may exist for non-English government databases
- Access restrictions may apply; record access failures as source gaps rather than no-result

**Status:** unverified

---

## Family 5: Company Websites and Directories

**id:** `company-websites`

**Examples:** Individual manufacturer websites, industry-specific supplier directories (e.g., Kompass, Europages), wholesale directory sites, niche B2B vertical directories, company LinkedIn pages, regional business directories

**Access notes:**
- Company websites are publicly accessible but require individual search and evaluation
- Industry directories may offer aggregated search across multiple company sites
- LinkedIn and similar professional networks can reveal company profiles and product portfolios
- Some directories offer advanced search by product, region, certification, and company size

**Useful for:**
- Direct supplier research after initial discovery
- Verifying product portfolios, capabilities, and company backgrounds
- Finding niche or specialized suppliers not listed on major B2B platforms
- Cross-referencing supplier claims with self-published information

**Not for:**
- Initial broad discovery (inefficient compared to aggregated sources)
- Trustworthiness verification (self-published claims are unverified)
- Automated bulk extraction (violates skill constraints against scraping)
- Contact enrichment or background checks beyond public web information

**Query patterns:**
- `{product} manufacturer site:{country TLD}` (e.g., `LED manufacturer site:.cn`)
- `{product} factory {region} "about us" "OEM"`
- `{industry} suppliers directory {region}`
- `{company name} manufacturer {product} official website`
- `intitle:{product} manufacturer {region}`

**Caveats:**
- Self-published information may be inaccurate or outdated; cross-check with multiple sources
- Company websites vary greatly in quality and information depth
- Language barriers may require translation tools or local-language query variants
- Some company sites use aggressive SEO; do not treat search ranking as quality signal

**Status:** unverified

---

## Family 6: Public Media and Community Sources

**id:** `media-community`

**Examples:** Industry news sites (e.g., Sourcing Journal, Just Style), Reddit communities (r/entrepreneur, r/ecommerce, niche sourcing subreddits), Quora sourcing discussions, industry forums, LinkedIn posts and articles, trade publications, sourcing blogs, YouTube supplier review videos, podcast mentions

**Access notes:**
- Public media sources are freely accessible via web search
- Community sources (forums, Reddit, Quora) contain user-generated content with variable quality
- Industry news sites may publish supplier profiles, industry roundups, and sourcing guides
- Social media and community discussions can reveal supplier recommendations and warnings

**Useful for:**
- Discovering supplier names mentioned in industry discussions
- Identifying emerging or niche suppliers not yet in major directories
- Gathering community sentiment and anecdotal supplier experiences
- Finding industry-specific sourcing guides and roundups

**Not for:**
- Verified supplier information (community content is unverified and subjective)
- Quality or trustworthiness proof (anecdotes are not evidence)
- Sole source of supplier discovery (should be cross-referenced with structured sources)
- Automated sentiment analysis or reputation scoring

**Query patterns:**
- `{product} supplier recommendation reddit`
- `{industry} sourcing guide {year}`
- `{product} manufacturer review forum`
- `{country} supplier experience quora`
- `{product} sourcing blog "supplier" "recommend"`
- `{industry} news supplier profile {region}`

**Caveats:**
- Community content is highly variable in quality and may contain misinformation
- Recommendations may be biased (affiliate links, paid promotions, personal grudges)
- Information ages quickly; prioritize recent discussions and verify with current sources
- Do not treat community consensus as evidence; always seek URL-backed primary sources

**Status:** unverified

---

## Registry Metadata

- **Registry name:** Supplier Discovery Source Registries
- **Version:** 0.1.0-draft
- **Purpose:** Seed registry for BigDeal Supplier Finder find-stage source selection
- **Format:** Markdown prose (agent-readable)
- **Coverage:** Six source families aligned with BSF SKILL.md find-stage scope
- **Status:** All entries unverified — use as source expansion only, not as quality or safety proof
