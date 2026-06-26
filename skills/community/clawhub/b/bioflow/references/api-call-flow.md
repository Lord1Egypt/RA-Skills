# BioFlow API Call Flow

## 0) Base
1. Base URL: `https://<host>/api/v1`
2. Auth header for protected APIs:
```http
Authorization: Bearer <access_token>
```

## 1) 注册
1. 先发短信验证码：`POST /auth/send_verification_code`
```json
{
  "phone": "13800138000",
  "country_intl": "86"
}
```
2. 再注册：`POST /auth/signup`
3. Body (recommended):
```json
{
  "email": "user@example.com",
  "password": "your_password",
  "password2": "your_password",
  "name": "Your Name",
  "telephone": "13800138000",
  "verification_code": "123456"
}
```
4. Notes:
- `password2` must match `password`.
- In current backend, `verification_code` is checked when `telephone` is provided.
- Optional fields: `organization`, `industry_types`, `job_title`.

## 2) 登录与刷新
1. Login: `POST /auth/login`
```json
{"email":"user@example.com","password":"your_password"}
```
2. Response: save `access_token` + `refresh_token`.
3. Refresh: `POST /auth/refresh`
```json
{"refresh_token":"<refresh_token>"}
```
4. Current user: `GET /auth/me`.

## 3) 工作区与余额
1. List workspace: `GET /workspaces?page=1&page_size=20`
2. Use one `ws_id` (for example `WS...`) in later steps.
3. Balance: `GET /token/balance` (optional query `account=person|team`).

## 4) 上传文件（Dataset）
1. Upload endpoint: `POST /datasets/upload` (`multipart/form-data`).
2. Form fields:
- `file` (required)
- `name` (optional)
- `description` (optional)
- `workspace_id` (optional, value is `ws_id` string, not DB id)
3. Return includes `dataset_id`, `file_type`, `status`.

## 5) 下载文件（Dataset）
1. Get download URL: `GET /datasets/{dataset_id}/download?expires_in=3600`
2. Response includes:
- `download_url` (presigned URL)
- `file_name`
- `expires_at`

## 6) 发起任务（PTMPred 示例）
1. Require an uploaded FASTA dataset (`dataset_id`).
2. `POST /algorithms/ptmpred`
```json
{
  "name": "ptmpred-demo",
  "ws_id": "WSXXXX",
  "fasta_dataset_id": "DSXXXX"
}
```
3. Response includes `id` as `job_id`.

## 7) 查看任务与结果
1. Job detail: `GET /algorithms/ptmpred/{job_id}`
2. Results list: `GET /algorithms/ptmpred/{job_id}/results?page=1&page_size=20`
3. Result download:
- CSV: `GET /algorithms/ptmpred/{job_id}/download?type=csv`
- FASTA: `GET /algorithms/ptmpred/{job_id}/download?type=fasta`

## 8) 通用任务视图（跨算法）
1. Job list: `GET /jobs?ws_id={ws_id}&page=1&page_size=10`
2. Job detail: `GET /jobs/{job_id}`
