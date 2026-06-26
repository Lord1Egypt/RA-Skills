# BlackSnow Ontology

## Risk Vector Taxonomy

### Infrastructure (`infra.*`)

```
infra
├── energy
│   ├── grid
│   │   ├── transmission
│   │   ├── distribution
│   │   └── generation
│   ├── oil
│   │   ├── upstream
│   │   ├── midstream
│   │   └── downstream
│   ├── gas
│   │   ├── pipeline
│   │   ├── storage
│   │   └── lng
│   └── renewables
│       ├── solar
│       ├── wind
│       └── hydro
├── transport
│   ├── rail
│   │   ├── freight
│   │   └── passenger
│   ├── port
│   │   ├── container
│   │   └── bulk
│   ├── aviation
│   │   ├── cargo
│   │   └── passenger
│   └── road
│       ├── trucking
│       └── logistics_hubs
├── water
│   ├── supply
│   ├── treatment
│   └── irrigation
└── telecom
    ├── backbone
    ├── last_mile
    └── data_centers
```

### Labor (`labor.*`)

```
labor
├── union
│   ├── grievances
│   ├── negotiations
│   └── actions
├── attrition
│   ├── voluntary
│   ├── involuntary
│   └── critical_roles
├── hiring
│   ├── freezes
│   ├── surges
│   └── role_changes
└── safety
    ├── incidents
    ├── complaints
    └── inspections
```

### Legal (`legal.*`)

```
legal
├── regulation
│   ├── draft
│   ├── consultation
│   └── enacted
├── litigation
│   ├── filed
│   ├── discovery
│   └── settlement
├── compliance
│   ├── audits
│   ├── violations
│   └── remediation
└── contracts
    ├── force_majeure
    ├── termination
    └── renegotiation
```

### Supply Chain (`supply.*`)

```
supply
├── inventory
│   ├── buffering
│   ├── depletion
│   └── write_downs
├── logistics
│   ├── routing
│   ├── delays
│   └── capacity
├── procurement
│   ├── tenders
│   ├── awards
│   └── cancellations
└── vendors
    ├── substitution
    ├── concentration
    └── risk_ratings
```

### Finance (`finance.*`)

```
finance
├── credit
│   ├── spreads
│   ├── ratings
│   └── defaults
├── liquidity
│   ├── stress
│   ├── facilities
│   └── repo
└── exposure
    ├── counterparty
    ├── geographic
    └── sectoral
```

---

## Signal Types

| Type | Description | Weight |
|------|-------------|--------|
| `deferral` | Maintenance/action postponed | 0.6 |
| `acceleration` | Unexpected urgency | 0.8 |
| `substitution` | Vendor/resource swap | 0.5 |
| `language_shift` | Contractual/regulatory wording change | 0.7 |
| `attrition_spike` | Sudden personnel exits | 0.9 |
| `grievance_surge` | Union/labor complaints | 0.6 |
| `inventory_buffer` | Unusual stockpiling | 0.5 |
| `consultation_extension` | Regulatory delay | 0.4 |
| `attendance_decay` | Committee/board absences | 0.3 |

---

## Temporal Markers

- `immediate`: 0-7 days
- `near_term`: 7-30 days
- `medium_term`: 30-90 days
- `long_term`: 90-365 days

---

## Tradability Matrix

| Risk Vector | Insurance | Commodities | Logistics | Policy |
|-------------|-----------|-------------|-----------|--------|
| `infra.energy.*` | ✓ | ✓ | ✓ | ✓ |
| `infra.transport.*` | ✓ | ○ | ✓ | ○ |
| `labor.*` | ○ | ○ | ✓ | ✓ |
| `legal.*` | ✓ | ○ | ○ | ✓ |
| `supply.*` | ○ | ✓ | ✓ | ○ |
| `finance.*` | ✓ | ✓ | ○ | ✓ |

✓ = Primary tradability  
○ = Secondary/conditional
