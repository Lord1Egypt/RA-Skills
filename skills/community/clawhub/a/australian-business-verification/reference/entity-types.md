# ABR Entity Type Codes

`AbnDetails.aspx` and `AcnDetails.aspx` return both a 3-letter `EntityTypeCode`
and a full English `EntityTypeName`. In almost all cases, just present the
`EntityTypeName` to the user — you don't need to look anything up here.

This table is a quick reference for the codes you're most likely to encounter when
verifying SME, sole trader, and common company structures. For the complete
official list (including state/territory/commonwealth government variants and
superannuation fund types), see
https://abr.business.gov.au/Documentation/ReferenceData.

| Code  | Description                                           |
| ----- | ----------------------------------------------------- |
| `IND` | Individual / Sole Trader                              |
| `PRV` | Australian Private Company                            |
| `PUB` | Australian Public Company                             |
| `PTR` | Other Partnership                                     |
| `FPT` | Family Partnership                                    |
| `TRT` | Other Trust                                           |
| `DTT` | Discretionary Trading Trust                           |
| `DIT` | Discretionary Investment Trust                        |
| `FXT` | Fixed Trust                                           |
| `FUT` | Fixed Unit Trust                                      |
| `HYT` | Hybrid Trust                                          |
| `DST` | Discretionary Services Management Trust               |
| `CUT` | Corporate Unit Trust                                  |
| `PUT` | Listed Public Unit Trust                              |
| `PQT` | Unlisted Public Unit Trust                            |
| `JVT` | Joint Venture                                         |
| `COP` | Co-operative                                          |
| `OIE` | Other Incorporated Entity                             |
| `UIE` | Other Unincorporated Entity                           |
| `DES` | Deceased Estate                                       |
| `SUP` | Super Fund                                            |
| `SMF` | ATO Regulated Self-Managed Superannuation Fund (SMSF) |
| `NRF` | Non-Regulated Superannuation Fund                     |
| `GOV` | Government                                            |
| `STA` | State Government                                      |
| `LOC` | Local Government                                      |
| `TER` | Territory Government                                  |
| `CGE` | Commonwealth Government Entity                        |
| `SGE` | State Government Entity                               |
| `LGE` | Local Government Entity                               |
| `TGE` | Territory Government Entity                           |
| `DIP` | Diplomatic / Consulate Body or High Commissioner      |

## Reading entity type alongside other fields

- A `PRV` or `PUB` entity will normally also have an `Acn` populated (the ABN's
  last 9 digits are derived from the ACN for Australian companies).
- `IND` (sole trader), `PTR`/`FPT` (partnerships), and `TRT`/`DTT`/etc. (trusts)
  do **not** have an ACN — this is expected, not an error.
- Government entity types (`CGE`, `SGE`, `LGE`, `TGE`, and their many
  sub-variants for specific structures like cash management trusts or pooled
  development funds) are uncommon in typical SME verification but appear when
  checking government suppliers or agencies.
