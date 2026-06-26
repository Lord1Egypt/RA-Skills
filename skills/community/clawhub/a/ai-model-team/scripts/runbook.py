"""
Runbook & Operations Manual
P2: Troubleshooting, rollback procedures, on-call guide
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timezone

# ============ Runbook Entry ============

@dataclass
class RunbookEntry:
    """运行手册条目"""
    issue: str
    symptom: str
    cause: str
    diagnosis_steps: List[str]
    resolution: str
    prevention: str
    severity: str  # P1/P2/P3
    last_updated: str


class Runbook:
    """故障排查手册"""
    
    ENTRIES = [
        RunbookEntry(
            issue="模型加载失败",
            symptom="ImportError 或模型文件找不到",
            cause="模型文件损坏、版本不匹配、依赖缺失",
            diagnosis_steps=[
                "1. 检查错误日志中的具体 ImportError",
                "2. 验证模型文件是否存在: ls ~/.cache/huggingface/",
                "3. 检查 Python 版本: python3 --version",
                "4. 验证依赖安装: pip list | grep <model_name>",
                "5. 尝试重新安装模型"
            ],
            resolution="1. 清理缓存: rm -rf ~/.cache/huggingface/\n2. 重新安装依赖\n3. 重新下载模型",
            prevention="使用精确版本锁定，定期验证环境",
            severity="P1",
            last_updated="2026-04-15"
        ),
        RunbookEntry(
            issue="数据获取超时",
            symptom="requests timeout 或 ConnectionError",
            cause="网络问题、OKX API 限流、数据源不可用",
            diagnosis_steps=[
                "1. 检查网络: curl https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT-SWAP",
                "2. 检查 OKX 状态: https://www.okx.com/status",
                "3. 查看请求超时配置",
                "4. 检查是否有 IP 限流"
            ],
            resolution="1. 等待恢复\n2. 使用备用数据源\n3. 调整超时配置\n4. 联系 OKX 支持",
            prevention="实现降级策略，多数据源备份",
            severity="P1",
            last_updated="2026-04-15"
        ),
        RunbookEntry(
            issue="预测结果异常",
            symptom="预测值远超合理范围",
            cause="输入数据异常、模型未收敛、数据对齐问题",
            diagnosis_steps=[
                "1. 检查输入数据完整性: python3 -c 'from data_quality import *; print(check_data(df))'",
                "2. 验证时间对齐: 检查各数据源时间戳",
                "3. 查看数据分布是否异常",
                "4. 检查是否有 NaN/Inf 值"
            ],
            resolution="1. 使用数据质量校验\n2. 过滤异常数据\n3. 使用前一天的数据",
            prevention="数据校验前置，输出范围检查",
            severity="P1",
            last_updated="2026-04-15"
        ),
        RunbookEntry(
            issue="风控闸门误触发",
            symptom="连续阻止合法交易信号",
            cause="风控阈值设置过严、数据问题导致连续亏损",
            diagnosis_steps=[
                "1. 查看风控状态: GET /risk/status",
                "2. 检查触发规则: 查看 triggered_rules",
                "3. 分析交易历史: 检查 loss 记录",
                "4. 验证数据质量"
            ],
            resolution="1. 冷却后自动恢复\n2. 手动重置风控状态\n3. 调整阈值参数",
            prevention="设置合理的风控阈值，定期复盘",
            severity="P2",
            last_updated="2026-04-15"
        ),
        RunbookEntry(
            issue="内存溢出 (OOM)",
            symptom="Python 进程被 killed",
            cause="模型过大、数据量过大、内存泄漏",
            diagnosis_steps=[
                "1. 检查内存使用: htop 或 ps aux | grep python",
                "2. 查看 dmesg 日志",
                "3. 检查模型大小",
                "4. 分析数据批量大小"
            ],
            resolution="1. 减小批处理大小\n2. 使用量化模型\n3. 增加 swap",
            prevention="模型量化，分批处理，内存监控",
            severity="P1",
            last_updated="2026-04-15"
        ),
        RunbookEntry(
            issue="社媒情绪数据噪声",
            symptom="情绪分数异常波动",
            cause="热点事件、机器人发帖、来源不稳定",
            diagnosis_steps=[
                "1. 检查去重结果: 查看 deduplicated count",
                "2. 分析来源分布",
                "3. 检查时间衰减设置",
                "4. 验证关键词过滤"
            ],
            resolution="1. 增强去重规则\n2. 提高来源权重\n3. 延长半衰期",
            prevention="多源交叉验证，异常检测",
            severity="P2",
            last_updated="2026-04-15"
        )
    ]
    
    @classmethod
    def get_entry(cls, issue: str) -> Optional[RunbookEntry]:
        """查找故障条目"""
        for entry in cls.ENTRIES:
            if issue.lower() in entry.issue.lower():
                return entry
        return None
    
    @classmethod
    def get_all(cls) -> List[RunbookEntry]:
        return cls.ENTRIES
    
    @classmethod
    def get_by_severity(cls, severity: str) -> List[RunbookEntry]:
        return [e for e in cls.ENTRIES if e.severity == severity]


class RollbackManager:
    """回滚管理器"""
    
    @staticmethod
    def rollback_config(backup_tag: str = None) -> bool:
        """
        回滚配置到上一个稳定版本
        
        Args:
            backup_tag: 备份标签，默认使用最近备份
        """
        import subprocess
        import shutil
        from pathlib import Path
        
        config_dir = Path(__file__).parent.parent
        backup_dir = config_dir / "backups"
        
        if not backup_dir.exists():
            print("No backups found")
            return False
        
        # 列出备份
        backups = sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not backups:
            print("No backups found")
            return False
        
        target = backups[0] if backup_tag is None else backup_dir / backup_tag
        
        if not target.exists():
            print(f"Backup {target} not found")
            return False
        
        # 执行回滚
        # 1. 备份当前
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        current_backup = config_dir / f"config_before_rollback_{timestamp}"
        shutil.copytree(config_dir / "scripts", current_backup / "scripts")
        
        # 2. 恢复目标备份
        shutil.rmtree(config_dir / "scripts")
        shutil.copytree(target / "scripts", config_dir / "scripts")
        
        print(f"Rolled back to {target}")
        return True
    
    @staticmethod
    def create_backup() -> str:
        """创建配置备份"""
        import shutil
        from pathlib import Path
        
        config_dir = Path(__file__).parent.parent
        backup_dir = config_dir / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"backup_{timestamp}"
        
        shutil.copytree(config_dir / "scripts", backup_path / "scripts")
        
        # 保存元数据
        import json
        with open(backup_path / "metadata.json", 'w') as f:
            json.dump({
                "created_at": datetime.now(timezone.utc).isoformat(),
                "version": "v2.0.0"
            }, f)
        
        print(f"Backup created: {backup_path}")
        return str(backup_path)


class OnCallGuide:
    """值班指南"""
    
    @staticmethod
    def get_health_check() -> Dict:
        """健康检查清单"""
        return {
            "system": [
                "✅ Python 进程运行中",
                "✅ 磁盘空间充足 (>20%)",
                "✅ 内存使用正常 (<80%)",
                "✅ 网络连接正常"
            ],
            "data": [
                "✅ OKX API 可访问",
                "✅ 数据获取正常",
                "✅ 数据完整率 >98%",
                "✅ 无时间漂移"
            ],
            "models": [
                "✅ Kronos 加载正常",
                "✅ TimesFM 加载正常",
                "✅ Chronos-2 加载正常",
                "✅ FinBERT 加载正常"
            ],
            "alerts": [
                "✅ 无 P1 告警",
                "✅ 无数据源断流",
                "✅ 风控状态正常",
                "✅ 日志无 ERROR"
            ]
        }
    
    @staticmethod
    def get_p1_response_steps() -> str:
        """P1 故障响应步骤"""
        return """
        P1 故障响应流程:
        
        1. 立即响应 (5分钟内)
           - 确认告警真实性
           - 评估影响范围
           - 启动 incident
        
        2. 止损 (15分钟内)
           - 停止有问题的交易
           - 启用备用策略
           - 通知相关方
        
        3. 诊断 (30分钟内)
           - 查看日志
           - 检查监控面板
           - 定位根因
        
        4. 修复 (根据情况)
           - 执行回滚如需要
           - 应用热修复
           - 验证修复有效
        
        5. 复盘 (事后)
           - 编写 incident report
           - 更新 runbook
           - 改进监控
        """
    
    @staticmethod
    def get_escalation_contacts() -> Dict:
        """升级联系人"""
        return {
            "L1_oncall": "ai-team-oncall@company.com",
            "L2_eng": "ai-engineering@company.com",
            "L3_lead": "ai-lead@company.com",
            "security": "security@company.com",
            "on_call_phone": "+86-XXX-XXXX-XXXX"
        }


def print_runbook():
    """打印完整运行手册"""
    print("=" * 80)
    print("AI Model Team 运行手册")
    print("=" * 80)
    
    runbook = Runbook()
    for severity in ["P1", "P2", "P3"]:
        entries = runbook.get_by_severity(severity)
        if entries:
            print(f"\n### {severity} 故障 ({len(entries)} 项)")
            print("-" * 80)
            
            for entry in entries:
                print(f"\n【{entry.issue}】")
                print(f"现象: {entry.symptom}")
                print(f"原因: {entry.cause}")
                print(f"诊断: {' -> '.join(entry.diagnosis_steps[:3])}...")
                print(f"解决: {entry.resolution[:100]}...")
    
    print("\n" + "=" * 80)
    print("健康检查清单:")
    health = OnCallGuide.get_health_check()
    for category, items in health.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  {item}")
    
    print("\n" + "=" * 80)
