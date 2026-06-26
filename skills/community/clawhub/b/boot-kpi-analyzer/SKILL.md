# Boot KPI Analyzer Skill

## 功能描述
分析 SS4 车机的开机 KPI 和关机 KPI 时序数据，帮助定位启动慢、关机慢等性能问题。

## 数据路径

### 开机 KPI（Boot KPI）
```
/home/lixiang/work/sdata/code/smk-1125/boot_kpi_server/backend/uploads/<YYYYMMDD_HHMMSS>/
```
每个子目录包含：
- `boot_kpi_summary.txt` — 预分析的中文摘要报告（3部分：系统服务启动分析、qcrosvm依赖分析、qcrosvm启动性能）
- `boot_kpi.log` — 原始事件：`<service> -> <state> at <ms>ms from system boot`
- `unit_kpi.log` — modemanager 日志：`[UnitKPI] Dependency of qcrosvm.service ... -> <state> at <ms>ms`

### 关机 KPI（Shutdown KPI）
```
/home/lixiang/work/sdata/code/smk-1125/boot_kpi_server/backend/reboot_tests/<YYYYMMDD_HHMMSS>/
```
每个子目录包含：
- `report.json` — 测试报告，包含 reboot_duration（整个重启周期秒数）、test_result、build_id 等
- `shutdown-monitor-units.log` — BPF 跟踪的关机事件日志

### Web 查询接口（私有 IP，须用 curl）
```
http://10.122.86.46:9999/
```
⚠️ web_fetch 无法访问私有 IP，必须使用 `execute_command` 运行 `curl` 命令。

## 使用方法

### 列出可用的开机 KPI 数据
```bash
ls /home/lixiang/work/sdata/code/smk-1125/boot_kpi_server/backend/uploads/
```

### 列出可用的关机 KPI 数据
```bash
ls /home/lixiang/work/sdata/code/smk-1125/boot_kpi_server/backend/reboot_tests/
```

### 分析脚本
使用 `skills/boot-kpi-analyzer/scripts/analyze.py` 进行自动化分析：

```bash
# 分析最新的开机 KPI
python3 /home/lixiang/.openclaw/skills/boot-kpi-analyzer/scripts/analyze.py boot --latest

# 分析指定目录的开机 KPI
python3 /home/lixiang/.openclaw/skills/boot-kpi-analyzer/scripts/analyze.py boot --dir <YYYYMMDD_HHMMSS>

# 分析最新的关机 KPI
python3 /home/lixiang/.openclaw/skills/boot-kpi-analyzer/scripts/analyze.py shutdown --latest

# 分析指定目录的关机 KPI
python3 /home/lixiang/.openclaw/skills/boot-kpi-analyzer/scripts/analyze.py shutdown --dir <YYYYMMDD_HHMMSS>

# 列出所有可用数据
python3 /home/lixiang/.openclaw/skills/boot-kpi-analyzer/scripts/analyze.py list
```

### curl 查询 Web 接口示例
```bash
curl -s http://10.122.86.46:9999/
curl -s http://10.122.86.46:9999/api/sessions
curl -s http://10.122.86.46:9999/api/latest
```

## 数据格式说明

### boot_kpi.log 格式
```
<service_name> -> <state> at <ms>ms from system boot
```
关键状态：`activating`、`active`、`deactivating`、`inactive`、`failed`

### shutdown-monitor-units.log 格式
```
[YYYY-MM-DD HH:MM:SS.mmm] Unit: <service> | State: <FROM> -> <TO> | BPF_timestamp: <ns>
```
- BPF_timestamp 单位：纳秒
- 关键里程碑：
  - `shutdown.target | State: INACTIVE -> ACTIVE` — 关机流程开始
  - `umount.target | State: INACTIVE -> ACTIVE` — 关机晚期阶段
  - `qcrosvm.service | State: ACTIVE -> DEACTIVATING` — Android VM 开始关闭

### report.json 关键字段
- `reboot_duration`: 整个重启周期（秒），含关机+开机
- `test_result`: `success` / `failure`
- `build_id`: 固件版本
- `has_lastlog`: 是否有 lastlog（异常重启标志）
- `error_message`: 失败原因

## 分析要点

### 开机性能关键指标
- **qcrosvm.service 激活耗时**：Android VM 启动时间，最重要的 KPI
- **慢服务（>100ms）**：影响开机速度的服务
- **频繁重启的服务**：可能有依赖问题
- **失败服务**：需要重点关注

### 关机性能关键指标
- **总关机时长**：从 shutdown.target 激活到系统关机
- **qcrosvm.service 关机耗时**：Android VM 关闭时间
- **reboot_duration**：完整重启周期（越小越好，目标通常 < 40s）
- **umount.target 之前的耗时**：文件系统卸载前的服务关闭阶段

## 典型分析流程

1. **列出数据** → 找到最新或指定时间段的数据目录
2. **读取 report.json** → 快速了解总体情况（reboot_duration、是否成功）
3. **分析关机日志** → 找出关机慢的服务（计算各服务从 DEACTIVATING 到 INACTIVE 的耗时）
4. **读取 boot_kpi_summary.txt** → 获取开机分析摘要
5. **深挖 boot_kpi.log** → 针对具体服务进行详细分析
6. **对比多次数据** → 找出性能波动规律
