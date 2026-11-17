
# 日志记录
import logging
logger = logging.getLogger(__name__)
"""
健康检查模块

提供系统健康状态检查接口。

版本: 1.0.0
作者: AGI Evolution Team
"""

__version__ = '1.0.0'
__author__ = 'AGI Evolution Team'

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import os
import json
import shutil
from interfaces import TraceContext, create_trace_context


class HealthStatus(Enum):
    """健康状态"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class HealthCheck:
    """健康检查数据结构"""
    name: str
    status: HealthStatus
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'name': self.name,
            'status': self.status.value,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp
        }


@dataclass
class HealthReport:
    """健康报告数据结构"""
    status: HealthStatus
    checks: List[HealthCheck] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'status': self.status.value,
            'checks': [c.to_dict() for c in self.checks],
            'timestamp': self.timestamp,
            'version': self.version
        }


class HealthChecker:
    """健康检查器"""
    
    def __init__(self):
        """初始化健康检查器"""
        self.checks: List[callable] = []
    
    def register_check(self, check_func: callable):
        """
        注册健康检查
        
        Args:
            check_func: 检查函数，返回HealthCheck对象
        """
        self.checks.append(check_func)
    
    def check_all(self) -> HealthReport:
        """
        执行所有健康检查
        
        Returns:
            健康报告
        """
        checks = []
        overall_status = HealthStatus.HEALTHY
        
        for check_func in self.checks:
            try:
                check = check_func()
                checks.append(check)
                
                # 更新整体状态
                if check.status == HealthStatus.UNHEALTHY:
                    overall_status = HealthStatus.UNHEALTHY
                elif check.status == HealthStatus.DEGRADED and overall_status != HealthStatus.UNHEALTHY:
                    overall_status = HealthStatus.DEGRADED
            except Exception as e:
                # 检查函数执行失败
                check = HealthCheck(
                    name=check_func.__name__,
                    status=HealthStatus.UNHEALTHY,
                    message=f"检查执行失败: {str(e)}"
                )
                checks.append(check)
                overall_status = HealthStatus.UNHEALTHY
        
        return HealthReport(
            status=overall_status,
            checks=checks
        )
    
    def export_json(self) -> str:
        """
        导出为JSON格式
        
        Returns:
            JSON字符串
        """
        report = self.check_all()
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)


# ============================================================================
# 预定义的健康检查函数
# ============================================================================

def check_disk_space() -> HealthCheck:
    """检查磁盘空间"""
    try:
        # 检查当前目录所在磁盘（跨平台：shutil.disk_usage 同时支持 Linux/Windows/macOS）
        # 注意：os.statvfs 是 Linux 专属 API，在 Windows 上不存在，会导致检查直接抛异常
        usage = shutil.disk_usage('.')
        free_space = usage.free
        total_space = usage.total
        used_percent = ((total_space - free_space) / total_space) * 100
        
        if used_percent > 90:
            status = HealthStatus.UNHEALTHY
            message = f"磁盘空间不足: {used_percent:.1f}% 已使用"
        elif used_percent > 80:
            status = HealthStatus.DEGRADED
            message = f"磁盘空间警告: {used_percent:.1f}% 已使用"
        else:
            status = HealthStatus.HEALTHY
            message = f"磁盘空间正常: {used_percent:.1f}% 已使用"
        
        return HealthCheck(
            name="disk_space",
            status=status,
            message=message,
            details={
                'free_space': free_space,
                'total_space': total_space,
                'used_percent': used_percent
            }
        )
    except Exception as e:
        return HealthCheck(
            name="disk_space",
            status=HealthStatus.UNHEALTHY,
            message=f"检查失败: {str(e)}"
        )


def check_memory_usage() -> HealthCheck:
    """检查内存使用"""
    try:
        # 尝试读取 /proc/meminfo（Linux系统）
        if os.path.exists('/proc/meminfo'):
            with open('/proc/meminfo', 'r') as f:
                meminfo = {}
                for line in f:
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip().split()[0]
                        meminfo[key] = int(value)
            
            total_memory = meminfo.get('MemTotal', 0)
            available_memory = meminfo.get('MemAvailable', 0)
            used_percent = ((total_memory - available_memory) / total_memory) * 100 if total_memory > 0 else 0
            
            if used_percent > 90:
                status = HealthStatus.UNHEALTHY
                message = f"内存使用过高: {used_percent:.1f}%"
            elif used_percent > 80:
                status = HealthStatus.DEGRADED
                message = f"内存使用警告: {used_percent:.1f}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"内存使用正常: {used_percent:.1f}%"
            
            return HealthCheck(
                name="memory_usage",
                status=status,
                message=message,
                details={
                    'total_memory': total_memory,
                    'available_memory': available_memory,
                    'used_percent': used_percent
                }
            )
        else:
            return HealthCheck(
                name="memory_usage",
                status=HealthStatus.HEALTHY,
                message="无法检查内存使用（非Linux系统）"
            )
    except Exception as e:
        return HealthCheck(
            name="memory_usage",
            status=HealthStatus.UNHEALTHY,
            message=f"检查失败: {str(e)}"
        )


def check_file_permissions() -> HealthCheck:
    """检查文件权限"""
    try:
        # 检查关键目录的读写权限
        test_dir = '/tmp/agi_health_check'
        os.makedirs(test_dir, exist_ok=True)
        
        test_file = os.path.join(test_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        with open(test_file, 'r') as f:
            content = f.read()
        
        os.remove(test_file)
        os.rmdir(test_dir)
        
        if content == 'test':
            return HealthCheck(
                name="file_permissions",
                status=HealthStatus.HEALTHY,
                message="文件读写权限正常"
            )
        else:
            return HealthCheck(
                name="file_permissions",
                status=HealthStatus.UNHEALTHY,
                message="文件读写权限异常"
            )
    except Exception as e:
        return HealthCheck(
            name="file_permissions",
            status=HealthStatus.UNHEALTHY,
            message=f"检查失败: {str(e)}"
        )


def check_python_version() -> HealthCheck:
    """检查Python版本"""
    try:
        import sys
        version = sys.version_info
        
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            return HealthCheck(
                name="python_version",
                status=HealthStatus.UNHEALTHY,
                message=f"Python版本过低: {version.major}.{version.minor}.{version.micro}",
                details={
                    'version': f"{version.major}.{version.minor}.{version.micro}",
                    'required': ">=3.8"
                }
            )
        else:
            return HealthCheck(
                name="python_version",
                status=HealthStatus.HEALTHY,
                message=f"Python版本正常: {version.major}.{version.minor}.{version.micro}",
                details={
                    'version': f"{version.major}.{version.minor}.{version.micro}",
                    'required': ">=3.8"
                }
            )
    except Exception as e:
        return HealthCheck(
            name="python_version",
            status=HealthStatus.UNHEALTHY,
            message=f"检查失败: {str(e)}"
        )


def check_dependencies() -> HealthCheck:
    """检查依赖"""
    try:
        missing_deps = []
        
        # 检查关键依赖
        try:
            import aiofiles
        except ImportError:
            missing_deps.append('aiofiles')
        
        if missing_deps:
            return HealthCheck(
                name="dependencies",
                status=HealthStatus.DEGRADED,
                message=f"缺少依赖: {', '.join(missing_deps)}",
                details={
                    'missing': missing_deps
                }
            )
        else:
            return HealthCheck(
                name="dependencies",
                status=HealthStatus.HEALTHY,
                message="所有依赖已安装"
            )
    except Exception as e:
        return HealthCheck(
            name="dependencies",
            status=HealthStatus.UNHEALTHY,
            message=f"检查失败: {str(e)}"
        )


def check_c_extensions() -> HealthCheck:
    """检查 C 扩展是否真正加载（跨平台，使用集中加载器验证）"""
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from c_ext_loader import (
            load_c_extension,
            PERSONALITY_CORE_SYMBOLS,
            PERCEPTION_NODE_SYMBOLS,
        )

        results = {}
        overall_loaded = True
        for name, syms, probe in (
            ("personality_core", PERSONALITY_CORE_SYMBOLS,
             ("calculate_similarity", ([0.5] * 5, [0.5] * 5), {})),
            ("core_perception_node", PERCEPTION_NODE_SYMBOLS,
             ("generate_trace_id", (), {})),
        ):
            _mod, ok, detail = load_c_extension(name, required_symbols=syms, runtime_probe=probe)
            results[name] = {"loaded": ok, "detail": detail}
            overall_loaded = overall_loaded and ok

        # Windows 无 .pyd 属预期降级，不应报 unhealthy；posix 未加载/执行崩溃
        # 时功能仍可由纯 Python 完整提供，只是性能下降，故报 degraded 而非 unhealthy。
        if overall_loaded:
            status = HealthStatus.HEALTHY
            message = "C 扩展全部加载成功"
        elif sys.platform.startswith("win"):
            status = HealthStatus.HEALTHY
            message = "Windows 无 .pyd，已优雅降级到纯 Python（预期）"
        else:
            status = HealthStatus.DEGRADED
            message = "Linux/macOS 下 C 扩展未能加载/执行（二进制与 CPU 指令集不兼容？），已降级到纯 Python，性能下降"
        return HealthCheck(name="c_extensions", status=status, message=message, details=results)
    except Exception as e:
        return HealthCheck(
            name="c_extensions",
            status=HealthStatus.UNHEALTHY,
            message=f"检查失败: {str(e)}"
        )


# ============================================================================
# 全局健康检查器实例
# ============================================================================

_global_health_checker = HealthChecker()

# 注册预定义的检查
_global_health_checker.register_check(check_disk_space)
_global_health_checker.register_check(check_memory_usage)
_global_health_checker.register_check(check_file_permissions)
_global_health_checker.register_check(check_python_version)
_global_health_checker.register_check(check_dependencies)
_global_health_checker.register_check(check_c_extensions)


def get_health_checker() -> HealthChecker:
    """获取全局健康检查器"""
    return _global_health_checker


def check_health() -> HealthReport:
    """执行健康检查（全局）"""
    return _global_health_checker.check_all()


def export_health_json() -> str:
    """导出健康报告为JSON（全局）"""
    return _global_health_checker.export_json()


if __name__ == '__main__':
    # 测试健康检查
    print('健康检查模块测试')
    
    # 执行健康检查
    report = check_health()
    
    print(f'整体状态: {report.status.value}')
    print(f'检查数量: {len(report.checks)}')
    
    for check in report.checks:
        print(f'  - {check.name}: {check.status.value} - {check.message}')
    
    # 导出JSON
    json_output = export_health_json()
    print(f'\nJSON导出: {len(json_output)} 字符')
    print(json_output)
    
    print('\n健康检查模块测试完成')
