"""
智能数据采集器命令行接口
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import Optional

from . import DataHarvester, Config
from .openclaw_integration import OpenClawSkillWrapper, SkillManifest

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO"):
    """设置日志配置"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def collect_command(args):
    """收集数据命令"""
    setup_logging(args.log_level)
    
    try:
        harvester = DataHarvester(config_path=args.config)
        harvester.initialize()
        
        if args.source == "all":
            results = harvester.collect_all()
            print(f"收集完成: {len(results)} 个数据源")
            for source_name, result in results.items():
                status = "成功" if result.success else "失败"
                print(f"  {source_name}: {status}")
                if not result.success and result.errors:
                    print(f"    错误: {result.errors[0]}")
        else:
            result = harvester.collect(args.source)
            if result.success:
                print(f"数据收集成功: {args.source}")
                print(f"数据大小: {len(str(result.data)) if result.data else 0} 字符")
                if args.export:
                    success = harvester.export(result.data, args.export)
                    print(f"导出 {'成功' if success else '失败'}: {args.export}")
            else:
                print(f"数据收集失败: {args.source}")
                for error in result.errors:
                    print(f"  错误: {error}")
        
        harvester.shutdown()
        
    except Exception as e:
        logger.error(f"命令执行失败: {e}")
        sys.exit(1)


def export_command(args):
    """导出数据命令"""
    setup_logging(args.log_level)
    
    try:
        # 这里需要根据实际情况实现数据加载
        print(f"导出功能待实现: {args.exporter}")
        # TODO: 实现数据加载和导出
        
    except Exception as e:
        logger.error(f"导出失败: {e}")
        sys.exit(1)


def status_command(args):
    """状态检查命令"""
    setup_logging(args.log_level)
    
    try:
        harvester = DataHarvester(config_path=args.config)
        harvester.initialize()
        
        status = harvester.get_status()
        print("数据采集器状态:")
        print(f"  初始化: {'是' if status['initialized'] else '否'}")
        print(f"  适配器数量: {status['adapter_count']}")
        print(f"  处理器数量: {status['processor_count']}")
        print(f"  导出器数量: {status['exporter_count']}")
        
        if status['scheduler_running']:
            print(f"  调度器运行中: 是")
            print(f"  活动任务: {status['active_tasks']}")
        
        harvester.shutdown()
        
    except Exception as e:
        logger.error(f"状态检查失败: {e}")
        sys.exit(1)


def skill_command(args):
    """技能管理命令"""
    setup_logging(args.log_level)
    
    try:
        if args.subcommand == "create":
            # 创建技能清单
            manifest = SkillManifest()
            output_dir = Path(args.output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            manifest.save(output_dir / "skill_manifest", format="json")
            manifest.save(output_dir / "skill_manifest", format="yaml")
            
            print(f"技能清单已创建: {output_dir}")
            print(f"  技能名称: {manifest.name}")
            print(f"  技能版本: {manifest.version}")
            print(f"  技能价格: 基础版¥299, 专业版¥899, 企业版¥2999")
            
        elif args.subcommand == "package":
            # 创建技能包
            skill = OpenClawSkillWrapper(args.config)
            package_dir = skill.create_skill_package(args.output_dir)
            
            print(f"技能包已创建: {package_dir}")
            print("包内文件:")
            for file in sorted(package_dir.rglob("*")):
                if file.is_file():
                    rel_path = file.relative_to(package_dir)
                    print(f"  - {rel_path}")
                    
        elif args.subcommand == "validate":
            # 验证技能清单
            manifest = SkillManifest.load(args.manifest_file)
            errors = manifest.validate()
            
            if errors:
                print(f"技能清单验证失败，发现 {len(errors)} 个错误:")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
            else:
                print("技能清单验证通过!")
                
        else:
            print(f"未知子命令: {args.subcommand}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"技能管理失败: {e}")
        sys.exit(1)


def create_parser():
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        description="智能数据采集器命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s collect --config config.yaml --source web_data
  %(prog)s collect --config config.yaml --source all
  %(prog)s status --config config.yaml
  %(prog)s skill create --output-dir skill_package/
  %(prog)s skill package --config config.yaml --output-dir dist/
        """
    )
    
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="日志级别"
    )
    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="命令")
    subparsers.required = True
    
    # collect命令
    collect_parser = subparsers.add_parser("collect", help="收集数据")
    collect_parser.add_argument("--config", required=True, help="配置文件路径")
    collect_parser.add_argument("--source", required=True, help="数据源名称或'all'")
    collect_parser.add_argument("--export", help="导出器名称")
    collect_parser.set_defaults(func=collect_command)
    
    # export命令
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("--config", required=True, help="配置文件路径")
    export_parser.add_argument("--exporter", required=True, help="导出器名称")
    export_parser.add_argument("--data", help="数据文件路径")
    export_parser.set_defaults(func=export_command)
    
    # status命令
    status_parser = subparsers.add_parser("status", help="检查状态")
    status_parser.add_argument("--config", required=True, help="配置文件路径")
    status_parser.set_defaults(func=status_command)
    
    # skill命令
    skill_parser = subparsers.add_parser("skill", help="技能管理")
    skill_subparsers = skill_parser.add_subparsers(dest="subcommand", help="子命令")
    skill_subparsers.required = True
    
    # skill create
    create_parser = skill_subparsers.add_parser("create", help="创建技能清单")
    create_parser.add_argument("--output-dir", default="skill_package", help="输出目录")
    create_parser.set_defaults(func=skill_command)
    
    # skill package
    package_parser = skill_subparsers.add_parser("package", help="创建技能包")
    package_parser.add_argument("--config", help="配置文件路径")
    package_parser.add_argument("--output-dir", default="dist", help="输出目录")
    package_parser.set_defaults(func=skill_command)
    
    # skill validate
    validate_parser = skill_subparsers.add_parser("validate", help="验证技能清单")
    validate_parser.add_argument("manifest_file", help="技能清单文件")
    validate_parser.set_defaults(func=skill_command)
    
    return parser


def main():
    """主函数"""
    parser = create_parser()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()