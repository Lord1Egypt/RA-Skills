# ClawHub API 数据模型

## Owner

```json
{
  "handle": "string",
  "displayName": "string",
  "image": "string"
}
```

## Skill

```json
{
  "slug": "string",
  "displayName": "string",
  "summary": "string",
  "tags": {},
  "stats": {},
  "createdAt": 0,
  "updatedAt": 0
}
```

## SkillListItem

```json
{
  "slug": "string",
  "displayName": "string",
  "summary": "string",
  "tags": {},
  "stats": {},
  "createdAt": 0,
  "updatedAt": 0,
  "latestVersion": {
    "version": "string",
    "createdAt": 0,
    "changelog": "string"
  }
}
```

## PackageCatalogItem

```json
{
  "name": "string",
  "displayName": "string",
  "family": "skill",
  "runtimeId": "string",
  "channel": "official",
  "isOfficial": true,
  "summary": "string",
  "ownerHandle": "string",
  "createdAt": 0,
  "updatedAt": 0,
  "latestVersion": "string",
  "capabilityTags": ["string"],
  "executesCode": true,
  "verificationTier": "structural"
}
```

## PackageCapabilities

```json
{
  "executesCode": true,
  "runtimeId": "string",
  "pluginKind": "string",
  "channels": ["string"],
  "providers": ["string"],
  "hooks": ["string"],
  "bundledSkills": ["string"],
  "setupEntry": true,
  "configSchema": true,
  "configUiHints": true,
  "materializesDependencies": true,
  "toolNames": ["string"],
  "commandNames": ["string"],
  "serviceNames": ["string"],
  "capabilityTags": ["string"],
  "httpRouteCount": 0,
  "bundleFormat": "string",
  "hostTargets": ["string"]
}
```

## PackageVerification

```json
{
  "tier": "structural",
  "scope": "artifact-only",
  "summary": "string",
  "sourceRepo": "string",
  "sourceCommit": "string",
  "sourceTag": "string",
  "hasProvenance": true,
  "scanStatus": "clean"
}
```

## SecuritySnapshot

```json
{
  "status": "clean",
  "hasWarnings": true,
  "checkedAt": 0,
  "model": "string",
  "hasScanResult": true,
  "sha256hash": "string",
  "virustotalUrl": "string",
  "scanners": {}
}
```

