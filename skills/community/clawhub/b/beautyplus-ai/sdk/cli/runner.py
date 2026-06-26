"""Task runner for BeautyPlus AI SDK CLI."""

from typing import Callable, Dict, Optional

from sdk.core.client import SkillClient


class TaskRunner:
    """Unified task runner for CLI operations."""

    def __init__(
        self,
        client: Optional[SkillClient] = None,
        ak: Optional[str] = None,
        sk: Optional[str] = None,
        region: str = "cn-north-4",
    ):
        """
        Initialize task runner.

        :param client: Existing SkillClient instance
        :param ak: Access Key (if client not provided)
        :param sk: Secret Key (if client not provided)
        :param region: API region
        """
        if client:
            self.client = client
        else:
            self.client = SkillClient(ak=ak, sk=sk, region=region)

    def run(
        self,
        task_name: str,
        input_src: str,
        params: Optional[Dict] = None,
        on_async_submitted: Optional[Callable[[str], None]] = None,
    ) -> Dict:
        """
        Run a task.

        :param task_name: Task preset name
        :param input_src: Input file path or URL
        :param params: Optional task parameters
        :param on_async_submitted: Callback for async submission
        :return: Task result
        """
        return self.client.run_task(
            task_name=task_name,
            image_path=input_src,
            params=params,
            on_async_submitted=on_async_submitted,
        )

    def resume(self, task_id: str) -> Dict:
        """
        Resume polling for an existing task.

        :param task_id: Task ID to resume
        :return: Task result
        """
        return self.client.poll_task_status(task_id)
