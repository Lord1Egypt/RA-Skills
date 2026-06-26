# AWS Pricing Cheat Sheet

## Price List API (GetProducts)
- Endpoint: `https://api.pricing.us-east-1.amazonaws.com/` (only available from `us-east-1`).
- Required IAM permission: `pricing:GetProducts`.
- CLI example:
  ```bash
  aws pricing get-products \
    --region us-east-1 \
    --service-code AmazonEC2 \
    --filters \
      "Field=instanceType,Type=TERM_MATCH,Value=c6i.large" \
      "Field=operatingSystem,Type=TERM_MATCH,Value=Linux" \
      "Field=tenancy,Type=TERM_MATCH,Value=Shared" \
      "Field=location,Type=TERM_MATCH,Value=Asia Pacific (Tokyo)" \
      "Field=regionCode,Type=TERM_MATCH,Value=ap-northeast-1" \
    --max-results 100 \
    --output json
  ```
- Common filter fields per service (case sensitive):
  - **AmazonEC2**: `instanceType`, `location`, `regionCode`, `operatingSystem`, `tenancy`, `capacitystatus`, `preInstalledSw`, `marketoption`, `termType`.
  - **AmazonRDS**: `databaseEngine`, `deploymentOption`, `instanceType`, `licenseModel`, `location`, `regionCode`.
  - **AmazonS3**: `usagetype`, `storageClass`, `location`, `regionCode`, `operation`.
  - **AmazonCloudFront**: `location`, `operation`, `termType`.
- `PriceList` array contains JSON strings; `terms.OnDemand` or `terms.Reserved` → `priceDimensions` → `pricePerUnit.USD`.

## Bulk Pricing JSON + Cache
- Structure: `products` dictionary + `terms` dictionary (OnDemand/Reserved) keyed by SKU.
- Public files hosted at `https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/<ServiceCode>/current/<region>/index.json`。
  - Example (EC2 Tokyo): `.../AmazonEC2/current/ap-northeast-1/index.json`。
- 下載檔案通常 10–200 MB。腳本會自動存到 `--cache-dir`（預設 `~/.cache/aws-price-csv`）。
  - 每次計算前先檢查快取：若檔案存在且未超過 30 天即直接使用。
  - 若檔案不存在、超過 30 天，或使用 `--force-refresh`（即時計算），就重新下載並覆寫快取。
  - 仍可透過 `--bulk-files ServiceCode=/path.json` 指定自備檔案並跳過快取。
- To find a price manually:
  1. Match `products[sku].attributes` with requested filters (`regionCode`, `instanceType`, `volumeApiName`, etc.).
  2. Go to `terms.<OnDemand|Reserved>[sku]`。
  3. Filter `termAttributes` when looking for RI（例如 `LeaseContractLength=1yr`, `PurchaseOption=No Upfront`, `OfferingClass=standard`）。
  4. Read `pricePerUnit.USD`, `unit`, `description`。

## Region Code → Location Name
| Region Code | Location Label |
|-------------|----------------|
| us-east-1 | US East (N. Virginia) |
| us-east-2 | US East (Ohio) |
| us-west-1 | US West (N. California) |
| us-west-2 | US West (Oregon) |
| ap-northeast-1 | Asia Pacific (Tokyo) |
| ap-northeast-2 | Asia Pacific (Seoul) |
| ap-northeast-3 | Asia Pacific (Osaka) |
| ap-south-1 | Asia Pacific (Mumbai) |
| ap-south-2 | Asia Pacific (Hyderabad) |
| ap-southeast-1 | Asia Pacific (Singapore) |
| ap-southeast-2 | Asia Pacific (Sydney) |
| ap-southeast-3 | Asia Pacific (Jakarta) |
| ap-southeast-4 | Asia Pacific (Melbourne) |
| ap-east-1 | Asia Pacific (Hong Kong) |
| ap-east-2 | Asia Pacific (Taipei) |
| ca-central-1 | Canada (Central) |
| eu-central-1 | EU (Frankfurt) |
| eu-central-2 | EU (Zurich) |
| eu-north-1 | EU (Stockholm) |
| eu-south-1 | EU (Milan) |
| eu-south-2 | EU (Spain) |
| eu-west-1 | EU (Ireland) |
| eu-west-2 | EU (London) |
| eu-west-3 | EU (Paris) |
| me-central-1 | Middle East (UAE) |
| me-south-1 | Middle East (Bahrain) |
| sa-east-1 | South America (São Paulo) |

## Sample Input Template
```yaml
currency: USD
items:
  - name: c6i.large Linux (on-demand 720h)
    service_code: AmazonEC2
    filters:
      instanceType: c6i.large
      operatingSystem: Linux
      tenancy: Shared
      capacitystatus: Used
      preInstalledSw: NA
    term:
      type: OnDemand
    usage:
      quantity: 720   # hours
      unit: Hrs

  - name: gp3 General Purpose SSD (1TB)
    service_code: AmazonEC2
    filters:
      volumeApiName: gp3
      storageMedia: SSD-backed
      usagetype: APN1-EBS:VolumeUsage.gp3
    term:
      type: OnDemand
    usage:
      quantity: 1024
      unit: GB-Mo

  - name: r6i.32xlarge 1yr RI (No Upfront)
    service_code: AmazonEC2
    filters:
      instanceType: r6i.32xlarge
      tenancy: Shared
      operatingSystem: Linux
      capacitystatus: Used
    term:
      type: Reserved
      attributes:
        LeaseContractLength: 1yr
        PurchaseOption: No Upfront
        OfferingClass: standard
    usage:
      quantity: 720
      unit: Hrs
```
