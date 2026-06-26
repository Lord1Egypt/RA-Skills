---
name: cpa-manager
description: CLIProxyAPI (CPA) 运维工具。基于官方 cpa-warden，用于库存扫描、401/限额清理、上传、补池与本地状态跟踪。
---

# CPA Manager - CLIProxyAPI 运维

基于官方 [cpa-warden](https://github.com/fantasticjoe/cpa-warden)。

## 先说结论

**以后默认不要再用 `--base-url` / `--token` 直传参数。**
当前官方用法应以 `config.json` 为主：

```bash
cd /path/to/cpa-manager/scripts
python3 cpa_warden.py --mode scan --config config.json
```

本地已验证：旧文档里的 `--base-url http://cpa-service:8317 --token your-token` 写法会报参数不识别。

---

## 配置路径

| 路径 | 说明 |
|------|------|
| `/path/to/cpa/config.yaml` | CPA 主配置文件（Docker 挂载） |
| `/path/to/cpa/auth/` | OAuth 认证文件目录（CPA 实际扫描源） |
| `http://cpa-service:8317` | CPA 服务地址（根据实际部署调整） |
| `your-management-token` | Management Token（从CPA配置中获取） |
| `/path/to/cpa-manager/scripts/config.json` | cpa-warden 本地配置 |

---

## 官方能力边界

cpa-warden 不是"只扫 401 的小脚本"，而是一个**有状态的 CPA 运维工具**，至少包含：

1. 拉取库存：`GET /v0/management/auth-files`
2. 用 `api-call` 并发探测 `wham/usage`
3. 维护模式删除 401 / 处理限额
4. 上传 auth 文件到 CPA
5. maintain-refill 补池
6. 本地 SQLite 状态跟踪
7. 导出 401 / quota JSON 结果

因此要区分三层口径：
- **CPA 库存层**：`/v0/management/auth-files`
- **cpa-warden 探测层**：通过 `api-call` 实测是否 401 / quota
- **本地状态层**：SQLite + 导出 JSON

它们**不是同一个口径**。

---

## 标准使用

### 1) 扫描（只读，不改远端）

```bash
cd /path/to/cpa-manager/scripts
python3 cpa_warden.py --mode scan --config config.json
```

适用：
- 看当前池子健康度
- 导出 401 / quota 列表
- 先预览再决定是否清理

### 2) 维护（扫描后执行删除/禁用）

```bash
python3 cpa_warden.py --mode maintain --config config.json --yes
```

适用：
- 删除 401
- 处理限额账号
- 执行恢复启用（若配置开启）

### 3) 预览维护（不删除 401）

```bash
python3 cpa_warden.py --mode maintain --config config.json --no-delete-401
```

适用：
- 先看 maintain 会命中哪些账号
- 不想立刻改远端状态时

### 4) 上传 auth 文件

```bash
python3 cpa_warden.py --mode upload --config config.json --upload-dir ./auth_files
```

### 5) maintain-refill

```bash
python3 cpa_warden.py --mode maintain-refill --config config.json --min-valid-accounts 100 --upload-dir ./auth_files
```

---

## 本地产物

cpa-warden 会写以下本地状态文件：

- `cpa_warden_state.sqlite3` - 本地状态数据库
- `cpa_warden_401_accounts.json` - 当前探测出的 401 列表
- `cpa_warden_quota_accounts.json` - 当前探测出的限额列表
- `cpa_warden.log` - 运行日志

**注意：这些文件会影响你对状态的理解。**
不要把它们误当成 CPA 实时库存本身。

---

## 最佳实践

### A. 管理扫描源目录
CPA 容器实际读的是 auth 目录。确保该目录只包含有效的认证文件，避免包含备份、日志等子目录。

### B. 备份策略
备份目录必须移出 auth 根目录外部，避免被 CPA 递归扫描。

### C. 文件命名规范
如果需要整理文件名，先离线 dedupe，再一次性生成新目录，最后原子替换。

### D. 状态验证
`auth-files` active 不等于账号真可用。清池要以 cpa-warden 的 probe 结果为准，不要只看库存列表。

---

## 推荐操作顺序

### 日常健康检查
1. `scan`
2. 看 401 / quota 输出
3. 决定是否 `maintain`

### 需要清池时
1. 确认 auth 目录下没有 backup/trash/logs 子目录
2. `maintain --yes`
3. 再 `scan` 复查剩余 401
4. 必要时再做下一轮 `maintain`

### 需要整理命名时
1. 先备份到 auth 根目录外部
2. 只基于**唯一 basename 集**做重排
3. 重命名后重启 CPA
4. 再 `scan`

---

## 当前本地推荐命令

```bash
cd /path/to/cpa-manager/scripts

# 扫描
python3 cpa_warden.py --mode scan --config config.json

# 清理 401 / 限额
python3 cpa_warden.py --mode maintain --config config.json --yes

# 上传
python3 cpa_warden.py --mode upload --config config.json --upload-dir ./auth_files
```

---

## 参考

- 官方 README：`https://github.com/fantasticjoe/cpa-warden?tab=readme-ov-file`
- 本地脚本：`/path/to/cpa-manager/scripts/cpa_warden.py`
- CPA 主配置：`/path/to/cpa/config.yaml`
- CPA auth 目录：`/path/to/cpa/auth/`
- 容器内挂载点：`/path/to/cpa/auth`

---

## 注意事项

- 不要再用旧文档里的 `--base-url --token` 直接传参
- 不要把 backup/trash/logs 放进 auth 目录
- 不要把 `auth-files` 库存口径当成 probe 口径
- 不要在生产 auth 目录上连续试验式重命名
- 不要把"删除接口返回成功"直接当成库存已收敛，必须再复查

## ClawHub 简短说明（可用于上传描述）

用于基于 auth 文件池的 CLIProxyAPI/CPA 运维，支持库存扫描、401/限额探测、清池、上传与补池。
适合有 management API 和本地 auth 目录的部署场景；不适用于纯转发型代理服务。
