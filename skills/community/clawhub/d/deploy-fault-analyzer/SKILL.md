---
name: deploy-fault-analyzer
description: 部署故障分析及解决助手 — 接收日志/报错文本，优先查询 MySQL 故障知识库；未命中时检索 /data/scripts/ 脚本库；支持交互式单条更新故障库并生成 Word 分析报告。
version: 1.2.1
author: Hermes
created: 2026-05-09
---

# 部署故障分析及解决助手

当用户提供日志文件（`.json` `.log`）或包含 error/错误/异常/故障/报错/failed 等关键词的文字内容时，自动分析故障并生成 Word 文档。分析前必须优先查询 MySQL 故障知识库 `fault_knowledge_base.fault_records`，用历史案例提高定位准确率；所有新问题继续记录到 Excel 知识库中累积沉淀，并可同步到数据库。

**⚠️ 交付规则：** Word 报告生成后必须在同一条回复中附带故障分析摘要 + 发送 Word 文件给用户，不能只生成到本地而不发送。

---

## 触发条件

满足以下任一条件即触发：

| 触发方式 | 判定标准 |
|----------|---------|
| **日志文件** | 用户上传/拖入 `.json`、`.log` 文件，或指明文件路径 |
| **报错文本** | 用户消息中包含 `error`/`错误`/`异常`/`故障`/`报错`/`failed`/`failure`/`exception`/`失败` 等关键词 |
| **主动请求** | 用户说"帮我分析这个故障"/"这是什么错"/"帮我看下日志"等 |

排除：用户只是在陈述中顺带提到"没有错误"/"没问题"/"成功了"时不触发。

---

## 故障知识库数据库

### 数据库信息

故障知识库来自部署排期表第 10 个 sheet「故障库」，由 `/data/work/scripts/sync_fault_knowledge_base.py` 同步到 MySQL。

| 项 | 值 |
|----|----|
| 数据库 | `fault_knowledge_base` |
| 主表 | `fault_records` |
| 连接命令 | `docker exec resource_pool_mysql mysql -upool_user -ppool_password_2024 fault_knowledge_base` |
| Python 脚本连库端口 | 宿主机 `33307`（`insert_fault_record.py` 默认已配置） |
| Excel 同步脚本 | `/data/work/scripts/sync_fault_knowledge_base.py` |
| 单条入库脚本 | `/data/work/scripts/insert_fault_record.py` |
| 脚本库检索 | `/data/work/scripts/search_deploy_scripts.py` |
| 默认 Excel | `/data/work/bom/基础平台部署排期表-2026年度.xlsx` |

### 部署脚本库（故障库未命中时的回退检索）

根目录：`/data/scripts/`

| 库目录 | 说明 | 典型场景 |
|--------|------|----------|
| `cephdeployscripts/` | **Ceph 块存储部署/扩容脚本**（Fabric + ceph-deploy） | 新建块存储集群、OSD 扩容、cusmartcache、cephfs、pool 创建 |
| `deploy-perfect-20250821/` | 基座新建部署脚本 | bootstrap、yum、repo、基座、DNS、ironic |
| `kubeos-ansible/` | 双引擎部署脚本 | OpenStack 组件部署/扩容/新建、nova、neutron |

---

### cephdeployscripts 架构与故障索引（块存储必读）

> **用途**：Ceph 块存储**新建部署**与**扩容**的标准脚本库。执行节点一般为部署机（含 `ceph-deploy`/`fabric`），通过 SSH 批量操作 monitor/OSD 节点。故障库未命中且涉及块存储、cinder、osd、pool、扩容时，**优先在本库检索**。

#### 目录结构

```
/data/scripts/cephdeployscripts/
├── blockstorage/              # 主入口：新建 + 扩容
│   ├── fabfile.py             # 核心编排（Fabric），新建/扩容主流程
│   ├── config.json            # 新建集群配置（monitors/osdnodes/disks）
│   ├── expand.json            # 扩容配置（newosdnodes/ebs0001_ip）
│   └── create_cephfs_pool.py  # 创建 CephFS pool + MDS（独立流程）
├── common/
│   └── common.py              # 公共逻辑：集群类型判定、校验、pool/OSD 检查
├── config_samples/            # 各场景配置样例（对照现场 config 用）
│   ├── config_mix.json
│   ├── config_allflash.json
│   ├── config_highperformance.json
│   ├── expand_mix.json
│   └── ...
├── resources/                 # 下发到各节点的辅助脚本/配置
│   ├── check-cusmartcache.sh  # cusmartcache LV 标签与 enable 校验
│   ├── modprobe-cusmartcache.sh
│   ├── clearcephlvm.sh        # 清理 ceph LVM（lv/vg/pv/dm）
│   ├── balancer_osd_pg.sh     # PG 分布与均衡诊断
│   ├── patch-ceph-osd-prestart.sh
│   ├── upgrade_package.sh     # openssl/openssh/libblkid 等版本升级
│   └── extended.ceph.conf
└── cephdeploy/                # 子模块（git），与上层 blockstorage 配合
```

#### 技术栈与执行约定

| 项 | 说明 |
|----|------|
| 编排框架 | Python 2 + **Fabric**（`fabric.api`），远程执行 `run`/`sudo` |
| Ceph 工具 | **ceph-deploy**（`ceph-deploy osd create`、`gatherkeys`、`mon create`） |
| 部署目录 | 各节点 `/opt/cephdeploy`，脚本从 `resources/` 拷贝 |
| 新建配置 | `blockstorage/config.json` |
| 扩容配置 | `blockstorage/expand.json`（含 `newosdnodes`、`ebs0001_ip`） |
| 工作目录 | 执行前 `cd /cephdeployscripts/blockstorage/`（代码内 `WORKDIR`） |

**fabfile.py 函数命名约定**（读代码/日志时对照）：

- `Capital*`：主流程入口（如 `DeployMixOsds`、`AddNewHostsToCluster`）
- `local_*`：部署节点本地执行
- `monitor_*`：monitor 节点
- `osd_*`：OSD 节点
- `all_*`：全部节点（mon + osd）

#### 集群类型（`decide_cluster_type`）

由 `config.json` / `expand.json` 中 `disks` 的 **hdds/ssds 组合**自动判定，**同一集群所有节点类型必须一致**：

| 类型常量 | 名称 | 磁盘特征 | 默认 RBD Pool |
|----------|------|----------|---------------|
| `CLUSTER_TYPE_ALLFLASH` (2) | allflash | 仅 SSD | `volumes-ssd` |
| `CLUSTER_TYPE_ALLNVME` (5) | allnvme | 仅 NVMe SSD | `volumes-nvme` |
| `CLUSTER_TYPE_HIGHPERFORMANCE` (3) | highperformance | SSD+HDD（无 cusmartcache） | `volumes` 或 `volumes-enhance` |
| `CLUSTER_TYPE_MIX` (4) | mix-cusmartcache | SSD+HDD + **cusmartcache** | `volumes` 或 `volumes-enhance` |

**mix 部署模式**（`mixdeploymode`，仅 MIX 集群）：

- `newcluster`：新建 mix 集群（默认）
- `addcusmartcacheforbcache`：为已有 bcache 补 cusmartcache
- `addcusmartcacheforhdd`：为 HDD 补 cusmartcache

**HCUFS 特殊集群**：8×NVMe + 60×HDD（`is_hcufs_cluster`），布局 `[8,8,8,8,7,7,7,7]` HDD/SSD 配对。

#### 新建部署主流程（`python fabfile.py` 或 `fab -f fabfile.py`）

```
Init() → 读 config.json → 校验磁盘/IP/挂载
  → all_generateauth / all_sshnopassword / all_systemconfig
  → all_do_misc_check（包版本、tuned、firewalld/SELinux）
  → all_install_ceph_package（mix 时含 cusmartcache）
  → CreateMonMgr() → Deploy*Osds() → RestartAllOsds() → Check*OsdCount()
  → 创建 pool（images + volumes*）+ client.cinder/client.glance + balancer
```

按集群类型分支：`DeployAllFlashOsds` / `DeployHighPerformaceOsds` / `DeployMixOsds`。

**新建成功判定**（`CheckNewClusterDeployResult`）：mon/mgr 进程数 = 配置数；`totalosd == uposd == inosd == total_data_disk_num`；mix 时 **cusmartcache 数量 = OSD 数量**。

#### 扩容主流程（`AddNewHostsToCluster`）

```
LoadExpandConfig() → 读 expand.json
  → check_expand_mon_osd / check_all_disks
  → decide_cluster_type（扩容节点类型）
  → get_expand_type（扩展现有 pool 或新建 pool）
  → IsEbs001MixNode()（mix 扩容时检查 ebs0001 是否 mix 节点）
  → ceph-deploy gatherkeys → 新节点 init（装包、拷 keyring、清盘）
  → Deploy*Osds() → Check*ExpandResult()
```

**扩容成功判定**：`totalosd - ORIGINALTOTAL == 新增 OSD 数`；失败常见日志：`some osds is FAILED, please double check your configuration`。

**expand_type**：

- `expand_current_pool`：OSD 加入现有 pool（如 `volumes`、`volumes-ssd`、`cephfs-data`）
- `create_new_pool`：需手工创建新 pool（日志提示 `please create new pool`）

#### CephFS 独立流程（`create_cephfs_pool.py`）

与块存储 RBD 新建并行可选步骤，依赖已有 Ceph 集群 + `config.json` 中 monitors 与 `ceph.conf` 一致：

```
CreateCephfsForCluster()
  → 安装 ceph-mds → 创建 MDS → 按主机名前缀创建 pool → 挂载目录初始化
```

主机名前缀 → pool 规格映射（`node_pool_map`）：`ebs`/`ebn`/`hci` → `cephfs-metadata`/`cephfs-data`；`nasssd` → `*-ssd`；`nashdden` → `*-enhance` 等。

#### 故障场景 → 脚本索引（Agent 检索用）

| 故障现象 / 关键词 | 优先检索路径 | 脚本内关注点 |
|-------------------|--------------|--------------|
| `osd node ip mismatch` / 配置 IP 不一致 | `blockstorage/fabfile.py` `LoadConfig`/`LoadExpandConfig` | `osdnodes` 与 `disks[].ips` 必须完全一致 |
| `not support nvme partition` / `ssd partition` | `fabfile.py` LoadConfig | SSD 不允许分区设备 |
| `no enough space for ssd` / `to many hdds` | `fabfile.py` osd_deploy_* | HDD/SSD 容量比、`MAXHDDPERSSD=6` |
| `some osds is FAILED` / OSD 数量不对 | `common/common.py` `CheckNewClusterDeployResult` | `ceph -s`、`pgrep ceph-osd`、cusmartcache 数量 |
| `cusmartcache num mismatch` | `common/common.py` + `resources/check-cusmartcache.sh` | `/proc/cusmartcache/`、`cusc_cli`、`lv_tags` |
| `cusmartcache kernel module not loaded` | `resources/modprobe-cusmartcache.sh` | `cusmartcache.ko`、`depmod`、`insmod` |
| `there are N objects in cluster` 无法新建 | `common/common.py` `CheckClusterObjectNum` | 集群已有数据，需清 pool 再部署 |
| `invalid expand pool` | `common/common.py` `check_expand_pool` | 扩容 pool 名与节点类型不匹配 |
| `ebs0001 is not mix node` | `common/common.py` `IsEbs001MixNode` | `expand.json` 中 `ebs0001_ip`/`ebs0001_password` |
| `host deploy type error` | `common/common.py` `decide_cluster_type` | 各节点磁盘类型不一致 |
| `package.*version` / openssl openssh | `common/common.py` `all_do_misc_check` | `resources/upgrade_package.sh` |
| LVM 激活失败 / 重启后 OSD down | `common/common.py` `osds_config_rc_local` | `ceph-volume lvm activate --all` |
| PG 不均衡 / incomplete pgs | `resources/balancer_osd_pg.sh` | `ceph pg dump`、primary PG 分布 |
| 清盘重装 / LVM 残留 | `resources/clearcephlvm.sh` | `lvremove`/`vgremove`/`pvremove` |
| cephfs pool / mds 创建失败 | `blockstorage/create_cephfs_pool.py` | monitors 与 ceph.conf 一致性、主机名前缀 |
| `ceph-deploy osd create` 失败 | `fabfile.py` `osd_deploy_*` | `wipefs`、`sgdisk`、`block-db`/`block-wal`/`data` 路径 |
| mix 扩容降级 highperformance | `fabfile.py` `LoadExpandConfig` | ebs0001 无 cusmartcache 时自动降级 |

#### 推荐检索命令（块存储）

```bash
# 1. 按现象检索（module 填 块存储）
python3 /data/work/scripts/search_deploy_scripts.py \
  --query "osd FAILED cusmartcache ceph-deploy" \
  --module "块存储" \
  --path-contains "cephdeployscripts/blockstorage" \
  --path-contains "cephdeployscripts/common" \
  --top 8 --json

# 2. 配置/校验类
python3 /data/work/scripts/search_deploy_scripts.py \
  --query "osd node ip mismatch expand.json config.json" \
  --module "块存储" \
  --path-contains "cephdeployscripts" \
  --top 5 --json

# 3. cusmartcache 专项
python3 /data/work/scripts/search_deploy_scripts.py \
  --query "cusmartcache cusc_cli lv_tags proc/cusmartcache" \
  --module "块存储" \
  --path-contains "cephdeployscripts/resources" \
  --top 5 --json
```

命中后须阅读对应脚本中的**校验分支与 exit 条件**（见 Step 2.6C），再给出可执行的排查/修复步骤。

---

当用户说“同步故障库”“把 Excel 故障库入库”等含义时，执行以下流程：

```bash
# 1. 先检查 Excel 可解析和有效行数
python3 /data/work/scripts/sync_fault_knowledge_base.py --dry-run

# 2. 正式同步，重复执行不会重复插入同一条故障
python3 /data/work/scripts/sync_fault_knowledge_base.py

# 3. 验证行数和去重
docker exec resource_pool_mysql mysql -upool_user -ppool_password_2024 fault_knowledge_base \
  -e "SELECT COUNT(*) AS total, COUNT(DISTINCT content_hash) AS unique_hashes FROM fault_records;"
```

如数据库未初始化，先执行：

```bash
docker exec -i resource_pool_mysql mysql -uroot -proot_password_2024 \
  < /data/work/sql/create_fault_knowledge_base.sql
```

### 字段含义

| 字段 | 含义 | 查询用途 |
|------|------|----------|
| `module_name` | 模块 | 第一层收窄范围，优先从报错中的产品/组件/任务名推断 |
| `issue_type` | 问题类型 | 第二层收窄范围，优先从故障现象推断 |
| `issue_description` | 问题描述 | 核心相似度匹配字段 |
| `solution_summary` | 解决方法概要 | 给出历史解决路径 |
| `product_version` | 交付产品集版本 | 版本相关问题过滤 |
| `delivery_branch` | 交付分支 | 架构/OS/分支差异过滤 |
| `resource_pool` | 资源池 | 判断是否为特定现场案例 |

### 字段填写质量规范（单条入库必遵）

以 `id:1110` 为标杆：

- **`issue_description`**：保留完整报错原文（命令输出、stderr、Traceback、exit code），≥50 字，禁止仅写「部署失败」等空泛描述
- **`solution_summary`**：明确可操作修复动作（如「部署表字段 X：TRUE 改 FALSE」），≥10 字，禁止「待排查」「联系研发」
- **`delivery_mode`（交付形态）**：必填，填写现场交付类型，例如：`私有云` / `行业云` / `内部上云`
- **`resource_pool`（资源池）**：必填，填写具体资源池名称，例如：`北京九区` / `巴西CT云` / `呼和国产化`
- **`product_version`（交付产品集版本）**：必填，填写版本号，例如：`7.6.0` / `7.7.0` / `7.5.0`
- **`delivery_branch`（交付分支）**：必填，填写架构与 OS 组合，例如：`@X86@CUlinux` / `@ARM@CUlinux` / `@X86@CentOS`；多分支用逗号分隔，如 `@X86@CUlinux,@ARM@CUlinux`
- **`deployer`（部署人）**：必填，填写实际部署负责人姓名，例如：`田庆霖` / `姜金科`

## 核心流程

### Step 0 — 保存原始输入

**任何输入在处理前必须先存档**，防止后续分析覆盖原始数据：

```python
from pathlib import Path
from datetime import datetime
import shutil

RAW_DIR = Path.home() / '.hermes/skills/openclaw-imports/deploy-fault-analyzer/data/raw'
RAW_DIR.mkdir(parents=True, exist_ok=True)

# 文件输入 → 复制到 raw/
ts = datetime.now().strftime('%Y-%m-%d_%H%M%S')
raw_path = RAW_DIR / f'{ts}_{Path(src_file).name}'
shutil.copy2(src_file, raw_path)

# 文本输入 → 写入 raw/
raw_path = RAW_DIR / f'{ts}_user_input.txt'
raw_path.write_text(user_text, encoding='utf-8')
```

### Step 1 — 读取并解析输入

按文件格式选择解析策略：

**1A. 结构化 JSON 日志**（特征：顶层有 `logs` 数组，每项有 `type/message` 字段）
```python
import json
with open(filepath) as f:
    data = json.load(f)

logs = data['logs']  # 日志数组
# 提取字段：
#   log['type']     → 'error'|'warning'|'info'|'success'
#   log['message']  → 日志内容（含时间戳 `[HH:MM:SS]`）
#   log['timestamp']→ ISO 时间（JSON字段，可能缺失）
#   log['task_id']  → 任务ID（如 PREP_UPLOAD_33B3DC）

errors   = [l for l in logs if l['type'] == 'error']
warnings = [l for l in logs if l['type'] == 'warning']
infos    = [l for l in logs if l['type'] == 'info']
```

**1B. 纯文本 .log 文件**
```python
# 逐行读取，按关键词提取 ERROR/WARN/CRITICAL/FAIL 行
# 使用正则: ^\d{4}-\d{2}-\d{2}.*(ERROR|WARN|CRITICAL|FAIL)
```

**1C. 用户粘贴文本** → 直接作为分析输入

### Step 2 — 错误自动归类与去重

#### 2A. 中文错误模式自动归类

使用关键词正则匹配，按优先级从高到低匹配：

| 优先级 | 匹配模式（关键词） | 类别 |
|--------|-------------------|------|
| 1 | `日期格式不正确` `日期格式错误` `格式yyyy-mm-dd` | **数据异常** — 日期格式 |
| 2 | `资源池名称不正确` `名称不一致` `sheet.*≠` | **配置错误** — 资源池名 |
| 3 | `未填写` `必填项.*未` `必填.*缺失` | **配置错误** — 必填字段 |
| 4 | `缺失` `不存在` `not found` `No such file` | **资源不足** — 文件/目录 |
| 5 | `格式不正确.*IP` `IP地址格式` `格式不合法` | **配置错误** — IP格式 |
| 6 | `already installed` `is already` `冲突` `conflict` | **服务异常** — 安装冲突 |
| 7 | `已终止` `用户.*终止` `用户.*取消` | **用户操作** — 部署终止 |
| 8 | `Verifying` `verification` `校验失败` `验证失败` | **服务异常** — 验证超时 |
| 9 | `连接.*拒绝` `Connection refused` `timeout` `unreachable` | **网络/连接故障** |
| 10 | `host.*not found` `DNS.*fail` `解析失败` | **网络/连接故障** |
| 11 | `bms.*pri` `hostname.*invalid` | **配置错误** — 主机名 |
| 12 | `Permission denied` `权限不足` `访问被拒` | **权限问题** |
| 13 | `OOM` `out of memory` `磁盘空间不足` `No space` | **资源不足** — 系统资源 |
| 14 | `ModuleNotFoundError` `ImportError` `依赖.*缺失` | **依赖缺失** |

**实现：**
```python
def categorize_error_message(msg: str) -> str:
    """根据中文关键词自动归类错误"""
    patterns = [
        (r'日期格式不正确|日期格式错误|格式yyyy-mm-dd', '数据异常'),
        (r'资源池名称不正确|名称不一致', '配置错误'),
        (r'未填写|必填项.*未填|必填.*缺失', '配置错误'),
        (r'缺失|不存在|not found|No such file|no such file', '资源不足'),
        (r'格式不正确.*IP|IP地址格式|格式不合法', '配置错误'),
        (r'already installed|is already|冲突|conflict', '服务异常'),
        (r'已终止|用户.*终止|用户.*取消', '用户操作'),
        (r'Connection refused|timeout|unreachable|连接.*拒绝', '网络/连接故障'),
        (r'Permission denied|权限不足|访问被拒', '权限问题'),
        (r'OOM|out of memory|磁盘空间不足|No space', '资源不足'),
        (r'ModuleNotFoundError|ImportError|依赖.*缺失', '依赖缺失'),
    ]
    for pattern, category in patterns:
        if re.search(pattern, msg):
            return category
    return '待分类'
```

#### 2B. 错误去重归并（关键步骤）

真实日志中同根因错误通常大量重复。**必须先去重再分析**：

1. 过滤掉 **用户操作类**（`已终止`/`用户终止`）→ 不计入故障，仅在报告中标注
2. 按 **错误消息去重**：取 `message` 中 `ERROR` 关键字后的核心文本去重
3. 按 **task_id + 类别** 归并：同一任务同一类别的多条错误合并为一个根因
4. **输出**：每个根因一个 `fault_data` 字典

```python
def deduplicate_errors(errors: list) -> list:
    """归并重复错误 → 根因列表"""
    # 1. 分离用户操作
    real_faults = [e for e in errors if '用户已终止' not in e['message'] and '用户终止' not in e['message']]
    
    # 2. 按消息核心去重
    seen = {}
    for e in real_faults:
        msg = e['message']
        # 提取核心：ERROR 后的文本或消息中独特部分
        core = re.sub(r'\[.*?\]', '', msg).strip()[:100]
        cat = categorize_error_message(core)
        key = f"{cat}:{core[:50]}"
        if key not in seen:
            seen[key] = {'count': 1, 'sample': e, 'category': cat, 'task_ids': {e.get('task_id','?')}}
        else:
            seen[key]['count'] += 1
            seen[key]['task_ids'].add(e.get('task_id', '?'))
    
    return list(seen.values())
```

### Step 2.5 — 优先查询 MySQL 故障知识库（必须执行）

在进入根因分析前，必须先用去重后的核心错误到 `fault_knowledge_base.fault_records` 查询历史案例。查询目标是找到相同或相近的 `module_name`、`issue_type`、`issue_description`，并把命中的 `solution_summary` 作为解决方案候选，而不是直接凭经验生成结论。

#### 2.5A. 先推断 `module_name`

优先从日志里的产品名、任务名、服务名、报错路径、部署阶段推断模块；无法确定时再不带模块查询。

高频 `module_name` 候选（按历史库频次和故障定位价值排序）：

| 候选模块 | 常见关键词 |
|----------|------------|
| `基座` | bootstrap、基础包、yum、repo、平台基础服务、部署脚本公共步骤 |
| `主机交付问题` | 主机、host、IPMI、root密码、操作系统、lldp、网络不通 |
| `环境检查` | precheck、前置检查、端口检查、连通性检查、环境检查 |
| `块存储` | cinder、ceph、块存储、volume、存储池、磁盘 |
| `VPP` | vpp、dpdk、转发、网卡绑定、HugePage |
| `监控` | telegraf、prometheus、grafana、监控节点、采集 |
| `SDN` | sdn、neutron、网络控制、云内sdn、云间sdn |
| `门户` | portal、控制台、门户导入表、规格族 |
| `对象存储` | obs、s3、对象存储、bucket |
| `CSK` / `容器` / `云原生` | csk、k8s、kube、容器、master、worker |
| `Trove` | mysql、redis、trove、数据库服务 |
| `虚拟化` / `裸金属` | nova、ecs、bms、ironic、裸金属 |
| `DNS` | dns、域名、解析失败 |
| `ECR` | ecr、镜像仓库、registry |
| `网络交付问题` | 交换机、路由、vlan、外部网络、防火墙 |

#### 2.5B. 再推断 `issue_type`

`issue_type` 用于第二层收窄。优先候选：

| 候选类型 | 常见关键词 |
|----------|------------|
| `脚本问题` | script、脚本、执行失败、返回码、命令失败、already installed |
| `环境问题` | 网络不通、端口不通、系统版本、依赖环境、服务状态 |
| `新建部署问题` | 新建、首次部署、安装、部署失败 |
| `新建验收问题` | 验收、验证、verification、检查失败 |
| `部署包问题` | 包缺失、rpm、tar、镜像、目录不存在、版本包 |
| `部署表问题` | Excel、部署表、必填、格式、资源池名称、规格族 |
| `网络交付问题` | DNS、路由、交换机、连通性、防火墙、VLAN |
| `主机交付问题` | 主机名、IPMI、操作系统、root密码、lldp、网卡 |
| `部署文档问题` | 文档、步骤、章节、说明不一致 |
| `操作问题` | 人工操作、输入错误、误操作、顺序错误 |
| `扩容问题` / `扩容验收问题` | 扩容、增加节点、扩容后验收 |
| `优化建议` / `其他问题` | 无明确故障但存在改进项 |

#### 2.5C. 查询策略

按“强约束 → 放宽”的顺序查询，避免一开始全库模糊搜索导致误命中：

1. `module_name + issue_type + issue_description` 关键词查询
2. `module_name + issue_description` 查询
3. `issue_type + issue_description` 查询
4. 仅 `issue_description` 全文/LIKE 查询
5. 如果完全无命中，继续按原流程分析，并在报告中注明“历史故障库未找到高置信匹配”

推荐命令模板：

```bash
docker exec resource_pool_mysql mysql -upool_user -ppool_password_2024 fault_knowledge_base -e "
SELECT
  id, module_name, issue_type, found_at, product_version, delivery_branch,
  LEFT(issue_description, 220) AS issue_preview,
  LEFT(solution_summary, 220) AS solution_preview
FROM fault_records
WHERE module_name = '基座'
  AND issue_type = '脚本问题'
  AND (
    issue_description LIKE '%bootstrap%'
    OR solution_summary LIKE '%bootstrap%'
    OR MATCH(issue_description, solution_summary, remark) AGAINST('bootstrap 脚本 失败' IN NATURAL LANGUAGE MODE)
  )
ORDER BY
  (module_name = '基座') DESC,
  (issue_type = '脚本问题') DESC,
  updated_at DESC
LIMIT 5;"
```

如果无法稳定判断模块，使用关键词全库检索：

```bash
docker exec resource_pool_mysql mysql -upool_user -ppool_password_2024 fault_knowledge_base -e "
SELECT id, module_name, issue_type,
       LEFT(issue_description, 200) AS issue_preview,
       LEFT(solution_summary, 200) AS solution_preview
FROM fault_records
WHERE issue_description LIKE '%关键报错%'
   OR solution_summary LIKE '%关键报错%'
   OR remark LIKE '%关键报错%'
LIMIT 10;"
```

#### 2.5D. 命中结果使用规则

- 高置信命中：`module_name`、`issue_type`、核心报错关键词均匹配，解决方案可作为首选，但仍要结合当前日志证据验证。
- 中置信命中：模块或问题类型匹配，但错误文本只部分相似，只能作为排查方向。
- 低置信命中：仅关键词相似，不能直接引用为结论，只在“历史类似案例”中备注。
- 如果多个历史案例冲突，优先选择同模块、同问题类型、同版本/分支的记录。
- Word 报告中增加“历史故障库匹配”小节，列出命中记录的模块、问题类型、问题摘要、解决摘要和置信度。

#### 2.5E. 未命中时的处理

若 Step 2.5 无高置信命中（模块、问题类型、核心报错关键词均未对齐），**必须先进入 Step 2.6 脚本库检索**，不得直接凭经验给出最终结论。

### Step 2.6 — 脚本库相似检索（故障库未命中时执行）

告知用户：**「历史故障库未找到高置信匹配，开始分析脚本库 /data/scripts/」**，然后执行：

#### 2.6A. 脚本索引范围（更精准的检索入口）

脚本库根目录：`/data/scripts/`，当前已知脚本库与推荐索引范围如下（**优先在推荐范围内命中**）：

| 脚本库 | 推荐索引范围（优先级从高到低） | 适用模块/场景（示例关键词） |
|--------|------------------------------|----------------------------|
| `deploy-perfect-20250821/` | `second_deploy/dns/`、`second_deploy/ironic/`、`second_deploy/trove/`、`second_deploy/dcs/`、`second_deploy/ecml/`、`second_deploy/dims/`、`second_deploy/cloud_sdn/`、`sdn/`、`yum_repo/`、`perfect_deploy.sh`、`create_conf.py`、`globals.yml` | 基座新建/二次部署、DNS/ironic/trove、yum/repo、部署表生成（`dns`、`ironic`、`trove`、`bootstrap`、`yum`、`repo`、`portal`、`多套内部浮动网`） |
| `kubeos-ansible/` | `ansible/site.yml`、`ansible/pre_deploy.yml`、`ansible/*extend*.yml`、`ansible/roles/**/tasks/`、`ansible/roles/**/templates/`、`tools/` | 双引擎 OpenStack/组件部署扩容（`ansible`、`nova`、`neutron`、`rabbitmq`、`prometheus`、`worker_extend`、`precheck`） |
| `cephdeployscripts/` | `blockstorage/fabfile.py`、`blockstorage/create_cephfs_pool.py`、`common/common.py`、`resources/*.sh`、`config_samples/` | 块存储新建/扩容（`ceph-deploy`、`osd`、`cusmartcache`、`pool`、`cephfs`、`expand.json`、`config.json`） |

**检索文件类型**：`.sh` `.py` `.yml` `.yaml` `.ini` `.conf` `.cfg` `.j2` `.md`  
**排除范围**：`.git`、`node_modules`、`.idea`、`__pycache__` 等非业务内容。

#### 2.6B. 从故障问题提取“可检索关键词”（必须做）

为保证脚本检索精准度，`--query` 不能只用“部署失败/执行失败”这类泛词，必须从输入中抽取：

- **核心报错原文片段**：如 `No valid service subnet`、`KeyError`、`Connection refused`、`TarballDownloadException`、`iptables -t raw` 等
- **组件/命令/脚本痕迹**：如 `neutron`、`ceph-deploy`、`cusc_cli`、`ceph-volume`、`fabfile`、`expand.json`、`wipefs`、`sgdisk`
- **关键资源名/路径**（可截断）：如 `ceph-provisioners-0.1.0.tgz`、`/data/monitor-deploy/`、`/opt/ECR/`

推荐：把 `issue_description` 中的 **2～6 个关键词**拼成 query（中英文混合可用）。

```bash
python3 /data/work/scripts/search_deploy_scripts.py \
  --query "核心报错关键词" \
  --module "推断的模块名" \
  --top 5 --json
```

#### 2.6C. 用脚本内容参与根因分析（必须做）

脚本检索的目的不是“给出一堆路径”，而是让故障问题**根据脚本内容**得到验证或定位。对每个 Top 候选脚本，至少完成以下动作之一：

- **定位校验点**：脚本里是否存在与报错对应的检查/条件分支/变量（例如：部署表字段校验、网段/子网匹配、iptables 规则写入）
- **定位失败点**：脚本里是否有与日志一致的命令调用（如 `neutron floatingip-create`、`armada apply`、`python2 /usr/bin/db_populate.py`）以及 rc/异常处理方式
- **给出验证命令/验证方法**：从脚本推导用户可执行的验证步骤（例如：检查配置文件、检查 service subnet、检查 iptables raw 表规则）

向用户展示 Top 候选（库名、脚本路径、匹配行摘要），并询问：

> 以上脚本是否命中并解决了此次问题？（是 / 否）

- **用户回答「是」** → 询问是否需要将此次 Q&A 更新到故障库；若需要，进入 Step 8
- **用户回答「否」** → 继续 Step 3 起的常规根因分析与报告生成

`remark` 字段可记录命中的脚本路径，例如：`脚本库命中: cephdeployscripts/blockstorage/fabfile.py` 或 `cephdeployscripts/resources/check-cusmartcache.sh`

### Step 3 — 故障信息提取（多故障）

从去重后的错误列表，为每个根因提取结构化信息：

**提取方法：**

| 提取项 | JSON 日志提取方法 | 文本日志提取方法 |
|--------|------------------|-----------------|
| **故障时间** | `e['timestamp']`（ISO格式）或从 `message` 中提取 `[HH:MM:SS]` | 正则 `\d{4}-\d{2}-\d{2}.*\d{2}:\d{2}:\d{2}` |
| **错误类型** | `task_id` + 异常描述拼接，如 `CHECK_DEPLOY_F5B45D: checkTableImpl.DateFormatError` | 异常类名或错误码 |
| **错误消息** | `e['message']` 前200字符 | 紧跟在 ERROR 后的描述文本 |
| **出现次数** | `dedup_count` | 行数统计 |
| **堆栈跟踪** | 从 `message` 中的 `checkTableImpl.py:318` 等提取调用链 | Traceback 段落前20行 |
| **影响组件** | `task_id` 前缀 + `message` 中的模块路径（如 `/home/conf/`） | 服务名、主机名 |
| **影响范围** | 从部署流程推断（阻塞/警告/跳过） | 从错误推断 |
| **关联配置** | `message` 中的文件路径、参数名 | 配置文件引用 |

**任务ID解析**（JSON日志特有）：
```python
# task_id 前缀含义:
#   PREP_UPLOAD_* → 上传检查步骤
#   PREP_TASK_*   → 前置任务
#   CHECK_DEPLOY_* → 部署表检查
#   PREP_DEPLOY_*  → 部署准备

def parse_task_id(task_id: str) -> dict:
    """解析 task_id → 任务类型和阶段"""
    if task_id is None:
        return {'phase': '全局', 'type': '系统'}
    parts = task_id.split('_')
    if len(parts) >= 2:
        return {'phase': parts[0], 'type': parts[1], 'id': parts[-1] if len(parts) > 2 else ''}
    return {'phase': task_id, 'type': 'UNKNOWN'}
```

### Step 4 — 根因分析

基于提取的信息，执行以下分析步骤：

1. **错误分类**：归入以下类别之一
   - 🟥 网络/连接故障（ConnectionError, timeout, unreachable）
   - 🟧 配置错误（config file, parameter, permission）
   - 🟨 资源不足（OOM, disk full, CPU throttle, fd limit）
   - 🟩 服务异常（service down, crash, restart loop）
   - 🟦 权限问题（permission denied, unauthorized）
   - 🟪 依赖缺失（module not found, library mismatch）
   - ⬜ 数据异常（data corrupt, schema mismatch）

2. **历史案例对齐**：把 Step 2.5 命中的故障库记录与当前日志证据逐项对比，确认模块、问题类型、关键词、版本/分支是否一致

3. **因果关系链**：从堆栈自底向上追溯，找到最初触发点

4. **关键证据**：摘录日志中能佐证根因的2-3条关键行

### Step 5 — 生成解决方案

优先采用高置信历史案例中的 `solution_summary`，再结合当前日志、环境和标准排查路径细化；没有命中时才完全按通用框架生成方案。

| 错误类别 | 标准排查路径 | 典型解决步骤 |
|----------|-------------|-------------|
| 网络/连接 | telnet/ping/curl 测试连通性 → 防火墙规则 → DNS解析 | 检查目的端口可达性、放行防火墙规则、修正IP配置 |
| 配置错误 | 对比配置模板 → 校验参数值 | 修正配置文件、重启服务、验证参数生效 |
| 资源不足 | free/df -h/ulimit -n 检查 → top 定位占用进程 | 清理磁盘、扩容、调大 ulimit、重启服务释放泄漏 |
| 服务异常 | systemctl status → journalctl 查崩溃原因 | 重启服务、检查依赖服务状态、排查 OOM killer |
| 权限问题 | ls -l / id / 检查 sudo | 修正文件权限(chmod/chown)、添加 sudo 授权 |
| 依赖缺失 | rpm -qa / pip list → 对比版本要求 | 安装缺失包、版本降级/升级 |
| 数据异常 | 检查数据完整性 → 对比 schema | 数据修复、迁移、回滚 |

**输出解决方案时遵循的结构：**
```
【解决方案】
1. 排查步骤
   - 第一步：xxx
   - 第二步：xxx
2. 修复操作
   - 操作命令（可复制执行）
3. 验证方法
   - 验证命令 + 预期结果
4. 回滚方案（如适用）
```

### Step 6 — 生成交付物

#### 6.1 判断生成模式

```python
if len(root_causes) == 1:
    mode = 'single'   # 单故障 → 标准五段式报告
else:
    mode = 'multi'    # 多故障 → 总览 + 逐项分析 + 综合建议
```

#### 6.2 Word 文档（单故障模式）

生成 `部署故障分析及解决方案_YYYY-MM-DD_HHmmss.docx`，标准五段式结构（同原版）。

#### 6.3 Word 文档（多故障模式）

当 `mode == 'multi'` 时，增加总览页和综合建议：

```
封面
├── 总体概况表
│   ├── 文档编号 / 分析时间 / 部署目标 / 部署计划
│   ├── 总日志数 / 总错误数 / 归并根因数
│   └── 最高故障级别
├── 错误全景图（表格）
│   ├── # / 故障 / 类别 / 级别 / 出现次数
├── 逐项详细分析
│   ├── 故障 1：...（完整五段式）
│   ├── 故障 2：...
│   └── ...
└── 综合建议与整改清单
    └── 按优先级排列的改进项
```

**重点**：每个故障页有明确的 `故障 N / 总N` 标注，分隔线分隔。

#### 6.4 使用 generate_report.py 脚本

```python
from scripts.generate_report import generate_fault_report, generate_multi_fault_report, append_to_excel

# 单故障
if len(faults) == 1:
    docx_path = generate_fault_report(output_path, faults[0])

# 多故障
else:
    docx_path = generate_multi_fault_report(output_path, faults)

# 批量追加 Excel（所有故障都写一行）
for fault in faults:
    append_to_excel(xlsx_path, {...})
```

**文档保存路径**: `~/.hermes/skills/openclaw-imports/deploy-fault-analyzer/output/`

### Step 7 — 发送交付物（必须执行）

**⚠️ 分析完成后必须在同一条回复中做两件事：**

1. **贴出故障分析摘要**（故障全景表 + 核心结论），让用户无需打开文件即可了解全貌
2. **发送 Word 文件** — 使用 `message` 工具发送文件给用户

```python
# 发送 .docx 文件给用户（以当前会话的 chat 通道发送）
# 使用 message 工具: action=send, filePath=docx_path, caption='部署故障分析报告'
```

**发送规则：**
- 回复消息中贴摘要表（纯文本，不依赖 markdown 表格渲染）
- 同时调用 `message` 工具发送 Word 文件
- 发送后回复 `NO_REPLY` 避免重复消息

**摘要模板（回复消息中贴出）：**
```
🔍 部署故障分析结果

概览：N条日志，M条错误 → 归并 K 个根因

| # | 故障 | 类别 | 级别 | 次数 | 定位 |
F1 | xxx | 数据异常 | P1 | 44 | xxx
F2 | ...

🎯 核心结论：xxx

📄 Word 报告已同步发送，请查收。
```

### Step 8 — 单条更新故障库（交互式）

适用场景：
1. Step 2.6 中用户确认脚本已解决问题，且同意更新故障库
2. 用户主动说「录入这条故障」「更新故障库」「把这次问题加到故障库」

**注意**：本流程**仅写入 MySQL** `fault_records`，不修改 Excel。

#### 8.1 Agent 起草记录

根据会话上下文整理 JSON 草稿，字段规则：

| 字段 | 必填 | 规则 |
|------|------|------|
| `module_name` | 是 | 复用 Step 2.5A 推断 |
| `issue_type` | 建议 | 复用 Step 2.5B 推断 |
| `issue_description` | 是 | 完整报错原文，参照 id:1110 |
| `solution_summary` | 是 | 明确修复动作，参照 id:1110 |
| `found_at` | 建议 | 默认今天 `YYYY-MM-DD` |
| `delivery_mode` | 是 | 交付形态，如 `私有云` / `行业云` / `内部上云` |
| `resource_pool` | 是 | 资源池名称，如 `北京九区` |
| `product_version` | 是 | 交付产品集版本，如 `7.6.0` |
| `delivery_branch` | 是 | 交付分支，如 `@X86@CUlinux` / `@ARM@CUlinux` / `@X86@CentOS` |
| `deployer` | 是 | 部署人姓名 |
| `word_file` | 否 | 默认 `不涉及` |
| `remark` | 否 | 可写关联脚本路径 |

草稿 JSON 示例：

```json
{
  "module_name": "DNS",
  "issue_type": "新建部署问题",
  "found_at": "2026-06-08",
  "issue_description": "+ neutron floatingip-create ...\nfloatingip 创建失败,请检查\n+ exit 1",
  "solution_summary": "部署表「内网dns云主机是否通过外部网络访问外网」TRUE 改 FALSE",
  "delivery_mode": "私有云",
  "resource_pool": "巴西CT云",
  "product_version": "7.6.0",
  "delivery_branch": "@X86@CUlinux",
  "deployer": "田庆霖",
  "word_file": "不涉及",
  "remark": "脚本库命中: deploy-perfect-20250821/second_deploy/dns/dns_deploy/dns.sh"
}
```

将草稿保存到 skill 目录，例如：`output/fault_draft_YYYY-MM-DD_HHmmss.json`

#### 8.2 展示草稿并等待用户确认

向用户展示完整草稿（模板如下），询问：

```
📋 故障库入库草稿（请确认或补充）

模块：DNS
问题类型：新建部署问题
问题描述：
  <完整报错原文...>
解决方法概要：
  部署表「内网dns云主机是否通过外部网络访问外网」TRUE 改 FALSE
交付形态：私有云
资源池：巴西CT云 | 版本：7.6.0 | 分支：@X86@CUlinux | 部署人：田庆霖

请回复：确认同步 / 需要修改：<说明> / 取消
```

> 请确认或补充：回复「确认同步」/「需要修改：…」/「取消」

#### 8.3 校验与入库

用户确认后执行：

```bash
# 1. 校验（不写入）
python3 /data/work/scripts/insert_fault_record.py \
  --json output/fault_draft_YYYY-MM-DD_HHmmss.json --dry-run

# 2. 正式写入（追加到最后，id = MAX(id)+1）
python3 /data/work/scripts/insert_fault_record.py \
  --json output/fault_draft_YYYY-MM-DD_HHmmss.json \
  --port 33307

# 3. 验证
docker exec resource_pool_mysql mysql -upool_user -ppool_password_2024 fault_knowledge_base \
  -e "SELECT id, module_name, issue_type, LEFT(issue_description,80), LEFT(solution_summary,80) FROM fault_records ORDER BY id DESC LIMIT 1;"
```

校验失败时根据脚本输出修正草稿，重新展示给用户确认，不得使用 `--force` 跳过校验。

---

## Python 脚本模板

### docx 生成脚本

```python
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import os

def generate_fault_report(output_path, fault_data):
    """
    fault_data = {
        'fault_time': '2026-05-09 10:23:45',
        'error_type': 'ConnectionError',
        'error_message': '...',
        'stack_trace': '...',
        'affected_component': 'nova-api',
        'affected_scope': 'AZ-1 计算节点',
        'related_config': '/etc/nova/nova.conf',
        'error_category': '网络/连接故障',
        'fault_level': 'P1',
        'root_cause': '...',
        'evidence_lines': ['...', '...'],
        'solution_steps': [...],
        'verification': '...',
        'prevention': '...',
    }
    """
    doc = Document()
    
    # 标题
    title = doc.add_heading('部署故障分析及解决方案', level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 文档信息表
    doc.add_paragraph('')
    info_table = doc.add_table(rows=3, cols=2, style='Light Grid Accent 1')
    info_data = [
        ('文档编号', f"DOC-{datetime.now().strftime('%Y%m%d')}-{fault_data.get('fault_level','P2')}"),
        ('分析时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ('故障级别', fault_data.get('fault_level', 'P2')),
    ]
    for i, (k, v) in enumerate(info_data):
        info_table.rows[i].cells[0].text = k
        info_table.rows[i].cells[1].text = v
    
    doc.add_paragraph('')
    
    # 一、故障概述
    doc.add_heading('一、故障概述', level=1)
    doc.add_paragraph(f"故障时间：{fault_data.get('fault_time', '未知')}")
    doc.add_paragraph(f"影响组件：{fault_data.get('affected_component', '未知')}")
    doc.add_paragraph(f"影响范围：{fault_data.get('affected_scope', '未知')}")
    doc.add_paragraph(f"错误类型：{fault_data.get('error_type', '未知')}")
    
    # 二、故障详情
    doc.add_heading('二、故障详情', level=1)
    doc.add_heading('错误消息', level=2)
    doc.add_paragraph(fault_data.get('error_message', ''))
    
    if fault_data.get('stack_trace'):
        doc.add_heading('堆栈跟踪', level=2)
        p = doc.add_paragraph()
        p.style = doc.styles['No Spacing']
        for line in fault_data['stack_trace'].split('\n')[:20]:
            doc.add_paragraph(line, style='No Spacing')
    
    if fault_data.get('related_config'):
        doc.add_paragraph(f"关联配置：{fault_data['related_config']}")
    
    # 三、根因分析
    doc.add_heading('三、根因分析', level=1)
    doc.add_paragraph(f"错误分类：{fault_data.get('error_category', '未分类')}")
    doc.add_paragraph(f"根本原因：{fault_data.get('root_cause', '待进一步分析')}")
    
    if fault_data.get('evidence_lines'):
        doc.add_heading('关键证据', level=2)
        for i, line in enumerate(fault_data['evidence_lines'], 1):
            doc.add_paragraph(f"{i}. {line}")
    
    # 四、解决方案
    doc.add_heading('四、解决方案', level=1)
    for step in fault_data.get('solution_steps', []):
        doc.add_paragraph(step, style='List Bullet')
    
    if fault_data.get('verification'):
        doc.add_heading('验证方法', level=2)
        doc.add_paragraph(fault_data['verification'])
    
    # 五、预防措施
    doc.add_heading('五、预防措施', level=1)
    doc.add_paragraph(fault_data.get('prevention', '—'))
    
    doc.save(output_path)
    return output_path
```

---

## 边界情况与注意事项

### 当输入过于模糊时
如果日志/文本中找不到明确的错误信息，不要强行编造分析结果。此时：
- 输出一份简要的"日志初步筛查报告" Word 文档
- 在文档中标注"待补充信息"
- Excel 中错误类别记为"待分类"

### 当单个输入包含多个错误时（重要）

**流程：**
1. Step 2A 自动归类 → 按关键词将错误分入不同类别
2. Step 2B 错误去重 → 归并重复错误，统计每个根因出现次数
3. 过滤"用户操作"类（`已终止`/`用户终止`）→ 不计入故障清单
4. 对每个根因执行 Step 2.5，按 `module_name`、`issue_type`、`issue_description` 查询 MySQL 故障知识库
5. 按**故障级别**（P1→P2→P3）和历史命中置信度排序输出
6. Word 文档使用**多故障模式** → 生成总览表 + 逐项分析 + 历史故障库匹配
7. Excel 中每个根因占一行，必要时同步到 MySQL 故障库

### 真实案例参考

以下是从实际部署日志中提取的典型错误模式，用于指导分类：

**模式 1 — 部署表日期格式错误（44条 → 1个根因）**
```
[CHECK_DEPLOY_F5B45D] 导入表：日期格式不正确45677.7661111, 格式yyyy-mm-dd hh:mm:ss
→ 类别：数据异常 | 根因：Excel日期序列号未转换 | 级别：P1
```

**模式 2 — 资源池名称不一致（35条 → 1个根因）**
```
[CHECK_DEPLOY_F5B45D] 资源池名称不正确 sheet11:呼和交付验证云池; sheet1:呼和国产化...
→ 类别：配置错误 | 根因：多sheet资源池名未统一 | 级别：P1
```

**模式 3 — 部署包目录缺失（6条 → 1个根因）**
```
[PREP_UPLOAD_33B3DC] /opt/ImageManager: 缺失
→ 类别：资源不足 | 根因：部署包未上传或不在此次部署范围 | 级别：P1
```

**模式 4 — RPM 安装误报（1条 → 不阻塞）**
```
[PREP_TASK_53658B] rpm -ivh → already installed → exit code ≠ 0
→ 类别：服务异常 | 根因：安装脚本未处理"已安装"状态 | 级别：P3
```

### 用户操作类不计入故障

以下消息类型**不归类为故障**，仅在报告中备注：
- `用户已终止部署流程` → 用户主动操作
- `部署已自动暂停，等待用户确认` → 流程机制，非故障本身
- `用户确认继续` → 流程恢复

### 路径规范
所有输出统一在 skill 目录下：
```
~/.hermes/skills/openclaw-imports/deploy-fault-analyzer/
├── SKILL.md
├── output/          # Word 文档输出
├── data/
│   ├── problems.xlsx   # Excel 知识库
│   └── raw/             # 原始输入存档
```

MySQL 故障知识库不在 skill 目录下，固定查询 `fault_knowledge_base.fault_records`。
相关脚本均在 `/data/work/scripts/`：`sync_fault_knowledge_base.py`（Excel 批量同步）、`insert_fault_record.py`（单条入库）、`search_deploy_scripts.py`（脚本库检索）。

---

## 快速参考

| 用户说什么 | 你做什么 |
|-----------|---------|
| 上传 xxxx.log | 读取 → 提取ERROR行 → 推断 `module_name`/`issue_type` → 查询 MySQL 故障库 → 分析 → 生成 docx + 写入 xlsx → **发送 docx 给用户 + 贴摘要** |
| 粘贴报错文本 | 同日志流程，必须先查 `fault_knowledge_base.fault_records` 再给结论 |
| "帮我看下这个报错" | 识别附带文本 → 查 MySQL 历史案例 → 分析 → 生成 docx + 写入 xlsx → **发送 docx 给用户 + 贴摘要** |
| "查一下之前类似问题" | 优先查询 `fault_knowledge_base.fault_records`，按模块、问题类型、问题描述返回历史案例 |
| "这个错之前遇到过吗" | 在 MySQL 故障库中搜索匹配的 `issue_description` 和 `solution_summary` |
| 故障库未命中 | 告知用户 → `search_deploy_scripts.py` 检索 `/data/scripts/` → 询问是否解决 → 可选进入 Step 8 |
| "同步故障库" / "把 Excel 故障库入库" | `sync_fault_knowledge_base.py --dry-run` → 确认后正式同步 |
| "更新故障库" / "录入这条故障" / "把这次问题加到故障库" | Step 8：起草 JSON → 用户确认 → `insert_fault_record.py --dry-run` → 正式写入 |
