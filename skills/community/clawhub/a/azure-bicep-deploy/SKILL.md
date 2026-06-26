---
name: azure-bicep-deploy
description: Deploy and validate Azure Bicep files and ARM templates. Use for: (1) Deploying Bicep (.bicep) or ARM (JSON) templates to Azure, (2) Validating Bicep/ARM templates for syntax errors, (3) Creating Azure resources via Bicep, (4) Managing multi-environment deployments (dev/staging/prod) via parameters. Supports Azure Container Apps commonly used workloads. Prerequisites: Azure CLI (az) installed, Azure CLI authenticated (az login), Bicep CLI installed (az bicep install), appropriate Azure subscription access.
---

# Azure Bicep Deploy

## Prerequisites (Required)

Before using this skill, ensure:

1. **Azure CLI installed**
   ```bash
   az --version
   ```
   Install from: https://docs.microsoft.com/cli/azure/install-azure-cli

2. **Azure CLI authenticated**
   ```bash
   az login          # Interactive login
   az login --tenant <tenant-id>  # For specific tenant
   az account show   # Verify logged in
   ```

3. **Correct subscription selected** (if multiple)
   ```bash
   az account list                           # List subscriptions
   az account set --subscription <sub-id>   # Switch subscription
   ```

4. **Bicep CLI installed**
   ```bash
   az bicep install      # Install Bicep
   az bicep version      # Verify installation
   ```
   Or use built-in: `az deployment group create` auto-compiles Bicep

### Deploy a Bicep File

```bash
az deployment group create \
  --resource-group <rg-name> \
  --template-file <path-to-bicep> \
  --parameters <params-file>.json
```

### Deploy an ARM Template

```bash
az deployment group create \
  --resource-group <rg-name> \
  --template-file <path-to-arm.json> \
  --parameters <params-file>.json
```

### Validate a Template (What-If)

```bash
az deployment group what-if \
  --resource-group <rg-name> \
  --template-file <path-to-bicep>
```

### Validate Syntax Only (Bicep)

```bash
az bicep build --file <bicep-file>
```

## Multi-Environment Deployments

Use parameter files for each environment:

```
params/
├── dev.bicepparam      # or dev.json
├── staging.bicepparam  # or staging.json
└── prod.bicepparam     # or prod.json
```

Deploy with environment:

```bash
az deployment group create \
  --resource-group <rg>-dev \
  --template-file main.bicep \
  --parameters @params/dev.json
```

## Azure Container Apps

See [references/container-apps.md](references/container-apps.md) for detailed Container App patterns including:
- Basic container deployment
- Ingress configuration
- Scaling rules
- revisions/versions

## Create New Resources

When asked to create Azure resources via Bicep:

1. Check if existing templates in `references/` match your need
2. For Container Apps: use the sample in `assets/container-app/`
3. For other resources: generate using `az bicep build-params --file` or reference Azure QuickStart Templates

## Scripts

Copy scripts from references or use directly:

- [references/deploy.md](references/deploy.md) — Deployment script with environment selection
- [references/validate.md](references/validate.md) — Validate and what-if
- [references/bicep-build.md](references/bicep-build.md) — Build Bicep to ARM

Quick deploy (copy-paste one-liner):
```bash
az deployment group create --resource-group <rg> --template-file main.bicep --parameters @params/dev.json
```