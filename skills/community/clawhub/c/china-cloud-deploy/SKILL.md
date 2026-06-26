---
name: china-cloud-deploy
description: "Deploy applications to Chinese cloud platforms (Tencent Cloud, Alibaba Cloud, Huawei Cloud) using their official CLIs. Teach AI agents how to deploy to SCF (Serverless), Lighthouse (VPS), OSS/COS (object storage), and Container Registry on China's three major cloud providers. Covers: Tencent Cloud SCF function deployment, Alibaba Cloud FC + OSS static hosting, Huawei Cloud FunctionGraph, cross-cloud deployment strategy, and ICP filing guidance. Triggers on: 中国云部署, china cloud deploy, 腾讯云部署, tencent cloud deploy, 阿里云部署, alibaba cloud deploy, 华为云部署, huawei cloud deploy, SCF部署, serverless china, 国内云服务部署, china serverless, ICP备案, icp filing, 国内VPS部署, china VPS deploy, COS上传, OSS上传, 中国云CLI, china cloud CLI"
---

# China Cloud Deploy - 中国云部署专家

You are an expert at deploying applications to China's three major cloud platforms using their official CLI tools. You handle the unique challenges of deploying in China: ICP filing, Great Firewall considerations, and platform-specific quirks.

## Core Philosophy

**Deploying in China is not just `deploy` — it's `ICP + deploy + CDN + monitor`.** Each step has regulatory requirements that don't exist elsewhere. You guide agents through the full pipeline.

## Platform Overview

| Platform | CLI | Install | Best For |
|----------|-----|---------|----------|
| Tencent Cloud | `tccli` | `pip install tccli` | SCF serverless, Lighthouse VPS, COS storage |
| Alibaba Cloud | `aliyun` | `pip install aliyun-python-cli` | FC serverless, OSS storage, ECS VPS |
| Huawei Cloud | `hcloud` | `pip install hcloud` | FunctionGraph, OBS storage, ECS VPS |

## Workflow 1: Tencent Cloud SCF (Serverless) Deployment

**When**: Deploy API/function as serverless on Tencent Cloud

### Setup
```bash
# Install CLI
pip install tccli

# Configure credentials
tccli configure
# SecretId: AKIDxxxxx
# SecretKey: xxxxxxx
# Region: ap-shanghai

# Verify
tccli scf ListFunctions --limit 1
```

### Deploy Function
```bash
# Step 1: Package function code
cd /path/to/function
zip -r function.zip index.js node_modules/  # Node.js
# or
zip -r function.zip main.py requirements.txt  # Python

# Step 2: Create or update function
tccli scf CreateFunction \
  --FunctionName "my-api" \
  --Runtime "Nodejs18.15" \
  --Handler "index.main" \
  --Code '{"ZipFile": "'$(base64 -w0 function.zip)'"}' \
  --Timeout 30 \
  --MemorySize 256

# Step 3: Create HTTP trigger (Function URL)
tccli scf CreateTrigger \
  --FunctionName "my-api" \
  --TriggerName "http-trigger" \
  --Type "http" \
  --TriggerDesc '{"AuthType":"NONE","NetConfig":{"EnableIntranet":false,"EnableExtranet":true}}'

# Step 4: Get function URL
tccli scf ListTriggers --FunctionName "my-api"
```

### Update Existing Function
```bash
# Update code only
tccli scf UpdateFunctionCode \
  --FunctionName "my-api" \
  --ZipFile "$(base64 -w0 function.zip)"

# Update configuration
tccli scf UpdateFunctionConfiguration \
  --FunctionName "my-api" \
  --Timeout 60 \
  --MemorySize 512 \
  --Environment '{"Variables":[{"Key":"NODE_ENV","Value":"production"}]}'
```

### SCF Layer for Dependencies
```bash
# Create layer for large dependencies
mkdir -p layer/nodejs && cd layer/nodejs
npm install express cors dotenv
cd ../.. && zip -r layer.zip layer/

tccli scf PublishLayerVersion \
  --LayerName "nodejs-deps" \
  --CompatibleRuntimes '["Nodejs18.15"]' \
  --Content '{"ZipFile": "'$(base64 -w0 layer.zip)'"}'

# Attach layer to function
tccli scf UpdateFunctionConfiguration \
  --FunctionName "my-api" \
  --Layers '[{"LayerName":"nodejs-deps","LayerVersion":1}]'
```

## Workflow 2: Alibaba Cloud FC + OSS Static Hosting

**When**: Deploy static site or SPA on Alibaba Cloud

### Setup
```bash
pip install aliyun-python-cli

aliyun configure
# AccessKey ID: LTAIxxxxx
# AccessKey Secret: xxxxxxx
# Region: cn-shanghai
```

### Static Site on OSS
```bash
# Step 1: Create OSS bucket
aliyun oss mb oss://my-static-site --region cn-shanghai

# Step 2: Set bucket to static website mode
aliyun oss website oss://my-static-site \
  --index-document index.html \
  --error-document 404.html

# Step 3: Upload built files
aliyun oss cp ./dist/ oss://my-static-site/ --recursive

# Step 4: Set public read
aliyun oss acl oss://my-static-site --acl public-read

# Step 5: Bind custom domain (requires ICP)
aliyun oss bucket-cname oss://my-static-site --domain www.example.com
```

### Serverless Function on FC
```bash
# Step 1: Deploy function using fun (FC CLI)
npm install -g fun

# Step 2: Create template.yml
cat > template.yml << 'EOF'
ROSTemplateFormatVersion: '2015-09-01'
Transform: 'Aliyun::Serverless-2018-04-03'
Resources:
  my-api:
    Type: 'Aliyun::Serverless::Service'
    handler:
      Type: 'Aliyun::Serverless::Function'
      Properties:
        Handler: index.main
        Runtime: nodejs18
        CodeUri: ./
        Timeout: 30
        MemorySize: 256
      Events:
        httpTrigger:
          Type: HTTP
          Properties:
            AuthType: ANONYMOUS
            Methods: ['GET', 'POST']
EOF

# Step 3: Deploy
fun deploy
```

## Workflow 3: Huawei Cloud FunctionGraph

**When**: Deploy on Huawei Cloud

```bash
# Install CLI
pip install hcloud

# Configure
hcloud configure
# AK: xxxxx
# SK: xxxxx
# Region: cn-north-4

# Deploy function
hcloud FunctionGraph CreateFunction \
  --function_name "my-api" \
  --runtime "Node.js18.17" \
  --handler "index.main" \
  --code_type "zip" \
  --func_code "$(base64 -w0 function.zip)"
```

## Workflow 4: Cross-Cloud Deployment Strategy

**When**: Need redundancy or multi-cloud architecture

### Decision Matrix
```
Use Case                    → Recommended Platform
─────────────────────────────────────────────────────
Serverless API              → Tencent SCF (best CLI) or Alibaba FC
Static Site                 → Alibaba OSS (cheapest CDN)
VPS / Long-running service  → Tencent Lighthouse (best value)
Container                   → Alibaba ACR + ECS
Database-heavy              → Alibaba (best RDS options)
Government/State client     → Huawei Cloud (compliance)
```

### Multi-Cloud Deploy Script
```bash
#!/bin/bash
# deploy-multi-cloud.sh
APP_NAME=$1
ENV=$2  # staging | prod

case $ENV in
  staging)
    # Deploy to Tencent SCF for testing
    tccli scf UpdateFunctionCode \
      --FunctionName "${APP_NAME}-staging" \
      --ZipFile "$(base64 -w0 function.zip)"
    echo "✅ Staging deployed to Tencent SCF"
    ;;
  prod)
    # Deploy to both Tencent and Alibaba for redundancy
    # Primary: Tencent SCF
    tccli scf UpdateFunctionCode \
      --FunctionName "${APP_NAME}" \
      --ZipFile "$(base64 -w0 function.zip)"
    echo "✅ Primary deployed to Tencent SCF"

    # Secondary: Alibaba FC
    fun deploy --stage prod
    echo "✅ Secondary deployed to Alibaba FC"

    # Update DNS weight (80% Tencent, 20% Alibaba)
    # ... DNS configuration
    ;;
esac
```

## Workflow 5: ICP Filing Guidance

**When**: Need to serve Chinese users with custom domain

**⚠️ ICP filing is legally required for any website hosted in mainland China.**

### ICP Filing Process
1. **Choose a cloud provider as filing agent** (must be same provider as server)
2. **Prepare documents**:
   - Business license or personal ID
   - Domain certificate (域名证书)
   - Server purchase proof
   - Website content description
3. **Submit via cloud provider's filing system**:
   - Tencent: https://console.cloud.tencent.com/beian
   - Alibaba: https://beian.aliyun.com
   - Huawei: https://beian.huaweicloud.com
4. **Wait 5-20 business days** for approval
5. **Add ICP number to website footer** after approval

### ICP Filing CLI Check
```bash
# Check if domain has ICP filing
curl -s "https://hlwicpfwc.miit.gov.cn/icpproject_query/api/project/queryByDomain" \
  -H "Content-Type: application/json" \
  -d '{"domain":"example.com"}'

# Quick check via tccli
tccli domain DescribeDomainBaseInfo --Domain example.com
```

### Without ICP Filing
If you don't have ICP filing:
- Use cloud provider's default domain (e.g., `xxx.ap-shanghai.run.tencentcloudapi.com`)
- Use Hong Kong/Macau server (no ICP required, but slower for mainland users)
- Use Function URL without custom domain binding

## Great Firewall Considerations

### What Gets Blocked
- Google services (gstatic, googleapis, firebase)
- GitHub raw content (sometimes)
- Foreign CDNs without China PoP
- WebSocket long connections (sometimes)
- Certain DNS resolutions

### Workarounds
```bash
# Replace Google Fonts with ChinaCDN
# Before: fonts.googleapis.com
# After:  fonts.loli.net or fonts.font.im

# Replace reCAPTCHA with Tencent Captcha
# Before: google.com/recaptcha
# After:  cloud.tencent.com/captcha

# Replace Firebase with Chinese alternatives
# Before: firebase.google.com
# After:  cloud.tencent.com (Tencent CloudBase)

# Check if your dependencies are accessible from China
npm config set registry https://registry.npmmirror.com  # Use China npm mirror
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple  # China PyPI mirror
```

## Safety Rules

1. **Never hardcode credentials**: Use environment variables or secret managers
2. **ICP compliance**: Never bind custom domain without ICP filing
3. **Data residency**: Keep Chinese user data in China regions
4. **Cost monitoring**: Set billing alerts — Chinese clouds charge for bandwidth aggressively
5. **Backup before deploy**: Always snapshot/backup before major changes
6. **Region selection**: Use regions closest to your users (Shanghai for East, Guangzhou for South)

## Quick Reference

```bash
# Tencent Cloud
tccli scf ListFunctions --limit 10
tccli scf UpdateFunctionCode --FunctionName xxx --ZipFile "$(base64 -w0 code.zip)"
tccli cos cp ./dist/ cos://bucket/ --recursive

# Alibaba Cloud
aliyun oss cp ./dist/ oss://bucket/ --recursive
fun deploy

# Huawei Cloud
hcloud FunctionGraph ListFunctions --limit 10
```
