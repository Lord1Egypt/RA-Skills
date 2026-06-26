# AWS Cloud Toolkit

<p align="center">
  <strong>🚀 全面的AWS云资源管理工具包 | Comprehensive AWS Cloud Resource Management Toolkit</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#api-reference">API</a>
</p>

---

## 🌟 Features

### ☁️ Multi-Service Support
- **EC2** - Instance lifecycle management (create, start, stop, terminate)
- **S3** - Bucket operations and object storage management
- **Lambda** - Serverless function deployment and invocation
- **RDS** - Database instance management
- **CloudWatch** - Metrics monitoring and alarm configuration

### 🔧 Automation Capabilities
- Auto-scaling configuration
- Scheduled backups
- Cost optimization recommendations
- Resource tagging automation

### 📊 Monitoring & Insights
- Real-time resource monitoring
- Cost analysis and forecasting
- Performance metrics dashboard
- Alert notifications

---

## 📦 Installation

```bash
# Install from source
git clone https://github.com/your-org/aws-cloud-toolkit.git
cd aws-cloud-toolkit
pip install -r requirements.txt

# Or install via pip (when published)
pip install aws-cloud-toolkit
```

### Prerequisites
- Python 3.8+
- AWS Account with appropriate IAM permissions
- AWS CLI configured (optional but recommended)

---

## ⚙️ Configuration

### Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### IAM Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "s3:*",
        "lambda:*",
        "cloudwatch:*",
        "logs:*"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 🚀 Usage

### Quick Start

```python
from aws_cloud_toolkit import EC2Manager, S3Manager, LambdaManager

# Initialize managers
ec2 = EC2Manager(region='us-east-1')
s3 = S3Manager(region='us-east-1')
lambda_mgr = LambdaManager(region='us-east-1')

# List all EC2 instances
instances = ec2.list_instances()
for inst in instances:
    print(f"{inst['id']}: {inst['state']} - {inst['type']}")

# Start an instance
ec2.start_instance('i-1234567890abcdef0')

# Create S3 bucket
s3.create_bucket('my-unique-bucket-name')

# Upload file
s3.upload_file('my-unique-bucket-name', 'data/file.csv', '/local/path/file.csv')
```

### EC2 Operations

```python
from aws_cloud_toolkit import EC2Manager

ec2 = EC2Manager(region='us-east-1')

# Create new instance
instance = ec2.create_instance(
    image_id='ami-0c55b159cbfafe1f0',
    instance_type='t2.micro',
    key_name='my-key-pair',
    security_group_ids=['sg-12345678']
)

# Manage instances
ec2.stop_instance('i-1234567890abcdef0')
ec2.start_instance('i-1234567890abcdef0')
ec2.terminate_instance('i-1234567890abcdef0')
```

### S3 Operations

```python
from aws_cloud_toolkit import S3Manager

s3 = S3Manager(region='us-east-1')

# Bucket operations
buckets = s3.list_buckets()
s3.create_bucket('my-new-bucket')
s3.delete_bucket('old-bucket')

# Object operations
s3.upload_file('my-bucket', 'path/in/bucket/file.txt', '/local/file.txt')
s3.download_file('my-bucket', 'path/in/bucket/file.txt', '/local/download.txt')
s3.delete_object('my-bucket', 'path/in/bucket/file.txt')

# List objects
objects = s3.list_objects('my-bucket', prefix='data/')
```

### Lambda Operations

```python
from aws_cloud_toolkit import LambdaManager

lambda_mgr = LambdaManager(region='us-east-1')

# Deploy function
lambda_mgr.create_function(
    function_name='my-function',
    runtime='python3.9',
    handler='lambda_function.handler',
    role_arn='arn:aws:iam::123456789012:role/lambda-role',
    code_path='/path/to/function.zip'
)

# Invoke function
result = lambda_mgr.invoke_function('my-function', payload={'key': 'value'})

# Update function
lambda_mgr.update_function_code('my-function', '/path/to/new-code.zip')
```

---

## 📚 API Reference

### EC2Manager

| Method | Description | Parameters |
|--------|-------------|------------|
| `list_instances()` | List all EC2 instances | filters (optional) |
| `create_instance()` | Launch new instance | image_id, instance_type, key_name, ... |
| `start_instance()` | Start stopped instance | instance_id |
| `stop_instance()` | Stop running instance | instance_id |
| `terminate_instance()` | Terminate instance | instance_id |

### S3Manager

| Method | Description | Parameters |
|--------|-------------|------------|
| `list_buckets()` | List all buckets | - |
| `create_bucket()` | Create new bucket | bucket_name, region |
| `delete_bucket()` | Delete empty bucket | bucket_name |
| `upload_file()` | Upload file to bucket | bucket, key, local_path |
| `download_file()` | Download file from bucket | bucket, key, local_path |

### LambdaManager

| Method | Description | Parameters |
|--------|-------------|------------|
| `list_functions()` | List all Lambda functions | - |
| `create_function()` | Create new function | function_name, runtime, handler, ... |
| `invoke_function()` | Invoke function | function_name, payload |
| `update_function()` | Update function code | function_name, code_path |

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=aws_cloud_toolkit --cov-report=html
```

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ for the AWS community
</p>
