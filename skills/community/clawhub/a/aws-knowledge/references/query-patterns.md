# AWS Query Patterns by Domain

Common search queries and tool combinations organized by AWS domain.

## Compute

```bash
# EC2 instance selection
mcporter call aws-knowledge.search_documentation query="EC2 instance type selection guide"

# Lambda optimization
mcporter call aws-knowledge.search_documentation query="Lambda cold start optimization best practices"

# ECS vs EKS decision
mcporter call aws-knowledge.search_documentation query="ECS vs EKS container orchestration comparison"

# Auto Scaling
mcporter call aws-knowledge.retrieve_agent_sops query="configure EC2 Auto Scaling group"
```

## Storage

```bash
# S3 security
mcporter call aws-knowledge.search_documentation query="S3 bucket policy security best practices"

# Storage class selection
mcporter call aws-knowledge.search_documentation query="S3 storage class selection lifecycle"

# EBS volume types
mcporter call aws-knowledge.search_documentation query="EBS volume types gp3 io2 comparison"
```

## Networking

```bash
# VPC design
mcporter call aws-knowledge.search_documentation query="VPC design production multi-AZ"

# Transit Gateway
mcporter call aws-knowledge.search_documentation query="Transit Gateway multi-VPC connectivity"

# PrivateLink
mcporter call aws-knowledge.retrieve_agent_sops query="set up VPC PrivateLink endpoint"
```

## Databases

```bash
# RDS vs Aurora
mcporter call aws-knowledge.search_documentation query="RDS vs Aurora comparison"

# DynamoDB modeling
mcporter call aws-knowledge.search_documentation query="DynamoDB single table design patterns"

# Database migration
mcporter call aws-knowledge.retrieve_agent_sops query="migrate database to RDS using DMS"
```

## Security & IAM

```bash
# IAM best practices
mcporter call aws-knowledge.search_documentation query="IAM least privilege best practices"

# Cross-account access
mcporter call aws-knowledge.search_documentation query="cross-account IAM role assume"

# Security audit
mcporter call aws-knowledge.retrieve_agent_sops query="security audit AWS account"
```

## Infrastructure as Code

```bash
# CDK getting started
mcporter call aws-knowledge.search_documentation query="CDK v2 getting started TypeScript"

# CloudFormation patterns
mcporter call aws-knowledge.search_documentation query="CloudFormation nested stack patterns"

# CDK best practices
mcporter call aws-knowledge.search_documentation query="CDK best practices constructs patterns"
```

## AI/ML

```bash
# Bedrock models
mcporter call aws-knowledge.search_documentation query="Bedrock foundation models comparison"

# SageMaker endpoints
mcporter call aws-knowledge.search_documentation query="SageMaker inference endpoint deployment"

# Bedrock availability
mcporter call aws-knowledge.get_regional_availability service="Amazon Bedrock" region="us-west-2"
```

## Serverless

```bash
# Step Functions
mcporter call aws-knowledge.search_documentation query="Step Functions workflow patterns"

# API Gateway
mcporter call aws-knowledge.search_documentation query="API Gateway REST vs HTTP comparison"

# EventBridge
mcporter call aws-knowledge.search_documentation query="EventBridge event-driven architecture patterns"
```

## Cost Optimization

```bash
# Savings Plans
mcporter call aws-knowledge.search_documentation query="Savings Plans vs Reserved Instances comparison"

# Cost allocation
mcporter call aws-knowledge.search_documentation query="cost allocation tags billing best practices"

# Right-sizing
mcporter call aws-knowledge.retrieve_agent_sops query="right-size EC2 instances Cost Explorer"
```
