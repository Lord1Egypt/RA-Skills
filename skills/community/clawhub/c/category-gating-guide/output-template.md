# Category Ungating Application -- Output Template

Organize all documentation for a category ungating application using this template.

## Application Summary

| Field | Value |
|---|---|
| **Seller Legal Name** | [Exact name from Seller Central registration] |
| **Seller Central Account ID** | [Merchant token or account number] |
| **Target Category** | [Category or subcategory name] |
| **Gate Type** | [Category / Subcategory / Brand / ASIN / Condition] |
| **Target ASINs** | [List each ASIN with product title] |
| **Application Date** | [YYYY-MM-DD] |
| **Application Type** | [Initial / Appeal / Resubmission] |

---

## Account Health Snapshot

Capture these metrics from Seller Central > Performance > Account Health at the time of application.

| Metric | Current Value | Threshold | Status |
|---|---|---|---|
| Order Defect Rate (ODR) | [X.XX%] | Below 1% | [Pass/Fail] |
| Valid Tracking Rate | [XX.X%] | Above 95% | [Pass/Fail] |
| Late Shipment Rate | [X.X%] | Below 4% | [Pass/Fail] |
| Policy Violations (past 90 days) | [Count] | 0 | [Pass/Fail] |
| A-to-Z Claims Under Investigation | [Count] | 0 | [Pass/Fail] |
| Account Age | [X months] | 3+ months | [Pass/Fail] |
| Seller Plan | [Professional/Individual] | Professional | [Pass/Fail] |

**Overall eligibility**: [Ready to apply / Resolve issues first]

---

## Invoice Documentation

Complete one entry per invoice submitted.

### Invoice 1

| Field | Value |
|---|---|
| **Supplier Name** | [Full legal name of supplier] |
| **Supplier Address** | [Complete address] |
| **Supplier Phone** | [Verifiable phone number] |
| **Supplier Website** | [URL] |
| **Invoice Number** | [Unique invoice ID] |
| **Invoice Date** | [YYYY-MM-DD] |
| **Days Since Issue** | [Number -- must be under 180] |
| **Buyer Name on Invoice** | [Must match Seller Central legal name] |
| **File Name** | [Invoice_SupplierName_Date.pdf] |

**Line Items**:

| Product Description | ASIN Match | Quantity | Unit Cost |
|---|---|---|---|
| [Description from invoice] | [ASIN] | [10+ required] | [Amount] |
| [Description from invoice] | [ASIN] | [10+ required] | [Amount] |

**Invoice verification checklist**:
- [ ] Buyer name matches Seller Central legal entity exactly
- [ ] Invoice date is within 180 days
- [ ] Minimum 10 units per ASIN
- [ ] Supplier contact information is complete and verifiable
- [ ] Document is PDF format with selectable text
- [ ] No visible editing artifacts or modifications
- [ ] Product descriptions are identifiable against ASIN listings

[Repeat the Invoice 1 structure for additional invoices]

---

## Product Image Documentation

Complete one entry per ASIN. Capture 6 images: front label, back label, ingredients/materials panel, UPC barcode, lot/batch number, and packaging.

| Image | File Name | Status |
|---|---|---|
| Front label | `ProductPhoto_[ASIN]_Front.jpg` | [Ready/Retake] |
| Back label | `ProductPhoto_[ASIN]_Back.jpg` | [Ready/Retake] |
| Ingredients | `ProductPhoto_[ASIN]_Ingredients.jpg` | [Ready/Retake] |
| UPC barcode | `ProductPhoto_[ASIN]_UPC.jpg` | [Ready/Retake] |
| Lot/Batch | `ProductPhoto_[ASIN]_Lot.jpg` | [Ready/Retake] |
| Packaging | `ProductPhoto_[ASIN]_Package.jpg` | [Ready/Retake] |

---

## Supporting Documents (if applicable)

| Document Type | File Name | Status |
|---|---|---|
| Brand authorization letter | [BrandAuth_BrandName_Date.pdf] | [Ready/N-A] |
| Safety certification (COA, CPC) | [Filename.pdf] | [Ready/N-A] |

---

## Rejection History (for appeals)

| Attempt | Date | Rejection Reason | Corrective Action |
|---|---|---|---|
| 1 | [YYYY-MM-DD] | [Exact reason] | [Changes made] |

---

## Submission Checklist

- [ ] All invoices verified (name match, date, quantity, format)
- [ ] All product images on white background, text legible, barcode visible
- [ ] Supporting documents attached (if applicable)
- [ ] Account health metrics all pass thresholds
- [ ] No other ungating applications currently pending
- [ ] All documents reviewed against `assets/quality-checklist.md`
