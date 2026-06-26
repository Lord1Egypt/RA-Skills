"""EMR on EKS management modules.

Provides high-level clients for managing EMR on EKS resources:

- :class:`EMRVirtualClusterManager`: Virtual cluster CRUD operations.
- :class:`EMRContainersJobRunManager`: Job run submission and lifecycle management.
"""

from scripts.on_eks.job_runs import EMRContainersJobRunManager
from scripts.on_eks.virtual_clusters import EMRVirtualClusterManager

__all__ = [
    "EMRContainersJobRunManager",
    "EMRVirtualClusterManager",
]
