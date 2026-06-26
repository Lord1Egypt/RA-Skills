# BioFlow Project Snapshot

## Project Intro
1. Framework: FastAPI + SQLAlchemy async + PostgreSQL.
2. API root: `/api/v1`.
3. Main groups:
- `/auth`: 注册、登录、用户信息
- `/datasets`: 上传、列表、详情、下载
- `/token`: 余额与资金账户
- `/algorithms/*`: 任务提交与结果查询
- `/workspaces`, `/jobs`: 工作区与任务列表/详情

## Auth Model
1. Password login endpoint: `POST /api/v1/auth/login`.
2. SMS code endpoint: `POST /api/v1/auth/send_verification_code`.
3. Signup endpoint: `POST /api/v1/auth/signup` (`password2` is required; when `telephone` is provided, `verification_code` is required and validated).
4. Refresh endpoint: `POST /api/v1/auth/refresh`.
5. Protected APIs use BioFlow local JWT Bearer token.
6. Token format: `access_token`, `refresh_token`, `token_type`.

## User and Account Basics
1. Auth user source table is shared `cs.users` (`AuthUser`).
2. BioFlow business data lives in `bioflow` DB.
3. Token balance query uses `/api/v1/token/balance` (person/team account).
4. Default workspace can be listed from `/api/v1/workspaces`.

## Recommended Minimal Demo Path
1. Register/login.
2. Upload one dataset file (`/api/v1/datasets/upload`).
3. Query token balance.
4. Submit one PTMPred job with uploaded `fasta_dataset_id`.
5. Poll job detail until finished.
6. Fetch results list and optionally download csv/fasta.
