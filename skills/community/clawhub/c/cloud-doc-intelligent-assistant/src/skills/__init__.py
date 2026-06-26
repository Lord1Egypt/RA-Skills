"""Skills 包 - DocAssistant facade"""

from .runtime import SkillRuntime
from .fetch_doc_skill import FetchDocSkill
from .check_changes_skill import CheckChangesSkill
from .compare_docs_skill import CompareDocsSkill
from .summarize_diff_skill import SummarizeDiffSkill
from .run_monitor_skill import RunMonitorSkill


class DocAssistant:
    """统一入口，暴露 5 个 skill

    Args:
        config_path: 配置文件路径
    """

    def __init__(self, config_path: str = "config.yaml", **kwargs):
        self._runtime = SkillRuntime(config_path)
        self._fetch_doc = FetchDocSkill(self._runtime)
        self._check_changes = CheckChangesSkill(self._runtime)
        self._compare_docs = CompareDocsSkill(self._runtime)
        self._summarize_diff = SummarizeDiffSkill(self._runtime)
        self._run_monitor = RunMonitorSkill(self._runtime)

    def fetch_doc(self, **kwargs):
        return self._fetch_doc.run(**kwargs)

    def check_changes(self, **kwargs):
        return self._check_changes.run(**kwargs)

    def compare_docs(self, **kwargs):
        return self._compare_docs.run(**kwargs)

    def summarize_diff(self, **kwargs):
        return self._summarize_diff.run(**kwargs)

    def run_monitor(self, **kwargs):
        return self._run_monitor.run(**kwargs)


__all__ = ["DocAssistant", "SkillRuntime"]
