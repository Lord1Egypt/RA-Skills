# AWS Product Query Examples | AWS产品查询示例

This document provides practical examples demonstrating how to use the AWS Product Query Skill to retrieve comprehensive product information from official sources.

本文档提供实用示例，演示如何使用AWS产品查询技能从官方渠道获取全面的产品信息。

---

## Example 1: Single Product Query - EC2 | 示例1：单个产品查询 - EC2

### User Query | 用户查询
"Please help me query detailed information about AWS EC2, including specifications, pricing, and quick start guide."
"请帮我查询AWS EC2的详细信息，包括规格、定价和快速入门指南。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Product | 识别产品
- **Product Name**: Amazon EC2 | 弹性计算云
- **Category**: Compute | 计算
- **Service Code**: ec2
- **Official URL**: https://aws.amazon.com/ec2/

#### Step 2: Construct Search Queries | 构建搜索查询
```
site:aws.amazon.com/ec2/
site:docs.aws.amazon.com/ec2 what is
site:docs.aws.amazon.com/ec2 getting started
site:aws.amazon.com/ec2 pricing
site:docs.aws.amazon.com/ec2 API reference
```

#### Step 3: Retrieve Product Information | 获取产品信息

**Product Homepage**: https://aws.amazon.com/ec2/

**Key Information Extracted**:
- **Tagline**: Secure and resizable compute capacity for virtually any workload
- **Core Features**: Elastic scaling, broad selection, secure, cost-effective
- **Instance Families**: General purpose, compute optimized, memory optimized, storage optimized, accelerated computing

#### Step 4: Retrieve Documentation | 获取技术文档

**Documentation URLs**:
- User Guide: https://docs.aws.amazon.com/ec2/latest/userguide/
- API Reference: https://docs.aws.amazon.com/ec2/latest/APIReference/
- Pricing: https://aws.amazon.com/ec2/pricing/

#### Step 5-7: Present Results | 呈现结果

```markdown
# Amazon EC2 | 弹性计算云

## Overview | 产品概述

**Tagline**: 
Secure and resizable compute capacity for virtually any workload
/ 为几乎所有工作负载提供安全且可调整大小的计算容量

**Description**:
Amazon Elastic Compute Cloud (Amazon EC2) provides on-demand, scalable computing capacity in the AWS Cloud. It allows you to provision virtual servers (instances) in minutes and scale capacity up or down as needed.

Amazon EC2在AWS云中提供按需、可扩展的计算容量。它允许您在几分钟内配置虚拟服务器（实例），并根据需要扩展或缩减容量。

**Core Features**:
- **Elastic Web-Scale Computing**: Scale capacity in minutes, not hours or days
  / 弹性Web规模计算：在几分钟内扩展容量，而不是几小时或几天
- **Completely Controlled**: You have root access to each instance
  / 完全控制：您可以对每个实例进行根访问
- **Flexible Cloud Hosting**: Choose from multiple instance types, OS, and software packages
  / 灵活的云托管：从多种实例类型、操作系统和软件包中选择
- **Integrated**: Integrated with most AWS services
  / 集成：与大多数AWS服务集成
- **Reliable**: Runs on AWS's proven network infrastructure and data centers
  / 可靠：运行在AWS经过验证的网络基础设施和数据中心上

**Use Cases**:
1. **Web Hosting**: Host websites and web applications
   / Web托管：托管网站和Web应用程序
2. **Enterprise Applications**: Run business-critical applications
   / 企业应用程序：运行业务关键型应用程序
3. **Development and Test**: Quickly provision and release resources
   / 开发和测试：快速配置和释放资源
4. **Big Data Analytics**: Process large datasets
   / 大数据分析：处理大型数据集
5. **Machine Learning**: Train and deploy ML models
   / 机器学习：训练和部署ML模型

---

## Specifications | 产品规格

### Instance Families | 实例规格族
| Family | Type | Description | Use Case |
|--------|------|-------------|----------|
| General Purpose | T4g, M6g, M6i | Balanced compute, memory, and networking | Web servers, small databases |
| Compute Optimized | C6g, C6i | High CPU performance | Batch processing, gaming |
| Memory Optimized | R6g, R6i, X2i | High memory capacity | In-memory databases, caching |
| Storage Optimized | I4i, D3 | High disk I/O | NoSQL databases, data warehousing |
| Accelerated Computing | P4, G5, Inf2 | GPU/FPGA/ASIC | ML training, graphics rendering |

### Supported Regions | 支持区域
- US East (N. Virginia) - us-east-1
- US West (Oregon) - us-west-2
- Europe (Ireland) - eu-west-1
- Asia Pacific (Tokyo) - ap-northeast-1
- Asia Pacific (Singapore) - ap-southeast-1
- China (Beijing) - cn-north-1
- China (Ningxia) - cn-northwest-1

---

## Pricing | 定价信息

### Pricing Models | 计费模式
- **On-Demand**: Pay for compute capacity by the hour or second with no long-term commitments
  / 按需：按小时或秒支付计算容量费用，无需长期承诺
- **Reserved Instances**: Significant discount (up to 72%) compared to On-Demand pricing
  / 预留实例：与按需定价相比，可享受大幅折扣（高达72%）
- **Spot Instances**: Request spare EC2 computing capacity for up to 90% off On-Demand price
  / Spot实例：请求 spare EC2计算容量，最高可享受按需价格90%的折扣
- **Savings Plans**: Flexible pricing model offering low prices on EC2 usage
  / 节省计划：灵活的定价模式，为EC2使用提供低价

### Price Examples | 价格示例 (us-east-1)
| Instance Type | vCPU | Memory | On-Demand | Reserved (1yr) |
|--------------|------|--------|-----------|----------------|
| t3.micro | 2 | 1 GiB | $0.0104/hr | $0.0065/hr |
| m6i.large | 2 | 8 GiB | $0.0864/hr | $0.0544/hr |
| c6i.xlarge | 4 | 8 GiB | $0.1700/hr | $0.1071/hr |

### Free Tier | 免费套餐
- 750 hours of t2.micro or t3.micro instances per month for 12 months
- 每月750小时的t2.micro或t3.micro实例，为期12个月

---

## Quick Start | 快速入门

### Prerequisites | 前提条件
- AWS account registered
- IAM permissions for EC2 operations
- VPC and subnet configured (default VPC available)

### Launch EC2 Instance | 启动EC2实例

**Via AWS Console**:
1. Sign in to AWS Management Console
2. Navigate to EC2 Dashboard
3. Click "Launch Instance"
4. Select Amazon Machine Image (AMI)
5. Choose instance type
6. Configure instance details (VPC, subnet, IAM role)
7. Add storage
8. Configure security group
9. Review and launch

**Via AWS CLI**:
```bash
aws ec2 run-instances \
  --image-id ami-12345678 \
  --instance-type t3.micro \
  --key-name MyKeyPair \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyInstance}]'
```

**Via Python SDK (Boto3)**:
```python
import boto3

ec2 = boto3.client(
    'ec2',
    aws_access_key_id='<your-access-key-id>',
    aws_secret_access_key='<your-secret-access-key>',
    region_name='us-east-1'
)

response = ec2.run_instances(
    ImageId='ami-12345678',
    InstanceType='t3.micro',
    MinCount=1,
    MaxCount=1,
    KeyName='MyKeyPair',
    SecurityGroupIds=['sg-12345678'],
    SubnetId='subnet-12345678',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'MyInstance'}
            ]
        }
    ]
)

print(f"Instance created: {response['Instances'][0]['InstanceId']}")
```

### Connect to Instance | 连接实例
- **Linux**: Use SSH with key pair
  ```bash
  ssh -i MyKeyPair.pem ec2-user@<instance-public-ip>
  ```
- **Windows**: Use RDP client with administrator credentials

---

## Development Reference | 开发参考

### API Overview | API概览
**Service Endpoint**: `https://ec2.<region>.amazonaws.com`

**Common Operations**:
| Operation | API Action | Description |
|-----------|-----------|-------------|
| Run Instances | RunInstances | Launch new EC2 instances |
| Describe Instances | DescribeInstances | Query instance details |
| Start Instances | StartInstances | Start stopped instances |
| Stop Instances | StopInstances | Stop running instances |
| Terminate Instances | TerminateInstances | Terminate instances |
| Modify Instance Attribute | ModifyInstanceAttribute | Change instance settings |

### SDK Support | SDK支持
- **Python**: `boto3`
- **Java**: `aws-sdk-java-v2`
- **Go**: `aws-sdk-go-v2`
- **Node.js**: `aws-sdk-js-v3`
- **.NET**: `aws-sdk-net`

---

## Related Resources | 相关资源

### Documentation | 文档链接
- [EC2 User Guide](https://docs.aws.amazon.com/ec2/latest/userguide/)
- [EC2 API Reference](https://docs.aws.amazon.com/ec2/latest/APIReference/)
- [EC2 Pricing](https://aws.amazon.com/ec2/pricing/)

### Related Products | 相关产品
- **Amazon VPC**: Network isolation for EC2 instances
- **Amazon EBS**: Persistent block storage
- **Elastic Load Balancing**: Distribute traffic across instances
- **Amazon CloudWatch**: Monitor instance metrics
- **AWS Auto Scaling**: Automatic capacity scaling
```

---

## Example 2: Product Comparison - RDS vs Aurora | 示例2：产品对比 - RDS vs Aurora

### User Query | 用户查询
"What's the difference between AWS RDS and Aurora? Which one should I choose?"
"AWS RDS和Aurora有什么区别？我应该选择哪个？"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Products | 识别产品
- **Product A**: Amazon RDS | 关系型数据库服务
- **Product B**: Amazon Aurora | Aurora数据库
- **Category**: Database | 数据库

#### Step 2: Construct Comparison Queries | 构建对比查询
```
site:aws.amazon.com/rds/
site:aws.amazon.com/rds/aurora/
site:docs.aws.amazon.com/rds what is
site:docs.aws.amazon.com/aurora what is
```

#### Step 7: Present Comparison Results | 呈现对比结果

```markdown
# Amazon RDS vs Amazon Aurora | Product Comparison

## Overview Comparison | 概览对比

| Aspect | Amazon RDS | Amazon Aurora |
|--------|-----------|---------------|
| **Database Engines** | MySQL, PostgreSQL, MariaDB, Oracle, SQL Server | Aurora MySQL, Aurora PostgreSQL |
| **Performance** | Standard performance | Up to 5x faster than MySQL, 3x faster than PostgreSQL |
| **Scalability** | Vertical scaling, read replicas | Auto-scaling storage, up to 15 read replicas |
| **Availability** | Multi-AZ deployment | 99.99% availability, self-healing storage |
| **Storage** | Provisioned storage | Auto-scaling up to 128TB |

## Detailed Comparison | 详细对比

### 1. Performance | 性能

**Amazon RDS**:
- Standard database performance
- Depends on instance size and storage type
- Manual optimization required

**Amazon Aurora**:
- Up to 5x faster than standard MySQL
- Up to 3x faster than standard PostgreSQL
- Distributed, fault-tolerant, self-healing storage system
- Automatic performance optimization

### 2. Scalability | 扩展性

| Feature | RDS | Aurora |
|---------|-----|--------|
| Compute Scaling | Vertical (instance upgrade) | Vertical + Aurora Serverless option |
| Storage Scaling | Manual, up to 64TB | Automatic, up to 128TB |
| Read Replicas | Up to 5 | Up to 15 |
| Cross-Region Replication | Supported | Aurora Global Database |

### 3. Availability & Durability | 可用性与持久性

**Amazon RDS**:
- Multi-AZ deployment for high availability
- Automated backups
- Manual failover (typically 60-120 seconds)

**Amazon Aurora**:
- 99.99% availability SLA
- Self-healing storage (6 copies across 3 AZs)
- Automatic failover (typically < 30 seconds)
- Continuous backup to S3

### 4. Pricing | 定价

| Component | RDS | Aurora |
|-----------|-----|--------|
| Instance Cost | Lower | Higher (but better performance per dollar) |
| Storage Cost | Provisioned IOPS/GB | IO-Optimized or Standard (auto-scaling) |
| I/O Cost | Included with provisioned IOPS | Charged separately for Standard, included for IO-Optimized |

## Recommendation | 选择建议

### Choose RDS when | 选择RDS的场景:
- You need specific database engines (Oracle, SQL Server, MariaDB)
- Cost is the primary concern
- Standard performance is sufficient
- You prefer more control over database configuration

### Choose Aurora when | 选择Aurora的场景:
- You use MySQL or PostgreSQL
- High performance and scalability are required
- Need enterprise-grade availability
- Want to reduce database management overhead
- Global application requiring cross-region replication
```

---

## Example 3: Pricing Analysis - S3 | 示例3：定价分析 - S3

### User Query | 用户查询
"I want to understand AWS S3 pricing details, including storage costs, data transfer fees, and request charges."
"我想了解AWS S3的定价详情，包括存储费用、数据传输费和请求费用。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Product | 识别产品
- **Product Name**: Amazon S3 | 简单存储服务
- **Service Code**: s3
- **Category**: Storage | 存储

#### Step 2: Construct Pricing Queries | 构建定价查询
```
site:aws.amazon.com/s3/pricing/
site:docs.aws.amazon.com/s3 pricing
```

#### Step 3-7: Present Pricing Analysis | 呈现定价分析

```markdown
# Amazon S3 Pricing Analysis | S3定价分析

## Pricing Components | 计费组成

### 1. Storage Pricing | 存储定价

| Storage Class | Price (per GB/month) | Use Case |
|--------------|---------------------|----------|
| S3 Standard | $0.023 | Frequently accessed data |
| S3 Intelligent-Tiering | $0.023 (frequent), $0.0125 (infrequent) | Unknown or changing access patterns |
| S3 Standard-IA | $0.0125 | Infrequently accessed data |
| S3 One Zone-IA | $0.010 | Infrequently accessed, non-critical data |
| S3 Glacier Instant Retrieval | $0.004 | Archive data with instant retrieval |
| S3 Glacier Flexible Retrieval | $0.0036 | Archive data (minutes to hours retrieval) |
| S3 Glacier Deep Archive | $0.00099 | Long-term archive (12-48 hours retrieval) |

### 2. Request & Data Retrieval Pricing | 请求和数据取回定价

| Request Type | Price (per 1,000 requests) |
|-------------|---------------------------|
| PUT, COPY, POST, LIST | $0.005 |
| GET, SELECT, and all other requests | $0.0004 |
| DELETE requests | Free |
| Glacier Instant Retrieval | $0.01 per GB |
| Glacier Flexible Retrieval | $0.01-$0.02 per GB (depending on speed) |
| Glacier Deep Archive | $0.02-$0.10 per GB |

### 3. Data Transfer Pricing | 数据传输定价

| Transfer Type | Price |
|--------------|-------|
| Data transfer IN to S3 | Free |
| Data transfer OUT to Internet | First 100GB/month free, then $0.09/GB |
| Data transfer OUT to CloudFront | Free |
| Data transfer OUT to same region EC2 | Free |
| Cross-region replication | $0.02/GB |

### 4. Additional Features | 附加功能定价

| Feature | Price |
|---------|-------|
| S3 Transfer Acceleration | $0.04/GB (accelerated) |
| S3 Object Lock | No additional charge |
| S3 Versioning | Storage for each version |
| S3 Lifecycle transitions | $0.0004 per 1,000 requests |

---

## Cost Calculation Example | 成本计算示例

### Scenario | 场景
- Storage: 10 TB S3 Standard
- Monthly data transfer out: 5 TB
- Monthly requests: 10 million (8M GET, 2M PUT)
- Lifecycle transition: 2 TB to Glacier after 90 days

### Calculation | 计算

| Component | Calculation | Cost |
|-----------|-------------|------|
| Storage (Standard) | 10,000 GB × $0.023 | $230 |
| Data Transfer Out | 5,000 GB × $0.09 | $450 |
| GET Requests | 8,000,000 ÷ 1,000 × $0.0004 | $3.20 |
| PUT Requests | 2,000,000 ÷ 1,000 × $0.005 | $10 |
| **Monthly Total** | | **$693.20** |

---

## Cost Optimization Strategies | 成本优化策略

### 1. Storage Class Optimization | 存储类型优化
- Use S3 Intelligent-Tiering for unknown access patterns
- Move infrequently accessed data to S3 Standard-IA
- Archive old data to Glacier classes
- Potential savings: 40-90%

### 2. Data Transfer Optimization | 数据传输优化
- Use CloudFront for content delivery (reduces data transfer costs)
- Keep data transfers within the same region when possible
- Use S3 Transfer Acceleration only when necessary

### 3. Request Optimization | 请求优化
- Batch operations to reduce request count
- Use multipart upload for large files
- Implement client-side caching

### 4. Free Tier Utilization | 免费套餐利用
- 5 GB of Standard storage
- 20,000 GET requests
- 2,000 PUT requests
- 100 GB data transfer out to internet

---

## Pricing Calculator | 定价计算器

Use the AWS Pricing Calculator for accurate estimates:
[AWS Pricing Calculator](https://calculator.aws/)

For detailed pricing, refer to:
[Amazon S3 Pricing](https://aws.amazon.com/s3/pricing/)
```

---

## Example 4: API Integration - Creating Lambda Function | 示例4：API集成 - 创建Lambda函数

### User Query | 用户查询
"I need to create an AWS Lambda function using API. Please provide complete code examples."
"我需要使用API创建AWS Lambda函数，请提供完整的代码示例。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Product | 识别产品
- **Product Name**: AWS Lambda
- **Service Code**: lambda
- **Category**: Compute | 计算

#### Step 2: Construct API Documentation Queries | 构建API文档查询
```
site:docs.aws.amazon.com/lambda API reference
site:docs.aws.amazon.com/lambda create function
site:aws.amazon.com/lambda SDK
```

#### Step 3-7: Present API Integration Guide | 呈现API集成指南

```markdown
# AWS Lambda API Integration Guide | Lambda API集成指南

## Prerequisites | 前提条件

1. AWS account with Lambda access permissions
2. AWS Access Key ID and Secret Access Key configured
3. IAM role with Lambda execution permissions
4. Basic understanding of Lambda function structure

## API Overview | API概览

**Service Endpoint**: `https://lambda.<region>.amazonaws.com`

**Authentication**: AWS Signature Version 4

## Code Examples | 代码示例

### Python SDK (Boto3) Example

```python
import boto3
import zipfile
import io

# Initialize Lambda client
lambda_client = boto3.client(
    'lambda',
    aws_access_key_id='<your-access-key-id>',
    aws_secret_access_key='<your-secret-access-key>',
    region_name='us-east-1'
)

# Create deployment package
def create_deployment_package(function_code):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('lambda_function.py', function_code)
    buffer.seek(0)
    return buffer.read()

# Lambda function code
function_code = '''
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
'''

# Create Lambda function
response = lambda_client.create_function(
    FunctionName='my-lambda-function',
    Runtime='python3.11',
    Role='arn:aws:iam::<account-id>:role/lambda-execution-role',
    Handler='lambda_function.lambda_handler',
    Code={
        'ZipFile': create_deployment_package(function_code)
    },
    Description='My first Lambda function',
    Timeout=30,
    MemorySize=128,
    Environment={
        'Variables': {
            'ENV': 'production'
        }
    },
    Tags={
        'Project': 'MyProject',
        'Environment': 'Production'
    }
)

print(f"Function created: {response['FunctionArn']}")
```

### Java SDK Example

```java
import software.amazon.awssdk.services.lambda.LambdaClient;
import software.amazon.awssdk.services.lambda.model.*;
import software.amazon.awssdk.core.SdkBytes;

public class LambdaFunctionCreator {
    public static void main(String[] args) {
        LambdaClient lambdaClient = LambdaClient.builder()
            .region(Region.US_EAST_1)
            .build();

        // Create function request
        CreateFunctionRequest request = CreateFunctionRequest.builder()
            .functionName("my-lambda-function")
            .runtime(Runtime.PYTHON3_11)
            .role("arn:aws:iam::<account-id>:role/lambda-execution-role")
            .handler("lambda_function.lambda_handler")
            .code(FunctionCode.builder()
                .zipFile(SdkBytes.fromUtf8String("# Lambda function code"))
                .build())
            .description("My first Lambda function")
            .timeout(30)
            .memorySize(128)
            .build();

        try {
            CreateFunctionResponse response = lambdaClient.createFunction(request);
            System.out.println("Function created: " + response.functionArn());
        } catch (LambdaException e) {
            System.err.println(e.getMessage());
        }

        lambdaClient.close();
    }
}
```

### Go SDK Example

```go
package main

import (
    "context"
    "fmt"
    "github.com/aws/aws-sdk-go-v2/aws"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/service/lambda"
    "github.com/aws/aws-sdk-go-v2/service/lambda/types"
)

func main() {
    cfg, err := config.LoadDefaultConfig(context.TODO(),
        config.WithRegion("us-east-1"),
    )
    if err != nil {
        panic(err)
    }

    client := lambda.NewFromConfig(cfg)

    input := &lambda.CreateFunctionInput{
        FunctionName: aws.String("my-lambda-function"),
        Runtime:      types.RuntimePython311,
        Role:         aws.String("arn:aws:iam::<account-id>:role/lambda-execution-role"),
        Handler:      aws.String("lambda_function.lambda_handler"),
        Code: &types.FunctionCode{
            ZipFile: []byte("# Lambda function code"),
        },
        Description: aws.String("My first Lambda function"),
        Timeout:     aws.Int32(30),
        MemorySize:  aws.Int32(128),
    }

    result, err := client.CreateFunction(context.TODO(), input)
    if err != nil {
        panic(err)
    }

    fmt.Printf("Function created: %s\n", *result.FunctionArn)
}
```

### AWS CLI Example

```bash
# Create deployment package
zip function.zip lambda_function.py

# Create Lambda function
aws lambda create-function \
  --function-name my-lambda-function \
  --runtime python3.11 \
  --role arn:aws:iam::<account-id>:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --description "My first Lambda function" \
  --timeout 30 \
  --memory-size 128 \
  --environment Variables={ENV=production} \
  --tags Project=MyProject,Environment=Production
```

## Common Operations | 常用操作

| Operation | API Action | Description |
|-----------|-----------|-------------|
| Create Function | CreateFunction | Create a new Lambda function |
| Update Function Code | UpdateFunctionCode | Update function code |
| Update Function Configuration | UpdateFunctionConfiguration | Update function settings |
| Delete Function | DeleteFunction | Delete a Lambda function |
| Invoke Function | Invoke | Invoke a Lambda function |
| List Functions | ListFunctions | List all Lambda functions |
| Add Permission | AddPermission | Add permissions to function |

## Error Handling | 错误处理

Common error codes and solutions:

| Error Code | Description | Solution |
|-----------|-------------|----------|
| ResourceConflictException | Function already exists | Use a different function name or update existing |
| InvalidParameterValueException | Invalid parameter | Check parameter format and values |
| ServiceException | AWS Lambda service error | Retry the request |
| CodeStorageExceededException | Code storage limit exceeded | Delete unused functions or request limit increase |

## Related Resources | 相关资源

- [Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Lambda API Reference](https://docs.aws.amazon.com/lambda/latest/api/)
- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/)
```

---

## Example 5: Architecture Recommendation - Serverless Web Application | 示例5：架构推荐 - 无服务器Web应用

### User Query | 用户查询
"I need to design a serverless web application architecture on AWS, including frontend, backend, database, and storage."
"我需要为AWS上的无服务器Web应用设计架构，包括前端、后端、数据库和存储。"

### Skill Execution Steps | 技能执行步骤

#### Step 1: Identify Required Products | 识别所需产品
- **Frontend**: CloudFront + S3
- **Backend**: API Gateway + Lambda
- **Database**: DynamoDB
- **Storage**: S3
- **Authentication**: Cognito
- **Monitoring**: CloudWatch

#### Step 2: Research Each Product | 调研每个产品
Execute queries for each identified product to gather specifications and integration patterns.

#### Step 3-7: Present Architecture Recommendation | 呈现架构推荐

```markdown
# Serverless Web Application Architecture on AWS | AWS无服务器Web应用架构

## Architecture Overview | 架构概览

This architecture provides a scalable, cost-effective serverless web application using AWS services.
本架构使用AWS服务构建可扩展、经济高效的无服务器Web应用。

```
                    [Users]
                      |
                      v
              [Amazon CloudFront]
                      |
        +-------------+-------------+
        |                           |
        v                           v
[Static Website (S3)]    [API Gateway]
                                 |
                                 v
                         [AWS Lambda]
                                 |
                    +-------------+-------------+
                    |                           |
                    v                           v
            [Amazon DynamoDB]          [Amazon S3]
            (User Data)                (File Storage)
                    |
                    v
            [Amazon Cognito]
            (Authentication)
```

## Component Details | 组件详情

### 1. Content Delivery & Frontend | 内容分发与前端

**Products**: Amazon CloudFront + Amazon S3

**Configuration**:
- S3 hosts static website (HTML, CSS, JavaScript)
- CloudFront provides global CDN with edge caching
- HTTPS with ACM certificate
- Origin Access Identity (OAI) for S3 security

**Pricing Estimate**:
- S3: $0.023/GB (storage) + $0.0004/10,000 requests
- CloudFront: $0.085/GB (data transfer out)

### 2. API Layer | API层

**Product**: Amazon API Gateway

**Configuration**:
- REST API or HTTP API
- Lambda proxy integration
- API throttling and caching
- Usage plans and API keys

**Pricing Estimate**:
- HTTP API: $1.00/million requests
- REST API: $3.50/million requests
- Caching: $0.020/hour (0.5GB cache)

### 3. Compute Layer | 计算层

**Product**: AWS Lambda

**Configuration**:
- Runtime: Node.js, Python, or Java
- Memory: 512MB - 1GB
- Timeout: 30 seconds
- Concurrent executions: 1000 (default)

**Pricing Estimate**:
- Free tier: 1M requests/month + 400,000 GB-seconds
- Beyond free: $0.20/million requests + $0.0000166667/GB-second

### 4. Database Layer | 数据库层

**Product**: Amazon DynamoDB

**Configuration**:
- On-demand capacity mode (for variable traffic)
- Single-table design pattern
- Global Tables (for multi-region)
- Point-in-time recovery (PITR)

**Pricing Estimate**:
- On-demand: $1.25/million write requests + $0.25/million read requests
- Storage: $0.25/GB/month

### 5. Storage Layer | 存储层

**Product**: Amazon S3

**Configuration**:
- S3 Standard for user uploads
- S3 Intelligent-Tiering for cost optimization
- Presigned URLs for secure uploads/downloads
- Lifecycle policies for archival

**Pricing Estimate**:
- Storage: $0.023/GB
- Requests: $0.0004-$0.005 per 1,000 requests

### 6. Authentication | 身份验证

**Product**: Amazon Cognito

**Configuration**:
- User pools for authentication
- Identity pools for AWS resource access
- Social identity providers (Google, Facebook)
- MFA support

**Pricing Estimate**:
- Free tier: 50,000 MAUs/month
- Beyond free: $0.0055/MAU

## Cost Summary | 成本汇总

### Monthly Cost Estimate (100,000 requests/month) | 月度成本估算

| Component | Configuration | Monthly Cost |
|-----------|--------------|--------------|
| CloudFront | 100 GB transfer | $8.50 |
| S3 (Static) | 1 GB storage + requests | $0.50 |
| API Gateway | 100K requests (HTTP) | $0.10 |
| Lambda | 100K requests + compute | $2.00 |
| DynamoDB | On-demand + 10GB storage | $5.00 |
| S3 (User Data) | 50 GB storage | $1.15 |
| Cognito | 1,000 MAUs | Free |
| **Total** | | **~$17.25/month** |

## Scaling Considerations | 扩展考虑

### Automatic Scaling | 自动扩展
- Lambda: Automatic scaling from 0 to thousands of concurrent executions
- API Gateway: Automatic scaling with no configuration needed
- DynamoDB: On-demand mode scales automatically

### Cost Optimization | 成本优化
- Use CloudFront caching to reduce origin requests
- Implement DynamoDB DAX for read-heavy workloads
- Use S3 Transfer Acceleration only when needed
- Monitor with CloudWatch and set billing alerts

### Security Best Practices | 安全最佳实践
- Use IAM roles for Lambda (not access keys)
- Enable CloudTrail for API auditing
- Use Cognito for user authentication
- Implement WAF on API Gateway for additional protection

## Related Products | 相关产品

- **AWS X-Ray**: Distributed tracing for debugging
- **Amazon SNS**: Notifications and messaging
- **Amazon SQS**: Queue service for async processing
- **AWS Step Functions**: Workflow orchestration
- **Amazon EventBridge**: Serverless event bus
```

---

## Summary | 总结

These examples demonstrate the complete workflow of the AWS Product Query Skill:

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
