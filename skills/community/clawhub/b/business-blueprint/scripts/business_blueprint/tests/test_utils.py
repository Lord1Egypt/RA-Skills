"""
测试工具函数

提供测试常用的工具函数：
- 加载测试数据集
- 运行导出命令
- 保存测试结果
- 生成测试报告
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import shutil


def load_test_set(test_dir: str) -> List[Dict]:
    """加载测试数据集"""
    test_path = Path(test_dir)
    if not test_path.exists():
        return []

    test_set = []
    for blueprint_file in test_path.glob("**/*.blueprint.json"):
        blueprint = json.load(open(blueprint_file))
        test_set.append({
            "blueprint": blueprint,
            "path": str(blueprint_file),
            "name": blueprint_file.stem
        })

    return test_set


def load_golden_fixtures(fixtures_dir: str) -> List[Dict]:
    """加载Golden Fixtures"""
    return load_test_set(fixtures_dir)


def run_export_command(blueprint_path: str, output_dir: str) -> Dict:
    """运行导出命令"""
    # 确保在项目根目录运行（设置cwd）
    project_root = Path(__file__).parent.parent.parent.parent

    cmd = [
        "python",
        str(project_root / "scripts" / "business_blueprint" / "cli.py"),
        "--export",
        blueprint_path
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(project_root)  # 确保工作目录是项目根目录
        )

        # 检查输出文件
        # stem处理：common.blueprint.json → common
        blueprint_file = Path(blueprint_path)
        blueprint_name = blueprint_file.stem.replace(".blueprint", "")
        exports_dir = blueprint_file.parent / f"{blueprint_name}.exports"

        output_files = []
        if exports_dir.exists():
            output_files = list(exports_dir.glob("*.svg")) + list(exports_dir.glob("*.html"))

        # 详细调试信息
        if result.returncode != 0 or not output_files:
            print(f"      Command: {cmd}")
            print(f"      Returncode: {result.returncode}")
            print(f"      Stdout: {result.stdout if result.stdout else 'None'}")
            print(f"      Stderr: {result.stderr if result.stderr else 'None'}")  # 显示完整stderr
            print(f"      Exports dir exists: {exports_dir.exists()}")
            print(f"      Output files: {len(output_files)}")

        return {
            "success": result.returncode == 0 and len(output_files) > 0,
            "output_files": [str(f) for f in output_files],
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exports_dir": str(exports_dir)
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Timeout"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def save_test_result(result: Dict, output_path: str):
    """保存测试结果"""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    json.dump(result, open(output_file, "w"), indent=2, ensure_ascii=False)


def copy_output_to_fixture(exports_dir: str, fixture_dir: str, name: str):
    """复制输出到fixture目录"""
    exports_path = Path(exports_dir)
    fixture_path = Path(fixture_dir)

    if not exports_path.exists():
        return

    # 复制SVG和HTML文件
    for file in exports_path.glob("*.svg"):
        shutil.copy(file, fixture_path / f"{name}.svg")

    for file in exports_path.glob("*.html"):
        shutil.copy(file, fixture_path / f"{name}.html")


def validate_output(output_path: str) -> bool:
    """验证输出是否有效"""
    output_file = Path(output_path)
    if not output_file.exists():
        return False

    content = output_file.read_text()

    # 检查是否有基本内容
    if len(content) < 100:
        return False

    # 检查是否有title
    if "<title>" not in content:
        return False

    # 检查是否有系统节点
    if "rect" not in content or "text" not in content:
        return False

    return True


def create_test_blueprint(
    goals: List[str],
    systems: List[Dict],
    industry: str = "common"
) -> Dict:
    """创建测试蓝图（简化版）"""
    return {
        "version": "1.0",
        "meta": {
            "title": "Test Blueprint",
            "industry": industry,
            "revisionId": "rev-20260425-01"
        },
        "context": {
            "goals": goals,
            "scope": [],
            "assumptions": [],
            "constraints": []
        },
        "library": {
            "capabilities": [],
            "actors": [],
            "flowSteps": [],
            "systems": systems
        },
        "relations": [],
        "views": [],
        "editor": {}
    }


def generate_final_report(phase_results: List[Dict]) -> Dict:
    """生成最终评估报告"""
    return {
        "test_date": "2026-04-25",
        "phases": phase_results,
        "overall_success": all(
            phase.get("pass_status", False)
            for phase in phase_results
        ),
        "summary": {
            "total_phases": len(phase_results),
            "passed_phases": sum(
                1 for phase in phase_results
                if phase.get("pass_status", False)
            ),
            "failed_phases": sum(
                1 for phase in phase_results
                if not phase.get("pass_status", False)
            )
        },
        "recommendations": generate_recommendations(phase_results)
    }


def generate_recommendations(phase_results: List[Dict]) -> List[str]:
    """生成改进建议"""
    recommendations = []

    for phase in phase_results:
        if not phase.get("pass_status", False):
            phase_name = phase.get("test_phase", "Unknown")
            failed_metrics = [
                k for k, v in phase.get("metrics", {}).items()
                if isinstance(v, tuple) and v[0] < v[1]
            ]

            if failed_metrics:
                recommendations.append(
                    f"{phase_name}: 需改进指标 {', '.join(failed_metrics)}"
                )

    return recommendations