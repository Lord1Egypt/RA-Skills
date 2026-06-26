---
name: "byted-byteplus-cdn"
description: "Skill for BytePlus CDN domain and policy management, purge and prefetch, and log delivery. When you need to use BytePlus CDN acceleration services, you can refer to this skill's guide to complete CDN domain access, origin configuration, policy template, purge and prefetch, and offline/real-time log delivery tasks."
version: "v1.1"
required_env_vars:
  - "BYTEPLUS_AK": "BytePlus Access Key for API authentication"
  - "BYTEPLUS_SK": "BytePlus Secret Key for API authentication"
primary_credential: "BytePlus account credentials"
---

# BytePlus CDN Skill

## Installation and Configuration

Before using the BytePlus CDN Skill, please configure your environment following these steps.

### 1. Install Dependencies

Before using this skill, you need to install Python dependencies first. Please run the following command in the terminal:

```bash
cd /path/to/byteplus-cdn
pip3 install -r reference/requirements.txt
```

### 2. Configure Authentication (Credentials)

Before executing any commands, you need to set the environment variables `BYTEPLUS_AK` and `BYTEPLUS_SK` for secure authentication. This is a prerequisite for calling BytePlus OpenAPI.

**Security Best Practices**:
- Create a `.env` file **only in the project root directory**
- Restrict BytePlus API keys to only the CDN permissions needed (least privilege principle)
- Never commit `.env` file to version control

You can create a `.env` file in the project root directory to store the AK and SK environment variables:
```
BYTEPLUS_AK=YourAccessKey
BYTEPLUS_SK=YourSecretKey
```

#### Windows PowerShell
```powershell
$env:BYTEPLUS_AK="YourAccessKey"
$env:BYTEPLUS_SK="YourSecretKey"
```

#### Linux / macOS
```bash
export BYTEPLUS_AK="YourAccessKey"
export BYTEPLUS_SK="YourSecretKey"
```

### 3. Verify Installation

After configuration, you can try running the CLI tool's help command to verify if the installation is successful:

```bash
python3 scripts/cli.py --help
```

If the help information is successfully output, it indicates that the environment configuration is complete.

---

## Feature Overview

This is a local command-line toolkit for operating BytePlus CDN, fully corresponding to all the instruction requirements in `CLI.md`. It includes the following core features:

1. **Add CDN Domain** - supports two methods:
   - Method 1: Directly configure the origin (supports Alibaba Cloud OSS, Tencent Cloud COS, AWS S3, BytePlus TOS, IP, Domain)
   - Method 2: Bind an existing distribution policy template
2. **Create Policy Template** - pre-configure and publish CDN distribution policies
3. **Purge Cache** - file refresh and directory refresh
4. **Prefetch Cache** - pre-load files from origin to CDN nodes
5. **Create Offline/Real-time Log Delivery Tasks** - configure log delivery destinations, supporting delivery to platforms like S3, BytePlus TOS, Splunk, etc.

**✨ New Feature: Interactive Guide (Interactive Mode)**
If you run a command without any parameters (e.g., `python3 scripts/cli.py add-domain oss`), the CLI will guide you through the required parameters step by step like a wizard!

## Agent Interaction Guidelines

When the Agent (AI) finds that it needs to collect missing parameters from the user, **must** follow these interaction specifications:
1. **Option Type Parameters**: Must use the `AskUserQuestion` tool to let the user make single or multiple selections (e.g., origin type, service type).
2. **In-depth Understanding and Transparency of Underlying Prompts**: Before calling `AskUserQuestion` to collect parameters, you **must** read the `prompt` and `help` definitions of the corresponding parameters in `scripts/cli.py`.
3. **Construct Precise Collection Forms**: In the collection form (AskUserQuestion) presented to the user, the `description` or options you provide **must fully include** the special prompts from `cli.py`! For example: if `cli.py` specifies that `--domain` can input `"all"` to represent all domains, you **must** provide a special `["All Domains (all)"]` option in the form, and must not make up irrelevant test options yourself.
4. **String Input Type Parameters**: Except for special values supported by the underlying layer (such as all), always provide a `["Manual Input (Please select Other to input)"]` option, allowing the user to evoke a friendly text input prompt via the system's own `Other` option.

## Command List (Corresponding to CLI List)

The following examples all demonstrate usage in non-interactive mode (bringing all parameters at once). If you want to use interactive mode, simply omit the `--xxx` parameters.

### 1-6. Add CDN Domain (`add-domain`)

* **Alibaba Cloud OSS (CLI 1)**
  ```bash
  python3 scripts/cli.py add-domain oss --domain YOUR_DOMAIN_NAME --origin YOUR_BUCKET_NAME.YOUR_OSS_REGION.aliyuncs.com --service-type web --private-bucket yes --bucket-ak YOUR_AK --bucket-sk YOUR_SK --apply-recommended yes
  ```
* **Tencent Cloud COS (CLI 2)**
  ```bash
  python3 scripts/cli.py add-domain cos --domain YOUR_DOMAIN_NAME --origin YOUR_BUCKET_NAME.cos.YOUR_COS_REGION.myqcloud.com --service-type download --private-bucket no --apply-recommended yes
  ```
* **AWS S3 (CLI 3)**
  ```bash
  python3 scripts/cli.py add-domain aws --domain YOUR_DOMAIN_NAME --origin YOUR_BUCKET_NAME.s3.YOUR_AWS_REGION.amazonaws.com --service-type video --private-bucket yes --bucket-ak YOUR_AK --bucket-sk YOUR_SK --region YOUR_AWS_REGION --apply-recommended yes
  ```
* **BytePlus TOS (CLI 4)**
  ```bash
  python3 scripts/cli.py add-domain tos --domain YOUR_DOMAIN_NAME --origin YOUR_BUCKET_NAME.YOUR_TOS_REGION.bytepluses.com --service-type web --private-bucket yes --apply-recommended yes
  ```
* **IP Origin (CLI 5)**
  ```bash
  python3 scripts/cli.py add-domain ip --domain YOUR_DOMAIN_NAME --origin YOUR_IP_ADDRESS --service-type web --apply-recommended yes
  ```
* **Domain Origin (CLI 6)**
  ```bash
  python3 scripts/cli.py add-domain domain --domain YOUR_DOMAIN_NAME --origin YOUR_ORIGIN_DOMAIN --service-type web --apply-recommended yes
  ```
* **Bind Policy Template** - add a domain by binding a published distribution policy
  ```bash
  # Basic Usage
  python3 scripts/cli.py add-domain template --domain YOUR_DOMAIN_NAME --service-template-id tpl-s2Q4mq
  
  # Enable HTTPS
  python3 scripts/cli.py add-domain template --domain YOUR_DOMAIN_NAME --service-template-id tpl-s2Q4mq --https-switch on --cert-id cert-044833503b2349b4b42c2e80b0aa8c23
  
  # Full Usage (including cipher policy and rule engine policy)
  python3 scripts/cli.py add-domain template --domain YOUR_DOMAIN_NAME,img.YOUR_DOMAIN_NAME --service-template-id tpl-s2Q4mq --cipher-template-id tpl-cqgRvW --https-switch on --cert-id cert-044833503b2349b4b42c2e80b0aa8c23 --rule-template-ids tpl-re9gvl6,tpl-abc123
  ```

### 7-11. Create Policy Template (`create-template`)

The command structure is similar to `add-domain`, using `--title` and `--message` instead of `--domain`.

* **Alibaba Cloud OSS (CLI 7)**
  ```bash
  python3 scripts/cli.py create-template oss --title "YOUR_TEMPLATE_TITLE" --origin YOUR_BUCKET_NAME.YOUR_OSS_REGION.aliyuncs.com --service-type web --private-bucket no --apply-recommended yes
  ```
* Other cloud providers and origin types (cos, aws, ip, domain) are the same, just use `create-template <origin-type>`.

### 12-13. Refresh Cache (`refresh purge`)

* **File Refresh (CLI 12)** - up to 100 URLs
  ```bash
  python3 scripts/cli.py refresh file --urls "https://YOUR_DOMAIN_NAME/1.jpg,https://YOUR_DOMAIN_NAME/2.jpg"
  ```

* **Directory Refresh (CLI 13)** - up to 50 directories, must end with `/`
  ```bash
  python3 scripts/cli.py refresh dir --urls "https://YOUR_DOMAIN_NAME/images/,https://YOUR_DOMAIN_NAME/assets/"
  ```

### 14. Prefetch Cache (`preload prefetch`)

* **File Pre-warm (CLI 14)** - up to 100 URLs
  ```bash
  python3 scripts/cli.py preload --urls "https://YOUR_DOMAIN_NAME/1.jpg,https://YOUR_DOMAIN_NAME/2.jpg"
  ```

### 15. Create Offline Log Delivery Task (`log-offline`)

Deliver offline logs of domains to object storage (TOS/S3).

* **Deliver to TOS**
  ```bash
  python3 scripts/cli.py log-offline tos --bucket YOUR_BUCKET_NAME/logs --domain YOUR_DOMAIN_NAME --private-bucket no --endpoint YOUR_TOS_ENDPOINT --region YOUR_TOS_REGION
  ```

* **Deliver to Private S3**
  ```bash
  python3 scripts/cli.py log-offline s3 --bucket YOUR_BUCKET_NAME/logs --domain YOUR_DOMAIN_NAME --endpoint YOUR_S3_ENDPOINT --region YOUR_AWS_REGION --private-bucket yes --ak YOUR_AK --sk YOUR_SK
  ```

### 16. Create Real-time Log Delivery Task (`log-realtime`)

Deliver real-time logs of domains to external systems (TLS, SLS, HttpServer, Splunk, BigQuery).

* **Deliver to TLS**
  ```bash
  python3 scripts/cli.py log-realtime tls --domain YOUR_DOMAIN_NAME --project-id YOUR_PROJECT_ID --region HongKong --topic-name YOUR_TOPIC_NAME --ttl 30
  ```

* **Deliver to SLS**
  ```bash
  python3 scripts/cli.py log-realtime sls --domain YOUR_DOMAIN_NAME --sls-endpoint YOUR_SLS_ENDPOINT --project YOUR_PROJECT_NAME --log-store YOUR_LOG_STORE --ak YOUR_AK --sk YOUR_SK
  ```

* **Deliver to HTTP Server**
  ```bash
  python3 scripts/cli.py log-realtime http_server --domain YOUR_DOMAIN_NAME --url https://log-server.YOUR_DOMAIN_NAME/ingest --auth-mechanism true --secret-key YOUR_SECRET_KEY --compress-type gzip
  ```

* **Deliver to Splunk**
  ```bash
  python3 scripts/cli.py log-realtime splunk --domain YOUR_DOMAIN_NAME --url https://splunk.YOUR_DOMAIN_NAME:8088/services/collector/event --token YOUR_TOKEN
  ```

* **Deliver to BigQuery**
  ```bash
  # Method 1: Pass JSON string directly
  python3 scripts/cli.py log-realtime bigquery --domain YOUR_DOMAIN_NAME --project-id YOUR_GCP_PROJECT_ID --dataset-id YOUR_DATASET_ID --table-id YOUR_TABLE_ID --auth-str '{"type":"service_account",...}'

  # Method 2 (Recommended): Pass JSON via local file (CLI will automatically read and escape)
  python3 scripts/cli.py log-realtime bigquery --domain YOUR_DOMAIN_NAME --project-id YOUR_GCP_PROJECT_ID --dataset-id YOUR_DATASET_ID --table-id YOUR_TABLE_ID --auth-file /path/to/gcp-auth.json
  ```

## Recommended Configuration Description (Only applicable to add-domain and create-template)

When you use `--apply-recommended yes`, the CLI will automatically inject the following CDN optimization configurations based on `--service-type`:

1. **Web Acceleration (web)**
   - Cache key includes all query parameters.
   - Do not cache `.php, .jsp, .asp, .aspx`, and cache all files matched by `/*` root directory for 30 days by default.
   - Enable HTML page optimization and Gzip smart compression.
2. **Download Acceleration (download)**
   - Cache key ignores all query parameters.
   - Enable Range shard origin pull, origin redirect follow, and Multi Range optimization.
3. **VOD Acceleration (video)**
   - Includes all optimizations from download acceleration.
   - Additionally enable video seek feature.

## Executable File Function Description

If you need to understand the function description of the multiple executable files provided in the scripts folder, you can directly refer to the `reference/about.txt` file.
