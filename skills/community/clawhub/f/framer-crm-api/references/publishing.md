# Publishing & Deployment

Reference for publishing previews, deploying to production, and monitoring deployment status.

---

## Publishing workflow

Framer uses a two-step deployment model:

1. **Publish** — creates a staging/preview version
2. **Deploy** — promotes the preview to production (live site)

---

## Publish a preview

```javascript
const result = await framer.publish()
// Returns:
// {
//   deployment: { id: "deploy_abc123" },
//   hostnames: ["preview-abc123.framer.app"]
// }
```

Publishing is safe — it creates a preview URL without affecting the live site.

---

## Deploy to production

```javascript
await framer.deploy(result.deployment.id)
```

**Always confirm with the user before deploying.** This makes changes live.

---

## Check what changed before publishing

```javascript
const changes = await framer.getChangedPaths()
console.log("Added:", changes.added)
console.log("Modified:", changes.modified)
console.log("Removed:", changes.removed)
```

Use this to show the user what will be published before they confirm.

---

## Check who made changes

```javascript
const contributors = await framer.getChangeContributors()
// Returns array of contributor UUIDs
```

---

## View deployment history

```javascript
const deployments = await framer.getDeployments()
for (const d of deployments) {
  console.log(d.id, d.createdAt, d.status)
}
```

---

## Get current publish status

```javascript
const info = await framer.getPublishInfo()
// Shows current production and staging deployment info
```

---

## Full publish-and-deploy pattern

```javascript
// 1. Check for changes
const changes = await framer.getChangedPaths()
const totalChanges = changes.added.length + changes.modified.length + changes.removed.length

if (totalChanges === 0) {
  console.log("No changes to publish.")
  return
}

console.log(`${totalChanges} changes detected:`)
console.log(`  Added: ${changes.added.length}`)
console.log(`  Modified: ${changes.modified.length}`)
console.log(`  Removed: ${changes.removed.length}`)

// 2. Publish preview
const result = await framer.publish()
console.log("Preview URL:", result.hostnames[0])

// 3. Ask user to verify preview, then deploy
// await framer.deploy(result.deployment.id)
```

---

## Project info

```javascript
const info = await framer.getProjectInfo()
// { id, name, apiVersion1Id }

const user = await framer.getCurrentUser()
// { id, name, avatar }
```
