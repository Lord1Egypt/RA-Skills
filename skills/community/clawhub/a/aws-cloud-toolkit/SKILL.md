# aws-cloud-toolkit

## Name
- **en**: AWS Cloud Toolkit
- **zh**: AWS云服务工具包

## Description
- **en**: Comprehensive AWS cloud resource management toolkit supporting EC2, S3, RDS, Lambda operations with automated deployment and monitoring capabilities.
- **zh**: 全面的AWS云资源管理工具包，支持EC2、S3、RDS、Lambda操作，具备自动化部署和监控能力。

## Tools

### EC2 Instance Management

**Tool**: `ec2_manager`
**Description**: Manage AWS EC2 instances - list, start, stop, create, terminate

**Input Schema**:
```json
{
  "action": {"type": "string", "enum": ["list", "start", "stop", "create", "terminate"]},
  "instance_id": {"type": "string"},
  "instance_type": {"type": "string", "default": "t2.micro"},
  "image_id": {"type": "string"},
  "key_name": {"type": "string"},
  "security_group_ids": {"type": "array", "items": {"type": "string"}},
  "region": {"type": "string", "default": "us-east-1"}
}
```

**Example**:
```json
{
  "action": "list",
  "region": "us-east-1"
}
```

### S3 Bucket Operations

**Tool**: `s3_manager`
**Description**: Manage AWS S3 buckets - create, delete, list, upload, download objects

**Input Schema**:
```json
{
  "action": {"type": "string", "enum": ["list_buckets", "create_bucket", "delete_bucket", "list_objects", "upload", "download", "delete_object"]},
  "bucket_name": {"type": "string"},
  "object_key": {"type": "string"},
  "local_path": {"type": "string"},
  "region": {"type": "string", "default": "us-east-1"}
}
```

**Example**:
```json
{
  "action": "list_buckets",
  "region": "us-east-1"
}
```

### Lambda Function Management

**Tool**: `lambda_manager`
**Description**: Deploy and manage AWS Lambda functions

**Input Schema**:
```json
{
  "action": {"type": "string", "enum": ["list", "create", "update", "delete", "invoke"]},
  "function_name": {"type": "string"},
  "runtime": {"type": "string", "default": "python3.9"},
  "handler": {"type": "string"},
  "role_arn": {"type": "string"},
  "code_path": {"type": "string"},
  "region": {"type": "string", "default": "us-east-1"}
}
```

### CloudWatch Monitoring

**Tool**: `cloudwatch_monitor`
**Description**: Monitor AWS resources with CloudWatch metrics and alarms

**Input Schema**:
```json
{
  "action": {"type": "string", "enum": ["get_metrics", "create_alarm", "list_alarms", "get_logs"]},
  "namespace": {"type": "string"},
  "metric_name": {"type": "string"},
  "dimensions": {"type": "object"},
  "alarm_name": {"type": "string"},
  "threshold": {"type": "number"},
  "region": {"type": "string", "default": "us-east-1"}
}
```

## Configuration

**Environment Variables**:
```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
```

## Usage Examples

```python
from aws_cloud_toolkit import EC2Manager, S3Manager, LambdaManager

# EC2 operations
ec2 = EC2Manager(region='us-east-1')
instances = ec2.list_instances()
ec2.start_instance('i-1234567890abcdef0')

# S3 operations
s3 = S3Manager(region='us-east-1')
s3.create_bucket('my-new-bucket')
s3.upload_file('my-bucket', 'data.csv', '/local/path/data.csv')

# Lambda operations
lambda_mgr = LambdaManager(region='us-east-1')
lambda_mgr.deploy_function('my-function', 'python3.9', 'handler.lambda_handler')
```

## Installation

```bash
pip install boto3 python-dotenv
```

## Requirements

- Python 3.8+
- AWS Account with appropriate IAM permissions
- boto3 library
