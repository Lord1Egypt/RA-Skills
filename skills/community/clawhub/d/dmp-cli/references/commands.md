# DMP CLI Command Reference

## Installation

### Install From Releases

Download pre-built binaries from the releases page:

`https://github.com/a652/dmp-cli/releases`

Available platforms:

| File Pattern | OS | Arch |
|--------------|----|------|
| `dmp-<version>-linux-amd64` | Linux | x86_64 |
| `dmp-<version>-linux-arm64` | Linux | ARM64 |
| `dmp-<version>-darwin-amd64` | macOS | Intel |
| `dmp-<version>-darwin-arm64` | macOS | Apple Silicon |
| `dmp-<version>-windows-amd64.exe` | Windows | x86_64 |

Linux and macOS example:

```bash
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "$ARCH" in
  x86_64) ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
esac

TAG=$(curl -sf https://api.github.com/repos/a652/dmp-cli/releases/latest | grep '"tag_name"' | cut -d'"' -f4)
FILENAME="dmp-${TAG}-${OS}-${ARCH}"

curl -fL "https://github.com/a652/dmp-cli/releases/download/${TAG}/${FILENAME}" -o dmp
chmod +x dmp
sudo mv dmp /usr/local/bin/
dmp version
```

## Global Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-o, --output` | `table` | Output format: `table`, `json`, or `plain` |
| `--context` | current | Override the active context |
| `-v, --verbose` | false | Print redacted request metadata to stderr |

## JSON Parameter Convention

Flags accepting JSON support inline data or `@filename` syntax:

```bash
--files '[{"idType":"MD5_OAID","path":"/data/test.csv"}]'
--files @/tmp/files.json
```

## Audience Commands

Core entity details:

- Audience types: `1=upload 2=combine 3=rule 4=expand 5=idlink`
- Audience statuses: `0=failed 1=success 2=waiting 3=computing`
- Track types: `MOBILE`, `OTT`, `PC`
- Common ID types: `MD5_OAID`, `MD5_MAC`, `MD5_IMEI`, `MD5_IDFA`, `PHONE_NUM`

### List Audiences

```bash
dmp audience list \
  [--type 1] \
  [--status 1] \
  [--ids 101500,101499] \
  [--page 1] [--size 20] \
  -o json
```

### Check Audience Status

```bash
dmp audience status <id> [<id>...] -o json
```

### Create Upload Audience

SFTP:

```bash
dmp audience create upload \
  --name "my-audience" \
  --track-type MOBILE \
  --upload-type sftp \
  --account user@example.com \
  --files '[{"idType":"MD5_OAID","path":"/data/test.csv"}]'
```

S3:

```bash
DMP_UPLOAD_PASSWORD=<s3-secret> dmp audience create upload \
  --name "my-audience" \
  --track-type MOBILE \
  --upload-type s3 \
  --s3-source 3 \
  --account <s3-access-key> \
  --files '[{"idType":"MD5_OAID","path":"s3://bucket/test.csv"}]'
```

### Create Combined Audience

```bash
dmp audience create combine \
  --name "combined" \
  --track-type MOBILE \
  --id-types MD5_OAID \
  --data '[{"op":"and","rule":{"audience":[101499]}}]'
```

`--data` is an array of rule objects with `op` and `rule` members.

### Create Lookalike Expand Audience

By scale:

```bash
dmp audience create expand \
  --name "expanded" \
  --seed-id 101500 \
  --id-types MD5_OAID \
  --expand-type scale \
  --scale 10000
```

By confidence:

```bash
dmp audience create expand \
  --name "expanded" \
  --seed-id 101500 \
  --id-types MD5_OAID \
  --expand-type confidence \
  --confidence-min 0.5 \
  --confidence-max 0.9
```

Optional: `--negative-seed-id <id>`.

### Create Cross-device ID Link Audience

```bash
dmp audience create idlink \
  --name "idlink" \
  --link-type 1 \
  --input-track-type MOBILE \
  --input-id-types MD5_OAID \
  --input-audience-id 101500 \
  --output-track-type OTT \
  --output-id-types MD5_MAC
```

### Create Rule-based Advertisement Audience

```bash
dmp audience create rule-advertisement \
  --name "adv-rule" \
  --track-type MOBILE \
  --id-types MD5_OAID \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --data @/tmp/adv_rule.json
```

Use `dmp ref ad-dimensions` to discover valid dimension values.

### Create Rule-based App Audience

```bash
dmp audience create rule-app \
  --name "app-rule" \
  --track-type MOBILE \
  --id-types MD5_OAID \
  --app-type 0 \
  --packages com.taobao.taobao,com.tmall.wireless,com.jd.app.reader,com.meituan.android.pt
```

`--app-type`: `0=active 1=installed`. Minimum 4 unique package names required.

### Create Rule-based LBS Audience

```bash
dmp audience create rule-lbs \
  --name "lbs-rule" \
  --track-type MOBILE \
  --id-types MD5_OAID \
  --data @/tmp/lbs.json
```

### Create Transform Audience

```bash
DMP_UPLOAD_PASSWORD=<pw> dmp audience create transform \
  --name "transform" \
  --track-type PHONE_NUM \
  --s3-source 1 \
  --account <ak> \
  --files '[{"idType":"PHONE_NUM","path":"s3://bucket/phones.csv"}]'
```

## Insight Commands

### List Insight Tasks

```bash
dmp insight list [--ids 100145,100148] -o json
```

### Create Insight Task

```bash
dmp insight create \
  --name "my-insight" \
  --audience-id 101500 \
  --type 0 \
  --conditions demographic,interest,media
```

- `--type`: `0=miaolue insight`, `1=partner insight`
- `--name` maximum 20 characters

### Get Insight Results

```bash
dmp insight result <task-id> -o json
```

## Sync Commands

Platforms:

- `1=ByteDance`
- `2=Tencent`
- `3=Alipay`
- `4=Bilibili`
- `5=XiaoHongShu`

### List Platform Advertisers

```bash
dmp sync advertisers --platform 5 -o json
```

### Create Sync Task

Standard:

```bash
dmp sync create \
  --audience-id 101500 \
  --platform 5 \
  --advertiser-id <id> \
  --advertiser-brand <brand>
```

ByteDance cloud push:

```bash
dmp sync create \
  --audience-id 101500 \
  --platform 1 \
  --advertiser-id <id> \
  --bytedance-push-cloud=true \
  --bytedance-cloud-adv-id 123456789
```

Validation rules:

- `--advertiser-brand` is required when `platform=5`
- `--bytedance-cloud-adv-id` is required and digits-only when `--bytedance-push-cloud=true`
- `--bytedance-cloud-adv-id` and `--bytedance-cloud-name` are forbidden when cloud push is false or unset

### List Sync Tasks

```bash
dmp sync list \
  [--ids 123,456] \
  [--status 1] \
  [--start-date 2025-01-01] [--end-date 2025-12-31] \
  [--page 1] [--size 20] \
  -o json
```

## Deal Commands

### List Deals

```bash
dmp deal list [--name "keyword"] [--ids 20000112,20000111] [--page 1] [--size 20] -o json
```

### Create Deal

```bash
dmp deal create --file /tmp/deal.json
```

The `audiences` field accepts simplified format `[101, 102]`, which the CLI converts into DTO objects.

### Modify Deal

```bash
dmp deal modify --id 20000112 --file /tmp/patch.json
```

- `audiences` is append-only
- Do not include `dealId` in the patch JSON

## Reference Data Commands

### Tags

```bash
dmp ref tags [--type 1] -o json
```

### Apps

```bash
dmp ref apps [--category 购物] [--install-level "安装量级1亿以上"] -o json
```

### Regions

```bash
dmp ref regions --track-type MOBILE -o json
```

### Ad Dimensions

```bash
dmp ref ad-dimensions --track-type MOBILE --type 活动维度 -o json
```

