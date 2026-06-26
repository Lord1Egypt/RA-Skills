# DMP CLI Workflows

## Create Audience And Poll Until Ready

```bash
AID=$(dmp audience create combine \
  --name "agent-segment-$(date +%s)" \
  --track-type MOBILE \
  --id-types MD5_OAID \
  --data @rule.json -o plain)

dmp audience status $AID -o json
```

Continue polling until `audienceStatus` is `1` or `0`.

## Create Audience Then Sync To Platform

```bash
AID=$(dmp audience create upload --name "upload-seg" --track-type MOBILE \
  --upload-type sftp --account user@sftp.com \
  --files '[{"idType":"MD5_OAID","path":"/data/users.csv"}]' -o plain)

dmp audience status $AID -o json
dmp sync advertisers --platform 1 -o json
dmp sync create --audience-id $AID --platform 1 --advertiser-id <adv-id>
```

## Create Audience Then Run Insight

```bash
AID=$(dmp audience create rule-app --name "app-users" --track-type MOBILE \
  --id-types MD5_OAID --packages com.a,com.b,com.c,com.d -o plain)

dmp audience status $AID -o json

TID=$(dmp insight create --name "insight-$(date +%s)" \
  --audience-id $AID --type 0 --conditions demographic,interest,media -o plain)

dmp insight list --ids $TID -o json
dmp insight result $TID -o json
```

## Discover Reference Data Before Building Rules

```bash
dmp ref ad-dimensions --track-type MOBILE --type 活动维度 -o json
dmp ref apps --category 购物 -o json
dmp ref regions --track-type MOBILE -o json
dmp ref tags --type 1 -o json
```

