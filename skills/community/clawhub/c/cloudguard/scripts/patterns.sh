#!/usr/bin/env bash
# CloudGuard -- Cloud Security Pattern Definitions
# Each pattern: REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# 90 patterns across 6 categories (15 patterns each):
#   S3 -- Storage Security              (S3-001 through S3-015)
#   IM -- IAM & Permissions             (IM-001 through IM-015)
#   NW -- Network Security              (NW-001 through NW-015)
#   EN -- Encryption                    (EN-001 through EN-015)
#   LG -- Logging & Monitoring          (LG-001 through LG-015)
#   CF -- Configuration & Compliance    (CF-001 through CF-015)
#
# Severity levels:
#   critical -- Immediate infrastructure compromise risk (open to internet, wildcard admin)
#   high     -- Significant security gap that could be exploited
#   medium   -- Best practice violation that increases attack surface
#   low      -- Informational, minor hygiene issue, hardening recommendation
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - Avoid Perl-only features (\d, \w, \b, lookahead/lookbehind, etc.)
# - Use [0-9] instead of \d
# - Escape special chars in character classes properly
# - Test with: grep -E "pattern" testfile.tf

set -euo pipefail

# ============================================================================
# 1. S3 / STORAGE SECURITY (S3-001 through S3-015)
# ============================================================================

declare -a CLOUDGUARD_S3_PATTERNS=()

CLOUDGUARD_S3_PATTERNS+=(
  # --- S3 bucket with public-read or public-read-write ACL ---
  'acl[[:space:]]*=[[:space:]]*"public-read|critical|S3-001|S3 bucket with public ACL (public-read or public-read-write) -- data exposed to internet|Set acl = "private" and use bucket policies for controlled access; enable S3 Block Public Access'

  # --- S3 bucket missing server-side encryption configuration ---
  'aws_s3_bucket[[:space:]]+"[^"]*"[[:space:]]*\{|critical|S3-002|S3 bucket resource detected -- verify server_side_encryption_configuration is present|Add server_side_encryption_configuration block with AES256 or aws:kms encryption'

  # --- S3 bucket versioning not enabled ---
  'versioning[[:space:]]*\{[[:space:]]*(#.*)?$|high|S3-003|S3 bucket versioning block found -- verify enabled = true is set|Set versioning { status = "Enabled" } to protect against accidental deletion and enable recovery'

  # --- Bucket policy with Principal * (public access) ---
  '"Principal"[[:space:]]*:[[:space:]]*"\*"|critical|S3-004|Bucket policy with Principal: * grants public access to all AWS users|Restrict Principal to specific AWS accounts, IAM roles, or use conditions to limit access'

  # --- S3 bucket missing logging configuration ---
  'logging[[:space:]]*\{|medium|S3-005|S3 bucket logging block found -- verify target_bucket is configured|Configure server access logging with a dedicated logging bucket for audit trail'

  # --- S3 bucket without lifecycle rule ---
  'lifecycle_rule[[:space:]]*\{|low|S3-006|S3 lifecycle rule block found -- verify transition and expiration are configured|Add lifecycle rules for cost optimization: transition to IA/Glacier and expire old versions'

  # --- Missing S3 Block Public Access settings ---
  'block_public_acls[[:space:]]*=[[:space:]]*false|critical|S3-007|S3 Block Public Access explicitly disabled -- bucket may be publicly accessible|Set block_public_acls, block_public_policy, ignore_public_acls, restrict_public_buckets to true'

  # --- CloudFront distribution without HTTPS-only viewer protocol ---
  'viewer_protocol_policy[[:space:]]*=[[:space:]]*"allow-all"|high|S3-008|CloudFront allows HTTP traffic -- data transmitted without encryption|Set viewer_protocol_policy = "redirect-to-https" or "https-only" for all cache behaviors'

  # --- EFS file system without encryption ---
  'aws_efs_file_system[[:space:]]+"[^"]*"[[:space:]]*\{|high|S3-009|EFS file system detected -- verify encrypted = true is set|Add encrypted = true and kms_key_id for EFS encryption at rest'

  # --- DynamoDB table without encryption ---
  'aws_dynamodb_table[[:space:]]+"[^"]*"[[:space:]]*\{|high|S3-010|DynamoDB table detected -- verify server_side_encryption block with enabled = true|Add server_side_encryption { enabled = true } with optional kms_key_arn for CMK encryption'

  # --- S3 bucket policy allowing s3:GetObject to all ---
  '"Action"[[:space:]]*:[[:space:]]*"s3:GetObject".*"Effect"[[:space:]]*:[[:space:]]*"Allow"|critical|S3-011|S3 bucket policy allows s3:GetObject -- may grant public read access|Add conditions to restrict access by IP, VPC endpoint, or specific principals'

  # --- S3 bucket without object lock ---
  'object_lock_configuration[[:space:]]*\{|medium|S3-012|S3 object lock block found -- verify object_lock_enabled = true on the bucket|Enable object lock with governance or compliance mode for immutable backup protection'

  # --- S3 bucket without MFA delete protection ---
  'mfa_delete[[:space:]]*=[[:space:]]*"?Disabled"?|medium|S3-013|S3 bucket MFA delete is disabled -- versioned objects can be permanently deleted|Enable MFA delete to require MFA token for permanent version deletion'

  # --- S3 bucket without replication for disaster recovery ---
  'aws_s3_bucket_replication_configuration|low|S3-014|S3 replication configuration found -- verify rules and destination are properly set|Configure cross-region replication with appropriate IAM roles for disaster recovery'

  # --- S3 bucket policy with overly broad action ---
  '"Action"[[:space:]]*:[[:space:]]*"s3:\*"|critical|S3-015|S3 bucket policy grants s3:* (all S3 actions) -- overly permissive|Restrict actions to specific operations needed (s3:GetObject, s3:PutObject, etc.)'
)

# ============================================================================
# 2. IM / IAM & PERMISSIONS (IM-001 through IM-015)
# ============================================================================

declare -a CLOUDGUARD_IM_PATTERNS=()

CLOUDGUARD_IM_PATTERNS+=(
  # --- IAM policy with Action: * (wildcard all actions) ---
  '"Action"[[:space:]]*:[[:space:]]*"\*"|critical|IM-001|IAM policy with Action: * grants all AWS API permissions -- full admin access|Follow least privilege: specify only the exact actions needed for the role'

  # --- AdministratorAccess managed policy attachment ---
  'arn:aws:iam::.*:policy/AdministratorAccess|critical|IM-002|AdministratorAccess managed policy attached -- unrestricted admin privileges|Create a custom policy with only the permissions required; avoid AdministratorAccess'

  # --- AssumeRole policy with Principal: * ---
  '"Principal"[[:space:]]*:[[:space:]]*"\*".*"Action"[[:space:]]*:[[:space:]]*"sts:AssumeRole"|high|IM-003|AssumeRole trust policy with Principal: * allows any AWS entity to assume this role|Restrict Principal to specific AWS accounts or IAM entities'

  # --- IAM user with inline policy ---
  'aws_iam_user_policy[[:space:]]+"[^"]*"[[:space:]]*\{|high|IM-004|IAM user with inline policy -- harder to audit and manage than managed policies|Use aws_iam_group_policy_attachment with managed policies instead of inline user policies'

  # --- IAM policy missing MFA condition ---
  '"Condition"[[:space:]]*:[[:space:]]*\{[[:space:]]*"Bool"[[:space:]]*:[[:space:]]*\{|high|IM-005|IAM policy with Condition block -- verify aws:MultiFactorAuthPresent is enforced for sensitive actions|Add Condition: { Bool: { aws:MultiFactorAuthPresent: true } } for privileged operations'

  # --- Root account usage indicator ---
  '"arn:aws:iam::[0-9]+:root"|critical|IM-006|Root account ARN referenced in policy -- root should never be used for daily operations|Remove root account references; use IAM users/roles with least privilege instead'

  # --- IAM policy with Resource: * (wildcard all resources) ---
  '"Resource"[[:space:]]*:[[:space:]]*"\*"|high|IM-007|IAM policy with Resource: * applies to all AWS resources -- overly broad scope|Specify resource ARNs to limit the scope of permissions to required resources only'

  # --- iam:PassRole with wildcard resource ---
  '"Action"[[:space:]]*:.*"iam:PassRole".*"Resource"[[:space:]]*:[[:space:]]*"\*"|critical|IM-008|iam:PassRole with Resource: * allows passing any IAM role -- privilege escalation risk|Restrict iam:PassRole to specific role ARNs that the entity actually needs to pass'

  # --- IAM role without permission boundary ---
  'aws_iam_role[[:space:]]+"[^"]*"[[:space:]]*\{|medium|IM-009|IAM role detected -- verify permissions_boundary is set to limit maximum permissions|Add permissions_boundary with a managed policy ARN to cap the maximum permissions for the role'

  # --- Missing IAM password policy ---
  'aws_iam_account_password_policy|medium|IM-010|IAM password policy resource found -- verify strong settings are configured|Set minimum_password_length >= 14, require_symbols, require_numbers, require_uppercase_characters'

  # --- Cross-account trust with overly broad principal ---
  '"AWS"[[:space:]]*:[[:space:]]*"arn:aws:iam::[0-9]+:root"|high|IM-011|Cross-account trust policy trusts entire external account root -- too broad|Restrict trust to specific IAM roles or users in the external account, not the root'

  # --- IAM policy without explicit deny ---
  '"Effect"[[:space:]]*:[[:space:]]*"Allow".*"Action"[[:space:]]*:[[:space:]]*"\*"|medium|IM-012|IAM policy with Allow + Action:* without explicit Deny -- no guardrails|Add explicit Deny statements for sensitive actions (iam:*, organizations:*, sts:*)'

  # --- Lambda function with admin role ---
  'arn:aws:iam::.*:policy/AdministratorAccess.*lambda|critical|IM-013|Lambda function associated with AdministratorAccess policy -- excessive permissions|Create a minimal execution role with only the permissions the Lambda function needs'

  # --- IAM user with both console and programmatic access ---
  'aws_iam_user_login_profile[[:space:]]+"[^"]*"[[:space:]]*\{|medium|IM-014|IAM user login profile detected -- verify user does not also have access keys|Separate human (console) and machine (API) access into different IAM principals'

  # --- IAM group without attached policy ---
  'aws_iam_group[[:space:]]+"[^"]*"[[:space:]]*\{|low|IM-015|IAM group defined -- verify it has policies attached and is not empty|Attach appropriate managed policies to the group; empty groups serve no purpose'
)

# ============================================================================
# 3. NW / NETWORK SECURITY (NW-001 through NW-015)
# ============================================================================

declare -a CLOUDGUARD_NW_PATTERNS=()

CLOUDGUARD_NW_PATTERNS+=(
  # --- Security group ingress open to 0.0.0.0/0 ---
  'cidr_blocks[[:space:]]*=[[:space:]]*\["0\.0\.0\.0/0"\]|critical|NW-001|Security group ingress open to 0.0.0.0/0 (entire internet)|Restrict cidr_blocks to specific IP ranges, VPC CIDRs, or security group references'

  # --- SSH (port 22) open to internet ---
  'from_port[[:space:]]*=[[:space:]]*22.*to_port[[:space:]]*=[[:space:]]*22|critical|NW-002|SSH port 22 rule detected -- verify it is not open to 0.0.0.0/0|Restrict SSH access to specific bastion host IPs or use AWS Systems Manager Session Manager'

  # --- RDP (port 3389) open to internet ---
  'from_port[[:space:]]*=[[:space:]]*3389.*to_port[[:space:]]*=[[:space:]]*3389|critical|NW-003|RDP port 3389 rule detected -- verify it is not open to 0.0.0.0/0|Restrict RDP to specific admin IPs or use a VPN/bastion; never expose RDP to internet'

  # --- Database ports exposed (3306, 5432, 27017) ---
  'from_port[[:space:]]*=[[:space:]]*(3306|5432|27017)|high|NW-004|Database port (MySQL/PostgreSQL/MongoDB) rule detected -- verify not public|Place databases in private subnets; restrict access to application security groups only'

  # --- All ports open (0 to 65535) ---
  'from_port[[:space:]]*=[[:space:]]*0[[:space:]]*.*to_port[[:space:]]*=[[:space:]]*65535|critical|NW-005|Security group rule opens all ports (0-65535) -- entire port range exposed|Specify exact ports needed; never open all ports in a security group rule'

  # --- Resource without VPC/subnet configuration ---
  'aws_instance[[:space:]]+"[^"]*"[[:space:]]*\{|high|NW-006|EC2 instance detected -- verify it is deployed in a VPC with proper subnet_id|Always specify subnet_id in a private subnet; never use EC2-Classic or default VPC'

  # --- Subnet without network ACL ---
  'aws_network_acl[[:space:]]+"[^"]*"[[:space:]]*\{|medium|NW-007|Network ACL resource detected -- verify it is associated with appropriate subnets|Associate network ACLs with all subnets; use NACLs as an additional defense layer'

  # --- Public subnet with direct IGW route ---
  'gateway_id[[:space:]]*=[[:space:]]*aws_internet_gateway\.|high|NW-008|Route to Internet Gateway detected -- verify this is in a public subnet with NAT for private|Ensure private subnets route through NAT Gateway, not directly to Internet Gateway'

  # --- Default VPC usage ---
  'default[[:space:]]*=[[:space:]]*true.*vpc|medium|NW-009|Default VPC or default setting detected -- avoid using default VPC for production|Create custom VPCs with proper CIDR planning, subnet segregation, and security controls'

  # --- Unrestricted egress rule ---
  'egress[[:space:]]*\{.*cidr_blocks[[:space:]]*=[[:space:]]*\["0\.0\.0\.0/0"\]|medium|NW-010|Security group egress open to 0.0.0.0/0 -- unrestricted outbound traffic|Restrict egress to required destinations; use VPC endpoints for AWS service access'

  # --- IPv6 ingress open to world ---
  'ipv6_cidr_blocks[[:space:]]*=[[:space:]]*\["::/0"\]|high|NW-011|Security group IPv6 ingress open to ::/0 (entire internet)|Restrict IPv6 CIDR blocks to specific ranges; apply same rules as IPv4 restrictions'

  # --- VPC without flow logs ---
  'aws_flow_log[[:space:]]+"[^"]*"[[:space:]]*\{|high|NW-012|VPC flow log resource found -- verify it captures all traffic (traffic_type = ALL)|Enable VPC flow logs with traffic_type = "ALL" and deliver to CloudWatch or S3 for analysis'

  # --- Elasticsearch domain with public access ---
  'enforce_https[[:space:]]*=[[:space:]]*false|critical|NW-013|HTTPS enforcement disabled -- data transmitted in plaintext|Set enforce_https = true and tls_security_policy = "Policy-Min-TLS-1-2-2019-07"'

  # --- ElastiCache without subnet group ---
  'aws_elasticache_cluster[[:space:]]+"[^"]*"[[:space:]]*\{|high|NW-014|ElastiCache cluster detected -- verify it uses a subnet_group_name in a private VPC|Place ElastiCache in private subnets with a dedicated subnet group; never expose to internet'

  # --- Load balancer on HTTP only (no HTTPS) ---
  'protocol[[:space:]]*=[[:space:]]*"HTTP".*load_balancer|high|NW-015|Load balancer listener using HTTP protocol -- traffic not encrypted|Use HTTPS (port 443) with an ACM certificate; redirect HTTP to HTTPS'
)

# ============================================================================
# 4. EN / ENCRYPTION (EN-001 through EN-015)
# ============================================================================

declare -a CLOUDGUARD_EN_PATTERNS=()

CLOUDGUARD_EN_PATTERNS+=(
  # --- EBS volume with encrypted = false ---
  'encrypted[[:space:]]*=[[:space:]]*false|critical|EN-001|Resource with encrypted = false -- data stored without encryption at rest|Set encrypted = true and specify a KMS key for encryption at rest'

  # --- KMS key without rotation ---
  'enable_key_rotation[[:space:]]*=[[:space:]]*false|high|EN-002|KMS key rotation explicitly disabled -- compromised keys remain active indefinitely|Set enable_key_rotation = true for automatic annual key rotation'

  # --- RDS instance without encryption ---
  'storage_encrypted[[:space:]]*=[[:space:]]*false|critical|EN-003|RDS/Aurora storage encryption disabled -- database data stored in plaintext|Set storage_encrypted = true; note: encryption must be enabled at creation time'

  # --- Resource without SSL/TLS certificate ---
  'aws_lb_listener[[:space:]]+"[^"]*"[[:space:]]*\{|high|EN-004|Load balancer listener detected -- verify ssl_policy and certificate_arn are configured|Add certificate_arn from ACM and set ssl_policy to ELBSecurityPolicy-TLS-1-2-2017-01 or newer'

  # --- ElastiCache without transit encryption ---
  'transit_encryption_enabled[[:space:]]*=[[:space:]]*false|high|EN-005|ElastiCache transit encryption disabled -- data in transit sent in plaintext|Set transit_encryption_enabled = true and at_rest_encryption_enabled = true'

  # --- Weak TLS version (1.0 or 1.1) ---
  'TLS[_-]?1[_.-]?[01]|high|EN-006|Weak TLS version (1.0 or 1.1) detected -- vulnerable to known attacks|Use TLS 1.2 or 1.3 minimum; update ssl_policy to a modern policy'

  # --- S3 bucket without SSE (duplicate check from storage perspective) ---
  'server_side_encryption_configuration[[:space:]]*\{|critical|EN-007|S3 SSE configuration block found -- verify sse_algorithm is AES256 or aws:kms|Set sse_algorithm = "aws:kms" with a dedicated KMS key for S3 encryption'

  # --- Redshift cluster without encryption ---
  'aws_redshift_cluster[[:space:]]+"[^"]*"[[:space:]]*\{|critical|EN-008|Redshift cluster detected -- verify encrypted = true is set|Add encrypted = true and kms_key_id; encryption must be enabled at cluster creation'

  # --- SQS queue without encryption ---
  'aws_sqs_queue[[:space:]]+"[^"]*"[[:space:]]*\{|medium|EN-009|SQS queue detected -- verify kms_master_key_id is set for server-side encryption|Add kms_master_key_id with a KMS key ARN for SQS server-side encryption'

  # --- SNS topic without encryption ---
  'aws_sns_topic[[:space:]]+"[^"]*"[[:space:]]*\{|medium|EN-010|SNS topic detected -- verify kms_master_key_id is set for encryption|Add kms_master_key_id with a KMS key ARN for SNS topic encryption'

  # --- CloudWatch log group without KMS encryption ---
  'aws_cloudwatch_log_group[[:space:]]+"[^"]*"[[:space:]]*\{|medium|EN-011|CloudWatch log group detected -- verify kms_key_id is set for encryption|Add kms_key_id for log group encryption; protect sensitive log data at rest'

  # --- EBS default encryption not enabled ---
  'aws_ebs_default_kms_key[[:space:]]+"[^"]*"[[:space:]]*\{|high|EN-012|EBS default KMS key resource found -- verify aws_ebs_encryption_by_default is also enabled|Add aws_ebs_encryption_by_default resource to ensure all new EBS volumes are encrypted'

  # --- Aurora cluster without encryption ---
  'aws_rds_cluster[[:space:]]+"[^"]*"[[:space:]]*\{|critical|EN-013|Aurora/RDS cluster detected -- verify storage_encrypted = true is set|Set storage_encrypted = true and kms_key_id; must be set at cluster creation time'

  # --- Kinesis stream without encryption ---
  'aws_kinesis_stream[[:space:]]+"[^"]*"[[:space:]]*\{|medium|EN-014|Kinesis stream detected -- verify encryption_type = "KMS" is configured|Set encryption_type = "KMS" and kms_key_id for stream encryption'

  # --- Secrets Manager without customer-managed KMS key ---
  'aws_secretsmanager_secret[[:space:]]+"[^"]*"[[:space:]]*\{|low|EN-015|Secrets Manager secret detected -- verify kms_key_id is set for CMK encryption|Add kms_key_id for customer-managed key instead of default AWS-managed key'
)

# ============================================================================
# 5. LG / LOGGING & MONITORING (LG-001 through LG-015)
# ============================================================================

declare -a CLOUDGUARD_LG_PATTERNS=()

CLOUDGUARD_LG_PATTERNS+=(
  # --- Missing CloudTrail ---
  'aws_cloudtrail[[:space:]]+"[^"]*"[[:space:]]*\{|critical|LG-001|CloudTrail resource found -- verify is_multi_region_trail = true and enable_logging = true|Enable CloudTrail in all regions with S3 logging, CloudWatch integration, and log file validation'

  # --- CloudTrail not multi-region ---
  'is_multi_region_trail[[:space:]]*=[[:space:]]*false|high|LG-002|CloudTrail is not multi-region -- API activity in other regions goes unmonitored|Set is_multi_region_trail = true to capture API calls across all AWS regions'

  # --- VPC without flow logs ---
  'aws_vpc[[:space:]]+"[^"]*"[[:space:]]*\{|high|LG-003|VPC resource detected -- verify aws_flow_log is configured for this VPC|Create an aws_flow_log resource for the VPC with traffic_type = "ALL" for full visibility'

  # --- GuardDuty not enabled ---
  'aws_guardduty_detector[[:space:]]+"[^"]*"[[:space:]]*\{|high|LG-004|GuardDuty detector found -- verify enable = true for threat detection|Set enable = true on the GuardDuty detector for continuous threat monitoring'

  # --- Missing CloudWatch alarm ---
  'aws_cloudwatch_metric_alarm[[:space:]]+"[^"]*"[[:space:]]*\{|medium|LG-005|CloudWatch alarm found -- verify alarm_actions and threshold are properly configured|Configure alarm_actions with SNS topic ARN for notification on threshold breach'

  # --- Missing SNS notification topic ---
  'aws_sns_topic[[:space:]]+"[^"]*"[[:space:]]*\{|medium|LG-006|SNS topic detected -- verify it has subscriptions for security notifications|Add aws_sns_topic_subscription for email/PagerDuty/Slack alerts on security events'

  # --- S3 access logging disabled ---
  'target_bucket[[:space:]]*=[[:space:]]*""|medium|LG-007|S3 access logging target bucket is empty string -- logging effectively disabled|Set target_bucket to a dedicated logging bucket ARN for access audit trail'

  # --- ALB access logs disabled ---
  'access_logs[[:space:]]*\{[[:space:]]*(#.*)?$|medium|LG-008|ALB access logs block found -- verify enabled = true with S3 bucket configured|Set enabled = true in access_logs block with a dedicated S3 bucket for ALB log storage'

  # --- RDS audit logging not enabled ---
  'enabled_cloudwatch_logs_exports|high|LG-009|RDS CloudWatch log export configuration found -- verify audit logs are included|Include "audit" in enabled_cloudwatch_logs_exports list for database audit logging'

  # --- Lambda without log group ---
  'aws_lambda_function[[:space:]]+"[^"]*"[[:space:]]*\{|medium|LG-010|Lambda function detected -- verify corresponding CloudWatch log group exists with retention|Create an aws_cloudwatch_log_group for the Lambda with appropriate retention_in_days'

  # --- AWS Config recorder not enabled ---
  'aws_config_configuration_recorder[[:space:]]+"[^"]*"[[:space:]]*\{|high|LG-011|AWS Config recorder found -- verify recording_group captures all resource types|Enable AWS Config with all_supported = true to track configuration changes'

  # --- CloudTrail log file validation disabled ---
  'enable_log_file_validation[[:space:]]*=[[:space:]]*false|high|LG-012|CloudTrail log file validation disabled -- logs may be tampered without detection|Set enable_log_file_validation = true to detect unauthorized log modifications'

  # --- Missing CloudWatch metric filters ---
  'aws_cloudwatch_log_metric_filter[[:space:]]+"[^"]*"[[:space:]]*\{|medium|LG-013|CloudWatch metric filter found -- verify pattern covers security-relevant events|Create metric filters for unauthorized API calls, root login, IAM changes, and console sign-in'

  # --- EKS cluster without audit logging ---
  'enabled_cluster_log_types|high|LG-014|EKS cluster log types configuration found -- verify audit logging is included|Include "audit" and "authenticator" in enabled_cluster_log_types for security visibility'

  # --- IAM Access Analyzer not configured ---
  'aws_accessanalyzer_analyzer[[:space:]]+"[^"]*"[[:space:]]*\{|low|LG-015|IAM Access Analyzer found -- verify type = "ACCOUNT" or "ORGANIZATION" is set|Configure Access Analyzer at account or organization level for external access findings'
)

# ============================================================================
# 6. CF / CONFIGURATION & COMPLIANCE (CF-001 through CF-015)
# ============================================================================

declare -a CLOUDGUARD_CF_PATTERNS=()

CLOUDGUARD_CF_PATTERNS+=(
  # --- Missing resource tags ---
  'tags[[:space:]]*=[[:space:]]*\{|medium|CF-001|Resource tags block found -- verify Name, Environment, Owner, and CostCenter tags are present|Add mandatory tags: Name, Environment, Owner, CostCenter, ManagedBy for governance'

  # --- Hardcoded AWS region ---
  'region[[:space:]]*=[[:space:]]*"(us-east-1|us-west-2|eu-west-1|ap-southeast-1)"|medium|CF-002|Hardcoded AWS region string detected -- reduces portability|Use var.region or data.aws_region.current instead of hardcoded region strings'

  # --- Hardcoded AMI ID ---
  'ami-[0-9a-f]{8,17}|medium|CF-003|Hardcoded AMI ID detected -- AMIs are region-specific and become outdated|Use data.aws_ami to dynamically look up the latest AMI by owner and filters'

  # --- Missing backup configuration ---
  'backup_retention_period[[:space:]]*=[[:space:]]*0|high|CF-004|Backup retention period set to 0 -- no automated backups configured|Set backup_retention_period >= 7 for RDS; configure AWS Backup for other resources'

  # --- Missing deletion protection ---
  'deletion_protection[[:space:]]*=[[:space:]]*false|medium|CF-005|Deletion protection explicitly disabled -- accidental deletion possible|Set deletion_protection = true for production databases, load balancers, and critical resources'

  # --- Hardcoded availability zone ---
  'availability_zone[[:space:]]*=[[:space:]]*"[a-z]+-[a-z]+-[0-9][a-z]"|low|CF-006|Hardcoded availability zone detected -- reduces flexibility|Use data.aws_availability_zones or var.availability_zone for dynamic AZ selection'

  # --- Missing auto-scaling configuration ---
  'aws_autoscaling_group[[:space:]]+"[^"]*"[[:space:]]*\{|medium|CF-007|Auto Scaling Group detected -- verify min_size, max_size, and scaling policies are set|Configure appropriate min_size, max_size, desired_capacity, and target tracking scaling policies'

  # --- RDS without multi-AZ ---
  'multi_az[[:space:]]*=[[:space:]]*false|high|CF-008|RDS multi-AZ explicitly disabled -- single point of failure for database|Set multi_az = true for production RDS instances to enable automatic failover'

  # --- Terraform backend without encryption ---
  'backend[[:space:]]*"s3"[[:space:]]*\{|high|CF-009|Terraform S3 backend detected -- verify encrypt = true and dynamodb_table for state locking|Add encrypt = true and dynamodb_table in the backend block for state encryption and locking'

  # --- Missing health check ---
  'aws_lb_target_group[[:space:]]+"[^"]*"[[:space:]]*\{|medium|CF-010|Load balancer target group detected -- verify health_check block is configured|Add health_check block with path, healthy_threshold, and interval for proper health monitoring'

  # --- Non-standard resource naming ---
  'name[[:space:]]*=[[:space:]]*"[A-Z]|low|CF-011|Resource name starts with uppercase -- may not follow naming convention|Use lowercase with hyphens or underscores for consistent resource naming (e.g., my-resource-name)'

  # --- Terraform provider without version constraint ---
  'provider[[:space:]]*"aws"[[:space:]]*\{|medium|CF-012|AWS provider block detected -- verify version constraint is set in required_providers|Add version constraint in required_providers to prevent breaking changes from provider updates'

  # --- Missing prevent_destroy lifecycle ---
  'lifecycle[[:space:]]*\{|low|CF-013|Lifecycle block found -- verify prevent_destroy = true for critical resources|Add prevent_destroy = true for production databases, S3 buckets, and other irreplaceable resources'

  # --- Terraform module without outputs ---
  'module[[:space:]]*"[^"]*"[[:space:]]*\{|low|CF-014|Terraform module invocation found -- verify the module defines outputs for key resource attributes|Ensure modules output resource IDs, ARNs, and endpoints for downstream consumption'

  # --- Hardcoded AWS account ID ---
  '[0-9]{12}|medium|CF-015|12-digit number detected -- may be a hardcoded AWS account ID|Use data.aws_caller_identity.current.account_id instead of hardcoding account IDs'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
cloudguard_pattern_count() {
  local count=0
  count=$((count + ${#CLOUDGUARD_S3_PATTERNS[@]}))
  count=$((count + ${#CLOUDGUARD_IM_PATTERNS[@]}))
  count=$((count + ${#CLOUDGUARD_NW_PATTERNS[@]}))
  count=$((count + ${#CLOUDGUARD_EN_PATTERNS[@]}))
  count=$((count + ${#CLOUDGUARD_LG_PATTERNS[@]}))
  count=$((count + ${#CLOUDGUARD_CF_PATTERNS[@]}))
  echo "$count"
}

# List patterns by category
cloudguard_list_patterns() {
  local filter_type="${1:-all}"
  local -n _cg_patterns_ref

  case "$filter_type" in
    S3) _cg_patterns_ref=CLOUDGUARD_S3_PATTERNS ;;
    IM) _cg_patterns_ref=CLOUDGUARD_IM_PATTERNS ;;
    NW) _cg_patterns_ref=CLOUDGUARD_NW_PATTERNS ;;
    EN) _cg_patterns_ref=CLOUDGUARD_EN_PATTERNS ;;
    LG) _cg_patterns_ref=CLOUDGUARD_LG_PATTERNS ;;
    CF) _cg_patterns_ref=CLOUDGUARD_CF_PATTERNS ;;
    all)
      cloudguard_list_patterns "S3"
      cloudguard_list_patterns "IM"
      cloudguard_list_patterns "NW"
      cloudguard_list_patterns "EN"
      cloudguard_list_patterns "LG"
      cloudguard_list_patterns "CF"
      return
      ;;
    *)
      echo "Unknown category: $filter_type"
      echo "Available: S3, IM, NW, EN, LG, CF"
      return 1
      ;;
  esac

  for entry in "${_cg_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "%-12s %-8s %s\n" "$check_id" "$severity" "$description"
  done
}

# Get patterns array name for a category
get_cloudguard_patterns_for_category() {
  local category="$1"
  case "$category" in
    S3) echo "CLOUDGUARD_S3_PATTERNS" ;;
    IM) echo "CLOUDGUARD_IM_PATTERNS" ;;
    NW) echo "CLOUDGUARD_NW_PATTERNS" ;;
    EN) echo "CLOUDGUARD_EN_PATTERNS" ;;
    LG) echo "CLOUDGUARD_LG_PATTERNS" ;;
    CF) echo "CLOUDGUARD_CF_PATTERNS" ;;
    *)  echo "" ;;
  esac
}

# All category names for iteration
get_all_cloudguard_categories() {
  echo "S3 IM NW EN LG CF"
}

# Category labels for display
get_cloudguard_category_label() {
  local category="$1"
  case "$category" in
    S3) echo "Storage Security" ;;
    IM) echo "IAM & Permissions" ;;
    NW) echo "Network Security" ;;
    EN) echo "Encryption" ;;
    LG) echo "Logging & Monitoring" ;;
    CF) echo "Configuration & Compliance" ;;
    *)  echo "$category" ;;
  esac
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# Get patterns limited by tier count
# Usage: get_tier_limited_patterns "S3" 30
# Returns patterns array limited to (limit / 6) per category
get_tier_pattern_count_per_category() {
  local total_limit="$1"
  echo $(( total_limit / 6 ))
}
