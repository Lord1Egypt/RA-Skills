---
name: edi-parser
description: Parse EDI X12 files (810 Invoice, 850 Purchase Order, 856 ASN). Extract structured data from ISA/GS envelopes, transaction sets, and segments. Use when working with EDI files, Walmart/retail supplier compliance, or extracting PO, invoice, and shipment data from X12 format.
---

# EDI X12 Parser

Parse and extract structured data from EDI X12 transaction sets.

## Supported Transaction Sets

- **810** -- Invoice
- **850** -- Purchase Order
- **856** -- Advance Ship Notice (ASN)

## Parsing Approach

EDI files use `~` as segment terminator, `*` as element separator, and `>` or `:` as sub-element separator (check ISA-16).

### Envelope Structure

```
ISA*QQ*SenderID*RR*ReceiverID*Date*Time*:*Version*Control#*AckReq*Mode*SubSep~
  GS*FuncCode*SenderCode*ReceiverCode*Date*Time*GroupControl*Standard*Version~
    ST*TransactionSet*Control#~
      ... segments ...
    SE*SegmentCount*Control#~
  GE*TransactionCount*GroupControl~
IEA*GroupCount*InterchangeControl~
```

### Key ISA Fields (1-indexed)
- ISA-05: Sender qualifier (`12`=UCS, `ZZ`=mutually defined, `08`=UCC)
- ISA-06: Sender ID (left-padded to 15 chars)
- ISA-07: Receiver qualifier
- ISA-08: Receiver ID

### 850 Purchase Order
| Segment | Key Fields |
|---------|-----------|
| BEG | BEG-03=PO Number, BEG-05=PO Date |
| DTM | DTM-01=Qualifier (002=Delivery, 010=Requested Ship), DTM-02=Date |
| N1 | N1-01=Entity (ST=Ship-To, BY=Buyer, SF=Ship-From), N1-02=Name |
| PO1 | PO1-02=Qty, PO1-04=Unit Price, PO1-07=UPC/SKU |
| PID | PID-05=Description |

### 810 Invoice
| Segment | Key Fields |
|---------|-----------|
| BIG | BIG-01=Invoice Date, BIG-02=Invoice#, BIG-04=PO# |
| REF | REF-01=Qualifier (IA=Vendor#, BM=BOL#), REF-02=Value |
| N1 | N1-01=Entity (ST=Ship-To, RE=Remit-To) |
| IT1 | IT1-02=Qty, IT1-04=Unit Price, IT1-07=UPC |
| TDS | TDS-01=Total invoice amount (cents, divide by 100) |

### 856 ASN
| Segment | Key Fields |
|---------|-----------|
| BSN | BSN-02=Shipment ID, BSN-03=Date |
| HL | HL-03=Level (S=Shipment, O=Order, P=Pack, I=Item) |
| REF | REF-01=Qualifier (BM=BOL, IA=Vendor#, LO=Load#, AO=Appointment) |
| PRF | PRF-01=PO Number |
| MAN | MAN-02=SSCC-18 barcode |
| LIN | LIN-03=UPC |
| SN1 | SN1-02=Qty Shipped, SN1-03=UOM |

## Walmart-Specific Notes

- Walmart ISA receiver: qualifier `08`, ID `925485US00`
- REF*IA = Walmart vendor number (required on 856)
- REF*LO = Load number (new requirement)
- N1*ST with `UL` qualifier = GLN for ship-to location
- MAN*GM = SSCC-18 (required per pallet on 856)

## Output Format

When parsing, output a clean table:

```
| Field | Value |
|-------|-------|
| Transaction | 856 ASN |
| ISA Sender | 12 / 1234567890 |
| ISA Receiver | 08 / 925485US00 |
| PO# | 0123456789 |
| Ship Date | 2026-02-16 |
| Items | 16 line items |
```

For bulk parsing, output CSV with one row per line item.
