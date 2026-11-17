# Visa Rules Knowledge Model

## Snapshot Structure

Each country entry in `RULES` (embedded in `scripts/border_buddy.py`) is keyed by ISO-3166 alpha-2 code and contains:

| Field | Type | Meaning |
|---|---|---|
| `name` | str | Country display name |
| `visa_policy` | dict | Nationality group → policy object |
| `passport_validity` | dict | Rule for passport validity at entry |
| `yellow_fever` | dict | Requirement + endemic reference list |
| `customs` | dict | Duty-free allowances + cash threshold |
| `transit` | dict | Airside transit visa policy by group |
| `authority` | str | Official body to verify current rules with |
| `as_of` | str | Snapshot date — rules may have changed since |

## Nationality Groups

To keep the snapshot compact, nationalities are bucketed by visa-policy behavior:

- `WESTERN_HEISOSPHERE` — US, CA, UK, AU, NZ, JP, KR, SG, and most EU-adjacent
- `EU_EFTA` — EU/EEA + Switzerland (freedom of movement inside Schengen)
- `SOUTH_AMERICA` — BR, AR, CL, UY, PY, PE, CO, EC, BO (visa-liberal for most of Schengen)
- `SOUTH_ASIA` — IN, PK, BD, LK, NP (e-visa/visa-required for most Western destinations)
- `AFRICA` — NG, GH, KE, ZA, EG, MA (varies by destination)

Each destination maps group → one of:

```
visa_free          — no visa, max stay days given
visa_on_arrival    — pay at border, max stay days given
eta                — electronic travel authorization pre-departure
evisa              — online visa, print the confirmation
visa_required      — embassy/consulate application
```

## Transit Rules (the big surprises)

Airside transit (staying in the international zone, no border entry) is its own policy:

- **No visa needed for airside transit** (most nationalities): most of Schengen when staying airside
- **Transit visa required regardless of airside**: US, CA, AU, UK (Direct Airside Transit Visa for many South Asian / African nationalities)
- **China**: 24-hour TWOV (Two-One Visa-free transit) applies when staying airside or leaving via same city; 144-hour regional TWOV for many nationalities when entering landside
- **Rule of thumb**: if you change airports (e.g., LHR → LGW), it is NOT airside transit — you enter the country and need a full entry visa.

## Passport Validity Rules

| Rule | Countries (examples) | Meaning |
|---|---|---|
| `six_months` | CN, TH, TR, EG, VN, ID, most of Africa/ME | passport must be valid 6 months beyond entry |
| `three_months_beyond_departure` | Schengen | 3 months beyond intended departure, issued within last 10 years |
| `valid_for_stay` | PH, HK, KR, AR, BR home rule | just valid through the stay |

Plus the universal recommendation: at least 6 months validity and 2 blank pages regardless of the legal minimum — airlines enforce their own stricter versions and deny boarding on their interpretation.

## Health Certificates

**Yellow fever** is the only broadly-enforced international certificate (International Health Regulations). Required when:

1. Arriving from a country with risk of YF transmission (WHO list), OR
2. The destination itself is a risk country

The snapshot encodes an endemic set (Africa: NG, GH, CD, KE, etc.; South America: BR north/risk areas, CO, PE, EC, BO, PY). Brazil requires a certificate from endemic arrivals; the EU generally does not unless arriving from an endemic country.

Other certificates occasionally enforced: polio (PK, AF), meningitis (SA for Hajj). Treat as notes, not legal advice.

## Customs Allowances (adult travelers, snapshot values)

Typical duty-free into the EU: 1L spirits (>22%) or 2L <22%, 4L wine, 200 cigarettes. US: 1L alcohol, 200 cigarettes, $800 exemption. Cash: EU €10,000, US $10,000, CN ¥20,000+... declaration thresholds — declaring is free, failing to declare is a crime.

## Keeping the Snapshot Honest

Every report footer prints `as_of` and the authority to verify with. When this skill is used, the agent should:
1. Present the snapshot answer.
2. Offer/direct a live verification against the named authority (IANATimatic for airlines is the de-facto operational source).

## Verification

`python3 scripts/border_buddy.py rules --destination XX` dumps the raw snapshot entry so the agent (or user) can inspect exactly what the report is based on.
