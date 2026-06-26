---
name: Migrate Cloud Data with Automated SFTP Transfers & Google Drive Sync
description: "Automate multi-cloud migrations and infrastructure deployments with customizable IaC workflows. Use when the user needs cloud strategy planning, infrastructure-as-code generation, deployment automation, or multi-environment provisioning."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AZURE_SUBSCRIPTION_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "GCP_PROJECT_ID", "GCP_SERVICE_ACCOUNT_JSON"],
        "bins": ["terraform", "ansible", "aws-cli", "az", "gcloud", "docker"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"]
    },
    "emoji": "☁️"
  }
---

## Overview

CloudMigrate is a production-grade skill for automating complex cloud migrations and infrastructure deployments across AWS, Azure, GCP, and hybrid environments. It orchestrates Infrastructure-as-Code (IaC) generation, multi-step deployment workflows, service discovery, data migration planning, and environment configuration — eliminating manual processes that introduce errors and delay time-to-production.

**Why CloudMigrate Matters:**
- **Reduces Migration Complexity**: Converts high-level requirements into executable Terraform, CloudFormation, and Ansible playbooks
- **Multi-Cloud Support**: Seamlessly provisions across AWS (EC2, RDS, Lambda), Azure (VMs, SQL Database, App Service), and GCP (Compute Engine, Cloud SQL)
- **Risk Mitigation**: Generates validation scripts, pre-flight checks, and rollback procedures automatically
- **Team Enablement**: Integrates with Slack for approval workflows and GitHub for GitOps-ready code repositories
- **Cost Optimization**: Analyzes current infrastructure and recommends cost-reduction strategies before migration

**Typical Use Cases:**
- Lift-and-shift migration from on-premises to public cloud
- Multi-region failover and disaster recovery setup
- Microservices deployment with containerization
- Database migration with zero-downtime cutover planning
- DevOps pipeline automation and CI/CD infrastructure

---

## Quick Start

Try these prompts immediately to see CloudMigrate in action:

### Example 1: Generate AWS Migration Plan
```
Plan a migration for a 50-server on-premises data center to AWS. 
The environment includes:
- 10 Windows servers running legacy applications (SQL Server backend)
- 20 Linux web servers (Apache/PHP)
- 15 database servers (MySQL, PostgreSQL)
- Network: 10.0.0.0/8 with 5 subnets

Generate:
1. Network architecture diagram (as code)
2. Terraform configuration for VPC, subnets, security groups
3. AWS Database Migration Service (DMS) configuration
4. Cost estimate (3-year TCO comparison)
5. Risk assessment and mitigation steps
```

### Example 2: Create Multi-Environment Infrastructure
```
Create Terraform code for a production SaaS application with:
- Development, staging, and production environments
- Application load balancer routing to auto-scaling groups
- RDS PostgreSQL with read replicas
- ElastiCache Redis cluster for sessions
- S3 buckets with versioning and encryption
- CloudFront CDN configuration
- Monitoring with CloudWatch and SNS alerts

Include:
- Environment variable files (.tfvars)
- Terraform state locking with DynamoDB
- IAM roles and policies (least privilege)
- Backup and disaster recovery automation
```

### Example 3: Azure Hybrid Cloud Deployment
```
Generate infrastructure-as-code for a hybrid Azure deployment:
- On-premises Hyper-V VMs migrated to Azure
- Azure ExpressRoute connection
- Azure SQL Database failover groups (read replicas)
- App Service with staging slots for blue-green deployments
- Azure DevOps pipeline for automated testing
- Monitoring with Application Insights

Provide:
1. Bicep templates (Azure native IaC)
2. Network configuration and security policies
3. Azure Migrate assessment and scripts
4. Cutover schedule with validation steps
5. Rollback procedures
```

### Example 4: Kubernetes Deployment Automation
```
Create a complete Kubernetes infrastructure for a microservices platform:
- EKS cluster on AWS (multi-AZ)
- Container registry (ECR)
- Helm charts for 5 microservices
- Persistent storage (EBS volumes)
- Ingress controller with TLS
- Service mesh (Istio) for traffic management
- Prometheus + Grafana monitoring
- RBAC and network policies

Include deployment scripts and GitOps workflows with Flux.
```

---

## Capabilities

### 1. Infrastructure-as-Code Generation
**What it does:** Converts natural language requirements into production-ready Terraform, CloudFormation, Bicep, or Ansible code.

**Example Usage:**
```
Generate a Terraform module for a secure multi-AZ RDS cluster with:
- Automated backups (30-day retention)
- Encryption at rest (KMS) and in transit (TLS)
- IAM database authentication
- Performance Insights enabled
- Parameter group tuning for PostgreSQL 14
- Subnet group spanning 3 availability zones
```

**Supported IaC Frameworks:**
- Terraform (HCL)
- AWS CloudFormation (JSON/YAML)
- Azure Bicep
- Ansible playbooks
- Kubernetes manifests (YAML)
- Docker Compose
- Helm Charts

### 2. Multi-Cloud Migration Planning
**What it does:** Assesses source environments and generates cloud-specific migration strategies.

**Outputs Include:**
- Current state analysis (resource inventory, dependencies, costs)
- Target architecture diagrams
- Network topology with CIDR planning
- Database migration strategy (schema conversion, data replication)
- Application re-platforming recommendations
- Cost analysis (CapEx → OpEx breakdown)
- Timeline and resource allocation

### 3. Deployment Orchestration
**What it does:** Creates step-by-step automation workflows for safe, validated deployments.

**Features:**
- Pre-deployment validation scripts (connectivity, permissions, quotas)
- Rolling deployments with health checks
- Canary releases with traffic shifting
- Automated rollback on failure detection
- Post-deployment smoke tests
- Approval gates (integrate with Slack for manual sign-offs)

### 4. Data Migration & Cutover Planning
**What it does:** Generates scripts and procedures for zero-downtime data migration.

**Capabilities:**
- Schema validation and conversion (Oracle → PostgreSQL, etc.)
- Replication lag monitoring
- Cutover scheduling and validation
- DNS failover automation
- Data validation queries
- Backup and recovery procedures

### 5. Security & Compliance Automation
**What it does:** Embeds security best practices into generated infrastructure.

**Includes:**
- IAM role and policy generation (least privilege principle)
- Network segmentation (security groups, NACLs, firewalls)
- Encryption configuration (KMS, TDE, SSL/TLS)
- Compliance scanning (CIS benchmarks, PCI-DSS)
- Secrets management (HashiCorp Vault, AWS Secrets Manager)
- Audit logging and monitoring

### 6. Cost Optimization Analysis
**What it does:** Recommends cost-saving strategies and calculates savings.

**Outputs:**
- Reserved instance recommendations
- Spot instance opportunities
- Right-sizing recommendations
- Storage optimization (S3 tiers, compression)
- Network cost analysis
- 3-year TCO projections

---

## Configuration

### Required Environment Variables

```bash
# AWS
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"

# Azure
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"

# GCP
export GCP_PROJECT_ID="your-project-id"
export GCP_SERVICE_ACCOUNT_JSON="/path/to/service-account.json"

# CloudMigrate Specific
export CLOUDMIGRATE_STATE_BUCKET="your-terraform-state-bucket"
export CLOUDMIGRATE_SLACK_WEBHOOK="https://hooks.slack.com/services/YOUR/WEBHOOK"
export CLOUDMIGRATE_GITHUB_TOKEN="your-github-pat-token"
export CLOUDMIGRATE_VAULT_ADDR="https://vault.example.com"
```

### Setup Instructions

1. **Install Required Binaries:**
   ```bash
   # macOS (Homebrew)
   brew install terraform ansible awscli azure-cli google-cloud-sdk docker

   # Linux (Debian/Ubuntu)
   sudo apt-get install -y terraform ansible awscli azure-cli docker.io

   # Windows (Chocolatey)
   choco install terraform ansible awscli azure-cli docker-desktop
   ```

2. **Authenticate Cloud Providers:**
   ```bash
   # AWS
   aws configure
   
   # Azure
   az login
   
   # GCP
   gcloud auth application-default login
   ```

3. **Initialize Terraform State Backend:**
   ```bash
   cloudmigrate init-backend \
     --provider aws \
     --bucket my-terraform-state \
     --region us-east-1
   ```

4. **Configure Slack Integration (Optional):**
   ```bash
   cloudmigrate config slack \
     --webhook-url "https://hooks.slack.com/services/YOUR/WEBHOOK" \
     --channel "#infrastructure"
   ```

### Configuration Options

```yaml
# cloudmigrate-config.yaml
migration:
  strategy: "lift-and-shift"  # or "refactor", "replatform", "repurchase"
  parallelization:
    max_concurrent_deployments: 5
    max_concurrent_migrations: 3
  validation:
    pre_deployment_checks: true
    post_deployment_tests: true
    health_check_retries: 5

cloud_targets:
  aws:
    regions: ["us-east-1", "us-west-2", "eu-west-1"]
    instance_types: ["t3.medium", "m5.large", "c5.xlarge"]
  azure:
    regions: ["eastus", "westeurope"]
    vm_sizes: ["Standard_B2s", "Standard_D2s_v3"]
  gcp:
    regions: ["us-central1", "europe-west1"]
    machine_types: ["e2-medium", "n2-standard-2"]

security:
  encryption_at_rest: true
  encryption_in_transit: true
  enable_mfa: true
  compliance_framework: "pci-dss"  # or "hipaa", "gdpr", "sox"

cost_optimization:
  reserved_instances: true
  spot_instances: false
  auto_shutdown_dev: true
  budget_alerts: true
```

---

## Example Outputs

### Generated Terraform Code
```hcl
# main.tf - Generated by CloudMigrate
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "CloudMigrate"
      Project     = var.project_name
    }
  }
}

# VPC with private/public subnets
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Security Group with least-privilege rules
resource "aws_security_group" "app" {
  name        = "${var.project_name}-app-sg"
  description = "Security group for application tier"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-app-sg"
  }
}

# RDS PostgreSQL with encryption
resource "aws_db_instance" "postgres" {
  allocated_storage      = var.db_storage_gb
  engine                 = "postgres"
  engine_version         = "14.7"
  instance_class         = var.db_instance_class
  db_name                = var.db_name
  username               = var.db_username
  password               = random_password.db.result
  parameter_group_name   = aws_db_parameter_group.postgres.name
  skip_final_snapshot    = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"

  # Security
  storage_encrypted      = true
  kms_key_id            = aws_kms_key.db.arn
  publicly_accessible   = false
  db_subnet_group_name  = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.database.id]

  # High Availability
  multi_az               = true
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  # Performance
  performance_insights_enabled = true
  performance_insights_retention_period = 7
  enabled_cloudwatch_logs_exports = ["postgresql"]

  tags = {
    Name = "${var.project_name}-postgres"
  }

  depends_on = [aws_security_group.database]
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  name                = "${var.project_name}-asg"
  vpc_zone_identifier = aws_subnet.private[*].id
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  min_size         = var.asg_min_size
  max_size         = var.asg_max_size
  desired_capacity = var.asg_desired_capacity

  tag {
    key                 = "Name"
    value               = "${var.project_name}-asg-instance"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }
}
```

### Migration Assessment Report (JSON)
```json
{
  "assessment_id": "mig-2024-001",
  "timestamp": "2024-01-15T10:30:00Z",
  "source_environment": {
    "type": "on-premises",
    "location": "data-center-01",
    "total_servers": 47,
    "total_storage_gb": 5120,
    "total_vms": {
      "windows": 10,
      "linux": 37
    }
  },
  "target_environment": {
    "provider": "aws",
    "regions": ["us-east-1", "us-west-2"],
    "estimated_monthly_cost": 18500
  },
  "migration_strategy": "lift-and-shift",
  "timeline": {
    "assessment_phase": "2 weeks",
    "planning_phase": "4 weeks",
    "migration_phase": "12 weeks",