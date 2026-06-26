# Azure Product Query Examples | Azure产品查询示例

This document provides practical examples demonstrating how to use the Azure Product Query Skill to retrieve comprehensive product information from official sources.

本文档提供实用示例，演示如何使用Azure产品查询技能从官方渠道获取全面的产品信息。

---

## Example 1: Single Product Query - Virtual Machines | 示例1：单个产品查询 - 虚拟机

### User Query | 用户查询
"Please help me query detailed information about Azure Virtual Machines, including specifications, pricing, and quick start guide."
"请帮我查询Azure虚拟机的详细信息，包括规格、定价和快速入门指南。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Product | 识别产品
- **Product Name**: Azure Virtual Machines | Azure虚拟机
- **Category**: Compute | 计算
- **Service Code**: virtual-machines
- **Official URL**: https://azure.microsoft.com/en-us/products/virtual-machines/

#### Step 2: Construct Search Queries | 构建搜索查询
```
site:azure.microsoft.com virtual-machines
site:learn.microsoft.com/azure/virtual-machines/overview
site:azure.microsoft.com/pricing/details/virtual-machines/
site:learn.microsoft.com/rest/api/compute/virtual-machines
```

#### Step 3: Retrieve Product Information | 获取产品信息

**Product Homepage**: https://azure.microsoft.com/en-us/products/virtual-machines/

**Key Information Extracted**:
- **Tagline**: Access cloud compute capacity and scale on demand—and only pay for the resources you use
- **Core Features**: Scalable, secure, customizable, hybrid capabilities
- **VM Series**: General purpose, compute optimized, memory optimized, storage optimized, GPU, high performance compute

#### Step 4: Retrieve Documentation | 获取技术文档

**Documentation URLs**:
- Overview: https://learn.microsoft.com/en-us/azure/virtual-machines/
- Quickstart: https://learn.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-cli
- REST API: https://learn.microsoft.com/en-us/rest/api/compute/virtual-machines

#### Step 5-7: Present Results | 呈现结果

```markdown
# Azure Virtual Machines | Azure虚拟机

## Overview | 产品概述

**Tagline**: 
Access cloud compute capacity and scale on demand—and only pay for the resources you use
/ 按需访问云计算容量并扩展规模——只为您使用的资源付费

**Description**:
Azure Virtual Machines (VM) is one of several types of on-demand, scalable computing resources that Azure offers. Typically, you choose a VM when you need more control over the computing environment than the other choices offer.

Azure虚拟机(VM)是Azure提供的多种按需、可扩展计算资源之一。通常，当您需要比其他选项更多的计算环境控制时，您会选择VM。

**Core Features**:
- **Scalable**: Scale up or down on demand, with millions of compute options
  / 可扩展：按需扩展或缩减，有数百万种计算选项
- **Secure**: Built-in security with Azure Security Center and Microsoft Defender
  / 安全：内置Azure安全中心和Microsoft Defender的安全功能
- **Customizable**: Choose from Linux or Windows, and multiple VM sizes and types
  / 可定制：从Linux或Windows中选择，多种VM大小和类型
- **Hybrid**: Extend your on-premises infrastructure to the cloud
  / 混合：将本地基础设施扩展到云端

**Use Cases**:
1. **Development and Testing**: Quickly create dev/test environments
   / 开发和测试：快速创建开发/测试环境
2. **Web Hosting**: Host websites and web applications
   / Web托管：托管网站和Web应用程序
3. **Enterprise Applications**: Run business-critical applications
   / 企业应用程序：运行业务关键型应用程序
4. **Big Data Analytics**: Process large datasets with HPC VMs
   / 大数据分析：使用HPC VM处理大型数据集
5. **AI and Machine Learning**: Train ML models with GPU VMs
   / AI和机器学习：使用GPU VM训练ML模型

---

## Specifications | 产品规格

### VM Series | VM系列
| Series | Type | Description | Use Case |
|--------|------|-------------|----------|
| D-series | General Purpose | Balanced CPU-to-memory ratio | Web servers, small databases |
| B-series | Burstable | Cost-effective with burst capability | Dev/test, low-traffic web |
| F-series | Compute Optimized | High CPU-to-memory ratio | Batch processing, gaming |
| E-series | Memory Optimized | High memory-to-CPU ratio | In-memory databases, SAP |
| Ls-series | Storage Optimized | High disk throughput and I/O | NoSQL databases, data warehousing |
| N-series | GPU | NVIDIA GPU-powered VMs | AI/ML, graphics rendering |
| H-series | High Performance Compute | Fastest and most powerful CPU | HPC, computational fluid dynamics |

### Supported Regions | 支持区域
- East US
- West US 2
- West Europe
- Southeast Asia
- Japan East
- Australia East
- China East 2 (Azure China)
- China North 2 (Azure China)

---

## Pricing | 定价信息

### Pricing Models | 计费模式
- **Pay-as-you-go**: Pay for compute capacity by the second with no long-term commitment
  / 按需付费：按秒支付计算容量费用，无需长期承诺
- **Reserved Instances**: Up to 72% discount compared to pay-as-you-go for 1 or 3-year terms
  / 预留实例：1年或3年期限，与按需付费相比最高可享72%折扣
- **Spot VMs**: Access unused Azure compute capacity at deep discounts (up to 90% off)
  / Spot虚拟机：以深度折扣（最高90%折扣）访问未使用的Azure计算容量
- **Azure Hybrid Benefit**: Use existing Windows Server and SQL Server licenses for additional savings
  / Azure混合权益：使用现有的Windows Server和SQL Server许可证获得额外节省

### Price Examples | 价格示例 (Linux, East US)
| VM Size | vCPU | Memory | Pay-as-you-go | Reserved (1yr) |
|---------|------|--------|---------------|----------------|
| B1s | 1 | 1 GiB | $0.0104/hr | $0.0062/hr |
| D2s_v5 | 2 | 8 GiB | $0.0960/hr | $0.0576/hr |
| E4s_v5 | 4 | 32 GiB | $0.2520/hr | $0.1512/hr |
| NC6s_v3 | 6 | 112 GiB + 1 V100 | $3.168/hr | N/A |

### Free Services | 免费服务
- 750 hours of B1s VM per month for 12 months (new customers)
- 新用户每月750小时B1s VM，为期12个月

---

## Quick Start | 快速入门

### Prerequisites | 前提条件
- Azure subscription
- Azure CLI or Azure PowerShell installed (optional)
- Resource group created

### Create VM via Azure Portal | 通过Azure门户创建VM
1. Sign in to Azure Portal
2. Navigate to Virtual Machines
3. Click "Create" → "Azure virtual machine"
4. Select subscription and resource group
5. Enter VM name and select region
6. Choose image (OS) and VM size
7. Configure authentication (SSH key or password)
8. Configure networking (VNet, subnet, public IP)
9. Review and create

### Create VM via Azure CLI | 通过Azure CLI创建VM
```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "<subscription-id>"

# Create resource group
az group create \
  --name myResourceGroup \
  --location eastus

# Create VM
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image Ubuntu2204 \
  --size Standard_D2s_v5 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard
```

### Create VM via Python SDK | 通过Python SDK创建VM
```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient

# Initialize credentials and clients
credential = DefaultAzureCredential()
subscription_id = '<subscription-id>'

compute_client = ComputeManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)
resource_client = ResourceManagementClient(credential, subscription_id)

# Create resource group
resource_client.resource_groups.create_or_update(
    'myResourceGroup',
    {'location': 'eastus'}
)

# Create VM
vm_parameters = {
    'location': 'eastus',
    'os_profile': {
        'computer_name': 'myVM',
        'admin_username': 'azureuser',
        'admin_password': '<admin-password>'
    },
    'hardware_profile': {
        'vm_size': 'Standard_D2s_v5'
    },
    'storage_profile': {
        'image_reference': {
            'publisher': 'Canonical',
            'offer': '0001-com-ubuntu-server-jammy',
            'sku': '22_04-lts-gen2',
            'version': 'latest'
        }
    },
    'network_profile': {
        'network_interfaces': [{
            'id': nic_id,
            'primary': True
        }]
    }
}

vm = compute_client.virtual_machines.begin_create_or_update(
    'myResourceGroup',
    'myVM',
    vm_parameters
).result()

print(f"VM created: {vm.name}")
```

### Connect to VM | 连接VM
- **Linux**: Use SSH
  ```bash
  ssh azureuser@<public-ip-address>
  ```
- **Windows**: Use RDP client

---

## Development Reference | 开发参考

### API Overview | API概览
**Base URL**: `https://management.azure.com`

**Common Operations**:
| Operation | API Endpoint | Description |
|-----------|-------------|-------------|
| Create/Update VM | PUT /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{name} | Create or update a VM |
| Get VM | GET /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{name} | Get VM details |
| Start VM | POST /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{name}/start | Start a VM |
| Stop VM | POST /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{name}/powerOff | Stop a VM |
| Delete VM | DELETE /subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{name} | Delete a VM |

### SDK Support | SDK支持
- **Python**: `azure-mgmt-compute`
- **.NET**: `Azure.ResourceManager.Compute`
- **Java**: `azure-mgmt-compute`
- **JavaScript**: `@azure/arm-compute`
- **Go**: `github.com/Azure/azure-sdk-for-go/sdk/resourcemanager/compute/armcompute`

---

## Related Resources | 相关资源

### Documentation | 文档链接
- [VM Documentation](https://learn.microsoft.com/en-us/azure/virtual-machines/)
- [VM Sizes](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/)
- [VM Pricing](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/)

### Related Products | 相关产品
- **Azure Virtual Network**: Network isolation for VMs
- **Azure Managed Disks**: Persistent block storage
- **Azure Load Balancer**: Distribute traffic across VMs
- **Azure Monitor**: Monitor VM metrics and logs
- **Azure Backup**: Backup and restore VMs
- **Azure Site Recovery**: Disaster recovery for VMs
```

---

## Example 2: Product Comparison - Azure SQL Database vs SQL Managed Instance | 示例2：产品对比 - Azure SQL Database vs SQL托管实例

### User Query | 用户查询
"What's the difference between Azure SQL Database and SQL Managed Instance? Which one should I choose?"
"Azure SQL数据库和SQL托管实例有什么区别？我应该选择哪个？"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Products | 识别产品
- **Product A**: Azure SQL Database | Azure SQL数据库
- **Product B**: Azure SQL Managed Instance | Azure SQL托管实例
- **Category**: Databases | 数据库

#### Step 7: Present Comparison Results | 呈现对比结果

```markdown
# Azure SQL Database vs Azure SQL Managed Instance | Product Comparison

## Overview Comparison | 概览对比

| Aspect | Azure SQL Database | Azure SQL Managed Instance |
|--------|-------------------|---------------------------|
| **Deployment Model** | Single database or elastic pool | Instance with multiple databases |
| **SQL Server Compatibility** | Partial (most features) | Near 100% compatibility |
| **Instance-level Features** | Limited | Full support (SQL Agent, CLR, etc.) |
| **Migration Complexity** | May require app changes | Lift-and-shift migration |
| **Management Overhead** | Low (fully managed) | Low (fully managed) |
| **Pricing Model** | DTU or vCore based | vCore based only |

## Detailed Comparison | 详细对比

### 1. Architecture | 架构

**Azure SQL Database**:
- Single database: One database per server
- Elastic pool: Multiple databases sharing resources
- Serverless option: Auto-scaling, pay-per-second
- Hyperscale: For very large databases (up to 100TB)

**Azure SQL Managed Instance**:
- Full SQL Server instance in the cloud
- Supports multiple databases per instance
- Includes SQL Agent, Database Mail, Linked Servers
- Supports cross-database queries and transactions

### 2. Features | 功能

| Feature | SQL Database | SQL Managed Instance |
|---------|-------------|---------------------|
| SQL Server Agent | ❌ | ✅ |
| CLR Integration | ❌ | ✅ |
| Database Mail | ❌ | ✅ |
| Linked Servers | Limited | ✅ |
| Service Broker | ✅ | ✅ |
| Always Encrypted | ✅ | ✅ |
| Row-Level Security | ✅ | ✅ |
| Dynamic Data Masking | ✅ | ✅ |
| Auditing | ✅ | ✅ |

### 3. Migration Scenarios | 迁移场景

**Choose SQL Database when | 选择SQL数据库的场景**:
- Building new cloud-native applications
- Need elastic pool for multiple databases with varying usage
- Want serverless for intermittent workloads
- Don't need instance-level features
- Cost optimization is important

**Choose SQL Managed Instance when | 选择SQL托管实例的场景**:
- Migrating existing SQL Server workloads
- Need instance-level features (Agent, CLR, etc.)
- Require cross-database queries
- Want minimal application changes
- Need near 100% SQL Server compatibility

### 4. Pricing | 定价

| Model | SQL Database | SQL Managed Instance |
|-------|-------------|---------------------|
| DTU-based | ✅ (Single DB/Elastic Pool) | ❌ |
| vCore-based | ✅ | ✅ |
| Serverless | ✅ | ❌ |
| Hyperscale | ✅ | ❌ |
| Business Critical | ✅ | ✅ |
| General Purpose | ✅ | ✅ |

## Recommendation | 选择建议

### For New Cloud Applications | 新建云应用
**推荐**: Azure SQL Database
- Lower cost for simple scenarios
- More deployment options (Serverless, Hyperscale)
- Better integration with PaaS services

### For SQL Server Migration | SQL Server迁移
**推荐**: Azure SQL Managed Instance
- Minimal code changes required
- Full feature parity with on-premises SQL Server
- Easier lift-and-shift migration
```

---

## Example 3: Pricing Analysis - Blob Storage | 示例3：定价分析 - Blob存储

### User Query | 用户查询
"I want to understand Azure Blob Storage pricing details, including storage costs, data transfer fees, and operation charges."
"我想了解Azure Blob存储的定价详情，包括存储费用、数据传输费和操作费用。"

### Skill Execution Steps | 技能执行步骤

#### Step 3-7: Present Pricing Analysis | 呈现定价分析

```markdown
# Azure Blob Storage Pricing Analysis | Blob存储定价分析

## Pricing Components | 计费组成

### 1. Storage Pricing | 存储定价

| Access Tier | Price (per GB/month) | Use Case |
|------------|---------------------|----------|
| Hot | $0.0184 | Frequently accessed data |
| Cool | $0.0100 | Infrequently accessed data (stored 30+ days) |
| Archive | $0.00099 | Rarely accessed data (stored 180+ days) |

### 2. Operation and Data Transfer Pricing | 操作和数据传输定价

| Operation Type | Price (per 10,000 operations) |
|---------------|------------------------------|
| Write operations (Hot) | $0.05 |
| Write operations (Cool) | $0.10 |
| Write operations (Archive) | $0.10 |
| Read operations (Hot) | $0.004 |
| Read operations (Cool) | $0.01 |
| Read operations (Archive) | $5.00 |
| List/Create Container operations | $0.05 |

**Data Transfer**:
- Data ingress: Free
- Data egress (first 5GB/month): Free
- Data egress (beyond 5GB): $0.087 per GB

### 3. Data Retrieval and Early Deletion | 数据取回和提前删除

| Tier | Retrieval Fee | Early Deletion Period |
|------|--------------|----------------------|
| Cool | $0.01 per GB | 30 days |
| Archive | $0.022 per GB | 180 days |

---

## Cost Calculation Example | 成本计算示例

### Scenario | 场景
- Storage: 10 TB in Hot tier, 5 TB in Cool tier
- Monthly operations: 10 million (8M reads, 2M writes)
- Data egress: 2 TB per month

### Calculation | 计算

| Component | Calculation | Cost |
|-----------|-------------|------|
| Hot Storage | 10,000 GB × $0.0184 | $184.00 |
| Cool Storage | 5,000 GB × $0.0100 | $50.00 |
| Read Operations | 8,000,000 ÷ 10,000 × $0.004 | $3.20 |
| Write Operations | 2,000,000 ÷ 10,000 × $0.05 | $10.00 |
| Data Egress | (2,048 GB - 5 GB free) × $0.087 | $177.74 |
| **Monthly Total** | | **~$425/month** |

---

## Cost Optimization Strategies | 成本优化策略

### 1. Access Tier Optimization | 访问层级优化
- Use lifecycle management policies to automate tier transitions
- Move data to Cool tier after 30 days of no access
- Archive old data that won't be needed for 6+ months
- Potential savings: 40-90%

### 2. Reserved Capacity | 预留容量
- Purchase reserved capacity for 1 or 3 years
- Up to 38% discount for storage
- Best for predictable storage needs

### 3. Data Transfer Optimization | 数据传输优化
- Use CDN (Azure Front Door) for content delivery
- Keep data transfers within the same region when possible
- Use Azure Private Link for internal transfers

### 4. Free Tier Utilization | 免费套餐利用
- 5 GB LRS Hot blob storage with 20,000 read and 10,000 write operations for 12 months
- Always free: 5,000 read and 1,000 write operations per month
```

---

## Example 4: API Integration - Creating Azure Functions | 示例4：API集成 - 创建Azure函数

### User Query | 用户查询
"I need to create an Azure Function using API. Please provide complete code examples."
"我需要使用API创建Azure函数，请提供完整的代码示例。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Product | 识别产品
- **Product Name**: Azure Functions | Azure函数
- **Service Code**: azure-functions
- **Category**: Compute | 计算

#### Step 3-7: Present API Integration Guide | 呈现API集成指南

```markdown
# Azure Functions API Integration Guide | Azure函数API集成指南

## Prerequisites | 前提条件

1. Azure subscription
2. Service Principal with Contributor role
3. Resource group created
4. Storage account for function app

## API Overview | API概览

**Base URL**: `https://management.azure.com`

**Authentication**: Azure AD OAuth 2.0

## Code Examples | 代码示例

### Python SDK Example

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.web import WebSiteManagementClient

# Initialize credentials
credential = DefaultAzureCredential()
subscription_id = '<subscription-id>'

# Create clients
resource_client = ResourceManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)
web_client = WebSiteManagementClient(credential, subscription_id)

resource_group = 'myResourceGroup'
location = 'eastus'
function_app_name = 'my-function-app-123'
storage_account_name = 'myfuncstorage123'

# Create storage account
storage_async_operation = storage_client.storage_accounts.begin_create(
    resource_group,
    storage_account_name,
    {
        'location': location,
        'sku': {'name': 'Standard_LRS'},
        'kind': 'StorageV2'
    }
)
storage_account = storage_async_operation.result()

# Get storage connection string
keys = storage_client.storage_accounts.list_keys(resource_group, storage_account_name)
storage_connection_string = f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={keys.keys[0].value};EndpointSuffix=core.windows.net"

# Create function app
function_app = web_client.web_apps.begin_create_or_update(
    resource_group,
    function_app_name,
    {
        'location': location,
        'kind': 'functionapp',
        'site_config': {
            'app_settings': [
                {'name': 'FUNCTIONS_WORKER_RUNTIME', 'value': 'python'},
                {'name': 'FUNCTIONS_EXTENSION_VERSION', 'value': '~4'},
                {'name': 'AzureWebJobsStorage', 'value': storage_connection_string}
            ]
        }
    }
).result()

print(f"Function app created: {function_app.default_host_name}")
```

### Deploy Function Code | 部署函数代码

```python
import requests
import zipfile
import io

# Create deployment package
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
    # Add function code
    function_code = '''
import logging
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    
    if name:
        return func.HttpResponse(f"Hello, {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )
'''
    zip_file.writestr('HttpTrigger/__init__.py', function_code)
    
    # Add function.json
    function_json = '''
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get", "post"]
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    }
  ]
}
'''
    zip_file.writestr('HttpTrigger/function.json', function_json)

zip_buffer.seek(0)

# Deploy using Azure REST API
import json

access_token = credential.get_token("https://management.azure.com/.default").token

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/zip'
}

url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Web/sites/{function_app_name}/zipdeploy?api-version=2022-03-01"

response = requests.post(url, headers=headers, data=zip_buffer.getvalue())
print(f"Deployment status: {response.status_code}")
```

### Azure CLI Example

```bash
# Create resource group
az group create \
  --name myResourceGroup \
  --location eastus

# Create storage account
az storage account create \
  --name myfuncstorage123 \
  --location eastus \
  --resource-group myResourceGroup \
  --sku Standard_LRS

# Get storage connection string
storage_conn_string=$(az storage account show-connection-string \
  --name myfuncstorage123 \
  --resource-group myResourceGroup \
  --query connectionString \
  --output tsv)

# Create function app
az functionapp create \
  --resource-group myResourceGroup \
  --name my-function-app-123 \
  --storage-account myfuncstorage123 \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4

# Deploy function code
func azure functionapp publish my-function-app-123
```

## Common Operations | 常用操作

| Operation | Azure CLI | Description |
|-----------|-----------|-------------|
| Create Function App | `az functionapp create` | Create a new function app |
| List Functions | `az functionapp function list` | List all functions |
| Delete Function App | `az functionapp delete` | Delete function app |
| Show Function App | `az functionapp show` | Get function app details |
| Restart Function App | `az functionapp restart` | Restart the function app |

## Related Resources | 相关资源

- [Azure Functions Documentation](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Functions Triggers and Bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings/)
- [Functions Pricing](https://azure.microsoft.com/en-us/pricing/details/functions/)
```

---

## Example 5: Architecture Recommendation - Serverless Web App | 示例5：架构推荐 - 无服务器Web应用

### User Query | 用户查询
"I need to design a serverless web application architecture on Azure, including frontend, backend, database, and storage."
"我需要为Azure上的无服务器Web应用设计架构，包括前端、后端、数据库和存储。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Required Products | 识别所需产品
- **Frontend**: Azure Static Web Apps + Azure CDN
- **Backend**: Azure Functions + API Management
- **Database**: Azure Cosmos DB
- **Storage**: Blob Storage
- **Authentication**: Azure AD B2C
- **Monitoring**: Application Insights

#### Step 3-7: Present Architecture Recommendation | 呈现架构推荐

```markdown
# Serverless Web Application on Azure | Azure无服务器Web应用

## Architecture Overview | 架构概览

```
                    [Users]
                      |
                      v
              [Azure CDN / Front Door]
                      |
                      v
        [Azure Static Web Apps]
                      |
        +-------------+-------------+
        |                           |
        v                           v
[Static Content]          [API Management]
                                  |
                                  v
                          [Azure Functions]
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
            [Azure Cosmos DB]          [Blob Storage]
            (User Data)                (File Storage)
                    |
                    v
            [Azure AD B2C]
            (Authentication)
```

## Component Details | 组件详情

### 1. Frontend Hosting | 前端托管

**Product**: Azure Static Web Apps + Azure CDN

**Configuration**:
- Static Web Apps for React/Vue/Angular apps
- Azure CDN for global content delivery
- Custom domain with free SSL
- GitHub/ADO integration for CI/CD

**Pricing**:
- Static Web Apps: Free tier (100GB bandwidth), Standard ($9/month)
- CDN: $0.087/GB outbound transfer

### 2. API Layer | API层

**Product**: Azure API Management + Azure Functions

**Configuration**:
- API Management for API gateway (rate limiting, caching)
- Azure Functions for serverless compute
- HTTP triggers for REST API endpoints
- Consumption plan for pay-per-execution

**Pricing**:
- API Management: Developer ($48/month), Basic ($147/month)
- Functions: Free tier (1M executions), $0.20/million executions after

### 3. Database | 数据库

**Product**: Azure Cosmos DB (Serverless)

**Configuration**:
- Serverless mode for variable traffic
- SQL API for document storage
- Global distribution (optional)
- Point-in-time backup

**Pricing**:
- Serverless: $0.25/million RU-seconds
- Storage: $0.25/GB/month

### 4. Storage | 存储

**Product**: Azure Blob Storage (Hot tier)

**Configuration**:
- Hot tier for user uploads
- SAS tokens for secure access
- Lifecycle policies for cost optimization

**Pricing**:
- Storage: $0.0184/GB/month
- Operations: $0.004-$0.05 per 10,000 operations

### 5. Authentication | 身份验证

**Product**: Azure AD B2C

**Configuration**:
- User sign-up/sign-in flows
- Social identity providers (Google, Facebook)
- Custom policies for advanced scenarios

**Pricing**:
- First 50,000 authentications/month free
- $0.032 per 1,000 authentications after

### 6. Monitoring | 监控

**Product**: Application Insights + Azure Monitor

**Configuration**:
- Application performance monitoring
- Distributed tracing
- Custom dashboards and alerts

**Pricing**:
- $2.88/GB data ingested
- First 5GB/month free

## Cost Summary | 成本汇总

### Monthly Estimate (100,000 requests/month) | 月度估算

| Component | Configuration | Monthly Cost |
|-----------|--------------|--------------|
| Static Web Apps | Standard | $9.00 |
| CDN | 100 GB | $8.70 |
| API Management | Basic | $147.00 |
| Functions | 100K executions | Free |
| Cosmos DB | Serverless + 10GB | ~$25.00 |
| Blob Storage | 50 GB + operations | ~$5.00 |
| AD B2C | 1,000 users | Free |
| Application Insights | < 5GB | Free |
| **Total** | | **~$195/month** |

## Scaling Considerations | 扩展考虑

### Automatic Scaling | 自动扩展
- Static Web Apps: Automatic global CDN scaling
- Functions: Automatic scaling from 0 to thousands of instances
- Cosmos DB: Automatic RU scaling in serverless mode
- API Management: Auto-scale based on CPU/memory

### Cost Optimization | 成本优化
- Use Static Web Apps free tier for development
- Implement caching in API Management
- Use Cosmos DB partial document updates to reduce RU
- Monitor with Application Insights cost caps

### Security Best Practices | 安全最佳实践
- Use Managed Identity for Functions to access Cosmos DB
- Enable WAF on API Management
- Use SAS tokens with expiration for Blob Storage
- Enable continuous export of security logs

## Related Products | 相关产品

- **Azure Key Vault**: Secure secrets management
- **Azure Service Bus**: Async messaging
- **Azure Event Grid**: Event-driven architecture
- **Azure Logic Apps**: Workflow automation
```

---

## Summary | 总结

These examples demonstrate the complete workflow of the Azure Product Query Skill:

1. **Single Product Query**: Deep dive into one product with full specifications, pricing, and usage guides
2. **Product Comparison**: Side-by-side analysis of similar products for informed decision-making
3. **Pricing Analysis**: Detailed cost breakdown with optimization strategies
4. **API Integration**: Complete code examples for programmatic access
5. **Architecture Design**: Multi-product solution architecture with cost estimates

When using this skill, always:
- Use `WebSearch` to find official documentation URLs
- Use `WebFetch` or `Browser Navigate` to retrieve detailed content
- Cross-reference multiple sources for accuracy
- Provide bilingual (Chinese/English) output when appropriate
- Include credential placeholders in all code examples
