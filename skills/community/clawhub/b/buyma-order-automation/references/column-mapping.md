# Column Mapping

## BUYMA CSV -> Order Sheet

- P 受注メモ -> B
- K 発送方法 -> D
  - startswith `その他 /` => `사가`
  - startswith `韓国郵便局 /` => `KP`
- C 価格 -> G
- L 色・サイズ -> K
- D 受注数 -> L
- M 連絡事項 -> N (translate to Korean outside these scripts if needed)
- O 名前（ローマ字） -> N
  - only if region is OKINAWA -> append `오키나와`
  - if N already has content, append with newline

## Product name
- Write F using Chrome auto-translated Korean product name as shown in browser

## History enrichment by F

Search historical rows using Korean product name in F.

### I/J
- If one match: copy I and J
- If multiple different values: join with newline and mark red

### M
- If historical value is `9부산` or `5신강`: keep as-is
- If historical value is `6노원`, `7마산`, `8울산`: write `화라`
- If multiple different values: join with newline and mark red
