# Examples

## 1) High-confidence auto-match

Listing A:

`Apple iPhone 15 128GB Blue`

Listing B:

`iPhone 15 (128 GB, Blue) - Apple`

Result:

- decision: auto-match
- confidence: high
- reason: `R001`

## 2) Variant mismatch rejection

Listing A:

`Samsung Galaxy S24 8GB/128GB`

Listing B:

`Samsung Galaxy S24 8GB/256GB`

Result:

- decision: reject
- reason: `R101`

## 3) Bundle mismatch rejection

Listing A:

`Sony WH-1000XM5 Headphones`

Listing B:

`Sony WH-1000XM5 + Charger + Case Combo`

Result:

- decision: reject
- reason: `R102`

## 4) Medium-confidence manual review

Listing A:

`OnePlus 12R 256GB Gray`

Listing B:

`One Plus 12 R 256 GB Iron`

Result:

- decision: manual review
- confidence: medium
- reason: `R003`

