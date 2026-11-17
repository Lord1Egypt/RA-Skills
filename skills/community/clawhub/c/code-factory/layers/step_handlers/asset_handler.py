"""
Step 3 处理器 —— 资产文件生成
"""

from pathlib import Path
from typing import Dict, Any, Optional

from layers.step_handlers.base_handler import BaseStepHandler
from layers.asset_generator import AssetGenerator
from middlewares.side_effect_log import SideEffectTracker
from middlewares.service_container import ServiceContainer


class AssetHandler(BaseStepHandler):
    """Step 3: 资产文件生成处理器"""

    def __init__(
        self,
        project_name: str,
        derived_spec: Optional[Dict],
        target_dir: Path,
        container: ServiceContainer,
        tracker: SideEffectTracker,
    ):
        self.project_name = project_name
        self.derived_spec = derived_spec
        self.target_dir = target_dir
        self.container = container
        self.tracker = tracker
        self.generator = AssetGenerator()

    def execute(self) -> Dict[str, Any]:
        tx = self.container.create_transaction_manager(self.target_dir)
        try:
            assets = self.generator.generate(
                project_name=self.project_name,
                spec=self.derived_spec,
                tx=tx,
                tracker=self.tracker,
            )
            tx.commit()
            return {"generated_files": assets}
        except Exception:
            tx.rollback()
            raise
