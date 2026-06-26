import os
import json
from datetime import datetime
from typing import Any, Optional, Dict, List


class AnalysisWorkflow:
    """
    数据分析工作流管理器

    管理每次分析的生命周期，包括：
    - 工作区创建
    - 步骤输出保存/加载
    - 断点检查
    - 文件路径管理
    """

    STEP_STRUCTURE = {
        "01_exploration": {
            "description": "数据探查",
            "outputs": [
                "tables.json",
                "schema_{table_name}.json"
            ]
        },
        "02_acquisition": {
            "description": "数据获取",
            "outputs": [
                "raw_data.csv"
            ]
        },
        "03_quality": {
            "description": "质量检查",
            "outputs": [
                "quality_report.json"
            ]
        },
        "04_eda": {
            "description": "探索性分析",
            "outputs": [
                "metrics.json",
                "trends.json",
                "comparison.json",
                "topn.json"
            ]
        },
        "05_conclusion": {
            "description": "结论提炼",
            "outputs": [
                "conclusion.md",
                "reflection.json"
            ]
        },
        "06_report": {
            "description": "报告生成",
            "outputs": [
                "analysis_report.html",
                "analysis_report.png"
            ]
        }
    }

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            current_file = os.path.abspath(__file__)
            skill_dir = os.path.dirname(current_file)
            base_dir = os.path.dirname(skill_dir)
            while base_dir and not os.path.exists(os.path.join(base_dir, '.trae')):
                parent = os.path.dirname(base_dir)
                if parent == base_dir:
                    break
                base_dir = parent

        self.workspace_root = os.path.join(base_dir, "workspace")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.analysis_id = f"analysis_{self.timestamp}"
        self.workspace = os.path.join(self.workspace_root, self.analysis_id)
        self.context: Dict[str, Any] = {}

    def create_workspace(self) -> str:
        """
        创建工作目录结构

        Returns:
            工作区路径，例如: /path/to/workspace/analysis_20260308_143022/
        """
        for step_name in self.STEP_STRUCTURE.keys():
            path = os.path.join(self.workspace, step_name)
            os.makedirs(path, exist_ok=True)

        self._save_metadata()
        return self.workspace

    def _save_metadata(self):
        """保存分析元数据"""
        metadata = {
            "analysis_id": self.analysis_id,
            "timestamp": self.timestamp,
            "created_at": datetime.now().isoformat(),
            "steps": {k: v["description"] for k, v in self.STEP_STRUCTURE.items()}
        }
        metadata_path = os.path.join(self.workspace, "metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

    def get_workspace_path(self) -> str:
        """获取当前工作区路径"""
        return self.workspace

    def get_analysis_id(self) -> str:
        """获取分析ID"""
        return self.analysis_id

    def get_step_path(self, step_name: str) -> str:
        """获取指定步骤的目录路径"""
        return os.path.join(self.workspace, step_name)

    def get_output_path(self, step_name: str, filename: str) -> str:
        """获取指定输出文件的完整路径"""
        return os.path.join(self.workspace, step_name, filename)

    def save_step_output(
        self,
        step_name: str,
        filename: str,
        data: Any,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        保存步骤输出

        Args:
            step_name: 步骤名称，如 "01_exploration"
            filename: 文件名，如 "tables.json"
            data: 数据内容 (dict, list, DataFrame, str)
            metadata: 可选的元数据

        Returns:
            保存的文件路径
        """
        path = os.path.join(self.workspace, step_name, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if isinstance(data, (dict, list)):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif hasattr(data, 'to_csv'):
            data.to_csv(path, index=False, encoding='utf-8')
        elif hasattr(data, 'to_json'):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(data.to_json(orient='records', force_ascii=False))
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(str(data))

        if metadata:
            meta_path = path + ".meta.json"
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)

        return path

    def load_step_output(self, step_name: str, filename: str) -> Any:
        """
        加载步骤输出（断点续传用）

        Args:
            step_name: 步骤名称
            filename: 文件名

        Returns:
            加载的数据，文件不存在返回 None
        """
        path = os.path.join(self.workspace, step_name, filename)
        if not os.path.exists(path):
            return None

        if filename.endswith('.json'):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif filename.endswith('.csv'):
            import pandas as pd
            return pd.read_csv(path)
        elif filename.endswith('.md'):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()

    def check_step_completed(self, step_name: str) -> bool:
        """
        检查步骤是否已完成

        Args:
            step_name: 步骤名称

        Returns:
            如果步骤目录存在且有输出文件返回 True
        """
        if step_name not in self.STEP_STRUCTURE:
            return False

        step_dir = os.path.join(self.workspace, step_name)
        if not os.path.exists(step_dir):
            return False

        expected_outputs = self.STEP_STRUCTURE[step_name]["outputs"]
        for output in expected_outputs:
            if output.startswith("{"):
                pattern_parts = output.replace("}", "").split("{")
                for part in os.listdir(step_dir):
                    if any(p in part for p in pattern_parts if p):
                        return True
                continue
            if os.path.exists(os.path.join(step_dir, output)):
                return True

        return len(os.listdir(step_dir)) > 0

    def get_completed_steps(self) -> List[str]:
        """获取已完成的步骤列表"""
        completed = []
        for step_name in self.STEP_STRUCTURE.keys():
            if self.check_step_completed(step_name):
                completed.append(step_name)
        return completed

    def get_next_step(self) -> Optional[str]:
        """获取下一个需要执行的步骤"""
        for step_name in self.STEP_STRUCTURE.keys():
            if not self.check_step_completed(step_name):
                return step_name
        return None

    def get_relative_path(self, full_path: str) -> str:
        """获取相对于项目根的路径"""
        return full_path.replace(self.workspace_root + "/", "")

    def get_workspace_url(self) -> str:
        """获取工作区的 file:// URL"""
        return f"file://{self.workspace}"

    def set_context(self, key: str, value: Any):
        """设置上下文数据"""
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """获取上下文数据"""
        return self.context.get(key, default)

    def save_context(self):
        """保存上下文到文件"""
        context_path = os.path.join(self.workspace, "context.json")
        with open(context_path, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, ensure_ascii=False, indent=2)

    def load_context(self) -> bool:
        """从文件加载上下文"""
        context_path = os.path.join(self.workspace, "context.json")
        if os.path.exists(context_path):
            with open(context_path, 'r', encoding='utf-8') as f:
                self.context = json.load(f)
            return True
        return False

    def save_data_sources(self, sources: List[Dict[str, Any]]):
        """保存多数据源配置（Step 1 必用）"""
        data = {"sources": sources}
        self.save_step_output("01_exploration", "data_sources.json", data)
        self.set_context("data_sources", sources)

    def load_data_sources(self) -> Optional[List[Dict[str, Any]]]:
        """加载多数据源配置"""
        data = self.load_step_output("01_exploration", "data_sources.json")
        if data:
            return data.get("sources", [])
        return self.get_context("data_sources")

    def save_acquisition_summary(self, summary: Dict[str, Any]):
        """保存数据获取摘要（Step 2 必用）"""
        self.save_step_output("02_acquisition", "acquisition_summary.json", summary)

    def load_acquisition_summary(self) -> Optional[Dict[str, Any]]:
        """加载数据获取摘要"""
        return self.load_step_output("02_acquisition", "acquisition_summary.json")

    def get_source_data(self, source_name: str) -> Optional[Any]:
        """获取指定数据源的数据（按名称查找 CSV 文件）"""
        acquisition_dir = os.path.join(self.workspace, "02_acquisition")
        if not os.path.exists(acquisition_dir):
            return None

        for filename in os.listdir(acquisition_dir):
            if filename.endswith('.csv') and source_name in filename:
                import pandas as pd
                return pd.read_csv(os.path.join(acquisition_dir, filename))
        return None

    def list_workspaces(self) -> List[Dict[str, str]]:
        """列出所有工作区"""
        if not os.path.exists(self.workspace_root):
            return []

        workspaces = []
        for name in os.listdir(self.workspace_root):
            path = os.path.join(self.workspace_root, name)
            if os.path.isdir(path):
                meta_path = os.path.join(path, "metadata.json")
                metadata = {}
                if os.path.exists(meta_path):
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)

                workspaces.append({
                    "id": name,
                    "path": path,
                    "created_at": metadata.get("created_at", ""),
                    "timestamp": metadata.get("timestamp", name.replace("analysis_", ""))
                })

        return sorted(workspaces, key=lambda x: x["timestamp"], reverse=True)


def create_workflow(base_dir: Optional[str] = None) -> AnalysisWorkflow:
    """创建并初始化工作流"""
    wf = AnalysisWorkflow(base_dir)
    wf.create_workspace()
    return wf


def resume_workflow(analysis_id: str, base_dir: Optional[str] = None) -> Optional[AnalysisWorkflow]:
    """
    恢复已有工作流（断点续传）

    Args:
        analysis_id: 分析ID，如 "analysis_20260308_143022"
        base_dir: 项目根目录

    Returns:
        AnalysisWorkflow 实例，不存在返回 None
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.path.dirname(base_dir)

    workspace = os.path.join(base_dir, "workspace", analysis_id)
    if not os.path.exists(workspace):
        return None

    wf = AnalysisWorkflow(base_dir)
    wf.analysis_id = analysis_id
    wf.workspace = workspace

    wf.load_context()

    return wf
