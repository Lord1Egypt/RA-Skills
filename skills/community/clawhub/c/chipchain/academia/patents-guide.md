# Patent Analysis Guide for Semiconductor Supply Chain Intelligence

## Key Patent Classification Codes

### Primary: H01L — Semiconductor Devices
- H01L 21/ — Manufacturing processes (THE master code)
- H01L 21/027 — Mask making
- H01L 21/30 — CMP/planarization
- H01L 21/311 — Etching
- H01L 21/3205 — Metal deposition
- H01L 21/56 — Encapsulation/packaging
- H01L 21/67 — Manufacturing apparatus (equipment)
- H01L 21/683 — Wafer handling
- H01L 25/065 — 3D stacking (HBM, chiplets)

### CPC H10 (newer, replacing some H01L):
- H10B — Memory devices (DRAM, NAND, MRAM, ReRAM)
- H10D — Semiconductor device structures

### C23C — Coating/Deposition
- C23C 14/34 — Sputtering
- C23C 16/44 — CVD
- C23C 16/455 — **ALD** (critical for advanced nodes)
- C23C 16/50 — PECVD

### G03F — Photolithography
- G03F 7/004 — Photoresist chemistry
- G03F 7/09 — EUV resist
- G03F 7/20 — Lithography apparatus

### B24B 37/ — CMP
- B24B 37/04 — CMP pads
- B24B 37/044 — CMP slurry compositions

### C30B — Crystal Growth
- C30B 15/ — Czochralski (silicon wafer production)
- C30B 29/36 — SiC crystal growth

## Free Patent Search Databases

| Database | URL | Best for |
|---|---|---|
| **Google Patents** | patents.google.com | Cross-jurisdiction search, machine translation |
| **Espacenet** | worldwide.espacenet.com | Patent families (INPADOC), classification search |
| **Lens.org** | lens.org | Links patents to scholarly articles, API available |
| **KIPRIS** | kipris.or.kr | Korean patents |
| **J-PlatPat** | j-platpat.inpit.go.jp | Japanese patents |
| **CNIPA** | pss-system.cponline.cnipa.gov.cn | Chinese patents |
| **TIPO** | twpat.tipo.gov.tw | Taiwan patents |
| **USPTO** | patft.uspto.gov | US patents |

## Patent Analysis Methods for Supply Chain Mapping

### 1. Co-filing / Co-assignee Analysis
When two companies co-file a patent → active collaboration / supplier relationship.
```
Search Google Patents: assignee:"Samsung Electronics" AND assignee:"JSR"
→ Reveals joint photoresist development = confirmed supply relationship
```

### 2. Citation Analysis
- **Forward citations:** Who cites a company's patents → depends on/builds upon their tech
- **Backward citations:** What a company cites → their technology inputs/dependencies
- Aggregate backward citations by citing assignee = technology dependency map

### 3. Inventor Analysis
- Track named inventors moving between companies (via LinkedIn + patent assignee changes)
- Shared inventors between company and university = active collaboration

### 4. Technology Landscape Mapping
- Pull all patents in a CPC code (e.g., C23C 16/455 for ALD)
- Aggregate by assignee → who dominates this technology area
- Track year-over-year → who's entering, who's declining

### 5. China Self-Sufficiency Tracking
- Monitor Chinese company patent filing rates in areas controlled by foreign suppliers
- Surge in Chinese patents in G03F 7/ (photoresist) = active domestic development
- Compare CPC code coverage: Chinese companies vs Japanese/US/European leaders
