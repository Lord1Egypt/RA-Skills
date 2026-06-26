"""EMR On EC2 module.

Exports:
    EMRClusterManager: High-level client for managing EMR clusters on EC2.
    EMRStepManager: High-level client for managing EMR steps on EC2 clusters.
"""

from scripts.on_ec2.clusters import EMRClusterManager
from scripts.on_ec2.steps import EMRStepManager

__all__ = [
    "EMRClusterManager",
    "EMRStepManager",
]
