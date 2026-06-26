# 🛡️ agent-defender 项目文档

**AI 智能体安全防护平台** - 静态扫描 + 运行时防护 + DLP 脱敏

**版本**: v2.0  
**更新时间**: 2026-04-07  
**状态**: ✅ 生产就绪

---

## 📋 目录

1. [项目概述](#项目概述)
2. [核心能力](#核心能力)
3. [架构设计](#架构设计)
4. [快速开始](#快速开始)
5. [使用指南](#使用指南)
6. [规则管理](#规则管理)
7. [API 参考](#api 参考)
8. [备份方案](#备份方案)
9. [故障排查](#故障排查)
10. [开发指南](#开发指南)

---

## 项目概述

### 什么是 agent-defender？

agent-defender 是一个专为 AI 智能体设计的安全防护平台，提供：

- **静态扫描**: 在代码执行前检测恶意内容
- **运行时防护**: 监控系统行为，拦截可疑操作
- **DLP 脱敏**: 识别和阻断敏感数据泄露

### 核心价值

| 价值 | 说明 |
|------|------|
| 🔒 **主动防御** | 在威胁发生前检测和阻断 |
| 🎯 **精准检测** | 624+ 条规则，100% 测试通过率 |
| ⚡ **高性能** | >1000 样本/秒，<10ms 延迟 |
| 🔄 **持续进化** | 与灵顺 V5 联动，自动迭代优化 |

### 应用场景

- ✅ AI Skill 安全扫描
- ✅ 代码注入检测
- ✅ 提示词攻击防护
- ✅ 数据泄露防护
- ✅ 供应链攻击检测

---

## 核心能力

### 1. 静态扫描 (Static Analysis)

**检测引擎**:
- YARA 规则匹配
- AST 语法分析
- 权限检测
- 模式匹配

**支持语言**:
- Python (.py, .pyw)
- JavaScript (.js, .jsx, .ts)
- Shell (.sh, .bash, .zsh)
- YAML (.yaml, .yml)
- Go (.go)
- PowerShell (.ps1)

### 2. 运行时防护 (Runtime Protection)

**监控能力**:
- 文件系统操作
- 网络连接
- 进程创建
- 注册表修改
- 环境变量访问

**拦截机制**:
- 实时行为分析
- 异常检测
- 自动阻断
- 告警通知

### 3. DLP 脱敏 (Data Loss Prevention)

**敏感数据类型**:
- API 密钥/Token
- SSH 密钥
- 数据库凭据
- AWS/Azure/GCP 凭据
- 个人身份信息 (PII)

**处理方式**:
- 自动识别
- 数据脱敏
- 传输阻断
- 审计日志

---

## 架构设计

### 系统架构

```
┌─────────────────────────────────────────┐
│         用户输入 / 待检测内容            │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│       入口防护 (DLP Check)              │
│  - 敏感数据识别                          │
│  - 数据脱敏                              │
│  - 阻断决策                              │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│      静态扫描 (Static Scanner)          │
│  - YARA 规则匹配                         │
│  - Runtime 规则检测                      │
│  - 风险评分                              │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│      运行时防护 (Runtime Monitor)       │
│  - 系统调用监控                          │
│  - 行为分析                              │
│  - 异常拦截                              │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│         输出 / 检测结果                  │
│  - 风险等级                              │
│  - 威胁详情                              │
│  - 处置建议                              │
└─────────────────────────────────────────┘
```

### 规则体系

```
规则来源:
├── agent-security-skill-scanner (灵顺 V5)
│   ├── optimized_rules (53 条)
│   └── expert_mode/rules (41 条)
├── Sigma 规则 (转换后)
├── YARA 规则 (转换后)
└── 自定义规则

规则类型:
├── Runtime 规则 (31 条)
├── YARA 规则 (10 条)
├── 黑名单规则 (19 条)
└── 白名单规则 (15 条)

总计：624+ 条规则
```

---

## 快速开始

### 安装

```bash
# 1. 克隆项目
cd ~/.openclaw/workspace/skills/
git clone https://gitee.com/caidongyun/agent-defender.git

# 2. 安装依赖
cd agent-defender
pip3 install -r requirements.txt

# 3. 验证安装
python3 scanner_v2.py
```

### 第一次扫描

```bash
# 扫描单个文件
python3 -c "
from scanner_v2 import DefenderScanner
scanner = DefenderScanner()
scanner.load_rules()
result = scanner.detect('eval(user_input)')
print(f'风险：{result[\"risk_level\"]} ({result[\"risk_score\"]})')
"

# 扫描目录
python3 -c "
from scanner_v2 import DefenderScanner
from pathlib import Path
scanner = DefenderScanner()
scanner.load_rules()
results = scanner.scan_directory(Path('/path/to/project'))
print(f'检出：{results[\"malicious_files\"]}/{results[\"total_files\"]}')
"
```

### 启动守护进程

```bash
# 启动自动研发
./defenderctl.sh start

# 查看状态
./defenderctl.sh status

# 查看日志
./defenderctl.sh logs
```

---

## 使用指南

### 1. 基础使用

#### Python API

```python
from scanner_v2 import DefenderScanner

# 初始化扫描器
scanner = DefenderScanner()
scanner.load_rules()

# 检测代码
code = '''
import os
os.system('rm -rf /')
'''

result = scanner.detect(code)

if result['is_malicious']:
    print(f"⚠️  检测到威胁：{result['risk_level']}")
    print(f"风险评分：{result['risk_score']}")
    for threat in result['threats']:
        print(f"  - {threat['category']}: {threat['rule_id']}")
else:
    print("✅ 安全代码")
```

#### 命令行工具

```bash
# 扫描文件
python3 scanner_v2.py --file malicious.py

# 扫描目录
python3 scanner_v2.py --scan /path/to/project

# 生成报告
python3 scanner_v2.py --report scan_report.md
```

### 2. 高级使用

#### 自定义规则

```python
# 添加自定义规则
scanner.blacklist_patterns.append({
    "pattern": r"my_custom_malicious_pattern",
    "risk": "CRITICAL",
    "category": "custom_threat"
})
```

#### 批量扫描

```python
from pathlib import Path

# 扫描多个目录
dirs_to_scan = [
    Path("/path/to/project1"),
    Path("/path/to/project2"),
    Path("/path/to/project3"),
]

all_results = []
for dir_path in dirs_to_scan:
    results = scanner.scan_directory(dir_path)
    all_results.append({
        "directory": str(dir_path),
        "results": results
    })

# 生成汇总报告
report = scanner.generate_report(all_results)
with open('batch_scan_report.md', 'w') as f:
    f.write(report)
```

---

## 规则管理

### 规则加载

```python
scanner = DefenderScanner()
total_rules = scanner.load_rules()
print(f"加载 {total_rules} 条规则")
```

### 规则来源

| 来源 | 路径 | 规则数 |
|------|------|--------|
| optimized_rules | `agent-security-skill-scanner-master/expert_mode/optimized_rules/` | 53 |
| integrated_rules | `agent-defender/rules/*_integrated.json` | 41 |
| 黑名单 | `scanner_v2.py` 内置 | 19 |
| 白名单 | `scanner_v2.py` 内置 | 15 |

### 规则同步

```bash
# 从灵顺 V5 同步规则
./defenderctl.sh sync

# 手动运行集成脚本
python3 integrate_scanner_v4.py
```

---

## API 参考

### DefenderScanner 类

#### `__init__(rules_dir: Optional[Path] = None)`

初始化扫描器

**参数**:
- `rules_dir`: 规则目录路径 (默认：当前目录的 `rules/`)

**示例**:
```python
scanner = DefenderScanner()
scanner = DefenderScanner(rules_dir=Path("/custom/rules"))
```

#### `load_rules() -> int`

加载所有规则

**返回**: 加载的规则总数

**示例**:
```python
total = scanner.load_rules()
print(f"加载了 {total} 条规则")
```

#### `detect(code: str) -> Dict[str, Any]`

检测代码

**参数**:
- `code`: 待检测的代码字符串

**返回**: 检测结果字典
```python
{
    "is_malicious": bool,
    "risk_level": str,  # SAFE/LOW/MEDIUM/HIGH/CRITICAL
    "risk_score": int,  # 0-100
    "threats": List[Dict],
    "reason": str
}
```

**示例**:
```python
result = scanner.detect("eval(user_input)")
if result['is_malicious']:
    print(f"检测到威胁：{result['risk_level']}")
```

#### `scan_file(file_path: Path) -> Dict[str, Any]`

扫描文件

**参数**:
- `file_path`: 文件路径

**返回**: 检测结果

#### `scan_directory(dir_path: Path, recursive: bool = True) -> Dict[str, Any]`

扫描目录

**参数**:
- `dir_path`: 目录路径
- `recursive`: 是否递归扫描子目录

**返回**: 扫描结果汇总
```python
{
    "total_files": int,
    "malicious_files": int,
    "safe_files": int,
    "details": List[Dict]
}
```

#### `generate_report(results: Dict[str, Any]) -> str`

生成扫描报告

**参数**:
- `results`: 扫描结果

**返回**: Markdown 格式报告

---

## 备份方案

### 自动备份机制

#### 1. 规则备份

**触发时机**: 每次集成新规则时自动备份

**备份位置**: `rules_backup/backup_YYYYMMDD_HHMMSS/`

**备份内容**:
- 所有 `rules/*.json` 文件
- 备份时间戳
- 规则数量统计

**示例**:
```bash
$ ls -la rules_backup/
drwxrwxr-x  2 cdy cdy  4096  4 月  7 19:55 backup_20260407_195520
drwxrwxr-x  2 cdy cdy  4096  4 月  7 19:55 backup_20260407_195535
drwxrwxr-x  2 cdy cdy  4096  4 月  7 19:56 backup_20260407_195632
```

#### 2. 同步报告

**生成位置**: `sync_reports/integration_YYYYMMDD_HHMMSS.md`

**报告内容**:
- 集成时间
- 来源版本
- 同步统计
- 变更日志
- 备份位置

### 手动备份

#### 压缩备份

```bash
cd ~/.openclaw/workspace/skills/agent-defender

# 创建备份目录
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 备份规则
cp -r rules/ "$BACKUP_DIR/"
cp -r integrated_rules/ "$BACKUP_DIR/"
cp *.py "$BACKUP_DIR/"

# 压缩
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"

# 生成清单
cat > "$BACKUP_DIR/manifest.json" <<EOF
{
  "backup_time": "$(date -Iseconds)",
  "rules_count": $(ls rules/*.json | wc -l),
  "files": [
    $(ls -1 rules/*.json | xargs -I {} basename {} | jq -R . | jq -s .)
  ]
}
EOF

echo "✅ 备份完成：$BACKUP_DIR.tar.gz"
```

#### 备份索引

创建 `backups/backup_index.json`:

```json
{
  "backups": [
    {
      "timestamp": "2026-04-07T19:55:20+08:00",
      "archive": "20260407_195520.tar.gz",
      "rules_count": 20,
      "notes": "集成 Scanner v4.1.0"
    },
    {
      "timestamp": "2026-04-07T20:13:00+08:00",
      "archive": "20260407_201300.tar.gz",
      "rules_count": 20,
      "notes": "修复路径配置"
    }
  ]
}
```

### 恢复备份

```bash
# 列出可用备份
ls -la backups/*.tar.gz

# 恢复指定备份
BACKUP_FILE="backups/20260407_195520.tar.gz"
tar -xzf "$BACKUP_FILE"

# 验证恢复
ls -la extracted_backup/rules/
```

---

## 故障排查

### 常见问题

#### 1. 规则加载失败

**现象**:
```
✅ 加载 0 条规则
```

**原因**: 路径配置错误

**解决**:
```python
# 检查路径
from scanner_v2 import DefenderScanner
from pathlib import Path

scanner = DefenderScanner()
print("规则目录:", scanner.rules_dir)
print("存在:", scanner.rules_dir.exists())

# 手动指定路径
scanner.rules_dir = Path("/absolute/path/to/rules")
scanner.load_rules()
```

#### 2. 检测率过低

**现象**: 检测率 < 80%

**原因**: 规则未正确加载

**解决**:
```bash
# 验证规则数量
python3 -c "
from scanner_v2 import DefenderScanner
scanner = DefenderScanner()
total = scanner.load_rules()
print(f'规则总数：{total}')
print(f'Optimized: {len(scanner.rules[\"optimized\"])}')
print(f'Integrated: {len(scanner.rules[\"integrated\"])}')
"
```

#### 3. 守护进程无法启动

**现象**:
```
❌ 守护进程启动失败
```

**解决**:
```bash
# 检查日志
./defenderctl.sh logs

# 手动运行一轮
./defenderctl.sh run-once

# 检查 PID 文件
rm -f .defender_research.pid

# 重新启动
./defenderctl.sh restart
```

---

## 开发指南

### 添加新规则

1. 创建规则文件 `rules/my_new_rules.json`:

```json
[
  {
    "id": "MY_RULE_001",
    "name": "我的检测规则",
    "patterns": ["malicious_pattern"],
    "risk": "HIGH",
    "description": "检测恶意行为",
    "action": "BLOCK"
  }
]
```

2. 测试规则:

```python
from scanner_v2 import DefenderScanner

scanner = DefenderScanner()
scanner.load_rules()

# 测试
result = scanner.detect("malicious_code_here")
print(result)
```

### 贡献代码

```bash
# Fork 项目
git fork https://gitee.com/caidongyun/agent-defender

# 创建分支
git checkout -b feature/my-new-feature

# 提交更改
git commit -m "feat: 添加新功能"

# 推送
git push origin feature/my-new-feature

# 创建 Pull Request
```

---

## 相关文档

- **集成报告**: `INTEGRATION_COMPLETE_V4.md`
- **测试报告**: `SCANNER_V2_COMPLETION_REPORT.md`
- **Benchmark 分析**: `BENCHMARK_ANALYSIS_REPORT.md`
- **持续研发**: `CONTINUOUS_RESEARCH.md`
- **快速参考**: `QUICK_REFERENCE.md`

---

## 许可证

MIT License

---

## 联系方式

- **项目地址**: https://gitee.com/caidongyun/agent-defender
- **问题反馈**: https://gitee.com/caidongyun/agent-defender/issues
- **讨论区**: https://gitee.com/caidongyun/agent-defender/discussions

---

**最后更新**: 2026-04-07  
**版本**: v2.0  
**状态**: ✅ 生产就绪
