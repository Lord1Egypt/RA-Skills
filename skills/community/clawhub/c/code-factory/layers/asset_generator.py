"""
Step 3: 资产文件生成器 —— 根据 Spec 生成标准化项目结构。

所有文件写入通过 TransactionManager 暂存，而非直接写磁盘。
配合 SideEffectTracker 记录所有操作。
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional

from middlewares.transaction_manager import TransactionManager
from middlewares.side_effect_log import SideEffectTracker, SideEffectType
from contracts.asset_manifest_schema import (
    AssetManifest,
    AssetEntry,
    AssetGenerationMethod,
)
from contracts.input_schema import ProjectType
from templates.project_structure import get_directory_structure
from templates.readme_template import generate_readme
from templates.manifest_template import generate_manifest_json
from templates.environment_template import generate_environment_toml
from templates.skill_template import generate_skill_md
from templates.run_sh_template import generate_run_sh


class AssetGenerator:
    """资产文件生成器 —— 所有写入通过 TransactionManager（v3.0：幂等性增强）"""

    def generate(
        self,
        project_name: str,
        spec: Optional[Dict],
        tx: TransactionManager,
        tracker: SideEffectTracker,
        force: bool = False,
    ) -> List[str]:
        """
        根据 Spec 生成所有资产文件。

        v3.0 增强：幂等性检查。
        如果目标文件已存在且内容相同，默认跳过生成（force=True 可强制覆盖）。

        Args:
            project_name: 项目名称
            force: 强制覆盖已存在的文件（默认 False，启用幂等性检查）
            spec: Step 2 推导出的 Spec（dict 格式）
            tx: 事务管理器（staging 模式）
            tracker: 副作用追踪器

        Returns:
            生成的文件路径列表
        """
        if spec is None:
            raise ValueError(
                "AssetGenerator.generate() 收到 spec=None —— "
                "Step 2 Spec 推导可能失败或未执行。请检查上游步骤。"
            )
        files = spec.get("files", [])
        deps = spec.get("dependencies", [])
        description = spec.get("description", "") or project_name

        generated: List[str] = []
        manifest_entries: List[AssetEntry] = []

        # 确保目录结构存在
        dirs = get_directory_structure()
        for d in dirs:
            tx.stage_create(f"{d}/.gitkeep", "")

        # 按 Spec 中的文件列表生成
        for file_spec in files:
            path = file_spec.get("path", "")
            desc = file_spec.get("description", "")
            is_hard_gate = file_spec.get("is_hard_gate", False)
            content = self._generate_file_content(path, project_name, description, deps)

            # v3.2: 幂等性检查——如果目标文件已存在且内容相同，跳过 staging
            if not force and self._is_content_identical(path, content, tx):
                self._record_asset(generated, manifest_entries, tracker,
                                   path, desc, is_hard_gate, content, project_name)
                continue

            tx.stage_create(path, content)
            self._record_asset(generated, manifest_entries, tracker,
                               path, desc, is_hard_gate, content, project_name)

        # 生成资产清单
        manifest = AssetManifest(
            project_name=project_name,
            project_description=description,
            assets=manifest_entries,
        )

        # ASSET_MANIFEST.md（人类可读）
        manifest_md = manifest.to_markdown()
        tx.stage_create("ASSET_MANIFEST.md", manifest_md)
        generated.append("ASSET_MANIFEST.md")
        tracker.record(SideEffectType.FILE_CREATE, "ASSET_MANIFEST.md", after_state=manifest_md)

        # manifest.json（机器可读）
        manifest_json = json.dumps(manifest.to_json_dict(), ensure_ascii=False, indent=2)
        tx.stage_create("manifest.json", manifest_json)
        generated.append("manifest.json")
        tracker.record(SideEffectType.FILE_CREATE, "manifest.json", after_state=manifest_json)

        # README
        readme = generate_readme(project_name, description)
        tx.stage_create("docs/README.md", readme)
        generated.append("docs/README.md")
        tracker.record(SideEffectType.FILE_CREATE, "docs/README.md", after_state=readme)

        # environment.toml
        env_toml = generate_environment_toml(project_name)
        tx.stage_create("environment.toml", env_toml)
        generated.append("environment.toml")
        tracker.record(SideEffectType.FILE_CREATE, "environment.toml", after_state=env_toml)

        # SKILL.md
        skill_md = generate_skill_md(project_name, description)
        tx.stage_create("SKILL.md", skill_md)
        generated.append("SKILL.md")
        tracker.record(SideEffectType.FILE_CREATE, "SKILL.md", after_state=skill_md)

        # run.sh
        run_sh = generate_run_sh(project_name)
        tx.stage_create("run.sh", run_sh)
        generated.append("run.sh")
        tracker.record(SideEffectType.FILE_CREATE, "run.sh", after_state=run_sh)

        # requirements.txt
        req_content = "\n".join(deps) + "\n"
        tx.stage_create("requirements.txt", req_content)
        generated.append("requirements.txt")
        tracker.record(SideEffectType.FILE_CREATE, "requirements.txt", after_state=req_content)

        return generated

    @staticmethod
    def _resolve_target_path(path: str, tx: TransactionManager) -> Optional[Path]:
        """解析文件在目标目录中的绝对路径（用于幂等性检查）"""
        target = tx.target_dir / path
        return target if target.exists() else None

    @staticmethod
    def _is_content_identical(path: str, content: str, tx: TransactionManager) -> bool:
        """检查目标文件是否存在且内容与待生成内容相同"""
        target = AssetGenerator._resolve_target_path(path, tx)
        if not target:
            return False
        try:
            return target.read_text(encoding="utf-8") == content
        except (OSError, UnicodeDecodeError):
            return False

    @staticmethod
    def _record_asset(
        generated: List[str],
        manifest_entries: List[AssetEntry],
        tracker: SideEffectTracker,
        path: str,
        desc: str,
        is_hard_gate: bool,
        content: str,
        project_name: str,
    ) -> None:
        """记录已生成的文件到 generated 列表、manifest 和 tracker"""
        generated.append(path)
        manifest_entries.append(AssetEntry(
            path=path,
            purpose=desc,
            generation_method=AssetGenerationMethod.AUTO_GENERATED,
            is_hard_gate=is_hard_gate,
        ))
        tracker.record(
            SideEffectType.FILE_CREATE, path,
            after_state=content,
            project_name=project_name,
        )

    def _generate_file_content(
        self, path: str, project_name: str, description: str, deps: List[str]
    ) -> str:
        """
        根据文件路径生成对应的内容。

        Raises:
            ValueError: 未知的文件路径（拒绝生成空文件）
        """
        if path == "src/main.py":
            return self._generate_main_py(project_name, description)
        elif path == "tests/test_main.py":
            return self._generate_test_py(project_name)
        elif path == "requirements.txt":
            return "\n".join(deps) + "\n"
        elif path == "src/app.py":
            return self._generate_app_py(project_name)
        elif path == "src/api.py":
            return self._generate_api_py(project_name)
        elif path.endswith((".md", ".toml", ".json", ".sh")):
            # 这些文件由模板函数生成，不在 _generate_file_content 中处理
            # 但为防止意外到达这里，返回占位内容并记录
            return f"# {path}\n# 此文件由模板生成器处理\n"
        raise ValueError(
            f"未知文件类型: '{path}' — 无法生成内容。"
            f"支持的类型: src/main.py, tests/test_main.py, requirements.txt,"
            f" src/app.py, src/api.py"
        )

    def _generate_app_py(self, project_name: str) -> str:
        """生成 Web 应用模块"""
        return f'''"""
{project_name} — Web 应用模块
<!-- HARD-GATE -->
"""


def create_app():
    """创建 Flask 应用实例"""
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def index():
        return {{"status": "ok", "app": "{project_name}"}}

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
'''

    def _generate_api_py(self, project_name: str) -> str:
        """生成 API 路由模块"""
        return f'''"""
{project_name} — API 路由定义
<!-- HARD-GATE -->
"""

from fastapi import FastAPI

app = FastAPI(title="{project_name}")


@app.get("/")
async def root():
    return {{"status": "ok", "app": "{project_name}"}}
'''

    def _generate_main_py(self, project_name: str, description: str) -> str:
        """生成主程序模板"""
        return f'''"""
{project_name} — {description}
<!-- HARD-GATE -->
"""

import sys
from typing import Optional


def main(args: Optional[list[str]] = None) -> int:
    """主入口函数"""
    print(f"{{project_name}} 启动成功")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

    def _generate_test_py(self, project_name: str) -> str:
        """生成测试文件模板"""
        return f'''"""
{project_name} — 单元测试
"""

import pytest
from src.main import main


def test_main_returns_zero():
    """测试主函数正常返回 0"""
    result = main([])
    assert result == 0


def test_main_with_args():
    """测试主函数接受参数"""
    result = main(["--help"])
    assert isinstance(result, int)
'''
